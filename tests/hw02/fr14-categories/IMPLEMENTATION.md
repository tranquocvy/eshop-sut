# Triển khai T03 — Category Management

Code hiện thực **CAT-TC01–CAT-TC33** từ [design.md](design.md) và [test-cases.md](test-cases.md) v0.2, đã duyệt tại commit `b84417b`. Hai tài liệu được giữ nguyên. **Bước này chưa thực thi runner/TC trên SUT, chưa sinh kết quả hoặc report.**

## Các file

| File | Nội dung |
| --- | --- |
| [scripts/cases.json](scripts/cases.json) | 33 ID riêng, nguyên văn technique/traceability/precondition/input/steps/expected và dòng nguồn của mỗi TC; dữ liệu literal, fixture, method, body, loại token và oracle thực thi; hash hai tài liệu |
| [scripts/run.py](scripts/run.py) | Điều phối TC; thao tác Web qua Playwright; request API riêng; quan sát API và SQLite chỉ đọc; assertions theo bộ thiết kế |
| [requirements.txt](requirements.txt) | Playwright Python cho nhóm Web; HTTP/SQLite/biến đổi JWT dùng thư viện chuẩn Python |

Mỗi record trong catalogue là một TC, dù dùng chung handler. Expected lấy từ bảng nguồn; không lấy hành vi hiện tại của server làm expected, không cộng đôi TC có cả Domain và BVA. Hash kiểm tra khác biệt nội dung tài liệu, bỏ qua chuyển đổi xuống dòng LF/CRLF của Git.

## Ánh xạ TC sang code

| TC | Handler / thao tác / assertion |
| --- | --- |
| 01–03 | `web_view`: đăng nhập admin, xem rồi reload; đối chiếu đủ ID/tên với C0/C1/C3, không xét thứ tự |
| 04–07 | `web_add`: nhập đúng `Đồ học tập T03`, rỗng, `A`, `AB`; bấm một lần; quan sát phản hồi, dữ liệu và UI trước/sau reload. Ca rỗng phải bị từ chối; các tên hợp lệ tạo đúng một bản ghi |
| 08–10 | `api`: POST trực tiếp bằng TA; phân biệt `{}`, `{"name":null}`, `{"name":""}`; từ chối và giữ nguyên danh mục. TC10 là điểm B02-0 |
| 11–12 | `web_delete`: xác định i2/i1 bằng tên fixture, chọn đúng dòng và Xóa; chấp nhận confirm nếu có; kiểm tra chỉ đích bị xóa, kể cả danh mục cuối; xem lại sau reload |
| 13 | `web_access/guest`: context mới không token; mở Admin và reload; không vào được quản lý danh mục |
| 14 | `web_access/login_user`: kiểm tra danh tính user hợp lệ, nhập đúng thông tin tại Admin Login; kiểm tra bị chặn trước/sau reload |
| 15–17 | `api`: POST/DELETE/PUT không gửi Authorization; từ chối do xác thực/quyền và không đổi danh mục |
| 18–20 | `api`: cùng ba method, `Bearer not-a-jwt` |
| 21–23 | `api`: cùng ba method, token user nguyên gốc đã xác minh qua `/users/me` |
| 24 | `api`: DELETE ID vắng, bắt đầu bằng 999999 và tìm ứng viên khác nếu cần; chỉ assert tập danh mục không đổi, không yêu cầu status/message cụ thể |
| 25–26 | `api`: POST `A`/`AB` bằng TA; đúng hai điểm B02-1/2, thêm một bản ghi và giữ các bản ghi cũ |
| 27–29 | `api`: TP sửa duy nhất role payload TU thành admin, giữ H/S, không ký lại; POST/DELETE/PUT đều phải bị từ chối |
| 30–32 | `api`: TS lật bit `0x01` ở byte đầu chữ ký TA, giữ H/P; cùng ba method phải bị từ chối |
| 33 | `web_access/stored_user`: ghi nguyên TU vào `localStorage.adminToken`, đóng tab và mở tab mới cùng context; không submit Login, không dùng init script để ép token sau reload; kiểm tra bị chặn ở cả hai lần quan sát |

TC PUT chỉ kiểm tra quyền/xác thực; không thêm nghiệp vụ Update. Missing/null không được đổi thành chuỗi rỗng khi gửi API. Token bị sửa chỉ là dữ liệu âm, không sửa role tài khoản hoặc ký token bằng secret của SUT. Token/password không được ghi vào dữ liệu quan sát login; phần ghi nhận request âm chỉ lưu tên biến thể token.

## Fixture và điều kiện trước

Runner dùng đúng **C0/C1/C3** từ catalogue và bộ thiết kế; so tên theo nguyên chuỗi, ánh xạ ID thực qua tên, kiểm tra không có sản phẩm tham chiếu. Trước TC, danh mục từ GET bằng TA phải khớp SQLite của runtime được chọn. Account admin/user cần đúng role; token gốc lấy qua login bình thường và xác minh `/users/me` trước khi dùng/biến đổi.

**Fixture do bước chuẩn bị execution cung cấp**, ngoài thao tác đang đánh giá. Runner không INSERT/UPDATE/DELETE database, không xóa seed, không reset, không restart dịch vụ và không import `backend/database.js`. SQLite dùng `mode=ro`, `query_only=ON` và đóng connection sau mỗi lần đọc. Database trong repo bị từ chối; manifest phải trỏ đúng database của backend đang phục vụ UI/API.

