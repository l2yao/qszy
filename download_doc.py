#!/usr/bin/env python3
"""Download DOC files from a numbered range with a/b suffixes.

Example:
    python download_doc.py --start 1 --end 22 --output downloaded

This downloads files like:
    https://v.xwcz.org/CHT/14/14-004/14-004-0001a.doc
    https://v.xwcz.org/CHT/14/14-004/14-004-0001b.doc
"""

from __future__ import annotations

import argparse
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

BASE_URL_CHT = "https://v.xwcz.org/CHT/14/14-004"
BASE_URL_CHS = "https://v.xwcz.org/CHS/14/14-004"
FILENAME_TEMPLATE = "14-004-{number:04d}{suffix}.doc"
SUFFIXES = ["a", "b"]


def download_file(url: str, dest: Path, timeout: int = 30) -> bool:
    request = Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urlopen(request, timeout=timeout) as response, open(dest, "wb") as out_file:
            out_file.write(response.read())
        return True
    except HTTPError as exc:
        print(f"HTTP error {exc.code} for {url}")
    except URLError as exc:
        print(f"URL error for {url}: {exc.reason}")
    except OSError as exc:
        print(f"Failed writing {dest}: {exc}")
    return False


def build_urls(start: int, end: int, use_suffixes: bool, base_url: str) -> list[tuple[str, str]]:
    urls: list[tuple[str, str]] = []
    for index in range(start, end + 1):
        if use_suffixes:
            for suffix in SUFFIXES:
                filename = FILENAME_TEMPLATE.format(number=index, suffix=suffix)
                url = f"{base_url}/{filename}"
                urls.append((url, filename))
        else:
            filename = FILENAME_TEMPLATE.format(number=index, suffix="")
            url = f"{base_url}/{filename}"
            urls.append((url, filename))
    return urls


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Download DOC files in numeric range with a/b suffixes from v.xwcz.org",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("--start", type=int, default=1, help="Starting numeric index")
    parser.add_argument("--end", type=int, default=22, help="Ending numeric index")
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("downloads"),
        help="Output directory for downloaded DOCs",
    )
    parser.add_argument(
        "--lang",
        choices=["cht", "chs"],
        default="cht",
        help="Choose traditional (CHT) or simplified (CHS) text archive",
    )
    parser.add_argument(
        "--skip-existing",
        action="store_true",
        help="Skip files that already exist locally",
    )
    parser.add_argument(
        "--no-suffix",
        action="store_true",
        help="Download files without a/b suffixes (e.g., 14-004-0010.doc)",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.start < 1 or args.end < args.start:
        print("Error: invalid range. Ensure 1 <= start <= end.")
        return 1

    base_url = BASE_URL_CHT if args.lang == "cht" else BASE_URL_CHS
    output_dir = args.output
    output_dir.mkdir(parents=True, exist_ok=True)

    urls = build_urls(args.start, args.end, not args.no_suffix, base_url)
    print(f"Downloading {len(urls)} files to {output_dir} using {args.lang.upper()} URL base")

    success_count = 0
    for url, filename in urls:
        dest = output_dir / filename
        if args.skip_existing and dest.exists():
            print(f"Skipping existing {filename}")
            success_count += 1
            continue

        print(f"Downloading {filename}...")
        if download_file(url, dest):
            success_count += 1
        else:
            print(f"Failed: {url}")

    print(f"Finished. {success_count}/{len(urls)} files downloaded or skipped.")
    return 0 if success_count == len(urls) else 2


if __name__ == "__main__":
    raise SystemExit(main())
