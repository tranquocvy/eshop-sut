# Báo cáo kết quả — Mobile Account Registration

**HW02 / Pool D — Trần Quốc Vỹ — 23120410.** Tổng hợp các run thực tế; execution do Codex thực hiện, chưa ghi nhận sinh viên review kết quả.

## 1. Phạm vi và môi trường

Nguồn: [design.md](design.md) và [test-cases.md](test-cases.md) v0.3, đã duyệt tại commit `5ca63e1`. Bộ 54 TC giữ nguyên input/expected. Domain dùng nguồn tham khảo Kaner (reference-provisional); BVA theo tài liệu tự học môn trang 44 như thiết kế. Không sinh lại mô hình trong báo cáo execution.

Run chính `MR-RUN-01`: 01:35:19 20/10/2026 (UTC+07:00) đến khi dừng 02:08:49 20/10/2026 (UTC+07:00). Base SUT/test `b8b1d2b`; source nghiệp vụ giữ nguyên. Android 15/API 35, emulator-5554, 720×1280, Expo Go 54.0.8/SDK 54, React Native 0.81.5; Windows 11, Node 24.14.0.

Backend chạy từ bản sao isolated cổng 3001; Mobile chỉ đổi API URL sang 192.168.101.4:3001, Metro 8083. Database T01 và database gốc không bị reset. Seed có admin@eshop.com/test@eshop.com; probe dùng namespace riêng, run chính dùng t02r01. Mọi submit qua native UI; DB chỉ đọc để kiểm tra persistence.


**Lịch sử execution:**

- `MR-RUN-01`: 01:35:19 20/10/2026 (UTC+07:00) → 02:08:49 20/10/2026 (UTC+07:00); interrupted.
- `MR-RUN-02`: 02:44:50 20/10/2026 (UTC+07:00) → 02:45:35 20/10/2026 (UTC+07:00); finished.
- `MR-RUN-03`: 02:45:48 20/10/2026 (UTC+07:00) → 02:49:26 20/10/2026 (UTC+07:00); stopped.
- `MR-RUN-04`: 02:50:21 20/10/2026 (UTC+07:00) → 02:52:00 20/10/2026 (UTC+07:00); stopped.
- `MR-RUN-05`: 02:52:40 20/10/2026 (UTC+07:00) → 02:56:16 20/10/2026 (UTC+07:00); interrupted.
- `MR-RUN-06`: 02:56:16 20/10/2026 (UTC+07:00) → 02:58:35 20/10/2026 (UTC+07:00); finished.
- `MR-RUN-07`: 02:58:53 20/10/2026 (UTC+07:00) → 03:13:02 20/10/2026 (UTC+07:00); finished.

Từ MR-RUN-02, giữ phiên app đang mở, không restart Expo cho từng TC. MR-RUN-02/03 rút gọn bước setup khi đã ở Login/Register bằng cách quay lại form hoặc thay input; đây là điều chỉnh setup, vẫn kiểm tra P0 và dữ liệu riêng. Từ MR-RUN-04 điều hướng Home → Login → Register theo S bằng cùng phiên app. Layout dùng `--no-idle` cùng kiểm tra màn hình/feedback rõ ràng. Backend/DB được tái sử dụng, không reset; input, expected, các bước submit/quan sát và sequence giữ theo TC. Hash code dùng cho mỗi run nằm trong nguồn kết quả.

[results.json](results.json) là nguồn chung: metadata run một lần, mỗi TC một entry, sequence nằm trong entry; observation UI, count/dữ liệu account trước–sau và history probe đủ đối chiếu. Không giữ bộ ảnh/layout riêng cho từng TC trong bản bàn giao.

## 2. Kết quả hiện hành

**54 TC thiết kế: 35 Đạt, 15 Không đạt, 4 Bị chặn, 0 Chưa chạy.** Executed = 50/54; not_executed = 4; pass rate trên executed = 70.00%. Mỗi TC lấy kết quả main/resume mới nhất theo `selected_results`; probe và lượt rerun không cộng thành TC mới. Lịch sử blocked của TC26 và lần dở dang TC29 vẫn được giữ.

