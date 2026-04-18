#!/usr/bin/env python3
"""Download the CUDA Programming Guide and in-scope linked files."""

from __future__ import annotations

import argparse
import re
import sys
from collections import deque
from pathlib import Path
from typing import Iterable
from urllib.parse import urljoin, urlsplit, urlunsplit

import requests
from bs4 import BeautifulSoup
from requests import Response, Session
from requests.adapters import HTTPAdapter
from urllib3.util import Retry


DEFAULT_BASE_URL = "https://docs.nvidia.com/cuda/cuda-programming-guide/"
DEFAULT_OUTPUT_DIR = "docs/cuda-programming-guide"
DEFAULT_TIMEOUT = 30.0
DEFAULT_USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:149.0) "
    "Gecko/20100101 Firefox/149.0"
)
STYLE_URL_RE = re.compile(r"url\((['\"]?)(.*?)\1\)")
META_REFRESH_RE = re.compile(r"url=(.+)", re.IGNORECASE)


def build_session(user_agent: str) -> Session:
    retry = Retry(
        total=5,
        backoff_factor=1.0,
        status_forcelist=(429, 500, 502, 503, 504),
        allowed_methods=frozenset({"GET"}),
    )
    adapter = HTTPAdapter(max_retries=retry)

    session = requests.Session()
    session.headers.update({"User-Agent": user_agent})
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session


