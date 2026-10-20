# T04 — FR-07 Shopping Cart: bộ test case

Thiết kế v0.2 — 20/10/2026 (UTC+7). **60 TC: 34 Web + 26 API.** 48 TC v0.1 đã được Vỹ đọc và xác nhận; giữ nguyên ID/nội dung. A15–A26 được AI bổ sung theo yêu cầu mở rộng API của Vỹ, Vỹ đã xác nhận kiểm tra hồ sơ T04 và chốt hoàn tất ngày 20/10/2026. Đây là bộ thiết kế; kết quả chạy thật ở [report.md](report.md), không điền Actual/Pass/Fail vào bảng thiết kế. Nguồn R/D/B/A và ánh xạ mục tiêu Web/API tại [design.md](design.md).

## Fixture và quy ước thao tác

**P0:** môi trường riêng, không thay đổi đồng thời, Web desktop, không coupon/checkout. Mỗi TC bắt đầu từ giỏ độc lập. Giỏ Web chỉ chuẩn bị bằng UI; cần giỏ rỗng có thể dùng phiên trình duyệt kiểm thử mới. Không gọi API cart hoặc inject React state để dựng giỏ Web. Nếu setup qua UI thất bại, ghi dependency khi thực thi; không thay expected để hợp code. Không reload giữa các bước trừ ca yêu cầu.

**Dữ liệu cố định từ seed S5:** P = iPhone 15 Pro Max, 30.000.000 ₫; Q = Samsung Galaxy S24 Ultra, 28.000.000 ₫; M = MacBook Pro M3, 45.000.000 ₫; H = Tai nghe AirPods Pro 2, 6.000.000 ₫; K = Bàn phím cơ Keychron Q1, 4.000.000 ₫. Ghi ID thực tương ứng trước khi chạy, không mặc định ID 1..5. Kiểm tra giá vẫn đúng; fixture khác thì khôi phục môi trường thử riêng trước ca. Không import `database.js` để đọc seed.

**C0** = giỏ trống. **C1** = P×1 (30.000.000). **C2** = P×2 (60.000.000). **C3** = P×2,Q×3,H×4 (60.000.000+84.000.000+24.000.000 = **168.000.000 ₫**). C5 = cả 5 seed mỗi loại 1, tổng **113.000.000 ₫**. Những precondition này phải kiểm tra trên Web trước bước mục tiêu, không giả định setup thành công.

**Add(X,q):** dùng link nội bộ tới chi tiết X; thay toàn bộ ô Số lượng bằng q (rỗng = xóa hết); bấm Thêm vào giỏ hàng **đúng một lần**; ghi phản hồi trực quan; mở link Giỏ hàng trong cùng SPA; đối chiếu số dòng, ID/tên/giá/q/thành tiền/tổng. Không tự bấm lần hai khi lần đầu không có tác dụng. **Check(C):** đối chiếu từng dòng với fixture và T=Σp×q; có các cột R03 và nhãn đúng “Tổng cộng” khi có hàng; không chấp nhận NaN/Infinity. Không áp một dấu phân cách hàng nghìn cụ thể khi đặc tả không quy định locale.

**Reject:** không thêm/cộng/đổi bất cứ dòng nào; số lượng và tổng trước–sau bằng nhau; không chấp nhận input thành quantity khác bằng cắt phần thập phân. Có chặn/validation rõ ở điểm nhập hoặc khi bấm; không áp exact message. Nếu browser không cho nhập chuỗi, ghi chính xác bị chặn tại UI, không sửa DOM/type hay gửi API để nhận coverage Web.

**API setup:** base `http://localhost:3000`; JSON `Content-Type: application/json`; TU/TV là JWT hợp lệ của hai user thử khác nhau qua login bình thường. API cart của TU có thể không trống: dùng user thử độc lập/fixture runtime đã được người chạy chuẩn bị, không restart backend đang dùng vì seed reset. `AP0` = API cart TU rỗng đã GET xác nhận; `AP1` = API cart TU có P×1 đã POST/GET xác nhận. Không suy trạng thái AP0/AP1 từ Web.

