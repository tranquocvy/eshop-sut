# Mobile Account Registration — bộ test case Domain/BVA

**Design v0.3 — 20/10/2026 (UTC+7) — Vỹ đã review toàn bộ.** Toàn bộ **54 TC: Not Run**. Test basis, quy ước S7 và phạm vi tại [design.md](design.md). Không có kết quả chạy trong tài liệu này.

## Quy ước dữ liệu và điều kiện trước

- Mọi ID rút gọn R/D/B trong bảng có prefix `MR-`. `TC01` nghĩa là `MR-TC01`.
- **P0:** người dùng chưa đăng nhập; form native Đăng ký mở được; backend kết nối được; dữ liệu của ca độc lập. Kiểm tra E mới trước ca. Không reset backend trong một sequence.
- **C-guard:** chỉ TC34–37 yêu cầu field Confirmation thật sự tồn tại và nhập được. Nếu thiếu, giữ TC và ghi không thể tới rule equality khi thực thi; không giả lập field hay gửi C qua API. TC33 tự kiểm tra sự tồn tại của field, không yêu cầu C-guard.
- **Dữ liệu mặc định:** N=`Nguyen Van A`; P=`Abcde1!x`; E của TC số NN là **`mr.t02r01.tcNN@example.com`**, ví dụ TC01=`mr.t02r01.tc01@example.com`, TC40=`mr.t02r01.tc40@example.com`. Mỗi TC dùng đúng E riêng, trừ override trong bảng. `t02r01` là namespace dữ liệu cụ thể cho lần chạy đầu; khi rerun thay token đồng nhất và ghi lại token thật. Chưa tạo các account này trong lượt thiết kế.
- **C mặc định:** nếu UI có field thì nhập đúng bằng P; nếu UI thiếu field, các TC kiểm tra N/E/P vẫn đánh giá rule riêng của chúng và ghi giới hạn form. Không credit R10 từ những ca đó. C-guard áp dụng riêng khi TC nhắm trực tiếp vào nhập/so sánh C.
- `""` là để trống; backtick chứa space là ký tự cần nhập thật, không phải dấu phân cách. Các password ASCII trong bảng là chuỗi literal, không gõ dấu backtick.
- **Quy ước theo review S7:** tên toàn whitespace bị từ chối; Ecanon là email sau bỏ whitespace đầu/cuối, validation/lưu/uniqueness dùng Ecanon và so sánh có phân biệt hoa/thường. Password đếm Unicode code point; special là dấu/ký hiệu Unicode P*/S*, không tính whitespace. Không trim password và không tự cấm mọi space khi P đã có special hợp lệ. Giữ nguyên input có space để ứng dụng tự xử lý, không trim trước bằng tool.

## Bước dùng chung và oracle

**S:** (1) Từ Home → Đăng nhập → Đăng ký ngay. (2) Điền N/E/P đúng dữ liệu của ca, C=P nếu có field; override C khi ca chỉ định. (3) Bấm Đăng ký **một lần**; quan sát phản hồi, đóng alert nếu cần để xác định màn hình đích. (4) Dùng quan sát dữ liệu **chỉ đọc** trên database runtime để đối chiếu account count/name/email trước–sau. Đây là phép quan sát phụ trợ; không thay bước submit native bằng API. Nếu không quan sát được persistence thì ghi giới hạn, không suy ra từ alert.

**ACCEPT:** dữ liệu thỏa các rule đang kiểm tra được chấp nhận, tạo đúng 1 account mới với name tương ứng và email Ecanon sau trim, chuyển tới màn hình Đăng nhập. Nguồn: FR-01/R11 cùng các rule đầu vào đã dẫn; quy ước trim/case/Unicode từ review S7; S3 chỉ bổ trợ contract success API. Không đòi một câu toast/id cố định. Không tính ACCEPT của ca N/E/P là đã kiểm tra C.