class Downloader:
    def __init__(
        self,
        base_url: str,
        output_dir: Path,
        timeout: float,
        user_agent: str,
        max_files: int | None,
    ) -> None:
        self.base_url = self.normalize_base_url(base_url)
        split = urlsplit(self.base_url)
        self.base_scheme = split.scheme
        self.base_netloc = split.netloc
        self.base_path = split.path
        self.output_dir = output_dir
        self.timeout = timeout
        self.max_files = max_files
        self.session = build_session(user_agent)
        self.pending: deque[str] = deque()
        self.seen: set[str] = set()
        self.downloaded = 0
        self.missing = 0
        self.failed: list[tuple[str, str]] = []

    @staticmethod
    def normalize_base_url(base_url: str) -> str:
        split = urlsplit(base_url)
        path = split.path or "/"
        if not path.endswith("/"):
            path = f"{path}/"
        return urlunsplit((split.scheme.lower(), split.netloc.lower(), path, "", ""))

    def canonicalize(self, raw_url: str, current_url: str | None = None) -> str | None:
        if not raw_url:
            return None

        candidate = raw_url.strip()
        if not candidate:
            return None

        lowered = candidate.lower()
        if lowered.startswith(("javascript:", "mailto:", "tel:", "data:")):
            return None

        absolute = urljoin(current_url or self.base_url, candidate)
        split = urlsplit(absolute)
        if split.scheme.lower() not in {"http", "https"}:
            return None

        path = split.path or "/"
        if path.endswith("/"):
            path = f"{path}index.html"

        canonical = urlunsplit(
            (split.scheme.lower(), split.netloc.lower(), path, "", "")
        )
        if split.scheme.lower() != self.base_scheme or split.netloc.lower() != self.base_netloc:
            return None
        if not path.startswith(self.base_path):
            return None
        return canonical

    def enqueue(self, raw_url: str, current_url: str | None = None) -> None:
        canonical = self.canonicalize(raw_url, current_url=current_url)
        if canonical is None or canonical in self.seen:
            return
        self.seen.add(canonical)
        self.pending.append(canonical)

    def response_is_html(self, url: str, response: Response) -> bool:
        content_type = response.headers.get("Content-Type", "").lower()
        return "text/html" in content_type or url.endswith(".html")

    def relative_path_for(self, url: str) -> Path:
        split = urlsplit(url)
        relative_path = split.path.removeprefix(self.base_path).lstrip("/")
        if not relative_path:
            relative_path = "index.html"
        return Path(relative_path)

    def save(self, url: str, content: bytes) -> Path:
        target = self.output_dir / self.relative_path_for(url)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(content)
        return target

    def extract_links(self, current_url: str, html: bytes) -> Iterable[str]:
        soup = BeautifulSoup(html, "html.parser")
        base_tag = soup.find("base", href=True)
        page_base = urljoin(current_url, base_tag["href"]) if base_tag else current_url

        for tag in soup.find_all(True):
            for attr in ("href", "src", "data", "poster"):
                value = tag.get(attr)
                if isinstance(value, str):
                    yield urljoin(page_base, value)

            srcset = tag.get("srcset")
            if isinstance(srcset, str):
                for item in srcset.split(","):
                    candidate = item.strip().split(" ", 1)[0]
                    if candidate:
                        yield urljoin(page_base, candidate)

            style = tag.get("style")
            if isinstance(style, str):
                for candidate in self.extract_style_urls(style):
                    yield urljoin(page_base, candidate)

            if tag.name == "meta":
                http_equiv = tag.get("http-equiv")
                content = tag.get("content")
                if (
                    isinstance(http_equiv, str)
                    and http_equiv.lower() == "refresh"
                    and isinstance(content, str)
                ):
                    match = META_REFRESH_RE.search(content)
                    if match:
                        yield urljoin(page_base, match.group(1).strip())

        for style_tag in soup.find_all("style"):
            text = style_tag.string or style_tag.get_text()
            if text:
                for candidate in self.extract_style_urls(text):
                    yield urljoin(page_base, candidate)

        for raw_link in self._iter_generated_links(soup):
            yield urljoin(page_base, raw_link)

    @staticmethod
    def extract_style_urls(text: str) -> Iterable[str]:
        for match in STYLE_URL_RE.finditer(text):
            candidate = match.group(2).strip()
            if candidate:
                yield candidate

    @staticmethod
    def _iter_generated_links(soup: BeautifulSoup) -> Iterable[str]:
        manifest = soup.find("link", rel=lambda value: value and "manifest" in value)
        if manifest and manifest.get("href"):
            yield manifest["href"]

        preloads = soup.find_all("link", rel=lambda value: value and "preload" in value)
        for preload in preloads:
            href = preload.get("href")
            if isinstance(href, str):
                yield href

        for canonical in soup.find_all("link", rel=lambda value: value and "canonical" in value):
            href = canonical.get("href")
            if isinstance(href, str):
                yield href

    def enqueue_markdown_sidecar(self, html_url: str) -> None:
        if not html_url.endswith(".html"):
            return
        self.enqueue(f"{html_url}.md")

    def fetch(self, url: str) -> Response | None:
        try:
            response = self.session.get(url, timeout=self.timeout)
        except requests.RequestException as exc:
            self.failed.append((url, str(exc)))
            print(f"ERROR {url} -> {exc}", file=sys.stderr)
            return None

        if response.status_code == 404:
            self.missing += 1
            print(f"MISS  {url}")
            return None

        try:
            response.raise_for_status()
        except requests.HTTPError as exc:
            self.failed.append((url, str(exc)))
            print(f"ERROR {url} -> {exc}", file=sys.stderr)
            return None

        return response

    def crawl(self) -> int:
        self.enqueue(self.base_url)

        while self.pending:
            if self.max_files is not None and self.downloaded >= self.max_files:
                print(f"Reached --max-files={self.max_files}, stopping early.")
                break

            url = self.pending.popleft()
            response = self.fetch(url)
            if response is None:
                continue

            target = self.save(url, response.content)
            self.downloaded += 1
            print(f"SAVED {url} -> {target}")

            if not self.response_is_html(url, response):
                continue

            self.enqueue_markdown_sidecar(url)
            for raw_link in self.extract_links(url, response.content):
                self.enqueue(raw_link, current_url=url)

        print(
            f"Done. downloaded={self.downloaded} missing={self.missing} "
            f"failed={len(self.failed)} queued={len(self.seen)}"
        )
        return 0 if not self.failed else 1


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Recursively download files linked from the CUDA Programming Guide. "
            "For every HTML page, also try to fetch the matching .html.md file."
        )
    )
    parser.add_argument(
        "--base-url",
        default=DEFAULT_BASE_URL,
        help=f"Docs root to crawl. Default: {DEFAULT_BASE_URL}",
    )
    parser.add_argument(
        "--output-dir",
        default=DEFAULT_OUTPUT_DIR,
        help=f"Directory used to store downloaded files. Default: {DEFAULT_OUTPUT_DIR}",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=DEFAULT_TIMEOUT,
        help=f"Per-request timeout in seconds. Default: {DEFAULT_TIMEOUT}",
    )
    parser.add_argument(
        "--user-agent",
        default=DEFAULT_USER_AGENT,
        help="HTTP user agent sent with requests.",
    )
    parser.add_argument(
        "--max-files",
        type=int,
        default=None,
        help="Stop after saving this many files. Useful for smoke tests.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    downloader = Downloader(
        base_url=args.base_url,
        output_dir=Path(args.output_dir),
        timeout=args.timeout,
        user_agent=args.user_agent,
        max_files=args.max_files,
    )
    return downloader.crawl()


if __name__ == "__main__":
    raise SystemExit(main())
