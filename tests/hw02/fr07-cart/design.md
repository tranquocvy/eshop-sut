# T04 — FR-07 Shopping Cart: thiết kế Domain và BVA

Thiết kế AI v0.1, ngày 20/10/2026 (UTC+7). Vỹ đã đọc và xác nhận các TC hiện có ngày 20/10/2026; giữ nguyên nội dung thiết kế, chỉ cập nhật trạng thái review. Bộ TC: [test-cases.md](test-cases.md). Tất cả **Not Run**; tài liệu này không phải báo cáo thực thi. Không đánh dấu T04 hoàn tất vì execution, evidence, báo cáo và AI log chưa thực hiện trong lượt thiết kế.

## 1. Test basis và phương pháp

Baseline đọc tĩnh: `df7135b9abf5b03e3149e147b43006950c5258fa` tại `HW02/eshop-sut`. Thay đổi Mobile và file cache đang có được giữ nguyên.

| Nguồn | Vị trí | Vai trò |
| --- | --- | --- |
| S1 | [README](../../../README.md), FR-07, dòng 93–100 | Các cột, +/−, gộp cùng sản phẩm, xác nhận xóa, tiếp tục mua sắm, nhãn tổng, giỏ trống |
| S2 | README, FR-06, dòng 83–87 | Số lượng nguyên dương tối thiểu 1 và phản hồi sau thêm; dependency cần thiết để đưa sản phẩm vào giỏ |
| S3 | [API specification](../../../api_specification.md), §4.1–4.2 | GET/POST `/api/cart`, Bearer token và JSON id/name/price/quantity; không có endpoint chỉnh/xóa cart trong contract |
| S4 | [CartContext.jsx](../../../frontend-web/src/context/CartContext.jsx), [Cart.jsx](../../../frontend-web/src/pages/Cart.jsx), [ProductDetail.jsx](../../../frontend-web/src/pages/ProductDetail.jsx), [App.jsx](../../../frontend-web/src/App.jsx); [server.js](../../../backend/server.js), dòng 284–295 | Đường vào `/product/:id`, `/cart`; Web context và API userCarts tách biệt; chỉ giúp chọn điểm quan sát/rủi ro, không làm oracle |
| S5 | [database.js](../../../backend/database.js), dòng 97–103 | Dữ liệu seed cố định để đối chiếu giá; không import module vì có reset database |
| S6 | [Đề HW02](../../../../2026.HW02.Domain%20Testing_Vn.md), §6.1–6.2; [quyết định T01](../../../../T01-setup/ENVIRONMENT.md), dòng 24–41 | Giải thích từng bước, chủ động thêm TC; phương pháp đã chọn cho HW02 |
| S7 | Các references `domain-testing.md`, `boundary-value-analysis.md`, `test-case-contract.md` của skill `C:/Users/DELL/.codex/skills/domain-bva-testing/` đã đọc trong lượt này | Mô hình biến, miền, điểm đại diện, oracle minh bạch, kiểm tra coverage |

`method_profile`: **reference-provisional** cho lượt này. Domain theo references của skill; chưa có slide Domain riêng. BVA giữ quyết định T01: `course-guide-3-value`, quanh biên hợp lệ b lấy b−δ, b, b+δ. Nguồn gốc quyết định là tài liệu tự học môn trang 44 đã ghi ở T01; lượt này chưa đọc lại trang đó nên không tự nhận mới đối chiếu bài giảng. Không gọi tập {0,1,2} là helper `istqb-3` (profile đó có cách đếm khác).

Lớp chính là **Web**. API là tập bổ trợ có ID riêng, không thay bằng chứng Web hoặc fixture cho Web. Phạm vi FR-07 và dependency nhập số lượng FR-06; không mở rộng kiểm thử checkout, coupon, quản lý sản phẩm hoặc login tổng quát.

## 2. Bước 0 — Rules và oracle

