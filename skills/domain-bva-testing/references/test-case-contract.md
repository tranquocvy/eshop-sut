# Quy cách bộ test được thiết kế

Dùng định dạng hiện có hoặc `assets/test-cases.template.md` khi cần lưu file. Yêu cầu sinh TC nhanh có thể trả trực tiếp bảng, không cần tạo thêm báo cáo.

## Dữ liệu bàn giao

| Thành phần | Nội dung |
| --- | --- |
| Test basis | Feature, requirement/nguồn expected, lớp mục tiêu, phiên bản nguồn nếu biết |
| Rule | ID, điều kiện/kết quả đúng, nguồn, confirmed/assumption/unresolved |
| Domain | ID, biến/predicate, rule, điểm đại diện và lý do |
| Boundary | ID, rule/domain, hai phía/dấu bằng, đơn vị/step, biến thể và coverage items |
| Test case | ID, technique, rule/domain/boundary-item liên quan, precondition, input cụ thể, steps, expected và nguồn expected |

Giữ ID đã có; khi cần mới dùng quy ước như `<feature>-R01`, `-D01`, `-B01`, `-TC01`. TC chỉ thuộc Domain không bắt buộc có boundary ID. TC mang cả hai nhãn chỉ tính một lần trong tổng số unique TC. Cùng input nhưng khác precondition/layer/oracle có thể là TC khác.

## Mức diễn giải

- **Sinh nhanh:** bảng TC, tóm tắt nguồn/quy tắc và giả định, lý do chọn điểm hoặc liên kết miền/biên đủ hiểu. Có thể đặt các mục tiêu đã bao phủ trong cột rationale thay vì nhiều bảng riêng.
- **Giải thích từng bước:** thêm bảng rules/variables/domains, inventory biên, phương pháp chọn điểm, truy vết và coverage thiết kế. Áp dụng khi đề/task yêu cầu, như phần Domain/BVA của HW02 §6.

Không cần người dùng chọn một mã mode; suy ra mức chi tiết từ yêu cầu và tài liệu được giao.

## Kiểm tra trước khi kết thúc

Test có expected từ nguồn, input thực hiện được về mặt thiết kế, không vô tình vi phạm điều kiện khác che lỗi mục tiêu. Giữ phần chưa rõ dưới dạng assumption/unresolved thay vì bịa oracle. Coverage thiết kế chỉ tính trên inventory có công bố, không gọi là đã chạy hoặc bao phủ mọi hành vi phần mềm.

Đây là đầu vào độc lập cho người hoặc công cụ thực thi về sau. Khi cần bàn giao, dẫn bộ TC và phiên bản/baseline thiết kế hiện có; giữ bản AI ban đầu/diff nếu đã được yêu cầu lưu. Không tự gọi bước thực thi, AI log, AI gap analysis chính thức hay báo cáo kết quả sau khi bảng TC hoàn tất.
