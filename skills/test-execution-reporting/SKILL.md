---
name: test-execution-reporting
description: Chạy bộ TC đã có và tổng hợp kết quả thật thành báo cáo gọn, với kết quả chung và ảnh JPG cần thiết cho bug. Dùng cho execution, report-only hoặc AI gap analysis; không sinh lại bộ TC.
---

# Thực thi test và báo cáo

Nhận TC đã thiết kế, giữ ID, dữ liệu, precondition, steps và expected. Execution cho phép chạy SUT; report-only dùng kết quả đã có. Không bắt gọi lại skill thiết kế trước khi thực hiện.

## Luồng mặc định

1. Xác định bộ TC/phiên bản, lớp Web/native/API và môi trường. Tận dụng setup/runner đang có, chỉ chuẩn bị phần cần thiết. Nêu ngắn flow và đầu ra trước đợt chạy lớn.
2. Chạy đúng bước của TC, ghi actual từ quan sát/assertion thật. Giữ session/app đang chạy khi precondition cho phép; chỉ restart/reset khi TC hoặc trạng thái môi trường đòi hỏi. Giữ state giữa các bước sequence.
3. Ghi vào **một nguồn kết quả chung** của bộ test. Mỗi TC là một entry, không phải một thư mục/bộ file. Run ID, thời gian, revision và môi trường lưu một lần mỗi run; từng TC tham chiếu run đó. Dùng lại output phù hợp của runner, không nhân bản cùng dữ liệu thành nhiều JSON/CSV/bảng phụ.
4. Xuất report Markdown từ nguồn chung: summary, bảng TC, bugs và coverage/gaps thuộc phạm vi được giao. Bảng phải cho người đọc đối chiếu ngay nội dung kiểm tra/input chính → expected → actual → kết luận, có link về bộ TC và bug. Dẫn lại thiết kế đã có; không chép toàn bộ để làm report dài hơn.

Khi chưa có cấu trúc phù hợp: `results.json` cho toàn bộ TC và lịch sử run, `report.md` là bản chính để người học đọc và nghiệm thu, `images/` cho JPG cần thiết. Chỉ thêm CSV, file bug hoặc index riêng khi task/cách dùng cần. Không tạo bản kết quả gồm một TC và hàng chục TC `not_run` cho mỗi lần thử harness.

## Evidence vừa đủ

- Mỗi TC đã chạy có actual cụ thể và observation/assertion hỗ trợ, ví dụ UI tới Login và account 0→1. **Mobile không bắt buộc screenshot cho mọi TC.** Chỉ kiểm tra DB/API phụ trợ khi oracle cần; chúng không thay thao tác native.
- Chụp bug hoặc trạng thái UI cần chứng minh; thêm ảnh input khi cần hiểu lỗi. Nhiều TC cùng bug có thể dẫn tới chung ảnh. Không chụp trùng “result” và “case-ended”.
- Xuất JPG thật và mở kiểm tra. PNG tạm do task tạo được xóa sau khi JPG hợp lệ; có thể chuyển trong bộ nhớ để không ghi PNG. Không tự xóa ảnh người dùng cung cấp. Xem [evidence](references/evidence.md) khi capture/xuất ảnh.
- Lưu observation/assertion ngắn trong kết quả chung. Không dump toàn bộ layout sau mỗi thao tác, DB dump hoặc bật recorder phụ cho mọi TC. Chỉ bật log debug giới hạn khi cần điều tra lỗi; không đưa log thừa vào bộ bàn giao.

## Giữ tính đúng đắn

Giữ `passed`, `failed`, `blocked`, `not_run`; không đổi expected theo code, sửa nghiệp vụ hay bỏ lỗi để làm kết quả xanh. Lỗi setup/harness khác bug sản phẩm. Không dùng toast làm chứng cứ duy nhất khi expected yêu cầu dữ liệu đã lưu.

Giữ lịch sử run/rerun thật trong nguồn chung; summary đếm unique TC theo kết quả được chọn và nêu quy ước đó. Coverage thiết kế, coverage đã exercise và pass rate tính riêng. Khi bị ngắt, ghi bước dở dang; không nhận đã hoàn tất hoặc tự submit lại khi chưa rõ lần trước đã tạo dữ liệu chưa.

Khi lỗi harness lặp lại, dừng phần bị ảnh hưởng, lưu chẩn đoán ngắn và sửa/kiểm chứng trước khi mở rộng chạy. Không tạo hàng loạt probe, framework hoặc dịch vụ phụ để tiếp tục một luồng chưa ổn định. Chi tiết execution/bug ở [execution-and-bugs](references/execution-and-bugs.md).

## Báo cáo và giới hạn

Đọc [report-contract](references/report-contract.md) khi tổng hợp; [template report](assets/feature-report.template.md) là gợi ý, chỉ dùng mục phù hợp. Đọc [AI gap analysis](references/ai-gap-analysis.md) khi được giao phần này; dùng bản đầu/review có nguồn, không dựng lại lịch sử hoặc bịa gap.

HW02 yêu cầu bug trong Markdown và GitHub Issues kèm ảnh. Chuẩn bị detail trong report; chỉ đăng khi được giao và tracker rõ. Kiểm tra số liệu, link, ảnh nhúng và cách giải thích kết luận trong Markdown. Chưa đăng issue thì ghi đúng trạng thái.

Không tự ghi AI audit, commit/push, upload video hoặc nộp bài. Chỉ đọc [demo](references/demo.md) khi chuẩn bị demo; [research](references/research.md) lưu nguồn phương pháp.