**Post(X,q):** POST `/api/cart` với `{ "id": <ID thực X>, "name": <tên X>, "price": <giá X>, "quantity": q }` và Bearer TU; GET lại bằng TU để so sánh. **AR:** từ chối request, không thay đổi giỏ đã GET trước, không nhận 2xx đơn lẻ là chứng minh dữ liệu đúng. API success/error code cụ thể chưa được contract định nghĩa; oracle validation nghiệp vụ API theo A03/A06, ghi tách biệt.

## A. Web — requirement, miền và biên

| TC ID | Technique / trace | Precondition | Input và steps | Expected và nguồn |
| --- | --- | --- | --- | --- |
| CART-W01 | Domain+BVA; R08/D01/B03=0 | P0,C0 | Mở Giỏ hàng | Có minh họa và thông báo rõ giỏ trống; không dòng hàng/tổng cũ. R08/S1 |
| CART-W02 | Domain+BVA; R01,R03,R04,R07,R09/D02,D05/B01=1,B03=1 | P0,C0 | Add(P,1); Check(P×1) | Một click thêm đúng một dòng P, q=1, đơn giá/thành tiền/tổng 30.000.000; có phản hồi và cột/nhãn R03/R07. S1/S2 |
| CART-W03 | Domain; R01,R04,R09/D02,D05 | P0,C0 | Add(P,3) | Một dòng q=3; thành tiền/tổng 90.000.000; đúng giá P. R01/R04/R09 |
| CART-W04 | Domain; R02,R04/D03 | P0,C2 | Add(P,3) | Chỉ một dòng P, q=5, thành tiền/tổng 150.000.000; không replace q=3. R02/R04 |
| CART-W05 | Domain; R01,R04/D04 | P0,C2 | Add(Q,3) | Hai dòng P×2=60.000.000 và Q×3=84.000.000; tổng 144.000.000; P giữ nguyên. R01/R04 |
| CART-W06 | Domain; R02,R04/D03 | P0,C3 | Add(P,3) | Vẫn ba dòng; P×5=150.000.000, Q×3=84.000.000,H×4=24.000.000; tổng 258.000.000. R02/R04; tránh gộp nhầm dòng cuối |
| CART-W07 | Domain; R01,R02,R04/D03,D16 | P0,C0 | Add(P,1), lặp Add(P,1) hai lần qua các lượt điều hướng bình thường | Sau lần 1/2/3: một dòng P, q=1/2/3 và tổng 30/60/90 triệu; mỗi thao tác chỉ cộng 1. R01/R02/R04 |
| CART-W08 | Domain; R01,R03,R04/D04 | P0,C0 | Add lần lượt P,Q,M,H,K, mỗi q=1; Check(C5) | Năm ID/năm dòng, đúng từng tên/giá/q/thành tiền; tổng 113.000.000; không bỏ M/H/K. R01/R03/R04 |
| CART-W09 | Domain; R03,R07/D02 | P0,C1 | Quan sát header bảng, controls và nhãn tổng | Đủ Sản phẩm, Đơn giá, Số lượng với +/−, Thành tiền, Thao tác; nhãn chính xác “Tổng cộng”. R03/R07; ca trình bày độc lập với add |
| CART-W10 | Domain+BVA; R09/D06/B01=0 | P0,C2 | Add(Q,0) | Reject; C2/tổng 60.000.000 giữ nguyên. R09/S2 |
| CART-W11 | Domain; R09/D06 | P0,C2 | Add(Q,−1), nhập dấu trừ ASCII | Reject; C2 giữ nguyên. R09; số âm khác biên 0 |
| CART-W12 | Domain; R09/D07 | P0,C2 | Add(Q,0.5) | Reject; không tạo q=0 hoặc dòng 0 tiền. R09 |
| CART-W13 | Domain; R09/D07 | P0,C2 | Add(Q,1.5) | Reject; không cắt thành q=1. R09 |
| CART-W14 | Domain; R09/D07 | P0,C2 | Add(Q,−0.5), nhập dấu trừ ASCII | Reject; không cắt thành 0/âm. R09 |
| CART-W15 | Domain; R09/D08 | P0,C2 | Xóa hết quantity trên Q rồi bấm Thêm một lần | Reject; không sinh NaN quantity/thành tiền hoặc tự thêm hàng khi chưa có số lượng. R09 |
| CART-W16 | Domain+BVA; R03,R04,A01/D09/B02=2 | P0,C1 | Bấm + trên P một lần | Có nút + theo R03; theo A01 q=2, thành tiền/tổng 60.000.000; R04. Không có control thì không dùng API thay |
| CART-W17 | Domain+BVA; R03,R04,A01/D09/B02=1 | P0,C2 | Bấm − trên P một lần | Có nút −; theo A01 q=1, thành tiền/tổng 30.000.000, còn dòng. R03/R04,A01 |
| CART-W18 | Domain+BVA; R05,A01/D09/B02=0 attempt | P0,C1 | Thử bấm −; nếu bị disable ghi trạng thái; nếu hỏi xóa thì hủy | Theo A01 không xuất hiện q≤0; chặn giảm hoặc hỏi xác nhận rồi hủy giữ C1; không xóa im lặng theo R05. Không yêu cầu duy nhất cách disable |
| CART-W19 | Domain; R05,R04/D10 | P0,C3 | Bấm Xóa Q, quan sát dialog, chọn Hủy | Dialog trước thay đổi; khi đang hỏi và sau hủy vẫn đủ P×2,Q×3,H×4; tổng 168.000.000. R05/R04 |
| CART-W20 | Domain+BVA; R05,R08/D01,D10/B03 1→0 | P0,C1 | Bấm Xóa P; xác nhận đồng ý | Trước đồng ý vẫn còn P; sau đó 0 dòng, có minh họa/thông báo giỏ trống, không giữ 30.000.000. R05/R08 |
| CART-W21 | Domain; R05,R04/D10 | P0,C3, thứ tự thêm P,Q,H | Xóa Q (dòng giữa), đồng ý | Chỉ Q biến mất; P×2,H×4 đúng; tổng 84.000.000. R05/R04; phát hiện xóa nhầm index |
| CART-W22 | Domain; R01,R05,R04/D10,D16 | P0,C3 | Xóa P xác nhận; Add(P,1) qua UI | Sau xóa còn Q×3,H×4 tổng 108.000.000; thêm lại P chỉ q=1, một dòng, tổng 138.000.000; không phục hồi q=2 cũ. R01/R05/R04 |
| CART-W23 | Domain; R06,R08/D01,D11 | P0; hai substep độc lập C0 rồi C1 | Tại mỗi trạng thái bấm Tiếp tục mua sắm; quan sát route và trang đích | Cả hai về trang chủ `/`; giỏ rỗng vẫn có thông báo/minh họa trước click. Không áp chữ nút riêng ngoài R06. S1 |
| CART-W24 | Domain; R01,R04,A04/D05,D12 | P0,C0 | Add(H,1000) | Dữ liệu thử lớn, không là BVA max: nếu nhận, q=1000, thành tiền/tổng chính xác 6.000.000.000 ₫; nếu chặn phải có lý do/giới hạn quan sát được để đối chiếu, chưa kết luận rule max. Không overflow/NaN. R04+A04 |
| CART-W25 | Domain; A04/D05,D12 | P0,C2 | Trên Q thử nhập 9007199254740992 và bấm thêm một lần | Theo A04 chặn hoặc báo rõ không thể xử lý an toàn; không lưu số bị làm tròn hoặc tổng sai. Không coi số này là max nghiệp vụ; oracle đề xuất về biểu diễn JS |
| CART-W26 | Domain; R09,A04/D08 | P0,C2, reset mỗi substep | Trên Q thử gõ/dán `abc`, rồi ba dấu cách; bấm thêm nếu UI cho | Chặn nhập hoặc Reject, C2 nguyên vẹn; không biến thành q mặc định/NaN. R09, cách xử lý lexical theo A04 |
| CART-W27 | Domain khảo sát; A05/D12 | P0,C0 riêng mỗi mẫu | Add(Q,q) với text `2.0`, `2e0`, `+2`, `02`, ` 2 `; ghi chuỗi UI thực giữ lại | Khảo sát có chuẩn hóa/chặn; nếu nhận phải là q=2, tổng 56.000.000, không cắt thành số khác. Chưa có oracle bắt buộc nhận/từ chối từng cú pháp; A05. Không credit coverage validation lexical đã xác nhận |
| CART-W28 | Domain; R02,R04,A07/D04,D12 | P0, fixture riêng X/Y khác ID cùng tên `T04 <b>Hàng thử</b> tên dài tiếng Việt`, giá X=125000,Y=275000 | Dùng UI Add(X,2), Add(Y,3), Add(X,1) | Theo A07 hai dòng theo ID, không gộp theo tên; X×3=375.000,Y×3=825.000,T=1.200.000; tên là văn bản, không chạy markup; R02/R04 cho gộp/số học. Fixture tạo ngoài TC, không sửa SUT |
| CART-W29 | Domain; R06,A02/D11 | P0,C3 | Tiếp tục mua sắm → mở lại giỏ bằng link; Back rồi Forward trong cùng tab, không reload | Về trang chủ theo R06; theo A02 khi quay lại vẫn đúng C3/T=168.000.000, không nhân đôi hàng do điều hướng |
| CART-W30 | Domain; A02/D11 | P0,C3 | Reload trang `/cart` trong cùng phiên/tab | Theo policy đề xuất A02 giữ C3 và tổng 168.000.000; khác biệt persistence là chưa đáp ứng đề xuất, chưa đủ kết luận vi phạm S1 |
| CART-W31 | Domain; R03,R04,A01/D09,D12 | P0,C3 | Bấm + Q một lần, sau đó − H một lần | Theo A01 Q×4=112.000.000, H×3=18.000.000,P×2=60.000.000; T lần lượt 196.000.000 rồi 190.000.000; không chỉnh nhầm dòng. R03/R04 |
| CART-W32 | Domain; R01,R09,R04/D16 | P0,C2 | Add(Q,0) bị chặn; nhập lại q=2, Add một lần | Sau sai C2 nguyên vẹn; sau sửa có P×2,Q×2,T=116.000.000, không giữ lỗi hoặc cộng dữ liệu lần bị từ chối. R01/R09/R04 |
| CART-W33 | Domain; R02,R04,A01/D16 | P0,C2 | Bấm + trên P 3 lần liên tiếp, rồi − 2 lần; đếm đúng 5 click | Theo A01 đạt q=5 rồi 3; cuối T=90.000.000, một dòng, không mất cập nhật/âm/nhân đôi. R02/R04; không mô phỏng retry mạng |
| CART-W34 | Domain+BVA; R01,R09,R04/D05/B01=2 | P0,C0 | Add(P,2) | Một dòng q=2, thành tiền/tổng 60.000.000, phản hồi thêm sau một click; R01/R09/R04 |

