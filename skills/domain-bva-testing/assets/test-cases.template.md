# Test cases — <feature>

> Mẫu thiết kế; bắt đầu từ đặc tả và chủ động bổ sung TC có giá trị cho coverage. Chỉ giữ mức diễn giải task yêu cầu, không điền kết quả chạy giả.

## Test basis và giả định

Feature, nguồn requirement/API/bài giảng, lớp mục tiêu, phiên bản nguồn nếu biết; method_profile `lecture-aligned` hoặc `reference-provisional` khi áp dụng. Nêu assumption/unresolved.

Ca ngoài điều đặc tả viết rõ được tự bổ sung khi hữu ích, không chờ duyệt từng ca. Ghi lý do/rủi ro và oracle: requirement đã xác nhận hoặc assumption/quy ước do AI đề xuất. Expected tạm thời không được nhận là requirement hay là chính sách sinh viên đã chốt.

## Mô hình Domain và lựa chọn dữ liệu

| Domain ID | Biến / predicate | Rule và nguồn | Điểm đại diện | Lý do chọn |
| --- | --- | --- | --- | --- |

## BVA và lựa chọn giá trị biên

| Boundary ID | Rule / hai miền | Dấu bằng / đơn vị / step | Biến thể và coverage items | Lý do / ngoại lệ |
| --- | --- | --- | --- | --- |

## Test cases

| TC ID | Technique | Rule / Domain / Boundary ID | Precondition | Input | Steps | Expected và nguồn |
| --- | --- | --- | --- | --- | --- | --- |

## Kiểm tra thiết kế và coverage

Truy vết mục tiêu tới TC, trường hợp thiếu hoặc không áp dụng, số unique TC và coverage thiết kế nếu đã có inventory đầy đủ. Giữ ID/bản gốc/diff khi sửa bộ test hiện có. Không có Actual, Pass/Fail hoặc run evidence trong đầu ra thiết kế này.

Rà khoảng trống và tự thêm ca trước khi bàn giao. Nêu phần bao phủ requirement, phần theo giả định và mục tiêu khảo sát chưa đủ oracle; không gộp chúng để khẳng định đủ toàn feature. Không tăng TC bằng các biến thể trùng ý nghĩa.
