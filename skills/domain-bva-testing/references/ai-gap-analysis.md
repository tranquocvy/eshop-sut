# Mô-đun 3 — AI gap analysis

## Giữ diễn biến để phân tích thật

Trước review/execution, giữ `ai-initial-design.md` cho phiên bản AI ban đầu (rule/domain/boundary/TC) và các nguồn tạo ra nó. Khi người dùng sửa, giữ diff hoặc revision cụ thể. Snapshot này không thay log prompt/output của từng tương tác.

Nếu đã có version ban đầu, tiếp tục lịch sử đang có; không tạo lại một bản “AI ban đầu” từ bản cuối. Nếu không còn bản gốc hoặc người học chưa review, báo phần thiếu; không dựng trải nghiệm để đủ nội dung critique.

## Đối chiếu

| Phần kiểm tra | Câu hỏi |
| --- | --- |
| Requirement | Rule nào có nguồn nhưng chưa được mô hình hóa? Có max/regex/expected tự bịa không? |
| Domain | Miền không hợp lệ, trạng thái, đơn vị hoặc quan hệ nào bị bỏ qua? Test có bị điều kiện khác chặn trước không? |
| BVA | Dấu bằng/độ phân giải/coverage item đúng chưa? Có nhầm một bộ ba điểm với biến thể khác không? |
| Execution | Script có chạy đúng lớp/phiên bản? Có lấy API để nhận đã test native, hoặc coi screenshot source là ảnh bug runtime không? |
| Reporting | Đã giữ failed/blocked? Bug có oracle, bước tái hiện và evidence không? |

Mỗi gap có ID, phiên bản/tương tác ban đầu, nội dung AI đã làm hoặc bỏ sót, nguồn phát hiện, tác động, sửa/bổ sung, ai thực hiện và kết quả kiểm tra lại. Phân biệt **case gap**, **oracle error**, **model gap**, **execution/evidence gap**; các nhãn này chỉ để phân tích, không thay verdict AI-02.

## Giải thích nguyên nhân

Đánh giá theo bằng chứng: prompt thiếu nguồn/ràng buộc; model bỏ qua rule đã có; đặc tả chưa rõ; tương tác nhiều biến; giới hạn công cụ/môi trường; hoặc nguyên nhân chưa xác định. Một lời giải thích hợp lý vẫn có thể là giả thuyết: ghi mức chắc chắn và phép kiểm tra đã làm, không tự biết nguyên nhân nội bộ của mô hình.

AI đề xuất lại một test sau review không chứng minh “sinh viên tự viết test”. Yêu cầu AI sửa khác với tự sửa trực tiếp. Một bug đã được AI chỉ ra trong lúc đọc source không được kể lại là bug AI bỏ sót; một case bị bỏ sót chỉ gọi đã tìm được bug sau khi có bằng chứng chạy hoặc xác minh phù hợp.

Nếu đối chiếu chưa phát hiện gap, ghi phạm vi đã review và kết quả đó; không tạo một lỗi giả. Đề yêu cầu báo những trường hợp bỏ sót nếu có, không buộc phải bịa số lỗi AI.

Đầu ra: bảng gap analysis có nguồn và các thay đổi tương ứng; summary feature ngắn. AI Critique 200–300 từ của bài có thể dùng dữ liệu này khi được giao, nhưng không tự nhận tác giả/human oversight chưa có thật.
