# T04 — Implementation và execution Shopping Cart

Hiện thực **60 TC**: 48 TC v0.1 đã được Vỹ duyệt tại commit `475165e`, cộng A15–A26 trong v0.2 theo yêu cầu bổ sung API và kiểm thử. Nội dung 48 TC cũ giữ nguyên; [design.md](design.md) §6 và [test-cases.md](test-cases.md) mục C ghi phần mới. Kết quả tại [report.md](report.md), nguồn chung [results.json](results.json).

## Code và mapping

- [scripts/run.py](scripts/run.py) đọc nguyên văn năm cột của từng TC từ Markdown, kiểm tra đủ 60 ID duy nhất; không thêm catalogue JSON trùng lặp. Các handler có nhánh cho đủ W01–34/A01–26, kể cả khi precondition ngăn chạy nhánh mục tiêu trên SUT hiện tại.
- W01 empty; W02/03/24/34 Add từ C0; W04–06 gộp/thêm từ C2/C3; W07/08/28 sequence; W09 schema; W10–15/25 invalid; W16–18/31/33 controls; W19–22 delete; W23/29 continue/history; W30 reload; W26/27 lexical; W32 phục hồi invalid. Input/expected lấy từ bộ thiết kế, không dùng implementation SUT làm oracle.
- A01/02 auth; A03 GET empty; A04/05 add; A06 merge; A07–11 quantity/required/type; A12 ID vắng; A13 giá client; A14 hai user. Mỗi ca/substep cần reset dùng user thử mới qua register/login để không restart backend hoặc sửa `userCarts`. JWT chỉ giữ trong bộ nhớ, không ghi result.
- [scripts/report.py](scripts/report.py) render report từ nguồn chung; mỗi hàng có expected/actual/status và link đúng TC/run. Ảnh SUT và trang GitHub issue giữ riêng với capture time trong result. [requirements.txt](requirements.txt) khai báo Playwright; lượt này tái sử dụng venv T03 đã có Chromium.
- [scripts/prepare_fixture.py](scripts/prepare_fixture.py) đóng gói lại đúng thao tác chuẩn bị sản phẩm đã thực hiện qua terminal: chỉ nhận database ngoài repo trong `.runtime`, backup trước khi thêm sản phẩm còn thiếu, không xóa dữ liệu; GET xác minh trước khi xuất manifest. File được viết sau run để tái sử dụng, chưa thực thi lại hoặc ghi thêm fixture lần hai.

## Fixture và trạng thái

Backend cũ trên cổng 3000 đang chạy, source không đổi; dùng lại SQLite runtime T03 và backup trước khi thêm fixture ở `HW02/.runtime/T04-execution-20261020/before-fixture.sqlite`. Chỉ bổ sung năm seed product đã vắng sau fixture T03, cùng X/Y cho W28; không reset category/users/orders và không đổi database Git theo dõi. Web dùng source `frontend-web` nguyên bản, Vite 5173. Manifest local `HW02/.runtime/T04-execution-20261020/services.json` giữ ID/tên/giá và đường dẫn DB, có GET products đối chiếu trước run.

Web fixture chỉ qua UI, context độc lập cho từng TC; C1 dùng nút Home riêng. C2/C3 dùng một click Add chi tiết theo thiết kế; khi không đạt ghi blocked thay vì bấm hai lần hoặc inject state. Vì vậy runner có đủ nhánh nhưng không tuyên bố đã exercise đủ mọi dòng code/test target. Không dùng API cart để dựng hay kiểm chứng giỏ Web.

## Chạy lại

Không có `--execute` thì chỉ đọc/liệt kê TC, không mở browser/gọi SUT/ghi results. Có `--execute` cần fixture manifest đúng, service đang chạy và run ID mới; ID đã tồn tại bị từ chối. Chọn `--case` để chỉ rerun ca cần thiết; history giữ nguyên, summary chọn kết quả mới theo ID.

```powershell
python tests/hw02/fr07-cart/scripts/run.py
python tests/hw02/fr07-cart/scripts/run.py --execute --manifest ../.runtime/T04-execution-20261020/services.json --run-id CART-RUN-NEW --case CART-W02
python tests/hw02/fr07-cart/scripts/report.py
```

