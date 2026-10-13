# System Design Study — học System Design bằng tiếng Việt dễ hiểu

Bản giải thích **cho người không chuyên phần mềm** của [ByteByteGo — System Design 101](https://github.com/ByteByteGoHq/system-design-101):
chuyện đời thường trước, thuật ngữ sau, có biểu tượng, có câu hỏi tự kiểm tra. Hình gốc được **nhúng bằng đường dẫn gốc**, không sao chép vào repo.

**Trạng thái: bản nháp riêng tư để tự học, chưa phát hành, chưa đăng Facebook.** Nguồn theo giấy phép CC BY-NC-ND 4.0
(không thương mại, không cải biên); quyền dùng cho việc đăng công khai chưa được giải quyết. Văn bản trong repo tự viết, không dịch sát nguồn.

## Có gì ở đây
- `articles/` — bài học (`sd-01-001` là bài mẫu; các bài khác do team VPS viết theo lô).
- `catalog/api-web-development.json` — 50 chủ đề chương 1 (id `sd-01-NNN`, nguồn ghim commit, URL ảnh gốc). 17 bài đầu có sẵn ý chính, ẩn dụ, thuật ngữ bắt buộc, điểm dễ nói sai và lô: `pilot`, `F1`–`F4`.
- `STYLEGUIDE.md` — quy tắc viết cho model miễn phí và người audit.
- `scripts/check_articles.py` — cổng kiểm tính được: `python3 scripts/check_articles.py --all`. Test: `python3 -m unittest discover -s tests`.
- `scripts/make_batch_spec.py` + `team/F1..F4/` — gói spec/tasks/acceptance (do Claude làm kiến trúc) cho team VPS.

## Chạy một lô bằng team VPS (`docs/vps-team.md` của claude-agent-routing-template)
```bash
team new F1 --repo git@github.com:vohoailinh90/System-design-study.git
cp team/F1/*.md /srv/team/work/F1/      # từ bản clone repo này; ghi đè request/spec/tasks/acceptance
team check-spec F1 && team run F1 --detach
# xong: Claude audit (team prompt claude-audit F1) -> verdict.md; APPROVE -> team push F1 -> PR -> CI -> merge
```
Việc chuyển thành bài Facebook làm sau: dùng dòng `hook`, ba ý tóm tắt và câu hỏi cuối bài làm nguyên liệu.
