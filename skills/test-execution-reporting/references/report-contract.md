# Kết quả chung và báo cáo

Một nguồn kết quả phục vụ cả bộ TC; report là bản đọc/tổng hợp từ nguồn đó. Dùng output phù hợp của runner, không nhân bản dữ liệu thành JSON + CSV + bảng phụ chỉ vì có thể. CSV là lựa chọn khi người đọc/công cụ cần.

## Nội dung tối thiểu

- **Run:** ID, thời gian/múi giờ, SUT/test revision hoặc diff, layer/môi trường, fixture và người/công cụ thực thi; lưu một lần mỗi run.
- **TC:** ID, run ID, expected/nguồn tham chiếu, actual cụ thể, status, observations/assertions cần chứng minh; bug/ảnh nếu có. Sequence chứa các bước và state liên quan ngay trong entry TC.
- **Evidence:** observation đã lưu hoặc tham chiếu ảnh/đoạn log. Ảnh có capture time và trạng thái chứng minh; không bắt file riêng cho mỗi TC.

Ví dụ entry pass: UI chuyển Login; account theo email 0→1; name/email đúng. Các giá trị phải được quan sát thật, không chỉ có nhãn passed. Chỉ lưu dữ liệu cần đối chiếu, không đính toàn bộ DB/layout hoặc secrets.

Giữ lịch sử rerun trong nguồn chung bằng run ID. Nếu summary dùng kết quả mới nhất thì nêu quy ước; không xóa lần failed/blocked trước. Run bị ngắt ghi bước dở dang và lý do; không tự gán đã pass/fail. Nếu framework đã có lịch sử phù hợp thì tham chiếu output gốc.

## Bản report

Dùng [template](../assets/feature-report.template.md) tùy task: phạm vi/môi trường → bảng kết quả → bug/gap và summary. Dẫn bộ thiết kế/TC đúng phiên bản; chỉ chèn lại mô hình Domain/BVA khi sản phẩm cần. Không lập bảng truy vết thứ hai nếu nguồn hiện có đã đủ.

`report.md` phải đủ để người học review kết quả mà không cần đọc JSON cho từng TC. Bảng gợi ý: **TC có link về thiết kế | Nội dung kiểm tra / input chính | Expected | Actual | Kết luận / bug**. Nêu dữ liệu mặc định và giải thích ký hiệu một lần; mỗi hàng chỉ ghi input khác biệt và expected ngắn, giữ ý nghĩa của oracle đã duyệt. Với sequence, giữ các lần chuyển trạng thái và điều kiện cuối; không rút gọn thành chỉ expected của bước đầu. Input của ca chưa chạy là dữ liệu dự kiến, không phải xác nhận đã nhập. Expected vẫn hiển thị cho ca blocked/not_run; actual ghi rõ điểm chặn hoặc chưa có quan sát.

Dùng nhãn dễ hiểu kèm status gốc: Đạt (passed), Không đạt (failed), Bị chặn (blocked), Chưa chạy (not_run); ca bị ngắt ghi rõ dở dang. Có thể chia bảng theo nhóm chức năng để dễ đọc, không thêm bảng chi tiết trùng lặp. Link TC dẫn tới tài liệu gốc, bug dẫn tới detail/ảnh ngay trong report. JSON giữ chi tiết assertion/lịch sử để kiểm tra sâu; không biến JSON thành tài liệu bắt buộc phải đọc để biết vì sao TC đạt hay không đạt. Không ghi sinh viên đã nghiệm thu nếu chưa có review thật.

Mỗi bug có precondition/input, steps, expected/actual, oracle, TC/run, ảnh và trạng thái issue. Đặt detail trong report; chỉ tách file bug khi cần dùng/nộp riêng. Nhiều TC cùng lỗi dùng chung bug/ảnh khi có căn cứ. Phân biệt requirement với giả định/quy ước bổ sung.

AI gaps chỉ phân tích khi được giao, từ bản đầu/review có nguồn và kết quả thật. Không tạo lại mô hình/bản AI ban đầu để điền đủ report. Thiếu lịch sử hoặc chưa phát hiện gap thì ghi đúng phạm vi đó.

## Số liệu và kiểm tra cuối

- `executed = passed + failed`; `not_executed = blocked + not_run`; tổng là unique TC trong phạm vi. Nêu cách xử lý rerun, không đếm lượt chạy thành TC mới.
- Tách coverage thiết kế, coverage đã exercise và pass rate. Chỉ nhận item đã exercise khi TC thật sự tới điều kiện/bước đó; sequence thiếu bước chưa chứng minh trọn sequence.
- Report lấy số liệu từ nguồn chung; ảnh/link tồn tại, caption khớp actual. Metadata/index ảnh đặt trong report hoặc kết quả; không mặc định thêm file index/manifest.
- Kiểm tra bản Markdown đọc được: input/expected/actual/kết luận khớp nhau, giải thích ký hiệu, link đúng và ảnh cần thiết hiển thị. Không sinh thêm định dạng cho mọi summary.
- Ghi đúng phần chưa chạy/review/đăng Issues hoặc định dạng chưa có. Không tự ghi AI audit, commit/push, demo hay nộp bài để kết thúc một task execution/report.
