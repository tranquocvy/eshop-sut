# Mobile Account Registration — thiết kế Domain Testing và BVA

Phiên bản **design v0.3**, ngày 20/10/2026 (UTC+7). Vỹ đã review toàn bộ hai file thiết kế và bộ 54 TC. Các quy ước bổ sung được ghi riêng với yêu cầu gốc. Toàn bộ TC **Not Run**; chưa có kết quả thực thi. Bản AI v0.1 và bản v0.2 được giữ ngoài repo để đối chiếu.

## 1. Test basis và phạm vi

Feature Pool D: **Đăng ký tài khoản trên Mobile**, thuộc FR-20 và áp dụng quy tắc FR-01. Target là giao diện **native React Native**; Android là môi trường đã chuẩn bị. Các TC không thay thao tác Mobile bằng request API. Đọc API/source chỉ để hiểu luồng và khả năng quan sát.

Baseline source: `8018b73e9e0d9066efdb1ffe3512303e033a6cb4`; source SUT tại baseline này trùng `85af3ba`. Bộ thiết kế gồm file này và [test-cases.md](test-cases.md).

| Mã nguồn | Tài liệu và vị trí | Dùng cho |
| --- | --- | --- |
| S1 | [README — FR-01](../../../README.md#fr-01-đăng-ký-tài-khoản), dòng 30–36 | Required fields, email, password, confirmation, chuyển sang đăng nhập |
| S2 | [README — FR-20](../../../README.md#fr-20-tính-năng-mobile), dòng 233–235 | Áp dụng đăng ký tài khoản trên Mobile |
| S3 | [API specification — §1.1](../../../api_specification.md), dòng 11–21 | `POST /api/register`, body `name/email/password`, success 200 có message/id; không đặc tả error code |
| S4 | [App.js](../../../frontend-mobile/App.js), state dòng 42–46, handler 209–240, form 797–837; [server.js](../../../backend/server.js) 20–30; [database.js](../../../backend/database.js) 48–61 | Luồng nhập/submit, quan sát và rủi ro; **không dùng làm expected nghiệp vụ** |
| S5 | [Tài liệu tự học CTFL của môn](<../../../../../HW01/ISTQB Foundation Level (CTFL v4.0.1).pdf>), trang PDF 43–44; [bản web của giảng viên](https://www.fit.hcmus.edu.vn/~lqvu/Courses/SoftwareTesting/istqb-foundation-selfstudy.html#sec-4-3) | EP và cách chọn BVA quanh biên của partition hợp lệ |
| S6 | Cem Kaner, [Teaching Domain Testing: A Status Report](https://www.kaner.com/pdfs/domain_testing_cseet.pdf), §2; [reference Domain của skill](../../../skills/domain-bva-testing/references/domain-testing.md) | Mô hình miền, chọn đại diện, giữ biến khác hợp lệ và xem xét tương tác |
| S7 | Các quy ước thiết kế đã được review ngày 20/10/2026 | Tên nonempty, tên toàn space bị từ chối, email trim + phân biệt case, special Unicode không tính whitespace và độ dài theo code point. Đây là quy ước bổ sung, không tự gán thành câu chữ sẵn có trong README |

`method_profile`: **Domain = reference-provisional** (nguồn S6; chưa có bài giảng Domain riêng). **BVA = lecture-aligned với tài liệu tự học S5, trang 44**, quy ước `course-guide-3-value`: biên hợp lệ `b` và `b−δ`, `b+δ`. Đây là lựa chọn đã chốt ở T01, không tự nhận thứ tự bước của skill là quy trình chính thức của giảng viên. Không dùng helper `istqb-3` vì profile đó tạo tập điểm khác.

Không bao gồm đăng nhập/lockout FR-02 như một feature riêng, profile, reset password, toàn bộ GUI/security audit hoặc đăng ký trực tiếp bằng API. Sau đăng ký chỉ kiểm tra chuyển đến màn hình đăng nhập; không kiểm tra bộ đếm login. Bộ này chưa đánh dấu T02 hoàn tất toàn chu trình trong plan.

## 2. Bước 0 — Trích rule và xử lý chỗ chưa rõ

Bảng dưới đây tách nguồn quy tắc gốc S1/S2 khỏi **quy ước bổ sung qua review S7**. Các kết quả reject/accept được suy ra theo nguồn tương ứng; không chốt câu thông báo hay HTTP error code mà đặc tả chưa quy định. Việc Vỹ chốt policy giúp bộ test có oracle rõ, không biến policy đó thành câu chữ có sẵn trong README.

| Rule | Điều kiện đúng | Nguồn |
| --- | --- | --- |
| MR-R01 | Phải cung cấp Họ Tên; khi kiểm tra required, tên sau bỏ khoảng trắng đầu/cuối phải nonempty; chưa thêm min/max hoặc restriction khác | Required: S1 dòng 32; cách hiểu tên/whitespace: S7 |
| MR-R02 | Phải cung cấp Email có định dạng hợp lệ; bỏ khoảng trắng đầu/cuối trước validation và dùng email đã bỏ space làm giá trị lưu/so sánh | Required/format: S1 dòng 32–33; trim: S7 |
| MR-R03 | Email là duy nhất; so sánh email sau trim có phân biệt hoa/thường. Không tạo thêm tài khoản trùng nguyên chuỗi đã chuẩn hóa này | Uniqueness: S1 dòng 33; case/trim: S7 |
| MR-R04 | Phải cung cấp Mật khẩu | S1 dòng 32 |
| MR-R05 | Mật khẩu dài ít nhất 8 Unicode code point; không dùng số UTF-16 unit làm độ dài | Ngưỡng 8: S1 dòng 34; đơn vị: S7 |
| MR-R06 | Mật khẩu có ít nhất 1 chữ hoa | S1 dòng 34 |
| MR-R07 | Mật khẩu có ít nhất 1 chữ thường | S1 dòng 34 |
| MR-R08 | Mật khẩu có ít nhất 1 chữ số | S1 dòng 34 |
| MR-R09 | Mật khẩu có ít nhất 1 dấu/ký hiệu Unicode; áp dụng các nhóm Unicode Punctuation hoặc Symbol (`P*`/`S*`), không tính whitespace. Tập `S0={@,$,!,%,*,?,&}` là các ví dụ trong README, không phải allow-list đầy đủ | Yêu cầu special và S0: S1 dòng 34; mở rộng special/không tính whitespace: S7 |
| MR-R10 | Có trường Xác nhận mật khẩu; từ chối khi confirmation không khớp password | S1 dòng 35 |
| MR-R11 | Đăng ký thành công chuyển người dùng tới màn hình Đăng nhập | S1 dòng 36 |

### Giả định và quy ước thiết kế

| ID | Loại | Cách xử lý trong thiết kế |
| --- | --- | --- |
| A01 | Đã được Vỹ đồng ý khi review, S7 | Tên phải có nội dung non-whitespace, chưa thêm restriction khác. Giữ expected ACCEPT cho `V`, `Vy`, `Trần Quốc Vỹ`; giữ biên tên 0/1/2. Không tự yêu cầu ít nhất 2 ký tự hoặc nhiều từ. |
| A02 | Assumption về điểm vào | Người dùng chưa đăng nhập, kết nối bình thường, submit tuần tự; account state độc lập giữa TC. Không giả định reset backend là một bước vô hại. |
| A03 | Phạm vi dữ liệu kiểm soát | Các điểm BVA ASCII giữ nguyên vì độ dài code point/UTF-16 unit/byte bằng nhau ở mẫu ASCII. TC46–48 bổ sung 7/8/9 code point có emoji để phân biệt cách đếm. Các class chữ hoa/thường/số đang lấy mẫu bằng ASCII; review chưa định nghĩa toàn bộ class chữ/số Unicode. |
| Q01 | Đã chốt qua review, S7 | Tên chỉ có khoảng trắng là chưa cung cấp tên: REJECT ở TC41. Chuỗi có space không bằng chuỗi rỗng theo nghĩa literal; phép kiểm tra required xét nội dung sau trim. Chưa yêu cầu trim giá trị tên được lưu nếu tên có nội dung. |
| Q02 | Đã chốt qua review, S7 | Email có phân biệt hoa/thường khi so sánh uniqueness sau trim. TC42 dùng local-part khác case: ACCEPT nếu chuỗi mới chưa tồn tại. |
| Q03 | Đã chốt qua review, S7 | Bỏ space đầu/cuối email rồi validate/lưu/kiểm tra uniqueness. TC43 ACCEPT email mới sau trim; TC53 REJECT nếu sau trim trùng email cũ. Space bên trong vẫn invalid ở TC10. |
| Q04 | Đã chốt qua review, S7 | Special gồm dấu/ký hiệu Unicode, mô hình hóa bằng các category P*/S*. `#`, `_`, `—`, `€`, `😀` là các điểm bổ sung; whitespace không được dùng để thỏa điều kiện special. Không có quy tắc cấm space trong password vốn đã có special hợp lệ; TC54 kiểm tra sự khác biệt này. |
| Q05 | Đã chốt qua review, S7 | Độ dài tính bằng Unicode code point. Emoji `😀` đơn là 1 code point; không tự normalize Unicode trước đếm. `Abc1!😀d` là 7 nên REJECT; TC47–48 có 8/9 code point nên ACCEPT. |
| Q06 | Quy ước phạm vi thiết kế | Không thêm max nghiệp vụ khi đặc tả không đặt max; các chuỗi dài như password 64 là điểm đại diện, không phải giới hạn trên. Email lấy mẫu theo dạng thông dụng và các lỗi định dạng rõ ràng, chưa nhận hỗ trợ toàn bộ IDN/quoted email. Password đếm nguyên chuỗi code point, không tự normalize; class hoa/thường/số lấy mẫu ASCII. Không công bố coverage cho mọi độ dài, email hoặc chữ/số Unicode. Minimum tên non-whitespace và minimum password 8 đã được xác định. |

TC41–46 có expected theo S7; TC47–54 bổ sung các miền/biên Unicode và tương tác dữ liệu. Toàn bộ 54 TC đã được review. Các ca dựa trên S7 đánh giá **quy ước thiết kế bổ sung**, không gán nguồn thành requirement README đã ghi rõ.

### Đối chiếu source để tránh bỏ qua requirement

S4 hiện chỉ có state/input Name, Email, Password; form chưa thấy Confirmation. Handler kiểm tra password bằng regex rồi gửi `name/email/password` tới `/register`. Regex dùng nhóm “không phải chữ/số” làm special; route/schema chưa thể hiện đầy đủ validation/uniqueness trong đoạn đăng ký đã đọc. Đây là **nghi vấn từ static reading**, không phải lỗi runtime đã xác nhận.

Do vậy vẫn giữ TC33–37 cho MR-R10. TC33 kiểm tra sự tồn tại của trường trên native; TC34–37 cần trường này để nhập dữ liệu, ghi **guard** rõ ràng. Khi execution sau này nếu trường thật sự không có thì không nhập confirmation qua API, không sửa SUT để chạy được, không ghi các TC equality là đã kiểm tra. Các TC còn lại chỉ credit rule mục tiêu của chúng; không dùng việc đăng ký được khi thiếu Confirmation để credit MR-R10.

## 3. Bước 1 — Biến và mô hình miền

| Biến | Kiểu/đơn vị và nominal | Rule/quan hệ |
| --- | --- | --- |
| N | Chuỗi tên; nominal `Nguyen Van A`. Required xét `trim(N)`. Khi BVA dùng tên ASCII non-whitespace, `nN` step 1 | MR-R01; rỗng hoặc toàn whitespace bị từ chối |
| E | Chuỗi email nhập; `Ecanon=trim(E)`; nominal mới `mr.t02r01.tcNN@example.com` | MR-R02; validate/lưu/so sánh Ecanon, không tự lowercase |
| U(Ecanon) | `new` hoặc `existing_exact`, so sánh có phân biệt case, phụ thuộc dữ liệu/lịch sử | MR-R03; không phải khoảng số thứ tự |
| P | Chuỗi password; nominal `Abcde1!x` | MR-R04–09 |
| L(P) | Số Unicode code point trong P; nominal 8 | MR-R05: `L≥8`; không đếm byte/UTF-16 unit |
| nU,nL,nD,nS | Số hoa ASCII/thường ASCII/digit ASCII trong mẫu đang dùng; nS đếm code point có category Unicode P* hoặc S* | MR-R06–09: mỗi count ít nhất 1; whitespace không tăng nS |
| C | Confirmation; nominal bằng P | MR-R10: required field và quan hệ `C=P`; quan hệ equality không có BVA số mặc định |
| F,Q | Form có field C không; trạng thái sửa lỗi, trước/sau một submit | MR-R10, MR-R03, MR-R11 |

Trong mô hình đang dùng, điều kiện đăng ký là phép **AND** của `trim(N)≠""`, Ecanon hợp lệ/mới theo phép so sánh case-sensitive, `L(P)≥8` theo code point, `nU,nL,nD,nS≥1`, có C và `C=P`. Mỗi điều kiện sai được lấy mẫu riêng để tránh một lỗi khác che mục tiêu. Khi giảm một class count về 0, các điểm BVA thay bằng ký tự nhóm khác để giữ L=8. Space vẫn đóng góp vào độ dài nhưng không vào nS; không trim password. Không lấy tích Descartes của mọi chuỗi.

### Bước 2 — Phân miền, điểm đại diện và lý do

Đây là **37 mục tiêu miền** sau review (29 ban đầu và 8 bổ sung). Các chiều khác nhau có thể chồng nhau; không nhận là 37 partition toán học rời nhau. Trong chiều độ dài P, các lớp `0`, `1..7`, `≥8` không chồng và không có khoảng hở, với đơn vị code point đã chốt.

| Domain | Predicate / điểm đại diện | Rule | TC | Lý do chọn |
| --- | --- | --- | --- | --- |
| MR-D01 | N rỗng `""` | R01 | 02 | Required bị bỏ qua |
| MR-D02 | `trim(N)` không rỗng: nominal, `V`, `Vy`, `Trần Quốc Vỹ` | R01 | 01,03–05 | Required hợp lệ; không bao gồm tên toàn space ở D30 |
| MR-D03 | Email valid/new: `mr.t02r01.tc01@example.com` | R02–03 | 01 | Control hợp lệ cho các lớp email invalid |
| MR-D04 | E rỗng | R02 | 06 | Required email |
| MR-D05 | E thiếu `@`: `mr.t02r01.tc07.example.com` | R02 | 07 | Tách local/domain sai |
| MR-D06 | E thiếu local-part: `@example.com` | R02 | 08 | Không chỉ kiểm tra có dấu `@` |
| MR-D07 | E thiếu domain: `mr.t02r01.tc09@` | R02 | 09 | Domain rỗng |
| MR-D08 | E có space trong local đơn giản: `mr t02r01.tc10@example.com` | R02 | 10 | Space bên trong, không phải tranh luận trim đầu/cuối |
| MR-D09 | E có hai `@` không quote: `mr.t02r01.tc11@@example.com` | R02 | 11 | Validator quá đơn giản |
| MR-D10 | E valid đã tồn tại từ trước: `test@eshop.com` | R03 | 12 | Phân biệt syntax hợp lệ và uniqueness |
| MR-D11 | E chuyển new→existing sau lần đăng ký đầu | R03 | 13 | Kiểm tra state thay vì chỉ seed cố định |
| MR-D12 | P rỗng | R04 | 14 | Required; đồng thời sai nhiều điều kiện nên không credit các class count riêng |
| MR-D13 | `1≤L(P)≤7`: `Abcde1!` | R05 | 15 | Chỉ sai độ dài, vẫn đủ 4 nhóm ký tự |
| MR-D14 | `L(P)≥8`: độ dài 8,9,64 code point | R05 | 16–17,40,47–48 | Biên ASCII/Unicode và đại diện xa biên; 64 không phải max |
| MR-D15 | `nU=0`: `abcde1!x` | R06 | 18 | Bỏ sót yêu cầu chữ hoa |
| MR-D16 | `nU≥1`: `Abcde1!x`, `ABcde1!x` | R06 | 16,19 | Chấp nhận đúng một/nhiều chữ hoa |
| MR-D17 | `nL=0`: `ABCDE1!X` | R07 | 20 | Bỏ sót yêu cầu chữ thường |
| MR-D18 | `nL≥1`: `ABCDa1!X`, `ABCDab1!` | R07 | 21–22 | Đúng một và nhiều chữ thường |
| MR-D19 | `nD=0`: `Abcdef!x` | R08 | 23 | Bỏ sót yêu cầu chữ số |
| MR-D20 | `nD≥1`: `Abcde1!x`, `Abcde12!` | R08 | 16,24 | Đúng một và nhiều chữ số |
| MR-D21 | Không có special, P chỉ alphanumeric: `Abcde12x` | R09 | 25 | Control nS=0, không có whitespace/Unicode gây nhiễu |
| MR-D22 | Có special trong S0: `Abcde1!x`, `Abcde1!!`; thay `!` bằng từng `@,$,%,*,?,&` | R09 | 16,26–32 | Count 1/2 và đủ 7 ví dụ trong README; S0 không còn là tập special đầy đủ |
| MR-D23 | Schema form phải có C | R10 | 33 | Không bỏ requirement chỉ vì source thiếu input |
| MR-D24 | C rỗng trong khi P hợp lệ | R10 | 34 (guard) | Required confirmation và mismatch |
| MR-D25 | `C=P` | R10 | 37 (guard) | Control hợp lệ cho so sánh hai trường |
| MR-D26 | `C≠P`, cùng độ dài: `Abcde1!y` vs `Abcde1!x` | R10 | 35 (guard) | Tránh chỉ kiểm tra độ dài |
| MR-D27 | `C≠P`, khác độ dài: `Abcde1!` vs `Abcde1!x` | R10 | 36 (guard) | Tránh so khớp prefix/cắt chuỗi |
| MR-D28 | Reject rồi sửa đúng cùng email | R05,R03,R11 | 38 | Invalid không được tạo account ẩn; trạng thái lỗi không được chặn submit hợp lệ sau đó |
| MR-D29 | Email duplicate AND P yếu | R03,R06 | 39 | Tương tác thật giữa hai điều kiện; không áp đặt thứ tự thông báo lỗi |
| MR-D30 | `trim(N)=""` nhưng N không rỗng literal: 1 space | R01,Q01 | 41 | Phân biệt kiểm tra empty đơn thuần với required theo nội dung |
| MR-D31 | Ecanon khác case local-part so với email đã lưu | R03,Q02 | 42 | Case-sensitive theo S7, không tự lowercase |
| MR-D32 | E có space đầu/cuối, Ecanon valid/new | R02–03,Q03 | 43 | Tách bước trim khỏi validation/lưu dữ liệu |
| MR-D33 | Special ngoài S0: `#`, `_`, `😀`, `—`, `€` | R09,Q04 | 44,49–52 | Đại diện dấu/ký hiệu Unicode ngoài bảy ví dụ; không nhận bao phủ mọi category/ký hiệu |
| MR-D34 | Có space nhưng không có dấu/ký hiệu P*/S* | R09,Q04 | 45 | Không dùng whitespace thay special |
| MR-D35 | P có emoji, L=7/8/9 code point | R05,Q05 | 46–48 | Phát hiện nhầm số UTF-16 unit thành độ dài nghiệp vụ |
| MR-D36 | E có space đầu/cuối nhưng Ecanon đã tồn tại | R03,Q03 | 53 | Uniqueness phải xét sau trim, không chỉ validate sau trim |
| MR-D37 | P có space và có special `!` hợp lệ | R05,R09,Q04 | 54 | Không đếm space là special khác với cấm toàn bộ space trong P |

Trong bảng, `Rxx`/TC số rút gọn lần lượt là `MR-Rxx`/`MR-TCxx`. Không dùng ON/OFF/IN/OUT cho email hoặc role khi chưa có định nghĩa bài giảng phù hợp.

### Bước 3 — Chọn điểm và hiện thực dữ liệu

1. Dùng một control hợp lệ P=`Abcde1!x`, E mới, N nonempty; giữ các điều kiện này khi khảo sát email hoặc tên.
2. Với từng rule password, thay đúng nhóm mục tiêu. Ví dụ `abcde1!x` có 8 ký tự, 0 hoa nhưng vẫn có thường/số/`!`; reject của TC18 có thể truy tới R06 thay vì bị thiếu độ dài che mất.
3. Tách email syntax và uniqueness: TC07–11 dùng chuỗi chưa có trong fixture; TC12 dùng email trùng nguyên chuỗi, password vẫn mạnh.
4. Chọn đủ từng ký hiệu S vì rủi ro escape regex/allow-list khác nhau. Đây là lấy mẫu theo tập thành viên, không gọi là BVA.
5. Thêm hai sequence có mục tiêu: TC13 new→existing; TC38 invalid→corrected. TC39 là tương tác nhiều điều kiện sai, không dùng nó thay các ca sai độc lập.
6. Với C, giữ cả cặp same-length/different-length và matching control. Phân biệt yêu cầu field có tồn tại (33) với việc nhập và so sánh được (34–37).
7. Sau review S7, thêm Unicode 7/8/9 code point và các đại diện special ngoài S0; giữ các điều kiện khác hợp lệ. Thêm email duplicate sau trim và password chứa cả space/`!` để kiểm tra tương tác giữa các quy ước đã chốt.

## 4. Bước 4 — Boundary Value Analysis riêng

S5 trang 44 chọn quanh biên hợp lệ `b`: `b−δ`, `b`, `b+δ`. Với độ dài P, `δ=1 Unicode code point` theo S7; với các class count, step là 1 phần tử được đếm. Các mẫu tên B06 dùng ASCII non-whitespace nên step là 1 ký tự. MR-B01 là biên tối thiểu password được nêu trực tiếp; MR-B02–05 suy từ “ít nhất 1”; MR-B06 suy từ required N và A01 đã được Vỹ đồng ý.

| Boundary | Hai miền / dấu bằng | Nguồn | Coverage items và TC | Kiểm soát |
| --- | --- | --- | --- | --- |
| MR-B01 | `L(P)<8` / `L(P)≥8`, b=8 code point | R05; đơn vị S7 | `B01-7`→15,46; `B01-8`→16,47; `B01-9`→17,48 | ASCII và Unicode cùng ngưỡng; đủ hoa/thường/số/special; C khớp khi field có |
| MR-B02 | `nU=0` / `nU≥1`, b=1 | R06 | `B02-0`→18, `B02-1`→16, `B02-2`→19 | L=8; các nhóm còn lại hợp lệ |
| MR-B03 | `nL=0` / `nL≥1`, b=1 | R07 | `B03-0`→20, `B03-1`→21, `B03-2`→22 | L=8; các nhóm còn lại hợp lệ |
| MR-B04 | `nD=0` / `nD≥1`, b=1 | R08 | `B04-0`→23, `B04-1`→16, `B04-2`→24 | L=8; các nhóm còn lại hợp lệ |
| MR-B05 | Không special / `nS≥1`, b=1, mẫu invalid chỉ alphanumeric | R09 | `B05-0`→25, `B05-1`→16, `B05-2`→26 | L=8; các nhóm còn lại hợp lệ; `#` là special theo S7 nên không dùng làm điểm 0 |
| MR-B06 | N rỗng / N có ít nhất 1 ký tự non-whitespace, b=1 | R01 + A01 | `B06-0`→02, `B06-1`→03, `B06-2`→04 | Dùng `""`,`V`,`Vy`, P mạnh và E mới; không tự đặt min tên là 2 |

**Giải thích dấu bằng:** P dài 8 và count đúng 1 thuộc miền hợp lệ; P dài 7 hoặc count 0 thuộc miền không hợp lệ. Giá trị 9 và count 2 giúp phân biệt triển khai nhầm `=8`/`=1` thay cho `≥`. Tên 1/2 ký tự dựa trên required và chưa có restriction khác; nếu bổ sung grammar tên, phải cập nhật biên R01/A01.

**Không có biên trên nghiệp vụ được đặc tả.** TC40 dùng 64 ký tự như một điểm đại diện miền dài; không gọi 63/64/65 là BVA. Không tạo độ dài âm, không dùng giới hạn byte/keyboard của môi trường làm max nghiệp vụ. Các regex/email khác nhau, email tồn tại, presence của field và `C=P` là phân loại/quan hệ, không tự đặt BVA số cho chúng. Riêng C ngắn hơn P ở TC36 chỉ là đại diện mismatch, không chứng minh một rule minimum length của C.

Có **6 boundary inventories × 3 items = 18 items**. TC16 cùng lúc chạm B01-8/B02-1/B04-1/B05-1. Bản đầu có 15 unique TC BVA; sau review thêm TC46–48 hiện thực lại 3 items B01 bằng Unicode, thành **18 unique TC BVA**. Số boundary items vẫn là 18; không cộng lần hiện thực ASCII/Unicode thành biên mới hoặc đếm TC16 bốn lần.

## 5. Bước 5 — Tự kiểm tra thiết kế và coverage

Phần này mô tả **AI tự rà soát thiết kế**; Vỹ đã hoàn tất review bộ tài liệu sau đó. Bản v0.1 được giữ để đối chiếu. Các điểm biên ASCII vẫn giữ nguyên, TC46–48 bổ sung cùng B01 bằng Unicode. Expected bổ sung dẫn S7, không dựa vào regex/code đang có.

| Inventory | Ánh xạ thiết kế | Giới hạn |
| --- | --- | --- |
| Rules | 11/11 rule có TC: R01→01–05,41; R02→01,06–11,43,53; R03→01,12–13,38–39,42–43,53; R04→14; R05→15–17,38,40,46–48,50,54; R06→16,18–19,39; R07→20–22; R08→16,23–24; R09→16,25–32,44–45,49–52,54; R10→33–37; R11→các ca ACCEPT | Nguồn gồm requirement và review S7. R10 equality còn guard; ánh xạ thiết kế không phải đã kiểm chứng |
| Domain targets | 37/37 mục tiêu có TC thiết kế | Theo source, 33 mục tiêu có đường nhập/quan sát; D24–27 phụ thuộc field C. Đây là reachability tĩnh, không phải execution coverage |
| Special samples | 7/7 ví dụ S0 trong README và 5 điểm ngoài S0 (`#`, `_`, `😀`, `—`, `€`) có TC ACCEPT | Không nhận đã bao phủ mọi ký hiệu hoặc mọi category Unicode; đây là đại diện có mục tiêu |
| BVA items | 18/18 items được ánh xạ, 18 unique TC BVA | ASCII và Unicode hiện thực cùng 3 items B01; không tăng mẫu số vì thêm dữ liệu |
| Review | A01,Q01–05 đã chốt; toàn bộ 54 TC đã được review | Q06 công bố phạm vi thiết kế; review hoàn tất không đồng nghĩa đã thực thi |

Tổng **54 unique TC**, mọi ca có expected theo requirement và các quy ước/giả định đã ghi nguồn. **4 TC (34–37) cần field C** để nhập/so sánh. Có 18 TC mang cả Domain và BVA; vẫn chỉ đếm 54 unique TC. Toàn bộ **Not Run**; không có actual, execution coverage hay bug verdict.

## 6. Quy ước đã chốt và giới hạn thiết kế

### Các quyết định đã ghi nhận ngày 20/10/2026

Các quy ước S7 dưới đây đã được đối chiếu với bộ TC. Tên/Email/Password lần lượt ký hiệu N/E/P; cột cuối liên kết đến các ca áp dụng. Đây là cơ sở thiết kế, chưa phải kết quả chạy SUT.

| Điểm | Kết luận đã chốt | Ảnh hưởng và vị trí để đọc |
| --- | --- | --- |
| **A01 — Tên** | Tên không rỗng và có nội dung non-whitespace; chưa thêm restriction khác | Giữ ACCEPT cho `V`, `Vy`, `Trần Quốc Vỹ`; [TC03–05](D:/Workspace/SoftwareTesting/HW02/eshop-sut/tests/hw02/mobile-registration/test-cases.md:33); giữ [BVA tên B06](D:/Workspace/SoftwareTesting/HW02/eshop-sut/tests/hw02/mobile-registration/design.md:147) |
| **Q01 — Tên toàn space** | Tên chỉ gồm khoảng trắng bị coi là chưa nhập tên, nên REJECT | [TC41](D:/Workspace/SoftwareTesting/HW02/eshop-sut/tests/hw02/mobile-registration/test-cases.md:92). Phân biệt chuỗi literal `" "` có 1 ký tự với giá trị sau trim rỗng; không bắt buộc trim tên được lưu nếu tên có nội dung |
| **Q02 — Case email** | So sánh email sau trim **có phân biệt hoa/thường** | [TC42](D:/Workspace/SoftwareTesting/HW02/eshop-sut/tests/hw02/mobile-registration/test-cases.md:93) ACCEPT `TEST@eshop.com` khi chỉ có `test@eshop.com`; [TC12–13](D:/Workspace/SoftwareTesting/HW02/eshop-sut/tests/hw02/mobile-registration/test-cases.md:42) vẫn REJECT đăng ký trùng nguyên chuỗi |
| **Q03 — Space ngoài email** | Bỏ khoảng trắng đầu/cuối rồi validate/lưu/kiểm tra uniqueness | [TC43](D:/Workspace/SoftwareTesting/HW02/eshop-sut/tests/hw02/mobile-registration/test-cases.md:94) ACCEPT email mới sau trim; [TC53](D:/Workspace/SoftwareTesting/HW02/eshop-sut/tests/hw02/mobile-registration/test-cases.md:111) REJECT email sau trim đã tồn tại |
| **Q04 — Special** | Công nhận dấu/ký hiệu Unicode, mô hình hóa Punctuation/Symbol; whitespace không được tính là special | [TC44–45](D:/Workspace/SoftwareTesting/HW02/eshop-sut/tests/hw02/mobile-registration/test-cases.md:95): `#` ACCEPT, space-only-special REJECT. [TC49–52](D:/Workspace/SoftwareTesting/HW02/eshop-sut/tests/hw02/mobile-registration/test-cases.md:107) thêm `_`, emoji, em dash, euro. [TC54](D:/Workspace/SoftwareTesting/HW02/eshop-sut/tests/hw02/mobile-registration/test-cases.md:112) phân biệt “không đếm space là special” với “cấm mọi space” |
| **Q05 — Độ dài** | Đếm **Unicode code point**, `😀` đơn tính 1; không đếm UTF-16 unit | [TC46–48](D:/Workspace/SoftwareTesting/HW02/eshop-sut/tests/hw02/mobile-registration/test-cases.md:97) có 7/8/9 code point, lần lượt REJECT/ACCEPT/ACCEPT. Không tự chuẩn hóa ký tự Unicode trước đếm |

### Phạm vi và điều kiện thực thi

- **Confirmation có requirement rõ:** [FR-01 dòng 35](D:/Workspace/SoftwareTesting/HW02/eshop-sut/README.md:35) yêu cầu trường xác nhận và từ chối khi không khớp. [Form Mobile dòng 797](D:/Workspace/SoftwareTesting/HW02/eshop-sut/frontend-mobile/App.js:797) chưa thể hiện field này trong source đã đọc. Giữ [TC33–37](D:/Workspace/SoftwareTesting/HW02/eshop-sut/tests/hw02/mobile-registration/test-cases.md:77); khi execution được giao, kiểm tra toàn form bằng TC33. Nếu thiếu thật, TC34–37 không nhập được; không ghi pass hay thay bằng API.
- **Độ dài và định dạng (Q06):** [FR-01 dòng 32–34](D:/Workspace/SoftwareTesting/HW02/eshop-sut/README.md:32) không đặt max tên/email/password. Thiết kế không thêm ngưỡng tùy ý; chỉ kiểm tra các minimum đã xác định và điểm dài đại diện. Bộ hiện tại dùng email thông dụng, code point nguyên bản và mẫu chữ/số ASCII; không nhận đã bao phủ toàn bộ grammar email, normalization hoặc mọi Unicode.
- **Phạm vi kiểm thử:** các TC dùng submit tuần tự, kết nối bình thường theo A02. Race giữa hai client, mất mạng/retry, hiệu năng và security payload nằm ngoài bộ Domain/BVA này; đây là lựa chọn phạm vi, không phải các đầu việc review còn treo.
- **Quan sát account khi chạy:** [oracle và bước chung](D:/Workspace/SoftwareTesting/HW02/eshop-sut/tests/hw02/mobile-registration/test-cases.md:15) yêu cầu đối chiếu dữ liệu runtime chỉ đọc theo Ecanon/case; thao tác đăng ký vẫn qua native. Chỉ thấy toast không chứng minh đã lưu đúng một account. Chưa chạy/query DB trong bước thiết kế này.

Bản AI v0.1 và snapshot v0.2 được giữ local ngoài repo trong `HW02/.runtime/design-baselines/`. Bản thiết kế hiện tại đã được review; giữ nguyên 54 TC và các ID để truy vết. Chưa có kết quả thực thi.
