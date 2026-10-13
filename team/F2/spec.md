# Spec F2

## Goal
Add articles/sd-01-006.md .. articles/sd-01-009.md (sd-01-006,sd-01-007,sd-01-008,sd-01-009), each passing `python3 scripts/check_articles.py --ids <id>`.

## Non-goals
No Facebook or social text. No changes to the validator, catalog, STYLEGUIDE.md or other articles. No images stored in git.

## Changes by file
- articles/sd-01-006.md: new; follow STYLEGUIDE.md and copy the structure of articles/sd-01-001.md (the pilot).
- articles/sd-01-007.md: new; follow STYLEGUIDE.md and copy the structure of articles/sd-01-001.md (the pilot).
- articles/sd-01-008.md: new; follow STYLEGUIDE.md and copy the structure of articles/sd-01-001.md (the pilot).
- articles/sd-01-009.md: new; follow STYLEGUIDE.md and copy the structure of articles/sd-01-001.md (the pilot).
- tests/test_batch_F2.py: new, written by the tester role only (see below).

## Data contracts and interfaces
Front matter: id, title (the catalog `title_plain`), hook (20-140 chars, one line, no URL), source_path and source_commit copied from the catalog, status: draft.
Image URLs, source_path and source_commit come from catalog/api-web-development.json for the same id; copy them exactly.
Tester role: write tests/test_batch_F2.py (unittest, stdlib). For each id in ['sd-01-006', 'sd-01-007', 'sd-01-008', 'sd-01-009']: assert articles/<id>.md exists and that
`check_articles.check_article(path, check_articles.load_catalog(ROOT))` returns an empty list (import it from scripts/).

## Topics (architect's briefing: the only facts you may use)
- sd-01-006 "HTTP header: "tem dán ngoài phong bì" của mỗi yêu cầu web" (source data/guides/important-things-about-http-headers-you-may-not-know.md)
  - analogy: thông tin ghi ngoài phong bì thư; terms that must appear: HTTP, header, request, response
  - facts to convey: Yêu cầu và phản hồi là cặp hỏi–đáp; Header là thông tin thêm: bạn là ai, gửi loại dữ liệu gì; Header phản hồi cho biết kiểu dữ liệu nhận về hoặc chỉ dẫn đặc biệt; Cần hiểu header để hai bên hiểu đúng nhau
  - watch out: Chỉ nêu ví dụ header dễ hiểu (như loại nội dung, ngôn ngữ), không liệt kê hàng loạt.
- sd-01-007 "DNS chỉ đường: 6 cách chia người dùng tới máy chủ" (source data/guides/internet-traffic-routing-policies.md)
  - analogy: tổng đài chỉ đường tới nhiều chi nhánh; terms that must appear: DNS, failover, độ trễ, trọng số
  - facts to convey: Simple: một điểm đến duy nhất; Failover: hỏng thì sang điểm dự phòng; Geolocation: theo vị trí người dùng; Latency: tới nơi phản hồi nhanh nhất; Multivalue: trả nhiều địa chỉ, không thay thế cân bằng tải; Weighted: chia theo tỷ lệ
  - watch out: DNS là danh bạ đổi tên miền thành địa chỉ; nói rõ chính sách này do DNS thực hiện.
- sd-01-008 "Trình duyệt biến mã thành trang web trước mắt bạn thế nào?" (source data/guides/how-does-the-browser-render-a-web-page.md)
  - analogy: thợ xây dựng nhà từ bản vẽ; terms that must appear: HTML, CSS, DOM, GPU
  - facts to convey: Đọc HTML dựng cây DOM; Đọc CSS dựng cây CSSOM; Gộp hai cây thành cây hiển thị, bỏ phần ẩn; Layout: tính vị trí và kích thước; Paint rồi hiển thị lên màn hình
  - watch out: Mỗi bước giải thích bằng một hình ảnh đời thường, không dùng thuật ngữ trần.
- sd-01-009 "HTTP/2 nhanh hơn HTTP/1 nhờ đâu?" (source data/guides/what-makes-http2-faster-than-http1.md)
  - analogy: đường một làn đổi thành nhiều làn; terms that must appear: HTTP/2, multiplexing, HPACK, frame
  - facts to convey: Chia dữ liệu thành các mảnh nhỏ (frame) dạng nhị phân; Multiplexing: nhiều yêu cầu chạy xen kẽ trên một kết nối; Ưu tiên luồng quan trọng trước; Server push: gửi trước tài nguyên, thực tế ít được dùng và nhiều trình duyệt đã bỏ hỗ trợ; HPACK nén header
  - watch out: Nguồn tự nhắc HTTP/2 vẫn có thể chậm tùy tình huống; giữ lời nhắc đó.

## Invariants
The pilot article, the validator and its tests keep passing. Each article is original wording, Vietnamese, 450-1500 words.

## Security and data notes
Links are limited to the image URLs, the pinned source link and the CC link (the validator enforces it). Never copy binary images.

## Risks and open points
The models cannot see the diagrams: they describe only what the catalog facts say. The audit must compare each article with its original image.
Source licence is CC BY-NC-ND 4.0: nothing here is cleared for publication.
