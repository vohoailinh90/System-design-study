#!/usr/bin/env python3
"""Write the architect's handoff files (request/spec/tasks/acceptance) for one batch into team/<batch>/.

    python3 scripts/make_batch_spec.py F1 --repo git@github.com:OWNER/REPO.git
Copy team/F1/* to /srv/team/work/F1/ after `team new F1 --repo ...`, then `team check-spec F1`.
The files avoid the placeholder marker `team check-spec` rejects, and stay under its 120-line spec limit.
"""
import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def topics_of(batch: str) -> list[dict]:
    data = json.loads((ROOT / "catalog" / "api-web-development.json").read_text(encoding="utf-8"))
    return [t for t in data["topics"] if t.get("batch") == batch]


def render(batch: str, repo: str) -> dict[str, str]:
    topics = topics_of(batch)
    if not topics:
        raise SystemExit(f"no topics with batch {batch!r} in the catalog")
    ids = [t["id"] for t in topics]
    id_list = ",".join(ids)
    test_file = f"tests/test_batch_{batch}.py"
    request = f"""# Request {batch}

Repo: {repo} (base `main`)
Sensitivity: public (every source is public; the repository is private only because of the source licence; no secrets)

## What should change
Write {len(ids)} Vietnamese explainer articles ({', '.join(ids)}) for readers with no software background, as defined in STYLEGUIDE.md.

## Why / who uses it
The owner learns system design from them. Later a script may turn them into Facebook posts; do not write posts now.

## Constraints and known decisions
Original images are embedded by URL only. No new dependencies; Python standard library only.
"""
    topic_lines = []
    for t in topics:
        topic_lines += [
            f"- {t['id']} \"{t['title_plain']}\" (source {t['source_path']})",
            f"  - analogy: {t['analogy']}; terms that must appear: {', '.join(t['terms'])}",
            f"  - facts to convey: {'; '.join(t['facts'])}",
            f"  - watch out: {t['watch_out']}",
        ]
    spec = "\n".join([
        f"# Spec {batch}", "",
        "## Goal",
        f"Add articles/{ids[0]}.md .. articles/{ids[-1]}.md ({id_list}), each passing `python3 scripts/check_articles.py --ids <id>`.", "",
        "## Non-goals",
        "No Facebook or social text. No changes to the validator, catalog, STYLEGUIDE.md or other articles. No images stored in git.", "",
        "## Changes by file",
        *[f"- articles/{i}.md: new; follow STYLEGUIDE.md and copy the structure of articles/sd-01-001.md (the pilot)." for i in ids],
        f"- {test_file}: new, written by the tester role only (see below).", "",
        "## Data contracts and interfaces",
        "Front matter: id, title (the catalog `title_plain`), hook (20-140 chars, one line, no URL), source_path and source_commit copied from the catalog, status: draft.",
        "Image URLs, source_path and source_commit come from catalog/api-web-development.json for the same id; copy them exactly.",
        f"Tester role: write {test_file} (unittest, stdlib). For each id in {ids}: assert articles/<id>.md exists and that",
        "`check_articles.check_article(path, check_articles.load_catalog(ROOT))` returns an empty list (import it from scripts/).", "",
        "## Topics (architect's briefing: the only facts you may use)",
        *topic_lines, "",
        "## Invariants",
        "The pilot article, the validator and its tests keep passing. Each article is original wording, Vietnamese, 450-1500 words.", "",
        "## Security and data notes",
        "Links are limited to the image URLs, the pinned source link and the CC link (the validator enforces it). Never copy binary images.", "",
        "## Risks and open points",
        "The models cannot see the diagrams: they describe only what the catalog facts say. The audit must compare each article with its original image.",
        "Source licence is CC BY-NC-ND 4.0: nothing here is cleared for publication.",
    ]) + "\n"
    tasks = "# Tasks " + batch + "\n\n" + "\n".join(
        f"## T{n}: write {t['id']}\nFiles: articles/{t['id']}.md\nDo not touch: catalog/, scripts/, tests/, STYLEGUIDE.md, every other article\n"
        f"Verify: python3 scripts/check_articles.py --ids {t['id']}\n" for n, t in enumerate(topics, 1))
    acceptance = f"""# Acceptance {batch}

```bash
python3 scripts/check_articles.py --ids {id_list}
python3 -m unittest discover -s tests -p "test_batch_{batch}.py"
python3 -m unittest discover -s tests -p "test_check_articles.py"
```
"""
    return {"request.md": request, "spec.md": spec, "tasks.md": tasks, "acceptance.md": acceptance}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("batch", help="F1, F2, ... as set in the catalog")
    parser.add_argument("--repo", default="git@github.com:vohoailinh90/System-design-study.git")
    args = parser.parse_args()
    out = ROOT / "team" / args.batch
    out.mkdir(parents=True, exist_ok=True)
    for name, text in render(args.batch, args.repo).items():
        (out / name).write_text(text, encoding="utf-8")
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
