# Spec F1

## Goal
Add articles/sd-01-002.md .. articles/sd-01-005.md (sd-01-002,sd-01-003,sd-01-004,sd-01-005), each passing `python3 scripts/check_articles.py --ids <id>`.

## Non-goals
No Facebook or social text. No changes to the validator, catalog, STYLEGUIDE.md or other articles. No images stored in git.

## Changes by file
- articles/sd-01-002.md: new; follow STYLEGUIDE.md and copy the structure of articles/sd-01-001.md (the pilot).
- articles/sd-01-003.md: new; follow STYLEGUIDE.md and copy the structure of articles/sd-01-001.md (the pilot).
- articles/sd-01-004.md: new; follow STYLEGUIDE.md and copy the structure of articles/sd-01-001.md (the pilot).
- articles/sd-01-005.md: new; follow STYLEGUIDE.md and copy the structure of articles/sd-01-001.md (the pilot).
- tests/test_batch_F1.py: new, written by the tester role only (see below).

## Data contracts and interfaces
Front matter: id, title (the catalog `title_plain`), hook (20-140 chars, one line, no URL), source_path and source_commit copied from the catalog, status: draft.
Image URLs, source_path and source_commit come from catalog/api-web-development.json for the same id; copy them exactly.
Tester role: write tests/test_batch_F1.py (unittest, stdlib). For each id in ['sd-01-002', 'sd-01-003', 'sd-01-004', 'sd-01-005']: assert articles/<id>.md exists and that
`check_articles.check_article(path, check_articles.load_catalog(ROOT))` returns an empty list (import it from scripts/).

## Topics (architect's briefing: the only facts you may use)
- sd-01-002 "Người điều phối giúp web không sập: 6 việc thực tế" (source data/guides/load-balancer-realistic-use-cases-you-may-not-know.md)
  - analogy: nhân viên điều phối ở nhà hàng đông khách; terms that must appear: cân bằng tải, SSL, health check
  - facts to convey: Xử lý lỗi: chuyển khách khỏi máy hỏng; Kiểm tra sức khỏe: chỉ gửi khách tới máy còn chạy tốt; Định tuyến theo thiết bị: điện thoại và máy tính có thể đi đường khác nhau; Giải mã SSL thay cho máy chủ để máy chủ nhẹ việc; Cân bằng giữa nhiều vùng; dính phiên: cùng một người luôn về cùng một máy
  - watch out: Giải thích SSL là khóa bảo mật của kết nối an toàn (https), không đi sâu mật mã.
- sd-01-003 "5 "mã lỗi web" kỳ quặc có thật" (source data/guides/5-http-status-codes-that-should-never-have-been-created.md)
  - analogy: tem phiếu trả lời của bưu điện; terms that must appear: HTTP, mã trạng thái, 451, 418
  - facts to convey: 451: bị chặn vì lý do pháp lý; 418 Tôi là ấm trà: trò đùa Cá tháng Tư; 420: cách cũ của Twitter báo gọi quá nhiều, nay dùng 429; 530 và 218 là mã không chính thức của một số dịch vụ; Mã trạng thái là con số ngắn máy chủ trả lời trình duyệt
  - watch out: Các mã 218, 420, 530 không thuộc chuẩn chính thức; nói rõ "không chính thức". 418 là đùa trong một tài liệu 1998.
- sd-01-004 "gRPC: các dịch vụ nói chuyện nhanh với nhau thế nào?" (source data/guides/how-does-grpc-work.md)
  - analogy: hai bộ phận trong công ty trao đổi bằng mã viết tắt; terms that must appear: gRPC, RPC, JSON, HTTP/2
  - facts to convey: RPC: gọi hàm ở máy khác như gọi hàm tại chỗ; Dữ liệu được nén thành dạng nhị phân gọn hơn JSON; Chạy trên HTTP/2; Luồng: khách gọi → dịch vụ đơn hàng → dịch vụ thanh toán → trả kết quả ngược lại; Nguồn nói nhanh hơn JSON khoảng 5 lần: nói là "có thể nhanh hơn nhiều, tùy trường hợp"
  - watch out: Không khẳng định con số 5 lần như chắc chắn. Không viết mã.
- sd-01-005 "NAT: vì sao cả nhà dùng chung một địa chỉ Internet?" (source data/guides/how-nat-made-the-growth-of-the-internet-possible.md)
  - analogy: lễ tân tòa nhà nhận thư chung rồi chuyển đến từng phòng; terms that must appear: NAT, IP, router, IPv4
  - facts to convey: Nhiều thiết bị trong nhà dùng chung một địa chỉ công khai; Router đổi địa chỉ riêng thành địa chỉ công khai khi đi ra, đổi ngược khi nhận về; Tiết kiệm địa chỉ IPv4 vốn có hạn; Che địa chỉ nội bộ nên có tác dụng như tường lửa cơ bản
  - watch out: NAT che địa chỉ nội bộ nhưng không thay thế tường lửa thật.

## Invariants
The pilot article, the validator and its tests keep passing. Each article is original wording, Vietnamese, 450-1500 words.

## Security and data notes
Links are limited to the image URLs, the pinned source link and the CC link (the validator enforces it). Never copy binary images.

## Risks and open points
The models cannot see the diagrams: they describe only what the catalog facts say. The audit must compare each article with its original image.
Source licence is CC BY-NC-ND 4.0: nothing here is cleared for publication.
