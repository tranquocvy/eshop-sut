# Báo cáo kiểm thử — <feature>

> Template báo cáo, chưa phải dữ liệu/kết quả bài thật. Lấy thiết kế từ bộ TC đầu vào và kết quả từ run thật. Chỉ dùng các phần thuộc task; không sinh lại TC để điền đủ mẫu.

## 1. Phạm vi, test basis và phương pháp

Feature/pool, file TC và phiên bản, requirement/API/bài giảng, method_profile từ thiết kế, commit SUT, lớp kiểm thử, dữ liệu, câu hỏi còn mở. Nêu phần nào confirmed, assumption hoặc unresolved.

## 2. Domain Testing — giải thích từng bước

Dẫn chiếu hoặc chèn phần thiết kế đã có; không phân tích và sinh lại trong lượt chỉ thực thi/report.

### Rules, variables và mô hình miền

| ID | Biến/điều kiện | Rule/source | Miền/predicate | Rationale và điểm đại diện |
| --- | --- | --- | --- | --- |

### Domain test cases và coverage

| TC ID | Rule/domain IDs | Precondition/input | Steps | Expected và nguồn | Lớp chạy |
| --- | --- | --- | --- | --- | --- |

Nêu cách chọn điểm theo bài giảng, ràng buộc liên biến, coverage thiết kế và phần chưa bao phủ.

## 3. Boundary Value Analysis — giải thích từng bước

Dẫn chiếu hoặc chèn inventory/TC BVA từ thiết kế đầu vào. Phần thiếu được ghi rõ để bổ sung riêng.

| Boundary ID | Rule và hai miền | Dấu bằng/đơn vị/step | Profile, coverage items | TC IDs |
| --- | --- | --- | --- | --- |

Giải thích phép suy ra, điểm không biểu diễn được và phần không có thứ tự. Không tự điền max hoặc tỷ lệ coverage khi chưa có inventory.

## 4. Review và execution

Ai review, review gì, chỉnh sửa nào có nguồn. Nếu chưa review/chưa chạy thì ghi rõ.

| Run ID | TC/revision | Environment/commit/layer | Timestamp | Actual | Status | Evidence ID / file / Bug |
| --- | --- | --- | --- | --- | --- | --- |

Tách coverage thiết kế, coverage đã exercise và pass rate; không đếm trùng TC mang hai nhãn kỹ thuật.

### Evidence và ảnh kết quả

Dẫn chỉ mục evidence của run. Chèn ảnh JPG thật khi task/đề yêu cầu, dùng đường dẫn tương đối và caption nêu TC/run, bước, thời gian capture và trạng thái chứng minh. Phân biệt ảnh symptom trên SUT với ảnh trang GitHub issue. Không để ảnh rời không liên kết tới actual.

| Evidence ID | TC / Run / Bug | File hoặc entry log | Capture time | Nội dung chứng minh / nguồn ảnh |
| --- | --- | --- | --- | --- |

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

Khi xuất theo task/đề, kiểm tra định dạng báo cáo, ảnh nhúng/caption đọc được, các file evidence tồn tại và số liệu nhất quán. Không nhận đã có PDF hoặc ảnh issue nếu chưa xuất/chụp thật.
