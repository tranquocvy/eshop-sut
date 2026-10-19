---
name: course-ai-log
description: Trích xuất nhật ký tương tác AI và điền AI Audit Report, Disclosure, Privacy Checklist theo đề và biểu mẫu của từng bài tập. Dùng khi cập nhật AI log hoặc hồ sơ khai báo AI cho HW, seminar hay đồ án; giữ prompt/output có nguồn và văn phong báo cáo sinh viên.
---

# AI log và biểu mẫu cho bài tập

Tự làm phần chép log, tổng hợp artifact và soạn biểu mẫu để sinh viên đọc, kiểm tra và dùng tiếp. Viết tiếng Việt tự nhiên, cụ thể và bám biểu mẫu được cung cấp. Giữ đầy đủ nội dung cần đối chiếu; đưa ID nguồn, hash và chi tiết trích xuất vào dữ liệu hỗ trợ thay vì làm chúng lấn át báo cáo.

## Xác định đúng bài và nguồn

- Đọc đề/rubric, chính sách AI, biểu mẫu và bộ file hiện hành của **bài đang được giao**. Lấy mã bài, tên bài, yêu cầu nộp, độ dài và định dạng từ nguồn này; không cố định HW02, Domain Testing hay một thư mục đầu ra trong skill.
- Nguồn đầu vào gồm đề, chính sách AI, biểu mẫu và hội thoại do người dùng cung cấp. Mẫu bài trước có thể giúp chọn cách trình bày; đề và thông báo hiện hành quyết định yêu cầu của bài đang làm. Không cần hồ sơ cá nhân hay một kho skill khác để dùng bộ này.
- Tiếp tục bộ file đang có, giữ tên/vị trí và phần người dùng đã sửa. Nếu chưa có, đặt bộ file AI cạnh sản phẩm bài tập theo cấu trúc workspace; đây là lựa chọn tổ chức, không phải quy định của giảng viên.
- Khi được giao cập nhật log, tự ghi dữ kiện có nguồn và soạn bản nháp local. Yêu cầu chỉ xem/đợi duyệt trong lần cụ thể vẫn được ưu tiên. Tạo hay sửa skill không tự khởi chạy việc ghi lại toàn bộ lịch sử hoặc viết lại báo cáo cũ.

## Thực hiện

1. Xác định phạm vi cần ghi: task, phiên hoặc các lượt được chỉ định. Đọc nguồn hội thoại của chính phạm vi đó; chỉ dùng lời gốc còn truy cập được hoặc transcript/export. Không phục dựng prompt/output từ summary, file sản phẩm hay trí nhớ.
2. Trích prompt và các phản hồi AI theo thứ tự, gồm phản hồi tiến độ, kết quả, yêu cầu sửa và lượt sửa sai. Giữ công cụ và timestamp thật. UI reply do người dùng nhập là tương tác; ambient context tự sinh không phải prompt của sinh viên.
3. Cập nhật Prompt Log bằng [helper và quy cách log](references/log-format.md). Bản đọc dùng `P-000`, thời gian, công cụ, Prompt và Output. Helper giữ dữ liệu đối chiếu, chống trùng và bảo toàn sửa tay. Nó không tự tìm lịch sử hay chạy nền.
4. Nhận diện artifact thực và phiên bản được đánh giá: báo cáo, bộ test, script, skill, hình ảnh, bảng tính... Một artifact có thể qua nhiều lượt; không đếm mỗi tin nhắn/file phụ thành một artifact. Giữ output ban đầu và bản sửa cần đối chiếu, không thay output cũ bằng file cuối.
5. Điền các biểu mẫu được giao theo [quy cách biểu mẫu](references/forms.md). AI-02 đánh giá từng artifact theo yêu cầu tạo ra nó; AI-03 khai báo ngắn gọn; AI-05 theo checklist thực tế khi có mẫu. Toàn bộ trao đổi nằm trong Prompt Log, không nhân bản mọi thông báo tiến độ sang audit.
6. Đối chiếu nguyên văn, liên kết, số liệu, phiên bản và người thực hiện. Bàn giao ngắn: file đã cập nhật, phạm vi đã ghi và phần thực sự cần bổ sung. Nếu chưa đủ lịch sử, ghi rõ khoảng thiếu một lần và vẫn hoàn thành phần có nguồn.

## Dữ kiện và giọng văn

- Dùng thông tin sinh viên ổn định từ tài liệu chính người dùng cung cấp khi đã rõ cùng một người; không bắt xác nhận lại MSSV/lớp ở mỗi HW. Tool, model, ngày dùng, hoạt động review, verdict và chữ ký của bài cũ không chứng minh những việc đó cho bài mới.
- Tự điền bản nháp nhận xét có căn cứ. Đánh giá **đúng yêu cầu của artifact**, nêu sai/thiếu cụ thể và cách sửa. Tiến độ cả bài chỉ liên quan nếu nằm trong phạm vi artifact được yêu cầu.
- Một ghi chú đầu tài liệu đủ để xác định bản nháp/verdict đề xuất đang chờ sinh viên duyệt. Không lặp “chưa xác nhận”, “không tự coi”, “không có bằng chứng” trong từng ô. Trường thật sự chưa biết để trống hoặc ghi ngắn tại đúng chỗ.
- Bản khai có thể dùng ngôi “tôi” cho hoạt động có thật của sinh viên, ví dụ “Tôi dùng Codex để...”. Việc AI chạy test thì viết “Codex đã chạy...”; chỉ viết “Tôi đã đối chiếu/chạy/sửa...” khi có dữ kiện người dùng đã làm. Không suy ra review chỉ từ một lời đồng ý chung.
- Giữ đầy đủ prompt/output gốc, không paraphrase chúng cho văn vẻ. Nhận xét và khai báo dùng câu dễ hiểu, tên artifact và kết quả cụ thể. Chi tiết như `turn_context`, dòng transcript, hash và source UUID thuộc dữ liệu hỗ trợ.

## Hoàn tất và giới hạn

Log đủ lượt và nội dung còn nguyên văn là hai thuộc tính riêng: có thể đủ lượt nhưng một phần nội dung đã được che. Ghi rõ vị trí/lý do che, không gắn nhãn “thiếu lịch sử” chỉ vì đã ẩn một đường dẫn. Không xuất system/developer instructions, suy luận nội bộ, secrets hoặc chat ngoài phạm vi. Giữ quyền riêng tư của skill cá nhân; skill kỹ thuật được giao để nộp có thể là artifact.

Số liệu và nhận xét phải khớp dữ kiện; đề xuất AI chưa phải verdict sinh viên đã duyệt. Chữ ký để sinh viên thực hiện. Không tự đánh dấu đã nộp hoặc mọi ô AI-05 hoàn tất. Giữ quyền Git/xuất bản của từng task; skill ghi log không cấp thêm quyền commit, push, đăng issue hay nộp bài. Xuất PDF/Critique khi được giao và theo yêu cầu bài hiện hành.
