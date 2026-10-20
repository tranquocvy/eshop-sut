**Khoa Công nghệ Thông tin (FIT) – Trường Đại học Khoa học Tự nhiên (HCMUS)**

**Kiểm chứng Phần mềm (AI-augmented · 2026)**

**CHÍNH SÁCH AI · BIỂU MẪU — 2026 v1.0**

# Biểu mẫu Khai báo Sử dụng AI — HW02

*Biểu mẫu được FIT@HCMUS điều chỉnh từ Med Kharbach, PhD (2026), AI Use Policy Templates for Higher Education. Giấy phép CC BY-NC-SA 4.0.*

> Bản nháp khai báo việc xây/sửa ba skill, thiết kế, triển khai, thực thi và báo cáo Mobile Account Registration, cùng thiết kế/review, implementation và execution/report Category Management; tiếp tục bổ sung theo tiến độ HW02.

## 1. Thông tin môn học và sinh viên

| Mục | Giá trị |
| --- | --- |
| Môn học | Kiểm chứng Phần mềm |
| Mã bài tập | HW02-AI |
| Tên bài tập | Domain Testing on EShop |
| Cấp độ AI (1–5) | Chính sách Open theo đề HW02; chưa xác định mức tương ứng trên thang 1–5 |
| Ngày sử dụng AI | 19–20/10/2026 |
| Họ tên sinh viên | TRẦN QUỐC VỸ |
| MSSV | 23120410 |
| Lớp / Khóa | 23_3 |

## 2. Câu hỏi khai báo

### 1. Công cụ AI đã dùng

OpenAI Codex, model gpt-6.1-sol.

### 2. Giai đoạn nào của bài tập có dùng AI

- [x] Outline: tổ chức quy trình AI log, thiết kế test và thực thi/báo cáo.
- [x] Viết nháp: hướng dẫn skill, quy cách biểu mẫu, bộ thiết kế Domain/BVA và TC Mobile Registration, Category Management.
- [x] Phản hồi: đối chiếu HW01, giải thích Domain/BVA, cách đọc bộ test và ranh giới giữa đặc tả với giả định.
- [x] Sửa chữa: cải thiện log, tách hai skill kỹ thuật, cập nhật thiết kế và thu gọn skill/evidence/report; sửa lỗi harness khi execution.
- [x] Code: helper đồng bộ log, tính điểm biên, xuất JPG, các kiểm tra helper và bộ code triển khai 54 TC Mobile Registration và 33 TC Category Management.
- [x] Khác: khảo sát skill public trên GitHub/Reddit; Codex chạy kiểm thử native, đối chiếu UI/DB và tổng hợp report/results; chạy Web/API Category, đăng GitHub Issues và lưu ảnh bằng chứng.

### 3. Prompt / nhiệm vụ chính cho AI