## B. API bổ trợ — giữ riêng trạng thái và oracle

| TC ID | Technique / trace | Precondition | Input và steps | Expected và nguồn |
| --- | --- | --- | --- | --- |
| CART-A01 | Domain; R10/D13 | API TU hợp lệ, ghi cart TU trước | GET rồi POST `/api/cart` không Authorization; POST body P,q=1 hợp lệ; GET lại bằng TU | Cả hai request mục tiêu bị từ chối xác thực; cart TU không đổi. R10/S3; không suy từ API sang Web |
| CART-A02 | Domain; R10/D13 | Như A01 | GET rồi POST với `Authorization: Bearer invalid-token`; body P,q=1; GET lại TU | Từ chối token không hợp lệ, không đổi cart TU. R10/S3 |
| CART-A03 | Domain; R10,A03/D13,D14 | AP0 | GET bằng TU | Token user hợp lệ đọc được cart; kết quả giỏ rỗng theo fixture. S3+A03; không đòi token admin |
| CART-A04 | Domain+BVA; A03/D14/B04=1 | AP0 | Post(P,1) | Theo A03 GET có một dòng P×1, dữ liệu đúng và tổng suy ra 30.000.000; không yêu cầu API trả field total chưa có contract |
| CART-A05 | Domain+BVA; A03/D14/B04=2 | AP0 | Post(P,2) | Theo A03 một dòng P×2, thành tiền suy ra 60.000.000; không gọi Web để kiểm chứng API |
| CART-A06 | Domain; A03/D14 | AP1 | Post(P,3) | Theo A03 chỉ một dòng ID P,q=4, thành tiền suy ra 120.000.000; không append/replace |
| CART-A07 | Domain+BVA; A03/D14/B04=0 | AP1 | Post(Q,0) | AR theo A03; AP1 không đổi; không suy FR-06 mặc nhiên là API contract |
| CART-A08 | Domain; A03/D14 | AP1 | Post(Q,−1) | AR theo A03; không có quantity âm |
| CART-A09 | Domain; A03/D14 | AP1 | Post(Q,1.5) | AR theo A03; không truncate thành 1 |
| CART-A10 | Domain; A03/D14 | AP1, reset mỗi substep | Body Q hợp lệ nhưng lần lượt bỏ field quantity, rồi quantity=null | AR từng substep theo A03; AP1 không đổi; missing khác null |
| CART-A11 | Domain; A06/D15 | AP1, reset mỗi substep | POST body Q hợp lệ với quantity lần lượt `"2"`, true, [], {} | Theo policy đề xuất A06 chỉ nhận JSON number nguyên dương, AR các kiểu này; không có contract strict type được xác nhận |
| CART-A12 | Domain; A06/D15 | AP1; xác minh ID z không tồn tại | Post body id=z,name=`T04 Unknown`,price=28000000,quantity=1 | Theo A06 AR, không phát sinh sản phẩm ảo; không giả định z=maxID+1 nếu chưa kiểm tra membership |
| CART-A13 | Domain; A06/D15 | AP0; biết giá thật P=30000000 | POST id P,name đúng,price=1,quantity=2; GET TU | Theo A06 từ chối hoặc dùng giá thật: không có dòng P giá 1; nếu chấp nhận P×2 phải suy ra 60.000.000. Đây là policy giỏ API đề xuất, không mượn FR-08 total_amount làm rule price |
| CART-A14 | Domain; A06/D15 | Hai user TU/TV khác ID; API cả hai rỗng đã GET xác nhận | Post(P,2) bằng TU; GET TU và TV | Theo A06 TU có P×2 còn TV rỗng; không rò/ghi chéo cart. Không yêu cầu Web hai user đồng bộ |

