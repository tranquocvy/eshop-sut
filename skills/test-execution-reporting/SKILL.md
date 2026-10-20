---
name: test-execution-reporting
description: Chạy bộ TC đã có, tổng hợp kết quả thật thành báo cáo và hoàn thiện GitHub Issues cùng ảnh bằng chứng khi thuộc yêu cầu task. Dùng cho execution, report-only hoặc AI gap analysis; không sinh lại bộ TC.
---

# Thực thi test và báo cáo

Nhận TC đã thiết kế, giữ ID, dữ liệu, precondition, steps và expected. Execution cho phép chạy SUT; report-only dùng kết quả đã có. Không bắt gọi lại skill thiết kế trước khi thực hiện.

## Luồng mặc định

1. Xác định bộ TC/phiên bản, lớp Web/native/API và môi trường. Tận dụng setup/runner đang có, chỉ chuẩn bị phần cần thiết. Nêu ngắn flow và đầu ra trước đợt chạy lớn.
2. Chạy đúng bước của TC, ghi actual từ quan sát/assertion thật. Giữ session/app đang chạy khi precondition cho phép; chỉ restart/reset khi TC hoặc trạng thái môi trường đòi hỏi. Giữ state giữa các bước sequence.
3. Ghi vào **một nguồn kết quả chung** của bộ test. Mỗi TC là một entry, không phải một thư mục/bộ file. Run ID, thời gian, revision và môi trường lưu một lần mỗi run; từng TC tham chiếu run đó. Dùng lại output phù hợp của runner, không nhân bản cùng dữ liệu thành nhiều JSON/CSV/bảng phụ.
4. Xuất report Markdown từ nguồn chung: summary, bảng TC, bugs và coverage/gaps thuộc phạm vi được giao. Bảng phải cho người đọc đối chiếu ngay nội dung kiểm tra/input chính → expected → actual → kết luận. **Mỗi dòng TC đã chạy, kể cả passed, phải có link tới log/assertion hoặc ảnh thật của đúng TC và run được chọn**, ngoài link thiết kế/bug. Dẫn lại thiết kế đã có; không chép toàn bộ để làm report dài hơn.
5. Khi phạm vi được giao bao gồm báo lỗi lên GitHub, tạo/cập nhật issue ở tracker đã xác định, kiểm tra nội dung và ảnh bug hiển thị, rồi cập nhật URL vào report. **Với HW02, phải chụp trang GitHub issue thật sau khi đăng**, lưu JPG và dẫn ảnh trong report. Đây là phần cần hoàn tất của nhiệm vụ có yêu cầu Issues, không dừng ở bản nháp Markdown. Làm theo [quy trình GitHub](references/execution-and-bugs.md#github).

Khi chưa có cấu trúc phù hợp: `results.json` cho toàn bộ TC và lịch sử run, `report.md` là bản chính để người học đọc và nghiệm thu, `images/` cho JPG cần thiết. Chỉ thêm CSV, file bug hoặc index riêng khi task/cách dùng cần. Không tạo bản kết quả gồm một TC và hàng chục TC `not_run` cho mỗi lần thử harness.

## Evidence vừa đủ

- Mỗi TC đã chạy có actual cụ thể và observation/assertion hỗ trợ, ví dụ UI tới Login và account 0→1. **Mobile không bắt buộc screenshot cho mọi TC.** Chỉ kiểm tra DB/API phụ trợ khi oracle cần; chúng không thay thao tác native.
- Đặt link evidence ngay trong dòng TC của report, dùng cột `Evidence (log/JPG)` hoặc link rõ trong ô Actual. TC pass dùng log/observation có sẵn trong kết quả chung; TC fail vẫn cần evidence đúng TC/run ngoài link bug. Ca blocked/dở dang đã có thao tác thì dẫn log điểm chặn; ca chưa chạy ghi chưa có evidence. Xem [quy tắc link evidence](references/report-contract.md#link-evidence-cho-từng-tc).
- Chụp bug hoặc trạng thái UI cần chứng minh; thêm ảnh input khi cần hiểu lỗi. Nhiều TC cùng bug có thể dẫn tới chung ảnh. Không chụp trùng “result” và “case-ended”.
- Ảnh lỗi SUT đính trong GitHub issue và ảnh chụp trang issue đã đăng là hai bằng chứng khác nhau. Với HW02, mỗi issue được báo phải có cả hai; ảnh trang issue phải đọc được tiêu đề/số issue và nội dung/ảnh bug liên quan.
- Xuất JPG thật và mở kiểm tra. PNG tạm do task tạo được xóa sau khi JPG hợp lệ; có thể chuyển trong bộ nhớ để không ghi PNG. Không tự xóa ảnh người dùng cung cấp. Xem [evidence](references/evidence.md) khi capture/xuất ảnh.
- Lưu observation/assertion ngắn trong kết quả chung. Không dump toàn bộ layout sau mỗi thao tác, DB dump hoặc bật recorder phụ cho mọi TC. Chỉ bật log debug giới hạn khi cần điều tra lỗi; không đưa log thừa vào bộ bàn giao.

## Giữ tính đúng đắn

Giữ `passed`, `failed`, `blocked`, `not_run`; không đổi expected theo code, sửa nghiệp vụ hay bỏ lỗi để làm kết quả xanh. Lỗi setup/harness khác bug sản phẩm. Không dùng toast làm chứng cứ duy nhất khi expected yêu cầu dữ liệu đã lưu.

Giữ lịch sử run/rerun thật trong nguồn chung; summary đếm unique TC theo kết quả được chọn và nêu quy ước đó. Coverage thiết kế, coverage đã exercise và pass rate tính riêng. Khi bị ngắt, ghi bước dở dang; không nhận đã hoàn tất hoặc tự submit lại khi chưa rõ lần trước đã tạo dữ liệu chưa.

Khi lỗi harness lặp lại, dừng phần bị ảnh hưởng, lưu chẩn đoán ngắn và sửa/kiểm chứng trước khi mở rộng chạy. Không tạo hàng loạt probe, framework hoặc dịch vụ phụ để tiếp tục một luồng chưa ổn định. Chi tiết execution/bug ở [execution-and-bugs](references/execution-and-bugs.md).

## Báo cáo và giới hạn

Đọc [report-contract](references/report-contract.md) khi tổng hợp; [template report](assets/feature-report.template.md) là gợi ý, chỉ dùng mục phù hợp. Đọc [AI gap analysis](references/ai-gap-analysis.md) khi được giao phần này; dùng bản đầu/review có nguồn, không dựng lại lịch sử hoặc bịa gap.

HW02 yêu cầu bug trong Markdown và GitHub Issues kèm ảnh; bổ sung ảnh chụp trang issue theo yêu cầu nộp bài của người dùng. Khi nhiệm vụ bao gồm đăng Issues và tracker đã rõ, dùng quyền đã được giao để làm đầy đủ, không hỏi lại xác nhận. Task chỉ sửa skill, thiết kế hay chỉ lập bản nháp không tự cho phép đăng. Thiếu đích hoặc quyền đăng thì giữ nội dung sẵn có và nêu đúng phần còn thiếu. Report-only dùng kết quả/evidence đã có, không tự chạy lại SUT để đăng issue. Kiểm tra số liệu, URL, ảnh nhúng và ảnh trang issue trước khi nhận đã hoàn tất; issue đã đăng nhưng thiếu ảnh trang thì ghi rõ trạng thái đó.

Không tự ghi AI audit, commit/push, upload video hoặc nộp bài. Chỉ đọc [demo](references/demo.md) khi chuẩn bị demo; [research](references/research.md) lưu nguồn phương pháp.