| Rule | Điều kiện/kết quả đúng | Trạng thái, nguồn |
| --- | --- | --- |
| R01 | Sau mỗi thao tác thêm hợp lệ, giỏ phản ánh sản phẩm và số lượng đã thêm; có phản hồi trực quan sau bấm | Confirmed S1/S2; một click là một thao tác, không mặc định phải bấm hai lần |
| R02 | Thêm cùng sản phẩm (cùng ID) làm cộng số lượng, không sinh dòng mới | Confirmed S1 |
| R03 | Giỏ có cột Sản phẩm, Đơn giá, Số lượng với +/−, Thành tiền, Thao tác | Confirmed S1 |
| R04 | Thành tiền từng dòng = giá × số lượng; tổng = tổng thành tiền các dòng; thay đổi phải cập nhật nhất quán | Oracle số học suy ra từ ý nghĩa S1, không lấy cách tính của source làm expected |
| R05 | Trước khi xóa phải có dialog xác nhận; hủy không xóa, xác nhận chỉ xóa sản phẩm đích | Confirmed S1; hủy/đồng ý là ngữ nghĩa của xác nhận |
| R06 | Nút Tiếp tục mua sắm đưa về trang chủ | Confirmed S1, áp dụng giỏ rỗng/có hàng |
| R07 | Tổng tiền dùng nhãn chính xác “Tổng cộng” | Confirmed S1 |
| R08 | Giỏ trống có hình minh họa và thông báo rõ ràng | Confirmed S1 |
| R09 | Số lượng khi thêm chỉ nhận số nguyên dương q≥1; 0, âm, phân số, thiếu giá trị không được thêm | Confirmed S2; không ấn định câu lỗi/mã lỗi |
| R10 | GET/POST API cart yêu cầu Bearer token hợp lệ | Confirmed S3; không yêu cầu role admin hoặc exact 401/403 |

| Giả định | Oracle đề xuất/chưa rõ | Lý do và phạm vi |
| --- | --- | --- |
| A01 | Trong giỏ, + tăng đúng 1, − giảm đúng 1; ở q=1 không tạo q=0/âm hoặc xóa im lặng. Có thể chặn giảm hoặc hỏi xác nhận xóa | Quy ước đề xuất từ +/−, R05, dependency S2; S1 chưa quy định chính xác xử lý tại min |
| A02 | Điều hướng nội bộ và Back/Forward cùng tab giữ giỏ; reload giữ giỏ trong cùng phiên | Đề xuất trải nghiệm liên tục; reload persistence chưa được S1 xác nhận; tách TC reload khỏi ca nội bộ |
| A03 | API thêm/gộp và quantity tuân theo ngữ nghĩa R01/R02/R09, dù S3 chưa khẳng định đồng nhất Web/API | Oracle đề xuất chỉ cho nhóm API, không kết luận vi phạm contract chắc chắn nếu khác |
| A04 | Input Web dạng chữ/whitespace, giá trị ngoài biểu diễn an toàn phải được chặn hoặc xử lý rõ ràng, không sinh NaN/Infinity/giỏ sai âm | Robustness; không đặt max nghiệp vụ. Chỉ đòi tính toàn vẹn, chưa chốt mọi cú pháp nhập số |
| A05 | Chuỗi “2”, “2.0”, “2e0”, “+2”, “02”, khoảng trắng quanh “2” là mục tiêu khảo sát về chuẩn hóa; nếu được nhận thì giá trị phải đúng 2, không âm thầm thành giá trị khác | Không có contract lexical; ghi riêng khảo sát, không tự áp “chỉ chữ số” |
| A06 | API mỗi user có giỏ riêng; input sai kiểu/thiếu và product ID không tồn tại bị từ chối; không tin giá giả từ client | Chính sách đề xuất tăng coverage API; S3 chưa quy định validation/lookup giá; tách khỏi confirmed |
| A07 | Chuỗi tên sản phẩm được hiển thị như văn bản, không chạy HTML/script; nhiều ID có thể cùng tên mà vẫn là dòng khác nhau | Đề xuất tính toàn vẹn hiển thị/định danh; cần fixture bổ sung có kiểm soát |
| Q01 | Không có max quantity, giới hạn số dòng, tồn kho, precision tiền lẻ, persistence nhiều thiết bị, chính sách giá thay đổi hoặc merge giỏ sau login | Không tự thêm ngưỡng max/stock từ schema. Ca lớn là robustness, không là BVA max |
| Q02 | Web và API hiện có hai store khác nhau; contract không cam kết đồng bộ | Không yêu cầu API GET khớp Web hoặc kết luận lỗi sync; mỗi lớp setup/đối chiếu riêng |

