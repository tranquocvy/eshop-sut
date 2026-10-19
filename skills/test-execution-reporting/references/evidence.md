# Evidence cho execution và báo cáo

Mục tiêu là người đọc truy lại được kết quả, phiên bản SUT và bằng chứng đã quan sát. Đây là quy cách triển khai của skill; HW02 §6 yêu cầu ảnh bug trong GitHub issue, §14 yêu cầu ảnh bug trên trang Issues và các sản phẩm báo cáo. Đề HW02 không quy định đuôi JPG; JPG là lựa chọn người dùng cho ảnh cần xuất, trừ khi task/đề yêu cầu định dạng khác.

## Ghi nhận cùng lúc chạy

Với mỗi run, lưu ID và timestamp có múi giờ, SUT/test revision, lớp Web/native/API, môi trường/browser/device/viewport liên quan, dữ liệu/preconditions và người/công cụ chạy. Nếu working tree có thay đổi ảnh hưởng SUT/test, ghi phiên bản/diff thay vì chỉ commit SHA. Không đưa secrets hoặc dữ liệu ngoài phạm vi vào evidence.

Mỗi TC đã chạy ghi expected có nguồn, actual cụ thể, status và ít nhất một tham chiếu evidence phù hợp để đối chiếu actual. Có thể dùng chung một log cho nhiều TC khi chỉ rõ đoạn/entry tương ứng. `blocked` ghi điểm chặn và evidence lỗi nếu có; `not_run` ghi lý do, không tạo ảnh hay log chạy giả.

| Loại kiểm tra | Evidence thích hợp |
| --- | --- |
| Web/native UI | Ảnh trạng thái và dữ liệu liên quan tại bước quyết định; thêm trạng thái trước/sau nếu cần hiểu kết quả |
| API | Method/path, request đã xử lý thông tin nhạy cảm, status/response, assertion/exit code và thời gian; ảnh khi task/đề yêu cầu |
| Bộ đếm/trạng thái/thời gian | Chuỗi thao tác, mốc thời gian và log/request tương ứng; một ảnh tĩnh không tự chứng minh ranh giới thời gian |
| Bug | TC/run, input/preconditions, expected/actual, ảnh symptom và log bổ sung cần thiết |
| GitHub issue | Issue URL/ID và ảnh trang issue có tiêu đề, expected/actual hoặc evidence đã đính kèm; khác với ảnh symptom trên SUT |

Chụp và lưu evidence trước reset/cleanup. Khi một ảnh chỉ cho thấy một phần kết quả, giới hạn caption theo đúng phần đó. Không dùng ảnh mockup, ảnh sinh bằng AI, screenshot source hoặc ảnh run cũ để chứng minh trạng thái UI của run hiện tại.

## Tổ chức và ánh xạ

Giữ cấu trúc hiện có nếu đủ truy vết. Khi chưa có, có thể dùng:

```text
evidence/<feature>/<run-id>/
  evidence-index.md
  images/<TC-ID>__step03__actual.jpg
  images/<BUG-ID>__github-issue.jpg
  originals/                         # Ảnh nguồn khi đã chuyển định dạng/che dữ liệu
  logs/                              # Request/response, runner output hoặc chuỗi thao tác cần thiết
```

Đây là gợi ý, không bắt tạo file/thư mục rỗng hoặc một ảnh cho mọi thao tác. Kết quả TC có thể nằm trong CSV/JSON/Markdown đang dùng; đừng nhân bản nhiều bộ số liệu. Mỗi rerun có run ID/thư mục riêng, không ghi đè ảnh của lần trước.

Dùng `assets/evidence-index.template.md` hoặc bảng tương đương. Mỗi evidence có ID, TC/run, Bug ID nếu có, đường dẫn tương đối, thời gian capture, bước/trạng thái chứng minh và ảnh nguồn nếu đã chuyển/che. Không lấy giờ export, mtime hoặc EXIF không rõ xuất xứ làm giờ chạy. Thiếu capture timestamp thì ghi chưa biết, vẫn giữ phần nguồn còn truy cập được.

## Xuất ảnh JPG

1. Lưu screenshot thật bằng công cụ của lớp đang chạy. Giữ ảnh gốc khi có chuyển định dạng hoặc che dữ liệu; bản đã che ghi rõ là derivative và giới hạn truy cập ảnh gốc nhạy cảm.
2. Ưu tiên `.jpg` cho ảnh xuất khi task không quy định khác. Nếu công cụ trả PNG hay định dạng khác, chuyển bằng bộ mã hóa JPEG; đổi đuôi file không phải chuyển định dạng.
3. Có thể dùng helper từ thư mục skill với Python 3.10+ và Pillow có sẵn trong môi trường:

   ```powershell
   python scripts/export_jpg.py --input '<screenshot-nguon.png>' --output '<evidence/TC-01__actual.jpg>'
   ```

   Helper giữ file nguồn, không ghi đè đích, không crop/resize/chèn chữ. Nó chuẩn hóa hướng hiển thị theo EXIF khi có, nền trong suốt thành trắng, xuất JPEG chất lượng 95 và kiểm tra file giải mã được. JSON trả về có đường dẫn, kích thước, format, hash và thời gian chuyển; **thời gian chuyển không phải capture time**. Pillow là dependency riêng của helper; ưu tiên runtime có sẵn.
4. Mở ảnh JPG sẽ dùng trong report/issue để kiểm tra đúng màn hình, dữ liệu, thông báo và chữ còn đọc được. JPEG mất mát chất lượng nên giữ ảnh nguồn; nếu không đọc được, xuất lại từ nguồn hoặc chụp đúng vùng cần thiết và giữ ngữ cảnh, không đoán nội dung từ ảnh mờ.
5. Caption nằm trong báo cáo cạnh ảnh: TC/run, bước quan sát, expected/actual liên quan và thời gian capture. Nếu cần crop/chú thích/che thông tin, giữ derivative riêng và ghi thay đổi; helper chỉ chuyển định dạng, không tự che hay chỉnh nội dung.

## Gắn evidence vào báo cáo

- Mỗi kết quả TC và mỗi bug dẫn tới file cụ thể hoặc entry log. Ảnh bug được nhúng và có caption, không chỉ để một thư mục ảnh rời.
- Liên kết trong Markdown dùng đường dẫn tương đối để bộ nộp di chuyển được; trong phản hồi chat dùng đường dẫn đầy đủ khi giới thiệu file cho người dùng.
- Khi xuất PDF theo task/đề, kiểm tra ảnh được nhúng, không mất caption/bảng, text đọc được và số liệu khớp Markdown. Link local trong Markdown không tự chứng minh PDF có ảnh.
- Kiểm tra file tồn tại, nội dung giải mã đúng JPEG, đúng run và số liệu liên quan trước bàn giao. Evidence thiếu thì báo đúng phạm vi thiếu, không nhận là hồ sơ đã đầy đủ.
- Report-only có thể tổng hợp/chuyển ảnh từ dữ liệu có sẵn, không tự mở app chụp một trạng thái mới rồi gán vào run cũ. Cần bổ sung capture thật thì ghi việc còn thiếu hoặc thực hiện khi task đã bao hàm chạy bổ sung.

## Kiểm tra helper chuyển ảnh

Chạy `python -B scripts/test_export_jpg.py` từ thư mục skill, dùng Python có Pillow. Các kiểm tra chỉ tạo ảnh giả lập trong thư mục tạm để kiểm tra chuyển định dạng và bảo toàn file; chúng không phải screenshot hoặc bằng chứng chạy SUT.
