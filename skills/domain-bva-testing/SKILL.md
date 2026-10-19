---
name: domain-bva-testing
description: Sinh và rà soát test case từ đặc tả bằng Domain Testing và Boundary Value Analysis. Dùng khi cần thiết kế TC, phân tích miền hoặc chọn giá trị biên cho Web, API hay Mobile; kết thúc ở bộ test, không thực thi SUT hay lập báo cáo kết quả.
---

# Domain Testing + BVA — thiết kế và sinh test case

Nhận đặc tả feature và sinh bộ test theo luồng **Test basis → Domain Testing → BVA → Kiểm tra thiết kế → Test cases**. Dừng khi bộ test đáp ứng phạm vi được giao. Không tự khởi động ứng dụng, chạy test trên SUT, chụp bằng chứng, tạo bug report hay gọi skill khác sau khi sinh TC.

Đây là bộ thiết kế test có thể dùng độc lập hoặc đóng gói cùng bài nộp. Nguồn khảo sát và phương pháp nằm ở [research](references/research.md). Execution, AI gap analysis chính thức và báo cáo kết quả thuộc skill riêng `test-execution-reporting`, chỉ dùng khi người dùng giao phần đó.

## Đầu vào và cách bắt đầu

Xác định từ task, nguồn hiện có hoặc hỏi đúng phần thiếu:

- Feature, phạm vi/pool nếu có; requirement và API contract liên quan.
- Tài liệu bài giảng/phương pháp được giao; đặc biệt định nghĩa Domain Testing và biến thể BVA.
- Lớp mục tiêu của TC (Web/native/API), dữ liệu và precondition; repo/commit hoặc source liên quan nếu cần đọc thêm để hiểu luồng.
- Phần thiết kế được giao: Domain, BVA hoặc cả hai; mức diễn giải và định dạng đầu ra. Tận dụng dữ liệu đã có, không yêu cầu setup SUT chỉ để sinh TC.

Đọc đặc tả/bài giảng được cung cấp và phần source thực sự liên quan; không quét toàn repo khi đã đủ test basis. Gặp thiếu nguồn thì tiếp tục phần thiết kế có căn cứ, đánh dấu giả định/câu hỏi đúng chỗ. Thiếu môi trường chạy không chặn thiết kế test.

Khi yêu cầu “sinh TC nhanh”, trả bảng TC và các giả định/lý do chọn dữ liệu cần thiết; không dựng một báo cáo feature đầy đủ. Khi bài yêu cầu giải thích từng bước, trình bày thêm mô hình miền, inventory biên và coverage theo [quy cách bộ test](references/test-case-contract.md). Cả hai cách đều kết thúc ở thiết kế. Chỉ sinh TC cho kỹ thuật được giao; yêu cầu chỉ BVA có thể cần xác định miền nền nhưng không bắt buộc sinh thêm bộ TC Domain riêng.

Khi task cần giải thích phương pháp, nêu `method_profile` trong phần mô tả thiết kế:

| Profile | Điều kiện sử dụng |
| --- | --- |
| `lecture-aligned` | Đã đọc bài giảng; ghi file/mục/phiên bản và áp dụng đúng cách dạy |
| `reference-provisional` | Chưa có slide; dùng nguồn kỹ thuật trong bộ này để soạn nháp, chưa xác nhận phù hợp bài giảng |

Đề HW02 §6 yêu cầu giải thích từng bước và xem lại bài giảng; chính đề không cung cấp thuật toán Domain Testing chi tiết. Không tự đặt một thứ tự bước là quy trình chính thức của môn. Khi slide được bổ sung, đối chiếu mô hình/biên/coverage, giữ lịch sử sửa thay vì giả vờ đã dùng đúng từ đầu.

## Quy trình

### 0. Test basis và bản thiết kế ban đầu

Đọc đặc tả trước, dùng source để tìm luồng/điểm quan sát và nghi vấn, không dùng lỗi implementation làm expected. Lập rule IDs và nguồn; tách **confirmed**, **assumption**, **unresolved**. Các giả định chưa xác nhận không dùng để kết luận bug chắc chắn.

