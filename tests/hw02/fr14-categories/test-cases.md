# T03 — FR-14 Category Management: bộ test case

**Thiết kế v0.2 — 20/10/2026 (UTC+7). 33 TC — tất cả Not Run; Vỹ đã review và yêu cầu commit.** Đã bổ sung đủ ba nhóm Vỹ yêu cầu sau khi xem v0.1. Nguồn, mô hình, giả định và coverage tại [design.md](design.md). Mọi ký hiệu R/D/B rút gọn bên dưới có prefix `CAT-`; ID đầy đủ của TC giữ nguyên trong bảng. Bản AI v0.1 nguyên gốc được giữ ngoài repo tại `HW02/.runtime/design-baselines/fr14-categories-ai-v0.1/`.

## Điều kiện trước và dữ liệu

- **P0:** môi trường kiểm thử riêng, kết nối bình thường, không có thay đổi đồng thời. Dữ liệu trước mỗi TC độc lập; chưa chuẩn bị fixture hoặc gọi SUT trong lượt thiết kế này. Dùng snapshot/fixture do người thực thi chuẩn bị; không xóa seed hoặc khởi động lại backend để tạo empty state (module database có logic reset).
- **PA:** P0 + đăng nhập Web Admin bằng tài khoản demo `admin@eshop.com` / `Admin123!`, token hợp lệ role admin. Mở tab **Danh mục**. Đăng nhập chỉ là setup; không đánh giá FR-02.
- **TA/TU:** JWT còn hợp lệ của admin/user do luồng login bình thường cấp. Tài khoản user demo: `test@eshop.com` / `Test1234!`. TA dùng cho API required; TU dùng cho API role. Không sửa role tài khoản trong database hoặc sửa SUT để lấy token. Token gốc phải dùng được ở request đọc thông tin chính mình (`GET /api/users/me`, S3 §2.1) với role tương ứng trước khi biến đổi; nếu setup không hợp lệ thì không credit ca token bị sửa.
- **TP (sửa payload):** từ TU dạng `H.P.S`, giải mã P theo base64url thành JSON, chỉ đổi `role` từ `user` thành `admin`, mã hóa UTF-8/base64url không padding thành P′. Ghép `H.P′.S`, giữ nguyên header và chữ ký cũ, không ký lại. TP vẫn có ba phần hợp lệ về cú pháp nhưng chữ ký không còn xác thực payload; role thật của tài khoản vẫn là user. Chỉ biến đổi bản sao token làm dữ liệu âm, không biến nó thành TA.
- **TS (sửa chữ ký):** từ TA dạng `H.P.S`, giải mã S thành byte, XOR byte đầu với `0x01`, mã hóa lại base64url không padding thành S′; ghép `H.P.S′`. Giữ nguyên từng ký tự H/P, không ký lại. Cách đổi byte bảo đảm chữ ký thực sự khác, tránh chỉ đổi ký tự padding/bit không có ý nghĩa. Mỗi ca bắt đầu từ token gốc hợp lệ, không lấy TS từ TP.
- **C0:** không có danh mục. **C1:** chỉ một danh mục tên `T03 Mot`, ID ghi là `i1`. **C3:** đúng ba danh mục `T03 Mot`, `T03 Hai`, `T03 Ba`, ID tương ứng `i1/i2/i3`, khác nhau. Tất cả là fixture của người kiểm thử, không có sản phẩm tham chiếu. `i1/i2/i3` là ID thực từ fixture, không giả định bằng 1/2/3. C0/C1/C3 được chuẩn bị ngoài bước đang đánh giá và phải kiểm tra đúng trước ca.
- **CP:** dùng C3 và xác nhận tên mới của ca chưa tồn tại. Mỗi ca Create thành công khôi phục dữ liệu độc lập, đặc biệt `A`/`AB` phải chưa tồn tại. API role/validation cũng dùng CP, ID đích `i2` thuộc C3.
- `""` nghĩa là chuỗi rỗng/để trống ô; null là JSON null; `{}` là không có field name. Không nhập dấu backtick. API base theo S3: `http://localhost:3000`; JSON request có `Content-Type: application/json`.

## Steps và oracle dùng chung

**W-View:** mở tab Danh mục, quan sát ID/tên; tải lại trang, mở lại tab và đối chiếu tập danh mục với fixture. Không yêu cầu thứ tự hoặc đúng câu empty-state.