Chưa có fixture đúng thì TC `blocked`; đây không phải pass hoặc kết luận lỗi SUT. Các ca thêm/xóa có thể làm dataset khác C0/C1/C3, nên phải chuẩn bị lại fixture độc lập trước ca tiếp theo; runner không tự khôi phục để che kết quả của ca trước. Có thể chọn nhóm không thay đổi dữ liệu cùng fixture để chạy nối tiếp. Sau một ca bị SUT thay đổi dữ liệu trái expected, các ca sau vẫn phải qua kiểm tra fixture.

## Thao tác và quan sát

- Web dùng context mới cho mỗi TC. Thao tác đi qua form/nút thật; request API không thay thao tác Web và không mock/intercept response của SUT.
- Phản hồi được chờ bằng sự kiện/poll điều kiện có timeout; kiểm tra UI sau refresh/reload và dữ liệu trước/sau. Không chỉ dựa vào alert hoặc HTTP success để nhận thêm/xóa thành công.
- Đăng nhập là setup; không kiểm thử FR-02. HTTP observer dùng TA riêng, không tự kèm TA vào request âm. TC guest/user không được hưởng phiên admin của TC trước.
- NAME-REJECT cần feedback validation/thất bại, không có phản hồi thêm thành công và danh mục giữ nguyên. AUTH-REJECT cần quan sát được sự từ chối xác thực/quyền; không ép đúng một toast hoặc duy nhất mã 401/403.
- Nếu UI chặn tên rỗng, chỉ credit Web; TC10 vẫn gửi rỗng trực tiếp tới API. Thiếu điểm quan sát hoặc lỗi harness ghi blocked; request có kết quả chưa rõ sẽ dừng batch, không tự gửi lại mutation.
- TC24 chỉ kiểm tra invariant theo ID. Không bổ sung policy tên trùng, whitespace, max length, cascade hoặc xóa khi đang có sản phẩm ngoài hai tài liệu đã duyệt.

## Dùng ở bước execution sau

Python 3.10+; Web cần Playwright và Chromium. Cài dependency/browser là việc chuẩn bị cho lượt execution sau, chưa thực hiện trong bước này. API-only không khởi động browser. Tham khảo [cài Playwright](https://playwright.dev/python/docs/intro), [Locator](https://playwright.dev/python/docs/api/class-locator) và [Dialog](https://playwright.dev/python/docs/dialogs).

Không có `--execute`, script chỉ liệt kê TC/handler/oracle, không kết nối DB, gọi HTTP, mở browser hoặc tạo file kết quả. Tài liệu này chỉ minh họa lệnh; các lệnh dưới chưa được chạy.

```powershell
# Liệt kê catalogue, không thực thi TC
python .\tests\hw02\fr14-categories\scripts\run.py

# Khi được giao execution: ví dụ TC25 với fixture C3 đã chuẩn bị đúng
python .\tests\hw02\fr14-categories\scripts\run.py `
  --execute --case CAT-TC25 `
  --manifest '..\.runtime\<runtime-da-chon>\services.json' `
  --output '..\.runtime\<run-moi>\category-results.json'
```

Manifest cần `backend_database` là đường dẫn tuyệt đối tới SQLite runtime thực. UI/API theo đúng bộ TC: `http://localhost:5174/` và `http://localhost:3000/api`. Chọn nhiều ID bằng `--case CAT-TC15 CAT-TC16 CAT-TC17`; không mặc định rằng các TC thêm/xóa chia sẻ được cùng state. `--headed` hiện Chromium; `--timeout-ms` là timeout thao tác harness, không phải một biên nghiệp vụ.

Chỉ khi có `--execute`, runner mới tạo JSON execution tại đường dẫn mới được chỉ định, ghi kết quả/quan sát từng TC và giữ những ID chưa chạy ở `not_run`. File đã tồn tại bị từ chối để giữ lịch sử. Entry `execute_case` hỗ trợ lưu JPG lỗi khi bước execution truyền thư mục evidence; request API ghi method/path/body/biến thể token và response, không ghi JWT thật. Entry CLI không tự tạo report Markdown/PDF, issue hoặc AI log. **Lượt implementation này chỉ kiểm tra tĩnh, toàn bộ 33 TC vẫn Not Run.**

## Cập nhật execution T03 — 20/10/2026

Phần “chưa thực thi” ở trên mô tả mốc implementation ban đầu. Đợt execution theo skill đã chạy đủ **33 TC: 25 pass, 8 fail**, không blocked/not_run; xem [report](report.md) và [results.json](results.json). Design/TC v0.2 giữ nguyên.

Dùng runtime riêng tại `HW02/.runtime/T03-execution-20261020/`: `execute_suite.py` chuẩn bị fixture trong database mới trước từng TC rồi gọi `execute_case`; không viết DB từ runner và không đổi DB T01/Mobile. CAT-RUN-01 chạy TC01; CAT-RUN-02 chạy TC02–33. Adapter và services.json giữ trong runtime để tiếp tục tại máy hiện tại; các command main ở phần trên chỉ minh họa cách gọi runner với fixture ngoài. Harness bổ sung log body API/JPG lỗi, bỏ chờ Response.finished thừa gây cảnh báo teardown ở RUN01; không đổi input/expected/SUT. Không có mutation tự retry.

Report có link từng TC tới trích log theo đúng run và entry JSON; ghi 3 bug/issue #9–#11, 8 ảnh actual của TC fail, 3 JPG trang issue và 1 JPG danh sách. Các ảnh được chụp thật, không phải ảnh log dựng. Chưa ghi AI audit, commit/push hoặc video trong đợt execution này.
