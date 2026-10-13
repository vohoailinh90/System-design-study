# Spec F3

## Goal
Add articles/sd-01-010.md .. articles/sd-01-013.md (sd-01-010,sd-01-011,sd-01-012,sd-01-013), each passing `python3 scripts/check_articles.py --ids <id>`.

## Non-goals
No Facebook or social text. No changes to the validator, catalog, STYLEGUIDE.md or other articles. No images stored in git.

## Changes by file
- articles/sd-01-010.md: new; follow STYLEGUIDE.md and copy the structure of articles/sd-01-001.md (the pilot).
- articles/sd-01-011.md: new; follow STYLEGUIDE.md and copy the structure of articles/sd-01-001.md (the pilot).
- articles/sd-01-012.md: new; follow STYLEGUIDE.md and copy the structure of articles/sd-01-001.md (the pilot).
- articles/sd-01-013.md: new; follow STYLEGUIDE.md and copy the structure of articles/sd-01-001.md (the pilot).
- tests/test_batch_F3.py: new, written by the tester role only (see below).

## Data contracts and interfaces
Front matter: id, title (the catalog `title_plain`), hook (20-140 chars, one line, no URL), source_path and source_commit copied from the catalog, status: draft.
Image URLs, source_path and source_commit come from catalog/api-web-development.json for the same id; copy them exactly.
Tester role: write tests/test_batch_F3.py (unittest, stdlib). For each id in ['sd-01-010', 'sd-01-011', 'sd-01-012', 'sd-01-013']: assert articles/<id>.md exists and that
`check_articles.check_article(path, check_articles.load_catalog(ROOT))` returns an empty list (import it from scripts/).

## Topics (architect's briefing: the only facts you may use)
- sd-01-010 "CSS: lớp "trang điểm" cho trang web" (source data/guides/what-is-css-cascading-style-sheets.md)
  - analogy: tủ quần áo tách biệt với cơ thể; terms that must appear: CSS, HTML, Flexbox, Grid
  - facts to convey: HTML là nội dung, CSS là hình thức; Quy tắc gồm bộ chọn và thuộc tính (màu, cỡ chữ, vị trí); Cascading: quy tắc xung đột thì quy tắc có trọng số cao hơn thắng; Flexbox và Grid giúp bố cục hiện đại, tương thích nhiều màn hình
  - watch out: Không đưa mã. Mô tả bằng lời "đổi màu tất cả đoạn văn sang xanh".
- sd-01-011 "6 công dụng chính của cân bằng tải" (source data/guides/key-use-cases-for-load-balancers.md)
  - analogy: người chia khách ở bàn tiếp tân; terms that must appear: cân bằng tải, server, scalability, SSL
  - facts to convey: Chia đều lưu lượng; Sẵn sàng cao: máy hỏng thì chuyển sang máy tốt; Giải mã SSL hộ; Giữ phiên: cùng người dùng về cùng máy; Dễ mở rộng: thêm máy là xong; Theo dõi sức khỏe và loại máy lỗi
  - watch out: Bài này trùng nhiều ý với sd-01-002: viết bằng ví dụ khác, nhấn mạnh "mở rộng" và "sẵn sàng cao".
- sd-01-012 "18 "cổng" mạng phổ biến, như số phòng trong tòa nhà" (source data/guides/18-common-ports-worth-knowing.md)
  - analogy: số phòng trong một tòa nhà; terms that must appear: port, TCP, UDP, HTTPS
  - facts to convey: Địa chỉ IP là địa chỉ tòa nhà, cổng là số phòng; HTTP dùng 80, HTTPS 443; SSH 22, DNS 53; Email: SMTP 25, POP3 110, IMAP 143; Cơ sở dữ liệu: MySQL 3306, PostgreSQL 5432; RDP 3389
  - watch out: Chỉ chọn khoảng 6–8 cổng quen thuộc để giải thích kỹ, phần còn lại gom bảng ngắn. Số cổng phải đúng như nguồn.
- sd-01-013 "PAN, LAN, MAN, WAN: mạng nhỏ đến mạng toàn cầu" (source data/guides/what-are-the-differences-between-wan-lan-pan-and-man.md)
  - analogy: từ bàn làm việc đến cả thành phố và cả nước; terms that must appear: PAN, LAN, MAN, WAN
  - facts to convey: PAN: quanh một người, vài mét, ví dụ điện thoại và tai nghe Bluetooth; LAN: trong nhà, văn phòng, tòa nhà; MAN: cỡ một thành phố; WAN: cỡ quốc gia, lục địa; Internet là mạng WAN lớn nhất
  - watch out: Dùng ví dụ quen thuộc; mỗi loại một ví dụ đời thường.

## Invariants
The pilot article, the validator and its tests keep passing. Each article is original wording, Vietnamese, 450-1500 words.

## Security and data notes
Links are limited to the image URLs, the pinned source link and the CC link (the validator enforces it). Never copy binary images.

## Risks and open points
The models cannot see the diagrams: they describe only what the catalog facts say. The audit must compare each article with its original image.
Source licence is CC BY-NC-ND 4.0: nothing here is cleared for publication.
