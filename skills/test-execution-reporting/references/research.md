# Nguồn của phần thực thi và báo cáo

Phần này được tách từ bộ Domain/BVA ban đầu theo yêu cầu dùng skill sinh TC độc lập. Không thực hiện một đợt khảo sát mới; giữ các nguồn đã đọc ngày 19/10/2026 và yêu cầu bài do người dùng cung cấp.

- [rcptrkr/qa-skills — bug-report-forensics](https://github.com/rcptrkr/qa-skills/blob/8757aab2f5e1834be351eeb497bb3e7cf6991e9d/plugins/qa-essentials/skills/bug-report-forensics/SKILL.md), MIT: tham khảo oracle, bước tái hiện gọn và bằng chứng. Hướng dẫn trong bộ này được viết mới; không chép prompt/code của nguồn.
- Đề HW02 §6: Domain/BVA, AI gap analysis khi có bỏ sót, bug trong Markdown và GitHub Issues nhóm kèm screenshot; §14: số liệu test summary và sản phẩm nộp. Đọc đề hiện hành của task trước khi áp dụng, không biến quy định HW02 thành yêu cầu cho mọi dự án.

## Phân chia trách nhiệm

Skill thiết kế bàn giao TC và cơ sở expected; skill này nhận TC từ bất kỳ nguồn nào, giữ dữ liệu thiết kế và bổ sung run/evidence/gap/bug. Không tự gọi ngược lại skill thiết kế hoặc ép một task report-only phải chạy test. Có thể kết hợp hai chặng khi người dùng giao trọn quy trình; đó không phải mặc định cho yêu cầu sinh TC nhanh.

Kiểm tra cấu trúc skill không thay bằng chứng execution trên feature thật. Báo cáo phải phân biệt việc đã chạy, chỉ review/static, bị blocked và chưa chạy.
