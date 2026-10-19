# Demo phối hợp thiết kế và thực thi cho HW02 §7

Một demo có thể thể hiện hai chặng riêng: `domain-bva-testing` sinh bộ TC rồi kết thúc; sau đó người dùng gọi `test-execution-reporting` để chạy và tổng hợp. Khi TC đã có từ nguồn khác, skill thực thi nhận trực tiếp bộ đó. Đây là kịch bản quay gợi ý cho một feature hoàn chỉnh, không phải video đã có hoặc số lượng video bắt buộc.

1. Nêu feature, nguồn requirement, commit SUT và lớp chạy. Mở skill/bộ nguồn đúng; không chiếu dữ liệu riêng tư hoặc token.
2. Giao yêu cầu thiết kế cho `domain-bva-testing` với đặc tả và phương pháp được phép; skill trình bày input/rule/giả định. Đừng diễn lại một hội thoại như thể đó là bản gốc.
3. Cho thấy mô hình Domain, điểm đại diện và cách suy ra một vài TC; người học giải thích một lựa chọn quan trọng.
4. Cho thấy inventory biên, biến thể, độ phân giải và cách ra dữ liệu. Nếu chạy helper, giải thích input lấy từ đâu và helper không tạo oracle.
5. Review thật một output; giữ chỉnh sửa hoặc xác nhận có căn cứ. Nếu quay lại sau khi bài đã làm, ghi là demo/run mới.
6. Kết thúc chặng thiết kế và gọi riêng `test-execution-reporting` với bộ TC vừa bàn giao. Chạy trên đúng giao diện/native và cho xem kết quả liên kết; ghi run/evidence thật, không đổi assertion để xanh.
7. Nêu một gap thực nếu có và một bug tái hiện nếu có; cho thấy report và issue có ảnh khi đã đăng. Không bịa bug để có clip.
8. Cho thấy summary/coverage/AI log liên quan và điều còn thiếu. Tự giải thích được source expected và giới hạn của kỹ thuật.

Lựa chọn phù hợp cho feature đầu tiên: đăng ký Mobile có form và ngưỡng mật khẩu rõ. Cần chạy trên thiết bị/emulator; chỉ quay API không thay demo native. Bài giảng và assignment vẫn quyết định tiêu chí chính thức, không bắt buộc độ dài video từ hướng dẫn này.

Sau quay, tự mở link YouTube bằng quyền xem dự kiến của người chấm; thêm vào README bộ nộp. Không tự nhận có link trước khi video được tải lên và kiểm tra.
