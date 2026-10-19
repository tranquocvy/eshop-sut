# Mô-đun 4 — Thực thi và báo lỗi

## Thực thi đúng lớp và đúng dữ liệu

Chỉ chạy khi task bao hàm execution. Trước chạy, đọc setup và kiểm tra các tác động reset/seed; không restart/reset một phiên đang có dữ liệu cần giữ. Tách sửa cấu hình môi trường khỏi sửa logic SUT, ghi rõ diff cần thiết.

Mỗi run ghi ID, thời gian có múi giờ, commit SUT/test, lớp Web/native/API, môi trường, fixture/setup, TC, actual và evidence. Request/response phải từ run thật; lưu exit code thật. Test runner trả lỗi cần được phân loại thay vì bỏ qua.

Status đề xuất: `passed`, `failed`, `blocked`, `not_run`. Khi summary dùng bốn trạng thái này, quy ước `executed = passed + failed`, `not_executed = blocked + not_run`; tổng unique TC = executed + not_executed. Nếu dùng quy ước khác thì công bố. Không đếm số lần rerun thành số TC thiết kế. Chỉ đánh dấu coverage item đã exercise nếu biết test thực sự đi tới nó.

Web responsive không phải native Mobile. API chạy được chỉ chứng minh API trong phạm vi đã kiểm tra; cart state/UI validation có thể khác lớp API. Với control chưa tồn tại, ghi actual thiếu control và bug/blocker liên quan thay vì sửa giao diện hoặc bỏ test.

## Xác định bug và tái hiện

1. Tìm oracle bị vi phạm và vị trí nguồn. Nếu chỉ là mong muốn/chưa rõ, ghi câu hỏi hoặc assumption, không khẳng định defect requirement.
2. Phân loại sản phẩm, môi trường/harness, dữ liệu/setup hoặc nghi ngờ flaky. Code đáng ngờ là static finding; không tự có screenshot/actual runtime.
3. Rút ngắn cách tái hiện nhưng giữ điều kiện cần, ghi chính xác input và dữ liệu. Tần suất ghi theo số lần thực đã thử, không mặc định 3/3 hay 5/5.
4. Kiểm tra issue liên quan nếu có tracker và quyền đọc; giữ bug ID ổn định. Nhiều symptom chung nguyên nhân chỉ gộp khi có căn cứ; nhiều bug độc lập không gom thành một ticket mơ hồ.

## Nội dung bug Markdown

- Bug ID và tiêu đề nêu hành vi/điều kiện.
- Requirement/oracle/source; feature và TC/run liên quan.
- Môi trường/commit, preconditions và dữ liệu.
- Steps có thể tái hiện, expected và actual tách riêng.
- Screenshot bug; log hoặc request/response bổ sung khi cần. Không dùng ảnh chụp source làm ảnh bug giao diện.
- Tần suất đã đo; mức ảnh hưởng có lý do, priority chỉ là đề xuất nếu chưa có quyết định nhóm.
- Trạng thái xác minh, workaround nếu thực đã thử, issue URL/trạng thái đăng.

Không bắt buộc HAR, video, DB dump hoặc nhiều trình duyệt cho mọi bug; chọn evidence để hiểu và tái hiện. HW02 riêng yêu cầu ảnh bug trong GitHub issue nên không bỏ ảnh chỉ vì một nguồn cộng đồng ưu tiên log text. Cần ảnh trang issue cho checklist nộp thì chụp thật sau khi đăng.

## GitHub

Đích theo assignment/nhóm; không mặc định upstream công khai hay fork cá nhân. Chuẩn bị nội dung và ảnh trước thao tác đăng. Được giao đăng với đích rõ thì thực hiện trong quyền đã có; nếu chưa, giữ bản local và nêu việc còn thiếu. Sau đăng kiểm tra issue tồn tại, có ảnh và link đúng; không báo “đã đăng” từ thao tác mở trang soạn.

Không sửa nghiệp vụ, đổi expected hoặc tắt test để làm report xanh. Khi nhiệm vụ là kiểm thử, kết quả fail có thể chính là bằng chứng tốt; bài hoàn tất cần cách giải thích và hồ sơ đủ, không cần che bug để có 100% pass.
