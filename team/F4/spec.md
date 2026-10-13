# Spec F4

## Goal
Add articles/sd-01-014.md .. articles/sd-01-017.md (sd-01-014,sd-01-015,sd-01-016,sd-01-017), each passing `python3 scripts/check_articles.py --ids <id>`.

## Non-goals
No Facebook or social text. No changes to the validator, catalog, STYLEGUIDE.md or other articles. No images stored in git.

## Changes by file
- articles/sd-01-014.md: new; follow STYLEGUIDE.md and copy the structure of articles/sd-01-001.md (the pilot).
- articles/sd-01-015.md: new; follow STYLEGUIDE.md and copy the structure of articles/sd-01-001.md (the pilot).
- articles/sd-01-016.md: new; follow STYLEGUIDE.md and copy the structure of articles/sd-01-001.md (the pilot).
- articles/sd-01-017.md: new; follow STYLEGUIDE.md and copy the structure of articles/sd-01-001.md (the pilot).
- tests/test_batch_F4.py: new, written by the tester role only (see below).

## Data contracts and interfaces
Front matter: id, title (the catalog `title_plain`), hook (20-140 chars, one line, no URL), source_path and source_commit copied from the catalog, status: draft.
Image URLs, source_path and source_commit come from catalog/api-web-development.json for the same id; copy them exactly.
Tester role: write tests/test_batch_F4.py (unittest, stdlib). For each id in ['sd-01-014', 'sd-01-015', 'sd-01-016', 'sd-01-017']: assert articles/<id>.md exists and that
`check_articles.check_article(path, check_articles.load_catalog(ROOT))` returns an empty list (import it from scripts/).

## Topics (architect's briefing: the only facts you may use)
- sd-01-014 "JavaScript hoạt động thế nào trong trình duyệt?" (source data/guides/how-does-javascript-work.md)
  - analogy: người phiên dịch đọc đến đâu nói đến đó; terms that must appear: JavaScript, trình duyệt, bất đồng bộ, callback
  - facts to convey: JavaScript được trình duyệt đọc và chạy trực tiếp, hiện đại có biên dịch ngay khi chạy (JIT); Hàm là "công dân hạng nhất": gán, truyền, trả về như dữ liệu; Kiểu dữ liệu linh hoạt, chưa cần khai báo trước; Bất đồng bộ: việc chờ lâu chạy nền, xong thì báo; Tự dọn bộ nhớ
  - watch out: Nguồn gắn nhãn "client-side" cho ý bất đồng bộ: đừng lặp lại nhầm lẫn đó; JavaScript cũng chạy ở máy chủ (Node.js).
- sd-01-015 "8 mẹo để thiết kế API gọn gàng, dễ dùng" (source data/guides/8-tips-for-efficient-api-design.md)
  - analogy: thực đơn nhà hàng rõ ràng; terms that must appear: API, idempotence, phiên bản, phân trang
  - facts to convey: Đặt đường dẫn theo mô hình nghiệp vụ; Chọn đúng phương thức HTTP, dùng ít mã trạng thái; Idempotence: gọi lặp lại không gây hậu quả kép; Đánh số phiên bản từ đầu; Đường dẫn dễ hiểu; thao tác hàng loạt dùng chữ batch ở cuối đường dẫn; Quy tắc truy vấn: phân trang, sắp xếp, lọc
  - watch out: API = "thực đơn + cửa sổ gọi món" giữa hai phần mềm. Giải thích idempotence bằng nút thang máy.
- sd-01-016 "Reverse proxy, API gateway, cân bằng tải: khác nhau ở đâu?" (source data/guides/reverse-proxy-vs-api-gateway-vs-load-balancer.md)
  - analogy: bảo vệ, người đưa thư và cảnh sát giao thông; terms that must appear: reverse proxy, API gateway, cân bằng tải, server
  - facts to convey: Reverse proxy: đứng trước, giấu máy chủ thật; API gateway: nhận yêu cầu và chuyển đúng dịch vụ; Cân bằng tải: chia lưu lượng đều giữa các máy; Có thể dùng cả ba cùng nhau
  - watch out: Ba tên gọi chồng lấn thực tế; nói rõ đây là cách phân biệt vai trò chính.
- sd-01-017 "REST API: quy ước chung để các phần mềm gọi nhau" (source data/guides/how-does-rest-api-work.md)
  - analogy: quy tắc gọi món chung cho mọi nhà hàng; terms that must appear: REST, API, JSON, HTTP
  - facts to convey: REST là một phong cách thiết kế API dựa trên HTTP; Mỗi thứ (người dùng, đơn hàng) là một tài nguyên có địa chỉ riêng; Dùng các phương thức GET, POST, PUT, DELETE; Không nhớ trạng thái: mỗi yêu cầu tự mang đủ thông tin; Dữ liệu thường ở dạng JSON
  - watch out: Nguồn chỉ có hai hình và vài chữ: dựa vào hình gốc và kiến thức chuẩn, không bịa chi tiết hình.

## Invariants
The pilot article, the validator and its tests keep passing. Each article is original wording, Vietnamese, 450-1500 words.

## Security and data notes
Links are limited to the image URLs, the pinned source link and the CC link (the validator enforces it). Never copy binary images.

## Risks and open points
The models cannot see the diagrams: they describe only what the catalog facts say. The audit must compare each article with its original image.
Source licence is CC BY-NC-ND 4.0: nothing here is cleared for publication.
