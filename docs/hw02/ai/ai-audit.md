**Khoa Công nghệ Thông tin (FIT) – Trường Đại học Khoa học Tự nhiên (HCMUS)**

**Kiểm chứng Phần mềm (AI-augmented · 2026)**

**CHÍNH SÁCH AI · BIỂU MẪU — 2026 v1.0**

# AI Audit Report — HW02

*Biểu mẫu được FIT@HCMUS điều chỉnh từ Med Kharbach, PhD (2026), AI Use Policy Templates for Higher Education. Giấy phép CC BY-NC-SA 4.0.*

> Audit gồm ba artifact skill, thiết kế, implementation và kết quả/report Mobile Registration, cùng bộ thiết kế Category Management. Nhận xét/verdict A-00–A-03, A-05 và A-06 là đề xuất để sinh viên rà soát; A-04 giữ quyết định chấp nhận đầu ra ở bước implementation. A-06 đánh giá bản AI v0.1 còn thiếu, đồng thời giữ bản v0.2 đã được sinh viên đọc và yêu cầu commit.

## 1. Thông tin sinh viên

| Mục | Giá trị |
| --- | --- |
| Họ tên sinh viên (in hoa) | TRẦN QUỐC VỸ |
| MSSV | 23120410 |
| Lớp / Khóa | 23_3 |
| Mã bài tập | HW02-AI |
| Tên bài tập | Domain Testing on EShop |
| Ngày sử dụng AI | 19–20/10/2026 |
| Công cụ AI đã dùng | OpenAI Codex, model gpt-6.1-sol |
| Có sử dụng AI | Có |

## 2. Phạm vi ghi nhận

Phạm vi hiện có 31 mục P-000–P-030: các lượt xây/sửa skill, thiết kế và review Mobile Registration, triển khai code, execution, cải thiện report/evidence và thiết kế Category Management. P-024–P-026 ghi ba lượt Category; P-027–P-030 ghi bốn lượt bổ sung GitHub Issues/evidence và sửa skill được sinh viên chỉ định:

- **A-00 — Skill AI log:** [P-000](23120410_HW02_PromptLog.md#msg-55324f24f7a915146521) tạo skill, [P-001](23120410_HW02_PromptLog.md#msg-badc52515014adae1a4b) góp ý theo HW01 và [P-002](23120410_HW02_PromptLog.md#msg-3c20cea85631833613dd) mở rộng dùng chung.
- **A-01 — Skill Domain/BVA:** [P-003](23120410_HW02_PromptLog.md#msg-d9b48702e80bca216e2a) nghiên cứu và xây skill; [P-004](23120410_HW02_PromptLog.md#msg-c8655ff83338222bdb54) hỏi về execution; [P-005](23120410_HW02_PromptLog.md#msg-0d15905a7329be883e67) yêu cầu tách; [P-006](23120410_HW02_PromptLog.md#msg-c64a4bbe130b7d5e67a2) kiểm tra việc giữ phương pháp thiết kế.
- **A-02 — Skill execution/reporting:** được tách ở P-005, bổ sung evidence và JPG theo [P-007](23120410_HW02_PromptLog.md#msg-cc0d880e4ef9adbe98cd).

- **A-03 — Thiết kế Domain/BVA cho Mobile Account Registration:** [P-008](23120410_HW02_PromptLog.md#msg-9c5d57863614170c8ab0) sinh bộ test; [P-009](23120410_HW02_PromptLog.md#msg-1419f914508254329f1b) giải thích phương pháp và bước triển khai; [P-010](23120410_HW02_PromptLog.md#msg-57da3f9386c61457d81e) giải thích cách đọc; [P-011](23120410_HW02_PromptLog.md#msg-4873da5fa8bbf9630f5b) review cùng [P-012](23120410_HW02_PromptLog.md#msg-84ee0558719d3db513aa) trả lời làm rõ; [P-013](23120410_HW02_PromptLog.md#msg-4f7fab8add7e9c9a7096) và [P-014](23120410_HW02_PromptLog.md#msg-9b5e6837d82871732b9f) xác định cách dùng đặc tả, giả định và phạm vi.

- **A-04 — Code test Mobile Account Registration:** [P-015](23120410_HW02_PromptLog.md#msg-dc4f2e51b024238929a8) yêu cầu triển khai từ hai file đã duyệt, chưa thực thi code.

- **A-05 — Execution và report Mobile Registration:** [P-016](23120410_HW02_PromptLog.md#msg-ecfe30f8f95eb2cc71f0)–[P-023](23120410_HW02_PromptLog.md#msg-b9e49c78a2be320ca739); gồm review flow, thu gọn evidence/kết quả, bỏ PDF và chạy tiếp. Cập nhật skill A-02 gắn với [P-020](23120410_HW02_PromptLog.md#msg-e0dc57e10128c538b2f0) và [P-022](23120410_HW02_PromptLog.md#msg-844b978b0d8d18b2a3ed).

- **A-06 — Thiết kế Domain/BVA cho T03 Category Management:** [P-024](23120410_HW02_PromptLog.md#msg-2642f1f9f300cb746a59) sinh bộ test; [P-025](23120410_HW02_PromptLog.md#msg-7dffe02b118443b22b9a) rà lại độ đầy đủ theo đặc tả/phương pháp; [P-026](23120410_HW02_PromptLog.md#msg-7614bb5c1dae4235dc44) yêu cầu bổ sung BVA API, token bị sửa payload/chữ ký và mở lại Admin từ token user đã lưu.

**Bổ sung A-02/A-05:** [P-027](23120410_HW02_PromptLog.md#msg-36be906c669996d7cbf9) phát hiện Mobile chưa có issue; [P-028](23120410_HW02_PromptLog.md#msg-0453443a1aeea0f60e1a) yêu cầu sửa skill và chụp trang issue; [P-029](23120410_HW02_PromptLog.md#msg-f3b061c972ae96d0c800) giao đăng issue/lưu JPG và log; [P-030](23120410_HW02_PromptLog.md#msg-335afed53aaee172819f) yêu cầu skill bắt link evidence cho mỗi TC đã chạy. Bốn lượt có 12 phản hồi AI. Các lượt sửa report, giải thích log và commit tiếp theo không được thêm thành prompt trong phạm vi lần này; commit `e1fe254` chỉ được dùng làm mốc phiên bản file đã có.

Toàn bộ trao đổi nằm trong [Prompt Log](23120410_HW02_PromptLog.md). Mã P giữ ổn định theo lần bổ sung log; thời gian của từng lượt cho biết thứ tự trao đổi thực tế. Prompt đầu tiên của A-00 được giữ nguyên văn trong bảng audit dù sinh viên đã rút gọn phần mở đầu trong bản đọc Prompt Log.

Các trích output A-00 đã che đường dẫn tới skill cá nhân; phần còn lại giữ nguyên. Với hai skill kỹ thuật dùng để nộp, [các phiên bản artifact](artifacts.md) giữ cả bản trước và sau khi tách.

## 3. Bảng audit — một hàng mỗi artifact

| (1) Prompt + Công cụ | (2) Output AI | (3) Verdict | (4) Lý do / nguồn đối chiếu | (5) Bản SV sửa |
| --- | --- | --- | --- | --- |
| **A-00 — Quy trình và skill tự điền AI log**<br><br>**Tool:** OpenAI Codex<br>**Thời gian:** 19:15:38 19/10/2026 (UTC+07:00)<br>**Prompt ID:** [P-000](23120410_HW02_PromptLog.md#msg-55324f24f7a915146521)<br>**Prompt:** “như này căng quá nhỉ, đề rất khuyến khích việc tạo skill để thực hiện các việc này. Trước hết, hãy xem lại các qui định về ai log các file ai template để sinh ra 1 skill mà đề nhắc đến, tức là tự điền vào log”<br><br>Rà soát: [P-001](23120410_HW02_PromptLog.md#msg-badc52515014adae1a4b). Yêu cầu sửa: [P-002](23120410_HW02_PromptLog.md#msg-3c20cea85631833613dd). | Bản đầu `hw02-ai-log` hỗ trợ Prompt Log, AI-02 và AI-03. Output kết quả được chép tại **3.1**; bản sửa thành `course-ai-log` tại **3.2**. | **INCOMPLETE** — đánh giá phiên bản đầu | Bản đầu tự động hóa việc ghi dữ liệu nhưng phần trình bày đưa ID nguồn, hash và thông tin trích xuất vào bản đọc; bảng audit lặp nhiều trạng thái chờ, phần khai báo thiếu tự nhiên. Sinh viên đã đọc đầu ra và yêu cầu đối chiếu với HW01 tại P-001. Đề HW02 §9 yêu cầu tool, thời gian, prompt và output; AI-02 §3 yêu cầu đánh giá từng artifact; AI-03 câu 4–5 yêu cầu mô tả đóng góp và cách xác minh cụ thể [1]–[3]. Các thông tin kỹ thuật phục vụ đối chiếu cần được giữ riêng để biểu mẫu dễ đọc hơn. | Sinh viên cung cấp mẫu HW01, nêu điểm chưa hài lòng và yêu cầu sửa thành skill dùng chung ở P-002. Codex thực hiện sửa file: **log dùng mã P ngắn**, **dữ liệu đối chiếu lưu riêng**, **audit đúng phạm vi artifact**, **khai báo theo sáu câu hỏi** và **đọc đề của từng HW**. Bảng trước/sau tại mục 3.3. |
| **A-01 — Skill thiết kế Domain Testing/BVA**<br><br>**Tool:** OpenAI Codex<br>**Thời gian bắt đầu:** 20:25:47 19/10/2026 (UTC+07:00)<br>**Prompt:** [P-003](23120410_HW02_PromptLog.md#msg-d9b48702e80bca216e2a), nguyên văn tại **3.5**.<br><br>Làm rõ phạm vi: [P-004](23120410_HW02_PromptLog.md#msg-c8655ff83338222bdb54), [P-005](23120410_HW02_PromptLog.md#msg-0d15905a7329be883e67), [P-006](23120410_HW02_PromptLog.md#msg-c64a4bbe130b7d5e67a2). | Bản đầu gồm bốn mô-đun theo §6. Theo yêu cầu P-005, Codex sửa thành skill chỉ phân tích miền, chọn biên, sinh và kiểm tra TC. Giữ [bản tại commit đầu](https://github.com/tranquocvy/eshop-sut/blob/58481f466d78ed0f5801bfbc64a676006d2beac2/skills/domain-bva-testing/SKILL.md) và [bản sau khi tách](https://github.com/tranquocvy/eshop-sut/blob/ddcacdf72a041aca8fb37325d3c26b4e6290840e/skills/domain-bva-testing/SKILL.md); output gốc tại **3.5–3.6**. | **VALID** — đánh giá bản sau khi tách ở P-005/P-006 | Đáp ứng phạm vi đã làm rõ: đi từ test basis tới mô hình miền/biên, TC có oracle và truy vết, review coverage; kết thúc ở thiết kế. Giữ các điểm tham khảo từ skill public và giải thích phương pháp [1], [4]. Trạng thái `reference-provisional` nêu đúng việc chưa đối chiếu slide, nên không khẳng định đã khớp hoàn toàn bài giảng. Đây là đánh giá hướng dẫn/đóng gói skill, không phải kết luận chất lượng bộ TC trên một feature. | Sinh viên hỏi về execution và **đề xuất tách để sinh TC nhanh**. Codex **loại phần tự chạy SUT và report khỏi luồng thiết kế**, **giữ Domain/BVA và review thiết kế**, thêm mẫu bộ TC. P-006 giữ rõ quan hệ mục 1–2 với mục 3–4 của đề. Không phát hiện sai thuật toán cụ thể trong các lượt này; thay đổi chính là phạm vi sử dụng. |
| **A-02 — Skill thực thi và báo cáo**<br><br>**Tool:** OpenAI Codex, gpt-6.1-sol.<br>Khởi tạo ở P-005/P-007; review và sửa ở [P-018](23120410_HW02_PromptLog.md#msg-34c6c9ea763c4decf9f2), [P-019](23120410_HW02_PromptLog.md#msg-4e3c62ab0bb4d9f6e65d), [P-020](23120410_HW02_PromptLog.md#msg-e0dc57e10128c538b2f0), [P-022](23120410_HW02_PromptLog.md#msg-844b978b0d8d18b2a3ed). <br><br>Bổ sung: [P-027](23120410_HW02_PromptLog.md#msg-36be906c669996d7cbf9), [P-028](23120410_HW02_PromptLog.md#msg-0453443a1aeea0f60e1a), [P-030](23120410_HW02_PromptLog.md#msg-335afed53aaee172819f). | Giữ [bản đầu có evidence/JPG](https://github.com/tranquocvy/eshop-sut/blob/8018b73e9e0d9066efdb1ffe3512303e033a6cb4/skills/test-execution-reporting/SKILL.md) và [bản gọn tại cbf1ba9](https://github.com/tranquocvy/eshop-sut/blob/cbf1ba939c9a0b41281ccc1f053096ee60035897/skills/test-execution-reporting/SKILL.md). Bản mới dùng một nguồn kết quả, report Markdown và JPG cần thiết. Chi tiết tại **3.11**.  Bản bổ sung tại commit local `e1fe254`: [skill](../../../skills/test-execution-reporting/SKILL.md), [contract](../../../skills/test-execution-reporting/references/report-contract.md), [template](../../../skills/test-execution-reporting/assets/feature-report.template.md); mục **3.14** giữ yêu cầu và diễn biến. | **VALID** — đánh giá bản sau bổ sung P-028/P-030 | Luồng cũ yêu cầu lưu quá nhiều trace/layout và ảnh, được sinh viên phát hiện khi review. Bản sửa giữ actual, persistence, sequence, history, phân loại SUT/harness; bỏ screenshot mọi TC, ảnh trùng và hướng dẫn xuất PDF. Report phải đối chiếu được input/expected/actual/kết luận. Helper qua 10 kiểm tra; skill được dùng trong execution MR [10], [11].  Rà soát ở P-027 chỉ ra bước GitHub còn nằm ngoài luồng mặc định, chưa buộc kiểm tra/chụp trang issue khi nhiệm vụ yêu cầu. Bản bổ sung đã có bước đăng, chống trùng, xác minh ảnh/URL và evidence trang issue; P-030 thêm yêu cầu link log/ảnh theo từng TC/run. Link từng TC là yêu cầu làm rõ ở P-030, không suy thành rule sản phẩm SUT [13]. | Sinh viên **yêu cầu kết quả chung, evidence vừa đủ, xóa PNG tạm và bỏ PDF**. Codex **sửa skill, reference/template và helper**, đồng bộ bản local/repo; [diff thay đổi](https://github.com/tranquocvy/eshop-sut/compare/8018b73e9e0d9066efdb1ffe3512303e033a6cb4...cbf1ba939c9a0b41281ccc1f053096ee60035897). Đây là thay đổi do Codex thực hiện theo góp ý của sinh viên.  **Codex bổ sung bước GitHub và ảnh trang issue theo P-028; thêm cột/link evidence cho cả TC pass theo P-030.** Lượt P-030 chỉ sửa skill, chưa sửa report Mobile. |
| **A-03 — Bộ thiết kế Mobile Account Registration**<br><br>**Tool:** OpenAI Codex, gpt-6.1-sol<br>**Bắt đầu:** 23:58:19 19/10/2026 (UTC+07:00)<br>**Prompt:** [P-008](23120410_HW02_PromptLog.md#msg-9c5d57863614170c8ab0), nguyên văn tại **3.9**.<br><br>Giải thích và review: [P-009](23120410_HW02_PromptLog.md#msg-1419f914508254329f1b), [P-010](23120410_HW02_PromptLog.md#msg-57da3f9386c61457d81e), [P-011](23120410_HW02_PromptLog.md#msg-4873da5fa8bbf9630f5b), [P-012](23120410_HW02_PromptLog.md#msg-84ee0558719d3db513aa), [P-013](23120410_HW02_PromptLog.md#msg-4f7fab8add7e9c9a7096), [P-014](23120410_HW02_PromptLog.md#msg-9b5e6837d82871732b9f). | Hai file `design.md` và `test-cases.md`: bản đầu **v0.1 có 46 TC**, bản được đánh giá **v0.3 tại commit 5ca63e1 có 54 TC**, 37 mục tiêu miền, 18 boundary items; 18 TC mang cả Domain và BVA. [Bản đầu](history/mobile-registration-v0.1-design.md.txt), [bản đã review](https://github.com/tranquocvy/eshop-sut/blob/5ca63e1dadc0c69cd4a52b892f2c5a1dc1ff5d59/tests/hw02/mobile-registration/design.md), [bảng TC](https://github.com/tranquocvy/eshop-sut/blob/5ca63e1dadc0c69cd4a52b892f2c5a1dc1ff5d59/tests/hw02/mobile-registration/test-cases.md). | **VALID** — đánh giá bản thiết kế v0.3 đã review | Đáp ứng nhiệm vụ thiết kế: test basis FR-01/FR-20, bảng rule, mô hình miền, lý do chọn điểm, BVA 7/8/9 và các count 0/1/2, TC có precondition/input/steps/expected và truy vết. Expected theo đặc tả được tách với quy ước bổ sung về trim, case và Unicode. BVA dùng tài liệu môn trang 44; Domain ghi đúng nguồn tham khảo. Toàn bộ TC Not Run; 4 ca so sánh confirmation giữ điều kiện phải có field native [1], [6]–[8]. Chưa execution không phải lỗi của nhiệm vụ chỉ thiết kế. | Sinh viên hỏi lại lý thuyết/cách đọc và **review tên, khoảng trắng, case email, special, đơn vị Unicode** tại P-011/P-012. Codex **sửa expected TC41–46**, **bổ sung TC47–54**, **cập nhật mô hình và coverage**, giữ nguyên ID cũ. Bản sửa có đánh dấu trong [diff v0.1→v0.3](history/mobile-design-changes.diff). Tám ca bổ sung xuất phát từ các quy ước được làm rõ; không tự tính tất cả thành AI bỏ sót. |
| **A-04 — Code test Mobile Account Registration**<br><br>**Tool:** OpenAI Codex, gpt-6.1-sol<br>**Bắt đầu:** 01:03:41 20/10/2026 (UTC+07:00)<br>**Prompt:** [P-015](23120410_HW02_PromptLog.md#msg-dc4f2e51b024238929a8), nguyên văn tại **3.10**. | Bộ code cho **54 TC** từ thiết kế v0.3: `cases.json`, `native_android.py`, `run.py` và `IMPLEMENTATION.md`. [Bản output giữ nguyên](https://github.com/tranquocvy/eshop-sut/blob/b8b1d2b18203a0ebf0a24352890da1e80fc0d5fc/tests/hw02/mobile-registration/IMPLEMENTATION.md); phản hồi cuối tại **3.10**. | **VALID** — giữ nguyên theo xác nhận sinh viên, trong phạm vi implementation | Hai tài liệu đầu vào đã được review tại A-03. Codex đối chiếu tĩnh đủ 54 ID, dữ liệu literal và expected; giữ sequence TC13/TC38, C-guard TC34–37 và kiểm tra cú pháp AST. Code dùng thao tác native, quan sát SQLite chỉ đọc và chuẩn bị evidence khi chạy [8], [9]. Chưa thực thi code/SUT; đánh giá này không phải kết quả chạy test. | **Giữ nguyên đầu ra** vì code test được triển khai từ hai tài liệu thiết kế đã được duyệt trước đó. Không sửa nội dung ở bước này. |
| **A-05 — Kết quả execution và report Mobile Registration**<br><br>**Tool:** OpenAI Codex, gpt-6.1-sol.<br>**Bắt đầu:** 01:25:23 20/10/2026 (UTC+07:00).<br>**Prompt:** [P-016](23120410_HW02_PromptLog.md#msg-ecfe30f8f95eb2cc71f0)–[P-023](23120410_HW02_PromptLog.md#msg-b9e49c78a2be320ca739); nội dung tại **3.12** và Prompt Log. <br><br>Bổ sung hồ sơ Issues: [P-027](23120410_HW02_PromptLog.md#msg-36be906c669996d7cbf9) và [P-029](23120410_HW02_PromptLog.md#msg-f3b061c972ae96d0c800). | [Report](https://github.com/tranquocvy/eshop-sut/blob/62e34ecbcce65a8c803625ca8d210dfd9176dbbe/tests/hw02/mobile-registration/report.md), [results.json](https://github.com/tranquocvy/eshop-sut/blob/62e34ecbcce65a8c803625ca8d210dfd9176dbbe/tests/hw02/mobile-registration/results.json) và 15 JPG; bản tại commit **62e34ec**. 54 TC thiết kế, **35 pass, 15 fail, 4 blocked**; tám nhóm phát hiện, gồm bốn vi phạm requirement và bốn sai khác S7.  Sau rà soát đã có [8 GitHub Issues](https://github.com/tranquocvy/eshop-sut/issues) và 9 JPG trang/danh sách issue; [report](../../../tests/hw02/mobile-registration/report.md), [results](../../../tests/hw02/mobile-registration/results.json) tại mốc local `e1fe254`. | **INCOMPLETE** — đánh giá bản `62e34ec` trước bổ sung Issues | Bản `62e34ec` giữ đúng kết quả native/UI/DB, unique TC và lịch sử, nhưng chỉ có report local và ghi “chưa đăng Issues”. Khi đối chiếu yêu cầu báo lỗi của HW02 §6.4 và hồ sơ §14, phần GitHub/evidence còn thiếu; ghi đúng trạng thái chưa đăng không thay việc hoàn thành yêu cầu. Sinh viên phát hiện khi kiểm tra tracker ở P-027. Vì vậy điều chỉnh nhận xét đề xuất trước đây từ VALID sang INCOMPLETE cho đúng phiên bản đang đánh giá [1], [10], [13]. | Sinh viên **dừng để xem flow**, góp ý file/ảnh quá nhiều và **đã kiểm tra report/results**. Codex **gom kết quả**, **bỏ PNG tạm/ảnh trùng**, **sửa harness**, chạy lại phần bị ảnh hưởng rồi hoàn thiện report. [Kết quả run đầu](history/mobile-initial-results.json) và [diff harness](https://github.com/tranquocvy/eshop-sut/compare/b8b1d2b18203a0ebf0a24352890da1e80fc0d5fc...b1c122bd0f00bc982d19093abad0776f0434d04e) giữ diễn biến. Sinh viên sau đó yêu cầu commit riêng runner và report.  **Theo P-029, Codex đăng 8 issue (#1–#8), kiểm tra 14 ảnh SUT hiển thị và lưu 8 JPG trang issue + 1 JPG danh sách; bổ sung URL, thời gian và log tạo/xác minh/chụp.** Không chạy lại SUT; 35 pass, 15 fail, 4 blocked giữ nguyên. Bốn finding S7 được phân loại rõ; phần thiếu Issues đã được bổ sung trong bản sau, không ghi đè lịch sử bản cũ. |

| **A-06 — Bộ thiết kế Category Management**<br><br>**Tool:** OpenAI Codex, gpt-6.1-sol.<br>**Bắt đầu:** 11:15:35 20/10/2026 (UTC+07:00).<br>**Prompt:** [P-024](23120410_HW02_PromptLog.md#msg-2642f1f9f300cb746a59)–[P-026](23120410_HW02_PromptLog.md#msg-7614bb5c1dae4235dc44), nguyên văn tại **3.13**. | Hai file `design.md`, `test-cases.md`: [bản AI đầu v0.1](history/category-v0.1-design.md.txt) có **24 TC**; [bản v0.2 sau review](https://github.com/tranquocvy/eshop-sut/blob/b84417b841f7a1bd5d20386132a0f333d7487fb1/tests/hw02/fr14-categories/design.md) và [TC](https://github.com/tranquocvy/eshop-sut/blob/b84417b841f7a1bd5d20386132a0f333d7487fb1/tests/hw02/fr14-categories/test-cases.md) tại **b84417b** có **33 TC**, 19 mục tiêu miền, 6 BVA items theo lớp. | **INCOMPLETE** — đánh giá bản AI đầu v0.1; chấp nhận sau bổ sung ở v0.2 | Bản đầu có rule/miền/TC và đúng biên tên 0/1/2 trên Web, nhưng chưa lấy mẫu tên 1/2 ở API, JWT đúng cấu trúc bị sửa payload/chữ ký, hoặc khôi phục phiên Web từ token user. Một mẫu malformed JWT và coverage trên inventory tự chọn chưa đủ chứng minh đã xét các đường kiểm tra này. Căn cứ là FR-14 required/name, FR-12 JWT hợp lệ/role admin, điểm vào lưu phiên trong source và cách lấy mẫu miền/biên [7], [12]. Chưa chạy SUT không phải thiếu sót của nhiệm vụ thiết kế. | Sinh viên **hỏi lại độ đầy đủ** rồi **chỉ định ba nhóm cần bổ sung**. Codex **thêm TC25–26** cho BVA API, **TC27–32** cho hai loại token bị sửa trên POST/DELETE/PUT, **TC33** cho phiên user đã lưu; **gắn BVA cho TC10** thay vì tạo ca rỗng trùng. Giữ TC01–24, cập nhật miền/biên và truy vết; [diff v0.1→v0.2](history/category-design-changes.diff). Sinh viên đã đọc hai file và yêu cầu commit; không tự chốt các policy chưa có đặc tả. |

### 3.1. Output AI ban đầu — A-00 / P-000

**Thời gian:** 19:22:24 19/10/2026 (UTC+07:00).

```text
Đề §9 khuyến khích đúng việc này. Mình đã tạo [skill `hw02-ai-log`]([đường dẫn skill cá nhân đã ẩn]) để giảm việc chép tay.

Khi được dùng, skill sẽ tự cập nhật:

| File | Nội dung tự điền |
|---|---|
| `prompt_log.md` | Công cụ, thời gian, prompt và output nguyên văn; giữ các lượt sửa |
| `AI_Audit_Report.md` | Artifact, liên kết tương tác, đề xuất verdict, căn cứ và bản sửa |
| `AI_Disclosure.md` | Công cụ, giai đoạn, prompt quan trọng, đóng góp và cách xác minh có bằng chứng |

**Bạn chỉ cần xác nhận những phần thuộc đánh giá của mình**, thay vì tự chép toàn bộ log. Skill không tự nhận bạn đã review, tự sửa, tự chạy test hoặc ký cam đoan.

Cách gọi:

> Dùng `$hw02-ai-log` cập nhật log và biểu mẫu cho task vừa làm.

Đã kiểm chứng helper qua 8 nhóm tình huống, gồm chống ghi trùng, giữ nguyên nội dung và bảo toàn sửa tay. **Chưa ghi log bài thật.** Skill hoạt động khi được dùng trong phiên, không phải tiến trình ghi nền; lịch sử thiếu sẽ được đánh dấu rõ.
```

### 3.2. Output AI sau khi sửa — A-00 / P-002

**Thời gian:** 21:26:44 19/10/2026 (UTC+07:00).

```text
Đã sửa thành [**`course-ai-log`**]([đường dẫn skill cá nhân đã ẩn]), dùng chung cho các HW sau.

- Đọc đề và biểu mẫu riêng của từng bài.
- Trình bày theo HW01: log dễ đọc, audit từng artifact, khai báo tự nhiên và cụ thể.
- Giữ ID/hash trong dữ liệu hỗ trợ; giảm cảnh báo lặp.
- Dùng lại thông tin sinh viên ổn định, giữ đúng dữ kiện review của từng bài.
- Tên cũ `$hw02-ai-log` vẫn dùng được.

Đã qua **15 kiểm tra helper** và thử chuyển đổi trên bản sao log HW02: giữ nguyên **11 tin nhắn cùng liên kết cũ**.

Cách gọi:

> Dùng `$course-ai-log` cập nhật log và biểu mẫu AI cho task vừa làm.

Lượt này đã sửa skill và helper; các báo cáo HW02 hiện tại chưa được viết lại.
```

Phần phân tích nguyên nhân và hướng sửa ở P-001 được giữ đầy đủ trong [Prompt Log](23120410_HW02_PromptLog.md#msg-badc52515014adae1a4b).

### 3.3. Thay đổi theo góp ý của sinh viên

| Nội dung | Bản đầu | Bản đã sửa theo yêu cầu |
| --- | --- | --- |
| Prompt Log | Hiển thị nhiều ID nguồn và thông tin trích xuất | **Mã P-000, thời gian, công cụ, Prompt và Output; ID/hash lưu trong dữ liệu hỗ trợ** |
| AI-02 | Lặp nhiều trạng thái chờ và thông báo tiến độ | **Tập trung từng artifact, lỗi cụ thể, căn cứ và bản sửa; một ghi chú nháp chung** |
| Phạm vi verdict | Có lúc dùng mức hoàn thành cả HW để đánh giá một artifact | **Đánh giá theo nhiệm vụ đã giao cho artifact** |
| AI-03 | Dùng cách diễn đạt thiên về hệ thống ghi log | **Trả lời sáu câu hỏi bằng văn phong tự nhiên, có sản phẩm và hành động cụ thể** |
| Phạm vi sử dụng | Skill dành cho HW02 | **Đọc đề và biểu mẫu từng bài; dùng lại cho các HW sau, giữ tên gọi cũ để tương thích** |
| Thông tin sinh viên | MSSV/lớp để chờ xác nhận; quy tắc chưa tận dụng thông tin ổn định từ mẫu người dùng cung cấp | **Dùng lại thông tin ổn định có nguồn; ngày dùng, tool, review và verdict theo từng bài** |

Sinh viên đọc đầu ra, cung cấp HW01 để đối chiếu và xác định hướng điều chỉnh ở P-001/P-002. Codex sửa hướng dẫn và code helper theo các yêu cầu đó.

### 3.4. Kiểm chứng do Codex thực hiện

Trong lượt P-002, Codex chạy **15 kiểm tra helper, đều đạt**, kiểm tra cấu trúc skill và thử chuyển đổi dữ liệu log cũ trên bản sao. Lần chuyển đổi giữ nguyên **11 tin nhắn của bộ log cũ** cùng các liên kết; con số này thuộc phép kiểm chứng lúc sửa skill, khác với 14 tin nhắn của ba lượt AI log P-000–P-002. [Kết quả công cụ đã chạy](verification/ai-log-helper.txt).

### 3.5. Nghiên cứu và bản skill gộp ban đầu — A-01 / P-003

**Prompt — 20:25:47 19/10/2026 (UTC+07:00):**

```text
tiếp đến là skill agent, hãy research trên các mạng xã hội hay github, check xem có ai có skill về phần này không. Rồi tổng hợp lại lấy phần nào hay hoặc tự làm 1 bộ skill về domain testing phù hợp luôn, đề bài có yêu cầu các bước ấy, thì mình build nên bộ skill follow theo nó là được. Tôi thấy đề nói:

## 6. Yêu cầu

Với mỗi tính năng đã chọn, thực hiện các nhiệm vụ sau:

1. **Kiểm thử miền (Domain Testing).** Với sự hỗ trợ của công cụ AI, áp dụng kỹ thuật kiểm thử miền để thiết kế một bộ ca kiểm thử (test case) toàn diện. Khuyến khích bổ sung test case khi cần để bảo đảm độ bao phủ đầy đủ. Giải thích chi tiết từng bước áp dụng kỹ thuật. Ôn lại bài giảng của học phần trước khi bắt đầu.
2. **Phân tích giá trị biên (Boundary Value Analysis).** Tương tự, áp dụng kỹ thuật phân tích giá trị biên để thiết kế một bộ test case toàn diện; bổ sung khi cần để bảo đảm độ bao phủ đầy đủ. Giải thích chi tiết từng bước áp dụng kỹ thuật. Cũng cần ôn lại bài giảng trước khi thực hiện.
3. **Phân tích các trường hợp AI bỏ sót (AI gap analysis).** Nếu công cụ AI bỏ sót test case hoặc lỗi nào, phải báo cáo các trường hợp đó. Giải thích *vì sao* AI bỏ sót, chẳng hạn do chất lượng đầu vào (prompt), giới hạn của chính công cụ AI hoặc độ phức tạp vốn có của tính năng được kiểm thử.
4. **Báo cáo lỗi (Bug reporting).** Báo cáo tất cả lỗi phát hiện được trong cả báo cáo Markdown và trang GitHub Issues của nhóm. Đính kèm ảnh chụp màn hình minh họa lỗi vào từng GitHub issue.

## 7. Agent Skill

- Khuyến khích xây dựng Agent Skills áp dụng kỹ thuật kiểm thử miền và phân tích giá trị biên, để có thể tái sử dụng cho các tính năng khác trong những nhiệm vụ kiểm thử sau này.
- Nộp các skill cùng video minh họa (liên kết YouTube), thể hiện toàn bộ quy trình từ đầu đến cuối về cách sử dụng skill trên một tính năng hoàn chỉnh.


```

**Output cuối — 20:36:15 19/10/2026 (UTC+07:00):**

```text
Đã khảo sát GitHub/Reddit và tạo **[bộ `domain-bva-testing`](D:/Workspace/SoftwareTesting/HW02/eshop-sut/hw02/skills/domain-bva-testing/SKILL.md)**. Mình chọn cách tổ chức gọn: **một skill chính, bốn mô-đun đúng §6**, để bạn không phải gọi nhiều skill riêng.

Các nguồn có phần đáng tham khảo:

| Nguồn | Phần chọn lọc |
|---|---|
| [quality-skills](https://github.com/aks-builds/quality-skills/blob/main/skills/test-design-techniques/SKILL.md) | Đọc bối cảnh và đặc tả trước khi chọn dữ liệu kiểm thử |
| [testland/qa](https://github.com/testland/qa/blob/main/plugins/qa-manual-testing/skills/decision-table-test-design/SKILL.md) | Giải thích phép suy ra từng bước, liên kết mô hình với test |
| [bug-report-forensics](https://github.com/rcptrkr/qa-skills/blob/main/plugins/qa-essentials/skills/bug-report-forensics/SKILL.md) | Xác định oracle, rút gọn bước tái hiện và giữ bằng chứng |
| [Thảo luận QA skills trên Reddit](https://www.reddit.com/r/claudeskills/comments/1w0kaxm/what_claude_skillsai_skills_are_your_qa_teams/) | Tham khảo nhu cầu/workflow thực tế; không dùng làm định nghĩa kỹ thuật |

Phương pháp được kiểm tra chéo với nguồn tác giả [Cem Kaner về Domain Testing](https://www.kaner.com/pdfs/domain_testing_cseet.pdf) và [ISTQB CTFL §4.2.1–4.2.2](https://istqb.org/wp-content/uploads/2024/11/ISTQB_CTFL_Syllabus_v4.0.1.pdf). Nội dung bộ skill được viết mới; không lấy bài hay prompt HW02 của sinh viên khác. Chi tiết nguồn, revision và giấy phép nằm trong [bản tổng hợp khảo sát](D:/Workspace/SoftwareTesting/HW02/eshop-sut/hw02/skills/domain-bva-testing/references/research.md).

Bộ skill sẽ thực hiện:

1. **Domain Testing:** đọc rule → xác định biến/miền → chọn điểm đại diện → thiết kế test → giải thích coverage.
2. **BVA:** xác định biên và độ phân giải → chọn biến thể → sinh điểm → ánh xạ thành test.
3. **AI gap analysis:** giữ bản AI ban đầu, đối chiếu review/kết quả chạy và giải thích các thiếu sót thật.
4. **Bug reporting:** phân biệt nghi vấn với bug đã tái hiện, tạo báo cáo Markdown và chuẩn bị bằng chứng cho Issues nhóm.

Kèm theo có **template báo cáo**, **helper tính điểm biên** và **[hướng dẫn demo đầu cuối](D:/Workspace/SoftwareTesting/HW02/eshop-sut/hw02/skills/domain-bva-testing/references/demo.md)**.

Đã cài bản local để gọi:

> Dùng `$domain-bva-testing` cho Mobile Account Registration, bắt đầu từ đặc tả và thực hiện lần lượt các bước của HW02.

Kiểm tra cấu trúc, liên kết và 8 nhóm kiểm tra helper đều đạt. **Chưa chạy demo trên feature thật; phương pháp đang là bản tham khảo chờ đối chiếu slide môn học.**
```

Các đường dẫn trong khối output là đường dẫn lịch sử tại thời điểm trả lời. Bản Git trước khi tách được lưu tại [A-01 / bản đầu](https://github.com/tranquocvy/eshop-sut/blob/58481f466d78ed0f5801bfbc64a676006d2beac2/skills/domain-bva-testing/SKILL.md), gồm cả references, template và helper; nguồn khảo sát cùng revision/giấy phép được giữ trong [research của bản đầu](https://github.com/tranquocvy/eshop-sut/blob/58481f466d78ed0f5801bfbc64a676006d2beac2/skills/domain-bva-testing/references/research.md).

Ở [P-004](23120410_HW02_PromptLog.md#msg-c8655ff83338222bdb54), sinh viên hỏi vì sao có execute trong domain skill. Codex giải thích execution được ghép sau thiết kế để có actual và bằng chứng, liên hệ §14 của đề. Đây là lý do cấu trúc bản đầu bao quát cả bốn nhiệm vụ; yêu cầu tiếp theo làm rõ nhu cầu gọi riêng phần sinh TC.

### 3.6. Tách thiết kế khỏi execution/reporting — A-01 và A-02 / P-005

**Prompt — 22:00:06 19/10/2026 (UTC+07:00):**

```text
tôi nghĩ nên tách phần execute với report ra là 1 skill riêng, vì đây nên là 1 skill thuần về domaintesting, thuần viết sinh test case hơn, khi cần sinh tc nhanh mà phải đợi execute và report thì sẽ rất lâu
```

**Output cuối — 22:07:31 19/10/2026 (UTC+07:00):**

```text
Đã tách thành hai skill:

| Skill | Phạm vi |
|---|---|
| [`domain-bva-testing`](D:/Workspace/SoftwareTesting/HW02/eshop-sut/skills/domain-bva-testing/SKILL.md) | Phân tích miền, BVA, sinh TC và tự kiểm tra thiết kế. **Kết thúc ở bộ test**, không chạy SUT hay viết báo cáo kết quả. |
| [`test-execution-reporting`](D:/Workspace/SoftwareTesting/HW02/eshop-sut/skills/test-execution-reporting/SKILL.md) | Nhận TC có sẵn để thực thi, lưu bằng chứng, phân tích AI gaps và báo cáo. Có thể chỉ viết report từ kết quả đã có. |

Ví dụ gọi nhanh:

> Dùng `$domain-bva-testing` sinh TC nhanh cho FR-07.

Đã đồng bộ bản local và repo, kiểm tra định dạng cùng liên kết. **Chưa commit thay đổi này.**
```

| Nội dung | Trước khi tách | Bản sửa theo góp ý của sinh viên |
| --- | --- | --- |
| `domain-bva-testing` | Luồng gộp thiết kế, review, execution, AI gaps và bug report | **Chỉ đọc test basis, phân tích miền/biên, sinh TC và kiểm tra thiết kế; dừng ở bộ test** |
| `test-execution-reporting` | Tài nguyên nằm trong skill gộp | **Skill riêng nhận TC có sẵn; thực thi hoặc report-only từ dữ liệu thật khi được giao** |
| Quy cách đầu ra | Template báo cáo feature đầy đủ | **Template TC thuộc design; template kết quả/bug/gap và hướng dẫn demo thuộc execution/reporting** |
| Phương pháp và helper biên | Có Domain, BVA và helper tính điểm | **Giữ các bước phân tích và helper; sinh nhanh giảm diễn giải, không bỏ mô hình hay oracle** |

Ở [P-006](23120410_HW02_PromptLog.md#msg-c64a4bbe130b7d5e67a2), Codex xác nhận `domain-bva-testing` đảm nhiệm §6 mục 1–2; skill execution/reporting đảm nhiệm phần chạy cùng mục 3–4. Các điểm giữ từ nguồn public là đọc bối cảnh, giải thích phép suy ra, truy vết requirement và kiểm tra thiết kế. Phương pháp vẫn là `reference-provisional` cho tới khi có slide để đối chiếu; chưa gọi là `lecture-aligned`.

### 3.7. Bổ sung evidence và JPG — A-02 / P-007

**Prompt — 22:13:08 19/10/2026 (UTC+07:00):**

```text
test execution, hãy có evidence rõ ràng nhé, tôi sẽ dùng nó để chạy và xuất báo cáo, xuất cả img bằng jpg theo task/đề yêu cầu nếu có
```

**Output cuối — 22:18:37 19/10/2026 (UTC+07:00):**

```text
Đã cập nhật [`test-execution-reporting`](D:/Workspace/SoftwareTesting/HW02/eshop-sut/skills/test-execution-reporting/SKILL.md):

- Evidence truy vết **TC → run → ảnh/log → bug/issue**, có thời gian và môi trường.
- Chụp ảnh từ lần chạy thật; xuất **JPG** khi cần ảnh, theo định dạng task/đề yêu cầu.
- Giữ ảnh nguồn, phân biệt ảnh bug với ảnh trang GitHub issue.
- Báo cáo dẫn/nhúng ảnh với caption; xuất Markdown/PDF khi được giao.

Đã thêm helper chuyển JPG thật, qua **8 kiểm tra bằng dữ liệu giả lập**, và đồng bộ bản local với repo.

**Chưa commit.**
```

Bản artifact giữ [quy cách evidence](https://github.com/tranquocvy/eshop-sut/blob/8018b73e9e0d9066efdb1ffe3512303e033a6cb4/skills/test-execution-reporting/references/evidence.md), [mẫu chỉ mục](https://github.com/tranquocvy/eshop-sut/blob/8018b73e9e0d9066efdb1ffe3512303e033a6cb4/skills/test-execution-reporting/assets/evidence-index.template.md), [helper JPG](https://github.com/tranquocvy/eshop-sut/blob/8018b73e9e0d9066efdb1ffe3512303e033a6cb4/skills/test-execution-reporting/scripts/export_jpg.py) và [các kiểm tra helper](https://github.com/tranquocvy/eshop-sut/blob/8018b73e9e0d9066efdb1ffe3512303e033a6cb4/skills/test-execution-reporting/scripts/test_export_jpg.py). Ảnh phải xuất phát từ thao tác thật khi chạy feature; helper chỉ chuyển định dạng, không tạo screenshot.

### 3.8. Kiểm chứng hai skill kỹ thuật do Codex thực hiện

- P-003: 8 nhóm kiểm tra helper biên đạt, gồm hai profile, bước thập phân, số nguyên lớn, giới hạn biểu diễn, lattice và 12 input sai; kiểm tra CLI dùng thư mục tạm.
- P-005: kiểm tra cấu trúc và liên kết đạt; bản local khớp bản repo; helper biên không đổi. Tại thời điểm đó design có 9 file và execution/reporting có 8 file.
- P-007: 8 kiểm tra helper JPG đạt với fixture giả lập: giải mã JPEG, giữ nguồn/đích đã tồn tại, xử lý EXIF, từ chối ảnh động và đầu vào sai, cùng CLI/metadata. Bản execution/reporting sau bổ sung có 12 file.

[Output công cụ được lưu nguyên văn](verification/design-execution-helpers.txt). Những kiểm tra này xác minh helper và cấu trúc đóng gói; chưa có run EShop, screenshot bug hay demo feature trong năm lượt được ghi.

### 3.9. Thiết kế và review Mobile Registration — A-03

**Prompt gốc — [P-008](23120410_HW02_PromptLog.md#msg-9c5d57863614170c8ab0) — 23:58:19 19/10/2026 (UTC+07:00):**

```text
hãy dùng [$domain-bva-testing](C:\Users\DELL\\.codex\skills\domain-bva-testing\SKILL.md) để thực hiện Task T02, mobile account registration. không làm các việc khác ngoài skill
```

**Output AI ban đầu v0.1:** giữ nguyên hai file [design.md](history/mobile-registration-v0.1-design.md.txt) và [test-cases.md](history/mobile-registration-v0.1-test-cases.md.txt). Bản này có 46 TC, 29 mục tiêu miền và 18 boundary items, trong đó 15 TC mang cả hai kỹ thuật. TC41–46 còn expected có điều kiện vì các policy chưa rõ. Phản hồi tiến độ và kết quả gốc nằm trong P-008, không thay bằng lời mô tả bản cuối.

**Bản được đánh giá v0.3:** [design.md](https://github.com/tranquocvy/eshop-sut/blob/5ca63e1dadc0c69cd4a52b892f2c5a1dc1ff5d59/tests/hw02/mobile-registration/design.md) và [test-cases.md](https://github.com/tranquocvy/eshop-sut/blob/5ca63e1dadc0c69cd4a52b892f2c5a1dc1ff5d59/tests/hw02/mobile-registration/test-cases.md), lấy đúng commit `5ca63e1`. Có 54 unique TC, 37 mục tiêu miền, 18 boundary items; 18 TC mang cả Domain và BVA. Bản đầu và bản sửa đều còn trong bộ hồ sơ; [diff](history/mobile-design-changes.diff) đánh dấu từng dòng thay đổi.

| Nội dung được review | Bản đầu | Bản sửa theo review |
| --- | --- | --- |
| Cách đọc và phương pháp | Nhiều mã S/R/D/B/TC, khó đọc lần đầu; S còn dùng cho bước chung | **Giải thích ý nghĩa mã và thứ tự đọc**, phân biệt Domain/BVA với implementation/execution trong P-009/P-010 |
| Tên | Có giả định tên nonempty, chưa chốt tên toàn space | **Giữ tên ngắn/tiếng Việt hợp lệ; TC41 REJECT tên sau trim rỗng** |
| Email | Case và trim chưa có policy cuối | **TC42 ACCEPT email khác case; TC43 ACCEPT email mới sau trim; TC53 REJECT khi sau trim trùng email cũ** |
| Special | Bảy ký hiệu trong README được thử; ngoài danh sách còn conditional | **Công nhận dấu/ký hiệu Unicode, không tính whitespace; thêm các điểm #, _, emoji, em dash, euro** |
| Đơn vị độ dài | BVA chính dùng ASCII; Unicode còn conditional | **Đếm Unicode code point; TC46–48 kiểm tra 7/8/9 code point với emoji** |
| Coverage và khả năng nhập | 46 TC/29 mục tiêu miền; giữ 4 ca confirmation có guard | **54 TC/37 mục tiêu miền; giữ guard cho TC34–37**, không dùng kết quả API thay native và không nhận đã chạy |

Tại [P-011](23120410_HW02_PromptLog.md#msg-4873da5fa8bbf9630f5b)/[P-012](23120410_HW02_PromptLog.md#msg-84ee0558719d3db513aa), sinh viên đưa ý kiến và trả lời câu làm rõ; Codex thực hiện sửa file. Tại [P-013](23120410_HW02_PromptLog.md#msg-4f7fab8add7e9c9a7096)/[P-014](23120410_HW02_PromptLog.md#msg-9b5e6837d82871732b9f), hai bên làm rõ rằng expected phải có căn cứ từ đặc tả hoặc giả định được ghi riêng; trường hợp quá mơ hồ có thể để ngoài phạm vi thay vì tạo expected tùy ý. Đây là review thiết kế, chưa phải báo cáo AI gaps hoặc lỗi sản phẩm đã chạy.

Codex kiểm tra tĩnh số TC/ID, ánh xạ rule/miền/biên, độ dài/count dữ liệu và chuỗi Unicode. BVA theo cách trang 44 tài liệu môn [7], không đổi tên tập điểm thành profile `istqb-3` của helper. Các phép kiểm tra dữ liệu không phải thực thi SUT.

### 3.10. Code triển khai — A-04 / P-015

**Prompt — 01:03:41 20/10/2026 (UTC+07:00):**

```text
từ 2 file design.md và testcase.md vừa rồi, hãy implement code cho các test case này, đảm bảo bám đúng 100% theo 2 file docs. chưa thực thi code ở bước này
```

**Output cuối — 01:17:42 20/10/2026 (UTC+07:00):**

```text
Đã implement **54/54 TC** theo hai file docs, gồm hai sequence TC13/TC38, Unicode, kiểm tra SQLite chỉ đọc và C-guard cho TC34–37.

- [Hướng dẫn implementation](D:/Workspace/SoftwareTesting/HW02/eshop-sut/tests/hw02/mobile-registration/IMPLEMENTATION.md)
- [Runner](D:/Workspace/SoftwareTesting/HW02/eshop-sut/tests/hw02/mobile-registration/scripts/run.py)
- [Dữ liệu và expected từng TC](D:/Workspace/SoftwareTesting/HW02/eshop-sut/tests/hw02/mobile-registration/scripts/cases.json)

Đã kiểm tra cú pháp AST và đối chiếu dữ liệu tĩnh. **Chưa thực thi code/SUT**, chưa tạo kết quả hay evidence. Hai file docs và source SUT giữ nguyên; chưa commit.
```

**Artifact được đánh giá:** [bốn file output nguyên bản](https://github.com/tranquocvy/eshop-sut/blob/b8b1d2b18203a0ebf0a24352890da1e80fc0d5fc/tests/hw02/mobile-registration/IMPLEMENTATION.md), triển khai từ `design.md` và `test-cases.md` v0.3 đã duyệt tại commit `5ca63e1`. Catalogue giữ đủ 54 TC cùng precondition, input, steps, expected và truy vết. Runner tách sequence TC13/TC38, kiểm tra điều kiện có Confirmation cho TC34–37, thao tác qua native và đọc SQLite chỉ để quan sát dữ liệu. Các phản hồi tiến độ được giữ trong [P-015](23120410_HW02_PromptLog.md#msg-dc4f2e51b024238929a8).

**Quyết định sử dụng:** Giữ nguyên đầu ra vì code được triển khai từ hai tài liệu thiết kế đã được duyệt trước đó. Không có bản sửa nội dung trong bước này. Codex đã kiểm tra cú pháp AST và đối chiếu dữ liệu tĩnh; chưa import/chạy bộ code mới, chưa thực thi SUT và chưa sinh kết quả/evidence runtime. Quyết định giữ nguyên không được dùng để nhận rằng 54 TC đã pass.

### 3.11. Thu gọn skill execution/reporting — A-02

Sinh viên đọc flow và phát hiện phần lưu evidence quá nặng: restart Expo theo TC, dump layout lặp, nhiều ảnh cùng trạng thái và giữ cả PNG/JPG. Ở [P-019](23120410_HW02_PromptLog.md#msg-4e3c62ab0bb4d9f6e65d), sinh viên yêu cầu một kết quả chung; [P-020](23120410_HW02_PromptLog.md#msg-e0dc57e10128c538b2f0) yêu cầu sửa skill; [P-022](23120410_HW02_PromptLog.md#msg-844b978b0d8d18b2a3ed) bỏ phần xuất PDF.

| Nội dung | Trước sửa | Sau sửa theo góp ý |
| --- | --- | --- |
| Kết quả | Nhiều output/debug theo TC và probe | **Một results.json**, mỗi TC một entry, metadata/history theo run |
| Evidence | Chụp nhiều trạng thái, giữ PNG và JPG | **JPG cần thiết theo bug**, dùng ảnh đại diện; PNG tạm xóa sau xác minh |
| Thao tác | Restart client và đọc layout nhiều lần | **Giữ session khi phù hợp**, debug giới hạn, dừng khi harness lỗi lặp |
| Report | Actual/status khó đối chiếu nếu thiếu expected | **Input → expected → actual → kết luận/bug**, có giải thích và link |
| Định dạng | Có hướng dẫn xuất PDF | **Report Markdown** theo lựa chọn hiện tại |

Giữ nguyên các nguyên tắc: không đổi expected để làm xanh test; kiểm tra đúng lớp native; DB chỉ là oracle phụ trợ; giữ failed/blocked và lịch sử chạy lại. Bản đầu không bị ghi đè; [bản gọn](https://github.com/tranquocvy/eshop-sut/blob/cbf1ba939c9a0b41281ccc1f053096ee60035897/skills/test-execution-reporting/SKILL.md) và diff được giữ cùng artifact.

### 3.12. Execution và report Mobile Registration — A-05

**Prompt mở đầu — [P-016](23120410_HW02_PromptLog.md#msg-ecfe30f8f95eb2cc71f0) — 01:25:23 20/10/2026 (UTC+07:00):**

```text
dùng `$test-execution-reporting` để chạy và xuất report cho các testcase của MR
```

**Prompt tiếp tục — [P-023](23120410_HW02_PromptLog.md#msg-b9e49c78a2be320ca739) — 02:42:21 20/10/2026 (UTC+07:00):**

```text
oke tiếp tục dùng skill để tiếp tục chạy test `$test-execution-reporting`
```

**Đầu ra và diễn biến chính:**

- Bước đầu chạy native và phát hiện lỗi tên rỗng, email sai định dạng, email trùng. Khi sinh viên dừng để review, 28 TC có trạng thái: 18 pass, 9 fail, 1 blocked; TC29 dở dang. Trace, layout và ảnh bị lưu dư.
- Codex kiểm tra JPG rồi xóa 107 PNG tạm; gom kết quả chung và chuyển output thô ra ngoài repo. PDF tạm đã được chuyển ngoài repo theo yêu cầu sau đó.
- Khi chạy tiếp, Codex kiểm tra UI/DB trước khi bắt đầu lại, sửa lỗi idle/IME và detector bỏ sót validation đang hiện. Hai verdict fail nhầm của harness được đánh dấu và giữ trong history; kết quả được chọn của TC38/39 sau kiểm tra lại đều pass.
- Kết quả cuối: **50/54 TC có kết quả đánh giá: 35 pass, 15 fail; bốn TC blocked (TC34–37)** do thiếu Confirmation. Coverage exercise **33/37 mục tiêu miền** và **18/18 boundary items**; đây là số mục đã đi tới điều kiện/quan sát, không phải pass rate.
- **Tám nhóm phát hiện:** bốn vi phạm requirement, bốn khác quy ước S7. Bản bàn giao tại `62e34ec` giữ **report.md, results.json và 15 JPG**; lúc đó chưa đăng GitHub Issues. Đây là thiếu sót được phát hiện ở P-027 và bổ sung ở P-029 (mục 3.14).

Sinh viên xác nhận đã kiểm tra hai file report/results rồi yêu cầu commit. Code harness tại `b1c122b`; report/results/evidence tại `62e34ec`. Các bước chạy và sửa file do Codex thực hiện. Dữ liệu/expected của hai tài liệu đã duyệt giữ nguyên; các bản sao output và diff ở [A-05](artifacts.md#a-05--execution-và-report-mobile-registration).

### 3.13. Thiết kế và bổ sung Category Management — A-06

**Prompt — [P-024](23120410_HW02_PromptLog.md#msg-2642f1f9f300cb746a59) — 11:15:35 20/10/2026 (UTC+07:00):**

```text
hãy dùng [$domain-bva-testing](C:\Users\DELL\\.codex\skills\domain-bva-testing\SKILL.md) để thực hiện Task T03, Category Management. không làm các việc khác ngoài skill, làm đúng và đủ không quá over engineering
```

**Prompt — [P-025](23120410_HW02_PromptLog.md#msg-7dffe02b118443b22b9a) — 11:22:29 20/10/2026 (UTC+07:00):**

```text
sao ít tc quá nhỉ, ít hơn 1 nửa so với mobile luôn, tôi xem qua rồi, có thật sự là đầy đủ theo đặc tả và theo lí thuyết domain + bva chưa?
```

**Prompt — [P-026](23120410_HW02_PromptLog.md#msg-7614bb5c1dae4235dc44) — 12:28:57 20/10/2026 (UTC+07:00):**

```text
cần bổ sung:

1. **BVA phía API:** có tên dài 1 và 2 ký tự &#x20;
2. thêm token bị sửa payload/chữ ký để kiểm tra yêu cầu “JWT hợp lệ” sâu hơn trên các phương thức thay đổi dữ liệu.
3. kiểm tra mở lại Admin khi nơi lưu phiên chứa token user
```

**Output gốc:** toàn bộ ba lượt có 9 phản hồi AI (tiến độ và kết quả) được giữ nguyên văn trong Prompt Log. Các file được sinh qua công cụ được giữ độc lập để đối chiếu, không dùng lời final “đã tạo file” thay cho bộ thiết kế.

| Phiên bản | Sản phẩm và phạm vi |
| --- | --- |
| AI đầu v0.1 | [design.md](history/category-v0.1-design.md.txt), [test-cases.md](history/category-v0.1-test-cases.md.txt), sao từ baseline đã giữ trước khi bổ sung: **24 TC**, 16 mục tiêu miền, 3 BVA items Web; 21 Domain và 3 Domain + BVA. |
| Sau bổ sung và review v0.2 | [design.md](https://github.com/tranquocvy/eshop-sut/blob/b84417b841f7a1bd5d20386132a0f333d7487fb1/tests/hw02/fr14-categories/design.md), [test-cases.md](https://github.com/tranquocvy/eshop-sut/blob/b84417b841f7a1bd5d20386132a0f333d7487fb1/tests/hw02/fr14-categories/test-cases.md), lấy đúng commit **b84417b**: **33 TC**, 19 mục tiêu miền, 6 BVA items theo lớp; 27 Domain và 6 Domain + BVA. |
| Thay đổi | [Diff nguyên văn v0.1→v0.2](history/category-design-changes.diff). Bản đầu không bị thay bằng bản cuối. |

| Nhóm được yêu cầu bổ sung | Bản sửa do Codex thực hiện |
| --- | --- |
| BVA API | **TC25/26:** tên `A`/`AB` qua POST với admin hợp lệ; **TC10** thêm nhãn BVA cho tên rỗng. Bộ API có 0/1/2 ký tự, không tạo TC rỗng trùng; tách với biên Web. |
| JWT bị sửa | **TC27–29:** sửa role trong payload token user, giữ chữ ký cũ; **TC30–32:** sửa byte chữ ký token admin, giữ header/payload. Mỗi loại thử POST/DELETE/PUT, expected từ chối và không thay đổi danh mục theo FR-12. |
| Mở lại Web từ phiên user | **TC33:** token user hợp lệ nằm trong `localStorage.adminToken`; đóng/mở lại trang mà không đi qua Admin Login; expected không truy cập được phân hệ quản lý danh mục. |

Nguyên nhân thiếu ở bản đầu nằm ở cách lấy mẫu: chỉ lập BVA cho Web, dùng token malformed đại diện nhóm invalid và chỉ kiểm tra user qua màn hình Login. Khi sinh viên hỏi lại, Codex nhận ra coverage trên các miền tự chọn chưa chứng minh mô hình đầy đủ; sinh viên chọn đúng ba nhóm cần bổ sung. Đây là nhận xét về thiết kế ban đầu, không phải kết luận bug sản phẩm.

Sinh viên tiếp tục đọc hai file, hỏi về phạm vi hoàn tất và yêu cầu commit lúc **12:42:30 20/10/2026 (UTC+07:00)**. Lượt xác nhận/commit này chỉ dùng làm căn cứ review phiên bản artifact; không thêm thành prompt thứ tư trong log ba lượt được chỉ định. Commit `b84417b` chỉ gồm hai file Category. Các policy whitespace, tên trùng, giới hạn trên, Update và xóa danh mục đang có sản phẩm vẫn là giới hạn đặc tả, không bị tự đổi thành expected.

Codex tự kiểm tra ID, technique, tổ hợp token/method, truy vết và liên kết. Đây là kiểm tra thiết kế; **toàn bộ 33 TC vẫn Not Run**, chưa có kết quả thực thi Category. BVA theo tài liệu môn [7]; không gán role hoặc ID membership thành trục số để lấy ±1. Metadata và hash giữ trong dữ liệu hỗ trợ.

### 3.14. Bổ sung GitHub Issues và quy tắc evidence — A-02/A-05

**[P-027](23120410_HW02_PromptLog.md#msg-36be906c669996d7cbf9) — prompt nguyên văn:**

```text
cái skill execution + report hình như nó thiếu phần đưa lên github issue hay sao ấy, phần mobile tôi check trên github chưa thấy issue
```

**[P-028](23120410_HW02_PromptLog.md#msg-0453443a1aeea0f60e1a) — prompt nguyên văn:**

```text
bổ sung vào skill đi. thêm nữa là phải chụp ảnh màn hình github issue để làm bằng chứng. vì đề yêu cầu
```

**[P-029](23120410_HW02_PromptLog.md#msg-f3b061c972ae96d0c800) — prompt nguyên văn:**

```text
thử dùng skill [$test-execution-reporting](C:\Users\DELL\\.codex\skills\test-execution-reporting\SKILL.md) để update issue của mobile lên github và chụp log / img jpg lưu bằng chứng
```

**[P-030](23120410_HW02_PromptLog.md#msg-335afed53aaee172819f) — prompt nguyên văn:**

```text
update skill, với mỗi test đượ chạy, ở report phải link tới log hoặc img báo cáo, hiện tại chỉ có bug báo cáo thôi
```

**Phát hiện và bản sửa:**

- **P-027:** sinh viên kiểm tra GitHub và chỉ ra chưa có issue Mobile. Codex đọc skill/report và kiểm tra tracker cả open/closed: chưa có issue. Skill đã nhắc GitHub, nhưng luồng mặc định dừng ở Markdown; đây là thiếu sót trong việc hoàn thiện hồ sơ, không phải phát hiện thêm bug SUT.
- **P-028:** Codex sửa skill để có bước tạo/cập nhật issue đúng đích, tránh trùng, kiểm tra ảnh lỗi, chụp trang issue thật thành JPG và dẫn URL/ảnh/thời gian vào report. Phân biệt ảnh symptom trên SUT với ảnh trang issue đã đăng. Lượt này chỉ sửa skill, chưa đăng issue.
- **P-029:** Codex dùng kết quả cũ, đăng **8 issue (#1–#8)**, gồm **4 vi phạm requirement và 4 sai khác S7**; không biến 15 TC fail thành 15 issue. Codex mở từng issue, xác minh **14 ảnh SUT** từ URL cố định ở commit `6631d92`, lưu **8 JPG trang issue và 1 JPG danh sách**, bổ sung URL/thời gian và log thao tác trong `results.json`. Không chạy lại Mobile; kết quả vẫn **35 pass, 15 fail, 4 blocked**.
- **P-030:** sinh viên yêu cầu mỗi TC đã chạy phải có link log/ảnh, kể cả pass. Codex cập nhật skill, reference và template; link phải đúng TC/run, không lấy link bug hay link results chung ở đầu report thay thế. Không bắt ảnh cho mọi TC khi log đã đủ. Lượt này **chưa sửa report Mobile**; không nhận report đã đáp ứng quy tắc mới ngay tại P-030.

**Giới hạn phiên bản:** các lượt sửa report và giải thích log sau P-030 nằm ngoài bốn prompt được giao ghi lần này. File hiện hành đã commit tại `e1fe254` còn bao gồm các sửa report sau đó (54 link log theo TC/run, chuẩn hóa bảng và hướng dẫn đọc log). Dẫn mốc này để truy file thực, không gán các sửa sau cho output của P-029/P-030. Commit hiện được lưu local, chưa có căn cứ đã push; dùng link tương đối trong [artifact index](artifacts.md), không tạo link GitHub tới commit chưa được xuất bản.

**Bằng chứng và cách kiểm tra:** [report Mobile](../../../tests/hw02/mobile-registration/report.md), [results/log thao tác](../../../tests/hw02/mobile-registration/results.json), [ảnh danh sách issue](../../../tests/hw02/mobile-registration/images/MR-GitHub-issues.jpg), [skill đã bổ sung](../../../skills/test-execution-reporting/SKILL.md). `bugs[].github_activity` ghi thời gian tạo, xác minh nội dung và kiểm tra/chụp trang; `images[]` giữ metadata ảnh. Các phiên bản trước vẫn được dẫn ở A-02/A-05. Chữ in đậm trong mục này và cột bản sửa đánh dấu phần bổ sung theo góp ý.

## 4. Tổng kết độ chính xác AI

Tổng hợp bảy artifact, mỗi artifact tính một lần theo phiên bản được đánh giá trong bảng. A-00–A-03, A-05 và A-06 theo đánh giá đề xuất của bản nháp; A-04 giữ quyết định chấp nhận đầu ra ở bước implementation. A-02 lấy bản sau bổ sung P-028/P-030; A-05 lấy bản `62e34ec` còn thiếu Issues, dù bản sau đã bổ sung. A-06 lấy verdict của bản đầu v0.1 cần bổ sung; việc chấp nhận bản sửa không đổi hồi tố verdict bản đầu. Lần rà soát này sửa đánh giá đề xuất A-05 từ VALID sang INCOMPLETE theo thiếu sót có nguồn; không thêm artifact thứ tám cho từng issue/ảnh.

| Chỉ số | Số lượng | Tỉ lệ |
| --- | ---: | ---: |
| Tổng artifact được phân loại | 7 | 100% |
| VALID (đúng trong phạm vi được đánh giá) | 4 | 57,14% |
| INVALID (sai; loại bỏ) | 0 | 0% |
| INCOMPLETE (cần sửa/bổ sung để dùng) | 3 | 42,86% |

## 5. Kết luận — Khi nào nên / không nên dùng AI?

AI giúp tôi xây skill, thiết kế test và tổng hợp kết quả Mobile. Tuy nhiên, report ban đầu còn thiếu GitHub Issues dù đề yêu cầu. Tôi kiểm tra tracker, phát hiện thiếu sót rồi yêu cầu bổ sung quy trình đăng và chụp trang issue. Codex đã đăng tám issue, lưu chín JPG và cập nhật log; kết quả chạy không đổi. Tôi cũng yêu cầu mỗi TC có link evidence, kể cả pass. Bài học là report có số liệu đúng chưa đồng nghĩa hồ sơ đã đầy đủ. Cần kiểm tra từng đầu ra theo đề, phân biệt ảnh lỗi với ảnh trang issue, giữ bản cũ và nêu ai thực hiện phần sửa. Các verdict trong audit gắn với phiên bản cụ thể.

## 6. Mandatory Disclosure

*“Các skill, bộ thiết kế Mobile Registration và Category Management, code test và report Mobile Registration được sinh phiên bản đầu bởi OpenAI Codex. Tôi đã rà soát thiết kế và các quy ước tên, email, mật khẩu, Unicode; góp ý cách trình bày AI log, tách thiết kế khỏi execution, thu gọn evidence và kết quả chung. Codex sửa skill/code theo các yêu cầu đó, chạy native và đối chiếu UI/DB, ghi 35 pass, 15 fail, bốn blocked. Tôi đã kiểm tra report/results trước khi yêu cầu commit. Với Category, tôi đã đọc bản thiết kế, hỏi lại độ đầy đủ, yêu cầu bổ sung ba nhóm BVA API, token bị sửa và mở lại phiên user; Codex cập nhật từ 24 lên 33 TC. Tôi đã đọc hai file hoàn thiện rồi yêu cầu commit; các TC Category chưa được chạy. Tôi kiểm tra tracker, nhận thấy thiếu GitHub Issues và yêu cầu bổ sung ảnh trang issue cùng link evidence cho từng TC. Codex đã đăng tám issue, lưu chín JPG và sửa skill theo yêu cầu; việc đăng/chụp không phải lần chạy lại SUT. Phần góp ý và quyết định sử dụng do tôi đưa ra; việc thực thi, đăng issue và sửa file do Codex thực hiện. AI Audit Report chi tiết đính kèm ở Phụ lục A. Tôi cam đoan không dùng AI để sinh bất kỳ artifact nào thuộc danh mục bị cấm.”*

## Chữ ký

| Mục | Giá trị |
| --- | --- |
| Họ tên sinh viên (in hoa) | TRẦN QUỐC VỸ |
| MSSV | 23120410 |
| Lớp / Khóa | 23_3 |
| Môn học | Kiểm chứng Phần mềm |
| Ngày ký | |
| Chữ ký | |

## Tham khảo

[1] Đề “HW02 – Domain Testing on EShop,” §2 và §9. [Tài liệu đề bài](references/hw02-assignment.md).

[2] FIT@HCMUS, “AI Audit Report — Mẫu 5 mục cho mỗi Artifact,” 2026 v1.0, §2–6. [Mẫu AI-02](references/ai-audit-template.md).

[3] FIT@HCMUS, “Biểu mẫu Khai báo Sử dụng AI,” 2026 v1.0, sáu câu hỏi khai báo. [Mẫu AI-03](references/ai-disclosure-template.md).

[4] Các nguồn khảo sát và phương pháp đã dùng khi xây skill: [research của bản Domain/BVA hiện tại](https://github.com/tranquocvy/eshop-sut/blob/ddcacdf72a041aca8fb37325d3c26b4e6290840e/skills/domain-bva-testing/references/research.md), gồm GitHub/Reddit, Cem Kaner và ISTQB CTFL v4.0.1 §4.2.1–4.2.2. Các nguồn này không thay bài giảng của môn.

[5] Quy cách evidence và kết quả kiểm tra: [evidence](https://github.com/tranquocvy/eshop-sut/blob/8018b73e9e0d9066efdb1ffe3512303e033a6cb4/skills/test-execution-reporting/references/evidence.md), [output công cụ](verification/design-execution-helpers.txt).

[6] EShop, “Đặc tả Yêu cầu Hệ thống,” FR-01/FR-20, và “API Specification,” §1.1. [README](../../../README.md), [API](../../../api_specification.md).

[7] Tài liệu tự học CTFL của môn, trang PDF 43–44, [bản web cùng tài liệu](https://www.fit.hcmus.edu.vn/~lqvu/Courses/SoftwareTesting/istqb-foundation-selfstudy.html); Cem Kaner, “Teaching Domain Testing: A Status Report,” §2, [nguồn tác giả](https://kaner.com/pdfs/domain_testing_cseet.pdf).

[8] Bộ thiết kế Mobile Registration: [các phiên bản A-03](artifacts.md#a-03--thiết-kế-mobile-account-registration), bản v0.3 tại commit `5ca63e1`.

[9] Bộ code test Mobile Registration, [bản output A-04](https://github.com/tranquocvy/eshop-sut/blob/b8b1d2b18203a0ebf0a24352890da1e80fc0d5fc/tests/hw02/mobile-registration/IMPLEMENTATION.md), và lượt triển khai [P-015](23120410_HW02_PromptLog.md#msg-dc4f2e51b024238929a8); kiểm tra tĩnh, chưa execution.

[10] Mobile Registration, [report và kết quả execution](https://github.com/tranquocvy/eshop-sut/blob/62e34ecbcce65a8c803625ca8d210dfd9176dbbe/tests/hw02/mobile-registration/report.md), tại commit `62e34ec`; các lượt [P-016](23120410_HW02_PromptLog.md#msg-ecfe30f8f95eb2cc71f0)–[P-023](23120410_HW02_PromptLog.md#msg-b9e49c78a2be320ca739).

[11] Skill test-execution-reporting, [bản gọn](https://github.com/tranquocvy/eshop-sut/blob/cbf1ba939c9a0b41281ccc1f053096ee60035897/skills/test-execution-reporting/SKILL.md), commit `cbf1ba9`; [diff cải thiện workflow](https://github.com/tranquocvy/eshop-sut/compare/8018b73e9e0d9066efdb1ffe3512303e033a6cb4...cbf1ba939c9a0b41281ccc1f053096ee60035897).

[12] EShop, FR-14 và FR-12; “API Specification,” §3.4. [README](../../../README.md), [API](../../../api_specification.md); [các phiên bản Category Management — A-06](artifacts.md#a-06--thiết-kế-category-management). Bản v0.2 được lưu tại commit `b84417b`.

[13] Các lượt bổ sung Issues/evidence — P-027–P-030, [Prompt Log](23120410_HW02_PromptLog.md#msg-36be906c669996d7cbf9); [các phiên bản A-02/A-05](artifacts.md), bản trước `6631d92` và bản bổ sung tại commit local `e1fe254`; đề HW02 §6.4, §14.