**W-Add(N):** ghi tập danh mục trước; nhập đúng N vào “Tên danh mục mới”; bấm **Thêm mới** một lần; quan sát phản hồi/danh sách; tải lại trang, mở lại Danh mục và đối chiếu trước–sau. Với chuỗi rỗng, xóa hết nội dung ô rồi submit. Nếu UI chặn thì chỉ credit validation Web, không suy ra server đã được kiểm tra.

**W-Delete(id):** ghi tập danh mục trước; chọn nút **Xóa** của đúng ID; nếu ứng dụng có dialog thì xác nhận; quan sát, tải lại trang và đối chiếu. Không yêu cầu ứng dụng phải có dialog vì S1 không quy định.

**A(method,path,header,body):** dùng TA đọc `GET /api/categories` ghi tập `(id,name)` trước; gửi đúng một request mục tiêu với method/path/header/body trong hàng TC; lưu phản hồi để đối chiếu; dùng TA GET lại và so sánh. Không gọi thao tác Web thay cho request mục tiêu. GET chỉ là quan sát phụ trợ, không có expected “guest bị cấm GET”.

**ADD-OK:** chấp nhận thêm; xuất hiện đúng một danh mục mới có ID riêng và tên đã nhập, xem lại được sau reload; danh mục cũ giữ nguyên. Nguồn R02/S1 + POST S3. Không suy ra uniqueness toàn hệ thống từ việc dùng tên mới.

**NAME-REJECT:** từ chối thêm, có phản hồi validation/thất bại; tập danh mục giữ nguyên, không có bản ghi tên rỗng/null phát sinh. Nguồn R03/S1. UI có thể chặn gửi request; API phải tự từ chối input mục tiêu. Không áp exact toast/mã HTTP 400/409/500.

**AUTH-REJECT:** phản hồi từ chối do thiếu xác thực/quyền; không trả kết quả hoàn tất thay đổi thành công, tập `(id,name)` giữ nguyên. Nguồn R06/R07/S2. Không dùng việc UI giấu nút làm bằng chứng quyền API; không ấn định 401 hay 403 khi S2 không quy định.

Với Web, persistence có thể đối chiếu bổ sung qua GET bằng TA hoặc đọc dữ liệu chỉ đọc nếu sẵn có; vẫn phải thao tác/quan sát trên Web như steps. Không lấy alert hoặc HTTP success đơn lẻ làm bằng chứng danh mục đã thêm/xóa. Không ghi Pass khi thiếu điểm quan sát cần thiết.

## A. Xem, thêm và validation tên

| TC ID | Technique | Rule / Domain / Boundary | Precondition | Input | Steps | Expected và nguồn |
| --- | --- | --- | --- | --- | --- | --- |
| CAT-TC01 | Domain | R01 / D01 | PA + C0 | View danh sách rỗng | W-View | Không có dòng danh mục, không giữ dữ liệu cũ hoặc báo lỗi tải chỉ vì danh sách rỗng. R01/S1, GET S3 |
| CAT-TC02 | Domain | R01 / D02 | PA + C1 | View danh mục `i1, T03 Mot` | W-View | Hiển thị đúng một danh mục với tên tương ứng; reload vẫn đúng C1. R01/S1 |
| CAT-TC03 | Domain | R01 / D03 | PA + C3 | View ba danh mục fixture | W-View | Đủ ba ID/tên đúng cặp, không thiếu/nhân đôi dòng, không áp thứ tự. R01/S1 |
| CAT-TC04 | Domain | R01,R02,R06,R07 / D04,D16 | PA + CP | N=`Đồ học tập T03` | W-Add(N) | ADD-OK; tên tiếng Việt hiển thị đúng sau reload. R02/S1; A02; token admin theo S2 |
| CAT-TC05 | Domain + BVA | R03 / D05 / B01-0 | PA + CP | N=`""`, L=0 | W-Add(N) | NAME-REJECT; biên dưới không hợp lệ. R03/S1 |
| CAT-TC06 | Domain + BVA | R02,R03 / D04 / B01-1 | PA + CP; tên `A` chưa có | N=`A`, L=1 | W-Add(N) | ADD-OK; một ký tự đã thỏa nonempty, không tự đặt min 2. R02–03/S1, A02 |
| CAT-TC07 | Domain + BVA | R02,R03 / D04 / B01-2 | PA + CP; tên `AB` chưa có | N=`AB`, L=2 | W-Add(N) | ADD-OK; hàng xóm hợp lệ phía trên biên 1. R02–03/S1, A02 |
| CAT-TC08 | Domain | R03 / D06 | P0 + CP + TA | POST `/api/categories`; `Authorization: Bearer <TA>`; body `{}` | A với input của hàng | NAME-REJECT; không có name vẫn vi phạm required dù JSON hợp lệ. R03/S1; body S3 |
| CAT-TC09 | Domain | R03 / D07 | P0 + CP + TA | POST `/api/categories`; `Authorization: Bearer <TA>`; body `{"name":null}` | A với input của hàng | NAME-REJECT; null không cung cấp một tên. R03/S1 |
| CAT-TC10 | Domain + BVA | R03 / D05 / B02-0 | P0 + CP + TA | POST `/api/categories`; `Authorization: Bearer <TA>`; body `{"name":""}` | A với input của hàng | NAME-REJECT ở server; không credit từ việc TC05 bị UI chặn. R03/S1 |

