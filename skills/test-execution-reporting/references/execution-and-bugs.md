# Thực thi và báo lỗi

## Thực thi đúng lớp và đúng dữ liệu

Chỉ chạy khi task bao hàm execution. Dùng setup/runner hiện có; kiểm tra tác động reset/seed và ghi diff cấu hình cần thiết riêng với nghiệp vụ SUT. Không mặc định dựng backend/dataset/framework mới cho mọi feature.

Chọn flow ngắn nhất đáp ứng TC: mở form → kiểm tra precondition → nhập/submit → quan sát/assertion → ghi vào kết quả chung. Giữ app/session chạy khi phù hợp, dọn input hoặc navigate về form thay vì mở lại emulator/Expo/browser mỗi TC. Chỉ reset theo TC hoặc khi cần phục hồi môi trường; không reset giữa các bước sequence.

Run ID, thời gian/múi giờ, revision, layer, môi trường và fixture lưu một lần mỗi run. TC là entry chứa actual, status và observation/refs cần thiết. Request/response và exit code phải từ thao tác thật. Không nhân bản catalogue hay một bộ result/ảnh cho từng TC/probe. Xem [evidence](evidence.md) khi cần chọn/chụp bằng chứng.

Status: `passed`, `failed`, `blocked`, `not_run`; `executed = passed + failed`, `not_executed = blocked + not_run`. Giữ lịch sử và đếm unique TC, không đếm rerun thành TC mới. Coverage chỉ nhận điều kiện/bước thật sự đã exercise.

Web responsive không thay native Mobile; API/DB phụ trợ không chứng minh UI đã chạy. Field thiếu thì ghi schema failure/blocker phù hợp; TC phụ thuộc field đó giữ blocked, không thêm field giả hoặc bỏ TC.

Khi harness lỗi, giữ chẩn đoán ngắn và phân loại riêng. Có thể retry thao tác đọc an toàn khi hợp lý; không tự retry submit, reset hoặc tiếp tục sequence khi state không rõ. Lỗi lặp lại thì dừng phần bị ảnh hưởng để sửa/kiểm chứng, không tạo chuỗi probe nặng hoặc lặp lỗi qua cả suite. Khi bị ngắt, giữ kết quả đã ghi và dấu bước dở dang; kiểm tra state trước khi resume.

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
- Evidence phù hợp oracle; JPG khi cần chứng minh lỗi UI hoặc task yêu cầu, log/request/response khi phù hợp. Không dùng ảnh chụp source làm ảnh bug giao diện.
- Tần suất đã đo; mức ảnh hưởng có lý do, priority chỉ là đề xuất nếu chưa có quyết định nhóm.
- Trạng thái xác minh, workaround nếu thực đã thử, issue URL/trạng thái đăng.

Không bắt buộc HAR, video, DB dump hoặc nhiều trình duyệt cho mọi bug; chọn evidence để hiểu và tái hiện. HW02 riêng yêu cầu ảnh bug trong GitHub issue nên không bỏ ảnh chỉ vì một nguồn cộng đồng ưu tiên log text. Cần ảnh trang issue cho checklist nộp thì chụp thật sau khi đăng.

## GitHub

Đích theo assignment/nhóm; không mặc định upstream công khai hay fork cá nhân. Chuẩn bị nội dung và ảnh trước thao tác đăng. Được giao đăng với đích rõ thì thực hiện trong quyền đã có; nếu chưa, giữ bản local và nêu việc còn thiếu. Sau đăng kiểm tra issue tồn tại, có ảnh và link đúng; không báo “đã đăng” từ thao tác mở trang soạn.

Không sửa nghiệp vụ, đổi expected hoặc tắt test để làm report xanh. Khi nhiệm vụ là kiểm thử, kết quả fail có thể chính là bằng chứng tốt; bài hoàn tất cần cách giải thích và hồ sơ đủ, không cần che bug để có 100% pass.
