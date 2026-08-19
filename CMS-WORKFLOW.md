# Chú Nếp Công Nghệ — chuẩn bài CMS

Từ 2026-08-19, mọi bài mới phải được tạo trong `_posts` để Pages CMS nhìn thấy và có thể chỉnh tay. HTML hard-code không phải nguồn nội dung chính.

## Chuẩn bắt buộc cho mỗi bài
- `title`: rõ sản phẩm/vấn đề và search intent; không giật tít sai dữ kiện.
- `description`: mô tả SEO tự nhiên, ưu tiên 140–165 ký tự.
- `answer_summary`: 2–4 câu trả lời trực tiếp truy vấn chính để phục vụ AEO/GEO.
- `target_query`, `tags`, `category`, `section`, ngày xuất bản/cập nhật.
- `key_takeaways`: tối thiểu 3 ý người đọc cần biết ngay.
- `quick_compare`: tối thiểu 3 tiêu chí đối chiếu với đời trước, đối thủ, cấu hình khác hoặc phương án thay thế phù hợp với chủ đề.
- `sources`: nguồn chính thức hoặc nguồn gốc dữ liệu rõ ràng; claim của hãng phải gắn `vendor-claim` khi cần.
- `faq`: tối thiểu 2 câu hỏi sát search intent.
- Ảnh bài viết là asset độc lập, không nhúng thumbnail nén/base64 vào bài.

## Chuẩn thumbnail
- Mỗi bài có thumbnail riêng, tập trung vào đúng sản phẩm hoặc vấn đề đang nói tới.
- Không dùng template chữ chung kiểu “Tin nhanh”, “Có nguồn”, “Không bịa số”.
- Ưu tiên 1–2 chủ thể chính, headline ngắn, tương phản cao, đọc được khi card nhỏ.
- Không đưa số liệu chưa được xác nhận lên thumbnail.

## Chuẩn so sánh
- Mỗi bài đều phải giúp người đọc biết “khác gì so với phương án gần nhất”.
- Bài chuyên mục So sánh hiệu suất dùng thêm `comparison.metrics` và nguồn cho từng chỉ số.
- Không trộn điều kiện benchmark khác nhau rồi kết luận thắng/thua tuyệt đối.
- Thiếu dữ liệu thì ghi rõ chưa đủ dữ liệu, không ước đoán.

## SEO / AEO / GEO
- Một H1 duy nhất; H2/H3 mô tả câu hỏi người dùng thực sự tìm.
- Trả lời trực tiếp trước, giải thích sau; có bảng đối chiếu, FAQ, nguồn và kết luận theo từng nhóm nhu cầu.
- Internal link theo cụm chủ đề khi có bài liên quan.
- Article, FAQ và Breadcrumb structured data được layout sinh tự động.
