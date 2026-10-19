# Dữ liệu báo cáo và truy vết

Dùng `assets/feature-report.template.md` khi được giao báo cáo feature; giữ tài liệu hiện có khi cập nhật. Bộ TC và mô hình Domain/BVA là đầu vào đã thiết kế, được dẫn chiếu/chèn đúng phiên bản; không tự sinh lại để hoàn thiện template. Không điền số liệu giả.

## Chuỗi ID

Giữ hệ thống ID đã có, hoặc dùng `<feature>-R01`, `-D01`, `-B01`, `-TC01`, `-RUN01`, `-BUG01`, `-GAP01` khi chưa có. Đây là quy ước gợi ý, không phải mã giảng viên. Rule ID nội bộ không thay FR gốc.

| Đối tượng | Nội dung |
| --- | --- |
| Rule | ID, điều kiện/expected, nguồn, confirmed/assumption/unresolved |
| Domain | ID, biến/predicate, rule IDs, rationale, điểm đại diện |
| Boundary | ID, rule/domain IDs, hai phía/dấu bằng, đơn vị/step, profile, coverage items |
| Test | ID, technique labels, rule/domain/boundary-item IDs, lớp chạy, precondition, dữ liệu thật, steps, expected, nguồn expected |
| Run | ID, TC/revision, actual, status, thời gian, executor, environment/commit, evidence và bug liên quan |
| Evidence | ID, TC/run/bug liên quan, file hoặc entry log, capture time, trạng thái/bước chứng minh, nguồn/derivative nếu có |
| Gap | ID, bản AI ban đầu, thiếu/sai, nguồn phát hiện, nguyên nhân/độ chắc chắn, sửa/ai làm/kết quả |
| Bug | ID, oracle, TC/run, expected/actual, repro, screenshot, trạng thái và issue URL |

Không ép một test phải có cả domain ID và boundary ID: test Domain chỉ ánh xạ mục tiêu tương ứng; test bổ trợ UI không tự trở thành BVA. TC cùng dữ liệu nhưng khác precondition/layer/oracle có thể là TC khác; chỉ gộp khi vẫn chứng minh được từng mục tiêu.

## Coverage và số liệu

- Công bố tập requirement/domain/boundary items trong phạm vi và mục chưa rõ. Mỗi item có TC IDs và bằng chứng exercise nếu đã chạy.
- Tính riêng coverage thiết kế, coverage đã exercise và tỷ lệ pass. Không dùng count test nhiều để chứng minh đủ mọi miền.
- Lấy summary từ cùng bộ TC và run/revision được công bố; giữ lịch sử rerun riêng. Không trộn kết quả từ SUT commits khác mà không giải thích.
- Đếm bug theo bug IDs được xác nhận, giữ static suspected riêng. Một bug ảnh hưởng nhiều test không nhân thành nhiều bug.

## Hoàn tất phần được giao

Kết quả và số liệu phải truy vết tới TC/run/evidence thực; ghi đúng phần chưa chạy hoặc chưa xác minh. Chưa có review của người học thì giữ trạng thái đó. Không yêu cầu lập đủ báo cáo bài tập, AI audit hoặc demo để kết thúc một task chỉ chạy test/viết summary.

Theo [quy cách evidence](evidence.md), ảnh cần xuất mặc định là JPG, được dẫn/nhúng với caption; giữ chỉ mục nối tới kết quả TC và bug. Tạo đúng định dạng tài liệu task/đề yêu cầu khi được giao xuất báo cáo, gồm Markdown + PDF cho HW02 trong phạm vi đó; kiểm tra ảnh, liên kết và số liệu ở bản xuất cuối.

Khi được giao tổng hợp HW02, giữ bốn phần Domain/BVA/gaps/bugs theo đề: lấy hai phần thiết kế từ bộ đầu vào, thêm kết quả/gap/bug có nguồn. Nếu còn thiếu thiết kế, slide, review, issue, audit, commit hoặc demo thì ghi đúng phần thiếu, không tự nhận toàn bộ HW02 đã hoàn tất.
