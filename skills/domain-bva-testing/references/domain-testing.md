# Mô-đun 1 — Domain Testing

Đọc khi phân tích miền và chọn test. Đề giao kỹ thuật; trình tự dưới đây là cách triển khai của bộ skill, cần đối chiếu slide. Nguồn học thuật và nguồn khảo sát được chỉ ra trong `research.md`.

## Từ đặc tả tới mô hình

1. **Rule:** trích điều kiện và kết quả đúng, có vị trí nguồn. “Tên sản phẩm tối đa 255” không trở thành max tên danh mục. Implementation có HTTP 500 không biến 500 thành expected của mọi input lỗi.
2. **Biến:** tên, kiểu, đơn vị, lớp đưa dữ liệu vào, giá trị biểu diễn được, giá trị hợp lệ nghiệp vụ và giá trị nominal. Trạng thái khóa/thời gian từ lúc khóa là biến mô hình khi outcome phụ thuộc lịch sử; mô tả sequence để đạt trạng thái đó.
3. **Miền:** chia theo hành vi/rủi ro có căn cứ; gồm miền hợp lệ và từng miền không hợp lệ có ý nghĩa. Viết predicate hoặc điều kiện rõ. Với partition có thứ tự, kiểm tra khoảng hở/chồng nhau. Với phân nhóm rủi ro có thể chồng nhau, công bố chúng là các nhóm theo từng khía cạnh, không nhận là partition toán học rời nhau.
4. **Ranh giới/ràng buộc:** phân biệt dấu `<`, `<=`, `=`, khoảng mở/đóng, tập thành viên và quan hệ liên biến. Không tự áp thứ tự nhỏ/lớn cho role, định dạng email hoặc danh mục trạng thái.
5. **Điểm:** chọn đại diện và giải thích bằng lỗi mục tiêu; giữ các biến khác nominal hợp lệ để điều kiện lỗi không bị che. Thử kết hợp khi requirement có tương tác thực và có thể quan sát riêng; không tự lấy toàn bộ tích Descartes hoặc đổi sang pairwise để thay nhiệm vụ được giao.
6. **Test:** hiện thực điểm thành dữ liệu có thể nhập, setup, bước và expected. Chỉ ra khi điều kiện không thể tới qua UI nhưng tới được qua API; đó là hai lớp kiểm tra khác nhau.
7. **Coverage:** kiểm tra mỗi mục tiêu miền/rule có TC, và TC đó có thực sự chạm được điều kiện. Test bị validation trước chặn không chứng minh đã kiểm tra rule phía sau.

## Các thành phần mô hình

Khi sinh TC nhanh, có thể gộp các thông tin này vào bảng TC và rationale. Tách thành các bảng riêng khi cần giải thích từng bước; không bắt buộc dựng một tài liệu đầy đủ cho mọi yêu cầu sinh test.

| Bảng | Trường hữu ích |
| --- | --- |
| Rules | ID, mô tả, nguồn, confirmed/assumption/unresolved |
| Variables | ID, kiểu/đơn vị, nominal, thứ tự nếu có, giới hạn biểu diễn, rule IDs |
| Domains | ID, biến, predicate/nhóm rủi ro, hợp lệ/không hợp lệ, expected, nguồn |
| Points | ID, domain/rule, dữ liệu, rationale, điều kiện biến khác, khả năng tiếp cận |

Nếu slide dùng ON/OFF/IN/OUT: chép định nghĩa từ slide vào method profile, chỉ ra điểm nằm trên/ngoài/trong miền theo các điều kiện cụ thể; với ranh giới nhiều chiều, giữ hoặc thay đổi các biến có chủ đích và kiểm tra mọi ràng buộc còn lại. Không tự đặt số điểm theo số chiều khi chưa xác minh quy tắc được dạy. Với input không có thứ tự, chọn đại diện theo rủi ro và đánh dấu BVA số là không áp dụng.

Domain và BVA có thể chọn trùng dữ liệu, nhưng phần Domain vẫn phải giải thích mô hình miền/cách lấy mẫu; phần BVA phải trình bày rõ phép suy ra các giá trị biên.

## Áp dụng EShop khi cần

- **FR-02:** tách email/tài khoản/mật khẩu và điều kiện bộ đếm/trạng thái/thời gian; không đưa ngưỡng mật khẩu đăng ký thành rule đăng nhập. Đếm lần sai theo đặc tả, không theo code sai.
- **FR-07:** cart rỗng/có hàng, sản phẩm mới/cùng ID, quantity và số học. Rule quantity từ FR-06 là dependency cần ghi; chưa có max thì không tự đặt max. Cart Web và cart API có thể không chung state.
- **FR-14:** thân requirement yêu cầu Thêm/Xem/Xóa, tiêu đề CRUD/API PUT là điểm cần đối chiếu. Max tên và tên duy nhất chưa được đặc tả thì không tự thêm.
- **Mobile registration:** áp quy tắc đăng ký từ FR-01 thông qua FR-20; xác định trường/luồng bằng source/UI, không sửa màn hình cho giống test. Mỗi input password chỉ làm sai điều kiện mục tiêu khi đang kiểm tra riêng điều kiện đó.

Các gợi ý này là cách đọc requirement, không phải test case/kết quả chạy sẵn. Phạm vi hiện hành do người làm cung cấp quyết định.
