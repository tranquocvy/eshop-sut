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

## Ca bổ sung để tăng coverage

- Chủ động thêm ca có ích cho feature, kể cả ngoài rule viết rõ, theo quyền đã giao; không đợi review hay phê duyệt từng TC. Chọn theo miền/biên, đường vào, trạng thái hoặc rủi ro chưa được kiểm tra; không có quota TC hay yêu cầu lấy toàn bộ tổ hợp.
- Với mỗi ca bổ sung, ghi khoảng trống/rủi ro cần bao phủ, rationale và nguồn oracle. Có thể ghi ngay trong bảng hoặc nhóm dùng chung, không bắt thêm tài liệu hay cột cho mỗi TC. Truy vết tới requirement nếu đã có; nếu chưa, dùng ID assumption/quy ước đề xuất, không tạo FR giả.
- Tự chọn expected tạm thời khi có căn cứ hợp lý và ghi rõ giả định do AI đề xuất, chưa được sinh viên xác nhận. Ca như trim/Unicode/tên trùng có thể được thêm theo policy đề xuất; không gọi sai khác với policy đó là vi phạm đặc tả chắc chắn. Nếu không chọn được oracle có căn cứ, ghi mục tiêu khảo sát cùng phần chưa xác định và tách khỏi các TC có thể kết luận pass/fail.
- Giữ coverage của rule xác nhận và coverage theo giả định/khảo sát đọc phân biệt được. Bổ sung miền/biên vào inventory khi cần; không dùng tỷ lệ trên tập giả định để khẳng định toàn bộ requirement hay feature đã được bao phủ. Độ dài lớn chỉ là dữ liệu robustness nếu chưa có biên có căn cứ; không tự biến thành giới hạn nghiệp vụ hoặc BVA xác nhận.
- Khi mở rộng bộ test đã có, giữ ID cũ, thêm ID mới và cập nhật truy vết/rationale. Không tự đổi expected đã được duyệt; ca dùng oracle đề xuất khác phải ghi riêng để người đọc thấy sự khác biệt.

## Mức diễn giải

- **Sinh nhanh:** bảng TC, tóm tắt nguồn/quy tắc và giả định, lý do chọn điểm hoặc liên kết miền/biên đủ hiểu. Có thể đặt các mục tiêu đã bao phủ trong cột rationale thay vì nhiều bảng riêng.
- **Giải thích từng bước:** thêm bảng rules/variables/domains, inventory biên, phương pháp chọn điểm, truy vết và coverage thiết kế. Áp dụng khi đề/task yêu cầu, như phần Domain/BVA của HW02 §6.

Không cần người dùng chọn một mã mode; suy ra mức chi tiết từ yêu cầu và tài liệu được giao.

## Kiểm tra trước khi kết thúc

Test có expected từ requirement hoặc assumption/quy ước đề xuất được ghi rõ, input thực hiện được về mặt thiết kế, không vô tình vi phạm điều kiện khác che lỗi mục tiêu. Phần chưa rõ không ngăn tự bổ sung ca có giá trị; giữ trạng thái assumption/unresolved thay vì bịa nguồn oracle. Coverage thiết kế chỉ tính trên inventory có công bố, không gọi là đã chạy hoặc bao phủ mọi hành vi phần mềm.

Đây là đầu vào độc lập cho người hoặc công cụ thực thi về sau. Khi cần bàn giao, dẫn bộ TC và phiên bản/baseline thiết kế hiện có; giữ bản AI ban đầu/diff nếu đã được yêu cầu lưu. Không tự gọi bước thực thi, AI log, AI gap analysis chính thức hay báo cáo kết quả sau khi bảng TC hoàn tất.
