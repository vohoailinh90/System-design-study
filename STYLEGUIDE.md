# Style guide — explainer articles

Reader: an adult with no software background, learning for themselves. Language: Vietnamese, warm and plain.
Facebook posts come later: do NOT write any now. The `hook` line, the three summary bullets and the quiz question
are the raw material a later script will turn into a post, so keep them short and self-contained.

## Structure
Copy `articles/sd-01-001.md` exactly: front matter (`id`, `title`, `hook`, `source_path`, `source_commit`, `status: draft`),
one `# ` title, a `> ` hook line, the original image(s), a credit line, then the `## ` sections in this order:
Tóm tắt 30 giây · Hiểu bằng chuyện đời thường · Đọc hình từng bước · Khi nào dùng cách nào? · Từ khó, giải nghĩa ·
Thử trả lời · (optional) Gợi ý hình minh họa thêm · Nguồn. Every heading and the title start with an emoji.

## Rules
- Facts come only from the catalog entry (`facts`, `terms`, `analogy`, `watch_out`) and the source article named in `source_path`.
  Convey every item of `facts`; obey `watch_out`; add no numbers, dates or claims of your own.
- Use the catalog `analogy` as the through-line of "Hiểu bằng chuyện đời thường". Pick an everyday image the reader knows.
- First use of a technical word: say what it means in plain Vietnamese right there; the glossary repeats it.
- Original images: embed the exact `image_urls` from the catalog, in order, as `![alt](url)`; alt is >= 30 characters.
  Never download or copy an image into the repository. You cannot see the image: describe what the source text says it shows,
  and never invent colours, shapes or labels.
- Write in your own words. Do not translate sentences of the source. No code blocks, no tables of jargon.
- The only links allowed: the image URL(s), the pinned source link and the CC BY-NC-ND 4.0 link, as in the pilot.
- Quiz: one question, the answer inside a closed `<details><summary>` block.
- Optional image-prompt section: an `Alt:` line (>= 30 characters, Vietnamese) and an English `Prompt:` line (>= 15 words, no text in the picture).
- Length 450-1500 words. `python3 scripts/check_articles.py --ids <id>` is the verdict on all of this; the audit judges what it cannot:
  is the explanation correct, is the analogy apt, does it read easily to a beginner.

## Licence
The source is CC BY-NC-ND 4.0. This repository is private and not for release until the owner has settled the rights.
Every article credits ByteByteGo and links the pinned source.
