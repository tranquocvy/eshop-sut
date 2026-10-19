# Trích xuất và đồng bộ Prompt Log

Helper `scripts/sync_prompt_log.py` nhận dữ liệu đã trích từ hội thoại thật, gộp chống trùng và trình bày theo cặp prompt/output. Nó không tìm chat, viết audit hay tự chạy sau mọi tin nhắn.

## Nội dung cần giữ

- Giữ lời gốc của user và các phản hồi AI hiển thị, đúng thứ tự, gồm tiến độ và kết quả. Loại system/developer instructions, suy luận nội bộ, secrets và ambient context khỏi bộ xuất. Tool output là evidence của thao tác; không gán nó thành lời assistant.
- Dùng timestamp metadata có timezone; không lấy giờ export làm giờ message cũ. Thiếu thì để null và ghi “Chưa có thời gian từ nguồn”. Công cụ/model thuộc lần dùng thực tế.
- Giữ `id`, `sequence`, `reply_to` ổn định khi nguồn có. Nếu thiếu ID, tạo khóa ổn định cho chính record đã trích, không dùng timestamp hiện tại. ID/hash/dòng nguồn nằm trong `_data`, không cần hiện trong bản đọc.
- `coverage` đo đủ **lượt tương tác** trong phạm vi. Đủ lượt nhưng che một phần nội dung vẫn có thể là `complete_for_scope`; record đó có `verbatim: false` và ghi chú lý do che. Thiếu lượt thì `partial` và nêu khoảng thiếu. Không bỏ lời gốc bị sai hoặc lượt sửa để log trông đẹp hơn.
- `note` lưu nguồn kỹ thuật nội bộ; `display_note` dùng cho ghi chú ngắn thực sự cần người đọc biết, nhất là nội dung che. Không đưa đường dẫn/nội dung skill riêng vào report; lưu snapshot phù hợp của artifact kỹ thuật được giao để nộp.

## Input UTF-8

```json
{
  "assignment": "HW03",
  "utc_offset": "+07:00",
  "source_id": "session-task-id-on-dinh",
  "scope": "Task được giao ghi log",
  "source_kind": "transcript-export",
  "coverage": "complete_for_scope",
  "tool": "OpenAI Codex",
  "messages": [
    {
      "id": "user-message-id",
      "sequence": 1,
      "role": "user",
      "text": "Prompt gốc từ nguồn",
      "timestamp": "2026-10-20T03:00:00Z"
    },
    {
      "id": "assistant-message-id",
      "sequence": 2,
      "role": "assistant",
      "text": "Output gốc từ nguồn",
      "timestamp": "2026-10-20T03:01:00Z",
      "reply_to": "user-message-id",
      "channel": "final"
    }
  ]
}
```

Đây là schema minh họa, không phải tương tác để chép vào bài. `messages` cần `id`, `sequence`, `role`, `text`. Các trường tùy chọn: `timestamp`, `tool`, `model`, `channel`, `reply_to`, `note`, `display_note`, `verbatim` (mặc định true). Nguồn có thể thêm `coverage_note` và `display_note`; chỉ ghi chú hiển thị cần thiết mới xuất ra Markdown.

```powershell
python '<skill-folder>/scripts/sync_prompt_log.py' --input '<normalized-source.json>' --output-dir '<thu-muc-AI-cua-bai>' --assignment 'HW03'
```

`--assignment` có thể thay bằng trường input. Mã bài chỉ là nhãn, không cố định HW02. Múi giờ hiển thị mặc định +07:00; dùng `--utc-offset` để chọn múi giờ phù hợp, không thay timestamp nguồn. `--log-name` hỗ trợ tên file hiện hành, ví dụ `student_HW03_PromptLog.md`; chỉ dùng tên file Markdown trong output-dir. Nếu chưa có mã bài, tiêu đề là “Prompt Log”. Không dùng chung output-dir cho hai bài khác nhau.

## Bản đọc và dữ liệu hỗ trợ

```markdown
# HW03 Prompt Log

## P-000

- Timestamp: 10:00:00 20/10/2026 (UTC+07:00)
- Công cụ: OpenAI Codex

### Prompt

... nguyên văn ...

### Output

... các phản hồi nguyên văn, có thời gian ...
```

Mỗi prompt có mã P ổn định. Có nhiều phản hồi thì giữ từng phần theo thứ tự và thời gian. `reply_to` khác prompt hiện tại được ghi rõ là phản hồi bổ sung cho prompt tương ứng; output không có prompt trong nguồn được ghi riêng, không tạo prompt giả. Anchor message cũ vẫn giữ để các link đã có không hỏng.

Helper tạo/cập nhật file Markdown và `_data/interactions.json`. Giữ dữ liệu hỗ trợ local để chống trùng và đối chiếu; chỉ đưa vào bộ nộp khi cần. Sửa cùng ID thành lời khác, trùng sequence hay ghi đè log đã sửa tay đều bị từ chối trước khi ghi. Khi helper từ chối, giữ bản người dùng và xử lý xung đột dựa trên nguồn, không xóa hash/file để ép chạy.

## Dùng tiếp dữ liệu helper cũ

Đọc được dữ liệu helper schema v1; lần chạy hợp lệ chuyển sang schema v2, giữ nguyên messages và anchor, đổi cách trình bày. Không tự sửa bản log thật chỉ vì đang cập nhật skill. Khi được giao định dạng lại log cũ, chạy trên **bản sao tạm** để xem trước, đối chiếu nội dung và bảo toàn chỉnh sửa của người dùng rồi mới áp dụng. Một file thủ công chưa có state không nên ép import: trích xuất/đối chiếu nguồn trước hoặc cập nhật phần Markdown được giao một cách bảo toàn.

## Kiểm tra helper

Chạy bằng Python 3.10 trở lên, không cần dependency ngoài thư viện chuẩn:

```powershell
python -B scripts/test_sync_prompt_log.py
```

Các kiểm tra dùng dữ liệu giả lập và thư mục tạm; không đọc lịch sử chat hoặc sửa báo cáo thật. Bộ skill nhận transcript và biểu mẫu từ người dùng, không kèm dữ liệu sinh viên hay tài liệu môn riêng tư.
