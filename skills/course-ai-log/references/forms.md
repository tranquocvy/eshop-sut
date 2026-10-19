# Viết biểu mẫu AI để sinh viên đọc và nộp

Đọc mẫu hiện hành trước khi điền. Giữ các mục và nội dung bắt buộc của mẫu; không sửa file template gốc. Nếu người dùng cung cấp một bài mẫu, chỉ học cách trình bày; yêu cầu của bài hiện hành vẫn quyết định nội dung.

## Ba đầu ra có chức năng khác nhau

| Tài liệu | Nội dung |
| --- | --- |
| Prompt Log | Lịch sử prompt và phản hồi nguyên văn theo phạm vi, gồm các lượt sửa và thông báo tiến độ |
| AI-02 Audit | Một hàng cho mỗi artifact; output/phiên bản được audit, verdict, căn cứ và bản sửa |
| AI-03 Disclosure | Khai báo công cụ, giai đoạn, prompt chính, đóng góp và việc xác minh |

AI-05 dùng khi được giao hoặc hồ sơ yêu cầu và đã có mẫu phù hợp. AI Critique/PDF tạo khi được giao, theo đề. Dùng tên file hiện có; nếu chưa có, tên ngắn như `prompt_log.md`, `AI_Audit_Report.md`, `AI_Disclosure.md` là lựa chọn tổ chức.

## AI-02 — bảng năm cột

Điền thông tin sinh viên đã biết và thông tin thật của bài. Nếu đang soạn tự động, đặt một ghi chú đầu tài liệu: **“Bản nháp; nhận xét và verdict dưới đây là đề xuất để sinh viên rà soát.”** Khi một phần đã được duyệt, chỉ rõ phần còn dự thảo; không xóa hay hạ trạng thái phần đã được sinh viên xác nhận.

| Cột | Cách điền |
| --- | --- |
| (1) Prompt + Công cụ | Artifact ID ngắn `A-00`, tên, tool, ngày giờ, Prompt ID `P-000` và prompt nguyên văn. Prompt dài có thể đặt trong mục chi tiết bên dưới với dẫn chiếu rõ. |
| (2) Output AI | Tên sản phẩm/phiên bản và vị trí output gốc. Dán nguyên văn output được audit hoặc screenshot có chú thích theo mẫu; output dài đặt tại mục chi tiết dưới bảng. |
| (3) Verdict | Đề xuất VALID / INVALID / INCOMPLETE có căn cứ. Ghi chú nháp chung xác định đây chưa phải verdict sinh viên duyệt; không lặp trạng thái chờ trong từng ô. |
| (4) Lý do | Nói cụ thể đáp ứng hay sai/thiếu gì, dẫn requirement, slide, ISTQB/RFC hoặc kết quả đối chiếu phù hợp. Không bịa số mục, không lấy ví dụ kỹ thuật trong template làm bằng chứng. |
| (5) Bản SV sửa | Nêu bản sửa và vị trí thay đổi có thật; đánh dấu phần sửa. Nếu chưa sửa, ghi “Chưa sửa” hoặc “Không cần sửa nội dung” khi phù hợp. Nếu AI sửa theo yêu cầu sinh viên, viết đúng điều đó. |

Giữ đủ nội dung prompt/output được audit trong bộ báo cáo như mẫu yêu cầu. Không nhân bản toàn bộ các thông báo tiến độ vào AI-02: chúng đã có trong Prompt Log. Khi output là file được sinh qua công cụ, giữ phiên bản/ảnh chụp/nội dung phù hợp để thấy artifact ban đầu; chỉ chép lời final “đã tạo file” không thay thế được sản phẩm đang audit. Tránh chỉ dẫn tới một file cuối đã ghi đè bản gốc.

### Chọn phạm vi và verdict

Đánh giá đúng **nhiệm vụ đã giao cho artifact**:

- Yêu cầu xây skill: xem hướng dẫn/tài nguyên có thực hiện được quy trình đã giao, có sai hay thiếu gì. Việc cả HW còn chưa quay video không tự làm skill sai. Nếu nhiệm vụ bao gồm cả demo, phần demo thiếu mới là thiếu trong phạm vi đó.
- Yêu cầu khung báo cáo: có placeholder theo yêu cầu chưa đủ để kết luận INCOMPLETE; xem khung có thiếu mục cần có hay không. Nếu yêu cầu báo cáo hoàn chỉnh mà chỉ nhận khung, đó mới là thiếu.
- Yêu cầu thiết kế test: thiếu ca bắt buộc hoặc tự bịa Actual/Pass là vấn đề cụ thể. Chưa chạy SUT không tự là lỗi nếu chỉ được giao thiết kế; chưa chạy vẫn phải thể hiện trạng thái thật.

