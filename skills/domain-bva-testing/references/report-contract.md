# Dữ liệu báo cáo và truy vết

Dùng `assets/feature-report.template.md` cho một feature; giữ tài liệu hiện có khi được giao cập nhật. Không tự điền số liệu giả vào template.

## Chuỗi ID

Giữ hệ thống ID đã có, hoặc dùng `<feature>-R01`, `-D01`, `-B01`, `-TC01`, `-RUN01`, `-BUG01`, `-GAP01` khi chưa có. Đây là quy ước gợi ý, không phải mã giảng viên. Rule ID nội bộ không thay FR gốc.

| Đối tượng | Nội dung |
| --- | --- |
| Rule | ID, điều kiện/expected, nguồn, confirmed/assumption/unresolved |
| Domain | ID, biến/predicate, rule IDs, rationale, điểm đại diện |
| Boundary | ID, rule/domain IDs, hai phía/dấu bằng, đơn vị/step, profile, coverage items |
| Test | ID, technique labels, rule/domain/boundary-item IDs, lớp chạy, precondition, dữ liệu thật, steps, expected, nguồn expected |
| Run | ID, TC/revision, actual, status, thời gian, executor, environment/commit, evidence và bug liên quan |
| Gap | ID, bản AI ban đầu, thiếu/sai, nguồn phát hiện, nguyên nhân/độ chắc chắn, sửa/ai làm/kết quả |
| Bug | ID, oracle, TC/run, expected/actual, repro, screenshot, trạng thái và issue URL |

Không ép một test phải có cả domain ID và boundary ID: test Domain chỉ ánh xạ mục tiêu tương ứng; test bổ trợ UI không tự trở thành BVA. TC cùng dữ liệu nhưng khác precondition/layer/oracle có thể là TC khác; chỉ gộp khi vẫn chứng minh được từng mục tiêu.

## Coverage và số liệu

- Công bố tập requirement/domain/boundary items trong phạm vi và mục chưa rõ. Mỗi item có TC IDs và bằng chứng exercise nếu đã chạy.
- Tính riêng coverage thiết kế, coverage đã exercise và tỷ lệ pass. Không dùng count test nhiều để chứng minh đủ mọi miền.
- Lấy summary từ cùng bộ TC và run/revision được công bố; giữ lịch sử rerun riêng. Không trộn kết quả từ SUT commits khác mà không giải thích.
- Đếm bug theo bug IDs được xác nhận, giữ static suspected riêng. Một bug ảnh hưởng nhiều test không nhân thành nhiều bug.

## Điều kiện hoàn tất một feature

Có bốn phần Domain/BVA/gaps/bugs cùng giải thích từng bước, nguồn expected và traceability. Design-only không có số liệu thực thi giả; execution có phần chưa chạy phải nói rõ. Chưa có review của người học thì giữ trạng thái đó, dù agent đã tự kiểm tra. Chưa có slide thì method profile còn provisional. Chưa đăng issue/ghi AI audit/commit/quay demo thì không nhận đủ các hạng mục đó.