A01–A07 là oracle đề xuất của AI trong bộ TC đã được Vỹ đọc và xác nhận; việc duyệt bộ test không biến các giả định thành requirement có sẵn trong đề. Không phải lý do bỏ TC; ca tương ứng vẫn được thiết kế, nguồn expected ghi rõ. Không dùng ca khảo sát để công bố coverage rule chắc chắn.

## 3. Bước 1 — Biến và miền

Biến: `C` = tập dòng theo ID; `n=|C|` là số dòng khác sản phẩm, bước 1; `i` = ID tồn tại, là tập thành viên không là khoảng; `q_old`, `q_add`, `q_new` = số lượng đơn vị sản phẩm, nominal 2/3/5; `p` = giá VND nguyên từ fixture; `L=pq`, `T=ΣL`; `Op` = add/plus/minus/remove/cancel/continue; `Route` và `Session` = trạng thái điều hướng/phiên; `Auth` cho API.

Quan hệ trọng tâm: add ID mới ⇒ n′=n+1; cùng ID ⇒ n′=n, q′=q_old+q_add; +/- ⇒ q′=q±1 (A01); xóa đồng ý ⇒ C′=C\{i}, T′=T−p_i q_i; hủy ⇒ C′=C, T′=T. Chọn giá khác nhau để phát hiện lấy nhầm dòng; lặp cùng ID với quantity khác để phát hiện replace thay vì cộng. Giữ các biến khác hợp lệ khi đánh giá input sai.

Các hàng sau là mục tiêu theo các chiều, có thể chồng nhau, không nhận toàn bảng là partition rời nhau.

| Domain | Predicate, đại diện và lỗi mục tiêu | Rule | TC Web / API |
| --- | --- | --- | --- |
| D01 | C=∅, quan sát và trở lại giỏ trống: tránh dòng/tổng cũ | R08 | W01,W20,W23 |
| D02 | n=1, thêm mới P×1/P×3; kiểm tra click đầu và đúng q | R01,R03,R04,R07 | W02,W03,W09 |
| D03 | i∈C, cùng ID q_old=2,q_add=3; thêm lặp hoặc xen kẽ ID | R02,R04 | W04,W06,W07 |
| D04 | i∉C, nhiều ID/giá khác, bao gồm cùng tên khác ID | R01,R04; A07 | W05,W08,W28 |
| D05 | q nguyên hợp lệ, minimum/nominal/lớn | R09; A04 cho lớn | W02,W03,W24,W25 |
| D06 | q nguyên ≤0, đại diện 0/−1 | R09 | W10,W11 |
| D07 | q phân số, đại diện 0.5/1.5/−0.5 | R09 | W12,W13,W14 |
| D08 | q thiếu/không số, rỗng/chữ/whitespace | R09; A04 | W15,W26 |
| D09 | chỉnh tăng/giảm và chỉ đúng dòng, đạt min | R03,R04; A01 | W16,W17,W18 |
| D10 | xóa: mở dialog/hủy/đồng ý; nhiều dòng, dòng cuối | R05,R04,R08 | W19,W20,W21,W22 |
| D11 | điều hướng: tiếp tục mua sắm, Back/Forward, reload | R06; A02 | W23,W29,W30 |
| D12 | biểu diễn số/chuỗi và tổng lớn, tên dài/HTML | R04; A04,A05,A07 | W24,W25,W27,W28,W31 |
| D13 | API auth thiếu/sai/hợp lệ | R10 | A01,A02,A03 |
| D14 | API empty/new/duplicate, q 0/1/2, phân số, missing | A03 | A03,A04,A05,A06,A07,A08,A09,A10 |
| D15 | API sai kiểu/ID/giá/user khác nhau | A06 | A11,A12,A13,A14 |
| D16 | phục hồi sau input sai, xóa rồi thêm lại, thao tác nhanh | R01,R02,R04,R05; A01 | W07,W22,W32,W33 |