**REJECT:** không báo đăng ký thành công, có phản hồi validation/thất bại, không tạo account mới cho lần nhập invalid; không chuyển sang đăng nhập như một đăng ký thành công. Nguồn: rule bị vi phạm trong FR-01. Không áp đặt thứ tự lỗi, exact message hoặc HTTP 400/409 khi chưa được đặc tả. Với duplicate, so count theo email trước–sau không tăng và account cũ giữ nguyên.

Các kiểm tra count không so tổng account của cả DB khi có hoạt động khác; dùng namespace/Ecanon của ca và phép so sánh case-sensitive đã chốt. P chỉ là dữ liệu giả, không cần đọc/lưu mật khẩu từ DB để đối chiếu. Các expected bổ sung do review phải dẫn S7, không gán thành nội dung README đã ghi rõ.

## A. Required fields và miền email

Các ca dùng P0 và S, trừ nội dung thay đổi được ghi rõ. Các trường không nêu trong input giữ mặc định bên trên, nên mỗi hàng xác định một bộ dữ liệu đầy đủ.

| TC ID | Technique | Rule / Domain / Boundary | Precondition | Input cụ thể (override mặc định) | Steps | Expected và nguồn |
| --- | --- | --- | --- | --- | --- | --- |
| MR-TC01 | Domain | R01–09,R11; D02,D03 | P0; E01 mới | Bộ mặc định của TC01 | S | ACCEPT. Control cho bộ dữ liệu hợp lệ; S1 FR-01 dòng 32–36, S2. Không credit R10 |
| MR-TC02 | Domain+BVA | R01; D01; B06-0 | P0; E02 mới | N=`""` (0 ký tự) | S | REJECT vì thiếu Họ Tên; R01/S1:32 |
| MR-TC03 | Domain+BVA | R01; D02; B06-1 | P0; E03 mới; A01 | N=`V` (1 ký tự) | S | ACCEPT với tên nonempty; R01,R11/S1:32,36; A01 chưa có min tên khác |
| MR-TC04 | Domain+BVA | R01; D02; B06-2 | P0; E04 mới; A01 | N=`Vy` (2 ký tự) | S | ACCEPT; R01,R11/S1:32,36 và A01 |
| MR-TC05 | Domain | R01; D02 | P0; E05 mới; A01 | N=`Trần Quốc Vỹ` | S | ACCEPT; tên được cung cấp và không có rule ASCII-only; R01,R11/S1:32,36 và A01 |
| MR-TC06 | Domain | R02; D04 | P0; N/P hợp lệ | E=`""` | S | REJECT vì thiếu Email; R02/S1:32–33 |
| MR-TC07 | Domain | R02; D05 | P0; chuỗi E chưa tồn tại | E=`mr.t02r01.tc07.example.com` | S | REJECT vì thiếu `@`; R02/S1:33 |
| MR-TC08 | Domain | R02; D06 | P0; chuỗi E chưa tồn tại | E=`@example.com` | S | REJECT vì thiếu local-part; R02/S1:33 |
| MR-TC09 | Domain | R02; D07 | P0; chuỗi E chưa tồn tại | E=`mr.t02r01.tc09@` | S | REJECT vì thiếu domain; R02/S1:33 |
| MR-TC10 | Domain | R02; D08 | P0; chuỗi E chưa tồn tại | E=`mr t02r01.tc10@example.com` (space sau `mr`) | S | REJECT vì space trong local-part không quote của địa chỉ đơn giản; R02/S1:33; không xét trim |
| MR-TC11 | Domain | R02; D09 | P0; chuỗi E chưa tồn tại | E=`mr.t02r01.tc11@@example.com` | S | REJECT vì hai `@` liên tiếp, không quote; R02/S1:33 |
| MR-TC12 | Domain | R03; D10 | P0; xác nhận `test@eshop.com` tồn tại theo fixture; ghi count trước ca | E=`test@eshop.com`; N/P nominal | S | REJECT duplicate nguyên chuỗi; account count của E không tăng, dữ liệu account cũ không đổi; R03/S1:33; fixture từ README:24 |
| MR-TC13 | Domain (state) | R03,R11; D03,D11 | P0; E13 chưa tồn tại | Cả hai submit dùng E13, N/P nominal | S lần 1 → quay lại form native → nhập lại cùng dữ liệu → S bước 3–4 lần 2 | Lần 1 ACCEPT, lần 2 REJECT duplicate; sau hai submit chỉ có 1 account E13; R03,R11/S1:33,36 |