Xác định biến dữ liệu, biến trạng thái/thời gian cần thiết, đơn vị đo và điều kiện trước. Phân biệt yêu cầu nghiệp vụ với giới hạn biểu diễn, giới hạn UI và dữ liệu seed. Khi cần theo dõi AI gaps về sau, giữ bản thiết kế đầu qua phiên bản file hoặc nguồn hội thoại hiện có; không bắt buộc tạo báo cáo/snapshot riêng cho mọi lượt sinh TC nhanh.

### 1. Domain Testing

Đọc [domain-testing](references/domain-testing.md), rồi phân tích các nội dung sau. Khi sinh nhanh, có thể tóm tắt trong TC/rationale; tách thành bảng chi tiết khi task yêu cầu:

1. Bảng biến và các rule chi phối.
2. Mô hình miền/partition cùng lý do chọn cách phân chia, ranh giới và ràng buộc liên biến.
3. Các điểm đại diện, lý do chúng có khả năng phát hiện sai phạm và cách hiện thực dữ liệu.
4. Domain test cases cụ thể và truy vết tới mô hình/rule.
5. Bảng coverage thiết kế và các khoảng chưa bao phủ.

Không chỉ liệt kê happy path hoặc bảng EP rồi tự nhận đã làm mọi biến thể Domain Testing. Nếu bài giảng có ON/OFF/IN/OUT hay kỹ thuật miền nhiều chiều, áp dụng với đúng định nghĩa và chứng minh vị trí điểm; không gán các nhãn này cho mọi chuỗi email hoặc role.

### 2. Boundary Value Analysis

Đọc [boundary-value-analysis](references/boundary-value-analysis.md). Lập inventory các miền có thứ tự, biên, giá trị lân cận, độ phân giải và nguồn. Chọn profile BVA theo slide; nếu chưa có, ghi rõ đề xuất kỹ thuật và giới hạn.

Đối với các partition rời rạc liền kề đã xác định, có thể dùng `scripts/boundary_points.py` để kiểm tra phép tính theo `istqb-2` hoặc `istqb-3`. Script không tự tìm requirement, oracle hoặc tất cả ranh giới của feature. Khi phương pháp môn khác, ghi phương pháp đó và không đổi tên tập điểm thành ISTQB 3-value.

Giữ phần diễn giải BVA riêng với Domain Testing dù một TC có thể mang cả hai nhãn. Không đếm cùng TC hai lần trong tổng số test. Độ bao phủ thiết kế không phải độ bao phủ đã thực thi hoặc tỷ lệ pass.

### 3. Kiểm tra và hoàn thiện thiết kế

Đối chiếu từng rule/miền/biên với TC: dữ liệu và expected có nguồn, đúng dấu bằng/độ phân giải, giữ các điều kiện khác hợp lệ, có precondition để tiếp cận rule mục tiêu. Bổ sung ca thiếu và gộp ca trùng khi vẫn giữ được truy vết. Đây là tự kiểm tra thiết kế của AI, không phải xác nhận sinh viên đã review.

Nếu sửa bộ test đã có, giữ ID và bản gốc/diff cần đối chiếu. Khi cần AI gap analysis về sau, giữ được phiên bản AI ban đầu; không tái tạo một bản “ban đầu” từ kết quả cuối. Không cần viết bảng gap, bug report hoặc AI Critique trong lượt sinh TC.

## Đầu ra

Dùng [test-case-contract](references/test-case-contract.md); khi cần lưu file, có mẫu `assets/test-cases.template.md`. Đầu ra tối thiểu là **TC ID, technique, rule/domain/boundary liên quan, precondition, input, steps, expected và nguồn expected**. Trình bày trong chat hoặc file theo yêu cầu, giữ định dạng/bộ ID đã có.

Truy vết của skill này dừng ở **Rule → Domain/Boundary → TC**. Nếu cung cấp số lượng, chỉ tính unique TC đã thiết kế và coverage thiết kế có mẫu số rõ. Không điền Actual/Pass/Fail từ suy đoán; nếu file hiện có yêu cầu trạng thái thì để `Not Run`. Không sửa kết quả chạy thật đang có khi chỉ cập nhật thiết kế.

Chạy helper tính điểm biên là kiểm tra phép suy ra dữ liệu, không phải thực thi test trên SUT. Khi làm feature khác, đọc lại đặc tả thay vì tái dùng ngưỡng/FR/test data của EShop. Không thêm quota test, coverage %, framework, execution, report hay demo làm điều kiện để hoàn tất một lượt sinh TC.
