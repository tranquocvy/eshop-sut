# Triển khai test Mobile Registration

Bộ code hiện thực [design.md](design.md) và [test-cases.md](test-cases.md) **v0.3**: MR-TC01–MR-TC54. Hai tài liệu được giữ nguyên. **Chưa thực thi code hoặc TC trên SUT trong bước implementation.**

## Các file

| File | Chức năng |
| --- | --- |
| [scripts/cases.json](scripts/cases.json) | 54 ID, nguyên văn các cột của bảng TC, dữ liệu literal N/E/P/C, expected và các điều kiện fixture; kèm hash hai tài liệu |
| [scripts/native_android.py](scripts/native_android.py) | Mở/navigate app native, tìm input theo nhãn, nhập liệu bằng Android CLI, quan sát UI; giữ capture tạm trong bộ nhớ và chỉ lưu JPG cần thiết cho lỗi |
| [scripts/run.py](scripts/run.py) | Điều phối từng TC, precondition, sequence, đọc SQLite, assertions; nối lịch sử vào một nguồn kết quả chung |

Không có unit test mô phỏng validator thay thế việc kiểm tra Mobile. Expected ACCEPT/REJECT được cố định theo bảng TC, không tính lại từ regex hay hành vi hiện tại của SUT.

## Ánh xạ cách thực hiện

| TC | Triển khai |
| --- | --- |
| 01–12,14–32,40–54 | Nhập đúng N/E/P; nếu có Confirmation thì điền theo TC; submit một lần; đối chiếu UI và dữ liệu account |
| 13 | ACCEPT lần đầu → Home → Login → Register → nhập lại cùng email → REJECT lần hai. Không restart client/DB giữa hai lần |
| 33 | Quan sát/scroll toàn form; kiểm tra Confirmation có control riêng và editable; không submit |
| 34–37 | Kiểm tra C-guard trước; nếu không có Confirmation thì `blocked`, giữ nguyên TC. Nếu có, nhập C rỗng/sai/khớp theo tài liệu |
| 38 | REJECT password 7 → giữ N/E và form → chỉ sửa P/C thành password 8 → ACCEPT. Không reset dữ liệu giữa sequence |
| 39 | Email duplicate và password thiếu hoa; không áp đặt lỗi nào được báo trước |

Case catalogue giữ từng TC riêng, kể cả ca dùng chung dữ liệu hoặc boundary item. TC16 chỉ là một TC; không đếm lặp do có nhiều nhãn biên. TC47–54 vẫn giữ nguồn expected từ quy ước S7.

## Dữ liệu, nhập liệu và quan sát

