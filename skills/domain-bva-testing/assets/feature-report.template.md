# Báo cáo kiểm thử — <feature>

> Template triển khai, chưa phải dữ liệu/kết quả bài thật. Điền từ nguồn; xóa hướng dẫn minh họa khi hoàn thiện.

## 1. Phạm vi, test basis và phương pháp

Feature/pool, requirement/API/bài giảng, method_profile, commit SUT, lớp kiểm thử, dữ liệu, câu hỏi còn mở. Nêu phần nào confirmed, assumption hoặc unresolved.

## 2. Domain Testing — giải thích từng bước

### Rules, variables và mô hình miền

| ID | Biến/điều kiện | Rule/source | Miền/predicate | Rationale và điểm đại diện |
| --- | --- | --- | --- | --- |

### Domain test cases và coverage

| TC ID | Rule/domain IDs | Precondition/input | Steps | Expected và nguồn | Lớp chạy |
| --- | --- | --- | --- | --- | --- |

Nêu cách chọn điểm theo bài giảng, ràng buộc liên biến, coverage thiết kế và phần chưa bao phủ.

## 3. Boundary Value Analysis — giải thích từng bước

| Boundary ID | Rule và hai miền | Dấu bằng/đơn vị/step | Profile, coverage items | TC IDs |
| --- | --- | --- | --- | --- |

Giải thích phép suy ra, điểm không biểu diễn được và phần không có thứ tự. Không tự điền max hoặc tỷ lệ coverage khi chưa có inventory.

## 4. Review và execution

Ai review, review gì, chỉnh sửa nào có nguồn. Nếu chưa review/chưa chạy thì ghi rõ.

| Run ID | TC/revision | Environment/commit/layer | Actual | Status | Evidence/Bug |
| --- | --- | --- | --- | --- | --- |

Tách coverage thiết kế, coverage đã exercise và pass rate; không đếm trùng TC mang hai nhãn kỹ thuật.

## 5. AI gap analysis

| Gap ID | Bản AI ban đầu | Thiếu/sai | Nguồn phát hiện | Nguyên nhân/độ chắc chắn | Sửa/ai làm/kết quả |
| --- | --- | --- | --- | --- | --- |

Nếu chưa phát hiện gap, ghi phạm vi đối chiếu và kết quả thực, không bịa một trường hợp.

## 6. Bug reporting

| Bug ID | Requirement/oracle | TC/run | Expected/actual | Repro/evidence | Trạng thái/issue URL |
| --- | --- | --- | --- | --- | --- |

Mỗi bug có screenshot khi xác nhận và theo yêu cầu bài. Nghi vấn source giữ nhãn static/suspected, không tính thành bug runtime đã tái hiện.

## 7. Tổng kết và truy vết

Unique test designed, executed, passed, failed, blocked/not run; bugs đã xác nhận; coverage phạm vi; AI log/artifact sources; commit từng bước và link demo nếu đã có. Phần chưa hoàn tất phải được ghi đúng, không tự điền số liệu minh họa.
