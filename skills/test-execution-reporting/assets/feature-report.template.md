# Báo cáo kiểm thử — <feature>

> Khung gợi ý; chỉ dùng phần thuộc task. Lấy số liệu/actual từ kết quả thật, không sinh thêm bộ file để điền đủ mẫu.

## 1. Phạm vi và môi trường

Bộ TC/thiết kế và phiên bản; run ID, thời gian/múi giờ, SUT/test revision/diff, layer, môi trường và fixture. Người/công cụ chạy; review có thật. Dẫn thiết kế Domain/BVA và nguồn expected thay vì chép lại toàn bộ.

## 2. Kết quả chung

Nguồn kết quả; cách chọn run khi có rerun. Unique TC designed/executed/passed/failed/blocked/not run; coverage đã exercise nếu thuộc task. Không dùng pass rate thay coverage hoặc cộng trùng TC có nhiều nhãn.

Nêu dữ liệu mặc định và ý nghĩa ký hiệu một lần. Đạt (passed), Không đạt (failed), Bị chặn (blocked), Chưa chạy (not_run); ca bị ngắt ghi rõ dở dang. Input dưới đây là dữ liệu dự kiến theo TC; actual mới phản ánh phần đã thực hiện.

| TC có link về thiết kế | Nội dung kiểm tra / input chính | Expected | Actual | Kết luận / bug |
| --- | --- | --- | --- | --- |

Mỗi hàng phải đủ để đối chiếu expected với actual và hiểu kết luận, không cần mở JSON. Input chính là phần khác dữ liệu mặc định; expected tóm tắt đúng bản đã duyệt, nguồn chi tiết ở link TC. Actual ngắn nhưng cụ thể; observation chi tiết/sequence có thể ở nguồn chung. Giữ expected cho ca chưa chạy, nhưng không viết actual giả. Có thể chia bảng theo nhóm chức năng; không bắt screenshot hoặc thư mục riêng cho mỗi TC. Link bug tới detail/ảnh bên dưới.

## 3. Bug và evidence cần thiết

Mỗi bug: oracle, TC/run, precondition/input, steps, expected/actual, mức ảnh hưởng, tần suất thực đã thử và trạng thái/URL issue. Phân biệt requirement với quy ước bổ sung. Dùng lại ảnh chung cho TC cùng bug.

Nhúng JPG và caption trạng thái/capture time; thêm ảnh input khi cần hiểu lỗi. Metadata đặt ở đây hoặc nguồn chung, không cần index mặc định. Phân biệt ảnh SUT và ảnh trang Issues.

## 4. AI gap analysis — khi thuộc phạm vi

Bản AI đầu/review có nguồn, thiếu/sai cụ thể, nguồn phát hiện, nguyên nhân có căn cứ hoặc giả thuyết, người sửa và kết quả kiểm tra lại. Không bịa gap hoặc biến mọi bổ sung sau chốt policy thành AI bỏ sót.

## 5. Tổng kết

Kết quả chính, giới hạn/blocked và việc còn lại trong task. Kiểm tra số liệu, link và ảnh nhúng trong Markdown. Chưa đăng issue/review thì ghi đúng trạng thái.
