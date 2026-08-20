# Chính sách thumbnail — Chú Nếp Công Nghệ

Từ 20/08/2026, thumbnail bài viết phải tuân thủ các quy tắc sau:

1. **1 bài = 1 thumbnail riêng, duy nhất.** Không dùng lại cùng một file thumbnail cho hai bài khác nhau.
2. **Thumbnail phải là ảnh local trong repo** ở `assets/images/thumbs/<slug>.jpg` trước khi coi là hoàn tất.
3. **Không hotlink ảnh ngoài trên production.** Ảnh nguồn có thể lấy từ press/product photo hợp lệ nhưng phải được localize và kiểm tra trước khi render.
4. **Không dùng phác họa 2D/vector làm thumbnail sản phẩm.** Ưu tiên product photography, press photo hoặc editorial product image có chiều sâu.
5. **Ảnh phải đúng vấn đề của bài.** Bài hub/dock phải tập trung hub/dock; bài RAM/SSD phải thể hiện đúng linh kiện/workflow; bài so sánh phải có hai phía rõ ràng.
6. **Không bịa ngoại hình sản phẩm chưa xác nhận.** Nếu sản phẩm chưa có ảnh chính thức, dùng ảnh bối cảnh/chủ đề thật và ghi rõ concept khi cần.
7. **Anti-broken:** file phải tồn tại, decode được và đúng kích thước 1200×675.
8. **Anti-duplicate:** đường dẫn local và binary thumbnail phải duy nhất cho từng slug. Nếu nhiều bài dùng chung một ảnh nguồn, phải tạo composition/crop khác nhau và lưu thành file riêng.
9. Mỗi batch 12 bài mới phải kết thúc với **12 thumbnail local riêng** và pass kiểm tra trước khi coi batch hoàn tất.
10. Workflow `Localize unique article thumbnails` là gate bắt buộc: batch chưa pass thì chưa được coi là hoàn tất.