VALID: đáp ứng phạm vi, dùng nguyên nội dung. INVALID: sai đến mức loại bỏ. INCOMPLETE: còn nội dung cần sửa/bổ sung để dùng được. Không tạo lỗi, phần sửa hoặc artifact phụ chỉ để có đủ loại verdict hay số hàng. Nếu chưa kiểm tra được, để trống verdict và ghi đúng việc cần kiểm tra, không đoán.

Mỗi artifact giữ ID ổn định và các lượt quan trọng; một artifact qua nhiều lượt sửa vẫn có thể là một hàng với lịch sử rõ. Giữ output sai ban đầu và đánh dấu bản sửa bằng diff, chữ nổi bật hoặc cách tô sáng giữ được trong định dạng nộp.

### Thống kê và kết luận

Thống kê phải dựa trên cùng tập verdict: bản nháp có thể có **tổng hợp đánh giá đề xuất**, ghi rõ nhãn đó một lần; nó chưa phải tỷ lệ sinh viên đã xác nhận. Không trộn verdict đề xuất với verdict đã duyệt rồi gọi tất cả là đã duyệt. Bản hoàn tất tính từ những artifact đã audit được sinh viên xác nhận. Mỗi tỷ lệ = số artifact loại đó / tổng được phân loại × 100%; báo số chưa đánh giá riêng. Tổng bằng 0 thì tỷ lệ N/A.

Kết luận bám pattern đã quan sát: AI giúp ở đâu, lỗi cụ thể nào xuất hiện, cách dùng hiệu quả hơn. Tuân độ dài của mẫu hiện hành; AI-02 mẫu môn hiện tại là 80–150 chữ. AI Critique là phần riêng theo đề, không gộp hai mục rồi nhận đạt cả hai.

Giữ Mandatory Disclosure và cam đoan theo mẫu, điền phần đóng góp có căn cứ. Có thể soạn lời văn để sinh viên đọc; chữ ký/ngày ký để người dùng thực hiện, không sao chép chữ ký từ bài cũ.

## AI-03 — khai báo tự nhiên, đúng sáu câu hỏi

1. **Công cụ:** tên công cụ thực dùng; model nếu biết chắc và cần ghi. Không giải thích cách parse metadata hoặc liệt kê Python/PowerShell như những AI khác.
2. **Giai đoạn:** tick các giai đoạn thực có AI tham gia; viết “khác” cụ thể khi cần.
3. **Prompt chính:** chọn 2–3 prompt quan trọng nguyên văn theo mẫu, dẫn mã P và log đầy đủ. Không rút gọn lời prompt bằng dấu ba chấm rồi nhận là nguyên văn.
4. **Đóng góp:** một đoạn rõ AI tạo/hỗ trợ sản phẩm nào, dùng vào phần nào. Không tự bịa phần trăm hoặc tuyên bố một phần do sinh viên tự viết khi AI đã soạn.
5. **Rà soát/xác minh:** mô tả hành động thật và kết quả. Dùng ngôi “tôi” cho việc người dùng đã làm; việc AI tự chạy thì nêu “Codex đã chạy...”. Có thể ghi “Phần rà soát của sinh viên sẽ bổ sung sau khi kiểm tra sản phẩm” nếu chưa có dữ kiện; không kéo dài thành nhiều lời phủ nhận.
6. **Trích dẫn:** dùng phong cách mẫu yêu cầu và nguồn thực dùng; thông tin công cụ/model lấy từ dữ kiện đã xác minh, không cần đưa mã trường kỹ thuật vào câu văn.

Điền thông tin ổn định đã có nguồn. Không lấy thang Bloom-AI thay thang AI 1–5. Giữ nguyên cam đoan của mẫu; một nhãn dự thảo chung và chỗ chữ ký trống đủ thể hiện trạng thái.

## AI-05 — checklist theo tiến độ thật

Đọc mẫu được áp dụng; bài cũ có thể làm nguồn cấu trúc khi người dùng yêu cầu, còn bản đã tick của bài cũ không chứng minh bài mới hoàn tất. Đánh dấu từng mục có căn cứ, để mục chưa làm ở trạng thái chưa hoàn tất. Không tự biến mỗi ô checklist thành một yêu cầu nộp mới ngoài đề/chính sách.

Nguồn thiếu hay mâu thuẫn chỉ ghi ngắn tại nơi cần xử lý hoặc một ghi chú cuối. Không phát sinh bảng hỏi lặp lại cho thông tin đã có; không tự ký, không gọi bản nháp là hồ sơ đã nộp.