## B. Miền và biên password

Các ca đều dùng N nominal, E riêng mới. C=P nếu có field; chữ/số/`!` đều ASCII. Trừ TC14, mỗi ca invalid chỉ vi phạm **một** điều kiện password để có thể quan sát rule mục tiêu.

| TC ID | Technique | Rule / Domain / Boundary | Precondition | Input cụ thể (P override) | Steps | Expected và nguồn |
| --- | --- | --- | --- | --- | --- | --- |
| MR-TC14 | Domain | R04; D12 | P0; E14 mới | P=`""` | S | REJECT thiếu password; R04/S1:32. Không dùng ca này credit từng rule class count |
| MR-TC15 | Domain+BVA | R05; D13; B01-7 | P0; E15 mới | P=`Abcde1!` (7) | S | REJECT vì 7<8, các nhóm ký tự khác đủ; R05/S1:34 |
| MR-TC16 | Domain+BVA | R05–09,R11; D14,D16,D20,D22; B01-8,B02-1,B04-1,B05-1 | P0; E16 mới | P=`Abcde1!x` (8; U1,L5,D1,S1) | S | ACCEPT tại ngưỡng 8, đúng một hoa/số/S; R05–09,R11/S1:34,36 |
| MR-TC17 | Domain+BVA | R05; D14; B01-9 | P0; E17 mới | P=`Abcde1!xy` (9) | S | ACCEPT phía trên ngưỡng, không chỉ đúng 8 mới được chấp nhận; R05,R11/S1:34,36 |
| MR-TC18 | Domain+BVA | R06; D15; B02-0 | P0; E18 mới | P=`abcde1!x` (8; U0,L6,D1,S1) | S | REJECT chỉ vì thiếu chữ hoa; R06/S1:34 |
| MR-TC19 | Domain+BVA | R06; D16; B02-2 | P0; E19 mới | P=`ABcde1!x` (8; U2,L4,D1,S1) | S | ACCEPT với 2 chữ hoa; R06,R11/S1:34,36 |
| MR-TC20 | Domain+BVA | R07; D17; B03-0 | P0; E20 mới | P=`ABCDE1!X` (8; U6,L0,D1,S1) | S | REJECT chỉ vì thiếu chữ thường; R07/S1:34 |
| MR-TC21 | Domain+BVA | R07; D18; B03-1 | P0; E21 mới | P=`ABCDa1!X` (8; U5,L1,D1,S1) | S | ACCEPT đúng 1 chữ thường; R07,R11/S1:34,36 |
| MR-TC22 | Domain+BVA | R07; D18; B03-2 | P0; E22 mới | P=`ABCDab1!` (8; U4,L2,D1,S1) | S | ACCEPT với 2 chữ thường; R07,R11/S1:34,36 |
| MR-TC23 | Domain+BVA | R08; D19; B04-0 | P0; E23 mới | P=`Abcdef!x` (8; U1,L6,D0,S1) | S | REJECT chỉ vì thiếu chữ số; R08/S1:34 |
| MR-TC24 | Domain+BVA | R08; D20; B04-2 | P0; E24 mới | P=`Abcde12!` (8; U1,L4,D2,S1) | S | ACCEPT với 2 chữ số; R08,R11/S1:34,36 |
| MR-TC25 | Domain+BVA | R09; D21; B05-0 | P0; E25 mới | P=`Abcde12x` (8; U1,L5,D2,S0; chỉ alphanumeric) | S | REJECT vì hoàn toàn thiếu special; R09/S1:34 |
| MR-TC26 | Domain+BVA | R09; D22; B05-2 | P0; E26 mới | P=`Abcde1!!` (8; U1,L4,D1,S2) | S | ACCEPT với 2 special `!`; R09,R11/S1:34,36 |
| MR-TC27 | Domain (membership) | R09; D22 | P0; E27 mới | P=`Abcde1@x` | S | ACCEPT với `@` là special duy nhất; R09,R11/S1:34,36 |
| MR-TC28 | Domain (membership) | R09; D22 | P0; E28 mới | P=`Abcde1$x` | S | ACCEPT với `$` là special duy nhất; R09,R11/S1:34,36 |
| MR-TC29 | Domain (membership) | R09; D22 | P0; E29 mới | P=`Abcde1%x` | S | ACCEPT với `%` là special duy nhất; R09,R11/S1:34,36 |
| MR-TC30 | Domain (membership) | R09; D22 | P0; E30 mới | P=`Abcde1*x` | S | ACCEPT với `*` là special duy nhất; R09,R11/S1:34,36 |
| MR-TC31 | Domain (membership) | R09; D22 | P0; E31 mới | P=`Abcde1?x` | S | ACCEPT với `?` là special duy nhất; R09,R11/S1:34,36 |
| MR-TC32 | Domain (membership) | R09; D22 | P0; E32 mới | P=`Abcde1&x` | S | ACCEPT với `&` là special duy nhất; R09,R11/S1:34,36 |

