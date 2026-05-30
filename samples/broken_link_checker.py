#!/usr/bin/env python3
"""
Simple website link checker for small business website audits.

Usage:
  python3 broken_link_checker.py https://example.com report.csv

Scope:
  - checks links on one page only
  - ignores mailto:, tel:, javascript:, and anchor-only links
  - writes URL, status, and error columns
"""

import csv
import sys
from html.parser import HTMLParser
from typing import Optional
from urllib.parse import quote, urljoin, urldefrag, urlparse, urlsplit, urlunsplit
from urllib.request import Request, urlopen


class LinkParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.links: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, Optional[str]]]) -> None:
        if tag.lower() != "a":
            return
        for key, value in attrs:
            if key.lower() == "href" and value:
                self.links.append(value)


def fetch(url: str, timeout: int = 15) -> tuple[Optional[int], str]:
    try:
        req = Request(encode_url(url), headers={"User-Agent": "Mozilla/5.0 link-checker"})
        with urlopen(req, timeout=timeout) as response:
            return response.status, ""
    except Exception as exc:
        return None, str(exc)


def collect_links(page_url: str) -> list[str]:
    status, error = fetch(page_url)
    if status is None:
        raise RuntimeError(f"Could not open page: {error}")

    req = Request(encode_url(page_url), headers={"User-Agent": "Mozilla/5.0 link-checker"})
    with urlopen(req, timeout=15) as response:
        html = response.read().decode("utf-8", errors="ignore")

    parser = LinkParser()
    parser.feed(html)

    links = []
    for href in parser.links:
        if href.startswith(("#", "mailto:", "tel:", "javascript:")):
            continue
        absolute = urldefrag(urljoin(page_url, href))[0]
        parsed = urlparse(absolute)
        if parsed.scheme in {"http", "https"}:
            links.append(absolute)
    return sorted(set(links))


def encode_url(url: str) -> str:
    parts = urlsplit(url)
    path = quote(parts.path, safe="/%")
    query = quote(parts.query, safe="=&?/%")
    return urlunsplit((parts.scheme, parts.netloc, path, query, parts.fragment))


def main() -> int:
    if len(sys.argv) != 3:
        print("Usage: python3 broken_link_checker.py https://example.com report.csv", file=sys.stderr)
        return 2

    page_url = sys.argv[1]
    output_path = sys.argv[2]
    links = collect_links(page_url)

    with open(output_path, "w", newline="", encoding="utf-8") as target:
        writer = csv.DictWriter(target, fieldnames=["url", "status", "error"])
        writer.writeheader()
        for link in links:
            status, error = fetch(link)
            writer.writerow({"url": link, "status": status or "", "error": error})

    print(f"Checked {len(links)} links -> {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
