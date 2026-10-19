---
name: domain-bva-testing
description: Thiết kế và thực hiện kiểm thử từ đặc tả bằng Domain Testing và Boundary Value Analysis, giải thích từng bước, đối chiếu AI gaps và báo lỗi có bằng chứng. Dùng cho HW02 EShop hoặc feature khác có đặc tả; hỗ trợ Web, API và Mobile, không tự sửa nghiệp vụ SUT.
---

# Domain Testing + BVA — trợ lý kiểm thử theo từng bước

Nhận một feature và các nguồn liên quan, rồi thực hiện phần được giao theo bốn nhiệm vụ: **Domain Testing → Boundary Value Analysis → AI gap analysis → Bug reporting**. Execution cung cấp bằng chứng cho hai nhiệm vụ sau. Không biến yêu cầu “dùng skill” thành một prompt chung sinh test và kết luận đã kiểm thử xong.

Đây là bộ kỹ thuật có thể đóng gói cùng bài nộp. Không chứa thông tin sinh viên, đường dẫn cá nhân, số liệu chạy sẵn hoặc quyền Git/GitHub mặc định. Nội dung được viết mới sau khảo sát cộng đồng; nguồn, lựa chọn và giới hạn nằm ở [research](references/research.md).

## Đầu vào và cách bắt đầu

Xác định từ task, nguồn hiện có hoặc hỏi đúng phần thiếu:

- Feature, phạm vi/pool nếu có; requirement và API contract liên quan.
- Tài liệu bài giảng/phương pháp được giao; đặc biệt định nghĩa Domain Testing và biến thể BVA.
- Repo/commit SUT, đường chạy, lớp kiểm thử (Web/native/API), môi trường và dữ liệu chuẩn bị.
- Phần được giao: chỉ design, design + execution, review, hay toàn bộ; thư mục output và tracker khi cần đăng bug.

Đọc hướng dẫn áp dụng và tài liệu hiện có. Tận dụng thông tin đã biết, không bắt người dùng điền lại một bảng hỏi mỗi lần. Gặp thiếu nguồn thì làm phần độc lập; chỉ dừng hành động phụ thuộc thực sự vào điểm chưa rõ. Yêu cầu chỉ thiết kế không cho phép tự chạy app, reset dữ liệu hoặc đăng issue.

Ghi `method_profile` trong báo cáo:

| Profile | Điều kiện sử dụng |
| --- | --- |
| `lecture-aligned` | Đã đọc bài giảng; ghi file/mục/phiên bản và áp dụng đúng cách dạy |
| `reference-provisional` | Chưa có slide; dùng nguồn kỹ thuật trong bộ này để soạn nháp, chưa xác nhận phù hợp bài giảng |

Đề HW02 §6 yêu cầu giải thích từng bước và xem lại bài giảng; chính đề không cung cấp thuật toán Domain Testing chi tiết. Không tự đặt một thứ tự bước là quy trình chính thức của môn. Khi slide được bổ sung, đối chiếu mô hình/biên/coverage, giữ lịch sử sửa thay vì giả vờ đã dùng đúng từ đầu.

## Quy trình

### 0. Test basis và bản thiết kế ban đầu

Đọc đặc tả trước, dùng source để tìm luồng/điểm quan sát và nghi vấn, không dùng lỗi implementation làm expected. Lập rule IDs và nguồn; tách **confirmed**, **assumption**, **unresolved**. Các giả định chưa xác nhận không dùng để kết luận bug chắc chắn.

Xác định biến dữ liệu, biến trạng thái/thời gian cần thiết, đơn vị đo và điều kiện trước. Phân biệt yêu cầu nghiệp vụ với giới hạn biểu diễn, giới hạn UI và dữ liệu seed. Giữ một snapshot thiết kế AI ban đầu để phục vụ gap analysis; bản này không phải log hội thoại đầy đủ.

### 1. Domain Testing

Đọc [domain-testing](references/domain-testing.md), rồi tạo:

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

### 3. Review, execution và AI gap analysis

