#!/usr/bin/env python3
"""Upload gitignored gallery blobs to Backblaze B2 and patch site.yaml preview URLs."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import boto3
import yaml
from botocore.exceptions import ClientError
from dotenv import load_dotenv

try:
    from PIL import Image
except ImportError:  # pragma: no cover
    Image = None  # type: ignore

REPO_ROOT = Path(__file__).resolve().parent.parent
SITES_ROOT = REPO_ROOT / "sites"
FORMAT_PREFERENCE = ["svg", "png", "jpg", "jpeg"]
THUMB_SIZE = (640, 360)
SCREEN_BASENAME = re.compile(r"^screen\d{2}$")


def load_env() -> dict[str, str]:
    env_path = REPO_ROOT / ".env"
    if not env_path.is_file():
        print(
            "error: .env not found — copy .env.example to .env and fill B2 credentials",
            file=sys.stderr,
        )
        sys.exit(1)
    load_dotenv(env_path)
    import os

    keys = [
        "B2_APPLICATION_KEY_ID",
        "B2_APPLICATION_KEY",
        "B2_BUCKET_NAME",
        "B2_S3_ENDPOINT",
        "B2_PUBLIC_BASE_URL",
    ]
    cfg = {k: (os.environ.get(k) or "").strip() for k in keys}
    cfg["B2_PATH_PREFIX"] = (os.environ.get("B2_PATH_PREFIX") or "").strip().strip("/")
    endpoint = cfg["B2_S3_ENDPOINT"]
    if endpoint and not endpoint.startswith(("http://", "https://")):
        cfg["B2_S3_ENDPOINT"] = f"https://{endpoint}"
    missing = [k for k in keys if not cfg[k]]
    if missing:
        print(f"error: missing required .env variables: {', '.join(missing)}", file=sys.stderr)
        sys.exit(1)
    return cfg


def resolve_basename_files(site_dir: Path) -> dict[str, Path]:
    """Map logical basename (thumb, screen01, …) to winning local file."""
    by_basename: dict[str, list[tuple[int, Path]]] = {}
    for path in site_dir.iterdir():
        if not path.is_file():
            continue
        stem, ext = path.stem, path.suffix.lstrip(".").lower()
        if ext not in FORMAT_PREFERENCE:
            continue
        if stem != "thumb" and not SCREEN_BASENAME.match(stem):
            continue
        rank = FORMAT_PREFERENCE.index(ext)
        by_basename.setdefault(stem, []).append((rank, path))
    resolved: dict[str, Path] = {}
    for stem, candidates in by_basename.items():
        candidates.sort(key=lambda x: x[0])
        resolved[stem] = candidates[0][1]
    return resolved


def validate_thumb(path: Path) -> None:
    ext = path.suffix.lstrip(".").lower()
    if ext == "svg":
        text = path.read_text(encoding="utf-8", errors="replace")
        if 'width="640"' not in text and "width='640'" not in text:
            print(f"warn: {path.name}: SVG should set width=\"640\" height=\"360\"", file=sys.stderr)
        return
    if Image is None:
        return
    with Image.open(path) as img:
        if img.size != THUMB_SIZE:
            print(
                f"error: {path.name}: thumbnail must be {THUMB_SIZE[0]}x{THUMB_SIZE[1]}, got {img.size[0]}x{img.size[1]}",
                file=sys.stderr,
            )
            sys.exit(1)


def load_site_yaml(site_dir: Path) -> tuple[dict, Path]:
    manifest = site_dir / "site.yaml"
    if not manifest.is_file():
        print(f"error: missing {manifest}", file=sys.stderr)
        sys.exit(1)
    with manifest.open(encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    return data, manifest


def verify_slug_category(site_dir: Path, data: dict) -> tuple[str, str]:
    parts = site_dir.relative_to(SITES_ROOT).parts
    if len(parts) != 2:
        print(f"error: expected sites/<category>/<slug>/, got {site_dir}", file=sys.stderr)
        sys.exit(1)
    cat_dir, slug_dir = parts
    category = str(data.get("category", ""))
    slug = str(data.get("slug", ""))
    if category != cat_dir or slug != slug_dir:
        print(
            f"error: site.yaml category/slug ({category}/{slug}) "
            f"do not match path ({cat_dir}/{slug_dir})",
            file=sys.stderr,
        )
        sys.exit(1)
    return category, slug


def public_url(cfg: dict, category: str, slug: str, filename: str) -> str:
    base = cfg["B2_PUBLIC_BASE_URL"].rstrip("/")
    return f"{base}/{object_key(cfg, category, slug, filename)}"


def object_key(cfg: dict, category: str, slug: str, filename: str) -> str:
    key = f"{category}/{slug}/{filename}"
    prefix = cfg.get("B2_PATH_PREFIX") or ""
    if prefix:
        return f"{prefix}/{key}"
    return key


def content_type(path: Path) -> str:
    ext = path.suffix.lstrip(".").lower()
    return {
        "svg": "image/svg+xml",
        "png": "image/png",
        "jpg": "image/jpeg",
        "jpeg": "image/jpeg",
    }.get(ext, "application/octet-stream")


def upload_file(s3, cfg: dict, local: Path, key: str, dry_run: bool) -> None:
    if dry_run:
        print(f"  dry-run upload: {local.name} -> s3://{cfg['B2_BUCKET_NAME']}/{key}")
        return
    try:
        s3.upload_file(
            str(local),
            cfg["B2_BUCKET_NAME"],
            key,
            ExtraArgs={"ContentType": content_type(local)},
        )
        print(f"  uploaded: {local.name} -> {key}")
    except ClientError as exc:
        print(f"error: upload failed for {local}: {exc}", file=sys.stderr)
        sys.exit(1)


def patch_site_yaml(
    data: dict,
    thumb_url: str | None,
    screen_urls: list[str],
) -> dict:
    preview = data.setdefault("preview", {})
    if thumb_url:
        preview["thumbUrl"] = thumb_url
    if screen_urls:
        preview["screens"] = screen_urls
    elif "screens" in preview:
        del preview["screens"]
    if "imageUrl" in preview:
        del preview["imageUrl"]
    return data


def dump_site_yaml(path: Path, data: dict) -> None:
    with path.open("w", encoding="utf-8") as f:
        yaml.dump(
            data,
            f,
            default_flow_style=False,
            sort_keys=False,
            allow_unicode=True,
        )


def process_site(site_dir: Path, cfg: dict, dry_run: bool) -> None:
    site_dir = site_dir.resolve()
    print(f"\n{site_dir.relative_to(REPO_ROOT)}")

    data, manifest_path = load_site_yaml(site_dir)
    category, slug = verify_slug_category(site_dir, data)
    files = resolve_basename_files(site_dir)

    if "thumb" not in files:
        print("error: no local thumb.{svg,png,jpg,jpeg} at site root", file=sys.stderr)
        sys.exit(1)

    validate_thumb(files["thumb"])

    s3 = None
    if not dry_run:
        s3 = boto3.client(
            "s3",
            endpoint_url=cfg["B2_S3_ENDPOINT"],
            aws_access_key_id=cfg["B2_APPLICATION_KEY_ID"],
            aws_secret_access_key=cfg["B2_APPLICATION_KEY"],
        )

    thumb_path = files["thumb"]
    thumb_name = thumb_path.name
    upload_file(
        s3,
        cfg,
        thumb_path,
        object_key(cfg, category, slug, thumb_name),
        dry_run,
    )
    thumb_url = public_url(cfg, category, slug, thumb_name)

    screen_urls: list[str] = []
    for stem in sorted(k for k in files if SCREEN_BASENAME.match(k)):
        path = files[stem]
        upload_file(
            s3,
            cfg,
            path,
            object_key(cfg, category, slug, path.name),
            dry_run,
        )
        screen_urls.append(public_url(cfg, category, slug, path.name))

    updated = patch_site_yaml(data, thumb_url, screen_urls)
    print(f"  thumbUrl: {thumb_url}")
    for url in screen_urls:
        print(f"  screen:   {url}")

    if dry_run:
        print("  dry-run: site.yaml not written")
        return

    dump_site_yaml(manifest_path, updated)
    print(f"  updated: {manifest_path.relative_to(REPO_ROOT)}")


def discover_sites(site_arg: Path | None) -> list[Path]:
    if site_arg:
        site = site_arg.resolve()
        if not site.is_dir():
            print(f"error: not a directory: {site}", file=sys.stderr)
            sys.exit(1)
        return [site]

    sites: list[Path] = []
    if not SITES_ROOT.is_dir():
        return sites
    for cat in sorted(SITES_ROOT.iterdir()):
        if not cat.is_dir() or cat.name.startswith("."):
            continue
        for slug in sorted(cat.iterdir()):
            if not slug.is_dir() or slug.name.startswith("."):
                continue
            if resolve_basename_files(slug):
                sites.append(slug)
    return sites


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Publish gitignored gallery assets to B2 and patch site.yaml",
    )
    parser.add_argument(
        "--site",
        type=Path,
        help="Single template path (e.g. sites/_base/_default)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show uploads and URLs without S3 writes or site.yaml changes",
    )
    args = parser.parse_args()

    cfg = load_env()
    targets = discover_sites(args.site)
    if not targets:
        print("no sites with local thumb.* or screenNN.* files found", file=sys.stderr)
        sys.exit(1)

    for site_dir in targets:
        process_site(site_dir, cfg, args.dry_run)

    print("\ndone")


if __name__ == "__main__":
    main()
