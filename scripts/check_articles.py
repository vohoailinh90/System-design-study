#!/usr/bin/env python3
"""Deterministic gate for the Vietnamese explainer articles (stdlib only).

Everything here is computable, so no model is asked to judge it. What it cannot see
(is the explanation correct? is the analogy apt?) is left to the audit step.

    python3 scripts/check_articles.py --all
    python3 scripts/check_articles.py --ids sd-01-002,sd-01-003   # also fails if a file is missing
    python3 scripts/check_articles.py articles/sd-01-001.md
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import unicodedata
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent.parent
MIN_WORDS, MAX_WORDS = 450, 1500
MIN_EMOJI = 10
HOOK_MIN, HOOK_MAX = 20, 140  # the one-line opener; a later social post starts from it
MIN_VI_RATIO = 0.12  # share of letters that carry a Vietnamese diacritic (or đ)
ALLOWED_HOSTS = {"github.com", "assets.bytebytego.com", "bytebytego.com", "creativecommons.org"}
BINARY_IMAGES = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".avif", ".bmp", ".ico"}
SOURCE_REPO = "https://github.com/ByteByteGoHq/system-design-101"
FRONT_KEYS = ("id", "title", "hook", "source_path", "source_commit", "status")
STATUSES = {"draft", "review", "done"}
# (key, regex on the lowercased heading text): the `## ` sections, in this order.
# "image" (a prompt for an AI image tool) is optional; every other section is required.
SECTIONS = [
    ("summary", r"tóm tắt"), ("analogy", r"đời thường"), ("walkthrough", r"đọc hình"),
    ("choose", r"khi nào"), ("glossary", r"từ khó"), ("quiz", r"thử trả lời"),
    ("image", r"minh họa"), ("sources", r"nguồn"),
]
OPTIONAL = {"image"}
URL_RE = re.compile(r"https?://[^\s)>\]\"'`]+")
IMG_RE = re.compile(r"!\[([^\]]*)\]\(([^)\s]+)\)")
GLOSSARY_RE = re.compile(r"(?m)^[-*] \*\*[^*]+\*\* ?(?:—|-|:) ?\S.{8,}")
BANNED = ("TODO", "lorem", "<think>", "as an ai", "```")


def is_emoji(ch: str) -> bool:
    cp = ord(ch)
    return 0x1F000 <= cp <= 0x1FAFF or 0x2600 <= cp <= 0x27BF or cp in (0x2B50, 0x2B55, 0x2B06, 0x2B07)


def emoji_count(text: str) -> int:
    return sum(1 for ch in text if is_emoji(ch))


def vietnamese_ratio(text: str) -> float:
    letters = marked = 0
    for ch in text:
        if not ch.isalpha():
            continue
        letters += 1
        if ch in "đĐ" or any(unicodedata.combining(c) for c in unicodedata.normalize("NFD", ch)):
            marked += 1
    return marked / letters if letters else 0.0


def split_front_matter(text: str) -> tuple[dict[str, str], str]:
    match = re.match(r"---\n(.*?)\n---\n", text, re.S)
    if not match:
        return {}, text
    meta = {}
    for line in match.group(1).splitlines():
        key, sep, value = line.partition(":")
        if sep:
            meta[key.strip()] = value.strip()
    return meta, text[match.end():]


def split_sections(body: str) -> tuple[list[tuple[str, str]], list[str]]:
    """Returns ([(heading, content)], problems) for every `## ` section."""
    parts = re.split(r"(?m)^## ", body)[1:]
    sections = []
    for part in parts:
        heading, _, content = part.partition("\n")
        sections.append((heading.strip(), content.strip()))
    return sections, []


def load_catalog(root: Path) -> dict[str, dict]:
    topics: dict[str, dict] = {}
    for path in sorted((root / "catalog").glob("*.json")):
        for topic in json.loads(path.read_text(encoding="utf-8"))["topics"]:
            topics[topic["id"]] = topic
    return topics


def check_article(path: Path, catalog: dict[str, dict]) -> list[str]:
    errors: list[str] = []
    if not path.is_file():
        return ["file is missing"]
    text = path.read_text(encoding="utf-8")
    meta, body = split_front_matter(text)
    for key in FRONT_KEYS:
        if not meta.get(key):
            errors.append(f"front matter: '{key}' is missing or empty")
    if meta.get("status") and meta["status"] not in STATUSES:
        errors.append(f"front matter: status must be one of {sorted(STATUSES)}")
    topic = catalog.get(path.stem)
    if meta.get("id") != path.stem:
        errors.append(f"front matter: id {meta.get('id')!r} must equal the file name {path.stem!r}")
    if topic is None:
        return errors + [f"{path.stem!r} is not in the catalog"]
    for key in ("source_path", "source_commit"):
        if meta.get(key) != topic[key]:
            errors.append(f"front matter: {key} must be {topic[key]!r}")

    hook = meta.get("hook", "")
    if hook and (not HOOK_MIN <= len(hook) <= HOOK_MAX or "http" in hook.lower()):
        errors.append(f"front matter: hook must be {HOOK_MIN}-{HOOK_MAX} characters, no URL")
    lowered = text.lower()
    for banned in BANNED:
        if banned.lower() in lowered:
            errors.append(f"contains forbidden text {banned!r}")
    h1 = re.findall(r"(?m)^# (.+)$", body)
    if len(h1) != 1:
        errors.append("needs exactly one '# ' title")
    elif not is_emoji(h1[0][0]):
        errors.append("the title must start with an emoji")

    words = len(body.split())
    if not MIN_WORDS <= words <= MAX_WORDS:
        errors.append(f"{words} words; the body must have {MIN_WORDS}-{MAX_WORDS}")
    if emoji_count(body) < MIN_EMOJI:
        errors.append(f"only {emoji_count(body)} emoji; at least {MIN_EMOJI} are required")
    if vietnamese_ratio(body) < MIN_VI_RATIO:
        errors.append("the text does not look Vietnamese (too few letters with diacritics)")

    images = IMG_RE.findall(body)
    if [url for _, url in images] != topic["image_urls"]:
        errors.append(f"images must be exactly the original URLs, in order: {topic['image_urls']}")
    for alt, _ in images:
        if len(alt.strip()) < 30:
            errors.append("every image needs alt text of at least 30 characters describing it")
    for url in URL_RE.findall(body):
        parsed = urlparse(url)
        if parsed.hostname not in ALLOWED_HOSTS:
            errors.append(f"link to a host that is not allowed: {url}")
        elif parsed.hostname == "github.com" and not parsed.path.startswith("/ByteByteGoHq/"):
            errors.append(f"github link outside ByteByteGoHq: {url}")
    prose = URL_RE.sub("", body).lower()  # a term hiding in an image or source URL does not count
    for term in topic.get("terms", []):
        if term.lower() not in prose:
            errors.append(f"required term missing: {term!r}")

    sections, _ = split_sections(body)
    keys = []
    for heading, _content in sections:
        if not is_emoji(heading[:1]):
            errors.append(f"heading does not start with an emoji: {heading!r}")
        for key, pattern in SECTIONS:
            if re.search(pattern, heading.lower()):
                keys.append(key)
                break
    expected = [key for key, _ in SECTIONS if key not in OPTIONAL or key in keys]
    if keys != expected:
        errors.append(f"sections must be exactly, in order: {[k for k, _ in SECTIONS]} (optional: {sorted(OPTIONAL)}); found {keys}")
        return errors
    content = {key: sections[i][1] for i, key in enumerate(keys)}
    errors += check_sections(content, topic)
    return errors


def check_sections(content: dict[str, str], topic: dict) -> list[str]:
    errors: list[str] = []
    if len(re.findall(r"(?m)^[-*] ", content["summary"])) < 3:
        errors.append("summary: needs at least 3 bullets")
    if len(content["analogy"].split()) < 60:
        errors.append("analogy: needs at least 60 words")
    if len(re.findall(r"(?m)^(?:\d+\.|[-*]) ", content["walkthrough"])) < 3:
        errors.append("walkthrough: needs at least 3 numbered or bulleted steps")
    if len(re.findall(r"(?m)^(?:[-*] |\|)", content["choose"])) < 3:
        errors.append("choose: needs at least 3 bullets or table rows")
    if len(GLOSSARY_RE.findall(content["glossary"])) < 3:
        errors.append("glossary: needs at least 3 entries written '- **term** — explanation'")
    quiz = content["quiz"]
    if not ("<details>" in quiz and "<summary>" in quiz and "</details>" in quiz) or "<details open" in quiz:
        errors.append("quiz: the answer must sit in a closed <details><summary> block")
    if "image" in content:
        image = content["image"]
        alt = re.search(r"(?m)^Alt: (.+)$", image)
        prompt = re.search(r"(?m)^Prompt: (.+)$", image)
        if not alt or len(alt.group(1)) < 30:
            errors.append("image section: needs an 'Alt: ' line of at least 30 characters")
        if not prompt or len(prompt.group(1).split()) < 15:
            errors.append("image section: needs a 'Prompt: ' line (English) of at least 15 words")
    sources = content["sources"]
    pinned = f"{SOURCE_REPO}/blob/{topic['source_commit']}/{topic['source_path']}"
    for needle, label in (("ByteByteGo", "ByteByteGo credit"), ("CC BY-NC-ND 4.0", "licence name"), (pinned, "pinned source link")):
        if needle not in sources:
            errors.append(f"sources: missing the {label} ({needle})")
    return errors


def stray_images(root: Path) -> list[str]:
    return [str(p.relative_to(root)) for p in sorted(root.rglob("*"))
            if p.suffix.lower() in BINARY_IMAGES and ".git" not in p.relative_to(root).parts]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("paths", nargs="*", help="article files")
    parser.add_argument("--all", action="store_true", help="every file in articles/")
    parser.add_argument("--ids", help="comma-separated ids; a missing file is an error")
    parser.add_argument("--root", type=Path, default=ROOT)
    args = parser.parse_args(argv)
    root = args.root
    catalog = load_catalog(root)
    targets = [Path(p) for p in args.paths]
    if args.all:
        targets += sorted((root / "articles").glob("*.md"))
    if args.ids:
        targets += [root / "articles" / f"{i.strip()}.md" for i in args.ids.split(",") if i.strip()]
    if not targets:
        parser.error("nothing to check: give paths, --ids or --all")
    failed = 0
    for path in targets:
        for message in check_article(path, catalog):
            print(f"{path}: {message}")
            failed += 1
    for image in stray_images(root):
        print(f"{image}: binary images must not be stored in this repository; embed the original URL")
        failed += 1
    print(f"{len(targets)} article(s) checked, {failed} problem(s)")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