- Namespace mặc định là `t02r01`, đúng dữ liệu trong tài liệu. Tham số `--namespace` chỉ đổi token trong email của ca, không đổi password/tên/expected hay fixture cố định `test@eshop.com`/`TEST@eshop.com`.
- Đối chiếu email bằng `COLLATE BINARY`; trim chỉ dùng để xác định **oracle Ecanon**. Chuỗi gửi vào form vẫn có nguyên space/case. Password không bị trim, đổi ASCII, escape thành `%s` hoặc normalize Unicode.
- `android input text` thay nội dung input native qua một argv Unicode, không dùng shell để ghép lệnh. Tìm field bằng nhãn, lấy bounds mới trước tap; selector text đặt vào đúng EditText đang focus. Tham khảo [Android input text](https://developer.android.com/tools/agents/android-cli/commands/input_text), [layout](https://developer.android.com/tools/agents/android-cli/commands/layout).
- Chuỗi input literal và readback cần đối chiếu được lưu trong kết quả chung. Khi accessibility cho đọc plaintext, đối chiếu readback. Với field mật khẩu bị che, ghi rõ chỉ xác nhận native command thành công, không giả nhận đã đọc lại plaintext. Chi tiết kết quả Unicode phụ thuộc run thực tế, không suy ra chỉ từ code nhập liệu.
- SQLite mở bằng URI `mode=ro` và `query_only=ON`. Chỉ SELECT các cột account không chứa password/reset token. Không import backend, không INSERT/DELETE, không seed/reset hoặc tự tạo fixture còn thiếu.
- Database phải là bản runtime trong manifest môi trường. Runner từ chối `backend/database.sqlite` được theo dõi trong repo. Người chạy phải dùng đúng manifest của backend đang phục vụ app; runner không khởi động hoặc tái cấu hình backend/Metro.
- ACCEPT cần đúng một account Ecanon mới, name/email đúng và app tới Login; REJECT cần account không tăng/đổi, có feedback thất bại, không báo thành công hay chuyển tới Login. Các identity raw/trim/lowercase liên quan được đọc riêng để phát hiện sai normalization; không so tổng account của cả DB.
- Các kết quả phụ thuộc bước trước chỉ chạy khi bước trước đúng expected. Nếu bước đầu TC13/TC38 sai, case ghi `failed` và phần sequence còn lại chưa thực hiện, không sửa state để tiếp tục.
- Giữ phiên Expo Go đang chạy; từ Login quay về Register, hoặc thay dữ liệu trên form đang mở. Không clear app data/restart backend và không reset giữa sequence. Layout dùng `--no-idle` để tránh blocker do animation; vẫn đợi đúng màn hình/feedback và quan sát persistence trước khi kết luận. Màn hình onboarding/developer menu ngoài dự kiến là vấn đề setup, không phải test pass.
- Runner hiện điều hướng Home → Login → Register bằng phiên app đang mở theo bước S. Nếu validation làm field đang focus bị bàn phím che, đóng IME rồi kiểm tra lại field trước khi thay nội dung. C-guard thiếu Confirmation là dependency của TC; lỗi transport lặp hoặc submit chưa xác định thì dừng để kiểm tra state.

## Điều kiện chạy ở bước execution sau

Python 3.10+, Pillow để xuất JPG; Android CLI/adb của SDK đã chuẩn bị ở T01; emulator và backend/Metro được mở đúng cấu hình API trước khi chạy. Script không cài dependency, mở emulator, áp patch API hoặc tạo backend runtime.

Manifest `services.json` do setup tạo phải có `backend_database` là đường dẫn tuyệt đối và `mobile_api_url` đúng backend của app. Runner chỉ GET `/products` để kiểm tra kết nối; mọi submit đăng ký đều đi qua native, không gọi `/register` hoặc `/login` bằng API.

**Lệnh execution/resume**, từ repo; cần có kết quả chung của bộ MR để nối lịch sử:

```powershell
python .\tests\hw02\mobile-registration\scripts\run.py `
  --execute `
  --manifest '..\.runtime\<runtime-da-chon>\services.json' `
  --device emulator-5554 `
  --expo-url 'exp://10.0.2.2:8083' `
  --namespace t02r01
```

Có thể chọn ID bằng `--case MR-TC01 MR-TC13`. Mặc định tiếp tục các TC blocked/not_run; mỗi lần dùng run ID mới. Không có `--execute`, runner dừng trước mọi thao tác thiết bị/DB. Namespace/run ID được kiểm tra; run ID đã tồn tại bị từ chối để giữ lịch sử.

Các precondition phải được đáp ứng thật. Nếu email cần mới đã tồn tại, hoặc fixture cần có lại thiếu, case bị `blocked`. Đổi namespace không giải quyết fixture cố định `TEST@eshop.com` đã được tạo ở lần chạy TC42 trước; cần chọn dataset/runtime phù hợp trước lượt chạy mới, không tự xóa dữ liệu trong runner.

## Đầu ra khi có run thật

Một [results.json](results.json) lưu metadata mỗi run và lịch sử theo TC: input, observation UI, count/account trước–sau, assertion và readback cần thiết. Summary đếm kết quả được chọn mới nhất trên unique TC, loại probe khỏi summary. Không ghi thư mục/log/layout riêng cho từng TC. [report.md](report.md) là bản đọc để review input → expected → actual → kết luận.

Capture input/feedback tạm nằm trong bộ nhớ. Khi TC fail, lưu JPG input/actual cần thiết trong `images/`; các TC có cùng nhóm oracle và assertion failure có thể dùng chung ảnh đại diện, vẫn giữ observations riêng. TC pass không cần ảnh. Không ghi PNG ra đĩa.

Status: `passed`, `failed`, `blocked`, `not_run`. `executed = passed + failed`; `not_executed = blocked + not_run`. Không tạo GitHub Issues, AI log, PDF hoặc tự sửa hai tài liệu/SUT. Bộ JSON là dữ liệu đầu vào cho bước tổng hợp báo cáo sau này.