## C. API bổ sung v0.2 — cùng mục tiêu nghiệp vụ với Web

**AP2:** API TU độc lập, POST P×2 ngoài thao tác mục tiêu; GET xác nhận đúng một dòng P×2. **AP3:** chuẩn bị P×2,Q×3,H×4 bằng ba POST ID khác nhau rồi GET đối chiếu cả ba dòng, tổng suy ra 168.000.000 ₫. Đó là fixture API, không phải fixture của Web. Khi fixture không đạt thì ghi blocked, không sửa state nội bộ. Sequence giữ cùng TU giữa các bước; chỉ ca có substep độc lập mới dùng user mới để reset.

Oracle **A03/A06** vẫn là policy API đề xuất, không tự nâng thành requirement xác nhận. **A08** bổ sung A04 sang API: JSON quantity vượt vùng số nguyên an toàn của runtime cần bị từ chối hoặc có phản hồi rõ về giới hạn xử lý; không âm thầm lưu như một quantity được đảm bảo an toàn. A08 là oracle robustness đề xuất, không là max nghiệp vụ. Mọi GET phải quan sát dữ liệu thật; thành tiền/tổng bên dưới là phép suy ra để đối chiếu giá × q, không yêu cầu API phải trả field total.

| TC ID | Technique / trace | Precondition | Input và steps | Expected và nguồn |
| --- | --- | --- | --- | --- |
| CART-A15 | Domain; A03/D02,D05,D14; mục tiêu W03 | AP0 | Post(P,3), GET TU | Một dòng P×3, price=30000000, thành tiền suy ra 90.000.000; dữ liệu khác không phát sinh. A03 |
| CART-A16 | Domain; A03/D03,D14; mục tiêu W04 | AP2 | Post(P,3), GET TU | Chỉ một dòng ID P,q=5, giá không đổi; tổng suy ra 150.000.000; không append hoặc replace thành q=3. A03 |
| CART-A17 | Domain; A03/D04,D14; mục tiêu W05 | AP2 | Post(Q,3), GET TU | P×2 giữ nguyên; thêm đúng Q×3, hai ID/hai dòng; giá đúng từng sản phẩm; tổng suy ra 144.000.000. A03 |
| CART-A18 | Domain; A03/D03,D04,D14; mục tiêu W06 | AP3 | Post(P,3), GET TU | Ba dòng P×5,Q×3,H×4; giữ nguyên Q/H, tổng suy ra 258.000.000; không phụ thuộc thứ tự dòng. A03 |
| CART-A19 | Domain; A03/D03,D14,D16; mục tiêu W07 | AP0, cùng TU cả sequence | Post(P,1) ba lần; GET sau mỗi POST | Sau lần 1/2/3 luôn một dòng ID P, q=1/2/3; tổng suy ra 30/60/90 triệu; không mất/cộng trùng ngoài thao tác đã gửi. A03 |
| CART-A20 | Domain; A03/D04,D14; mục tiêu W08 | AP0, cùng TU | Post lần lượt P,Q,M,H,K, mỗi q=1; GET sau mỗi bước | Mỗi bước thêm một ID mới, giữ nguyên dòng cũ; cuối đủ năm ID/giá/q đúng, tổng suy ra 113.000.000. A03; không kiểm tra cột/nhãn UI bằng API |
| CART-A21 | Domain; A03,A07/D04,D12,D14; phần định danh/dữ liệu W28 | AP0; X/Y fixture khác ID cùng tên, giá 125000/275000 | Post(X,2), Post(Y,3), Post(X,1); GET sau mỗi bước | Sau hai bước có X×2,Y×3 tách theo ID; cuối X×3=375000,Y×3=825000, tổng suy ra 1.200.000; name giữ nguyên chuỗi fixture. A03/A07; API không chứng minh HTML được render an toàn trên Web |
| CART-A22 | Domain robustness; A03,A04/D05,D12,D14; mục tiêu W24 | AP0 | Post(H,1000), GET TU | Nếu nhận: một dòng H,q=1000,price=6000000, tích chính xác 6.000.000.000; nếu chặn phải có phản hồi giới hạn rõ, không sinh dữ liệu sai. A03/A04; không coi 1000 là biên max |
| CART-A23 | Domain robustness; A08/D05,D12,D15; mục tiêu W25 | AP2 | Post(Q,9007199254740992), GET TU | Theo A08: từ chối và giữ AP2, hoặc báo rõ giới hạn xử lý an toàn; không âm thầm xác nhận/lưu quantity này như số nguyên an toàn. Không kết luận max nghiệp vụ từ mẫu này |
| CART-A24 | Domain; A03/D07,D14; mục tiêu W12/W14 | AP2 độc lập mỗi mẫu | Post(Q,0.5), rồi mẫu độc lập Post(Q,-0.5); GET mỗi request | AR từng mẫu, giữ nguyên P×2; không truncate thành 0 hoặc quantity âm. A03; đây là partition phân số, không là BVA với δ=1 |
| CART-A25 | Domain; A06/D08,D15; phần dữ liệu W15/W26 | AP2 độc lập mỗi mẫu | POST Q với quantity lần lượt chuỗi rỗng, `abc`, ba dấu cách; GET mỗi request | Theo A06 từ chối và giữ AP2. Đây là JSON string sai kiểu; không đồng nhất với field Web rỗng hoặc browser chặn ký tự. Missing/null đã có A10 |
| CART-A26 | Domain sequence; A03/D14,D16; mục tiêu W32 | AP2, cùng TU, không reset giữa hai bước | Post(Q,0), GET; sau đó Post(Q,2), GET | Bước sai bị từ chối, cart vẫn P×2; bước hợp lệ thêm đúng Q×2, cuối chỉ P×2,Q×2, tổng suy ra 116.000.000; không giữ dòng q=0 từ bước bị từ chối. A03 |

## Kiểm tra trước bàn giao

60 ID không trùng; mỗi TC có technique, trace, precondition, input, bước, expected và nguồn. Nhóm có assumption/khảo sát giữ nguyên nhãn, không dùng để khẳng định rule có sẵn trong đề. Bản v0.1 có trong commit `475165e`; bản trước mở rộng và kết quả cũ được giữ local ngoài repo. Không thay verdict Web bằng kết quả API; mỗi TC mới có entry/run riêng trong results.json khi thực thi.
