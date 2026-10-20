# Các phiên bản artifact để đối chiếu

Các bản đã có trong lịch sử Git được dẫn tới đúng commit, gồm cả khi nội dung hiện tại đã thay đổi. Thư mục `history/` giữ output ban đầu chưa từng commit và phần thay đổi cần đọc cùng audit. Nội dung prompt/phản hồi gốc nằm trong [Prompt Log](23120410_HW02_PromptLog.md); nhận xét ở [AI Audit Report](ai-audit.md).

## A-00 — Quy trình và skill AI log

Output ban đầu và bản sửa được trích nguyên văn trong audit, mục 3.1–3.4. Skill kỹ thuật đã có tại [commit 6fb3d52](https://github.com/tranquocvy/eshop-sut/tree/6fb3d52/skills/course-ai-log). Kiểm tra helper trong [output công cụ](verification/ai-log-helper.txt).

## A-01 — Skill Domain Testing/BVA

- [Bản gộp trước khi tách — 58481f4](https://github.com/tranquocvy/eshop-sut/tree/58481f466d78ed0f5801bfbc64a676006d2beac2/skills/domain-bva-testing).
- [Bản chỉ thiết kế — ddcacdf](https://github.com/tranquocvy/eshop-sut/tree/ddcacdf72a041aca8fb37325d3c26b4e6290840e/skills/domain-bva-testing).
- Đã đối chiếu toàn bộ file của hai snapshot cũ với các commit tương ứng; chỉ khác xuống dòng CRLF/LF nếu có.

## A-02 — Skill execution/reporting

- [Bản có evidence/JPG — 8018b73](https://github.com/tranquocvy/eshop-sut/tree/8018b73e9e0d9066efdb1ffe3512303e033a6cb4/skills/test-execution-reporting).
- [Bản thu gọn — cbf1ba9](https://github.com/tranquocvy/eshop-sut/tree/cbf1ba939c9a0b41281ccc1f053096ee60035897/skills/test-execution-reporting).
- [Thay đổi giữa hai mốc](https://github.com/tranquocvy/eshop-sut/compare/8018b73e9e0d9066efdb1ffe3512303e033a6cb4...cbf1ba939c9a0b41281ccc1f053096ee60035897); [kết quả kiểm tra helper](verification/design-execution-helpers.txt).

- Bổ sung GitHub/evidence theo P-027/P-028/P-030, đã lưu tại **commit local `e1fe254040122e449ff184412853f9a8a0d72059`**: [SKILL.md](../../../skills/test-execution-reporting/SKILL.md), [quy trình GitHub](../../../skills/test-execution-reporting/references/execution-and-bugs.md), [report contract](../../../skills/test-execution-reporting/references/report-contract.md), [evidence](../../../skills/test-execution-reporting/references/evidence.md), [template](../../../skills/test-execution-reporting/assets/feature-report.template.md). Bản trước thay đổi nằm tại commit `6631d92`; không sao chép thêm toàn bộ skill vào hồ sơ AI. P-030 chỉ sửa hướng dẫn, chưa áp dụng lại lên report.

## A-03 — Thiết kế Mobile Account Registration

- AI đầu v0.1, 46 TC: [design nguyên văn](history/mobile-registration-v0.1-design.md.txt), [TC nguyên văn](history/mobile-registration-v0.1-test-cases.md.txt).
- Bản v0.3 đã review, 54 TC: [design](https://github.com/tranquocvy/eshop-sut/blob/5ca63e1dadc0c69cd4a52b892f2c5a1dc1ff5d59/tests/hw02/mobile-registration/design.md), [TC](https://github.com/tranquocvy/eshop-sut/blob/5ca63e1dadc0c69cd4a52b892f2c5a1dc1ff5d59/tests/hw02/mobile-registration/test-cases.md).
- [Diff v0.1 → v0.3](history/mobile-design-changes.diff).

## A-04 — Code test Mobile Account Registration

[Bộ implementation tại b8b1d2b](https://github.com/tranquocvy/eshop-sut/tree/b8b1d2b18203a0ebf0a24352890da1e80fc0d5fc/tests/hw02/mobile-registration) giữ `IMPLEMENTATION.md`, catalogue, thao tác native và runner nguyên bản. Đánh giá implementation gắn với mốc này; thay đổi execution sau đó được ghi riêng ở A-05.

## A-05 — Execution và report Mobile Registration

- [Kết quả run đầu chưa từng commit](history/mobile-initial-results.json): 18 pass, 9 fail, một blocked; TC29 dở dang.
- [Report](https://github.com/tranquocvy/eshop-sut/blob/62e34ecbcce65a8c803625ca8d210dfd9176dbbe/tests/hw02/mobile-registration/report.md), [results](https://github.com/tranquocvy/eshop-sut/blob/62e34ecbcce65a8c803625ca8d210dfd9176dbbe/tests/hw02/mobile-registration/results.json) và [ảnh](https://github.com/tranquocvy/eshop-sut/tree/62e34ecbcce65a8c803625ca8d210dfd9176dbbe/tests/hw02/mobile-registration/images) tại `62e34ec`: 35 pass, 15 fail, bốn blocked.
- [Thay đổi từ implementation tới harness đã sửa](https://github.com/tranquocvy/eshop-sut/compare/b8b1d2b18203a0ebf0a24352890da1e80fc0d5fc...b1c122bd0f00bc982d19093abad0776f0434d04e).

- Bản trước bổ sung Issues (`62e34ec`) được đánh giá **INCOMPLETE** về phần hồ sơ GitHub theo §6.4/§14, dù kết quả execution vẫn được giữ. P-029 đã bổ sung **8 issue, 14 ảnh lỗi hiển thị và 9 JPG trang/danh sách issue**, không chạy lại SUT.
- Mốc bổ sung file đã commit local `e1fe254040122e449ff184412853f9a8a0d72059`: [report](../../../tests/hw02/mobile-registration/report.md), [results/log thao tác](../../../tests/hw02/mobile-registration/results.json), [ảnh tổng quan](../../../tests/hw02/mobile-registration/images/MR-GitHub-issues.jpg). Tám ảnh riêng có tên `MR-BUG01-issue.jpg` đến `MR-BUG08-issue.jpg`, được dẫn trong từng bug của report. File mốc này còn có các sửa report sau bốn lượt được chọn; không gán những sửa đó cho P-029/P-030.
- Đăng trên tracker: [#1](https://github.com/tranquocvy/eshop-sut/issues/1), [#2](https://github.com/tranquocvy/eshop-sut/issues/2), [#3](https://github.com/tranquocvy/eshop-sut/issues/3), [#4](https://github.com/tranquocvy/eshop-sut/issues/4), [#5](https://github.com/tranquocvy/eshop-sut/issues/5), [#6](https://github.com/tranquocvy/eshop-sut/issues/6), [#7](https://github.com/tranquocvy/eshop-sut/issues/7), [#8](https://github.com/tranquocvy/eshop-sut/issues/8). MR-BUG05–08 ghi rõ sai khác S7. Dùng link tương đối cho các file commit local, không mặc định commit đã được push lên GitHub.

## A-06 — Thiết kế Category Management

- AI đầu v0.1, 24 TC: [design nguyên văn](history/category-v0.1-design.md.txt), [TC nguyên văn](history/category-v0.1-test-cases.md.txt).
- Bản v0.2 đã review, 33 TC: [design](https://github.com/tranquocvy/eshop-sut/blob/b84417b841f7a1bd5d20386132a0f333d7487fb1/tests/hw02/fr14-categories/design.md), [TC](https://github.com/tranquocvy/eshop-sut/blob/b84417b841f7a1bd5d20386132a0f333d7487fb1/tests/hw02/fr14-categories/test-cases.md).
- [Diff v0.1 → v0.2](history/category-design-changes.diff). Toàn bộ TC Category vẫn Not Run.

Các file `.md.txt` giữ nguyên byte của output Markdown ban đầu; phần mở rộng giúp đọc nguyên văn các đường dẫn lịch sử trong output. Bản sửa được dẫn tới Git đúng phiên bản. Các file diff giữ nguyên bản đã lưu trước khi tái cấu trúc. Dữ liệu đồng bộ, hash và metadata được giữ local trong `_data/`.
