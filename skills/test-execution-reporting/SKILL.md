---
name: test-execution-reporting
description: Thực thi bộ TC đã có, lưu evidence truy vết tới từng kết quả, xuất ảnh JPG và báo cáo theo task/đề. Dùng khi chạy test, phân tích AI gaps hoặc tổng hợp test summary/bug report; hỗ trợ report-only từ dữ liệu thật, không tự sinh lại bộ TC.
---

# Thực thi test và báo cáo kết quả

Nhận **bộ TC đã thiết kế** và phần công việc được giao. Chạy test khi được yêu cầu, hoặc lập báo cáo từ dữ liệu đã có. Không bắt sinh lại TC bằng một skill khác trước khi dùng. Nguồn phương pháp báo lỗi và phạm vi tách skill nằm ở [research](references/research.md).

## Đầu vào và phạm vi

- Bộ TC/phiên bản, precondition, input, steps, expected và nguồn; nhận TC từ bất kỳ tác giả/công cụ nào.
- Phạm vi: execution, report-only, AI gap analysis, bug report hoặc kết hợp. Yêu cầu “viết report” không tự cho phép chạy lại app.
- Khi chạy: repo/commit, lớp Web/native/API, môi trường, cách setup và dữ liệu. Khi báo cáo: run/evidence thực đã có và scope của chúng.
- Khi phân tích AI gaps: bản AI ban đầu, bản sửa và lịch sử review; thiếu phần nào thì nói rõ, không phục dựng.
- Yêu cầu đầu ra của task/đề: nơi lưu báo cáo/evidence, ảnh cần có, định dạng tài liệu và tracker. Mặc định ảnh cần xuất dùng `.jpg` theo lựa chọn người dùng; đề chỉ định khác thì tuân định dạng đó và nêu rõ.

Tận dụng thông tin đã có. TC thiếu oracle/precondition thì làm phần độc lập và chỉ rõ mục chưa thể chạy; không tự mở rộng thành một đợt thiết kế Domain/BVA. Nếu runtime phát hiện cần thêm test, ghi đề xuất hoặc gap rồi giữ phần bổ sung riêng theo yêu cầu người dùng.

## 1. Thực thi khi được giao

Đọc [execution-and-bugs](references/execution-and-bugs.md). Kiểm tra setup, phiên bản, dữ liệu, khả năng tái hiện và tác động reset/seed trước chạy. Dùng runner hoặc công cụ phù hợp đang có; không bắt buộc dựng framework mới cho mọi feature.

Chạy đúng lớp của TC, ghi actual, thời gian, môi trường, status, exit code và evidence từ thao tác thật. Giữ ID/revision; không đổi expected theo code lỗi, sửa nghiệp vụ SUT hoặc bỏ failed/blocked để báo cáo đẹp. Test chưa chạy giữ `not_run`; API không tự chứng minh UI/native đã chạy.

## Evidence và ảnh JPG

Đọc [quy cách evidence](references/evidence.md) trước khi chạy hoặc xuất ảnh. Mỗi kết quả đã chạy phải có nguồn kiểm chứng phù hợp, truy được **TC/revision → Run → Evidence → Bug/Issue nếu có**. Ghi thời gian capture và môi trường; giữ lịch sử rerun, ảnh gốc và tên file ổn định theo run.

Khi task/đề cần screenshot, chụp từ phiên chạy thật và xuất JPG đọc được. Nếu nguồn là PNG, dùng `scripts/export_jpg.py` để chuyển định dạng thật; không đổi mỗi phần mở rộng và không tạo ảnh bằng AI. Báo cáo phải dẫn tới ảnh/log cụ thể, có caption nói rõ trạng thái nào được chứng minh. Không bắt mọi TC đều có JPG khi request/response hoặc runner log mới là evidence phù hợp.

## 2. AI gap analysis khi có phạm vi được giao

Đọc [ai-gap-analysis](references/ai-gap-analysis.md), đối chiếu bản AI ban đầu với review và kết quả chạy. Bỏ sót có thể được phát hiện từ review thiết kế mà chưa có runtime; khi đó chỉ kết luận thiếu/sai trong thiết kế, không nhận đã tái hiện bug.

Ghi case/rule/oracle bị thiếu hoặc sai, nguồn phát hiện, tác động, nguyên nhân có căn cứ hay giả thuyết, người thực hiện sửa và kết quả kiểm tra lại nếu có. Không tạo lỗi AI giả hoặc một bản “AI ban đầu” từ file cuối.

## 3. Bug report và GitHub Issues

Với sai khác có oracle và bằng chứng, rút gọn bước tái hiện; phân biệt bug sản phẩm với lỗi setup/harness, dữ liệu hoặc static suspected. Báo cáo gồm precondition, steps, expected/actual, phiên bản, TC/run và screenshot phù hợp. Chi tiết ở [execution-and-bugs](references/execution-and-bugs.md).

HW02 §6 yêu cầu bug trong Markdown và GitHub Issues của nhóm, kèm ảnh bug. Chuẩn bị nội dung local; đăng khi đã được giao với đích/quyền rõ, kiểm tra trùng và kiểm tra issue sau đăng. Không mặc định fork cá nhân là tracker nhóm. Bản local chưa phải issue đã đăng.

## 4. Tổng hợp và kết thúc

Dùng [report-contract](references/report-contract.md) và `assets/feature-report.template.md` khi cần báo cáo feature. Tái sử dụng phần thiết kế đã có bằng dẫn chiếu hoặc chèn đúng phiên bản; không chờ sinh lại mô hình Domain/BVA mới được báo kết quả.

Tổng hợp unique TC designed/executed/passed/failed/blocked/not run, coverage thực có bằng chứng, bug/gap và phần còn thiếu. Công bố cách đếm; không cộng rerun thành TC mới hay trộn commits/layers không giải thích. Report-only giữ nguyên dữ liệu nguồn, không tạo run/ảnh/actual giả; có thể xuất JPG từ ảnh nguồn đã có và ghi đúng thời gian capture ban đầu.

Đầu ra theo task: kết quả TC, chỉ mục evidence và ảnh JPG cần thiết; summary/bug/gap cùng định dạng báo cáo được yêu cầu. Khi giao xuất báo cáo theo HW02 §14, tạo Markdown + PDF trong phạm vi đó, kiểm tra layout và ảnh nhúng; không coi mới có Markdown là đã xuất PDF. Nếu thiếu công cụ thì giữ nguồn và báo đúng định dạng chưa tạo. Không tự ghi AI audit, commit/push, upload video hay nộp bài. Kịch bản demo phối hợp hai skill nằm ở [demo](references/demo.md), chỉ đọc khi chuẩn bị demo.
