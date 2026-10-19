# Khảo sát nguồn và quyết định xây bộ skill

Khảo sát ngày **19/10/2026**. Các nhận xét là kết quả đọc nguồn, không phải chứng nhận chất lượng/độ phổ biến hoặc kết quả chạy skill cộng đồng. Bộ hiện tại được viết mới; không cài hay sao chép bộ prompt/script của các repo dưới đây.

## GitHub đã kiểm tra

| Nguồn và revision | Điều hữu ích để tham khảo | Phần không áp dụng nguyên trạng |
| --- | --- | --- |
| [aks-builds/quality-skills — test-design-techniques](https://github.com/aks-builds/quality-skills/blob/dbe5dcc80cf4c457152379b38038e26ab992737f/skills/test-design-techniques/SKILL.md), MIT | Đọc bối cảnh trước, chọn kỹ thuật và đưa chi tiết vào reference | Phạm vi QA quá rộng cho HW02; không kéo toàn bộ plugin/framework vào bài |
| [testland/qa — decision-table-test-design](https://github.com/testland/qa/blob/be07002bcccd37022753a984cce26402138ef911/plugins/qa-manual-testing/skills/decision-table-test-design/SKILL.md), MIT | Minh họa phép suy ra từng bước và phân biệt combination với boundary coverage | Đây là decision table, không phải bộ Domain/BVA cho HW02; không lấy nó thay hai kỹ thuật đề giao |
| [rcptrkr/qa-skills — bug-report-forensics](https://github.com/rcptrkr/qa-skills/blob/8757aab2f5e1834be351eeb497bb3e7cf6991e9d/plugins/qa-essentials/skills/bug-report-forensics/SKILL.md), MIT | Oracle, cách tái hiện gọn và bằng chứng | Ưu tiên evidence của cộng đồng không được thay yêu cầu screenshot của HW02; BVA ở roadmap chưa phải skill đã ship |
| [ll0v0ll/test-case-designer](https://github.com/ll0v0ll/test-case-designer/tree/8d48f7e9a436108e15d093da398e458e8b9f7c88) | Tách phân tích khỏi sinh test, truy vết requirement và lớp UI/API | Chưa thấy LICENSE ở revision đã kiểm tra; không sao chép. Không nhập quota test/risk, mandatory approval gate hay công thức sáu điểm vào rubric của môn |

Giấy phép MIT được đọc tại LICENSE của ba repo tương ứng. Do không đưa nguyên văn/chỉnh sửa trực tiếp prompt hoặc code của repo vào bộ này, các liên kết dùng để ghi nhận khảo sát; nếu sau này vendor nội dung MIT thì giữ thông báo bản quyền/giấy phép theo nguồn. Không tự gán giấy phép cho bài của sinh viên.

## Cộng đồng và nguồn kỹ thuật gốc

- [Thảo luận QA skills trên Reddit](https://www.reddit.com/r/claudeskills/comments/1w0kaxm/what_claude_skillsai_skills_are_your_qa_teams/): cho thấy người dùng đang tìm workflow QA cụ thể; không phải chứng minh một skill Domain/BVA đã được kiểm chứng.
- [Thảo luận workflow sinh test và quản lý test cases](https://www.reddit.com/r/softwaretesting/comments/1ttt2hg/ado_claude_test_case_magement/): có chia sẻ thử skill sinh case đơn giản. Chỉ là kinh nghiệm của người đăng, không dùng làm định nghĩa kỹ thuật hay căn cứ chấm bài.
- [Cem Kaner — Teaching Domain Testing: A Status Report](https://www.kaner.com/pdfs/domain_testing_cseet.pdf), đặc biệt §2: nguồn tác giả về domain/partition/đại diện và rủi ro khi kết hợp biến. Dùng để kiểm tra tư duy chọn dữ liệu, không thay slide của môn.
- [ISTQB CTFL Syllabus v4.0.1](https://istqb.org/wp-content/uploads/2024/11/ISTQB_CTFL_Syllabus_v4.0.1.pdf), §4.2.1–4.2.2: nguồn chính thức cho EP, miền có thứ tự và coverage items BVA 2-value/3-value. Không tự quy tất cả biến thể Domain Testing về một thuật ngữ duy nhất.

Kết quả tìm kiếm có xuất hiện bài HW02/EShop của sinh viên khác. Không mở rộng đọc bài/prompt/test case của họ để lấy lời giải. Đề HW02 §17 cấm sao chép giữa sinh viên, kể cả prompt; không dùng những bài đó làm mẫu cho bộ này.

## Quyết định cho HW02

Xây **một skill chính với bốn mô-đun**, đúng bốn nhiệm vụ §6; helper chỉ xử lý phép tính biên có input rõ, không nhận đã test SUT. Không tìm thấy trong các nguồn đã kiểm tra một bộ có thể dùng nguyên trạng để đáp ứng đồng thời cách dạy chưa được cung cấp, audit/AI gaps và hồ sơ bug của HW02. Đây là kết luận giới hạn ở phạm vi khảo sát, không phải khẳng định không ai trên Internet có bộ phù hợp.

Tình trạng phương pháp: **cần đối chiếu slide Domain Testing/BVA khi được bổ sung**. Tình trạng kỹ thuật của bộ phải dựa vào kiểm chứng thực tế được báo trong phiên; validation cấu trúc/helper không thay một demo trên feature thật.
