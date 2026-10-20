# Các phiên bản artifact để đối chiếu

Các bản đã có trong lịch sử Git được dẫn tới đúng commit, gồm cả khi nội dung hiện tại đã thay đổi. Thư mục `history/` giữ output ban đầu chưa từng commit và phần thay đổi cần đọc cùng audit. Nội dung prompt/phản hồi gốc nằm trong [Prompt Log](23120410_HW02_PromptLog.md); nhận xét ở [AI Audit Report](ai-audit.md).

## A-00 — Quy trình và skill AI log

Output ban đầu và bản sửa được trích nguyên văn trong audit, mục 3.1–3.4. Skill kỹ thuật đã có tại [commit 6fb3d52](https://github.com/tranquocvy/eshop-sut/tree/6fb3d52/skills/course-ai-log). Kiểm tra helper trong [output công cụ](verification/ai-log-helper.txt).

## A-01 — Skill Domain Testing/BVA

- [Bản gộp trước khi tách — 58481f4](https://github.com/tranquocvy/eshop-sut/tree/58481f466d78ed0f5801bfbc64a676006d2beac2/skills/domain-bva-testing).
- [Bản chỉ thiết kế — ddcacdf](https://github.com/tranquocvy/eshop-sut/tree/ddcacdf72a041aca8fb37325d3c26b4e6290840e/skills/domain-bva-testing).
- Đã đối chiếu toàn bộ file của hai snapshot cũ với các commit tương ứng; chỉ khác xuống dòng CRLF/LF nếu có.

## A-02 — Skill execution/reporting

- [Bản có evidence/JPG — 8018b73](https://github.com/tranquocvy/eshop-sut/tree/8018b73e9e0d9066efdb1ffe3512303e033a6cb4/skills/test-execution-reporting).
- [Bản thu gọn — cbf1ba9](https://github.com/tranquocvy/eshop-sut/tree/cbf1ba939c9a0b41281ccc1f053096ee60035897/skills/test-execution-reporting).
- [Thay đổi giữa hai mốc](https://github.com/tranquocvy/eshop-sut/compare/8018b73e9e0d9066efdb1ffe3512303e033a6cb4...cbf1ba939c9a0b41281ccc1f053096ee60035897); [kết quả kiểm tra helper](verification/design-execution-helpers.txt).

- Bổ sung GitHub/evidence theo P-027/P-028/P-030, đã lưu tại **commit local `e1fe254040122e449ff184412853f9a8a0d72059`**: [SKILL.md](../../../skills/test-execution-reporting/SKILL.md), [quy trình GitHub](../../../skills/test-execution-reporting/references/execution-and-bugs.md), [report contract](../../../skills/test-execution-reporting/references/report-contract.md), [evidence](../../../skills/test-execution-reporting/references/evidence.md), [template](../../../skills/test-execution-reporting/assets/feature-report.template.md). Bản trước thay đổi nằm tại commit `6631d92`; không sao chép thêm toàn bộ skill vào hồ sơ AI. P-030 chỉ sửa hướng dẫn, chưa áp dụng lại lên report.

## A-03 — Thiết kế Mobile Account Registration

- AI đầu v0.1, 46 TC: [design nguyên văn](history/mobile-registration-v0.1-design.md.txt), [TC nguyên văn](history/mobile-registration-v0.1-test-cases.md.txt).
- Bản v0.3 đã review, 54 TC: [design](https://github.com/tranquocvy/eshop-sut/blob/5ca63e1dadc0c69cd4a52b892f2c5a1dc1ff5d59/tests/hw02/mobile-registration/design.md), [TC](https://github.com/tranquocvy/eshop-sut/blob/5ca63e1dadc0c69cd4a52b892f2c5a1dc1ff5d59/tests/hw02/mobile-registration/test-cases.md).
- [Diff v0.1 → v0.3](history/mobile-design-changes.diff).

## A-04 — Code test Mobile Account Registration

[Bộ implementation tại b8b1d2b](https://github.com/tranquocvy/eshop-sut/tree/b8b1d2b18203a0ebf0a24352890da1e80fc0d5fc/tests/hw02/mobile-registration) giữ `IMPLEMENTATION.md`, catalogue, thao tác native và runner nguyên bản. Đánh giá implementation gắn với mốc này; thay đổi execution sau đó được ghi riêng ở A-05.

## A-05 — Execution và report Mobile Registration

- [Kết quả run đầu chưa từng commit](history/mobile-initial-results.json): 18 pass, 9 fail, một blocked; TC29 dở dang.
- [Report](https://github.com/tranquocvy/eshop-sut/blob/62e34ecbcce65a8c803625ca8d210dfd9176dbbe/tests/hw02/mobile-registration/report.md), [results](https://github.com/tranquocvy/eshop-sut/blob/62e34ecbcce65a8c803625ca8d210dfd9176dbbe/tests/hw02/mobile-registration/results.json) và [ảnh](https://github.com/tranquocvy/eshop-sut/tree/62e34ecbcce65a8c803625ca8d210dfd9176dbbe/tests/hw02/mobile-registration/images) tại `62e34ec`: 35 pass, 15 fail, bốn blocked.
- [Thay đổi từ implementation tới harness đã sửa](https://github.com/tranquocvy/eshop-sut/compare/b8b1d2b18203a0ebf0a24352890da1e80fc0d5fc...b1c122bd0f00bc982d19093abad0776f0434d04e).

- Bản trước bổ sung Issues (`62e34ec`) được đánh giá **INCOMPLETE** về phần hồ sơ GitHub theo §6.4/§14, dù kết quả execution vẫn được giữ. P-029 đã bổ sung **8 issue, 14 ảnh lỗi hiển thị và 9 JPG trang/danh sách issue**, không chạy lại SUT.
- Mốc bổ sung file đã commit local `e1fe254040122e449ff184412853f9a8a0d72059`: [report](../../../tests/hw02/mobile-registration/report.md), [results/log thao tác](../../../tests/hw02/mobile-registration/results.json), [ảnh tổng quan](../../../tests/hw02/mobile-registration/images/MR-GitHub-issues.jpg). Tám ảnh riêng có tên `MR-BUG01-issue.jpg` đến `MR-BUG08-issue.jpg`, được dẫn trong từng bug của report. File mốc này còn có các sửa report sau bốn lượt được chọn; không gán những sửa đó cho P-029/P-030.
- Đăng trên tracker: [#1](https://github.com/tranquocvy/eshop-sut/issues/1), [#2](https://github.com/tranquocvy/eshop-sut/issues/2), [#3](https://github.com/tranquocvy/eshop-sut/issues/3), [#4](https://github.com/tranquocvy/eshop-sut/issues/4), [#5](https://github.com/tranquocvy/eshop-sut/issues/5), [#6](https://github.com/tranquocvy/eshop-sut/issues/6), [#7](https://github.com/tranquocvy/eshop-sut/issues/7), [#8](https://github.com/tranquocvy/eshop-sut/issues/8). MR-BUG05–08 ghi rõ sai khác S7. Dùng link tương đối cho các file commit local, không mặc định commit đã được push lên GitHub.

## A-06 — Thiết kế Category Management

- AI đầu v0.1, 24 TC: [design nguyên văn](history/category-v0.1-design.md.txt), [TC nguyên văn](history/category-v0.1-test-cases.md.txt).
- Bản v0.2 đã review, 33 TC: [design](https://github.com/tranquocvy/eshop-sut/blob/b84417b841f7a1bd5d20386132a0f333d7487fb1/tests/hw02/fr14-categories/design.md), [TC](https://github.com/tranquocvy/eshop-sut/blob/b84417b841f7a1bd5d20386132a0f333d7487fb1/tests/hw02/fr14-categories/test-cases.md).
- [Diff v0.1 → v0.2](history/category-design-changes.diff). Toàn bộ TC Category mang trạng thái Not Run tại mốc thiết kế này; execution sau đó được ghi riêng tại A-08.

Các file `.md.txt` giữ nguyên byte của output Markdown ban đầu; phần mở rộng giúp đọc nguyên văn các đường dẫn lịch sử trong output. Bản sửa được dẫn tới Git đúng phiên bản. Các file diff giữ nguyên bản đã lưu trước khi tái cấu trúc. Dữ liệu đồng bộ, hash và metadata được giữ local trong `_data/`.

## A-07 — Code test T03 Category Management

- [P-031](23120410_HW02_PromptLog.md#msg-078e737e05a56044cac5) yêu cầu triển khai 33 TC từ design/test-cases v0.2, chưa chạy SUT hay viết report ở lượt implementation.
- [Output implementation ban đầu](history/category-implementation-initial.txt) giữ nguyên nội dung runner và IMPLEMENTATION.md ở cuối lượt từ patch công cụ thật. Catalogue và requirements không thay đổi trong execution, được giữ tại commit local `94fd43c`.
- [Runner hiện hành](../../../tests/hw02/fr14-categories/scripts/run.py), [catalogue 33 TC](../../../tests/hw02/fr14-categories/scripts/cases.json), [requirements](../../../tests/hw02/fr14-categories/requirements.txt), [IMPLEMENTATION.md](../../../tests/hw02/fr14-categories/IMPLEMENTATION.md): mốc `94fd43c`.
- [Diff implementation → execution](history/category-implementation-execution.diff) đánh dấu thay đổi harness: đóng kết nối SQLite, chỉ yêu cầu tài khoản liên quan đến precondition, nhận diện feedback từ chối, bỏ chờ Response.finished thừa, ghi body API và JPG lỗi. Không đổi bộ input/expected hoặc nghiệp vụ SUT.

## A-08 — Execution và report T03 Category Management

- [P-032](23120410_HW02_PromptLog.md#msg-ecff2281e0534402997b) giao chạy bộ 33 TC theo skill test-execution-reporting. [Report](../../../tests/hw02/fr14-categories/report.md), [results.json](../../../tests/hw02/fr14-categories/results.json) và [ảnh tổng quan issue](../../../tests/hw02/fr14-categories/images/CAT-GitHub-issues.jpg) giữ tại commit local `94fd43c`.
- CAT-RUN-01 chạy TC01; CAT-RUN-02 chạy TC02–33. Kết quả unique: **25 pass, 8 fail, 0 blocked, 0 not_run**. Mỗi dòng có link log đúng TC/run; 8 JPG actual của ca fail, 3 JPG trang issue và 1 JPG danh sách.
- Ba bug: [#9 — tên rỗng/thiếu/null](https://github.com/tranquocvy/eshop-sut/issues/9), [#10 — user JWT được POST/PUT/DELETE](https://github.com/tranquocvy/eshop-sut/issues/10), [#11 — Admin khôi phục phiên từ user token](https://github.com/tranquocvy/eshop-sut/issues/11). Log tạo/xác minh/chụp trong `bugs[].github_activity`; ảnh SUT và ảnh trang issue là hai loại bằng chứng riêng.
- Giữ cảnh báo teardown `Target closed` của RUN01 và thay đổi harness trước RUN02; không tự retry mutation hoặc đổi verdict để làm xanh. Coverage exercise 7/7 rule, 19/19 mục tiêu miền, 6/6 BVA items chỉ áp dụng inventory đã duyệt; PUT mới kiểm tra quyền, không nhận đã kiểm thử nghiệp vụ Update đầy đủ.
- Sinh viên đã nói “tôi đã kiểm tra report rồi, commit cho t03 đi”; dùng làm căn cứ review report và mốc commit, không thêm lượt này vào hai prompt được chọn ghi log. Không mặc định mốc local đã push lên GitHub.

## A-09 — Thiết kế T04 Shopping Cart

- [P-033](23120410_HW02_PromptLog.md#msg-fbcf3eb8ed26537524e3) giữ nguyên prompt và đủ bốn phản hồi AI ngày 20/10/2026, 15:28:20–15:32:30 (UTC+7).
- AI đầu v0.1: [design nguyên văn](history/cart-v0.1-design.md.txt), [TC nguyên văn](history/cart-v0.1-test-cases.md.txt). Bản sao giữ byte đầu ra trước cập nhật trạng thái review.
- Hai file đã được Vỹ đọc và xác nhận, commit local `475165e35a7c13988abf86bc10a988ab7a6b34f1`: [design](../../../tests/hw02/fr07-cart/design.md), [test cases](../../../tests/hw02/fr07-cart/test-cases.md). Tại mốc này chỉ sửa ghi chú review; 48 TC và expected giữ nguyên. Execution và mở rộng API về sau được dẫn ở phần tiếp theo; chưa mặc định commit đã push.
- 34 TC Web và 14 TC API bổ trợ; cả năm sản phẩm seed, phép tính cố định, 16 mục tiêu miền, bốn inventory biên tách requirement/assumption. Tất cả Not Run tại mốc thiết kế v0.1; execution về sau thuộc A-10, không thay lịch sử mốc này.
- Căn cứ review lúc 15:35:30 (UTC+7): “tôi đã đọc và xác nhận các tc hiện có. Tôi không thấy mục nào cần tôi verify, done?” Lời này không được thêm thành prompt mới ngoài phạm vi P-033; không suy thành đã chạy test hoặc xác nhận mọi giả định là requirement.

### A-09 — Mở rộng API v0.2 theo góp ý

- [P-036](23120410_HW02_PromptLog.md#msg-eb9325eff0dd943647c7) yêu cầu bổ sung TC API và kiểm thử; [góp ý/chỉnh sửa](23120410_HW02_PromptLog.md#t04-review-notes) giữ phần sinh viên phản biện đổi click, nguồn đặc tả và ánh xạ Web/API.
- [Design v0.2](../../../tests/hw02/fr07-cart/design.md), [60 TC](../../../tests/hw02/fr07-cart/test-cases.md), commit local `ee8e477edc30e3ddfed85c10fc5f82cb006ce15a`: thêm A15–A26, tổng 34 Web + 26 API. 48 hàng TC cũ giữ nguyên; §6 có mapping mục tiêu/miền → hiện thực theo layer/fixture.
- R01 được làm rõ nguồn: “sau khi bấm” là câu đặc tả; “đúng một click” là cụ thể hóa thao tác của TC. Không đổi bước/verdict Web sang double-click. A08 của API là oracle robustness đề xuất, không là max nghiệp vụ.
- Bản v0.1 đã được sinh viên đọc và xác nhận; không suy việc yêu cầu commit là đã review riêng mọi TC mới hoặc đã tự chạy toàn bộ suite.

## A-10 — Implementation, execution và report T04 Shopping Cart

- [P-034](23120410_HW02_PromptLog.md#msg-18993f7783fd6fec1999) giao implement/chạy T04; [P-035](23120410_HW02_PromptLog.md#msg-e35ac4755d97d4df1251) yêu cầu kiểm chứng một ca blocked; P-036 mở rộng API. Bản đọc rút gọn theo yêu cầu, không phải transcript đầy đủ.
- [Report v0.1 nguyên văn](history/cart-execution-v0.1-report.md.txt), được giữ từ snapshot trước mở rộng: 48 TC, 6 passed, 19 failed, 23 blocked; 9 issue/finding #12–#20. Kết quả 48 TC và history RUN01–03 vẫn có nguyên trong results.json hiện hành; đã so sánh trước/sau.
- Bản cuối commit local `ee8e477edc30e3ddfed85c10fc5f82cb006ce15a`: [IMPLEMENTATION](../../../tests/hw02/fr07-cart/IMPLEMENTATION.md), [runner](../../../tests/hw02/fr07-cart/scripts/run.py), [report](../../../tests/hw02/fr07-cart/report.md), [results.json](../../../tests/hw02/fr07-cart/results.json), ảnh liên kết trong report. RUN04 chỉ chạy 12 API mới: 4 passed, 8 failed. Tổng 60 TC: **10 passed, 27 failed, 23 blocked, 0 not_run**; Web 0/11/23, API 10/16/0.
- Giữ các lỗi harness và lần chạy cũ; không dùng API thay bằng chứng Web hoặc lấy blocked làm pass. Vỹ cho biết tự thêm được bằng double-click; runner vẫn giữ bước đã duyệt. Không ghi Vỹ tự chạy 60 TC hoặc đã review toàn report chỉ vì yêu cầu commit.
- Bổ sung evidence vào [#17 — gộp](https://github.com/tranquocvy/eshop-sut/issues/17#issuecomment-6287988816), [#18 — quantity](https://github.com/tranquocvy/eshop-sut/issues/18#issuecomment-6288012955); có response JPG và JPG trang issue sau cập nhật. Không tạo issue trùng cho mỗi TC failed.

Ghi nhận review T04 ngày 20/10/2026: Vỹ xác nhận đã kiểm tra hồ sơ và yêu cầu chốt T04. Kết quả 10 passed, 27 failed, 23 blocked giữ nguyên; không có yêu cầu verify lại đang chờ. Không suy việc review hồ sơ thành sinh viên tự chạy toàn bộ suite.

## A-11 — Thiết kế T05 FR-02 Login and Account Lockout

- [P-037](23120410_HW02_PromptLog.md#msg-4a94eeb3d11f70a2ae18), 19:09:05–19:11:44 ngày 20/10/2026 (UTC+7): sinh hai file design/TC, bốn phản hồi AI nguyên văn. [P-038](23120410_HW02_PromptLog.md#msg-e61152050f4f4050c8e4), 19:21:18–19:21:43: Vỹ xác nhận review và yêu cầu gộp/push một commit; ba phản hồi AI nguyên văn.
- Bản AI đầu từ commit cũ `2e535cd` (còn đọc được trong Git local): [design](history/fr02-v0.1-design.md.txt), [test cases](history/fr02-v0.1-test-cases.md.txt). Giữ nguyên nội dung gốc, không thay bằng file cuối có nhãn đã review. Hai commit đầu `e6836d8`/`2e535cd` được Codex tự tạo khi chưa được Vỹ cho phép; Vỹ phản đối và Codex thừa nhận lỗi.
- Sau ủy quyền cụ thể ở P-038, Codex gộp hai file thành `b3f0f6d` và push. Vỹ phát hiện hai file vẫn ghi chờ review, yêu cầu sửa; bản cuối [design](https://github.com/tranquocvy/eshop-sut/blob/4bb5158fd5d550f201eb1c3d8ce2a47c7dfae509/tests/hw02/fr02-login/design.md), [TC](https://github.com/tranquocvy/eshop-sut/blob/4bb5158fd5d550f201eb1c3d8ce2a47c7dfae509/tests/hw02/fr02-login/test-cases.md) tại `4bb5158` được amend/force-with-lease lên origin/main. [Diff trạng thái review](history/fr02-review-status.diff) giữ thay đổi thật, không đổi dữ liệu/expected.
- 45 TC unique: 19 Web, 26 API; 13 mục tiêu miền; B01 số lần sai 2/3/4 và B02 thời gian 29.999/30/30.001s. Method profile reference-provisional, sáu boundary items/lớp là coverage thiết kế; Not Run tại mốc thiết kế.
- [Năm lượt làm rõ/sửa nguyên văn](history/fr02-review-context.md) giữ câu hỏi về phạm vi, BVA, rule/oracle và trạng thái review. Không tính các trao đổi này thành artifact riêng hay thêm mã P ngoài hai prompt đã chọn.
- Vỹ xác nhận report execution lúc 19:40:43 ngày 20/10/2026: “tôi đã check report rồi, tôi confirm.” Đây là dữ kiện review; không suy sinh viên tự chạy suite, không thêm prompt execution/report hoặc artifact execution vào phạm vi log được chỉ định lần này.

## A-12 — Implementation, execution và report T05 FR-02

- [P-039](23120410_HW02_PromptLog.md#msg-b06191d493ae9fd1411e) giữ nguyên yêu cầu execution/report ngày20/10/2026, 19:23:50–19:35:57 (UTC+7), gồm sáu phản hồi tiến độ và kết quả cuối. [P-040](23120410_HW02_PromptLog.md#msg-96c5bfd21eb522b4817c), 19:52:25–19:52:43, giữ lời Vỹ xác nhận đã kiểm tra report/yêu cầu commit cùng hai phản hồi AI.
- Bộ được audit tại commit local `911185eb93209050b6b5ab6a53499b403db29212`: [report](../../../tests/hw02/fr02-login/report.md), [results.json](../../../tests/hw02/fr02-login/results.json), [IMPLEMENTATION](../../../tests/hw02/fr02-login/IMPLEMENTATION.md), [run.py](../../../tests/hw02/fr02-login/scripts/run.py), [verify.py](../../../tests/hw02/fr02-login/scripts/verify.py), [report.py](../../../tests/hw02/fr02-login/scripts/report.py) và16 JPG được report dẫn chiếu. Không sao chép cả bộ đã có trong Git vào history; không mặc định commit local đã push.
- 45 TC unique:18 passed/12 failed/15 blocked/0 not_run; Web19 TC=9/3/7, API26 TC=9/9/8. Executed30, chưa exercise trọn target15; pass rate60% trên30 executed. Summary chọn RUN03; RUN01/RUN02 giữ trong results, không cộng thành TC mới. VERIFY01 là repro bổ trợ, không tăng số TC.
- 9 blocked do SUT chặn Fn/success sequence; 6 blocked thiếu clock server ±1ms. Không tự ép precondition/đổi thao tác, không lấy API thay Web, không dùng request sau 31s để nhận equality30s. Deadline khoảng 180s được đối chiếu với timestamp request và response sau 31s.
- Ba defect confirmed: [#21 counter](https://github.com/tranquocvy/eshop-sut/issues/21), [#22 thời lượng](https://github.com/tranquocvy/eshop-sut/issues/22), [#23 email HTML5](https://github.com/tranquocvy/eshop-sut/issues/23). Ba finding assumption: [#24 A02](https://github.com/tranquocvy/eshop-sut/issues/24), [#25 A04](https://github.com/tranquocvy/eshop-sut/issues/25), [#26 A01](https://github.com/tranquocvy/eshop-sut/issues/26). Mỗi issue có ảnh symptom thực và JPG trang issue, timestamp/link nằm trong report/results. API symptom là API client harness thật, không phải UI EShop.
- Vỹ xác nhận đọc report lúc 19:40:43 và tại P-040 tiếp tục xác nhận trước khi yêu cầu commit. Codex sửa locator/encoding harness, thao tác Web/API/DB, đăng/chụp issue và commit theo yêu cầu; không ghi sinh viên tự chạy suite hoặc tự sửa runner. Các sửa harness/phiên bản run có sẵn trong nguồn chung, không tạo lại bản “ban đầu” giả.
- Đây là đợt bổ sung log execution sau khi hai prompt thiết kế/Git đã được ghi ở A-11. Ghi chú phạm vi của đợt trước được giữ như lịch sử; hiện P-039/P-040 đã được bổ sung. Nhận xét/verdict A-12 mới là đề xuất để Vỹ rà soát hồ sơ AI.