Không lấy tích Descartes toàn bộ q×C×Op×Session. Điểm nhiều chiều có mục đích: W06 cùng ID nhưng có dòng xen kẽ; W08 nhiều giá/quantity; W21 xóa dòng giữa để lộ nhầm index; W33 +/− nhanh kiểm tra mất cập nhật. Không gắn nhãn ON/OFF/IN/OUT khi chưa có định nghĩa slide.

## 4. Bước 2 — BVA riêng

| Boundary | Hai miền/nguồn | b, δ và items | Hiện thực / coverage thiết kế |
| --- | --- | --- | --- |
| B01 | q_add nguyên không hợp lệ ≤0 / hợp lệ ≥1; S2 | b=1, δ=1 đơn vị ⇒ 0,1,2 | W10,W02,W34: 3/3 |
| B02 | q_cart tối thiểu theo A01, không nhận q≤0 | b=1, δ=1 ⇒ 0,1,2 | W18 thử giảm từ 1 về 0; W17 đạt 1 từ 2; W16 tăng 1 lên 2: 3/3 theo assumption |
| B03 | n=0 / n≥1; R08, trạng thái không phải field nhập | b=0, δ=1 ⇒ −1,0,1 | −1 dòng không thể biểu diễn, không tạo TC nhập giả; W01/W02 chạm 0/1, W20 chạm chuyển 1→0: 2/2 khả thi |
| B04 | API q_add theo A03 | b=1, δ=1 ⇒ 0,1,2 | A07,A04,A05: 3/3 theo assumption |

B01 chỉ xét số nguyên: 0.5/1.5 không phải “hàng xóm” khi δ=1; thuộc D07 riêng. Không suy biên tiền tối thiểu 0 cho sản phẩm vì FR-07 không cho phép tạo giá 0; không tạo BVA ID từ min/max ID seed. Giá 6.000.000/28.000.000/30.000.000 là dữ liệu số học, không là boundary giá. q=1000 và q=9007199254740992 là robustness/biểu diễn, không là giới hạn tối đa nghiệp vụ được xác nhận.

## 5. Kiểm tra thiết kế và giới hạn bàn giao

- **48 unique TC:** 34 Web (W01–W34), 14 API (A01–A14). Mỗi hàng là một TC; biến thể dữ liệu trong một ca được ghi theo substep, không cộng thành TC mới. W27 là khảo sát biểu diễn, tách khỏi TC có oracle quyết định đầy đủ.
- Domain inventory: 16/16 mục tiêu có TC, trong đó D01–D10,D16 có phần requirement xác nhận, D11/D12/D13 là các nhóm có phạm vi/nguồn như bảng, D14/D15 theo assumption. Đây là truy vết thiết kế, không là 100% mọi hành vi.
- BVA requirement: B01 3/3 items và B03 2/2 khả thi; B03 còn 1 item không biểu diễn được. BVA assumption: B02 3/3, B04 3/3. Không cộng tỷ lệ assumption vào coverage requirement.
- R01–R10 đều có TC, nhưng R09 chỉ có min/kiểu số, chưa biết max; API auth không đại diện quyền checkout. Chưa có dữ liệu runtime, không có pass/fail, bug, evidence hay coverage thực thi.
- Self-review AI đã rà: click đầu; gộp cùng ID trong giỏ nhiều hàng; không gộp khác ID cùng tên; số lượng âm/0/phân số/rỗng; tính tổng sau chỉnh/xóa/hủy; dialog dòng cuối; điều hướng; nhiều seed product; lỗi biểu diễn và phân lớp API. Không gọi self-review này là review của Vỹ.
- Người chạy cần tạo fixture riêng khi cần, xác nhận giá/ID trước ca và ghi dependency nếu UI không cho đạt setup. Thiếu +/− hoặc add không đạt precondition phải ghi rõ khi thực thi, không sửa SUT, inject context hay dùng API để giả Web thành công.
- Chưa bao phủ mọi browser/viewport, concurrency nhiều tab, thay đổi giá giữa phiên, network retry/idempotency và login merge vì policy chưa rõ. Những giới hạn này không loại các ca bổ sung hữu ích đã thiết kế.

Giữ v0.1 trong lịch sử/version trước mọi lần sửa tiếp theo; không tái tạo “AI ban đầu” từ bộ đã review.