Ký hiệu `!` được thử riêng ở TC16; TC27–32 bổ sung sáu thành viên còn lại. Không nhân thêm BVA TC chỉ vì đổi special khi count/biên mục tiêu không đổi.

## C. Confirmation và tương tác trạng thái

| TC ID | Technique | Rule / Domain / Boundary | Precondition | Input cụ thể | Steps | Expected và nguồn |
| --- | --- | --- | --- | --- | --- | --- |
| MR-TC33 | Domain (form schema) | R10; D23 | P0; không cần C-guard | Không submit; form ban đầu | S bước 1, quan sát đủ form và scroll nếu cần để tìm Confirmation | Có trường Xác nhận mật khẩu, nhập được độc lập với P. Không suy chỉ từ một viewport; R10/S1:35 |
| MR-TC34 | Domain | R10; D24 | P0 + C-guard; E34 mới | N/E34/P nominal; C=`""` | S, để trống C | REJECT vì không khớp với P nonempty; R10/S1:35. Nếu không có field thì không thực hiện được ca equality này |
| MR-TC35 | Domain | R10; D26 | P0 + C-guard; E35 mới | P=`Abcde1!x`, C=`Abcde1!y` (đều 8, khác ký tự cuối) | S | REJECT dù hai chuỗi cùng độ dài; R10/S1:35 |
| MR-TC36 | Domain | R10; D27 | P0 + C-guard; E36 mới | P=`Abcde1!x`, C=`Abcde1!` (7, là prefix của P) | S | REJECT vì không bằng nhau; R10/S1:35, không gán minimum length riêng cho C |
| MR-TC37 | Domain | R10,R11; D25 | P0 + C-guard; E37 mới | P=C=`Abcde1!x`, N/E37 nominal | S, nhập C thật rồi submit | ACCEPT và chuyển sang Đăng nhập; R10,R11/S1:35–36; đây mới là control trực tiếp của confirmation |
| MR-TC38 | Domain (state) | R05,R03,R11; D13,D14,D28 | P0; E38 mới; giữ nguyên DB giữa hai submit | Lần 1 P=`Abcde1!` (7); lần 2 sửa P=`Abcde1!x` (8); cùng N/E38; sửa C theo P nếu có | S với P7 → kiểm tra không có account E38 → sửa P/C trên form → submit một lần nữa → quan sát dữ liệu/màn hình | Lần 1 REJECT, E38 chưa được tạo; lần 2 ACCEPT; cuối sequence có đúng 1 account E38. R05,R03,R11/S1:33–36 |
| MR-TC39 | Domain (interaction) | R03,R06; D10,D15,D29 | P0; `test@eshop.com` tồn tại; ghi count/dữ liệu trước ca | E=`test@eshop.com`, P=`abcde1!x` (thiếu hoa), N nominal | S | REJECT, không thêm/sửa account đã tồn tại. Bất kỳ rule invalid nào được thông báo trước đều được; không credit đã tới check uniqueness nếu password chặn trước. R03,R06/S1:33–34 |
| MR-TC40 | Domain (interior sample) | R05–09,R11; D14 | P0; E40 mới | P=`Ab1!Ab1!Ab1!Ab1!Ab1!Ab1!Ab1!Ab1!Ab1!Ab1!Ab1!Ab1!Ab1!Ab1!Ab1!Ab1!` (64 = `Ab1!` ×16); C=P nếu có | S | ACCEPT; thỏa ngưỡng tối thiểu và đủ nhóm ký tự, chưa có max được công bố; R05–09,R11/S1:34,36. Đây là điểm dài đại diện, không phải biên trên |

