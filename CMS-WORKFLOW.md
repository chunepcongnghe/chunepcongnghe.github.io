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
- Ảnh bài viết là asset độc lập trong `assets/posts`.

## Chuẩn thumbnail mặc định
Chi tiết đầy đủ nằm trong `THUMBNAIL-STYLE.md`. Từ đợt 2026-08-19, style mặc định là **3D product render realistic / editorial tech photography**.
- Mỗi bài có thumbnail riêng và sản phẩm/vấn đề phải là chủ thể lớn nhất.
- Không dùng vector phẳng hoặc background trơn đơn sắc làm style mặc định.
- Nền có chiều sâu: studio, bàn setup, môi trường sử dụng, road trip, bokeh/ánh sáng phù hợp nhưng không lấn át sản phẩm.
- Bài so sánh đặt hai phương án đối diện rõ ràng; bài review/tin mới tập trung một sản phẩm; bài thủ thuật ưu tiên bối cảnh thao tác.
- Hạn chế chữ trên thumbnail; chỉ giữ nhãn ngắn thật sự cần thiết như `M5 vs M4`, `16/24/32GB`, `Action 6 vs 5 Pro`.
- Không dùng slogan chung kiểu “Tin nhanh”, “Có nguồn”, “Không bịa số”.
- Không bịa ngoại hình sản phẩm chưa được công bố và không đưa số liệu chưa xác nhận lên ảnh.
- Tone sáng, premium, hiện đại, sắc nét; tránh tối cyberpunk quá mức.

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
