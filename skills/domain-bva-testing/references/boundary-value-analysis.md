# Mô-đun 2 — Boundary Value Analysis

Phải công bố biến thể đang áp dụng. BVA cần miền có thứ tự, biên có nguồn và giá trị lân cận được xác định theo cách dữ liệu biểu diễn. Không dùng `±1` với mọi số tiền, thời gian hoặc chuỗi. Slide môn được ưu tiên để xác định cách triển khai bài; nguồn ISTQB dùng để kiểm tra chéo, không tự nhận là slide.

## Inventory trước khi chọn dữ liệu

Mỗi boundary ghi: ID, biến, rule/source, hai miền tiếp giáp, điều kiện tại dấu bằng, đơn vị, bước nhỏ nhất có ý nghĩa và các biến nominal. Với string length phải nói đang đếm ký tự, code point, code unit hay byte theo nguồn; không tự lấy cách đếm của implementation làm quy tắc nghiệp vụ.

Input rỗng/thiếu/null/sai kiểu là các miền cần kiểm tra nhưng không phải tất cả đều là điểm biên số. Email không có max được đặc tả thì không tự tạo biên độ dài 254/255. ID đang tồn tại là tập thành viên, không mặc định là một khoảng liên tục từ 1 đến max ID.

## Hai profile của helper

Theo ISTQB CTFL v4.0.1 §4.2.2, mỗi boundary value có các coverage items khác nhau trong 2-value và 3-value. Khi đã xác định hai partition rời rạc liền kề, ví dụ requirement minh họa `x >= 18` trên số nguyên:

| Profile | Boundary values ở hai phía | Hợp các coverage items |
| --- | --- | --- |
| `istqb-2` | 17 và 18 | 17, 18 |
| `istqb-3` | 17 và 18, mỗi giá trị cùng hai hàng xóm | 16, 17, 18, 19 |

Vì vậy, một bộ “17/18/19” không tự đồng nghĩa đủ coverage 3-value theo profile này. Một số bài giảng dùng cách chọn quanh một ngưỡng hay quy ước khác: ghi tên/nguồn thực, giữ cách dạy và không đổi nhãn tùy tiện. Hai kỹ thuật có thể cùng dùng một giá trị nhưng coverage item phải được truy vết đúng.

Với bước tiền minh họa `0.01`, cặp liền kề `9.99 / 10.00` cho 3-value sẽ thêm `9.98 / 10.01`, không cộng/trừ một đơn vị tiền. Đây là ví dụ tính toán, không phải quy tắc tiền của EShop.

## Dùng helper

Xem `assets/boundary-input.example.json` để biết schema. File ví dụ dùng bài toán parcel count giả lập, không phải dữ liệu/bằng chứng HW02. Chạy từ thư mục skill, bằng PowerShell:

```powershell
python .\scripts\boundary_points.py --input .\assets\boundary-input.example.json --variant istqb-3
```

Muốn lưu JSON thì thêm `--output <duong-dan-output.json>` với đường dẫn thật. Không có dependency ngoài Python chuẩn. Helper nhận các cặp boundary values đã được analyst xác định, dùng Decimal, kiểm tra tính liền kề/bước/đơn vị và sinh các điểm kèm provenance. Nó không đọc spec, không tạo expected và không chứng minh tất cả biên của feature đã được đưa vào input.

`min_value`/`max_value` chỉ là giới hạn biểu diễn có nguồn, không tự suy ra max nghiệp vụ. Các điểm lân cận không thể biểu diễn sẽ được báo riêng; không chạy giá trị “độ dài âm” rồi coi đó là test nhập được. Giới hạn vật lý/kiểu dữ liệu cần được xem xét trong inventory riêng, không bị helper tự coi là biên nghiệp vụ đã bao phủ.

## Từ điểm biên tới test và coverage

- Hiện thực mỗi điểm bằng dữ liệu cụ thể, giữ các rule khác hợp lệ và setup đủ để tới đúng nhánh.
- Ghi expected của cả hai phía từ requirement, không suy ra chỉ từ điểm được helper tạo.
- Với thời gian: thiết kế rõ mốc t0, đồng hồ/đơn vị, δ, sai số và cách quan sát để người chạy thực hiện được. Một bước `sleep 30` không tự bảo đảm request đến đúng mốc 30 giây; không chạy SUT để kiểm tra thời điểm trong lượt sinh TC.
- Coverage thiết kế = số items có TC / tổng items đã xác định. Đây là ánh xạ từ mô hình sang TC; không dùng nó làm bằng chứng đã thực thi các điểm đó.
- Không gọi tỷ lệ trên inventory tự chọn là “100% mọi biên của phần mềm”; nêu nguồn, phạm vi và mục chưa biết.

Đầu ra BVA có TC với giá trị biên, expected có nguồn và lý do chọn điểm. Khi task yêu cầu giải thích từng bước, thêm bảng boundary/coverage items và ngoại lệ. JSON điểm biên chỉ hỗ trợ tính dữ liệu, không thay bộ TC hoặc tự tạo expected.