## D. Các TC đã chốt expected qua review của Vỹ

TC41–46 ban đầu là conditional; nay đã có expected theo S7. Đây là các quy ước review bổ sung vào phần README chưa diễn đạt đủ, không phải bằng chứng đã chạy test hoặc đã có lỗi runtime.

| TC ID | Technique | Rule / Domain / Boundary | Precondition | Input cụ thể | Steps | Expected và nguồn review |
| --- | --- | --- | --- | --- | --- | --- |
| MR-TC41 | Domain | R01; D30; Q01 | P0; E41 mới | N=` ` (1 space), E41/P nominal | S, nhập đúng 1 space, không tự trim trước bằng tool | REJECT vì tên sau trim rỗng; R01/S1:32 và review S7/Q01 |
| MR-TC42 | Domain | R03; D31; Q02 | P0; `test@eshop.com` tồn tại; `TEST@eshop.com` chưa có nguyên chuỗi | E=`TEST@eshop.com`, N/P nominal | S, giữ đúng case; quan sát hai email theo so sánh phân biệt case | ACCEPT tạo đúng 1 account `TEST@eshop.com`, account `test@eshop.com` cũ giữ nguyên. Email khác case là hai chuỗi khác theo review S7/Q02; R03/S1:33 |
| MR-TC43 | Domain | R02–03; D32; Q03 | P0; E43 canonical và chuỗi có space đều chưa tồn tại | E=` mr.t02r01.tc43@example.com ` (1 space đầu/cuối), N/P nominal | S, nhập cả space; kiểm tra Ecanon và chuỗi nguyên nhập sau submit | ACCEPT, chỉ tạo account với email `mr.t02r01.tc43@example.com` đã trim; không lưu email có space. R02–03/S1:33 và review S7/Q03 |
| MR-TC44 | Domain | R09; D33; Q04 | P0; E44 mới | P=`Abcde1#x` (8 code point, special duy nhất `#`) | S | ACCEPT vì `#` là dấu Unicode thuộc Punctuation; R09/S1:34 và review S7/Q04, không giới hạn special trong S0 |
| MR-TC45 | Domain | R09; D34; Q04 | P0; E45 mới | P=`Abcde1 x` (8 code point, 1 space giữa `1` và `x`, không có dấu/ký hiệu) | S, không thay space bằng `!` | REJECT vì space không đáp ứng yêu cầu special; các nhóm khác và độ dài vẫn hợp lệ. R09/S1:34 và review S7/Q04 |
| MR-TC46 | Domain+BVA | R05; D13,D35; B01-7; Q05 | P0; E46 mới; nhập được emoji nguyên vẹn | P=`Abc1!😀d` (7 code point, 8 UTF-16 unit), C=P nếu có | S, giữ nguyên chuỗi Unicode | REJECT vì 7<8 code point, dù đủ 8 UTF-16 unit. Có đủ hoa/thường/số/special. Ngưỡng R05/S1:34 và đơn vị review S7/Q05 |

## E. Unicode và tương tác dữ liệu

TC47–54 kiểm tra độ dài Unicode, các nhóm special mở rộng, uniqueness sau trim và password chứa cả space/special. Các ca áp dụng cùng quy ước đã chốt; không tăng ngưỡng hay giới hạn nghiệp vụ.

