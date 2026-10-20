# T05 — Execution implementation

Chạy bộ 45 TC v0.1 được Vỹ xác nhận tại commit `4bb5158`; không sửa design/test-cases trong execution. [report.md](report.md) là bản đọc; [results.json](results.json) là nguồn chung cho tất cả TC, history và repro bổ trợ.

## Môi trường

Ngày20/10/2026 UTC+7. Backend cũ không còn lắng nghe3000; khởi động bản copy nguyên nội dung server.js/database.js từ repo vào `HW02/.runtime/T05-execution-20261020/backend` (ngoài Git), PID27228. Database mới do init seed tại runtime riêng; không reset database T03/T04 hay DB được Git theo dõi. Module resolution dùng NODE_PATH tới backend/node_modules hiện có. SHA256 server.js nguồn và runtime cùng `E2263811A1690A63A7DBB4446C3FD33FB87F50D073D9F8CDFAB7083A52F5E8ED`. Web Vite5173 đang chạy được tái sử dụng. Không sửa logic SUT.

Runner dùng Python/Playwright ở venv T03 và Chromium156.0.8078.4. Không thêm dependency khi chạy. Runtime path trong results để đối chiếu môi trường thực; replay ở máy khác cần DB riêng trong `.runtime`, seed U/V đúng README, dịch vụ nguồn đúng phiên bản và run ID mới.

## Mapping

- `scripts/run.py` đọc trực tiếp năm cột TC từ Markdown, kiểm tra45ID duy nhất. Có handler WebW01–W19 và APIA01–A26. Không chạy nếu thiếu `--execute`; có `--case` để rerun đúng phần cần thiết, không ghi đè run ID đã có.
- U/V reset counter/lock/reset_token giữa TC; sequence nội bộ không reset. Fixture short.fr02@example.com/Ab1! tạo trực tiếp để tránh validator đăng ký che login. Email X được xác nhận vắng. Fn dựng từ request thật, không ép counter khi lỗi SUT cản precondition; vậy W04/W05/W12/A03/A04/A07/A26 blocked. W16/A20 dừng khi success bước3 bị khóa sớm, không giả đã kiểm tra reset chuỗi.
- FL trực tiếp chỉ dùng nơi TC cho phép: khóa U n=3 với deadline còn khoảng20s (t0 nominal10s trước); A11 thiết lập khóa30s rồi đợi thật31s. Không giả precision tuyệt đối cho τ10s. Web context mới giữa TC, giữ context giữa sequence.
- Sáu handler ±1ms ghi blocked trước request vì không có clock/trace server đủ chính xác; không thay bằng request sau sleep30s. Nhánh concurrency A26 chưa tiếp cận do F1 sai; cần bổ sung phép đo overlap khi precondition đạt trong lần rerun, không nhận đã exercise concurrency.
- API response status/body và DB before/after được ghi trong entry. JWT che trong logs. Web thao tác form thật bằng Playwright; DOM/UI/network/localStorage quan sát đúng lớp. Screenshot JPG trực tiếp, không giữ PNG tạm.
- `scripts/verify.py` là repro bổ trợ, không thêm TC: chức năng API client harness gửi fetch thật tới SUT, hiển thị status/body và DB observer read-only. Ảnh chụp trang client này ghi rõ là harness, không giả là Web EShop. Đo thời hạn khóa bằng bracket request kích hoạt/deadline DB và xác minh request sau31s vẫn bị từ chối. Các repro khác xác nhận policy findings. Chưa thực hiện thêm control clock hoặc thay Date của backend.
- `scripts/report.py` chỉ tổng hợp nguồn chung, không gọi SUT. Mỗi hàng TC dẫn entry đúng ID/run; bugs giữ ảnh symptom và ảnh trang GitHub issue riêng, kèm thời gian.

## Chạy lại

```powershell
python tests/hw02/fr02-login/scripts/run.py
python tests/hw02/fr02-login/scripts/run.py --execute --db <DB-T05-rieng-trong-.runtime> --run-id FR02-RERUN-NEW --case FR02-W03
python tests/hw02/fr02-login/scripts/verify.py --db <DB-T05-rieng-trong-.runtime> --id FR02-VERIFY-NEW
python tests/hw02/fr02-login/scripts/report.py
```

DB là SQLite runtime đang phục vụ backend, không import database.js vào DB có dữ liệu cần giữ. Replay suite sau sửa SUT cần đọc giới hạn nhánh concurrency/timing ở trên trước; không tự cho rằng runner hiện tại cung cấp server clock control.

## Lịch sử thật và giới hạn

RUN01 dừng vì locator hồ sơ sai. Sửa href và đọc value input email thay vì inner_text, RUN02 W01 passed; stdout cp1252 làm dừng sau khi lưu W03. Sửa output UTF-8, RUN03 hoàn tất45entry. Giữ lịch sử RUN01/RUN02 trong results; summary chọn RUN03. VERIFY01 có31s wait thật; timestamp và clock bracket lưu ở supplementary. Kết quả:18passed/12failed/15blocked. Không sinh lại TC, sửa expected, sửa SUT, ghi AI Audit hoặc commit/push trong task execution này.
