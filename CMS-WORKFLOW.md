# Chú Nếp Công Nghệ — CMS workflow

Từ 2026-08-19, CMS là nguồn nội dung chính của website. Mọi bài mới phải được tạo thành một record/file trong `_posts` để vừa xuất hiện trên web vừa có thể chỉnh tay trong CMS.

## Tuyến nội dung
- `tin-moi`: tin công nghệ và cập nhật nhanh.
- `tren-tay-danh-gia`: trải nghiệm, review, dùng thực tế.
- `tu-van-chon-mua`: tư vấn theo ngân sách, nhu cầu và trade-off.
- `so-sanh-hieu-suat`: so sánh cấu hình, benchmark và công năng.
- `thu-thuat`: hướng dẫn, tối ưu, xử lý lỗi.
- `deeptalk`: phân tích sâu, quan điểm và thảo luận.
- `video`: dữ liệu dành cho giai đoạn tích hợp YouTube sau.

## Quy tắc bắt buộc
- Một bài = một record/file nội dung do CMS nhìn thấy; không hard-code bài mới trực tiếp vào HTML trang chủ.
- Ảnh bài viết là asset độc lập trong `assets/posts`; không nhúng thumbnail base64 vào bài.
- Sửa tay trong CMS không được làm mất SEO/AEO/GEO, nguồn kiểm chứng, section, category, tags, publish date và updated date.
- Tin rò rỉ phải chọn `source_status: leak`; claim/benchmark của hãng phải chọn `vendor-claim` khi chưa có xác minh độc lập.
- Bài so sánh chỉ điền `comparison.metrics` khi mỗi metric có nguồn hoặc phương pháp test rõ ràng. Thiếu dữ liệu thì để trống, tuyệt đối không ước đoán cho đủ bảng.
- Trang chủ và các trang con đọc trực tiếp từ `site.posts`; bài CMS sẽ tự rơi vào đúng tuyến nội dung khi build website.
