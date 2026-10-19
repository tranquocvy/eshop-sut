# Evidence gọn và ảnh JPG

Mục tiêu là chứng minh actual và truy lại **TC → run → observation/ảnh → bug**. TC ID/run ID trong nguồn chung đủ làm khóa; không cần thư mục hoặc manifest cho mỗi TC.

## Chọn bằng chứng

| Trường hợp | Lưu mặc định |
| --- | --- |
| TC pass | Actual và observation/assertion cụ thể trong kết quả chung; không bắt ảnh |
| Web/native UI | Màn hình, feedback và trạng thái đã quan sát; chụp khi cần chứng minh bằng ảnh hoặc task yêu cầu |
| Persistence/state/sequence | Giá trị liên quan trước–sau và bước thực đã chạy; không suy từ toast hoặc một ảnh tĩnh |
| API | Request đã lọc dữ liệu nhạy cảm, status/response/assertion cần thiết; không bắt ảnh |
| Bug | Expected/actual, input/repro, TC/run và JPG symptom; ảnh input nếu cần |
| Blocked/harness | Lý do và bước cuối; thêm lỗi tool hoặc một ảnh điểm chặn khi hữu ích |

Observation phải từ thao tác thật, không tự viết một kết quả hợp lý rồi gọi là evidence. Chưa quan sát được phần oracle thì ghi giới hạn/blocked. API/DB không chứng minh native UI đã chạy. Nhiều TC được dùng chung ảnh/log khi chỉ rõ entry và phần được chứng minh.

Không lưu toàn bộ UI tree sau mỗi thao tác hoặc cùng trạng thái dưới nhiều tên ảnh. Khi cần debug, lưu đoạn liên quan đến lỗi; log chi tiết là tùy chọn, không phải output mặc định.

## Lưu trong nguồn chung

Run metadata có thời gian/múi giờ, SUT/test revision hoặc diff, layer, môi trường và fixture. TC có status, expected/nguồn tham chiếu, actual, observations và bug/evidence refs. Ảnh chỉ cần đường dẫn, TC/run, capture time và trạng thái chứng minh, đặt ngay trong kết quả/report. [Template evidence](../assets/evidence-index.template.md) chỉ dùng khi cần index riêng.

Cấu trúc gợi ý khi chưa có:

```text
feature/
  results.json
  report.md
  images/BUG01.jpg
```

Rerun thêm bản ghi có run ID trong nguồn chung; không ghi đè kết quả/ảnh cũ. Nếu framework đã lưu theo run thì giữ dữ liệu gốc và dẫn tới chúng, không sao chép sang nhiều định dạng. Không biến mỗi probe thành bản sao cả catalogue.

## JPG-only cho ảnh tạm của task

- Chụp từ SUT/run thật. Ưu tiên chuyển PNG bytes trong bộ nhớ sang JPEG và chỉ ghi JPG. Không dùng ảnh AI/mockup/source code làm ảnh bug runtime.
- Khi tool buộc ghi PNG tạm: chuyển, kiểm tra JPG giải mã được, đúng kích thước rồi xóa PNG. Không giữ hai định dạng chỉ để dự phòng. JPG chưa đạt thì giữ nguồn để xuất/chụp lại.
- Helper Python/Pillow hỗ trợ:

  ```powershell
  python scripts/export_jpg.py --input '<capture-tam.png>' --output '<images/BUG01.jpg>' --remove-source
  ```

  Chỉ dùng `--remove-source` cho PNG tạm tạo trong task. Helper kiểm tra JPEG trên đĩa trước khi xóa; lỗi xuất không làm mất nguồn. Không có cờ này sẽ giữ nguồn, phù hợp ảnh người dùng cung cấp. Ảnh đã là JPG và đạt yêu cầu thì dùng lại, không chuyển/sao chép thêm.
- Mở JPG sẽ dùng trong report/issue để kiểm tra đúng màn hình, input/thông báo và chữ đọc được. Chỉnh ảnh phải giữ ngữ cảnh cần chứng minh và ghi rõ thay đổi. Ảnh gốc cần giữ theo yêu cầu riêng thì lưu có kiểm soát; không tự xóa.
- Lấy capture time từ lúc chụp. Giờ chuyển JPG, mtime hoặc EXIF không rõ nguồn không thay capture time. Không bắt file hash/manifest riêng cho từng ảnh nếu task không cần.

## Report và Issues

Nhúng JPG bug cùng caption ngắn: TC/run, trạng thái và capture time. Caption chỉ nhận phần ảnh chứng minh; input/persistence bổ sung nằm trong kết quả chung. Dùng link tương đối; kiểm tra ảnh nhúng và số liệu trong Markdown.

HW02 §6 yêu cầu ảnh bug trong Issues, §14 yêu cầu hồ sơ/ảnh trên trang Issues. Ảnh issue khác ảnh symptom SUT: chỉ chụp trang thật sau khi đã đăng. JPG là lựa chọn định dạng người dùng, không phải quy định đuôi ảnh của đề.

Report-only không chụp trạng thái mới rồi gán vào run cũ. Không tự xóa/sắp xếp lại evidence cũ chỉ để áp dụng cấu trúc gọn, trừ khi được giao dọn chúng.