Đọc [ai-gap-analysis](references/ai-gap-analysis.md). Trước chạy, kiểm tra dữ liệu/expected/khả năng tiếp cận từng miền và các phụ thuộc. Tự tiếp tục phần thiết kế nháp có đủ nguồn; không tự nhận người học đã review vì agent vừa kiểm tra lại.

Nếu task cho phép execution, chạy theo [execution-and-bugs](references/execution-and-bugs.md): ghi setup, phiên bản, lớp chạy, actual, timestamp, status và evidence thật. Thiếu field/control của SUT là actual hoặc blocker cần giải thích, không phải lý do bỏ TC để tăng tỷ lệ đẹp.

Sau review/chạy, so sánh snapshot ban đầu với các bổ sung/sửa có nguồn. Báo lỗi hoặc test AI bỏ sót thực sự, nguyên nhân có căn cứ, độ chắc chắn và kết quả kiểm tra lại. Không bịa một “AI missed” từ lỗi đã được AI nêu trước khi thiết kế hoặc từ case chưa chạy.

### 4. Bug reporting

Với mỗi sai khác có oracle và bằng chứng, chuẩn bị báo cáo Markdown theo [execution-and-bugs](references/execution-and-bugs.md). Phân biệt nghi vấn static, bug tái hiện, lỗi setup/harness và test flaky. Dẫn screenshot, test/run và requirement; không sửa SUT/assertion để làm test pass.

Đối với HW02, đích đăng bug là **GitHub Issues của nhóm** theo đề §6, kèm ảnh bug; fork cá nhân không tự thay thế trang nhóm. Nếu đã được giao đăng và có đích/quyền rõ thì thực hiện, không hỏi lại. Chưa được giao thì hoàn thành nội dung/ảnh local và ghi phần còn thiếu; bản local chưa phải issue đã đăng. Kiểm tra trùng issue trước khi tạo, không tự bình luận/nhắn người khác.

## Đầu ra

Dùng [report-contract](references/report-contract.md) và `assets/feature-report.template.md` để tạo/cập nhật báo cáo. Mặc định một báo cáo feature, một snapshot thiết kế ban đầu và evidence gắn run; chỉ tách thêm dữ liệu/script khi cần chạy, không tạo báo cáo phụ cho mọi lần gọi.

Đáp ứng rõ bốn phần §6, kèm traceability **Rule → Domain/Boundary → TC → Run → Bug → Issue** và kết luận còn thiếu. Expected có nguồn; dữ liệu chưa chạy không được có actual/pass giả. Khi làm feature khác, đọc lại đặc tả thay vì tái dùng ngưỡng/FR/test data của EShop.

Nếu bài yêu cầu commit từng bước, giữ đầu ra theo bước có thể commit độc lập và nhắc phần Git chưa hoàn tất. Chỉ commit/push khi có ủy quyền; không dựng lịch sử giả sau khi làm xong. Không đặt tối thiểu số test/bug, code coverage %, framework hay CI làm tiêu chí môn nếu đề không có.

## AI audit và demo

Giữ được prompt/output thật, snapshot, diff và nguồn review cho log/audit. Nếu phiên có skill ghi AI log và đã được giao dùng, chuyển các nguồn này cho quy trình đó; nếu không, bảo toàn dữ liệu hiện có và báo phạm vi chưa ghi, không bịa log. Skill này không phụ thuộc vào một công cụ ghi log riêng để chạy.

Đọc [demo](references/demo.md) khi chuẩn bị §7: dùng skill trên một feature hoàn chỉnh, quay nguồn → Domain → BVA → review → chạy thật → gap/bug → summary. Chỉ có file skill hoặc video sinh test chưa chứng minh demo đầu cuối. Không tự upload, tạo YouTube link hoặc nhận đã quay video khi chưa thực hiện.

Kết thúc một lượt bằng file đã tạo/sửa, phương pháp đang dùng, số liệu có nguồn và phần tiếp theo. Nói rõ kết quả là design-only, đã chạy, đã được người học review hay còn provisional. Không dùng lời khẳng định “đủ 100 điểm” thay cho bằng chứng.