## B. Xóa và trạng thái dữ liệu

| TC ID | Technique | Rule / Domain | Precondition | Input | Steps | Expected và nguồn |
| --- | --- | --- | --- | --- | --- | --- |
| CAT-TC11 | Domain | R04,R06,R07 / D08,D16 | PA + C3, Ref(i2)=0 | Xóa `i2` (`T03 Hai`) | W-Delete(i2) | Chỉ i2 biến mất, i1/i3 và tên tương ứng giữ nguyên sau reload. R04/S1; path theo ID S3 |
| CAT-TC12 | Domain | R01,R04 / D09,D16 | PA + C1, Ref(i1)=0 | Xóa danh mục cuối `i1` | W-Delete(i1) | i1 bị xóa; danh sách rỗng sau reload, không còn dòng cũ. R01,R04/S1 |
| CAT-TC24 | Domain | R04 / D10 | P0 + C3 + TA; GET xác nhận ID `999999` vắng, nếu đã có phải chọn ID vắng khác và ghi lại | DELETE `/api/categories/999999`; `Authorization: Bearer <TA>`; không body | A, dùng đúng ID vắng đã xác nhận | Không xóa/đổi i1/i2/i3 hoặc tạo danh mục mới. Chỉ đánh giá invariant theo ID của R04/S3; status/message/idempotency chưa có oracle (Q05) |

## C. Quyền truy cập Web Admin

| TC ID | Technique | Rule / Domain | Precondition | Input | Steps | Expected và nguồn |
| --- | --- | --- | --- | --- | --- | --- |
| CAT-TC13 | Domain | R05 / D11 | P0 + C3; phiên trình duyệt mới không có adminToken | Guest mở `http://localhost:5174/` | Mở URL; thử tới tab Danh mục nếu giao diện cho phép; reload và kiểm tra lại | Không truy cập được màn hình quản lý danh mục/nút thao tác quản lý trong phân hệ Admin; có yêu cầu xác thực hoặc từ chối. Không áp một URL redirect cụ thể. R05/S2 |
| CAT-TC14 | Domain | R05 / D12 | P0 + C3; phiên mới; user demo tồn tại, đăng nhập được ở luồng bình thường | Email `test@eshop.com`, password `Test1234!` tại Admin Login | Mở Admin; nhập user hợp lệ, bấm Login một lần; thử mở Danh mục nếu có; reload kiểm tra lại | User thường không vào được phân hệ quản lý danh mục dù thông tin đăng nhập hợp lệ. Không đòi exact alert. R05/S2; identity là setup, không kiểm thử lockout FR-02 |
| CAT-TC33 | Domain | R05 / D19 | P0 + C3 + TU hợp lệ; phiên trình duyệt riêng không có token admin; dùng đúng origin `http://localhost:5174` | `localStorage` key `adminToken` chứa nguyên TU, không sửa payload | (1) Mở origin Admin và dùng DevTools ghi TU vào key `adminToken`. (2) Đóng tab, mở lại `http://localhost:5174/` trong cùng phiên để ứng dụng đọc token đã lưu. (3) Không submit Admin Login; thử mở Danh mục nếu giao diện cho phép. (4) Reload, kiểm tra quyền lại; GET bằng TA đối chiếu fixture nếu cần. | Không vào được phân hệ quản lý danh mục hoặc sử dụng nút quản lý với phiên user; phải yêu cầu tài khoản admin hoặc từ chối. Danh mục không đổi. Chỉ có response API bị chặn nhưng màn hình quản lý vẫn sử dụng được thì chưa đáp ứng oracle Web. Không yêu cầu xóa key/redirect cụ thể. R05/S2; key/điểm vào theo S4 |