**8 nhóm phát hiện:** 4 vi phạm requirement và 4 sai khác so với quy ước S7 đã duyệt; đã đăng và kiểm tra đủ 8 GitHub Issues (#1–#8). Một nhóm có thể ảnh hưởng nhiều TC, không đếm mỗi TC fail thành một bug.

**Coverage đã exercise:** 33/37 mục tiêu miền (89.19%); 18/18 boundary items (100.00%). Đây là số item đã đi tới điều kiện/quan sát, không phải tỷ lệ pass. Confirmation schema D23 được quan sát; equality D24–27 chưa exercise khi C-guard chặn. BVA đủ item không có nghĩa mọi rule hoặc mọi dữ liệu Unicode đều đúng.

### Cách đọc và kiểm chứng

Mỗi hàng cho biết **kiểm tra gì → mong đợi gì → quan sát được gì → kết luận → evidence**. Bấm mã TC để mở bộ thiết kế, rồi tìm đúng ID (Ctrl+F); bấm mã bug để xem bước tái hiện. Cột **Log / ảnh** ở cả 54 dòng dẫn tới log đúng TC/run được chọn; JPG chỉ thêm khi có ảnh thật của chính TC/run đó. Bảng vẫn đủ để hiểu kết quả mà không cần đọc JSON.

**Cách mở log:** Link `Log MR-TCxx / MR-RUN-yy` nhảy tới trích đoạn có anchor tại §6 trong report này, đúng TC/run được chọn trong `selected_results`. Mỗi đoạn dẫn tới [results.json](results.json) kèm vị trí `cases[i].results[j]` để kiểm tra bản ghi gốc khi đọc offline hoặc trên GitHub. Trích đoạn lấy từ kết quả đã lưu, không phải lần chạy mới. TC13 và TC38 giữ cả hai bước sequence; TC34–37 dẫn log C-guard, không nhận đã chạy được equality. TC53 dùng log input/UI/DB riêng; ảnh TC43 trong phần bug chỉ minh họa hành vi chung, không coi là ảnh submit TC53.

**Dữ liệu mặc định:** N = Họ Tên `Nguyen Van A`; E = Email riêng của TC, dạng `mr.t02r01.tcNN@example.com`; P = Password `Abcde1!x`; C = Confirmation (Xác nhận mật khẩu), nhập bằng P nếu UI có field. Bảng chỉ ghi phần thay đổi so với mặc định; “nominal” cũng nghĩa là dùng giá trị mặc định. U/L/D/S lần lượt là số chữ hoa/chữ thường/chữ số/dấu hoặc ký hiệu: U1 nghĩa là có 1 chữ hoa. Input ở ca chưa chạy là dữ liệu **dự kiến theo thiết kế**, chưa xác nhận đã nhập.

**Expected:** “Chấp nhận” nghĩa là tạo đúng 1 tài khoản với name/email đúng theo thiết kế và chuyển tới Đăng nhập; “Từ chối” nghĩa là có phản hồi thất bại, không tạo tài khoản mới và không xử lý như đăng ký thành công. Các yêu cầu sequence/trim/giữ dữ liệu cũ được ghi riêng. Special = dấu/ký hiệu; code point = đơn vị đếm Unicode đã chốt. S7 là quy ước bổ sung đã duyệt, khác với requirement được viết rõ; nguồn chi tiết ở bộ TC.

**Kết luận:** Đạt = actual đáp ứng expected; Không đạt = có khác biệt; Bị chặn = thiếu điều kiện/trường UI hoặc lỗi công cụ/môi trường ngăn đánh giá; Chưa chạy = chưa bắt đầu hoặc chưa có kết quả hoàn tất. Actual dùng số tài khoản **theo email đang kiểm tra**, không phải tổng số tài khoản của hệ thống. Các ca N/E/P chưa chứng minh rule Confirmation nếu form thiếu field.

### Đọc log: xem gì ngoài status?

Log là bản ghi kỹ thuật; đọc theo thứ tự **đã nhập gì → UI phản hồi gì → dữ liệu thay đổi thế nào → điều kiện nào không đạt**. Bảng kết quả phía dưới diễn giải bằng tiếng Việt; link Log dùng khi muốn kiểm chứng chi tiết.

- `run_id`: lần chạy của bản ghi; đối chiếu run ghi trên link. `started_at`/`finished_at` có `+00:00` là giờ UTC, cộng 7 giờ để khớp giờ trong report.
- `submissions`: số lần thực sự bấm gửi đăng ký. `steps`: từng bước trong ca; TC13 và TC38 có hai bước, phải đọc cả hai.
- `steps[].input`: dữ liệu của bước và `expected` (`ACCEPT` = cần chấp nhận, `REJECT` = cần từ chối). Riêng `input.confirmation` là giá trị trong dữ liệu TC; không chứng minh đã nhập Confirmation khi form thiếu field. Giới hạn này nằm trong `limitations`.
- `steps[].ui.feedback`: thông báo đọc từ UI; `login=true` = đã thấy màn hình Đăng nhập, `registration=true` = đang ở form Đăng ký. `success_signal` là dấu hiệu thành công trên UI, chưa đủ chứng minh đã lưu đúng dữ liệu.
- `steps[].accounts`: kết quả DB chỉ đọc, theo từng email đang theo dõi. `count_before`/`count_after` = số tài khoản trước/sau; `new_accounts` = dữ liệu tài khoản mới; `existing_rows_unchanged=true` = dữ liệu các tài khoản cũ được theo dõi giữ nguyên.
- `assertion_failures`: danh sách điều kiện kiểm tra không đạt ở bước đó; `[]` = không phát hiện vi phạm trong các assertion đã chạy, không có nghĩa mọi rule đều đã được kiểm tra. `reason`/`assertions.problems` nêu nguyên nhân lỗi hoặc điểm chặn.
- `form.fields`: các field quan sát được. **`form.complete=true` nghĩa là đã duyệt toàn form, không phải form có đủ field bắt buộc.** TC33–37 vẫn thiếu Confirmation; ca blocked có `submissions=0`, chưa thực hiện equality.
- `input_verification` và `limitations`: mức xác minh input và giới hạn kết luận. Password ghi `masked: transport acknowledged; plaintext not exposed` nghĩa là lệnh nhập đã được nhận nhưng chưa đọc lại plaintext; không diễn giải thành xác minh đầy đủ mật khẩu đã nhập.

**Ví dụ thật — MR-TC02 / MR-RUN-01:** dưới đây chỉ trích các trường cần đọc từ log, không phải một lần chạy mới.

```json
{
  "input": {
    "name": "",
    "expected": "REJECT"
  },
  "ui": {
    "feedback": [
      "Đăng ký tài khoản thành công."
    ],
    "login": true
  },
  "accounts": [
    {
      "count_before": 0,
      "count_after": 1,
      "new_accounts": [
        {
          "name": ""
        }
      ]
    }
  ],
  "assertion_failures": [
    "Invalid/duplicate submission created or changed watched account data",
    "Invalid submission reported registration success",
    "Invalid submission reached Login as if registration succeeded"
  ]
}
```

Đọc thành lời: **để trống tên, mong đợi bị từ chối; ứng dụng lại báo thành công và chuyển sang Đăng nhập; DB tăng từ 0 lên 1 tài khoản, tài khoản mới vẫn có tên rỗng.** Ba assertion thất bại lần lượt chỉ ra việc tạo dữ liệu không hợp lệ, báo thành công và chuyển tới Login. Vì vậy TC02 fail do vi phạm yêu cầu tên bắt buộc; đây không chỉ là suy luận từ một toast. Phần Confirmation vẫn chưa được kiểm tra trong ca này.

### A. Tên và email

| TC | Kiểm tra / input | Mong đợi | Quan sát thực tế | Kết luận / bug | Log / ảnh |
| ---------- | ---------- | ---------- | ---------- | ---------- | ---------- |
| [MR-TC01](test-cases.md) | Dữ liệu hợp lệ (control): Bộ mặc định của TC01 | Chấp nhận bộ dữ liệu hợp lệ; chưa đánh giá rule Confirmation | bước 1: tài khoản 0→1; báo thành công; Đăng nhập; name/email lưu đúng | **Đạt** (passed) | [Log MR-TC01 / MR-RUN-01](#log-mr-tc01) |
| [MR-TC02](test-cases.md) | Tên để trống: N=`""` (0 ký tự) | Từ chối vì thiếu Họ Tên | bước 1: tài khoản 0→1; báo thành công; Đăng nhập | **Không đạt** (failed); [MR-BUG01](#mr-bug01) | [Log MR-TC02 / MR-RUN-01](#log-mr-tc02); [JPG actual](images/MR-BUG01.jpg) |
| [MR-TC03](test-cases.md) | Tên dài 1 ký tự: N=`V` (1 ký tự) | Chấp nhận với tên nonempty | bước 1: tài khoản 0→1; báo thành công; Đăng nhập; name/email lưu đúng | **Đạt** (passed) | [Log MR-TC03 / MR-RUN-01](#log-mr-tc03) |
| [MR-TC04](test-cases.md) | Tên dài 2 ký tự: N=`Vy` (2 ký tự) | Chấp nhận | bước 1: tài khoản 0→1; báo thành công; Đăng nhập; name/email lưu đúng | **Đạt** (passed) | [Log MR-TC04 / MR-RUN-01](#log-mr-tc04) |
| [MR-TC05](test-cases.md) | Tên tiếng Việt có dấu: N=`Trần Quốc Vỹ` | Chấp nhận | bước 1: tài khoản 0→1; báo thành công; Đăng nhập; name/email lưu đúng | **Đạt** (passed) | [Log MR-TC05 / MR-RUN-01](#log-mr-tc05) |
| [MR-TC06](test-cases.md) | Email để trống: E=`""` | Từ chối vì thiếu Email | bước 1: tài khoản 0→1; báo thành công; Đăng nhập | **Không đạt** (failed); [MR-BUG02](#mr-bug02) | [Log MR-TC06 / MR-RUN-01](#log-mr-tc06) |
| [MR-TC07](test-cases.md) | Email thiếu @: E=`mr.t02r01.tc07.example.com` | Từ chối vì thiếu `@` | bước 1: tài khoản 0→1; báo thành công; Đăng nhập | **Không đạt** (failed); [MR-BUG02](#mr-bug02) | [Log MR-TC07 / MR-RUN-01](#log-mr-tc07) |
| [MR-TC08](test-cases.md) | Email thiếu local-part: E=`@example.com` | Từ chối vì thiếu local-part | bước 1: tài khoản 0→1; báo thành công; Đăng nhập | **Không đạt** (failed); [MR-BUG02](#mr-bug02) | [Log MR-TC08 / MR-RUN-01](#log-mr-tc08); [JPG input](images/MR-BUG02-input.jpg); [JPG actual](images/MR-BUG02.jpg) |
| [MR-TC09](test-cases.md) | Email thiếu domain: E=`mr.t02r01.tc09@` | Từ chối vì thiếu domain | bước 1: tài khoản 0→1; báo thành công; Đăng nhập | **Không đạt** (failed); [MR-BUG02](#mr-bug02) | [Log MR-TC09 / MR-RUN-01](#log-mr-tc09) |
| [MR-TC10](test-cases.md) | Email có space trong local-part: E=`mr t02r01.tc10@example.com` (space sau `mr`) | Từ chối vì space trong local-part không quote của địa chỉ đơn giản | bước 1: tài khoản 0→1; báo thành công; Đăng nhập | **Không đạt** (failed); [MR-BUG02](#mr-bug02) | [Log MR-TC10 / MR-RUN-01](#log-mr-tc10) |
| [MR-TC11](test-cases.md) | Email có hai @: E=`mr.t02r01.tc11@@example.com` | Từ chối vì hai `@` liên tiếp, không quote | bước 1: tài khoản 0→1; báo thành công; Đăng nhập | **Không đạt** (failed); [MR-BUG02](#mr-bug02) | [Log MR-TC11 / MR-RUN-01](#log-mr-tc11) |
| [MR-TC12](test-cases.md) | Email trùng dữ liệu có sẵn: E=`test@eshop.com`; N/P nominal | Từ chối email trùng; số tài khoản không tăng, dữ liệu cũ không đổi | bước 1: tài khoản 1→2; báo thành công; Đăng nhập | **Không đạt** (failed); [MR-BUG03](#mr-bug03) | [Log MR-TC12 / MR-RUN-01](#log-mr-tc12) |
| [MR-TC13](test-cases.md) | Đăng ký hai lần cùng email: Cả hai submit dùng E13, N/P nominal | Lần 1 chấp nhận, lần 2 từ chối email trùng; cuối cùng chỉ có 1 tài khoản E13 | bước 1: tài khoản 0→1; báo thành công; Đăng nhập; bước 2: tài khoản 1→2; báo thành công; Đăng nhập | **Không đạt** (failed); [MR-BUG03](#mr-bug03) | [Log MR-TC13 / MR-RUN-01](#log-mr-tc13); [JPG input](images/MR-BUG03-input.jpg); [JPG actual](images/MR-BUG03.jpg) |

### B. Password: miền và biên

| TC | Kiểm tra / input | Mong đợi | Quan sát thực tế | Kết luận / bug | Log / ảnh |
| ---------- | ---------- | ---------- | ---------- | ---------- | ---------- |
| [MR-TC14](test-cases.md) | Password để trống: P=`""` | Từ chối thiếu password | bước 1: tài khoản không đổi; có phản hồi từ chối; form Đăng ký | **Đạt** (passed) | [Log MR-TC14 / MR-RUN-01](#log-mr-tc14) |
| [MR-TC15](test-cases.md) | Password dài 7 ký tự: P=`Abcde1!` (7) | Từ chối vì 7 &lt; 8, các nhóm ký tự khác đủ | bước 1: tài khoản không đổi; có phản hồi từ chối; form Đăng ký | **Đạt** (passed) | [Log MR-TC15 / MR-RUN-01](#log-mr-tc15) |
| [MR-TC16](test-cases.md) | Password dài 8 ký tự: P=`Abcde1!x` (8; U1,L5,D1,S1) | Chấp nhận tại ngưỡng 8, đúng một hoa/số/S | bước 1: tài khoản 0→1; báo thành công; Đăng nhập; name/email lưu đúng | **Đạt** (passed) | [Log MR-TC16 / MR-RUN-01](#log-mr-tc16) |
| [MR-TC17](test-cases.md) | Password dài 9 ký tự: P=`Abcde1!xy` (9) | Chấp nhận phía trên ngưỡng, không chỉ đúng 8 mới được chấp nhận | bước 1: tài khoản 0→1; báo thành công; Đăng nhập; name/email lưu đúng | **Đạt** (passed) | [Log MR-TC17 / MR-RUN-01](#log-mr-tc17) |
| [MR-TC18](test-cases.md) | Password không có chữ hoa: P=`abcde1!x` (8; U0,L6,D1,S1) | Từ chối chỉ vì thiếu chữ hoa | bước 1: tài khoản không đổi; có phản hồi từ chối; form Đăng ký | **Đạt** (passed) | [Log MR-TC18 / MR-RUN-01](#log-mr-tc18) |
| [MR-TC19](test-cases.md) | Password có 2 chữ hoa: P=`ABcde1!x` (8; U2,L4,D1,S1) | Chấp nhận với 2 chữ hoa | bước 1: tài khoản 0→1; báo thành công; Đăng nhập; name/email lưu đúng | **Đạt** (passed) | [Log MR-TC19 / MR-RUN-01](#log-mr-tc19) |
| [MR-TC20](test-cases.md) | Password không có chữ thường: P=`ABCDE1!X` (8; U6,L0,D1,S1) | Từ chối chỉ vì thiếu chữ thường | bước 1: tài khoản không đổi; có phản hồi từ chối; form Đăng ký | **Đạt** (passed) | [Log MR-TC20 / MR-RUN-01](#log-mr-tc20) |
| [MR-TC21](test-cases.md) | Password có 1 chữ thường: P=`ABCDa1!X` (8; U5,L1,D1,S1) | Chấp nhận đúng 1 chữ thường | bước 1: tài khoản 0→1; báo thành công; Đăng nhập; name/email lưu đúng | **Đạt** (passed) | [Log MR-TC21 / MR-RUN-01](#log-mr-tc21) |
| [MR-TC22](test-cases.md) | Password có 2 chữ thường: P=`ABCDab1!` (8; U4,L2,D1,S1) | Chấp nhận với 2 chữ thường | bước 1: tài khoản 0→1; báo thành công; Đăng nhập; name/email lưu đúng | **Đạt** (passed) | [Log MR-TC22 / MR-RUN-01](#log-mr-tc22) |
| [MR-TC23](test-cases.md) | Password không có chữ số: P=`Abcdef!x` (8; U1,L6,D0,S1) | Từ chối chỉ vì thiếu chữ số | bước 1: tài khoản không đổi; có phản hồi từ chối; form Đăng ký | **Đạt** (passed) | [Log MR-TC23 / MR-RUN-01](#log-mr-tc23) |
| [MR-TC24](test-cases.md) | Password có 2 chữ số: P=`Abcde12!` (8; U1,L4,D2,S1) | Chấp nhận với 2 chữ số | bước 1: tài khoản 0→1; báo thành công; Đăng nhập; name/email lưu đúng | **Đạt** (passed) | [Log MR-TC24 / MR-RUN-01](#log-mr-tc24) |
| [MR-TC25](test-cases.md) | Password không có special: P=`Abcde12x` (8; U1,L5,D2,S0; chỉ alphanumeric) | Từ chối vì hoàn toàn thiếu dấu/ký hiệu | bước 1: tài khoản không đổi; có phản hồi từ chối; form Đăng ký | **Đạt** (passed) | [Log MR-TC25 / MR-RUN-01](#log-mr-tc25) |
| [MR-TC26](test-cases.md) | Password có 2 special: P=`Abcde1!!` (8; U1,L4,D1,S2) | Chấp nhận với 2 dấu/ký hiệu `!` | bước 1: tài khoản 0→1; báo thành công; Đăng nhập; name/email lưu đúng | **Đạt** (passed) | [Log MR-TC26 / MR-RUN-02](#log-mr-tc26) |
| [MR-TC27](test-cases.md) | Special là @: P=`Abcde1@x` | Chấp nhận với `@` là dấu/ký hiệu duy nhất | bước 1: tài khoản 0→1; báo thành công; Đăng nhập; name/email lưu đúng | **Đạt** (passed) | [Log MR-TC27 / MR-RUN-01](#log-mr-tc27) |
| [MR-TC28](test-cases.md) | Special là $: P=`Abcde1$x` | Chấp nhận với `$` là dấu/ký hiệu duy nhất | bước 1: tài khoản 0→1; báo thành công; Đăng nhập; name/email lưu đúng | **Đạt** (passed) | [Log MR-TC28 / MR-RUN-01](#log-mr-tc28) |
| [MR-TC29](test-cases.md) | Special là %: P=`Abcde1%x` | Chấp nhận với `%` là dấu/ký hiệu duy nhất | bước 1: tài khoản 0→1; báo thành công; Đăng nhập; name/email lưu đúng | **Đạt** (passed) | [Log MR-TC29 / MR-RUN-03](#log-mr-tc29) |
| [MR-TC30](test-cases.md) | Special là *: P=`Abcde1*x` | Chấp nhận với `*` là dấu/ký hiệu duy nhất | bước 1: tài khoản 0→1; báo thành công; Đăng nhập; name/email lưu đúng | **Đạt** (passed) | [Log MR-TC30 / MR-RUN-03](#log-mr-tc30) |
| [MR-TC31](test-cases.md) | Special là ?: P=`Abcde1?x` | Chấp nhận với `?` là dấu/ký hiệu duy nhất | bước 1: tài khoản 0→1; báo thành công; Đăng nhập; name/email lưu đúng | **Đạt** (passed) | [Log MR-TC31 / MR-RUN-03](#log-mr-tc31) |
| [MR-TC32](test-cases.md) | Special là &: P=`Abcde1&x` | Chấp nhận với `&` là dấu/ký hiệu duy nhất | bước 1: tài khoản 0→1; báo thành công; Đăng nhập; name/email lưu đúng | **Đạt** (passed) | [Log MR-TC32 / MR-RUN-03](#log-mr-tc32) |

### C. Confirmation và trạng thái

| TC | Kiểm tra / input | Mong đợi | Quan sát thực tế | Kết luận / bug | Log / ảnh |
| ---------- | ---------- | ---------- | ---------- | ---------- | ---------- |
| [MR-TC33](test-cases.md) | Form có Confirmation: Không submit; form ban đầu | Có trường Xác nhận mật khẩu, nhập được độc lập với P. Không suy chỉ từ một viewport | Đã kiểm tra toàn form: chỉ có Họ Tên, Email, Password; không có Confirmation; 0 submit. | **Không đạt** (failed); [MR-BUG04](#mr-bug04) | [Log MR-TC33 / MR-RUN-03](#log-mr-tc33); [JPG actual](images/MR-RUN-03-MR-TC33-actual.jpg) |
| [MR-TC34](test-cases.md) | Confirmation để trống: N/E34/P nominal; C=`""` | Từ chối vì không khớp với P nonempty | Thiếu Confirmation; không thể nhập/so sánh C trên native; 0 submit. | **Bị chặn** (blocked); phụ thuộc [MR-BUG04](#mr-bug04) | [Log MR-TC34 / MR-RUN-03](#log-mr-tc34) |
| [MR-TC35](test-cases.md) | Confirmation cùng độ dài nhưng khác nội dung: P=`Abcde1!x`, C=`Abcde1!y` (đều 8, khác ký tự cuối) | Từ chối dù hai chuỗi cùng độ dài | Thiếu Confirmation; không thể nhập/so sánh C trên native; 0 submit. | **Bị chặn** (blocked); phụ thuộc [MR-BUG04](#mr-bug04) | [Log MR-TC35 / MR-RUN-03](#log-mr-tc35) |
| [MR-TC36](test-cases.md) | Confirmation là prefix ngắn hơn password: P=`Abcde1!x`, C=`Abcde1!` (7, là prefix của P) | Từ chối vì không bằng nhau | Thiếu Confirmation; không thể nhập/so sánh C trên native; 0 submit. | **Bị chặn** (blocked); phụ thuộc [MR-BUG04](#mr-bug04) | [Log MR-TC36 / MR-RUN-04](#log-mr-tc36) |
| [MR-TC37](test-cases.md) | Confirmation bằng password: P=C=`Abcde1!x`, N/E37 nominal | Chấp nhận và chuyển sang Đăng nhập | Thiếu Confirmation; không thể nhập/so sánh C trên native; 0 submit. | **Bị chặn** (blocked); phụ thuộc [MR-BUG04](#mr-bug04) | [Log MR-TC37 / MR-RUN-04](#log-mr-tc37) |
| [MR-TC38](test-cases.md) | Sửa password từ 7 thành 8 ký tự: Lần 1 P=`Abcde1!` (7); lần 2 sửa P=`Abcde1!x` (8); cùng N/E38; sửa C theo P nếu có | Lần 1 từ chối, chưa tạo E38; lần 2 chấp nhận; cuối sequence có đúng 1 tài khoản E38 | bước 1: tài khoản không đổi; có phản hồi từ chối; form Đăng ký; bước 2: tài khoản 0→1; báo thành công; Đăng nhập; name/email lưu đúng | **Đạt** (passed) | [Log MR-TC38 / MR-RUN-06](#log-mr-tc38) |
| [MR-TC39](test-cases.md) | Email trùng và password thiếu chữ hoa: E=`test@eshop.com`, P=`abcde1!x` (thiếu hoa), N nominal | Từ chối, không thêm/sửa tài khoản đã tồn tại. Bất kỳ rule invalid nào được thông báo trước đều được | bước 1: tài khoản không đổi; có phản hồi từ chối; form Đăng ký | **Đạt** (passed) | [Log MR-TC39 / MR-RUN-06](#log-mr-tc39) |
| [MR-TC40](test-cases.md) | Password dài 64 ký tự: P = `Ab1!` lặp 16 lần (64 ký tự); C=P nếu có | Chấp nhận | bước 1: tài khoản 0→1; báo thành công; Đăng nhập; name/email lưu đúng | **Đạt** (passed) | [Log MR-TC40 / MR-RUN-07](#log-mr-tc40) |

### D. Quy ước đã duyệt (S7)

| TC | Kiểm tra / input | Mong đợi | Quan sát thực tế | Kết luận / bug | Log / ảnh |
| ---------- | ---------- | ---------- | ---------- | ---------- | ---------- |
| [MR-TC41](test-cases.md) | Tên chỉ có space: N=` ` (1 space), E41/P nominal | Từ chối vì tên sau trim rỗng | bước 1: tài khoản 0→1; báo thành công; Đăng nhập | **Không đạt** (failed); [MR-BUG05](#mr-bug05) | [Log MR-TC41 / MR-RUN-07](#log-mr-tc41); [JPG input](images/MR-RUN-07-MR-TC41-input.jpg); [JPG actual](images/MR-RUN-07-MR-TC41-actual.jpg) |
| [MR-TC42](test-cases.md) | Email khác chữ hoa/thường: E=`TEST@eshop.com`, N/P nominal | Chấp nhận tạo đúng 1 tài khoản `TEST@eshop.com`, tài khoản `test@eshop.com` cũ giữ nguyên. Email khác case là hai chuỗi khác theo review S7/Q02 | bước 1: tài khoản 0→1; báo thành công; Đăng nhập; name/email lưu đúng | **Đạt** (passed) | [Log MR-TC42 / MR-RUN-07](#log-mr-tc42) |
| [MR-TC43](test-cases.md) | Email có space đầu/cuối: E=` mr.t02r01.tc43@example.com ` (1 space đầu/cuối), N/P nominal | Chấp nhận, chỉ tạo tài khoản với email `mr.t02r01.tc43@example.com` đã bỏ space đầu/cuối; không lưu dạng có space | Báo thành công/Đăng nhập; email có space 0→1, email đã trim 0→0; lưu sai dạng email. | **Không đạt** (failed); [MR-BUG06](#mr-bug06) | [Log MR-TC43 / MR-RUN-07](#log-mr-tc43); [JPG input](images/MR-RUN-07-MR-TC43-input.jpg); [JPG actual](images/MR-RUN-07-MR-TC43-actual.jpg) |
| [MR-TC44](test-cases.md) | Special mở rộng là #: P=`Abcde1#x` (8 code point, special duy nhất `#`) | Chấp nhận vì `#` là dấu Unicode thuộc Punctuation | bước 1: tài khoản 0→1; báo thành công; Đăng nhập; name/email lưu đúng | **Đạt** (passed) | [Log MR-TC44 / MR-RUN-07](#log-mr-tc44) |
| [MR-TC45](test-cases.md) | Space không thay thế special: P=`Abcde1 x` (8 code point, 1 space giữa `1` và `x`, không có dấu/ký hiệu) | Từ chối vì space không đáp ứng yêu cầu dấu/ký hiệu | bước 1: tài khoản 0→1; báo thành công; Đăng nhập | **Không đạt** (failed); [MR-BUG07](#mr-bug07) | [Log MR-TC45 / MR-RUN-07](#log-mr-tc45); [JPG input](images/MR-RUN-07-MR-TC45-input.jpg); [JPG actual](images/MR-RUN-07-MR-TC45-actual.jpg) |
| [MR-TC46](test-cases.md) | Độ dài Unicode: 7 code point: P=`Abc1!😀d` (7 code point, 8 UTF-16 unit), C=P nếu có | Từ chối vì 7 &lt; 8 code point, dù đủ 8 UTF-16 unit. Có đủ hoa/thường/số/dấu/ký hiệu | bước 1: tài khoản 0→1; báo thành công; Đăng nhập | **Không đạt** (failed); [MR-BUG08](#mr-bug08) | [Log MR-TC46 / MR-RUN-07](#log-mr-tc46); [JPG input](images/MR-RUN-07-MR-TC46-input.jpg); [JPG actual](images/MR-RUN-07-MR-TC46-actual.jpg) |

### E. Unicode và tương tác dữ liệu (S7)

| TC | Kiểm tra / input | Mong đợi | Quan sát thực tế | Kết luận / bug | Log / ảnh |
| ---------- | ---------- | ---------- | ---------- | ---------- | ---------- |
| [MR-TC47](test-cases.md) | Độ dài Unicode: 8 code point: P=`Abc1!😀de` (8 code point, 9 UTF-16 unit), C=P nếu có | Chấp nhận tại ngưỡng 8 code point, đủ các nhóm ký tự | bước 1: tài khoản 0→1; báo thành công; Đăng nhập; name/email lưu đúng | **Đạt** (passed) | [Log MR-TC47 / MR-RUN-07](#log-mr-tc47) |
| [MR-TC48](test-cases.md) | Độ dài Unicode: 9 code point: P=`Abc1!😀def` (9 code point, 10 UTF-16 unit), C=P nếu có | Chấp nhận phía trên ngưỡng | bước 1: tài khoản 0→1; báo thành công; Đăng nhập; name/email lưu đúng | **Đạt** (passed) | [Log MR-TC48 / MR-RUN-07](#log-mr-tc48) |
| [MR-TC49](test-cases.md) | Special mở rộng là _: P=`Abcde1_x` (8 code point, special duy nhất `_`) | Chấp nhận vì `_` thuộc Punctuation | bước 1: tài khoản 0→1; báo thành công; Đăng nhập; name/email lưu đúng | **Đạt** (passed) | [Log MR-TC49 / MR-RUN-07](#log-mr-tc49) |
| [MR-TC50](test-cases.md) | Emoji là special duy nhất: P=`Abcdef1😀` (8 code point, special duy nhất `😀`) | Chấp nhận vì emoji này thuộc Symbol | bước 1: tài khoản 0→1; báo thành công; Đăng nhập; name/email lưu đúng | **Đạt** (passed) | [Log MR-TC50 / MR-RUN-07](#log-mr-tc50) |
| [MR-TC51](test-cases.md) | Special là em dash: P=`Abcde1—x` (8 code point, special duy nhất là em dash `—`, không phải dấu trừ) | Chấp nhận vì `—` thuộc Punctuation | bước 1: tài khoản 0→1; báo thành công; Đăng nhập; name/email lưu đúng | **Đạt** (passed) | [Log MR-TC51 / MR-RUN-07](#log-mr-tc51) |
| [MR-TC52](test-cases.md) | Special là ký hiệu euro: P=`Abcde1€x` (8 code point, special duy nhất `€`) | Chấp nhận vì `€` thuộc Symbol | bước 1: tài khoản 0→1; báo thành công; Đăng nhập; name/email lưu đúng | **Đạt** (passed) | [Log MR-TC52 / MR-RUN-07](#log-mr-tc52) |
| [MR-TC53](test-cases.md) | Email sau trim bị trùng: E=` test@eshop.com ` (1 space đầu/cuối), N/P nominal | Từ chối vì sau bỏ space đầu/cuối email trùng `test@eshop.com`; không tạo tài khoản ở cả hai dạng và không sửa dữ liệu cũ | bước 1: tài khoản 0→1; báo thành công; Đăng nhập | **Không đạt** (failed); [MR-BUG06](#mr-bug06) | [Log MR-TC53 / MR-RUN-07](#log-mr-tc53) |
| [MR-TC54](test-cases.md) | Password có cả special và space: P=`Abc1! xy` (8 code point, có `!` và 1 space sau `!`), C=P nếu có | Chấp nhận vì `!` thỏa dấu/ký hiệu, space không bị dùng để thay dấu/ký hiệu và chưa có rule cấm mọi space | bước 1: tài khoản 0→1; báo thành công; Đăng nhập; name/email lưu đúng | **Đạt** (passed) | [Log MR-TC54 / MR-RUN-07](#log-mr-tc54) |

## 3. Phát hiện và evidence

MR-BUG01–04 đối chiếu requirement FR-01 áp dụng cho Mobile qua FR-20. MR-BUG05–08 là sai khác so với quy ước S7 đã duyệt, không gán thành yêu cầu README viết rõ. Severity là đề xuất theo tác động. Detail, URL và JPG trang issue đã đăng nằm ngay trong từng bug bên dưới. Đã mở lại cả 8 issue, đối chiếu nội dung và kiểm tra đủ 14 ảnh SUT hiển thị. Ảnh lỗi dùng URL cố định tại commit `6631d92c856ddb4ac0e510697cce32beca33a2c3`; không cần upload bản sao hay chạy lại Mobile.

**Đọc evidence:** JPG chứng minh phần UI hiển thị; persistence được đối chiếu bằng observations/DB chỉ đọc. Password bị che: native command đã nhận input, chưa đọc lại plaintext. Các caption ghi TC/run, trạng thái và thời gian chụp.

**Bổ sung GitHub (report-only, 20/10/2026):** [Danh sách 8 issue](https://github.com/tranquocvy/eshop-sut/issues), từ MR-BUG01/#1 đến MR-BUG08/#8; MR-BUG05–08 có nhãn `[S7]` trong tiêu đề và giải thích phân loại. Log thao tác thật nằm tại `bugs[].github_activity`, metadata ảnh trang tại `images[]` trong [results.json](results.json). Log ghi thời gian tạo, kiểm tra nội dung qua API và mở trang/kiểm tra ảnh/chụp JPG; không tạo execution run mới.

![Danh sách 8 GitHub Issues Mobile](images/MR-GitHub-issues.jpg)

*Danh sách issue thật; chụp 13:47:14 20/10/2026 (UTC+07:00). Mỗi issue có JPG riêng bên dưới; ảnh tổng quan không thay ảnh chi tiết.*

<a id="mr-bug01"></a>

### MR-BUG01 — Họ Tên rỗng vẫn đăng ký thành công

**Oracle:** FR-01 / MR-R01. **TC:** MR-TC02. **Severity đề xuất:** Medium.

**Precondition/steps:** Mở Home → Đăng nhập → Đăng ký ngay. Để Họ Tên rỗng; Email=mr.t02r01.tc02@example.com; Password=Abcde1!x. Bấm Đăng ký một lần.

**Expected:** REJECT, có feedback và không tạo account khi thiếu Họ Tên.

**Actual:** bước 1: account 0→1; báo thành công; Login

DB lưu một account mới với `name=""`; ảnh chỉ cho thấy báo thành công/Login. Input rỗng và dữ liệu lưu phải đọc cùng observation TC02 trong results.json.

![MR-BUG01 actual](images/MR-BUG01.jpg)

*MR-TC02/MR-RUN-01 — Actual: 01:37:36 20/10/2026 (UTC+07:00). JPG từ capture thật; không chụp mới khi tổng hợp.*

**Tần suất quan sát:** 1 TC liên quan, mỗi TC chạy một lần trong run chính; không coi đó là nhiều lần lặp độc lập của cùng một input.

**GitHub:** [#1](https://github.com/tranquocvy/eshop-sut/issues/1) — Open. Đã mở trang, đối chiếu nội dung và kiểm tra 1 ảnh SUT tải/hiển thị đầy đủ. Đăng 13:44:29 20/10/2026 (UTC+07:00).

![MR-BUG01 — trang GitHub issue đã đăng](images/MR-BUG01-issue.jpg)

*Ảnh trang issue MR-BUG01 / #1; chụp 13:45:25 20/10/2026 (UTC+07:00). Ảnh chụp trang GitHub hiện tại, tách biệt với thời gian ảnh SUT/run gốc.*

<a id="mr-bug02"></a>

### MR-BUG02 — Email rỗng hoặc sai định dạng vẫn được chấp nhận

**Oracle:** FR-01 / MR-R02. **TC:** MR-TC06, MR-TC07, MR-TC08, MR-TC09, MR-TC10, MR-TC11. **Severity đề xuất:** High.

**Precondition/steps:** Mở form Đăng ký. Nhập Họ Tên=Nguyen Van A; Email=@example.com; Password=Abcde1!x. Bấm Đăng ký một lần. Các TC cùng nhóm kiểm tra email rỗng, thiếu @, thiếu domain, space trong local-part và hai @.

**Expected:** REJECT email rỗng/sai định dạng, không tạo account.

**Actual:** bước 1: account 0→1; báo thành công; Login

TC08 lưu account email `@example.com`; các TC06–11 đều có count 0→1 và báo thành công.

![MR-BUG02 input](images/MR-BUG02-input.jpg) ![MR-BUG02 actual](images/MR-BUG02.jpg)

*MR-TC08/MR-RUN-01 — Input: 01:44:33 20/10/2026 (UTC+07:00); Actual: 01:44:39 20/10/2026 (UTC+07:00). JPG từ capture thật; không chụp mới khi tổng hợp.*

**Tần suất quan sát:** 6 TC liên quan, mỗi TC chạy một lần trong run chính; không coi đó là nhiều lần lặp độc lập của cùng một input.

**GitHub:** [#2](https://github.com/tranquocvy/eshop-sut/issues/2) — Open. Đã mở trang, đối chiếu nội dung và kiểm tra 2 ảnh SUT tải/hiển thị đầy đủ. Đăng 13:44:30 20/10/2026 (UTC+07:00).

![MR-BUG02 — trang GitHub issue đã đăng](images/MR-BUG02-issue.jpg)

*Ảnh trang issue MR-BUG02 / #2; chụp 13:45:44 20/10/2026 (UTC+07:00). Ảnh chụp trang GitHub hiện tại, tách biệt với thời gian ảnh SUT/run gốc.*

<a id="mr-bug03"></a>

### MR-BUG03 — Đăng ký trùng email tạo thêm account

**Oracle:** FR-01 / MR-R03. **TC:** MR-TC12, MR-TC13. **Severity đề xuất:** High.

**Precondition/steps:** TC12 dùng test@eshop.com đã có trong seed. TC13: nhập Nguyen Van A / mr.t02r01.tc13@example.com / Abcde1!x; đăng ký lần đầu, đóng alert, navigate về Đăng ký và submit lại cùng dữ liệu. Không reset backend giữa hai lần.

**Expected:** Lần đăng ký trùng phải REJECT; số account theo email không tăng và các account cũ giữ nguyên.

**Actual:** bước 1: account 0→1; báo thành công; Login; bước 2: account 1→2; báo thành công; Login

TC12 tăng account `test@eshop.com` từ 1→2; TC13 tăng 0→1 ở bước đầu rồi 1→2 ở bước đăng ký trùng. Các account cũ được quan sát giữ nguyên.

![MR-BUG03 input](images/MR-BUG03-input.jpg) ![MR-BUG03 actual](images/MR-BUG03.jpg)

*MR-TC13/MR-RUN-01 — Input: 01:51:31 20/10/2026 (UTC+07:00); Actual: 01:51:37 20/10/2026 (UTC+07:00). JPG từ capture thật; không chụp mới khi tổng hợp.*

**Tần suất quan sát:** 2 TC liên quan, mỗi TC chạy một lần trong run chính; không coi đó là nhiều lần lặp độc lập của cùng một input.

**GitHub:** [#3](https://github.com/tranquocvy/eshop-sut/issues/3) — Open. Đã mở trang, đối chiếu nội dung và kiểm tra 2 ảnh SUT tải/hiển thị đầy đủ. Đăng 13:44:31 20/10/2026 (UTC+07:00).

![MR-BUG03 — trang GitHub issue đã đăng](images/MR-BUG03-issue.jpg)

*Ảnh trang issue MR-BUG03 / #3; chụp 13:46:10 20/10/2026 (UTC+07:00). Ảnh chụp trang GitHub hiện tại, tách biệt với thời gian ảnh SUT/run gốc.*

<a id="mr-bug04"></a>

### MR-BUG04 — Form Đăng ký thiếu trường Xác nhận mật khẩu

**Phân loại:** Vi phạm requirement. **Oracle:** FR-01 / MR-R10, áp dụng cho Mobile qua FR-20. **TC:** MR-TC33. **Severity đề xuất:** High.

**Precondition/steps:** Backend/fixture theo môi trường ở §1; người dùng chưa đăng nhập. Mở Home → Đăng nhập → Đăng ký ngay; quan sát toàn form và scroll đến cuối. Không submit.

**Expected:** Có field Confirmation riêng, nhập được độc lập với Password.

**Actual MR-TC33 / MR-RUN-03:** Full-form inspection: Required native Confirmation field is absent after full-form inspection

**Tác động:** Không thực hiện được bước xác nhận mật khẩu và các ca equality phụ thuộc field này.

![MR-BUG04 actual](images/MR-RUN-03-MR-TC33-actual.jpg)

*MR-TC33 / MR-RUN-03; actual; chụp 02:49:09 20/10/2026 (UTC+07:00).*

**Tần suất:** 1 TC liên quan, mỗi TC chạy một lần; chưa đo lặp độc lập cùng một input.

**GitHub:** [#4](https://github.com/tranquocvy/eshop-sut/issues/4) — Open. Đã mở trang, đối chiếu nội dung và kiểm tra 1 ảnh SUT tải/hiển thị đầy đủ. Đăng 13:44:32 20/10/2026 (UTC+07:00).

![MR-BUG04 — trang GitHub issue đã đăng](images/MR-BUG04-issue.jpg)

*Ảnh trang issue MR-BUG04 / #4; chụp 13:46:23 20/10/2026 (UTC+07:00). Ảnh chụp trang GitHub hiện tại, tách biệt với thời gian ảnh SUT/run gốc.*

<a id="mr-bug05"></a>

### MR-BUG05 — Tên chỉ có khoảng trắng vẫn tạo tài khoản

**Phân loại:** Sai khác quy ước S7. **Oracle:** Review S7/Q01; MR-R01 / MR-D30. **TC:** MR-TC41. **Severity đề xuất:** Medium.

**Precondition/steps:** Backend/fixture theo môi trường ở §1; người dùng chưa đăng nhập. Trên form Đăng ký, nhập N là đúng 1 space; E=mr.t02r01.tc41@example.com; P=Abcde1!x. Submit một lần.

**Expected:** Theo S7, từ chối tên sau trim rỗng; không tạo account.

**Actual MR-TC41 / MR-RUN-07:** bước 1: tài khoản 0→1; báo thành công; Đăng nhập

Quan sát DB chỉ đọc, bước 1: email='mr.t02r01.tc41@example.com': 0→1, dữ liệu cũ giữ nguyên.

Dữ liệu account mới: name=' ', email='mr.t02r01.tc41@example.com'.

**Tác động:** Dữ liệu tên không có nội dung vẫn được lưu; đây là sai khác với quy ước S7 đã duyệt.

![MR-BUG05 input](images/MR-RUN-07-MR-TC41-input.jpg)

*MR-TC41 / MR-RUN-07; input; chụp 03:00:43 20/10/2026 (UTC+07:00).*

![MR-BUG05 actual](images/MR-RUN-07-MR-TC41-actual.jpg)

*MR-TC41 / MR-RUN-07; actual; chụp 03:00:45 20/10/2026 (UTC+07:00).*

**Tần suất:** 1 TC liên quan, mỗi TC chạy một lần; chưa đo lặp độc lập cùng một input.

**GitHub:** [#5](https://github.com/tranquocvy/eshop-sut/issues/5) — Open. Đã mở trang, đối chiếu nội dung và kiểm tra 2 ảnh SUT tải/hiển thị đầy đủ. Đăng 13:44:34 20/10/2026 (UTC+07:00).

![MR-BUG05 — trang GitHub issue đã đăng](images/MR-BUG05-issue.jpg)

*Ảnh trang issue MR-BUG05 / #5; chụp 13:46:33 20/10/2026 (UTC+07:00). Ảnh chụp trang GitHub hiện tại, tách biệt với thời gian ảnh SUT/run gốc.*

<a id="mr-bug06"></a>

### MR-BUG06 — Email có khoảng trắng đầu/cuối không được chuẩn hóa theo S7

**Phân loại:** Sai khác quy ước S7. **Oracle:** Review S7/Q03; MR-R02–03 / MR-D32, MR-D36. **TC:** MR-TC43, MR-TC53. **Severity đề xuất:** Medium.

**Precondition/steps:** Backend/fixture theo môi trường ở §1; người dùng chưa đăng nhập. TC43: nhập E=" mr.t02r01.tc43@example.com ", N/P mặc định, submit. TC53: nhập E=" test@eshop.com " khi dạng không space đã tồn tại; submit một lần. Không trim trước bằng tool.

**Expected:** TC43 chỉ lưu email đã trim; TC53 từ chối email trùng sau trim, không thêm/sửa account ở cả hai dạng.

**Actual MR-TC43 / MR-RUN-07:** bước 1: tài khoản 0→1; báo thành công; Đăng nhập

Quan sát DB chỉ đọc, bước 1: email=' mr.t02r01.tc43@example.com ': 0→1, dữ liệu cũ giữ nguyên; email='mr.t02r01.tc43@example.com': 0→0, dữ liệu cũ giữ nguyên.

Dữ liệu account mới: name='Nguyen Van A', email=' mr.t02r01.tc43@example.com '.

**Actual MR-TC53 / MR-RUN-07:** bước 1: tài khoản 0→1; báo thành công; Đăng nhập

Quan sát DB chỉ đọc, bước 1: email=' test@eshop.com ': 0→1, dữ liệu cũ giữ nguyên; email='test@eshop.com': 2→2, dữ liệu cũ giữ nguyên.

Dữ liệu account mới: name='Nguyen Van A', email=' test@eshop.com '.

**Tác động:** Việc lưu/so khớp email có padding khác chính sách chuẩn hóa đã duyệt; tách khỏi lỗi uniqueness requirement MR-BUG03.

Ảnh đại diện chụp TC43; kết quả TC53 được đối chiếu bằng observations/DB riêng ở trên.

![MR-BUG06 input](images/MR-RUN-07-MR-TC43-input.jpg)

*MR-TC43 / MR-RUN-07; input; chụp 03:02:37 20/10/2026 (UTC+07:00).*

![MR-BUG06 actual](images/MR-RUN-07-MR-TC43-actual.jpg)

*MR-TC43 / MR-RUN-07; actual; chụp 03:02:38 20/10/2026 (UTC+07:00).*

**Tần suất:** 2 TC liên quan, mỗi TC chạy một lần; chưa đo lặp độc lập cùng một input.

**GitHub:** [#6](https://github.com/tranquocvy/eshop-sut/issues/6) — Open. Đã mở trang, đối chiếu nội dung và kiểm tra 2 ảnh SUT tải/hiển thị đầy đủ. Đăng 13:44:35 20/10/2026 (UTC+07:00).

![MR-BUG06 — trang GitHub issue đã đăng](images/MR-BUG06-issue.jpg)

*Ảnh trang issue MR-BUG06 / #6; chụp 13:46:42 20/10/2026 (UTC+07:00). Ảnh chụp trang GitHub hiện tại, tách biệt với thời gian ảnh SUT/run gốc.*

<a id="mr-bug07"></a>

### MR-BUG07 — Khoảng trắng được chấp nhận thay cho special trong password

**Phân loại:** Sai khác quy ước S7. **Oracle:** Review S7/Q04; MR-R09 / MR-D34. **TC:** MR-TC45. **Severity đề xuất:** Medium.

**Precondition/steps:** Backend/fixture theo môi trường ở §1; người dùng chưa đăng nhập. Nhập N/E45 mặc định và P="Abcde1 x" (8 code point, có space nhưng không có dấu/ký hiệu). Submit một lần.

**Expected:** Theo S7, từ chối vì space không được tính là special; không tạo account.

**Actual MR-TC45 / MR-RUN-07:** bước 1: tài khoản 0→1; báo thành công; Đăng nhập

Quan sát DB chỉ đọc, bước 1: email='mr.t02r01.tc45@example.com': 0→1, dữ liệu cũ giữ nguyên.

Dữ liệu account mới: name='Nguyen Van A', email='mr.t02r01.tc45@example.com'.

**Tác động:** Password không có dấu/ký hiệu vẫn được chấp nhận theo runtime, khác quy ước special đã duyệt.

![MR-BUG07 input](images/MR-RUN-07-MR-TC45-input.jpg)

*MR-TC45 / MR-RUN-07; input; chụp 03:04:30 20/10/2026 (UTC+07:00).*

![MR-BUG07 actual](images/MR-RUN-07-MR-TC45-actual.jpg)

*MR-TC45 / MR-RUN-07; actual; chụp 03:04:31 20/10/2026 (UTC+07:00).*

**Tần suất:** 1 TC liên quan, mỗi TC chạy một lần; chưa đo lặp độc lập cùng một input.

**GitHub:** [#7](https://github.com/tranquocvy/eshop-sut/issues/7) — Open. Đã mở trang, đối chiếu nội dung và kiểm tra 2 ảnh SUT tải/hiển thị đầy đủ. Đăng 13:44:36 20/10/2026 (UTC+07:00).

![MR-BUG07 — trang GitHub issue đã đăng](images/MR-BUG07-issue.jpg)

*Ảnh trang issue MR-BUG07 / #7; chụp 13:46:51 20/10/2026 (UTC+07:00). Ảnh chụp trang GitHub hiện tại, tách biệt với thời gian ảnh SUT/run gốc.*

<a id="mr-bug08"></a>

### MR-BUG08 — Password 7 Unicode code point vẫn được chấp nhận

**Phân loại:** Sai khác quy ước S7. **Oracle:** Review S7/Q05; MR-R05 / MR-D35 / B01-7. **TC:** MR-TC46. **Severity đề xuất:** Medium.

**Precondition/steps:** Backend/fixture theo môi trường ở §1; người dùng chưa đăng nhập. Nhập N/E46 mặc định, P="Abc1!😀d" nguyên vẹn (7 code point, 8 UTF-16 unit). Submit một lần.

**Expected:** Theo S7, từ chối vì chưa đủ 8 code point; không tạo account.

**Actual MR-TC46 / MR-RUN-07:** bước 1: tài khoản 0→1; báo thành công; Đăng nhập

Quan sát DB chỉ đọc, bước 1: email='mr.t02r01.tc46@example.com': 0→1, dữ liệu cũ giữ nguyên.

Dữ liệu account mới: name='Nguyen Van A', email='mr.t02r01.tc46@example.com'.

**Tác động:** Runtime chấp nhận chuỗi dưới ngưỡng theo đơn vị đã duyệt; expected vẫn giữ Unicode code point, không đổi sang UTF-16 để làm test pass.

![MR-BUG08 input](images/MR-RUN-07-MR-TC46-input.jpg)

*MR-TC46 / MR-RUN-07; input; chụp 03:05:27 20/10/2026 (UTC+07:00).*

![MR-BUG08 actual](images/MR-RUN-07-MR-TC46-actual.jpg)

*MR-TC46 / MR-RUN-07; actual; chụp 03:05:28 20/10/2026 (UTC+07:00).*

**Tần suất:** 1 TC liên quan, mỗi TC chạy một lần; chưa đo lặp độc lập cùng một input.

**GitHub:** [#8](https://github.com/tranquocvy/eshop-sut/issues/8) — Open. Đã mở trang, đối chiếu nội dung và kiểm tra 2 ảnh SUT tải/hiển thị đầy đủ. Đăng 13:44:38 20/10/2026 (UTC+07:00).

![MR-BUG08 — trang GitHub issue đã đăng](images/MR-BUG08-issue.jpg)

*Ảnh trang issue MR-BUG08 / #8; chụp 13:47:00 20/10/2026 (UTC+07:00). Ảnh chụp trang GitHub hiện tại, tách biệt với thời gian ảnh SUT/run gốc.*

## 4. Harness và AI gaps

PROBE-01–05 bị chặn trước submit do hidden node/bounds, cờ IME hoặc khởi chạy Expo/system panel; PROBE-06 pass. Đây là execution gaps có lịch sử thật, không phải bug sản phẩm. Không gọi mọi TC bổ sung sau review policy là AI bỏ sót.

TC26 ban đầu blocked vì Android CLI không lấy được idle state. MR-RUN-02 dùng `--no-idle`, kiểm tra readiness và persistence; kết quả sau được chọn theo quy ước summary, không xóa lần blocked. TC29 đã kiểm tra form/account trước khi bắt đầu lại, không tự lặp một submit có state không rõ.

MR-RUN-03 dừng sau hai C-guard liên tiếp; MR-RUN-04 phân biệt blocker schema đã biết với lỗi transport để tiếp tục phần độc lập. TC38 trong MR-RUN-04 hoàn tất lần reject đầu (account 0→0), nhưng chưa nhập được password lần hai vì bàn phím che field sau khi xuất hiện validation. Runner dừng trước submit lần hai. Sau kiểm tra UI/DB còn 0 account, xử lý field bị IME che rồi chạy lại.

MR-RUN-05 phát hiện lỗi quan sát: validation từ lần trước vẫn hiện, nhưng detector chỉ tìm text mới nên ghi nhầm TC38/39 là không feedback. Hai verdict này được giữ và đánh dấu lỗi harness, không tính thành bug sản phẩm. Đợt chạy dừng khi TC40 mới ở Login, chưa có account E40. MR-RUN-06 đọc cả validation đang hiện: TC38 hoàn tất reject→accept và TC39 reject đúng; MR-RUN-07 tiếp tục TC40–54. Đây là điều chỉnh cách quan sát, không thay expected.

Bằng chứng lỗi quan sát: [validation đang hiện trong TC38 / MR-RUN-05](images/MR-RUN-05-MR-TC38-actual.jpg). Ảnh này là chẩn đoán harness; các capture chẩn đoán trùng đã lưu ngoài repo.

Runner hiện ghi chung results, giữ app/session, không trace/layout dump hay ảnh pass; JPG chỉ lưu khi failure cần minh họa. Không thay nghiệp vụ, rule, literal input hoặc expected theo runtime. Đây là điều chỉnh harness/evidence, khác với thay thiết kế test.

## 5. Kết luận và phần còn lại

Đã có kết quả đánh giá cho 50/54 TC; 4 TC blocked (MR-TC34, MR-TC35, MR-TC36, MR-TC37); không còn TC chưa bắt đầu. Các ca Confirmation bị chặn do thiếu field thật; không gửi C bằng API hoặc tự thêm field để chạy. Một TC fail schema không thay việc thực thi các ca equality phụ thuộc.

Kết quả không đòi 100% pass để báo cáo trung thực: giữ toàn bộ fail và giới hạn. Sinh viên cần review bảng expected/actual và các ảnh/quan sát trước khi nghiệm thu. Đã hoàn tất đăng/kiểm tra 8 GitHub Issues và bổ sung 8 JPG trang issue cùng 1 JPG danh sách trong đợt report-only ngày 20/10/2026. Kết quả execution và ảnh SUT cũ giữ nguyên; log đăng/kiểm tra/chụp nằm trong results.json. Đợt bổ sung này không cập nhật AI audit hoặc tạo video. Không xuất PDF theo lựa chọn hiện tại. Bộ design/TC vẫn giữ nhãn Not Run tại thời điểm thiết kế; kết quả hiện hành ở report và results.json.

## 6. Log thực thi theo TC/run

Các trích đoạn dưới đây chỉ giữ trường cần đối chiếu từ bản ghi được chọn; lịch sử đầy đủ nằm trong [results.json](results.json). Thời gian giữ nguyên UTC; `input.confirmation` là dữ liệu TC, không chứng minh đã nhập khi form thiếu field. `input_verification` ghi mức xác minh thực tế. Các ca blocked giữ quan sát form và lý do chặn, không có submit giả.

<a id="log-mr-tc01"></a>
### MR-TC01 / MR-RUN-01

Nguồn: [results.json](results.json), `cases[0].results[6]`; ID `MR-TC01`, run `MR-RUN-01`, status `passed`.

**Actual đã ghi:** bước 1: account 0→1; báo thành công; Login

```json
{
  "started_at": "2026-10-19T18:35:19.847364+00:00",
  "finished_at": "2026-10-19T18:36:30.828131+00:00",
  "submissions": 1,
  "limitations": [
    "Confirmation absent; this case does not exercise MR-R10"
  ],
  "steps": [
    {
      "step": 1,
      "input": {
        "name": "Nguyen Van A",
        "email": "mr.t02r01.tc01@example.com",
        "password": "Abcde1!x",
        "confirmation": "Abcde1!x",
        "expected": "ACCEPT"
      },
      "ui": {
        "at": "2026-10-19T18:36:30.066912+00:00",
        "feedback": [
          "Đăng ký tài khoản thành công."
        ],
        "success_signal": true,
        "dialog_seen": true,
        "login": true,
        "registration": false,
        "timed_out": false
      },
      "accounts": [
        {
          "email": "mr.t02r01.tc01@example.com",
          "count_before": 0,
          "count_after": 1,
          "existing_rows_unchanged": true,
          "new_accounts": [
            {
              "id": 4,
              "name": "Nguyen Van A",
              "email": "mr.t02r01.tc01@example.com"
            }
          ]
        }
      ],
      "assertion_failures": [],
      "input_verification": [
        {
          "field": "name",
          "readback": "Nguyen Van A"
        },
        {
          "field": "email",
          "readback": "mr.t02r01.tc01@example.com"
        },
        {
          "field": "password",
          "readback": "masked: transport acknowledged; plaintext not exposed"
        }
      ]
    }
  ]
}
```

<a id="log-mr-tc02"></a>
### MR-TC02 / MR-RUN-01

Nguồn: [results.json](results.json), `cases[1].results[0]`; ID `MR-TC02`, run `MR-RUN-01`, status `failed`.

**Actual đã ghi:** bước 1: account 0→1; báo thành công; Login

```json
{
  "started_at": "2026-10-19T18:36:30.830414+00:00",
  "finished_at": "2026-10-19T18:37:41.281197+00:00",
  "submissions": 1,
  "limitations": [
    "Confirmation absent; this case does not exercise MR-R10"
  ],
  "steps": [
    {
      "step": 1,
      "input": {
        "name": "",
        "email": "mr.t02r01.tc02@example.com",
        "password": "Abcde1!x",
        "confirmation": "Abcde1!x",
        "expected": "REJECT"
      },
      "ui": {
        "at": "2026-10-19T18:37:40.500236+00:00",
        "feedback": [
          "Đăng ký tài khoản thành công."
        ],
        "success_signal": true,
        "dialog_seen": true,
        "login": true,
        "registration": false,
        "timed_out": false
      },
      "accounts": [
        {
          "email": "mr.t02r01.tc02@example.com",
          "count_before": 0,
          "count_after": 1,
          "existing_rows_unchanged": true,
          "new_accounts": [
            {
              "id": 5,
              "name": "",
              "email": "mr.t02r01.tc02@example.com"
            }
          ]
        }
      ],
      "assertion_failures": [
        "Invalid/duplicate submission created or changed watched account data",
        "Invalid submission reported registration success",
        "Invalid submission reached Login as if registration succeeded"
      ],
      "input_verification": [
        {
          "field": "name",
          "readback": ""
        },
        {
          "field": "email",
          "readback": "mr.t02r01.tc02@example.com"
        },
        {
          "field": "password",
          "readback": "masked: transport acknowledged; plaintext not exposed"
        }
      ]
    }
  ]
}
```

<a id="log-mr-tc03"></a>
### MR-TC03 / MR-RUN-01

Nguồn: [results.json](results.json), `cases[2].results[0]`; ID `MR-TC03`, run `MR-RUN-01`, status `passed`.

**Actual đã ghi:** bước 1: account 0→1; báo thành công; Login

```json
{
  "started_at": "2026-10-19T18:37:41.282494+00:00",
  "finished_at": "2026-10-19T18:38:52.229118+00:00",
  "submissions": 1,
  "limitations": [
    "Confirmation absent; this case does not exercise MR-R10"
  ],
  "steps": [
    {
      "step": 1,
      "input": {
        "name": "V",
        "email": "mr.t02r01.tc03@example.com",
        "password": "Abcde1!x",
        "confirmation": "Abcde1!x",
        "expected": "ACCEPT"
      },
      "ui": {
        "at": "2026-10-19T18:38:51.471137+00:00",
        "feedback": [
          "Đăng ký tài khoản thành công."
        ],
        "success_signal": true,
        "dialog_seen": true,
        "login": true,
        "registration": false,
        "timed_out": false
      },
      "accounts": [
        {
          "email": "mr.t02r01.tc03@example.com",
          "count_before": 0,
          "count_after": 1,
          "existing_rows_unchanged": true,
          "new_accounts": [
            {
              "id": 6,
              "name": "V",
              "email": "mr.t02r01.tc03@example.com"
            }
          ]
        }
      ],
      "assertion_failures": [],
      "input_verification": [
        {
          "field": "name",
          "readback": "V"
        },
        {
          "field": "email",
          "readback": "mr.t02r01.tc03@example.com"
        },
        {
          "field": "password",
          "readback": "masked: transport acknowledged; plaintext not exposed"
        }
      ]
    }
  ]
}
```

<a id="log-mr-tc04"></a>
### MR-TC04 / MR-RUN-01

Nguồn: [results.json](results.json), `cases[3].results[0]`; ID `MR-TC04`, run `MR-RUN-01`, status `passed`.

**Actual đã ghi:** bước 1: account 0→1; báo thành công; Login

```json
{
  "started_at": "2026-10-19T18:38:52.230436+00:00",
  "finished_at": "2026-10-19T18:40:04.011006+00:00",
  "submissions": 1,
  "limitations": [
    "Confirmation absent; this case does not exercise MR-R10"
  ],
  "steps": [
    {
      "step": 1,
      "input": {
        "name": "Vy",
        "email": "mr.t02r01.tc04@example.com",
        "password": "Abcde1!x",
        "confirmation": "Abcde1!x",
        "expected": "ACCEPT"
      },
      "ui": {
        "at": "2026-10-19T18:40:03.241341+00:00",
        "feedback": [
          "Đăng ký tài khoản thành công."
        ],
        "success_signal": true,
        "dialog_seen": true,
        "login": true,
        "registration": false,
        "timed_out": false
      },
      "accounts": [
        {
          "email": "mr.t02r01.tc04@example.com",
          "count_before": 0,
          "count_after": 1,
          "existing_rows_unchanged": true,
          "new_accounts": [
            {
              "id": 7,
              "name": "Vy",
              "email": "mr.t02r01.tc04@example.com"
            }
          ]
        }
      ],
      "assertion_failures": [],
      "input_verification": [
        {
          "field": "name",
          "readback": "Vy"
        },
        {
          "field": "email",
          "readback": "mr.t02r01.tc04@example.com"
        },
        {
          "field": "password",
          "readback": "masked: transport acknowledged; plaintext not exposed"
        }
      ]
    }
  ]
}
```

<a id="log-mr-tc05"></a>
### MR-TC05 / MR-RUN-01

Nguồn: [results.json](results.json), `cases[4].results[0]`; ID `MR-TC05`, run `MR-RUN-01`, status `passed`.

**Actual đã ghi:** bước 1: account 0→1; báo thành công; Login

```json
{
  "started_at": "2026-10-19T18:40:04.012723+00:00",
  "finished_at": "2026-10-19T18:41:13.231312+00:00",
  "submissions": 1,
  "limitations": [
    "Confirmation absent; this case does not exercise MR-R10"
  ],
  "steps": [
    {
      "step": 1,
      "input": {
        "name": "Trần Quốc Vỹ",
        "email": "mr.t02r01.tc05@example.com",
        "password": "Abcde1!x",
        "confirmation": "Abcde1!x",
        "expected": "ACCEPT"
      },
      "ui": {
        "at": "2026-10-19T18:41:12.452155+00:00",
        "feedback": [
          "Đăng ký tài khoản thành công."
        ],
        "success_signal": true,
        "dialog_seen": true,
        "login": true,
        "registration": false,
        "timed_out": false
      },
      "accounts": [
        {
          "email": "mr.t02r01.tc05@example.com",
          "count_before": 0,
          "count_after": 1,
          "existing_rows_unchanged": true,
          "new_accounts": [
            {
              "id": 8,
              "name": "Trần Quốc Vỹ",
              "email": "mr.t02r01.tc05@example.com"
            }
          ]
        }
      ],
      "assertion_failures": [],
      "input_verification": [
        {
          "field": "name",
          "readback": "Trần Quốc Vỹ"
        },
        {
          "field": "email",
          "readback": "mr.t02r01.tc05@example.com"
        },
        {
          "field": "password",
          "readback": "masked: transport acknowledged; plaintext not exposed"
        }
      ]
    }
  ]
}
```

<a id="log-mr-tc06"></a>
### MR-TC06 / MR-RUN-01

Nguồn: [results.json](results.json), `cases[5].results[0]`; ID `MR-TC06`, run `MR-RUN-01`, status `failed`.

**Actual đã ghi:** bước 1: account 0→1; báo thành công; Login

```json
{
  "started_at": "2026-10-19T18:41:13.232435+00:00",
  "finished_at": "2026-10-19T18:42:23.375040+00:00",
  "submissions": 1,
  "limitations": [
    "Confirmation absent; this case does not exercise MR-R10"
  ],
  "steps": [
    {
      "step": 1,
      "input": {
        "name": "Nguyen Van A",
        "email": "",
        "password": "Abcde1!x",
        "confirmation": "Abcde1!x",
        "expected": "REJECT"
      },
      "ui": {
        "at": "2026-10-19T18:42:22.591697+00:00",
        "feedback": [
          "Đăng ký tài khoản thành công."
        ],
        "success_signal": true,
        "dialog_seen": true,
        "login": true,
        "registration": false,
        "timed_out": false
      },
      "accounts": [
        {
          "email": "",
          "count_before": 0,
          "count_after": 1,
          "existing_rows_unchanged": true,
          "new_accounts": [
            {
              "id": 9,
              "name": "Nguyen Van A",
              "email": ""
            }
          ]
        }
      ],
      "assertion_failures": [
        "Invalid/duplicate submission created or changed watched account data",
        "Invalid submission reported registration success",
        "Invalid submission reached Login as if registration succeeded"
      ],
      "input_verification": [
        {
          "field": "name",
          "readback": "Nguyen Van A"
        },
        {
          "field": "email",
          "readback": ""
        },
        {
          "field": "password",
          "readback": "masked: transport acknowledged; plaintext not exposed"
        }
      ]
    }
  ]
}
```

<a id="log-mr-tc07"></a>
### MR-TC07 / MR-RUN-01

Nguồn: [results.json](results.json), `cases[6].results[0]`; ID `MR-TC07`, run `MR-RUN-01`, status `failed`.

**Actual đã ghi:** bước 1: account 0→1; báo thành công; Login

```json
{
  "started_at": "2026-10-19T18:42:23.376141+00:00",
  "finished_at": "2026-10-19T18:43:31.875957+00:00",
  "submissions": 1,
  "limitations": [
    "Confirmation absent; this case does not exercise MR-R10"
  ],
  "steps": [
    {
      "step": 1,
      "input": {
        "name": "Nguyen Van A",
        "email": "mr.t02r01.tc07.example.com",
        "password": "Abcde1!x",
        "confirmation": "Abcde1!x",
        "expected": "REJECT"
      },
      "ui": {
        "at": "2026-10-19T18:43:31.109947+00:00",
        "feedback": [
          "Đăng ký tài khoản thành công."
        ],
        "success_signal": true,
        "dialog_seen": true,
        "login": true,
        "registration": false,
        "timed_out": false
      },
      "accounts": [
        {
          "email": "mr.t02r01.tc07.example.com",
          "count_before": 0,
          "count_after": 1,
          "existing_rows_unchanged": true,
          "new_accounts": [
            {
              "id": 10,
              "name": "Nguyen Van A",
              "email": "mr.t02r01.tc07.example.com"
            }
          ]
        }
      ],
      "assertion_failures": [
        "Invalid/duplicate submission created or changed watched account data",
        "Invalid submission reported registration success",
        "Invalid submission reached Login as if registration succeeded"
      ],
      "input_verification": [
        {
          "field": "name",
          "readback": "Nguyen Van A"
        },
        {
          "field": "email",
          "readback": "mr.t02r01.tc07.example.com"
        },
        {
          "field": "password",
          "readback": "masked: transport acknowledged; plaintext not exposed"
        }
      ]
    }
  ]
}
```

<a id="log-mr-tc08"></a>
### MR-TC08 / MR-RUN-01

Nguồn: [results.json](results.json), `cases[7].results[0]`; ID `MR-TC08`, run `MR-RUN-01`, status `failed`.

**Actual đã ghi:** bước 1: account 0→1; báo thành công; Login

```json
{
  "started_at": "2026-10-19T18:43:31.877024+00:00",
  "finished_at": "2026-10-19T18:44:44.362474+00:00",
  "submissions": 1,
  "limitations": [
    "Confirmation absent; this case does not exercise MR-R10"
  ],
  "steps": [
    {
      "step": 1,
      "input": {
        "name": "Nguyen Van A",
        "email": "@example.com",
        "password": "Abcde1!x",
        "confirmation": "Abcde1!x",
        "expected": "REJECT"
      },
      "ui": {
        "at": "2026-10-19T18:44:43.581963+00:00",
        "feedback": [
          "Đăng ký tài khoản thành công."
        ],
        "success_signal": true,
        "dialog_seen": true,
        "login": true,
        "registration": false,
        "timed_out": false
      },
      "accounts": [
        {
          "email": "@example.com",
          "count_before": 0,
          "count_after": 1,
          "existing_rows_unchanged": true,
          "new_accounts": [
            {
              "id": 11,
              "name": "Nguyen Van A",
              "email": "@example.com"
            }
          ]
        }
      ],
      "assertion_failures": [
        "Invalid/duplicate submission created or changed watched account data",
        "Invalid submission reported registration success",
        "Invalid submission reached Login as if registration succeeded"
      ],
      "input_verification": [
        {
          "field": "name",
          "readback": "Nguyen Van A"
        },
        {
          "field": "email",
          "readback": "@example.com"
        },
        {
          "field": "password",
          "readback": "masked: transport acknowledged; plaintext not exposed"
        }
      ]
    }
  ]
}
```

<a id="log-mr-tc09"></a>
### MR-TC09 / MR-RUN-01

Nguồn: [results.json](results.json), `cases[8].results[0]`; ID `MR-TC09`, run `MR-RUN-01`, status `failed`.

**Actual đã ghi:** bước 1: account 0→1; báo thành công; Login

```json
{
  "started_at": "2026-10-19T18:44:44.363919+00:00",
  "finished_at": "2026-10-19T18:45:55.259595+00:00",
  "submissions": 1,
  "limitations": [
    "Confirmation absent; this case does not exercise MR-R10"
  ],
  "steps": [
    {
      "step": 1,
      "input": {
        "name": "Nguyen Van A",
        "email": "mr.t02r01.tc09@",
        "password": "Abcde1!x",
        "confirmation": "Abcde1!x",
        "expected": "REJECT"
      },
      "ui": {
        "at": "2026-10-19T18:45:54.474715+00:00",
        "feedback": [
          "Đăng ký tài khoản thành công."
        ],
        "success_signal": true,
        "dialog_seen": true,
        "login": true,
        "registration": false,
        "timed_out": false
      },
      "accounts": [
        {
          "email": "mr.t02r01.tc09@",
          "count_before": 0,
          "count_after": 1,
          "existing_rows_unchanged": true,
          "new_accounts": [
            {
              "id": 12,
              "name": "Nguyen Van A",
              "email": "mr.t02r01.tc09@"
            }
          ]
        }
      ],
      "assertion_failures": [
        "Invalid/duplicate submission created or changed watched account data",
        "Invalid submission reported registration success",
        "Invalid submission reached Login as if registration succeeded"
      ],
      "input_verification": [
        {
          "field": "name",
          "readback": "Nguyen Van A"
        },
        {
          "field": "email",
          "readback": "mr.t02r01.tc09@"
        },
        {
          "field": "password",
          "readback": "masked: transport acknowledged; plaintext not exposed"
        }
      ]
    }
  ]
}
```

<a id="log-mr-tc10"></a>
### MR-TC10 / MR-RUN-01

Nguồn: [results.json](results.json), `cases[9].results[0]`; ID `MR-TC10`, run `MR-RUN-01`, status `failed`.

**Actual đã ghi:** bước 1: account 0→1; báo thành công; Login

```json
{
  "started_at": "2026-10-19T18:45:55.261050+00:00",
  "finished_at": "2026-10-19T18:47:06.492764+00:00",
  "submissions": 1,
  "limitations": [
    "Confirmation absent; this case does not exercise MR-R10"
  ],
  "steps": [
    {
      "step": 1,
      "input": {
        "name": "Nguyen Van A",
        "email": "mr t02r01.tc10@example.com",
        "password": "Abcde1!x",
        "confirmation": "Abcde1!x",
        "expected": "REJECT"
      },
      "ui": {
        "at": "2026-10-19T18:47:05.699762+00:00",
        "feedback": [
          "Đăng ký tài khoản thành công."
        ],
        "success_signal": true,
        "dialog_seen": true,
        "login": true,
        "registration": false,
        "timed_out": false
      },
      "accounts": [
        {
          "email": "mr t02r01.tc10@example.com",
          "count_before": 0,
          "count_after": 1,
          "existing_rows_unchanged": true,
          "new_accounts": [
            {
              "id": 13,
              "name": "Nguyen Van A",
              "email": "mr t02r01.tc10@example.com"
            }
          ]
        }
      ],
      "assertion_failures": [
        "Invalid/duplicate submission created or changed watched account data",
        "Invalid submission reported registration success",
        "Invalid submission reached Login as if registration succeeded"
      ],
      "input_verification": [
        {
          "field": "name",
          "readback": "Nguyen Van A"
        },
        {
          "field": "email",
          "readback": "mr t02r01.tc10@example.com"
        },
        {
          "field": "password",
          "readback": "masked: transport acknowledged; plaintext not exposed"
        }
      ]
    }
  ]
}
```

<a id="log-mr-tc11"></a>
### MR-TC11 / MR-RUN-01

Nguồn: [results.json](results.json), `cases[10].results[0]`; ID `MR-TC11`, run `MR-RUN-01`, status `failed`.

**Actual đã ghi:** bước 1: account 0→1; báo thành công; Login

```json
{
  "started_at": "2026-10-19T18:47:06.494106+00:00",
  "finished_at": "2026-10-19T18:48:17.082916+00:00",
  "submissions": 1,
  "limitations": [
    "Confirmation absent; this case does not exercise MR-R10"
  ],
  "steps": [
    {
      "step": 1,
      "input": {
        "name": "Nguyen Van A",
        "email": "mr.t02r01.tc11@@example.com",
        "password": "Abcde1!x",
        "confirmation": "Abcde1!x",
        "expected": "REJECT"
      },
      "ui": {
        "at": "2026-10-19T18:48:16.254974+00:00",
        "feedback": [
          "Đăng ký tài khoản thành công."
        ],
        "success_signal": true,
        "dialog_seen": true,
        "login": true,
        "registration": false,
        "timed_out": false
      },
      "accounts": [
        {
          "email": "mr.t02r01.tc11@@example.com",
          "count_before": 0,
          "count_after": 1,
          "existing_rows_unchanged": true,
          "new_accounts": [
            {
              "id": 14,
              "name": "Nguyen Van A",
              "email": "mr.t02r01.tc11@@example.com"
            }
          ]
        }
      ],
      "assertion_failures": [
        "Invalid/duplicate submission created or changed watched account data",
        "Invalid submission reported registration success",
        "Invalid submission reached Login as if registration succeeded"
      ],
      "input_verification": [
        {
          "field": "name",
          "readback": "Nguyen Van A"
        },
        {
          "field": "email",
          "readback": "mr.t02r01.tc11@@example.com"
        },
        {
          "field": "password",
          "readback": "masked: transport acknowledged; plaintext not exposed"
        }
      ]
    }
  ]
}
```

<a id="log-mr-tc12"></a>
### MR-TC12 / MR-RUN-01

Nguồn: [results.json](results.json), `cases[11].results[0]`; ID `MR-TC12`, run `MR-RUN-01`, status `failed`.

**Actual đã ghi:** bước 1: account 1→2; báo thành công; Login

```json
{
  "started_at": "2026-10-19T18:48:17.086434+00:00",
  "finished_at": "2026-10-19T18:49:27.402865+00:00",
  "submissions": 1,
  "limitations": [
    "Confirmation absent; this case does not exercise MR-R10"
  ],
  "steps": [
    {
      "step": 1,
      "input": {
        "name": "Nguyen Van A",
        "email": "test@eshop.com",
        "password": "Abcde1!x",
        "confirmation": "Abcde1!x",
        "expected": "REJECT"
      },
      "ui": {
        "at": "2026-10-19T18:49:26.627379+00:00",
        "feedback": [
          "Đăng ký tài khoản thành công."
        ],
        "success_signal": true,
        "dialog_seen": true,
        "login": true,
        "registration": false,
        "timed_out": false
      },
      "accounts": [
        {
          "email": "test@eshop.com",
          "count_before": 1,
          "count_after": 2,
          "existing_rows_unchanged": true,
          "new_accounts": [
            {
              "id": 15,
              "name": "Nguyen Van A",
              "email": "test@eshop.com"
            }
          ]
        }
      ],
      "assertion_failures": [
        "Invalid/duplicate submission created or changed watched account data",
        "Invalid submission reported registration success",
        "Invalid submission reached Login as if registration succeeded"
      ],
      "input_verification": [
        {
          "field": "name",
          "readback": "Nguyen Van A"
        },
        {
          "field": "email",
          "readback": "test@eshop.com"
        },
        {
          "field": "password",
          "readback": "masked: transport acknowledged; plaintext not exposed"
        }
      ]
    }
  ]
}
```

<a id="log-mr-tc13"></a>
### MR-TC13 / MR-RUN-01

Nguồn: [results.json](results.json), `cases[12].results[0]`; ID `MR-TC13`, run `MR-RUN-01`, status `failed`.

**Actual đã ghi:** bước 1: account 0→1; báo thành công; Login; bước 2: account 1→2; báo thành công; Login

```json
{
  "started_at": "2026-10-19T18:49:27.404080+00:00",
  "finished_at": "2026-10-19T18:51:42.463905+00:00",
  "submissions": 2,
  "limitations": [
    "Confirmation absent; this case does not exercise MR-R10"
  ],
  "steps": [
    {
      "step": 1,
      "input": {
        "name": "Nguyen Van A",
        "email": "mr.t02r01.tc13@example.com",
        "password": "Abcde1!x",
        "confirmation": "Abcde1!x",
        "expected": "ACCEPT"
      },
      "ui": {
        "at": "2026-10-19T18:50:36.161480+00:00",
        "feedback": [
          "Đăng ký tài khoản thành công."
        ],
        "success_signal": true,
        "dialog_seen": true,
        "login": true,
        "registration": false,
        "timed_out": false
      },
      "accounts": [
        {
          "email": "mr.t02r01.tc13@example.com",
          "count_before": 0,
          "count_after": 1,
          "existing_rows_unchanged": true,
          "new_accounts": [
            {
              "id": 16,
              "name": "Nguyen Van A",
              "email": "mr.t02r01.tc13@example.com"
            }
          ]
        }
      ],
      "assertion_failures": [],
      "input_verification": [
        {
          "field": "name",
          "readback": "Nguyen Van A"
        },
        {
          "field": "email",
          "readback": "mr.t02r01.tc13@example.com"
        },
        {
          "field": "password",
          "readback": "masked: transport acknowledged; plaintext not exposed"
        }
      ]
    },
    {
      "step": 2,
      "input": {
        "name": "Nguyen Van A",
        "email": "mr.t02r01.tc13@example.com",
        "password": "Abcde1!x",
        "confirmation": "Abcde1!x",
        "expected": "REJECT"
      },
      "ui": {
        "at": "2026-10-19T18:51:41.693804+00:00",
        "feedback": [
          "Đăng ký tài khoản thành công."
        ],
        "success_signal": true,
        "dialog_seen": true,
        "login": true,
        "registration": false,
        "timed_out": false
      },
      "accounts": [
        {
          "email": "mr.t02r01.tc13@example.com",
          "count_before": 1,
          "count_after": 2,
          "existing_rows_unchanged": true,
          "new_accounts": [
            {
              "id": 17,
              "name": "Nguyen Van A",
              "email": "mr.t02r01.tc13@example.com"
            }
          ]
        }
      ],
      "assertion_failures": [
        "Invalid/duplicate submission created or changed watched account data",
        "Invalid submission reported registration success",
        "Invalid submission reached Login as if registration succeeded"
      ],
      "input_verification": [
        {
          "field": "name",
          "readback": "Nguyen Van A"
        },
        {
          "field": "email",
          "readback": "mr.t02r01.tc13@example.com"
        },
        {
          "field": "password",
          "readback": "masked: transport acknowledged; plaintext not exposed"
        }
      ]
    }
  ]
}
```

<a id="log-mr-tc14"></a>
### MR-TC14 / MR-RUN-01

Nguồn: [results.json](results.json), `cases[13].results[0]`; ID `MR-TC14`, run `MR-RUN-01`, status `passed`.

**Actual đã ghi:** bước 1: account không đổi; có validation; form Đăng ký

```json
{
  "started_at": "2026-10-19T18:51:42.465227+00:00",
  "finished_at": "2026-10-19T18:52:53.219587+00:00",
  "submissions": 1,
  "limitations": [
    "Confirmation absent; this case does not exercise MR-R10"
  ],
  "steps": [
    {
      "step": 1,
      "input": {
        "name": "Nguyen Van A",
        "email": "mr.t02r01.tc14@example.com",
        "password": "",
        "confirmation": "",
        "expected": "REJECT"
      },
      "ui": {
        "at": "2026-10-19T18:52:52.433024+00:00",
        "feedback": [
          "Mật khẩu quá yếu! Phải dài tối thiểu 8 ký tự, gồm chữ hoa, chữ thường, số và KÝ TỰ ĐẶC BIỆT."
        ],
        "success_signal": false,
        "dialog_seen": false,
        "login": false,
        "registration": true,
        "timed_out": false
      },
      "accounts": [
        {
          "email": "mr.t02r01.tc14@example.com",
          "count_before": 0,
          "count_after": 0,
          "existing_rows_unchanged": true,
          "new_accounts": []
        }
      ],
      "assertion_failures": [],
      "input_verification": [
        {
          "field": "name",
          "readback": "Nguyen Van A"
        },
        {
          "field": "email",
          "readback": "mr.t02r01.tc14@example.com"
        },
        {
          "field": "password",
          "readback": "masked: transport acknowledged; plaintext not exposed"
        }
      ]
    }
  ]
}
```

<a id="log-mr-tc15"></a>
### MR-TC15 / MR-RUN-01

Nguồn: [results.json](results.json), `cases[14].results[0]`; ID `MR-TC15`, run `MR-RUN-01`, status `passed`.

**Actual đã ghi:** bước 1: account không đổi; có validation; form Đăng ký

```json
{
  "started_at": "2026-10-19T18:52:53.221109+00:00",
  "finished_at": "2026-10-19T18:54:00.454346+00:00",
  "submissions": 1,
  "limitations": [
    "Confirmation absent; this case does not exercise MR-R10"
  ],
  "steps": [
    {
      "step": 1,
      "input": {
        "name": "Nguyen Van A",
        "email": "mr.t02r01.tc15@example.com",
        "password": "Abcde1!",
        "confirmation": "Abcde1!",
        "expected": "REJECT"
      },
      "ui": {
        "at": "2026-10-19T18:53:59.680922+00:00",
        "feedback": [
          "Mật khẩu quá yếu! Phải dài tối thiểu 8 ký tự, gồm chữ hoa, chữ thường, số và KÝ TỰ ĐẶC BIỆT."
        ],
        "success_signal": false,
        "dialog_seen": false,
        "login": false,
        "registration": true,
        "timed_out": false
      },
      "accounts": [
        {
          "email": "mr.t02r01.tc15@example.com",
          "count_before": 0,
          "count_after": 0,
          "existing_rows_unchanged": true,
          "new_accounts": []
        }
      ],
      "assertion_failures": [],
      "input_verification": [
        {
          "field": "name",
          "readback": "Nguyen Van A"
        },
        {
          "field": "email",
          "readback": "mr.t02r01.tc15@example.com"
        },
        {
          "field": "password",
          "readback": "masked: transport acknowledged; plaintext not exposed"
        }
      ]
    }
  ]
}
```

<a id="log-mr-tc16"></a>
### MR-TC16 / MR-RUN-01

Nguồn: [results.json](results.json), `cases[15].results[0]`; ID `MR-TC16`, run `MR-RUN-01`, status `passed`.

**Actual đã ghi:** bước 1: account 0→1; báo thành công; Login

```json
{
  "started_at": "2026-10-19T18:54:00.455976+00:00",
  "finished_at": "2026-10-19T18:55:09.858017+00:00",
  "submissions": 1,
  "limitations": [
    "Confirmation absent; this case does not exercise MR-R10"
  ],
  "steps": [
    {
      "step": 1,
      "input": {
        "name": "Nguyen Van A",
        "email": "mr.t02r01.tc16@example.com",
        "password": "Abcde1!x",
        "confirmation": "Abcde1!x",
        "expected": "ACCEPT"
      },
      "ui": {
        "at": "2026-10-19T18:55:09.091490+00:00",
        "feedback": [
          "Đăng ký tài khoản thành công."
        ],
        "success_signal": true,
        "dialog_seen": true,
        "login": true,
        "registration": false,
        "timed_out": false
      },
      "accounts": [
        {
          "email": "mr.t02r01.tc16@example.com",
          "count_before": 0,
          "count_after": 1,
          "existing_rows_unchanged": true,
          "new_accounts": [
            {
              "id": 18,
              "name": "Nguyen Van A",
              "email": "mr.t02r01.tc16@example.com"
            }
          ]
        }
      ],
      "assertion_failures": [],
      "input_verification": [
        {
          "field": "name",
          "readback": "Nguyen Van A"
        },
        {
          "field": "email",
          "readback": "mr.t02r01.tc16@example.com"
        },
        {
          "field": "password",
          "readback": "masked: transport acknowledged; plaintext not exposed"
        }
      ]
    }
  ]
}
```

<a id="log-mr-tc17"></a>
### MR-TC17 / MR-RUN-01

Nguồn: [results.json](results.json), `cases[16].results[0]`; ID `MR-TC17`, run `MR-RUN-01`, status `passed`.

**Actual đã ghi:** bước 1: account 0→1; báo thành công; Login

```json
{
  "started_at": "2026-10-19T18:55:09.861443+00:00",
  "finished_at": "2026-10-19T18:56:19.103006+00:00",
  "submissions": 1,
  "limitations": [
    "Confirmation absent; this case does not exercise MR-R10"
  ],
  "steps": [
    {
      "step": 1,
      "input": {
        "name": "Nguyen Van A",
        "email": "mr.t02r01.tc17@example.com",
        "password": "Abcde1!xy",
        "confirmation": "Abcde1!xy",
        "expected": "ACCEPT"
      },
      "ui": {
        "at": "2026-10-19T18:56:18.339297+00:00",
        "feedback": [
          "Đăng ký tài khoản thành công."
        ],
        "success_signal": true,
        "dialog_seen": true,
        "login": true,
        "registration": false,
        "timed_out": false
      },
      "accounts": [
        {
          "email": "mr.t02r01.tc17@example.com",
          "count_before": 0,
          "count_after": 1,
          "existing_rows_unchanged": true,
          "new_accounts": [
            {
              "id": 19,
              "name": "Nguyen Van A",
              "email": "mr.t02r01.tc17@example.com"
            }
          ]
        }
      ],
      "assertion_failures": [],
      "input_verification": [
        {
          "field": "name",
          "readback": "Nguyen Van A"
        },
        {
          "field": "email",
          "readback": "mr.t02r01.tc17@example.com"
        },
        {
          "field": "password",
          "readback": "masked: transport acknowledged; plaintext not exposed"
        }
      ]
    }
  ]
}
```

<a id="log-mr-tc18"></a>
### MR-TC18 / MR-RUN-01

Nguồn: [results.json](results.json), `cases[17].results[0]`; ID `MR-TC18`, run `MR-RUN-01`, status `passed`.

**Actual đã ghi:** bước 1: account không đổi; có validation; form Đăng ký

```json
{
  "started_at": "2026-10-19T18:56:19.104463+00:00",
  "finished_at": "2026-10-19T18:57:27.709547+00:00",
  "submissions": 1,
  "limitations": [
    "Confirmation absent; this case does not exercise MR-R10"
  ],
  "steps": [
    {
      "step": 1,
      "input": {
        "name": "Nguyen Van A",
        "email": "mr.t02r01.tc18@example.com",
        "password": "abcde1!x",
        "confirmation": "abcde1!x",
        "expected": "REJECT"
      },
      "ui": {
        "at": "2026-10-19T18:57:26.937180+00:00",
        "feedback": [
          "Mật khẩu quá yếu! Phải dài tối thiểu 8 ký tự, gồm chữ hoa, chữ thường, số và KÝ TỰ ĐẶC BIỆT."
        ],
        "success_signal": false,
        "dialog_seen": false,
        "login": false,
        "registration": true,
        "timed_out": false
      },
      "accounts": [
        {
          "email": "mr.t02r01.tc18@example.com",
          "count_before": 0,
          "count_after": 0,
          "existing_rows_unchanged": true,
          "new_accounts": []
        }
      ],
      "assertion_failures": [],
      "input_verification": [
        {
          "field": "name",
          "readback": "Nguyen Van A"
        },
        {
          "field": "email",
          "readback": "mr.t02r01.tc18@example.com"
        },
        {
          "field": "password",
          "readback": "masked: transport acknowledged; plaintext not exposed"
        }
      ]
    }
  ]
}
```

<a id="log-mr-tc19"></a>
### MR-TC19 / MR-RUN-01

Nguồn: [results.json](results.json), `cases[18].results[0]`; ID `MR-TC19`, run `MR-RUN-01`, status `passed`.

**Actual đã ghi:** bước 1: account 0→1; báo thành công; Login

```json
{
  "started_at": "2026-10-19T18:57:27.711229+00:00",
  "finished_at": "2026-10-19T18:58:36.311655+00:00",
  "submissions": 1,
  "limitations": [
    "Confirmation absent; this case does not exercise MR-R10"
  ],
  "steps": [
    {
      "step": 1,
      "input": {
        "name": "Nguyen Van A",
        "email": "mr.t02r01.tc19@example.com",
        "password": "ABcde1!x",
        "confirmation": "ABcde1!x",
        "expected": "ACCEPT"
      },
      "ui": {
        "at": "2026-10-19T18:58:35.538374+00:00",
        "feedback": [
          "Đăng ký tài khoản thành công."
        ],
        "success_signal": true,
        "dialog_seen": true,
        "login": true,
        "registration": false,
        "timed_out": false
      },
      "accounts": [
        {
          "email": "mr.t02r01.tc19@example.com",
          "count_before": 0,
          "count_after": 1,
          "existing_rows_unchanged": true,
          "new_accounts": [
            {
              "id": 20,
              "name": "Nguyen Van A",
              "email": "mr.t02r01.tc19@example.com"
            }
          ]
        }
      ],
      "assertion_failures": [],
      "input_verification": [
        {
          "field": "name",
          "readback": "Nguyen Van A"
        },
        {
          "field": "email",
          "readback": "mr.t02r01.tc19@example.com"
        },
        {
          "field": "password",
          "readback": "masked: transport acknowledged; plaintext not exposed"
        }
      ]
    }
  ]
}
```

<a id="log-mr-tc20"></a>
### MR-TC20 / MR-RUN-01

Nguồn: [results.json](results.json), `cases[19].results[0]`; ID `MR-TC20`, run `MR-RUN-01`, status `passed`.

**Actual đã ghi:** bước 1: account không đổi; có validation; form Đăng ký

```json
{
  "started_at": "2026-10-19T18:58:36.313257+00:00",
  "finished_at": "2026-10-19T18:59:45.549721+00:00",
  "submissions": 1,
  "limitations": [
    "Confirmation absent; this case does not exercise MR-R10"
  ],
  "steps": [
    {
      "step": 1,
      "input": {
        "name": "Nguyen Van A",
        "email": "mr.t02r01.tc20@example.com",
        "password": "ABCDE1!X",
        "confirmation": "ABCDE1!X",
        "expected": "REJECT"
      },
      "ui": {
        "at": "2026-10-19T18:59:44.761664+00:00",
        "feedback": [
          "Mật khẩu quá yếu! Phải dài tối thiểu 8 ký tự, gồm chữ hoa, chữ thường, số và KÝ TỰ ĐẶC BIỆT."
        ],
        "success_signal": false,
        "dialog_seen": false,
        "login": false,
        "registration": true,
        "timed_out": false
      },
      "accounts": [
        {
          "email": "mr.t02r01.tc20@example.com",
          "count_before": 0,
          "count_after": 0,
          "existing_rows_unchanged": true,
          "new_accounts": []
        }
      ],
      "assertion_failures": [],
      "input_verification": [
        {
          "field": "name",
          "readback": "Nguyen Van A"
        },
        {
          "field": "email",
          "readback": "mr.t02r01.tc20@example.com"
        },
        {
          "field": "password",
          "readback": "masked: transport acknowledged; plaintext not exposed"
        }
      ]
    }
  ]
}
```

<a id="log-mr-tc21"></a>
### MR-TC21 / MR-RUN-01

Nguồn: [results.json](results.json), `cases[20].results[0]`; ID `MR-TC21`, run `MR-RUN-01`, status `passed`.

**Actual đã ghi:** bước 1: account 0→1; báo thành công; Login

```json
{
  "started_at": "2026-10-19T18:59:45.551665+00:00",
  "finished_at": "2026-10-19T19:01:00.587762+00:00",
  "submissions": 1,
  "limitations": [
    "Confirmation absent; this case does not exercise MR-R10"
  ],
  "steps": [
    {
      "step": 1,
      "input": {
        "name": "Nguyen Van A",
        "email": "mr.t02r01.tc21@example.com",
        "password": "ABCDa1!X",
        "confirmation": "ABCDa1!X",
        "expected": "ACCEPT"
      },
      "ui": {
        "at": "2026-10-19T19:00:59.820254+00:00",
        "feedback": [
          "Đăng ký tài khoản thành công."
        ],
        "success_signal": true,
        "dialog_seen": true,
        "login": true,
        "registration": false,
        "timed_out": false
      },
      "accounts": [
        {
          "email": "mr.t02r01.tc21@example.com",
          "count_before": 0,
          "count_after": 1,
          "existing_rows_unchanged": true,
          "new_accounts": [
            {
              "id": 21,
              "name": "Nguyen Van A",
              "email": "mr.t02r01.tc21@example.com"
            }
          ]
        }
      ],
      "assertion_failures": [],
      "input_verification": [
        {
          "field": "name",
          "readback": "Nguyen Van A"
        },
        {
          "field": "email",
          "readback": "mr.t02r01.tc21@example.com"
        },
        {
          "field": "password",
          "readback": "masked: transport acknowledged; plaintext not exposed"
        }
      ]
    }
  ]
}
```

<a id="log-mr-tc22"></a>
### MR-TC22 / MR-RUN-01

Nguồn: [results.json](results.json), `cases[21].results[0]`; ID `MR-TC22`, run `MR-RUN-01`, status `passed`.

**Actual đã ghi:** bước 1: account 0→1; báo thành công; Login

```json
{
  "started_at": "2026-10-19T19:01:00.589392+00:00",
  "finished_at": "2026-10-19T19:02:12.666018+00:00",
  "submissions": 1,
  "limitations": [
    "Confirmation absent; this case does not exercise MR-R10"
  ],
  "steps": [
    {
      "step": 1,
      "input": {
        "name": "Nguyen Van A",
        "email": "mr.t02r01.tc22@example.com",
        "password": "ABCDab1!",
        "confirmation": "ABCDab1!",
        "expected": "ACCEPT"
      },
      "ui": {
        "at": "2026-10-19T19:02:11.865398+00:00",
        "feedback": [
          "Đăng ký tài khoản thành công."
        ],
        "success_signal": true,
        "dialog_seen": true,
        "login": true,
        "registration": false,
        "timed_out": false
      },
      "accounts": [
        {
          "email": "mr.t02r01.tc22@example.com",
          "count_before": 0,
          "count_after": 1,
          "existing_rows_unchanged": true,
          "new_accounts": [
            {
              "id": 22,
              "name": "Nguyen Van A",
              "email": "mr.t02r01.tc22@example.com"
            }
          ]
        }
      ],
      "assertion_failures": [],
      "input_verification": [
        {
          "field": "name",
          "readback": "Nguyen Van A"
        },
        {
          "field": "email",
          "readback": "mr.t02r01.tc22@example.com"
        },
        {
          "field": "password",
          "readback": "masked: transport acknowledged; plaintext not exposed"
        }
      ]
    }
  ]
}
```

<a id="log-mr-tc23"></a>
### MR-TC23 / MR-RUN-01

Nguồn: [results.json](results.json), `cases[22].results[0]`; ID `MR-TC23`, run `MR-RUN-01`, status `passed`.

**Actual đã ghi:** bước 1: account không đổi; có validation; form Đăng ký

```json
{
  "started_at": "2026-10-19T19:02:12.667710+00:00",
  "finished_at": "2026-10-19T19:03:24.886981+00:00",
  "submissions": 1,
  "limitations": [
    "Confirmation absent; this case does not exercise MR-R10"
  ],
  "steps": [
    {
      "step": 1,
      "input": {
        "name": "Nguyen Van A",
        "email": "mr.t02r01.tc23@example.com",
        "password": "Abcdef!x",
        "confirmation": "Abcdef!x",
        "expected": "REJECT"
      },
      "ui": {
        "at": "2026-10-19T19:03:24.099966+00:00",
        "feedback": [
          "Mật khẩu quá yếu! Phải dài tối thiểu 8 ký tự, gồm chữ hoa, chữ thường, số và KÝ TỰ ĐẶC BIỆT."
        ],
        "success_signal": false,
        "dialog_seen": false,
        "login": false,
        "registration": true,
        "timed_out": false
      },
      "accounts": [
        {
          "email": "mr.t02r01.tc23@example.com",
          "count_before": 0,
          "count_after": 0,
          "existing_rows_unchanged": true,
          "new_accounts": []
        }
      ],
      "assertion_failures": [],
      "input_verification": [
        {
          "field": "name",
          "readback": "Nguyen Van A"
        },
        {
          "field": "email",
          "readback": "mr.t02r01.tc23@example.com"
        },
        {
          "field": "password",
          "readback": "masked: transport acknowledged; plaintext not exposed"
        }
      ]
    }
  ]
}
```

<a id="log-mr-tc24"></a>
### MR-TC24 / MR-RUN-01

Nguồn: [results.json](results.json), `cases[23].results[0]`; ID `MR-TC24`, run `MR-RUN-01`, status `passed`.

**Actual đã ghi:** bước 1: account 0→1; báo thành công; Login

```json
{
  "started_at": "2026-10-19T19:03:24.888466+00:00",
  "finished_at": "2026-10-19T19:04:37.240196+00:00",
  "submissions": 1,
  "limitations": [
    "Confirmation absent; this case does not exercise MR-R10"
  ],
  "steps": [
    {
      "step": 1,
      "input": {
        "name": "Nguyen Van A",
        "email": "mr.t02r01.tc24@example.com",
        "password": "Abcde12!",
        "confirmation": "Abcde12!",
        "expected": "ACCEPT"
      },
      "ui": {
        "at": "2026-10-19T19:04:36.450332+00:00",
        "feedback": [
          "Đăng ký tài khoản thành công."
        ],
        "success_signal": true,
        "dialog_seen": true,
        "login": true,
        "registration": false,
        "timed_out": false
      },
      "accounts": [
        {
          "email": "mr.t02r01.tc24@example.com",
          "count_before": 0,
          "count_after": 1,
          "existing_rows_unchanged": true,
          "new_accounts": [
            {
              "id": 23,
              "name": "Nguyen Van A",
              "email": "mr.t02r01.tc24@example.com"
            }
          ]
        }
      ],
      "assertion_failures": [],
      "input_verification": [
        {
          "field": "name",
          "readback": "Nguyen Van A"
        },
        {
          "field": "email",
          "readback": "mr.t02r01.tc24@example.com"
        },
        {
          "field": "password",
          "readback": "masked: transport acknowledged; plaintext not exposed"
        }
      ]
    }
  ]
}
```

<a id="log-mr-tc25"></a>
### MR-TC25 / MR-RUN-01

Nguồn: [results.json](results.json), `cases[24].results[0]`; ID `MR-TC25`, run `MR-RUN-01`, status `passed`.

**Actual đã ghi:** bước 1: account không đổi; có validation; form Đăng ký

```json
{
  "started_at": "2026-10-19T19:04:37.241881+00:00",
  "finished_at": "2026-10-19T19:05:50.031923+00:00",
  "submissions": 1,
  "limitations": [
    "Confirmation absent; this case does not exercise MR-R10"
  ],
  "steps": [
    {
      "step": 1,
      "input": {
        "name": "Nguyen Van A",
        "email": "mr.t02r01.tc25@example.com",
        "password": "Abcde12x",
        "confirmation": "Abcde12x",
        "expected": "REJECT"
      },
      "ui": {
        "at": "2026-10-19T19:05:49.249040+00:00",
        "feedback": [
          "Mật khẩu quá yếu! Phải dài tối thiểu 8 ký tự, gồm chữ hoa, chữ thường, số và KÝ TỰ ĐẶC BIỆT."
        ],
        "success_signal": false,
        "dialog_seen": false,
        "login": false,
        "registration": true,
        "timed_out": false
      },
      "accounts": [
        {
          "email": "mr.t02r01.tc25@example.com",
          "count_before": 0,
          "count_after": 0,
          "existing_rows_unchanged": true,
          "new_accounts": []
        }
      ],
      "assertion_failures": [],
      "input_verification": [
        {
          "field": "name",
          "readback": "Nguyen Van A"
        },
        {
          "field": "email",
          "readback": "mr.t02r01.tc25@example.com"
        },
        {
          "field": "password",
          "readback": "masked: transport acknowledged; plaintext not exposed"
        }
      ]
    }
  ]
}
```

<a id="log-mr-tc26"></a>
### MR-TC26 / MR-RUN-02

Nguồn: [results.json](results.json), `cases[25].results[1]`; ID `MR-TC26`, run `MR-RUN-02`, status `passed`.

**Actual đã ghi:** bước 1: tài khoản 0→1; báo thành công; Đăng nhập

```json
{
  "started_at": "2026-10-19T19:44:50.823093+00:00",
  "finished_at": "2026-10-19T19:45:35.351307+00:00",
  "submissions": 1,
  "form": {
    "complete": true,
    "fields": {
      "name": {
        "bounds": "[48,316][672,398]",
        "editable": true,
        "class": "android.widget.EditText"
      },
      "email": {
        "bounds": "[48,481][672,563]",
        "editable": true,
        "class": "android.widget.EditText"
      },
      "password": {
        "bounds": "[48,646][672,728]",
        "editable": true,
        "class": "android.widget.EditText"
      }
    }
  },
  "limitations": [
    "Confirmation absent; this case does not exercise MR-R10"
  ],
  "steps": [
    {
      "step": 1,
      "input": {
        "name": "Nguyen Van A",
        "email": "mr.t02r01.tc26@example.com",
        "password": "Abcde1!!",
        "confirmation": "Abcde1!!",
        "expected": "ACCEPT"
      },
      "ui": {
        "at": "2026-10-19T19:45:34.740682+00:00",
        "feedback": [
          "Đăng ký tài khoản thành công."
        ],
        "success_signal": true,
        "dialog_seen": true,
        "login": true,
        "registration": false,
        "timed_out": false
      },
      "accounts": [
        {
          "email": "mr.t02r01.tc26@example.com",
          "count_before": 0,
          "count_after": 1,
          "existing_rows_unchanged": true,
          "new_accounts": [
            {
              "id": 26,
              "name": "Nguyen Van A",
              "email": "mr.t02r01.tc26@example.com"
            }
          ]
        }
      ],
      "assertion_failures": [],
      "input_verification": [
        {
          "field": "name",
          "readback": "Nguyen Van A"
        },
        {
          "field": "email",
          "readback": "mr.t02r01.tc26@example.com"
        },
        {
          "field": "password",
          "readback": "masked: transport acknowledged; plaintext not exposed"
        }
      ]
    }
  ]
}
```

<a id="log-mr-tc27"></a>
### MR-TC27 / MR-RUN-01

Nguồn: [results.json](results.json), `cases[26].results[0]`; ID `MR-TC27`, run `MR-RUN-01`, status `passed`.

**Actual đã ghi:** bước 1: account 0→1; báo thành công; Login

```json
{
  "started_at": "2026-10-19T19:05:57.313611+00:00",
  "finished_at": "2026-10-19T19:07:09.910221+00:00",
  "submissions": 1,
  "limitations": [
    "Confirmation absent; this case does not exercise MR-R10"
  ],
  "steps": [
    {
      "step": 1,
      "input": {
        "name": "Nguyen Van A",
        "email": "mr.t02r01.tc27@example.com",
        "password": "Abcde1@x",
        "confirmation": "Abcde1@x",
        "expected": "ACCEPT"
      },
      "ui": {
        "at": "2026-10-19T19:07:09.125483+00:00",
        "feedback": [
          "Đăng ký tài khoản thành công."
        ],
        "success_signal": true,
        "dialog_seen": true,
        "login": true,
        "registration": false,
        "timed_out": false
      },
      "accounts": [
        {
          "email": "mr.t02r01.tc27@example.com",
          "count_before": 0,
          "count_after": 1,
          "existing_rows_unchanged": true,
          "new_accounts": [
            {
              "id": 24,
              "name": "Nguyen Van A",
              "email": "mr.t02r01.tc27@example.com"
            }
          ]
        }
      ],
      "assertion_failures": [],
      "input_verification": [
        {
          "field": "name",
          "readback": "Nguyen Van A"
        },
        {
          "field": "email",
          "readback": "mr.t02r01.tc27@example.com"
        },
        {
          "field": "password",
          "readback": "masked: transport acknowledged; plaintext not exposed"
        }
      ]
    }
  ]
}
```

<a id="log-mr-tc28"></a>
### MR-TC28 / MR-RUN-01

Nguồn: [results.json](results.json), `cases[27].results[0]`; ID `MR-TC28`, run `MR-RUN-01`, status `passed`.

**Actual đã ghi:** bước 1: account 0→1; báo thành công; Login

```json
{
  "started_at": "2026-10-19T19:07:09.912130+00:00",
  "finished_at": "2026-10-19T19:08:22.579198+00:00",
  "submissions": 1,
  "limitations": [
    "Confirmation absent; this case does not exercise MR-R10"
  ],
  "steps": [
    {
      "step": 1,
      "input": {
        "name": "Nguyen Van A",
        "email": "mr.t02r01.tc28@example.com",
        "password": "Abcde1$x",
        "confirmation": "Abcde1$x",
        "expected": "ACCEPT"
      },
      "ui": {
        "at": "2026-10-19T19:08:21.771697+00:00",
        "feedback": [
          "Đăng ký tài khoản thành công."
        ],
        "success_signal": true,
        "dialog_seen": true,
        "login": true,
        "registration": false,
        "timed_out": false
      },
      "accounts": [
        {
          "email": "mr.t02r01.tc28@example.com",
          "count_before": 0,
          "count_after": 1,
          "existing_rows_unchanged": true,
          "new_accounts": [
            {
              "id": 25,
              "name": "Nguyen Van A",
              "email": "mr.t02r01.tc28@example.com"
            }
          ]
        }
      ],
      "assertion_failures": [],
      "input_verification": [
        {
          "field": "name",
          "readback": "Nguyen Van A"
        },
        {
          "field": "email",
          "readback": "mr.t02r01.tc28@example.com"
        },
        {
          "field": "password",
          "readback": "masked: transport acknowledged; plaintext not exposed"
        }
      ]
    }
  ]
}
```

<a id="log-mr-tc29"></a>
### MR-TC29 / MR-RUN-03

Nguồn: [results.json](results.json), `cases[28].results[1]`; ID `MR-TC29`, run `MR-RUN-03`, status `passed`.

**Actual đã ghi:** bước 1: tài khoản 0→1; báo thành công; Đăng nhập

```json
{
  "started_at": "2026-10-19T19:45:48.678924+00:00",
  "finished_at": "2026-10-19T19:46:37.099793+00:00",
  "submissions": 1,
  "form": {
    "complete": true,
    "fields": {
      "name": {
        "bounds": "[48,316][672,398]",
        "editable": true,
        "class": "android.widget.EditText"
      },
      "email": {
        "bounds": "[48,481][672,563]",
        "editable": true,
        "class": "android.widget.EditText"
      },
      "password": {
        "bounds": "[48,646][672,728]",
        "editable": true,
        "class": "android.widget.EditText"
      }
    }
  },
  "limitations": [
    "Confirmation absent; this case does not exercise MR-R10"
  ],
  "steps": [
    {
      "step": 1,
      "input": {
        "name": "Nguyen Van A",
        "email": "mr.t02r01.tc29@example.com",
        "password": "Abcde1%x",
        "confirmation": "Abcde1%x",
        "expected": "ACCEPT"
      },
      "ui": {
        "at": "2026-10-19T19:46:36.477887+00:00",
        "feedback": [
          "Đăng ký tài khoản thành công."
        ],
        "success_signal": true,
        "dialog_seen": true,
        "login": true,
        "registration": false,
        "timed_out": false
      },
      "accounts": [
        {
          "email": "mr.t02r01.tc29@example.com",
          "count_before": 0,
          "count_after": 1,
          "existing_rows_unchanged": true,
          "new_accounts": [
            {
              "id": 27,
              "name": "Nguyen Van A",
              "email": "mr.t02r01.tc29@example.com"
            }
          ]
        }
      ],
      "assertion_failures": [],
      "input_verification": [
        {
          "field": "name",
          "readback": "Nguyen Van A"
        },
        {
          "field": "email",
          "readback": "mr.t02r01.tc29@example.com"
        },
        {
          "field": "password",
          "readback": "masked: transport acknowledged; plaintext not exposed"
        }
      ]
    }
  ]
}
```

<a id="log-mr-tc30"></a>
### MR-TC30 / MR-RUN-03

Nguồn: [results.json](results.json), `cases[29].results[1]`; ID `MR-TC30`, run `MR-RUN-03`, status `passed`.

**Actual đã ghi:** bước 1: tài khoản 0→1; báo thành công; Đăng nhập

```json
{
  "started_at": "2026-10-19T19:46:37.102246+00:00",
  "finished_at": "2026-10-19T19:47:24.049711+00:00",
  "submissions": 1,
  "form": {
    "complete": true,
    "fields": {
      "name": {
        "bounds": "[48,316][672,398]",
        "editable": true,
        "class": "android.widget.EditText"
      },
      "email": {
        "bounds": "[48,481][672,563]",
        "editable": true,
        "class": "android.widget.EditText"
      },
      "password": {
        "bounds": "[48,646][672,728]",
        "editable": true,
        "class": "android.widget.EditText"
      }
    }
  },
  "limitations": [
    "Confirmation absent; this case does not exercise MR-R10"
  ],
  "steps": [
    {
      "step": 1,
      "input": {
        "name": "Nguyen Van A",
        "email": "mr.t02r01.tc30@example.com",
        "password": "Abcde1*x",
        "confirmation": "Abcde1*x",
        "expected": "ACCEPT"
      },
      "ui": {
        "at": "2026-10-19T19:47:23.429015+00:00",
        "feedback": [
          "Đăng ký tài khoản thành công."
        ],
        "success_signal": true,
        "dialog_seen": true,
        "login": true,
        "registration": false,
        "timed_out": false
      },
      "accounts": [
        {
          "email": "mr.t02r01.tc30@example.com",
          "count_before": 0,
          "count_after": 1,
          "existing_rows_unchanged": true,
          "new_accounts": [
            {
              "id": 28,
              "name": "Nguyen Van A",
              "email": "mr.t02r01.tc30@example.com"
            }
          ]
        }
      ],
      "assertion_failures": [],
      "input_verification": [
        {
          "field": "name",
          "readback": "Nguyen Van A"
        },
        {
          "field": "email",
          "readback": "mr.t02r01.tc30@example.com"
        },
        {
          "field": "password",
          "readback": "masked: transport acknowledged; plaintext not exposed"
        }
      ]
    }
  ]
}
```

<a id="log-mr-tc31"></a>
### MR-TC31 / MR-RUN-03

Nguồn: [results.json](results.json), `cases[30].results[1]`; ID `MR-TC31`, run `MR-RUN-03`, status `passed`.

**Actual đã ghi:** bước 1: tài khoản 0→1; báo thành công; Đăng nhập

```json
{
  "started_at": "2026-10-19T19:47:24.051579+00:00",
  "finished_at": "2026-10-19T19:48:11.125182+00:00",
  "submissions": 1,
  "form": {
    "complete": true,
    "fields": {
      "name": {
        "bounds": "[48,316][672,398]",
        "editable": true,
        "class": "android.widget.EditText"
      },
      "email": {
        "bounds": "[48,481][672,563]",
        "editable": true,
        "class": "android.widget.EditText"
      },
      "password": {
        "bounds": "[48,646][672,728]",
        "editable": true,
        "class": "android.widget.EditText"
      }
    }
  },
  "limitations": [
    "Confirmation absent; this case does not exercise MR-R10"
  ],
  "steps": [
    {
      "step": 1,
      "input": {
        "name": "Nguyen Van A",
        "email": "mr.t02r01.tc31@example.com",
        "password": "Abcde1?x",
        "confirmation": "Abcde1?x",
        "expected": "ACCEPT"
      },
      "ui": {
        "at": "2026-10-19T19:48:10.515231+00:00",
        "feedback": [
          "Đăng ký tài khoản thành công."
        ],
        "success_signal": true,
        "dialog_seen": true,
        "login": true,
        "registration": false,
        "timed_out": false
      },
      "accounts": [
        {
          "email": "mr.t02r01.tc31@example.com",
          "count_before": 0,
          "count_after": 1,
          "existing_rows_unchanged": true,
          "new_accounts": [
            {
              "id": 29,
              "name": "Nguyen Van A",
              "email": "mr.t02r01.tc31@example.com"
            }
          ]
        }
      ],
      "assertion_failures": [],
      "input_verification": [
        {
          "field": "name",
          "readback": "Nguyen Van A"
        },
        {
          "field": "email",
          "readback": "mr.t02r01.tc31@example.com"
        },
        {
          "field": "password",
          "readback": "masked: transport acknowledged; plaintext not exposed"
        }
      ]
    }
  ]
}
```

<a id="log-mr-tc32"></a>
### MR-TC32 / MR-RUN-03

Nguồn: [results.json](results.json), `cases[31].results[1]`; ID `MR-TC32`, run `MR-RUN-03`, status `passed`.

**Actual đã ghi:** bước 1: tài khoản 0→1; báo thành công; Đăng nhập

```json
{
  "started_at": "2026-10-19T19:48:11.129017+00:00",
  "finished_at": "2026-10-19T19:48:57.898513+00:00",
  "submissions": 1,
  "form": {
    "complete": true,
    "fields": {
      "name": {
        "bounds": "[48,316][672,398]",
        "editable": true,
        "class": "android.widget.EditText"
      },
      "email": {
        "bounds": "[48,481][672,563]",
        "editable": true,
        "class": "android.widget.EditText"
      },
      "password": {
        "bounds": "[48,646][672,728]",
        "editable": true,
        "class": "android.widget.EditText"
      }
    }
  },
  "limitations": [
    "Confirmation absent; this case does not exercise MR-R10"
  ],
  "steps": [
    {
      "step": 1,
      "input": {
        "name": "Nguyen Van A",
        "email": "mr.t02r01.tc32@example.com",
        "password": "Abcde1&x",
        "confirmation": "Abcde1&x",
        "expected": "ACCEPT"
      },
      "ui": {
        "at": "2026-10-19T19:48:57.290786+00:00",
        "feedback": [
          "Đăng ký tài khoản thành công."
        ],
        "success_signal": true,
        "dialog_seen": true,
        "login": true,
        "registration": false,
        "timed_out": false
      },
      "accounts": [
        {
          "email": "mr.t02r01.tc32@example.com",
          "count_before": 0,
          "count_after": 1,
          "existing_rows_unchanged": true,
          "new_accounts": [
            {
              "id": 30,
              "name": "Nguyen Van A",
              "email": "mr.t02r01.tc32@example.com"
            }
          ]
        }
      ],
      "assertion_failures": [],
      "input_verification": [
        {
          "field": "name",
          "readback": "Nguyen Van A"
        },
        {
          "field": "email",
          "readback": "mr.t02r01.tc32@example.com"
        },
        {
          "field": "password",
          "readback": "masked: transport acknowledged; plaintext not exposed"
        }
      ]
    }
  ]
}
```

<a id="log-mr-tc33"></a>
### MR-TC33 / MR-RUN-03

Nguồn: [results.json](results.json), `cases[32].results[1]`; ID `MR-TC33`, run `MR-RUN-03`, status `failed`.

**Actual đã ghi:** Full-form inspection: Required native Confirmation field is absent after full-form inspection

```json
{
  "started_at": "2026-10-19T19:48:57.903059+00:00",
  "finished_at": "2026-10-19T19:49:09.530600+00:00",
  "submissions": 0,
  "form": {
    "complete": true,
    "fields": {
      "name": {
        "bounds": "[48,316][672,398]",
        "editable": true,
        "class": "android.widget.EditText"
      },
      "email": {
        "bounds": "[48,481][672,563]",
        "editable": true,
        "class": "android.widget.EditText"
      },
      "password": {
        "bounds": "[48,646][672,728]",
        "editable": true,
        "class": "android.widget.EditText"
      }
    }
  },
  "reason": "Required native Confirmation field is absent after full-form inspection",
  "assertions": {
    "expected": "independent editable Confirmation field",
    "problems": [
      "Required native Confirmation field is absent after full-form inspection"
    ],
    "submissions": 0
  },
  "limitations": []
}
```

<a id="log-mr-tc34"></a>
### MR-TC34 / MR-RUN-03

Nguồn: [results.json](results.json), `cases[33].results[1]`; ID `MR-TC34`, run `MR-RUN-03`, status `blocked`.

**Actual đã ghi:** C-guard: Confirmation missing; equality case cannot be performed natively

```json
{
  "started_at": "2026-10-19T19:49:09.618530+00:00",
  "finished_at": "2026-10-19T19:49:17.926798+00:00",
  "submissions": 0,
  "form": {
    "complete": true,
    "fields": {
      "name": {
        "bounds": "[48,316][672,398]",
        "editable": true,
        "class": "android.widget.EditText"
      },
      "email": {
        "bounds": "[48,481][672,563]",
        "editable": true,
        "class": "android.widget.EditText"
      },
      "password": {
        "bounds": "[48,646][672,728]",
        "editable": true,
        "class": "android.widget.EditText"
      }
    }
  },
  "reason": "C-guard: Confirmation missing; equality case cannot be performed natively",
  "limitations": []
}
```

<a id="log-mr-tc35"></a>
### MR-TC35 / MR-RUN-03

Nguồn: [results.json](results.json), `cases[34].results[1]`; ID `MR-TC35`, run `MR-RUN-03`, status `blocked`.

**Actual đã ghi:** C-guard: Confirmation missing; equality case cannot be performed natively

```json
{
  "started_at": "2026-10-19T19:49:17.928704+00:00",
  "finished_at": "2026-10-19T19:49:26.262397+00:00",
  "submissions": 0,
  "form": {
    "complete": true,
    "fields": {
      "name": {
        "bounds": "[48,316][672,398]",
        "editable": true,
        "class": "android.widget.EditText"
      },
      "email": {
        "bounds": "[48,481][672,563]",
        "editable": true,
        "class": "android.widget.EditText"
      },
      "password": {
        "bounds": "[48,646][672,728]",
        "editable": true,
        "class": "android.widget.EditText"
      }
    }
  },
  "reason": "C-guard: Confirmation missing; equality case cannot be performed natively",
  "limitations": []
}
```

<a id="log-mr-tc36"></a>
### MR-TC36 / MR-RUN-04

Nguồn: [results.json](results.json), `cases[35].results[1]`; ID `MR-TC36`, run `MR-RUN-04`, status `blocked`.

**Actual đã ghi:** C-guard: Confirmation missing; equality case cannot be performed natively

```json
{
  "started_at": "2026-10-19T19:50:21.357984+00:00",
  "finished_at": "2026-10-19T19:50:40.291364+00:00",
  "submissions": 0,
  "form": {
    "complete": true,
    "fields": {
      "name": {
        "bounds": "[48,316][672,398]",
        "editable": true,
        "class": "android.widget.EditText"
      },
      "email": {
        "bounds": "[48,481][672,563]",
        "editable": true,
        "class": "android.widget.EditText"
      },
      "password": {
        "bounds": "[48,646][672,728]",
        "editable": true,
        "class": "android.widget.EditText"
      }
    }
  },
  "reason": "C-guard: Confirmation missing; equality case cannot be performed natively",
  "limitations": []
}
```

<a id="log-mr-tc37"></a>
### MR-TC37 / MR-RUN-04

Nguồn: [results.json](results.json), `cases[36].results[1]`; ID `MR-TC37`, run `MR-RUN-04`, status `blocked`.

**Actual đã ghi:** C-guard: Confirmation missing; equality case cannot be performed natively

```json
{
  "started_at": "2026-10-19T19:50:40.293475+00:00",
  "finished_at": "2026-10-19T19:50:58.427890+00:00",
  "submissions": 0,
  "form": {
    "complete": true,
    "fields": {
      "name": {
        "bounds": "[48,316][672,398]",
        "editable": true,
        "class": "android.widget.EditText"
      },
      "email": {
        "bounds": "[48,481][672,563]",
        "editable": true,
        "class": "android.widget.EditText"
      },
      "password": {
        "bounds": "[48,646][672,728]",
        "editable": true,
        "class": "android.widget.EditText"
      }
    }
  },
  "reason": "C-guard: Confirmation missing; equality case cannot be performed natively",
  "limitations": []
}
```

<a id="log-mr-tc38"></a>
### MR-TC38 / MR-RUN-06

Nguồn: [results.json](results.json), `cases[37].results[3]`; ID `MR-TC38`, run `MR-RUN-06`, status `passed`.

**Actual đã ghi:** bước 1: tài khoản không đổi; có phản hồi từ chối; form Đăng ký; bước 2: tài khoản 0→1; báo thành công; Đăng nhập

```json
{
  "started_at": "2026-10-19T19:56:16.523726+00:00",
  "finished_at": "2026-10-19T19:57:40.032736+00:00",
  "submissions": 2,
  "form": {
    "complete": true,
    "fields": {
      "name": {
        "bounds": "[48,472][672,554]",
        "editable": true,
        "class": "android.widget.EditText"
      },
      "email": {
        "bounds": "[48,637][672,719]",
        "editable": true,
        "class": "android.widget.EditText"
      },
      "password": {
        "bounds": "[48,802][672,884]",
        "editable": true,
        "class": "android.widget.EditText"
      }
    }
  },
  "limitations": [
    "Confirmation absent; this case does not exercise MR-R10"
  ],
  "steps": [
    {
      "step": 1,
      "input": {
        "name": "Nguyen Van A",
        "email": "mr.t02r01.tc38@example.com",
        "password": "Abcde1!",
        "confirmation": "Abcde1!",
        "expected": "REJECT"
      },
      "ui": {
        "at": "2026-10-19T19:57:15.646207+00:00",
        "feedback": [
          "Mật khẩu quá yếu! Phải dài tối thiểu 8 ký tự, gồm chữ hoa, chữ thường, số và KÝ TỰ ĐẶC BIỆT."
        ],
        "success_signal": false,
        "dialog_seen": false,
        "login": false,
        "registration": true,
        "timed_out": false
      },
      "accounts": [
        {
          "email": "mr.t02r01.tc38@example.com",
          "count_before": 0,
          "count_after": 0,
          "existing_rows_unchanged": true,
          "new_accounts": []
        }
      ],
      "assertion_failures": [],
      "input_verification": [
        {
          "field": "name",
          "readback": "Nguyen Van A"
        },
        {
          "field": "email",
          "readback": "mr.t02r01.tc38@example.com"
        },
        {
          "field": "password",
          "readback": "masked: transport acknowledged; plaintext not exposed"
        }
      ]
    },
    {
      "step": 2,
      "input": {
        "name": "Nguyen Van A",
        "email": "mr.t02r01.tc38@example.com",
        "password": "Abcde1!x",
        "confirmation": "Abcde1!x",
        "expected": "ACCEPT"
      },
      "ui": {
        "at": "2026-10-19T19:57:39.423152+00:00",
        "feedback": [
          "Đăng ký tài khoản thành công."
        ],
        "success_signal": true,
        "dialog_seen": true,
        "login": true,
        "registration": false,
        "timed_out": false
      },
      "accounts": [
        {
          "email": "mr.t02r01.tc38@example.com",
          "count_before": 0,
          "count_after": 1,
          "existing_rows_unchanged": true,
          "new_accounts": [
            {
              "id": 31,
              "name": "Nguyen Van A",
              "email": "mr.t02r01.tc38@example.com"
            }
          ]
        }
      ],
      "assertion_failures": [],
      "input_verification": [
        {
          "field": "password",
          "readback": "masked: transport acknowledged; plaintext not exposed"
        }
      ]
    }
  ]
}
```

<a id="log-mr-tc39"></a>
### MR-TC39 / MR-RUN-06

Nguồn: [results.json](results.json), `cases[38].results[2]`; ID `MR-TC39`, run `MR-RUN-06`, status `passed`.

**Actual đã ghi:** bước 1: tài khoản không đổi; có phản hồi từ chối; form Đăng ký

```json
{
  "started_at": "2026-10-19T19:57:40.037239+00:00",
  "finished_at": "2026-10-19T19:58:35.155687+00:00",
  "submissions": 1,
  "form": {
    "complete": true,
    "fields": {
      "name": {
        "bounds": "[48,316][672,398]",
        "editable": true,
        "class": "android.widget.EditText"
      },
      "email": {
        "bounds": "[48,481][672,563]",
        "editable": true,
        "class": "android.widget.EditText"
      },
      "password": {
        "bounds": "[48,646][672,728]",
        "editable": true,
        "class": "android.widget.EditText"
      }
    }
  },
  "limitations": [
    "Confirmation absent; this case does not exercise MR-R10"
  ],
  "steps": [
    {
      "step": 1,
      "input": {
        "name": "Nguyen Van A",
        "email": "test@eshop.com",
        "password": "abcde1!x",
        "confirmation": "abcde1!x",
        "expected": "REJECT"
      },
      "ui": {
        "at": "2026-10-19T19:58:34.546476+00:00",
        "feedback": [
          "Mật khẩu quá yếu! Phải dài tối thiểu 8 ký tự, gồm chữ hoa, chữ thường, số và KÝ TỰ ĐẶC BIỆT."
        ],
        "success_signal": false,
        "dialog_seen": false,
        "login": false,
        "registration": true,
        "timed_out": false
      },
      "accounts": [
        {
          "email": "test@eshop.com",
          "count_before": 2,
          "count_after": 2,
          "existing_rows_unchanged": true,
          "new_accounts": []
        }
      ],
      "assertion_failures": [],
      "input_verification": [
        {
          "field": "name",
          "readback": "Nguyen Van A"
        },
        {
          "field": "email",
          "readback": "test@eshop.com"
        },
        {
          "field": "password",
          "readback": "masked: transport acknowledged; plaintext not exposed"
        }
      ]
    }
  ]
}
```

<a id="log-mr-tc40"></a>
### MR-TC40 / MR-RUN-07

Nguồn: [results.json](results.json), `cases[39].results[2]`; ID `MR-TC40`, run `MR-RUN-07`, status `passed`.

**Actual đã ghi:** bước 1: tài khoản 0→1; báo thành công; Đăng nhập

```json
{
  "started_at": "2026-10-19T19:58:53.434642+00:00",
  "finished_at": "2026-10-19T19:59:52.879986+00:00",
  "submissions": 1,
  "form": {
    "complete": true,
    "fields": {
      "name": {
        "bounds": "[48,472][672,554]",
        "editable": true,
        "class": "android.widget.EditText"
      },
      "email": {
        "bounds": "[48,637][672,719]",
        "editable": true,
        "class": "android.widget.EditText"
      },
      "password": {
        "bounds": "[48,802][672,884]",
        "editable": true,
        "class": "android.widget.EditText"
      }
    }
  },
  "limitations": [
    "Confirmation absent; this case does not exercise MR-R10"
  ],
  "steps": [
    {
      "step": 1,
      "input": {
        "name": "Nguyen Van A",
        "email": "mr.t02r01.tc40@example.com",
        "password": "Ab1!Ab1!Ab1!Ab1!Ab1!Ab1!Ab1!Ab1!Ab1!Ab1!Ab1!Ab1!Ab1!Ab1!Ab1!Ab1!",
        "confirmation": "Ab1!Ab1!Ab1!Ab1!Ab1!Ab1!Ab1!Ab1!Ab1!Ab1!Ab1!Ab1!Ab1!Ab1!Ab1!Ab1!",
        "expected": "ACCEPT"
      },
      "ui": {
        "at": "2026-10-19T19:59:52.272378+00:00",
        "feedback": [
          "Đăng ký tài khoản thành công."
        ],
        "success_signal": true,
        "dialog_seen": true,
        "login": true,
        "registration": false,
        "timed_out": false
      },
      "accounts": [
        {
          "email": "mr.t02r01.tc40@example.com",
          "count_before": 0,
          "count_after": 1,
          "existing_rows_unchanged": true,
          "new_accounts": [
            {
              "id": 32,
              "name": "Nguyen Van A",
              "email": "mr.t02r01.tc40@example.com"
            }
          ]
        }
      ],
      "assertion_failures": [],
      "input_verification": [
        {
          "field": "name",
          "readback": "Nguyen Van A"
        },
        {
          "field": "email",
          "readback": "mr.t02r01.tc40@example.com"
        },
        {
          "field": "password",
          "readback": "masked: transport acknowledged; plaintext not exposed"
        }
      ]
    }
  ]
}
```

<a id="log-mr-tc41"></a>
### MR-TC41 / MR-RUN-07

Nguồn: [results.json](results.json), `cases[40].results[1]`; ID `MR-TC41`, run `MR-RUN-07`, status `failed`.

**Actual đã ghi:** bước 1: tài khoản 0→1; báo thành công; Đăng nhập

```json
{
  "started_at": "2026-10-19T19:59:52.882914+00:00",
  "finished_at": "2026-10-19T20:00:49.396089+00:00",
  "submissions": 1,
  "form": {
    "complete": true,
    "fields": {
      "name": {
        "bounds": "[48,316][672,398]",
        "editable": true,
        "class": "android.widget.EditText"
      },
      "email": {
        "bounds": "[48,481][672,563]",
        "editable": true,
        "class": "android.widget.EditText"
      },
      "password": {
        "bounds": "[48,646][672,728]",
        "editable": true,
        "class": "android.widget.EditText"
      }
    }
  },
  "reason": "Invalid/duplicate submission created or changed watched account data; Invalid submission reported registration success; Invalid submission reached Login as if registration succeeded",
  "limitations": [
    "Confirmation absent; this case does not exercise MR-R10"
  ],
  "steps": [
    {
      "step": 1,
      "input": {
        "name": " ",
        "email": "mr.t02r01.tc41@example.com",
        "password": "Abcde1!x",
        "confirmation": "Abcde1!x",
        "expected": "REJECT"
      },
      "ui": {
        "at": "2026-10-19T20:00:48.778354+00:00",
        "feedback": [
          "Đăng ký tài khoản thành công."
        ],
        "success_signal": true,
        "dialog_seen": true,
        "login": true,
        "registration": false,
        "timed_out": false
      },
      "accounts": [
        {
          "email": "mr.t02r01.tc41@example.com",
          "count_before": 0,
          "count_after": 1,
          "existing_rows_unchanged": true,
          "new_accounts": [
            {
              "id": 33,
              "name": " ",
              "email": "mr.t02r01.tc41@example.com"
            }
          ]
        }
      ],
      "assertion_failures": [
        "Invalid/duplicate submission created or changed watched account data",
        "Invalid submission reported registration success",
        "Invalid submission reached Login as if registration succeeded"
      ],
      "input_verification": [
        {
          "field": "name",
          "readback": ""
        },
        {
          "field": "email",
          "readback": "mr.t02r01.tc41@example.com"
        },
        {
          "field": "password",
          "readback": "masked: transport acknowledged; plaintext not exposed"
        }
      ]
    }
  ]
}
```

<a id="log-mr-tc42"></a>
### MR-TC42 / MR-RUN-07

Nguồn: [results.json](results.json), `cases[41].results[1]`; ID `MR-TC42`, run `MR-RUN-07`, status `passed`.

**Actual đã ghi:** bước 1: tài khoản 0→1; báo thành công; Đăng nhập

```json
{
  "started_at": "2026-10-19T20:00:49.510716+00:00",
  "finished_at": "2026-10-19T20:01:46.478730+00:00",
  "submissions": 1,
  "form": {
    "complete": true,
    "fields": {
      "name": {
        "bounds": "[48,316][672,398]",
        "editable": true,
        "class": "android.widget.EditText"
      },
      "email": {
        "bounds": "[48,481][672,563]",
        "editable": true,
        "class": "android.widget.EditText"
      },
      "password": {
        "bounds": "[48,646][672,728]",
        "editable": true,
        "class": "android.widget.EditText"
      }
    }
  },
  "limitations": [
    "Confirmation absent; this case does not exercise MR-R10"
  ],
  "steps": [
    {
      "step": 1,
      "input": {
        "name": "Nguyen Van A",
        "email": "TEST@eshop.com",
        "password": "Abcde1!x",
        "confirmation": "Abcde1!x",
        "expected": "ACCEPT"
      },
      "ui": {
        "at": "2026-10-19T20:01:45.870306+00:00",
        "feedback": [
          "Đăng ký tài khoản thành công."
        ],
        "success_signal": true,
        "dialog_seen": true,
        "login": true,
        "registration": false,
        "timed_out": false
      },
      "accounts": [
        {
          "email": "TEST@eshop.com",
          "count_before": 0,
          "count_after": 1,
          "existing_rows_unchanged": true,
          "new_accounts": [
            {
              "id": 34,
              "name": "Nguyen Van A",
              "email": "TEST@eshop.com"
            }
          ]
        },
        {
          "email": "test@eshop.com",
          "count_before": 2,
          "count_after": 2,
          "existing_rows_unchanged": true,
          "new_accounts": []
        }
      ],
      "assertion_failures": [],
      "input_verification": [
        {
          "field": "name",
          "readback": "Nguyen Van A"
        },
        {
          "field": "email",
          "readback": "TEST@eshop.com"
        },
        {
          "field": "password",
          "readback": "masked: transport acknowledged; plaintext not exposed"
        }
      ]
    }
  ]
}
```

<a id="log-mr-tc43"></a>
### MR-TC43 / MR-RUN-07

Nguồn: [results.json](results.json), `cases[42].results[1]`; ID `MR-TC43`, run `MR-RUN-07`, status `failed`.

**Actual đã ghi:** bước 1: tài khoản 0→1; báo thành công; Đăng nhập

```json
{
  "started_at": "2026-10-19T20:01:46.481237+00:00",
  "finished_at": "2026-10-19T20:02:42.620975+00:00",
  "submissions": 1,
  "form": {
    "complete": true,
    "fields": {
      "name": {
        "bounds": "[48,316][672,398]",
        "editable": true,
        "class": "android.widget.EditText"
      },
      "email": {
        "bounds": "[48,481][672,563]",
        "editable": true,
        "class": "android.widget.EditText"
      },
      "password": {
        "bounds": "[48,646][672,728]",
        "editable": true,
        "class": "android.widget.EditText"
      }
    }
  },
  "reason": "Expected exactly one new 'mr.t02r01.tc43@example.com' account, observed 0; Unexpected account change at watched identity ' mr.t02r01.tc43@example.com '",
  "limitations": [
    "Confirmation absent; this case does not exercise MR-R10"
  ],
  "steps": [
    {
      "step": 1,
      "input": {
        "name": "Nguyen Van A",
        "email": " mr.t02r01.tc43@example.com ",
        "password": "Abcde1!x",
        "confirmation": "Abcde1!x",
        "expected": "ACCEPT"
      },
      "ui": {
        "at": "2026-10-19T20:02:42.012463+00:00",
        "feedback": [
          "Đăng ký tài khoản thành công."
        ],
        "success_signal": true,
        "dialog_seen": true,
        "login": true,
        "registration": false,
        "timed_out": false
      },
      "accounts": [
        {
          "email": " mr.t02r01.tc43@example.com ",
          "count_before": 0,
          "count_after": 1,
          "existing_rows_unchanged": true,
          "new_accounts": [
            {
              "id": 35,
              "name": "Nguyen Van A",
              "email": " mr.t02r01.tc43@example.com "
            }
          ]
        },
        {
          "email": "mr.t02r01.tc43@example.com",
          "count_before": 0,
          "count_after": 0,
          "existing_rows_unchanged": true,
          "new_accounts": []
        }
      ],
      "assertion_failures": [
        "Expected exactly one new 'mr.t02r01.tc43@example.com' account, observed 0",
        "Unexpected account change at watched identity ' mr.t02r01.tc43@example.com '"
      ],
      "input_verification": [
        {
          "field": "name",
          "readback": "Nguyen Van A"
        },
        {
          "field": "email",
          "readback": " mr.t02r01.tc43@example.com "
        },
        {
          "field": "password",
          "readback": "masked: transport acknowledged; plaintext not exposed"
        }
      ]
    }
  ]
}
```

<a id="log-mr-tc44"></a>
### MR-TC44 / MR-RUN-07

Nguồn: [results.json](results.json), `cases[43].results[1]`; ID `MR-TC44`, run `MR-RUN-07`, status `passed`.

**Actual đã ghi:** bước 1: tài khoản 0→1; báo thành công; Đăng nhập

```json
{
  "started_at": "2026-10-19T20:02:42.677349+00:00",
  "finished_at": "2026-10-19T20:03:38.497458+00:00",
  "submissions": 1,
  "form": {
    "complete": true,
    "fields": {
      "name": {
        "bounds": "[48,316][672,398]",
        "editable": true,
        "class": "android.widget.EditText"
      },
      "email": {
        "bounds": "[48,481][672,563]",
        "editable": true,
        "class": "android.widget.EditText"
      },
      "password": {
        "bounds": "[48,646][672,728]",
        "editable": true,
        "class": "android.widget.EditText"
      }
    }
  },
  "limitations": [
    "Confirmation absent; this case does not exercise MR-R10"
  ],
  "steps": [
    {
      "step": 1,
      "input": {
        "name": "Nguyen Van A",
        "email": "mr.t02r01.tc44@example.com",
        "password": "Abcde1#x",
        "confirmation": "Abcde1#x",
        "expected": "ACCEPT"
      },
      "ui": {
        "at": "2026-10-19T20:03:37.867898+00:00",
        "feedback": [
          "Đăng ký tài khoản thành công."
        ],
        "success_signal": true,
        "dialog_seen": true,
        "login": true,
        "registration": false,
        "timed_out": false
      },
      "accounts": [
        {
          "email": "mr.t02r01.tc44@example.com",
          "count_before": 0,
          "count_after": 1,
          "existing_rows_unchanged": true,
          "new_accounts": [
            {
              "id": 36,
              "name": "Nguyen Van A",
              "email": "mr.t02r01.tc44@example.com"
            }
          ]
        }
      ],
      "assertion_failures": [],
      "input_verification": [
        {
          "field": "name",
          "readback": "Nguyen Van A"
        },
        {
          "field": "email",
          "readback": "mr.t02r01.tc44@example.com"
        },
        {
          "field": "password",
          "readback": "masked: transport acknowledged; plaintext not exposed"
        }
      ]
    }
  ]
}
```

<a id="log-mr-tc45"></a>
### MR-TC45 / MR-RUN-07

Nguồn: [results.json](results.json), `cases[44].results[1]`; ID `MR-TC45`, run `MR-RUN-07`, status `failed`.

**Actual đã ghi:** bước 1: tài khoản 0→1; báo thành công; Đăng nhập

```json
{
  "started_at": "2026-10-19T20:03:38.500340+00:00",
  "finished_at": "2026-10-19T20:04:36.137926+00:00",
  "submissions": 1,
  "form": {
    "complete": true,
    "fields": {
      "name": {
        "bounds": "[48,316][672,398]",
        "editable": true,
        "class": "android.widget.EditText"
      },
      "email": {
        "bounds": "[48,481][672,563]",
        "editable": true,
        "class": "android.widget.EditText"
      },
      "password": {
        "bounds": "[48,646][672,728]",
        "editable": true,
        "class": "android.widget.EditText"
      }
    }
  },
  "reason": "Invalid/duplicate submission created or changed watched account data; Invalid submission reported registration success; Invalid submission reached Login as if registration succeeded",
  "limitations": [
    "Confirmation absent; this case does not exercise MR-R10"
  ],
  "steps": [
    {
      "step": 1,
      "input": {
        "name": "Nguyen Van A",
        "email": "mr.t02r01.tc45@example.com",
        "password": "Abcde1 x",
        "confirmation": "Abcde1 x",
        "expected": "REJECT"
      },
      "ui": {
        "at": "2026-10-19T20:04:35.530370+00:00",
        "feedback": [
          "Đăng ký tài khoản thành công."
        ],
        "success_signal": true,
        "dialog_seen": true,
        "login": true,
        "registration": false,
        "timed_out": false
      },
      "accounts": [
        {
          "email": "mr.t02r01.tc45@example.com",
          "count_before": 0,
          "count_after": 1,
          "existing_rows_unchanged": true,
          "new_accounts": [
            {
              "id": 37,
              "name": "Nguyen Van A",
              "email": "mr.t02r01.tc45@example.com"
            }
          ]
        }
      ],
      "assertion_failures": [
        "Invalid/duplicate submission created or changed watched account data",
        "Invalid submission reported registration success",
        "Invalid submission reached Login as if registration succeeded"
      ],
      "input_verification": [
        {
          "field": "name",
          "readback": "Nguyen Van A"
        },
        {
          "field": "email",
          "readback": "mr.t02r01.tc45@example.com"
        },
        {
          "field": "password",
          "readback": "masked: transport acknowledged; plaintext not exposed"
        }
      ]
    }
  ]
}
```

<a id="log-mr-tc46"></a>
### MR-TC46 / MR-RUN-07

Nguồn: [results.json](results.json), `cases[45].results[1]`; ID `MR-TC46`, run `MR-RUN-07`, status `failed`.

**Actual đã ghi:** bước 1: tài khoản 0→1; báo thành công; Đăng nhập

```json
{
  "started_at": "2026-10-19T20:04:36.189573+00:00",
  "finished_at": "2026-10-19T20:05:32.717176+00:00",
  "submissions": 1,
  "form": {
    "complete": true,
    "fields": {
      "name": {
        "bounds": "[48,316][672,398]",
        "editable": true,
        "class": "android.widget.EditText"
      },
      "email": {
        "bounds": "[48,481][672,563]",
        "editable": true,
        "class": "android.widget.EditText"
      },
      "password": {
        "bounds": "[48,646][672,728]",
        "editable": true,
        "class": "android.widget.EditText"
      }
    }
  },
  "reason": "Invalid/duplicate submission created or changed watched account data; Invalid submission reported registration success; Invalid submission reached Login as if registration succeeded",
  "limitations": [
    "Confirmation absent; this case does not exercise MR-R10"
  ],
  "steps": [
    {
      "step": 1,
      "input": {
        "name": "Nguyen Van A",
        "email": "mr.t02r01.tc46@example.com",
        "password": "Abc1!😀d",
        "confirmation": "Abc1!😀d",
        "expected": "REJECT"
      },
      "ui": {
        "at": "2026-10-19T20:05:32.086777+00:00",
        "feedback": [
          "Đăng ký tài khoản thành công."
        ],
        "success_signal": true,
        "dialog_seen": true,
        "login": true,
        "registration": false,
        "timed_out": false
      },
      "accounts": [
        {
          "email": "mr.t02r01.tc46@example.com",
          "count_before": 0,
          "count_after": 1,
          "existing_rows_unchanged": true,
          "new_accounts": [
            {
              "id": 38,
              "name": "Nguyen Van A",
              "email": "mr.t02r01.tc46@example.com"
            }
          ]
        }
      ],
      "assertion_failures": [
        "Invalid/duplicate submission created or changed watched account data",
        "Invalid submission reported registration success",
        "Invalid submission reached Login as if registration succeeded"
      ],
      "input_verification": [
        {
          "field": "name",
          "readback": "Nguyen Van A"
        },
        {
          "field": "email",
          "readback": "mr.t02r01.tc46@example.com"
        },
        {
          "field": "password",
          "readback": "masked: transport acknowledged; plaintext not exposed"
        }
      ]
    }
  ]
}
```

<a id="log-mr-tc47"></a>
### MR-TC47 / MR-RUN-07

Nguồn: [results.json](results.json), `cases[46].results[1]`; ID `MR-TC47`, run `MR-RUN-07`, status `passed`.

**Actual đã ghi:** bước 1: tài khoản 0→1; báo thành công; Đăng nhập

```json
{
  "started_at": "2026-10-19T20:05:32.771034+00:00",
  "finished_at": "2026-10-19T20:06:28.889953+00:00",
  "submissions": 1,
  "form": {
    "complete": true,
    "fields": {
      "name": {
        "bounds": "[48,316][672,398]",
        "editable": true,
        "class": "android.widget.EditText"
      },
      "email": {
        "bounds": "[48,481][672,563]",
        "editable": true,
        "class": "android.widget.EditText"
      },
      "password": {
        "bounds": "[48,646][672,728]",
        "editable": true,
        "class": "android.widget.EditText"
      }
    }
  },
  "limitations": [
    "Confirmation absent; this case does not exercise MR-R10"
  ],
  "steps": [
    {
      "step": 1,
      "input": {
        "name": "Nguyen Van A",
        "email": "mr.t02r01.tc47@example.com",
        "password": "Abc1!😀de",
        "confirmation": "Abc1!😀de",
        "expected": "ACCEPT"
      },
      "ui": {
        "at": "2026-10-19T20:06:28.260554+00:00",
        "feedback": [
          "Đăng ký tài khoản thành công."
        ],
        "success_signal": true,
        "dialog_seen": true,
        "login": true,
        "registration": false,
        "timed_out": false
      },
      "accounts": [
        {
          "email": "mr.t02r01.tc47@example.com",
          "count_before": 0,
          "count_after": 1,
          "existing_rows_unchanged": true,
          "new_accounts": [
            {
              "id": 39,
              "name": "Nguyen Van A",
              "email": "mr.t02r01.tc47@example.com"
            }
          ]
        }
      ],
      "assertion_failures": [],
      "input_verification": [
        {
          "field": "name",
          "readback": "Nguyen Van A"
        },
        {
          "field": "email",
          "readback": "mr.t02r01.tc47@example.com"
        },
        {
          "field": "password",
          "readback": "masked: transport acknowledged; plaintext not exposed"
        }
      ]
    }
  ]
}
```

<a id="log-mr-tc48"></a>
### MR-TC48 / MR-RUN-07

Nguồn: [results.json](results.json), `cases[47].results[1]`; ID `MR-TC48`, run `MR-RUN-07`, status `passed`.

**Actual đã ghi:** bước 1: tài khoản 0→1; báo thành công; Đăng nhập

```json
{
  "started_at": "2026-10-19T20:06:28.892931+00:00",
  "finished_at": "2026-10-19T20:07:25.411583+00:00",
  "submissions": 1,
  "form": {
    "complete": true,
    "fields": {
      "name": {
        "bounds": "[48,316][672,398]",
        "editable": true,
        "class": "android.widget.EditText"
      },
      "email": {
        "bounds": "[48,481][672,563]",
        "editable": true,
        "class": "android.widget.EditText"
      },
      "password": {
        "bounds": "[48,646][672,728]",
        "editable": true,
        "class": "android.widget.EditText"
      }
    }
  },
  "limitations": [
    "Confirmation absent; this case does not exercise MR-R10"
  ],
  "steps": [
    {
      "step": 1,
      "input": {
        "name": "Nguyen Van A",
        "email": "mr.t02r01.tc48@example.com",
        "password": "Abc1!😀def",
        "confirmation": "Abc1!😀def",
        "expected": "ACCEPT"
      },
      "ui": {
        "at": "2026-10-19T20:07:24.793564+00:00",
        "feedback": [
          "Đăng ký tài khoản thành công."
        ],
        "success_signal": true,
        "dialog_seen": true,
        "login": true,
        "registration": false,
        "timed_out": false
      },
      "accounts": [
        {
          "email": "mr.t02r01.tc48@example.com",
          "count_before": 0,
          "count_after": 1,
          "existing_rows_unchanged": true,
          "new_accounts": [
            {
              "id": 40,
              "name": "Nguyen Van A",
              "email": "mr.t02r01.tc48@example.com"
            }
          ]
        }
      ],
      "assertion_failures": [],
      "input_verification": [
        {
          "field": "name",
          "readback": "Nguyen Van A"
        },
        {
          "field": "email",
          "readback": "mr.t02r01.tc48@example.com"
        },
        {
          "field": "password",
          "readback": "masked: transport acknowledged; plaintext not exposed"
        }
      ]
    }
  ]
}
```

<a id="log-mr-tc49"></a>
### MR-TC49 / MR-RUN-07

Nguồn: [results.json](results.json), `cases[48].results[1]`; ID `MR-TC49`, run `MR-RUN-07`, status `passed`.

**Actual đã ghi:** bước 1: tài khoản 0→1; báo thành công; Đăng nhập

```json
{
  "started_at": "2026-10-19T20:07:25.414823+00:00",
  "finished_at": "2026-10-19T20:08:21.757227+00:00",
  "submissions": 1,
  "form": {
    "complete": true,
    "fields": {
      "name": {
        "bounds": "[48,316][672,398]",
        "editable": true,
        "class": "android.widget.EditText"
      },
      "email": {
        "bounds": "[48,481][672,563]",
        "editable": true,
        "class": "android.widget.EditText"
      },
      "password": {
        "bounds": "[48,646][672,728]",
        "editable": true,
        "class": "android.widget.EditText"
      }
    }
  },
  "limitations": [
    "Confirmation absent; this case does not exercise MR-R10"
  ],
  "steps": [
    {
      "step": 1,
      "input": {
        "name": "Nguyen Van A",
        "email": "mr.t02r01.tc49@example.com",
        "password": "Abcde1_x",
        "confirmation": "Abcde1_x",
        "expected": "ACCEPT"
      },
      "ui": {
        "at": "2026-10-19T20:08:21.126423+00:00",
        "feedback": [
          "Đăng ký tài khoản thành công."
        ],
        "success_signal": true,
        "dialog_seen": true,
        "login": true,
        "registration": false,
        "timed_out": false
      },
      "accounts": [
        {
          "email": "mr.t02r01.tc49@example.com",
          "count_before": 0,
          "count_after": 1,
          "existing_rows_unchanged": true,
          "new_accounts": [
            {
              "id": 41,
              "name": "Nguyen Van A",
              "email": "mr.t02r01.tc49@example.com"
            }
          ]
        }
      ],
      "assertion_failures": [],
      "input_verification": [
        {
          "field": "name",
          "readback": "Nguyen Van A"
        },
        {
          "field": "email",
          "readback": "mr.t02r01.tc49@example.com"
        },
        {
          "field": "password",
          "readback": "masked: transport acknowledged; plaintext not exposed"
        }
      ]
    }
  ]
}
```

<a id="log-mr-tc50"></a>
### MR-TC50 / MR-RUN-07

Nguồn: [results.json](results.json), `cases[49].results[1]`; ID `MR-TC50`, run `MR-RUN-07`, status `passed`.

**Actual đã ghi:** bước 1: tài khoản 0→1; báo thành công; Đăng nhập

```json
{
  "started_at": "2026-10-19T20:08:21.761516+00:00",
  "finished_at": "2026-10-19T20:09:18.359489+00:00",
  "submissions": 1,
  "form": {
    "complete": true,
    "fields": {
      "name": {
        "bounds": "[48,316][672,398]",
        "editable": true,
        "class": "android.widget.EditText"
      },
      "email": {
        "bounds": "[48,481][672,563]",
        "editable": true,
        "class": "android.widget.EditText"
      },
      "password": {
        "bounds": "[48,646][672,728]",
        "editable": true,
        "class": "android.widget.EditText"
      }
    }
  },
  "limitations": [
    "Confirmation absent; this case does not exercise MR-R10"
  ],
  "steps": [
    {
      "step": 1,
      "input": {
        "name": "Nguyen Van A",
        "email": "mr.t02r01.tc50@example.com",
        "password": "Abcdef1😀",
        "confirmation": "Abcdef1😀",
        "expected": "ACCEPT"
      },
      "ui": {
        "at": "2026-10-19T20:09:17.751113+00:00",
        "feedback": [
          "Đăng ký tài khoản thành công."
        ],
        "success_signal": true,
        "dialog_seen": true,
        "login": true,
        "registration": false,
        "timed_out": false
      },
      "accounts": [
        {
          "email": "mr.t02r01.tc50@example.com",
          "count_before": 0,
          "count_after": 1,
          "existing_rows_unchanged": true,
          "new_accounts": [
            {
              "id": 42,
              "name": "Nguyen Van A",
              "email": "mr.t02r01.tc50@example.com"
            }
          ]
        }
      ],
      "assertion_failures": [],
      "input_verification": [
        {
          "field": "name",
          "readback": "Nguyen Van A"
        },
        {
          "field": "email",
          "readback": "mr.t02r01.tc50@example.com"
        },
        {
          "field": "password",
          "readback": "masked: transport acknowledged; plaintext not exposed"
        }
      ]
    }
  ]
}
```

<a id="log-mr-tc51"></a>
### MR-TC51 / MR-RUN-07

Nguồn: [results.json](results.json), `cases[50].results[1]`; ID `MR-TC51`, run `MR-RUN-07`, status `passed`.

**Actual đã ghi:** bước 1: tài khoản 0→1; báo thành công; Đăng nhập

```json
{
  "started_at": "2026-10-19T20:09:18.363111+00:00",
  "finished_at": "2026-10-19T20:10:14.562340+00:00",
  "submissions": 1,
  "form": {
    "complete": true,
    "fields": {
      "name": {
        "bounds": "[48,316][672,398]",
        "editable": true,
        "class": "android.widget.EditText"
      },
      "email": {
        "bounds": "[48,481][672,563]",
        "editable": true,
        "class": "android.widget.EditText"
      },
      "password": {
        "bounds": "[48,646][672,728]",
        "editable": true,
        "class": "android.widget.EditText"
      }
    }
  },
  "limitations": [
    "Confirmation absent; this case does not exercise MR-R10"
  ],
  "steps": [
    {
      "step": 1,
      "input": {
        "name": "Nguyen Van A",
        "email": "mr.t02r01.tc51@example.com",
        "password": "Abcde1—x",
        "confirmation": "Abcde1—x",
        "expected": "ACCEPT"
      },
      "ui": {
        "at": "2026-10-19T20:10:13.954906+00:00",
        "feedback": [
          "Đăng ký tài khoản thành công."
        ],
        "success_signal": true,
        "dialog_seen": true,
        "login": true,
        "registration": false,
        "timed_out": false
      },
      "accounts": [
        {
          "email": "mr.t02r01.tc51@example.com",
          "count_before": 0,
          "count_after": 1,
          "existing_rows_unchanged": true,
          "new_accounts": [
            {
              "id": 43,
              "name": "Nguyen Van A",
              "email": "mr.t02r01.tc51@example.com"
            }
          ]
        }
      ],
      "assertion_failures": [],
      "input_verification": [
        {
          "field": "name",
          "readback": "Nguyen Van A"
        },
        {
          "field": "email",
          "readback": "mr.t02r01.tc51@example.com"
        },
        {
          "field": "password",
          "readback": "masked: transport acknowledged; plaintext not exposed"
        }
      ]
    }
  ]
}
```

<a id="log-mr-tc52"></a>
### MR-TC52 / MR-RUN-07

Nguồn: [results.json](results.json), `cases[51].results[1]`; ID `MR-TC52`, run `MR-RUN-07`, status `passed`.

**Actual đã ghi:** bước 1: tài khoản 0→1; báo thành công; Đăng nhập

```json
{
  "started_at": "2026-10-19T20:10:14.566859+00:00",
  "finished_at": "2026-10-19T20:11:10.477383+00:00",
  "submissions": 1,
  "form": {
    "complete": true,
    "fields": {
      "name": {
        "bounds": "[48,316][672,398]",
        "editable": true,
        "class": "android.widget.EditText"
      },
      "email": {
        "bounds": "[48,481][672,563]",
        "editable": true,
        "class": "android.widget.EditText"
      },
      "password": {
        "bounds": "[48,646][672,728]",
        "editable": true,
        "class": "android.widget.EditText"
      }
    }
  },
  "limitations": [
    "Confirmation absent; this case does not exercise MR-R10"
  ],
  "steps": [
    {
      "step": 1,
      "input": {
        "name": "Nguyen Van A",
        "email": "mr.t02r01.tc52@example.com",
        "password": "Abcde1€x",
        "confirmation": "Abcde1€x",
        "expected": "ACCEPT"
      },
      "ui": {
        "at": "2026-10-19T20:11:09.870154+00:00",
        "feedback": [
          "Đăng ký tài khoản thành công."
        ],
        "success_signal": true,
        "dialog_seen": true,
        "login": true,
        "registration": false,
        "timed_out": false
      },
      "accounts": [
        {
          "email": "mr.t02r01.tc52@example.com",
          "count_before": 0,
          "count_after": 1,
          "existing_rows_unchanged": true,
          "new_accounts": [
            {
              "id": 44,
              "name": "Nguyen Van A",
              "email": "mr.t02r01.tc52@example.com"
            }
          ]
        }
      ],
      "assertion_failures": [],
      "input_verification": [
        {
          "field": "name",
          "readback": "Nguyen Van A"
        },
        {
          "field": "email",
          "readback": "mr.t02r01.tc52@example.com"
        },
        {
          "field": "password",
          "readback": "masked: transport acknowledged; plaintext not exposed"
        }
      ]
    }
  ]
}
```

<a id="log-mr-tc53"></a>
### MR-TC53 / MR-RUN-07

Nguồn: [results.json](results.json), `cases[52].results[1]`; ID `MR-TC53`, run `MR-RUN-07`, status `failed`.

**Actual đã ghi:** bước 1: tài khoản 0→1; báo thành công; Đăng nhập

```json
{
  "started_at": "2026-10-19T20:11:10.481216+00:00",
  "finished_at": "2026-10-19T20:12:06.008953+00:00",
  "submissions": 1,
  "form": {
    "complete": true,
    "fields": {
      "name": {
        "bounds": "[48,316][672,398]",
        "editable": true,
        "class": "android.widget.EditText"
      },
      "email": {
        "bounds": "[48,481][672,563]",
        "editable": true,
        "class": "android.widget.EditText"
      },
      "password": {
        "bounds": "[48,646][672,728]",
        "editable": true,
        "class": "android.widget.EditText"
      }
    }
  },
  "reason": "Invalid/duplicate submission created or changed watched account data; Invalid submission reported registration success; Invalid submission reached Login as if registration succeeded",
  "limitations": [
    "Confirmation absent; this case does not exercise MR-R10"
  ],
  "steps": [
    {
      "step": 1,
      "input": {
        "name": "Nguyen Van A",
        "email": " test@eshop.com ",
        "password": "Abcde1!x",
        "confirmation": "Abcde1!x",
        "expected": "REJECT"
      },
      "ui": {
        "at": "2026-10-19T20:12:05.402467+00:00",
        "feedback": [
          "Đăng ký tài khoản thành công."
        ],
        "success_signal": true,
        "dialog_seen": true,
        "login": true,
        "registration": false,
        "timed_out": false
      },
      "accounts": [
        {
          "email": " test@eshop.com ",
          "count_before": 0,
          "count_after": 1,
          "existing_rows_unchanged": true,
          "new_accounts": [
            {
              "id": 45,
              "name": "Nguyen Van A",
              "email": " test@eshop.com "
            }
          ]
        },
        {
          "email": "test@eshop.com",
          "count_before": 2,
          "count_after": 2,
          "existing_rows_unchanged": true,
          "new_accounts": []
        }
      ],
      "assertion_failures": [
        "Invalid/duplicate submission created or changed watched account data",
        "Invalid submission reported registration success",
        "Invalid submission reached Login as if registration succeeded"
      ],
      "input_verification": [
        {
          "field": "name",
          "readback": "Nguyen Van A"
        },
        {
          "field": "email",
          "readback": " test@eshop.com "
        },
        {
          "field": "password",
          "readback": "masked: transport acknowledged; plaintext not exposed"
        }
      ]
    }
  ]
}
```

<a id="log-mr-tc54"></a>
### MR-TC54 / MR-RUN-07

Nguồn: [results.json](results.json), `cases[53].results[1]`; ID `MR-TC54`, run `MR-RUN-07`, status `passed`.

**Actual đã ghi:** bước 1: tài khoản 0→1; báo thành công; Đăng nhập

```json
{
  "started_at": "2026-10-19T20:12:06.052116+00:00",
  "finished_at": "2026-10-19T20:13:02.753976+00:00",
  "submissions": 1,
  "form": {
    "complete": true,
    "fields": {
      "name": {
        "bounds": "[48,316][672,398]",
        "editable": true,
        "class": "android.widget.EditText"
      },
      "email": {
        "bounds": "[48,481][672,563]",
        "editable": true,
        "class": "android.widget.EditText"
      },
      "password": {
        "bounds": "[48,646][672,728]",
        "editable": true,
        "class": "android.widget.EditText"
      }
    }
  },
  "limitations": [
    "Confirmation absent; this case does not exercise MR-R10"
  ],
  "steps": [
    {
      "step": 1,
      "input": {
        "name": "Nguyen Van A",
        "email": "mr.t02r01.tc54@example.com",
        "password": "Abc1! xy",
        "confirmation": "Abc1! xy",
        "expected": "ACCEPT"
      },
      "ui": {
        "at": "2026-10-19T20:13:02.147029+00:00",
        "feedback": [
          "Đăng ký tài khoản thành công."
        ],
        "success_signal": true,
        "dialog_seen": true,
        "login": true,
        "registration": false,
        "timed_out": false
      },
      "accounts": [
        {
          "email": "mr.t02r01.tc54@example.com",
          "count_before": 0,
          "count_after": 1,
          "existing_rows_unchanged": true,
          "new_accounts": [
            {
              "id": 46,
              "name": "Nguyen Van A",
              "email": "mr.t02r01.tc54@example.com"
            }
          ]
        }
      ],
      "assertion_failures": [],
      "input_verification": [
        {
          "field": "name",
          "readback": "Nguyen Van A"
        },
        {
          "field": "email",
          "readback": "mr.t02r01.tc54@example.com"
        },
        {
          "field": "password",
          "readback": "masked: transport acknowledged; plaintext not exposed"
        }
      ]
    }
  ]
}
```
