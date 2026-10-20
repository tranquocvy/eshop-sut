# Hồ sơ AI — HW02

Hồ sơ của Trần Quốc Vỹ (23120410), được bổ sung vào Git ngày 20/10/2026 sau khi trước đó được quản lý local. Timestamp trong log giữ theo hội thoại gốc ngày 19–20/10/2026.

- [Prompt Log](23120410_HW02_PromptLog.md): 39 mục P-000–P-038 theo phạm vi đã được giao ghi log.
- [AI Audit Report](ai-audit.md): 12 artifact, có nhận xét và lịch sử sửa.
- [AI Disclosure](ai-disclosure.md): khai báo công cụ, đóng góp và cách rà soát.
- [Các phiên bản artifact](artifacts.md): output đầu, bản sửa và commit đối chiếu.
- [Đề HW02](references/hw02-assignment.md), [mẫu Audit](references/ai-audit-template.md), [mẫu Disclosure](references/ai-disclosure-template.md).

## Cách lưu

Đây là nơi cập nhật chính cho hồ sơ AI của HW02. `history/` chỉ giữ những output đầu chưa có trong Git và hai diff thiết kế; code, report, ảnh và skill đã có được dẫn tới commit tương ứng. `verification/` giữ hai output kiểm tra công cụ được audit dẫn chiếu.

Dữ liệu trích xuất/đồng bộ trong `_data/` được giữ local và đã ignore. Bản hồ sơ local trước khi chuyển nằm ngoài repo tại `HW02/Final/`; dùng làm bản lưu lịch sử. Các đường dẫn cũ trong prompt/output trích nguyên văn vẫn phản ánh thời điểm trao đổi; link điều hướng của audit/disclosure đã chuyển sang cấu trúc docs và các phiên bản Git.

## Phạm vi hiện tại

Hồ sơ gồm xây/sửa skill, thiết kế/implementation/execution Mobile Registration, bổ sung GitHub Issues/evidence và thiết kế/implementation/execution Category Management. Category đã chạy 33 TC: 25 pass, 8 fail, 0 blocked; ba bug có Issues #9–#11 và ảnh trang issue. Đây là hồ sơ theo các lượt đã được chọn, tiếp tục cập nhật khi làm phần việc tiếp theo. Nhận xét audit đề xuất và chữ ký được giữ đúng trạng thái trong biểu mẫu.

Đợt bổ sung trước ghi đúng bốn prompt P-027–P-030 và 12 phản hồi AI: kiểm tra thiếu Issues, cập nhật skill, đăng/chụp issue và thêm quy tắc link evidence cho từng TC. Cập nhật hai artifact hiện có A-02/A-05, không tăng số artifact theo từng issue/ảnh. Các lượt sửa report/giải thích log/commit sau đó không thuộc bốn prompt được chọn. Giữ nguyên phần Prompt Log cũ đã chỉnh tay; dữ liệu đồng bộ tiếp tục nằm trong `_data/` đã ignore.

Đợt T03 bổ sung đúng **hai prompt P-031/P-032 và 13 phản hồi AI**: code từ hai tài liệu đã duyệt, sau đó execution/report theo skill. Thêm A-07 (implementation) và A-08 (execution/report); giữ bản code ban đầu trong history và diff thay đổi harness. Report/results/12 JPG đã commit local `94fd43c`, sinh viên đã kiểm tra report. Không thêm các lượt hỏi loại test, đồng bộ T02 hoặc commit thành prompt; không chạy lại SUT trong lúc ghi log. Phần Category “Not Run” trong bản thiết kế giữ đúng mốc lịch sử.

Đợt T05 bổ sung **hai prompt P-037/P-038 và bảy phản hồi AI nguyên văn**, cùng phần đối chiếu năm lượt hỏi/đáp/sửa trạng thái review. Thêm một artifact A-11 cho cặp design/TC FR-02, không thêm artifact cho thao tác Git. Giữ bản đầu thực tế, diff trạng thái và bản đã review tại commit `4bb5158`. Các phần Prompt Log cũ chỉnh tay được bảo toàn; helper chỉ render trên staging canonical rồi nối phần mới. Không đưa prompt execution/report vào phạm vi lần này. Vỹ đã xác nhận report; dữ kiện này được ghi nhận riêng, chưa thay việc bổ sung log execution khi được giao.