## D. Quyền API của từng phương thức thay đổi dữ liệu

Mọi ca dưới dùng **P0 + CP**, `i2` tồn tại và Ref=0. TA được dùng riêng cho GET trước–sau theo A, không tự gửi TA kèm request âm. PUT dùng body name là dữ liệu đầu vào cụ thể theo cấu trúc POST và quan sát source; expected chỉ dựa điều kiện quyền S2, không nhận body này là contract Update đã được xác nhận.

| TC ID | Technique | Rule / Domain | Precondition bổ sung | Input request mục tiêu | Steps | Expected và nguồn |
| --- | --- | --- | --- | --- | --- | --- |
| CAT-TC15 | Domain | R06 / D13 | Không Authorization ở request mục tiêu | POST `/api/categories`; body `{"name":"T03 Moi"}` | A | AUTH-REJECT; không thêm `T03 Moi`. R06/S2 |
| CAT-TC16 | Domain | R06 / D13 | Không Authorization ở request mục tiêu | DELETE `/api/categories/<i2>`; không body | A | AUTH-REJECT; i2 vẫn tồn tại, tên cũ giữ nguyên. R06/S2 |
| CAT-TC17 | Domain | R06 / D13 | Không Authorization ở request mục tiêu | PUT `/api/categories/<i2>`; body `{"name":"T03 Doi"}` | A | AUTH-REJECT; i2 không bị đổi tên. Chỉ kiểm tra quyền PUT. R06/S2 |
| CAT-TC18 | Domain | R06 / D14 | Header `Authorization: Bearer not-a-jwt` | POST `/api/categories`; body `{"name":"T03 Moi"}` | A | AUTH-REJECT; không thêm `T03 Moi`. R06/S2 |
| CAT-TC19 | Domain | R06 / D14 | Header `Authorization: Bearer not-a-jwt` | DELETE `/api/categories/<i2>`; không body | A | AUTH-REJECT; i2 không bị xóa. R06/S2 |
| CAT-TC20 | Domain | R06 / D14 | Header `Authorization: Bearer not-a-jwt` | PUT `/api/categories/<i2>`; body `{"name":"T03 Doi"}` | A | AUTH-REJECT; i2 không bị đổi tên. R06/S2 |
| CAT-TC21 | Domain | R07 / D15 | TU hợp lệ role user; header `Authorization: Bearer <TU>` | POST `/api/categories`; body `{"name":"T03 Moi"}` | A | AUTH-REJECT; không thêm `T03 Moi` dù token hợp lệ. R07/S2 |
| CAT-TC22 | Domain | R07 / D15 | TU hợp lệ role user; header `Authorization: Bearer <TU>` | DELETE `/api/categories/<i2>`; không body | A | AUTH-REJECT; i2 không bị xóa. R07/S2 |
| CAT-TC23 | Domain | R07 / D15 | TU hợp lệ role user; header `Authorization: Bearer <TU>` | PUT `/api/categories/<i2>`; body `{"name":"T03 Doi"}` | A | AUTH-REJECT; i2 không bị đổi tên. R07/S2 |

## E. BVA API và token bị biến đổi — bổ sung v0.2

TC25–26 dùng TA, cùng biên tên 1 ký tự như Web; bộ API dài 0/1/2 là TC10/25/26. Các TC27–32 dùng **P0 + CP**, ID `i2` tồn tại, tên nhập hợp lệ. TP/TS là dữ liệu âm được chuẩn bị theo định nghĩa trên; request quan sát trước–sau vẫn dùng TA nguyên gốc. Với PUT, chỉ đánh giá xác thực theo R06, không credit nghiệp vụ Update. Các token không hợp lệ không được dùng để kiểm tra riêng R07 vì bước xác thực phải chặn trước.