| TC ID | Technique | Rule / Domain / Boundary | Precondition | Input cụ thể | Steps | Expected và nguồn |
| --- | --- | --- | --- | --- | --- | --- |
| MR-TC47 | Domain+BVA | R05; D14,D35; B01-8; Q05 | P0; E47 mới; nhập được emoji nguyên vẹn | P=`Abc1!😀de` (8 code point, 9 UTF-16 unit), C=P nếu có | S, giữ nguyên chuỗi Unicode | ACCEPT tại ngưỡng 8 code point, đủ các nhóm ký tự. R05,R11/S1:34,36 và review S7/Q05 |
| MR-TC48 | Domain+BVA | R05; D14,D35; B01-9; Q05 | P0; E48 mới; nhập được emoji nguyên vẹn | P=`Abc1!😀def` (9 code point, 10 UTF-16 unit), C=P nếu có | S, giữ nguyên chuỗi Unicode | ACCEPT phía trên ngưỡng; không chỉ chấp nhận đúng 8. R05,R11/S1:34,36 và review S7/Q05 |
| MR-TC49 | Domain (membership) | R09; D33; Q04 | P0; E49 mới | P=`Abcde1_x` (8 code point, special duy nhất `_`) | S | ACCEPT vì `_` thuộc Punctuation; R09,R11/S1:34,36 và review S7/Q04 |
| MR-TC50 | Domain (membership) | R05,R09; D33; Q04 | P0; E50 mới; nhập được emoji nguyên vẹn | P=`Abcdef1😀` (8 code point, special duy nhất `😀`) | S, giữ nguyên emoji | ACCEPT vì emoji này thuộc Symbol; có đủ hoa/thường/số, đủ 8 code point. R05,R09,R11/S1:34,36 và review S7/Q04–05 |
| MR-TC51 | Domain (membership) | R09; D33; Q04 | P0; E51 mới | P=`Abcde1—x` (8 code point, special duy nhất là em dash `—`, không phải dấu trừ) | S | ACCEPT vì `—` thuộc Punctuation; R09,R11/S1:34,36 và review S7/Q04 |
| MR-TC52 | Domain (membership) | R09; D33; Q04 | P0; E52 mới | P=`Abcde1€x` (8 code point, special duy nhất `€`) | S | ACCEPT vì `€` thuộc Symbol; R09,R11/S1:34,36 và review S7/Q04 |
| MR-TC53 | Domain (interaction) | R02–03; D36; Q03 | P0; `test@eshop.com` đã tồn tại; ghi count/dữ liệu trước ca | E=` test@eshop.com ` (1 space đầu/cuối), N/P nominal | S, không trim trước bằng tool; quan sát cả Ecanon và chuỗi có space | REJECT vì sau trim email trùng `test@eshop.com`; không tạo account mới ở cả hai dạng và không sửa account cũ. R03/S1:33 và review S7/Q02–03 |
| MR-TC54 | Domain (interaction) | R05,R09; D37; Q04 | P0; E54 mới | P=`Abc1! xy` (8 code point, có `!` và 1 space sau `!`), C=P nếu có | S, giữ đúng space trong P; không trim password | ACCEPT vì `!` thỏa special, space không bị dùng để thay special và chưa có rule cấm mọi space. R05,R09,R11/S1:34,36 và cách áp dụng review S7/Q04 |

## Bàn giao thiết kế

- **54 unique TC**, có expected theo requirement và quy ước review S7; không còn TC conditional ở Q01–05. TC34–37 có C-guard; giữ chúng khi form chưa đáp ứng schema. Không đổi rule từ README thành nguồn của các quy ước bổ sung.
- **18 TC Domain+BVA:** 02,03,04,15,16,17,18,19,20,21,22,23,24,25,26,46,47,48. Ánh xạ vào 18 boundary items; 3 ca Unicode hiện thực lại B01, không tạo thêm items và không đếm đôi TC.
- Tất cả **Not Run**. Vỹ đã review toàn bộ hai file thiết kế và bộ 54 TC. Không có actual, evidence hay kết luận lỗi. Bản AI v0.1 và snapshot v0.2 được giữ ngoài repo để đối chiếu.