Lượt thực tế dùng Python tại `HW02/.runtime/T03-execution-20261020/venv/Scripts/python.exe`. Không ghi password/token vào manifest. Nếu replay ở máy khác cần chuẩn bị runtime fixture tương đương, cập nhật ID qua GET và giữ đúng giá/input của thiết kế; không import `database.js` vào database có dữ liệu cần giữ vì module tự reset seed.

## Lịch sử harness và kiểm chứng

CART-RUN-01 smoke năm ca; phát hiện harness chỉ đợi URL SPA nên có observation trước DOM commit. Thêm chờ heading Giỏ, rerun các ca smoke trong RUN02; giữ kết quả cũ. RUN02 dừng tại W28 vì có hai h2 cùng tên trên Home; sửa locator đợi h1 chi tiết. RUN03 chạy W28–34 và API. Thay đổi chỉ ở runner, không thay TC hoặc logic SUT. Summary cuối: **6 passed, 19 failed, 23 blocked, 0 not_run**; 25 executed và 23 chưa thực thi được target.

Sau RUN03, thêm ghi nhận alert/quantity-error cho handler invalid để tránh hardcode feedback thất bại nếu tái dùng runner sau này. Các handler invalid Web hiện bị chặn ở precondition, nên không đổi verdict đã chọn; source hash trong mỗi run giữ đúng bản lúc chạy. Không ghi đây là lần chạy mới.

Không lấy empty cart do click no-op thành validation pass, không claim đã thử q invalid trong các ca bị C2 chặn. W27 khảo sát biểu diễn bị lỗi click đầu che nên blocked. Report ghi rõ phần rule/domain/BVA đã exercise và phần chưa tới; API A03/A06 là policy giả định. Ảnh và GitHub Issues được hoàn thiện ở bước report; không tự commit/push hay ghi AI Audit trong task này.

## Mở rộng API v0.2 — CART-RUN-04

Thêm A15–A26 vào thiết kế trước khi chạy; không đổi expected hoặc kết quả 48 TC trước. Runner đồng bộ catalogue bằng append ID mới, kiểm tra các trường của TC cũ vẫn khớp nguồn, tổng TC lấy từ dữ liệu thay vì hardcode 48. Mỗi case mới có request/response/GET trước–sau; các substep reset dùng user mới, riêng sequence giữ nguyên TU.

| Nhánh | Mục tiêu / mapping |
| --- | --- |
| A15–A18 | P×3; P2+P3; P2+Q3; AP3+P3, khớp W03–W06 |
| A19–A21 | Thêm P1 ba lần; đủ năm seed; X/Y cùng tên khác ID rồi thêm X, tương ứng nghiệp vụ W07/W08/W28 |
| A22–A25 | q=1000; unsafe integer theo A08; ±0.5; string rỗng/chữ/space, tách API representation với Web |
| A26 | AP2 → Q0 sai → Q2 hợp lệ trong cùng TU, đối chiếu cả bước sai và trạng thái cuối |

RUN04 chạy riêng 12 TC mới: **4 passed (A15/A17/A20/A22), 8 failed**, không blocked/not_run. Tổng **60 TC: 10 passed, 27 failed, 23 blocked**; Web giữ 0/11/23, API 10/16/0. Thêm đúng hai JPG response đại diện A16/A23; các TC khác có log/assertions riêng và dùng cùng finding merge/validation. Cập nhật issue #17/#18 với kết quả mới và ảnh trang issue sau cập nhật; không nhân số bug theo số TC failed. Chi tiết URL, capture time và log trong results.json/report.

Snapshot trước mở rộng được giữ local tại `HW02/.runtime/design-baselines/fr07-before-api-expansion-20261020/`. Source hash của design/TC/runner lúc RUN04 lưu trong run; 48 entries execution cũ không bị ghi đè. Phần API không credit các bước UI hoặc tạo endpoint cart chỉnh/xóa chưa có contract. Không tự ghi AI Audit, commit/push trong lượt mở rộng.
