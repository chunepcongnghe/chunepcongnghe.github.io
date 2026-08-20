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
- Ảnh bài viết là asset độc lập trong `assets/posts` hoặc được pipeline thumbnail localize về `assets/images/thumbs/<slug>.jpg`.

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
- **Một bài = một thumbnail duy nhất.** Thiếu ảnh, ảnh lỗi, trùng path hoặc trùng binary phải fail pipeline trước khi batch được tính là hoàn tất.

## Chuẩn so sánh
- Mỗi bài đều phải giúp người đọc biết “khác gì so với phương án gần nhất”.
- Bài chuyên mục So sánh hiệu suất dùng thêm `comparison.metrics` và nguồn cho từng chỉ số khi có benchmark/metric tương đương.
- Không trộn điều kiện benchmark khác nhau rồi kết luận thắng/thua tuyệt đối.
- Thiếu dữ liệu thì ghi rõ chưa đủ dữ liệu, không ước đoán.
- Claim phòng lab của hãng phải viết là mức hãng công bố/điều kiện hãng, không biến thành trải nghiệm thực tế.

## SEO / AEO / GEO
- Một H1 duy nhất; H2/H3 mô tả câu hỏi người dùng thực sự tìm.
- Trả lời trực tiếp trước, giải thích sau; có bảng đối chiếu, FAQ, nguồn và kết luận theo từng nhóm nhu cầu.
- Internal link theo cụm chủ đề khi có bài liên quan.
- Article, FAQ và Breadcrumb structured data được layout sinh tự động.

## Chuẩn Batch 4 trở đi — khóa cố định
- Mỗi batch có **12 bài net-new**, kiểm tra intent để tránh cannibalization với bài đã có.
- Toàn bộ văn bản thân bài, lead, list, blockquote, FAQ và ghi chú nguồn phải căn đều; heading, bảng và metadata giữ canh tự nhiên để dễ đọc.
- Mỗi bài có mục **`## Chú Nếp chốt nhanh`**: ngắn, rõ quan điểm, trả lời người đọc nên hiểu/chọn gì nhưng không viết kiểu quảng cáo.
- Fact, vendor claim và opinion phải tách rõ. Không giả hands-on nếu chưa cầm/sử dụng sản phẩm; ghi “phân tích theo dữ liệu” khi phù hợp.
- Ưu tiên bảng Markdown hoặc `quick_compare` khi có từ hai phương án trở lên; bảng phải cùng điều kiện hoặc ghi rõ giới hạn so sánh.
- Có thể thêm ảnh minh họa trong thân bài khi ảnh giúp giải thích cấu tạo, workflow, cổng kết nối hoặc điều kiện test; không thêm ảnh chỉ để lấp chỗ trống.
- Thumbnail phải realistic/product/editorial photography, đúng chủ thể, local sau pipeline, 1200×675, duy nhất và không lỗi.
- Batch chỉ hoàn tất sau khi post, thumbnail localizer và anti-duplicate/anti-broken đều pass trên `main`.