| TC ID | Technique | Rule / Domain / Boundary | Precondition | Input | Steps | Expected và nguồn |
| --- | --- | --- | --- | --- | --- | --- |
| CAT-TC25 | Domain + BVA | R02,R03 / D04,D16 / B02-1 | P0 + CP + TA; tên `A` chưa có | POST `/api/categories`; `Authorization: Bearer <TA>`; body `{"name":"A"}`, L=1 | A với input của hàng | ADD-OK ở API; thêm đúng một tên `A`, danh mục cũ giữ nguyên. Tại L=1 phải chấp nhận. R02–03/S1, S3, A02 |
| CAT-TC26 | Domain + BVA | R02,R03 / D04,D16 / B02-2 | P0 + CP + TA; tên `AB` chưa có | POST `/api/categories`; `Authorization: Bearer <TA>`; body `{"name":"AB"}`, L=2 | A với input của hàng | ADD-OK ở API; thêm đúng một tên `AB`, danh mục cũ giữ nguyên. Hàng xóm hợp lệ phía trên biên. R02–03/S1, S3, A02 |
| CAT-TC27 | Domain | R06 / D17 | P0 + CP; TP sửa role payload TU, giữ chữ ký cũ | POST `/api/categories`; `Authorization: Bearer <TP>`; body `{"name":"T03 Moi"}` | Chuẩn bị TP từ TU hợp lệ; A với input của hàng | AUTH-REJECT; không thêm `T03 Moi`, không tin role admin trong payload đã sửa. R06/S2 |
| CAT-TC28 | Domain | R06 / D17 | P0 + CP; TP sửa role payload TU, giữ chữ ký cũ | DELETE `/api/categories/<i2>`; `Authorization: Bearer <TP>`; không body | Chuẩn bị TP từ TU hợp lệ; A với input của hàng | AUTH-REJECT; i2 không bị xóa, toàn bộ danh mục giữ nguyên. R06/S2 |
| CAT-TC29 | Domain | R06 / D17 | P0 + CP; TP sửa role payload TU, giữ chữ ký cũ | PUT `/api/categories/<i2>`; `Authorization: Bearer <TP>`; body `{"name":"T03 Doi"}` | Chuẩn bị TP từ TU hợp lệ; A với input của hàng | AUTH-REJECT; i2 không bị đổi tên. Chỉ kiểm tra xác thực PUT. R06/S2 |
| CAT-TC30 | Domain | R06 / D18 | P0 + CP; TS chỉ sửa byte chữ ký TA, payload admin giữ nguyên | POST `/api/categories`; `Authorization: Bearer <TS>`; body `{"name":"T03 Moi"}` | Chuẩn bị TS từ TA hợp lệ; A với input của hàng | AUTH-REJECT; không thêm `T03 Moi` dù payload vẫn ghi admin. R06/S2 |
| CAT-TC31 | Domain | R06 / D18 | P0 + CP; TS chỉ sửa byte chữ ký TA, payload admin giữ nguyên | DELETE `/api/categories/<i2>`; `Authorization: Bearer <TS>`; không body | Chuẩn bị TS từ TA hợp lệ; A với input của hàng | AUTH-REJECT; i2 không bị xóa, toàn bộ danh mục giữ nguyên. R06/S2 |
| CAT-TC32 | Domain | R06 / D18 | P0 + CP; TS chỉ sửa byte chữ ký TA, payload admin giữ nguyên | PUT `/api/categories/<i2>`; `Authorization: Bearer <TS>`; body `{"name":"T03 Doi"}` | Chuẩn bị TS từ TA hợp lệ; A với input của hàng | AUTH-REJECT; i2 không bị đổi tên. Chỉ kiểm tra xác thực PUT. R06/S2 |

## Kiểm tra thiết kế

**33 ID unique, TC01–TC33**: 27 Domain và 6 Domain + BVA (TC05–07,10,25,26), không cộng đôi. TC24/33 đặt cùng nhóm Xóa/Web để dễ đọc. Giữ nguyên input/steps/expected của TC01–24; TC10 chỉ thêm nhãn BVA và B02-0. Truy vết 7 rules, 19 mục tiêu miền, 6 items BVA theo lớp và 15 tổ hợp quyền API âm ở [design.md §6](design.md#6-bước-4--hoàn-thiện-tc-và-tự-kiểm-tra-thiết-kế). Q01–Q06 là giới hạn đặc tả/phạm vi, không phải việc bắt buộc Vỹ phải quyết định thêm để hoàn tất bộ TC; chưa tự chốt policy tên trùng/whitespace/max/xóa danh mục có sản phẩm. Vỹ đã review và yêu cầu commit hai file. Tất cả Not Run; không có Actual, Pass/Fail hoặc kết luận lỗi.
