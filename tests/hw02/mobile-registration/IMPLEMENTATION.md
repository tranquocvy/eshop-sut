# Triển khai test Mobile Registration

Bộ code hiện thực [design.md](design.md) và [test-cases.md](test-cases.md) **v0.3**: MR-TC01–MR-TC54. Hai tài liệu được giữ nguyên. **Chưa thực thi code hoặc TC trên SUT trong bước implementation.**

## Các file

| File | Chức năng |
| --- | --- |
| [scripts/cases.json](scripts/cases.json) | 54 ID, nguyên văn các cột của bảng TC, dữ liệu literal N/E/P/C, expected và các điều kiện fixture; kèm hash hai tài liệu |
| [scripts/native_android.py](scripts/native_android.py) | Mở/navigate app native, tìm input theo nhãn, nhập liệu bằng Android CLI, quan sát UI và chụp PNG/JPG khi chạy |
| [scripts/run.py](scripts/run.py) | Điều phối từng TC, precondition, sequence, đọc SQLite, assertions và kết quả theo run |

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
- Mỗi input có receipt chứa chuỗi yêu cầu, số code point, số UTF-16 unit và SHA-256 UTF-8. Khi accessibility cho đọc plaintext, đối chiếu readback. Với field mật khẩu bị che, receipt ghi rõ chỉ xác nhận native command thành công, không giả nhận đã đọc lại plaintext. Khả năng nhập/readback Unicode của thiết bị phải được xác minh ở lượt execution; chưa có kết luận runtime ở bước này.
- SQLite mở bằng URI `mode=ro` và `query_only=ON`. Chỉ SELECT các cột account không chứa password/reset token. Không import backend, không INSERT/DELETE, không seed/reset hoặc tự tạo fixture còn thiếu.
- Database phải là bản runtime trong manifest môi trường. Runner từ chối `backend/database.sqlite` được theo dõi trong repo. Người chạy phải dùng đúng manifest của backend đang phục vụ app; runner không khởi động hoặc tái cấu hình backend/Metro.
- ACCEPT cần đúng một account Ecanon mới, name/email đúng và app tới Login; REJECT cần account không tăng/đổi, có feedback thất bại, không báo thành công hay chuyển tới Login. Các identity raw/trim/lowercase liên quan được đọc riêng để phát hiện sai normalization; không so tổng account của cả DB.
- Các kết quả phụ thuộc bước trước chỉ chạy khi bước trước đúng expected. Nếu bước đầu TC13/TC38 sai, case ghi `failed` và phần sequence còn lại chưa thực hiện, không sửa state để tiếp tục.
- Mỗi TC bắt đầu lại **client Expo Go**, không clear app data và không restart backend. Môi trường Expo Go phải sẵn sàng mở EShop; màn hình onboarding/developer menu ngoài dự kiến là vấn đề setup và không được tự nhận là test pass.

## Điều kiện chạy ở bước execution sau

Python 3.10+, Pillow để xuất JPG; Android CLI/adb của SDK đã chuẩn bị ở T01; emulator và backend/Metro được mở đúng cấu hình API trước khi chạy. Script không cài dependency, mở emulator, áp patch API hoặc tạo backend runtime.

Manifest `services.json` do setup tạo phải có `backend_database` là đường dẫn tuyệt đối và `mobile_api_url` đúng backend của app. Runner chỉ GET `/products` để kiểm tra kết nối; mọi submit đăng ký đều đi qua native, không gọi `/register` hoặc `/login` bằng API.

**Lệnh dành cho lượt execution sau — chưa chạy ở bước này**, từ repo:

```powershell
python .\tests\hw02\mobile-registration\scripts\run.py `
  --execute `
  --manifest '..\.runtime\<runtime-da-chon>\services.json' `
  --device emulator-5554 `
  --expo-url 'exp://10.0.2.2:8081' `
  --namespace t02r01
```

Có thể chọn ID bằng `--case MR-TC01 MR-TC13`. Không có `--execute`, runner dừng trước mọi thao tác thiết bị/DB. Namespace/run ID được kiểm tra để không tạo đường dẫn tùy ý; run folder đã tồn tại không bị ghi đè.

Các precondition phải được đáp ứng thật. Nếu email cần mới đã tồn tại, hoặc fixture cần có lại thiếu, case bị `blocked`. Đổi namespace không giải quyết fixture cố định `TEST@eshop.com` đã được tạo ở lần chạy TC42 trước; cần chọn dataset/runtime phù hợp trước lượt chạy mới, không tự xóa dữ liệu trong runner.

## Đầu ra khi có run thật

Chỉ khi chạy mới tạo `evidence/<run-id>/results.json` và thư mục evidence theo TC. Kết quả ghi expected, actual observation, snapshot account trước–sau, receipts, trace thao tác/layout, timestamp và PNG/JPG thật. Không tạo actual/status giả trong bước implementation.

Status: `passed`, `failed`, `blocked`, `not_run`. `executed = passed + failed`; `not_executed = blocked + not_run`. Không tạo GitHub Issues, AI log, PDF hoặc tự sửa hai tài liệu/SUT. Bộ JSON là dữ liệu đầu vào cho bước tổng hợp báo cáo sau này.