**Prompt 1 — [P-000](23120410_HW02_PromptLog.md#msg-55324f24f7a915146521) — 19:15:38 19/10/2026 (UTC+07:00):**

```text
như này căng quá nhỉ, đề rất khuyến khích việc tạo skill để thực hiện các việc này. Trước hết, hãy xem lại các qui định về ai log các file ai template để sinh ra 1 skill mà đề nhắc đến, tức là tự điền vào log
```

**Prompt 2 — [P-003](23120410_HW02_PromptLog.md#msg-d9b48702e80bca216e2a) — 20:25:47 19/10/2026 (UTC+07:00):**

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

**Prompt 3 — [P-023](23120410_HW02_PromptLog.md#msg-b9e49c78a2be320ca739) — 02:42:21 20/10/2026 (UTC+07:00):**

```text
oke tiếp tục dùng skill để tiếp tục chạy test `$test-execution-reporting`
```

Các lượt còn lại được ghi trong [Prompt Log](23120410_HW02_PromptLog.md), gồm 31 mục P-000–P-030 theo phạm vi được giao. P-008–P-014 là thiết kế/review, P-015 triển khai code; P-016–P-023 là execution, review flow/evidence và sửa skill/report. [P-024](23120410_HW02_PromptLog.md#msg-2642f1f9f300cb746a59)–[P-026](23120410_HW02_PromptLog.md#msg-7614bb5c1dae4235dc44) là ba lượt sinh, rà lại và bổ sung bộ thiết kế Category Management. P-027–P-030 là bốn lượt kiểm tra thiếu Issues Mobile, sửa skill, đăng/chụp issue và bổ sung yêu cầu link evidence từng TC. Các lượt sửa report/commit tiếp theo không được đưa vào phạm vi log lần này. Đây chưa phải toàn bộ lịch sử dùng AI của HW02.

### 4. Phần cụ thể AI đóng góp

Codex xây và sửa ba skill `course-ai-log`, `domain-bva-testing`, `test-execution-reporting`, cùng template và helper. Với Mobile Registration, Codex đọc FR-01/FR-20, lập mô hình miền, chọn điểm BVA và viết hai tài liệu thiết kế; sau review của tôi, bộ test từ 46 lên 54 TC, có 37 mục tiêu miền và 18 boundary items. Codex triển khai catalogue/runner từ hai tài liệu đã duyệt; bước implementation ban đầu chỉ kiểm tra tĩnh.

Trong execution, Codex thao tác trên Android native, dùng SQLite chỉ đọc làm oracle phụ trợ, sửa các lỗi harness và đối chiếu actual với expected. Codex còn thu gọn skill và output theo góp ý của tôi: một nguồn results.json, report Markdown dễ đọc và JPG cần thiết. Kết quả cuối có 35 pass, 15 fail và bốn blocked do thiếu Confirmation; tám nhóm phát hiện gồm bốn vi phạm requirement và bốn sai khác S7. Ở bản report trước, GitHub Issues chưa được đăng. Sau khi tôi phát hiện và giao bổ sung tại P-027–P-029, Codex đăng tám issue, kiểm tra 14 ảnh SUT hiển thị và lưu tám JPG trang issue cùng một JPG danh sách; URL, thời gian và log thao tác nằm trong report/results. Việc này dùng kết quả cũ, không chạy lại SUT. Ở P-030, Codex cập nhật skill để mỗi TC đã chạy có link log/ảnh đúng TC/run, kể cả pass; lượt đó chưa sửa report Mobile.

Với T03 Category Management, Codex dùng skill `domain-bva-testing` đọc FR-14/FR-12 và API, tạo `design.md`, `test-cases.md` ban đầu có 24 TC. Sau yêu cầu bổ sung của tôi, Codex thêm TC25–33, cập nhật TC10 và truy vết thành 33 TC, 19 mục tiêu miền, 6 BVA items theo lớp Web/API. Hai file đã được lưu tại commit `b84417b`; đó là trạng thái thiết kế trước execution. Theo [P-031](23120410_HW02_PromptLog.md#msg-078e737e05a56044cac5), Codex triển khai runner/catalogue 33 TC và kiểm tra tĩnh, chưa chạy SUT ở lượt đầu. Theo [P-032](23120410_HW02_PromptLog.md#msg-ecff2281e0534402997b), Codex chạy 12 TC Web/21 TC API trong runtime riêng, ghi 25 pass, 8 fail, 0 blocked và 0 not_run; hoàn thiện report có log cho từng TC, đăng ba issue #9–#11 và lưu 8 JPG actual + 3 JPG trang issue + 1 JPG danh sách. Các sửa harness và bản implementation ban đầu được giữ tại [A-07/A-08](artifacts.md#a-07--code-test-t03-category-management).

### 5. Cách tôi rà soát / chỉnh sửa / xác minh đầu ra AI

Tôi đã đọc output AI log, cung cấp HW01 để đối chiếu và yêu cầu sửa thành skill dùng chung. Tôi đề xuất tách thiết kế khỏi execution/reporting để sinh TC nhanh, yêu cầu evidence rõ và JPG theo task. Với bộ TC Mobile, tôi hỏi lại lý thuyết/cách đọc và review tên, whitespace, case email, trim, special và Unicode code point; Codex cập nhật thiết kế theo các ý kiến này. Ở bước implementation, tôi giữ nguyên output vì dựa trên hai tài liệu đã duyệt.

Khi bắt đầu execution, tôi yêu cầu dừng để xem flow, nhận thấy quá nhiều file/ảnh và yêu cầu kết quả chung, xóa PNG tạm sau khi kiểm tra JPG, thu gọn skill/report và bỏ PDF. Codex thực hiện sửa file, kiểm tra helper JPG (10 kiểm tra đạt ở bản sửa) và chạy lại các phần bị ảnh hưởng bởi harness. Codex kiểm tra UI/DB trước khi resume; các lỗi idle, focus/IME và bỏ sót validation đang hiện được ghi trong history, tách khỏi bug sản phẩm. Expected không đổi theo code SUT.

Tôi đã kiểm tra hai file report/results rồi yêu cầu commit riêng runner và report. Báo cáo giữ rõ 50 TC được đánh giá, bốn TC Confirmation bị chặn; coverage exercise không đồng nghĩa tỷ lệ pass. Các kiểm tra tĩnh ban đầu và việc tôi đọc tài liệu được phân biệt với thao tác chạy native do Codex thực hiện. Chi tiết và các phiên bản nằm trong AI Audit Report.

Với Category, tôi đã đọc bộ 24 TC và hỏi lại liệu đã đủ theo đặc tả và lý thuyết Domain/BVA. Sau phần rà soát của Codex, tôi yêu cầu thêm tên dài 1/2 ký tự ở API, token bị sửa payload/chữ ký trên các phương thức thay đổi dữ liệu và mở lại Admin từ token user đã lưu. Codex thực hiện sửa file, giữ bản đầu và diff; tôi đọc hai file hoàn thiện rồi yêu cầu commit. Việc review thiết kế này không phải xác nhận kết quả chạy Category.

Tôi đã kiểm tra GitHub và nhận thấy Mobile chưa có issue, rồi yêu cầu bổ sung vào skill cùng ảnh trang issue theo đề. Tôi tiếp tục giao Codex đăng các phát hiện và yêu cầu skill bắt link log/ảnh cho từng TC. Codex thực hiện đăng, mở lại issue để kiểm tra ảnh và lưu bằng chứng; đây là thao tác của Codex theo yêu cầu của tôi. Mốc file `e1fe254` còn có các sửa report sau P-030; các lượt đó không nằm trong bốn prompt được chọn lần này. Xem [A-02/A-05 và phiên bản đối chiếu](artifacts.md).

Với execution Category, tôi đã kiểm tra report rồi yêu cầu commit. Việc thao tác Web/API, đối chiếu DB, sửa harness, đăng issue và chụp bằng chứng do Codex thực hiện. Hai lượt được chọn ghi log lần này là implementation và execution/report; lời xác nhận review được dùng làm căn cứ, không thêm thành prompt mới. Kết quả T03 tại commit local `94fd43c`; chưa coi việc đọc report là xác nhận sinh viên tự chạy hoặc kiểm tra từng assertion.

### 6. Trích dẫn

[1] OpenAI, “Codex,” model gpt-6.1-sol, công cụ sử dụng trong các lượt trao đổi được ghi ngày 19–20/10/2026.

[2] “HW02 – Domain Testing on EShop,” §2, §6–7 và §9. [Đề bài](references/hw02-assignment.md).

[3] FIT@HCMUS, “AI Audit Report” và “Biểu mẫu Khai báo Sử dụng AI,” 2026 v1.0. Xem [AI Audit Report đã điền](ai-audit.md) và [Prompt Log](23120410_HW02_PromptLog.md).

[4] Các repo/cộng đồng và nguồn phương pháp đã tham khảo: [research được lưu cùng artifact](https://github.com/tranquocvy/eshop-sut/blob/ddcacdf72a041aca8fb37325d3c26b4e6290840e/skills/domain-bva-testing/references/research.md), gồm nguồn tác giả Cem Kaner và ISTQB CTFL v4.0.1. Chi tiết revision và phạm vi sử dụng được ghi trong tài liệu này.

[5] EShop, FR-01/FR-20, [đặc tả](../../../README.md); [các phiên bản thiết kế Mobile Registration](artifacts.md#a-03--thiết-kế-mobile-account-registration), v0.3 tại commit `5ca63e1`.

[6] Code test Mobile Registration, [artifact A-04](https://github.com/tranquocvy/eshop-sut/blob/b8b1d2b18203a0ebf0a24352890da1e80fc0d5fc/tests/hw02/mobile-registration/IMPLEMENTATION.md); prompt và output gốc tại [P-015](23120410_HW02_PromptLog.md#msg-dc4f2e51b024238929a8).

[7] Mobile Registration, [report/kết quả runtime và evidence](https://github.com/tranquocvy/eshop-sut/blob/62e34ecbcce65a8c803625ca8d210dfd9176dbbe/tests/hw02/mobile-registration/report.md), commit `62e34ec`; skill execution/reporting [bản gọn](https://github.com/tranquocvy/eshop-sut/blob/cbf1ba939c9a0b41281ccc1f053096ee60035897/skills/test-execution-reporting/SKILL.md), commit `cbf1ba9`.

[8] Category Management, [thiết kế và TC trước/sau bổ sung — A-06](artifacts.md#a-06--thiết-kế-category-management), v0.2 tại commit `b84417b`; test basis EShop FR-14/FR-12 và API §3.4. Ba prompt gốc ở P-024–P-026.

[9] Mobile Issues và quy tắc evidence, P-027–P-030 trong [Prompt Log](23120410_HW02_PromptLog.md#msg-36be906c669996d7cbf9); [GitHub Issues](https://github.com/tranquocvy/eshop-sut/issues), [report/log/bằng chứng hiện hành](../../../tests/hw02/mobile-registration/report.md), mốc local `e1fe254`.

[10] T03 implementation/execution, [P-031](23120410_HW02_PromptLog.md#msg-078e737e05a56044cac5) và [P-032](23120410_HW02_PromptLog.md#msg-ecff2281e0534402997b); [artifact A-07/A-08](artifacts.md#a-07--code-test-t03-category-management), report/results và ảnh tại commit local `94fd43c`.

## 3. Cam đoan trung thực

*Bằng việc ký tên dưới đây, tôi cam đoan thông tin khai báo ở trên là chính xác và đầy đủ. Tôi hiểu rằng việc không khai báo hoặc khai báo sai lệch về việc dùng AI sẽ bị coi là vi phạm liêm chính học thuật và có thể dẫn đến điểm 0 cho bài tập cùng việc bị chuyển lên hội đồng kỷ luật.*

## Chữ ký

| Mục | Giá trị |
| --- | --- |
| Họ tên sinh viên (in hoa) | TRẦN QUỐC VỸ |
| MSSV | 23120410 |
| Lớp / Khóa | 23_3 |
| Môn học | Kiểm chứng Phần mềm |
| Ngày ký | |
| Chữ ký | |
