"""Render Markdown from the single results source. Does not execute SUT."""
from collections import Counter
from datetime import datetime, timedelta, timezone
import json
from pathlib import Path

F=Path(__file__).resolve().parents[1]
def cell(s): return str(s).replace('|','\\|').replace('\n',' ').replace('<','&lt;')
def chosen(d,c): return next(r for r in reversed(c['results']) if r['run_id']==d['selected_results'][c['id']])
def main():
    path=F/'results.json'; d=json.loads(path.read_text(encoding='utf-8'))
    actual={
    'W01':'UI login thành công; token lưu client; mở hồ sơ đúng test@eshop.com, GET me có Bearer.',
    'W02':'Admin login thành công, client có token.',
    'W03':'Một submit U/Z: HTTP401, counter 0→2, chưa khóa; không token.',
    'W06':'U/Z và X/P đều hiển thị cùng lỗi chung; không token.',
    'W07':'plainaddress vẫn gửi POST →401; input type=text, validity=true.',
    'W08':'a@ vẫn gửi POST →401; input type=text, validity=true.',
    'W09':'Email rỗng bị required chặn; 0 request, counter=0.',
    'W10':'Password rỗng bị required chặn; 0 request, counter=0.',
    'W11':'FL trực tiếp n=3, còn khoảng 20s: đúng P bị từ chối; state không đổi.',
    'W17':'FL(U) trực tiếp: V login được; U giữ nguyên khóa.',
    'W18':'FL(U) trực tiếp: reload và context trình duyệt khác đều không login được U.',
    'W19':'Fixture password Ab1! login thành công, client có token.',
    'A01':'200/token/user; GET me bằng Bearer trả 200 đúng U.',
    'A02':'POST U/Z →401, counter 0→2, chưa khóa.',
    'A05':'U/Z và X/P đều401 cùng body Invalid email or password.',
    'A06':'FL trực tiếp, đúng P→403; counter/deadline không đổi.',
    'A11':'FL trực tiếp hết 30s; đợi thật31s: sai đầu counter3→5 và tái khóa180s, sai tiếp và đúng P đều403.',
    'A12':'Thiếu email→401, không token/500, counter=0.',
    'A13':'Thiếu password→401 nhưng counter0→2.',
    'A14':'Email rỗng→401; counter=0.',
    'A15':'Password rỗng→401 nhưng counter0→2.',
    'A16':'Email null→401, counter=0.',
    'A17':'Password null→401 nhưng counter0→2.',
    'A18':'Email array→401, không token/500, counter=0.',
    'A19':'Password object→401 nhưng counter0→2.',
    'A21':'Client HTTP mới: U đang khóa→403; V đúng→200; U vẫn khóa.',
    'A22':'Password đổi case bị401; counter0→2 thay vì1.',
    'A23':'Password thêm space bị401; counter0→2 thay vì1.',
    'A24':'SQL payload→401 lỗi chung, không bypass/SQL stack.',
    'A25':'200; user chứa password=Test1234! và reset_token=FR02_PRIVATE.'}
    if not d['bugs']:
        sup=d['supplementary'][0]
        imgs={i['bug']:i for i in sup['images']}
        def bug(n,title,kind,oracle,cases,steps,expected,observed,frequency,priority):
            bid=f'FR02-BUG{n:02}'; img=imgs.get(bid)
            if n==3:
                case=next(c for c in d['cases'] if c['id']=='FR02-W07'); img=chosen(d,case)['images'][0]
            return dict(id=bid,title=title,kind=kind,oracle=oracle,cases=cases,steps=steps,expected=expected,actual=observed,frequency=frequency,
                        priority=priority,symptom_image=img,issue=None)
        d['bugs']=[
        bug(1,'Counter tăng 2 mỗi lần sai, khóa sau hai lần thay vì ba','confirmed','S1 FR-02 / R02,R03',['FR02-W03','FR02-A02','FR02-A22','FR02-A23'],
            'F0 U; POST U/Wrong123! hai lần nối tiếp; sau đó U/Test1234!. Web cũng tái hiện lần sai đầu qua submit.',
            'Counter0→1→2; sau hai sai chưa khóa, đúng P được login.',
            'Counter0→2→4, locked_until được đặt ngay lần sai thứ2; đúng P→403.',
            'Counter +2: W03 RUN02/RUN03, A02 RUN03 và VERIFY01; early lock: W16/A20 RUN03 và VERIFY01. Không suy tỷ lệ cho môi trường khác.','P1: khóa nhầm tài khoản sớm'),
        bug(2,'Thời hạn khóa được đặt khoảng 180 giây, vẫn từ chối sau hơn31 giây','confirmed','S1 FR-02 / R04',[],
            'F0; gửi hai sai để tái hiện khóa thực tế; ghi bracket request kích hoạt và DB deadline; đợi31s thật rồi gửi đúng P.',
            'Khóa chỉ30s kể từ khi kích hoạt; sau31s đúng P được đăng nhập.',
            'VERIFY01: deadline cách request kích hoạt khoảng180s; đúng P sau31s vẫn403. Không credit các điểm ±1ms blocked.',
            '1/1 sequence VERIFY01 đo thời lượng; timestamp/bracket trong supplementary.','P1: người dùng bị khóa lâu hơn yêu cầu'),
        bug(3,'Email Web dùng type=text, email sai vẫn gửi login request','confirmed','S1 FR-02 / R07',['FR02-W07','FR02-W08'],
            'Mở /login; nhập plainaddress hoặc a@ cùng Test1234!, bấm Sign In; kiểm tra DOM và network.',
            'type=email, HTML5 chặn email sai trước khi gửi login request.',
            'type=text, validity=true; cả hai input phát POST /api/login, server401.',
            '2/2 input đã thử trong RUN03; không quy thành tỷ lệ mọi email.','P2: thiếu validation HTML5 đã đặc tả'),
        bug(4,'[A02] Password thiếu/rỗng/null/object vẫn làm tăng counter tài khoản','assumption','A02 đề xuất; API §1.2 không chốt validation/counter invalid payload',['FR02-A13','FR02-A15','FR02-A17','FR02-A19'],
            'Mỗi payload từ F0 riêng: email U và password absent, chuỗi rỗng, null, hoặc object {value:Test1234!}; POST /api/login.',
            'Theo A02: từ chối có kiểm soát, counter không đổi; chưa phải requirement xác nhận.',
            'Đều401 nhưng counter0→2. Bản thiếu password được tái hiện trong VERIFY01.',
            '4/4 biến thể RUN03; biến thể absent thêm1 lượt VERIFY01.','P2 đề xuất: invalid request có thể gây khóa; cần chốt policy'),
        bug(5,'[A04] Login response lộ password và reset_token trong user','assumption','A04 đề xuất; S2 cho user nhưng chưa mô tả field nhạy cảm',['FR02-A25'],
            'F0; đặt marker reset_token=FR02_PRIVATE qua fixture; POST U/Test1234!, inspect JSON user.',
            'Theo A04: token/user cần thiết, không password/reset_token.',
            '200 trả user.password=Test1234! và user.reset_token=FR02_PRIVATE; JWT đã che trong evidence.',
            '2/2 lượt A25 RUN03 và VERIFY01.','P1 đề xuất: lộ credential/reset marker; finding bảo mật theo A04'),
        bug(6,'[A01] Counter của khóa đã hết được dùng lại, lần sai đầu tái khóa','assumption','A01 đề xuất reset chuỗi sau hết khóa; S1 chưa quy định reset storage',['FR02-A11'],
            'FL trực tiếp n=3, deadline=t0+30s; đợi31s thật; gửi U/Z hai lần rồi U/P. VERIFY01 cô lập lại với FL đã hết1s.',
            'Theo A01: lần sai đầu chuỗi mới n=1, lần2 n=2 chưa khóa; đúng P thành công.',
            'Sai đầu dùng n=3 cũ thành5 và khóa180s; hai request sau403. Increment+2 là BUG01; việc dùng counter cũ là finding riêng.',
            'A11 RUN03 với wait31s và VERIFY01 expired fixture; 2 lượt.','P2 đề xuất: tái khóa sau expiry; cần chốt policy')]
    path.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8')
    chosen_results=[chosen(d,c) for c in d['cases']]; totals=Counter(r['status'] for r in chosen_results)
    review=d.get('student_review')
    review_text=('Vỹ đã kiểm tra và xác nhận report lúc '+datetime.fromisoformat(review['confirmed_at'].replace('Z','+00:00')).astimezone(timezone(timedelta(hours=7))).strftime('%H:%M:%S ngày %d/%m/%Y')+' (UTC+7). Việc review report không có nghĩa sinh viên tự chạy toàn bộ suite.') if review else 'Chưa có xác nhận Vỹ review kết quả chạy.'
    text=['# T05 — FR-02: Execution và report','',
    'Bộ thiết kế v0.1 đã được Vỹ duyệt tại `4bb5158`. Dẫn [design.md](design.md) và [test-cases.md](test-cases.md); giữ nguyên ID/input/expected. Report này ghi execution mới, không sửa trạng thái lịch sử “Not Run” trong bản thiết kế đã duyệt. '+review_text,'',
    f'**45 unique TC: {totals["passed"]} passed, {totals["failed"]} failed, {totals["blocked"]} blocked, 0 not_run.** Executed = passed+failed = {totals["passed"]+totals["failed"]}; chưa thực thi được target = {totals["blocked"]}. Pass rate trên executed = {totals["passed"]/(totals["passed"]+totals["failed"]):.0%}. Không đếm request/substep, retry, supplementary hay hai nhãn Domain+BVA thành TC mới.','',
    '## Môi trường và lịch sử run','',
    'Windows; Web source nguyên bản tại localhost:5173. Backend cổng3000 của T03/T04 đã dừng: copy server.js/database.js không đổi sang `HW02/.runtime/T05-execution-20261020/backend`, khởi động với database T05 mới. Không import/restart trên database cũ, không sửa logic SUT. PID lúc khởi động27228. Seed U/V đúng theo README; fixture short password tạo trực tiếp, X xác nhận vắng. Reset chỉ counter/lock/reset_token U/V giữa TC. FL trực tiếp ghi riêng trong entry.','',
    'Nguồn kết quả duy nhất: [results.json](results.json), `cases[].results[]`, `runs[]`, `supplementary[]`, `bugs[]`. Summary chọn entry theo `selected_results[id]`; RUN01/RUN02 giữ nguyên để audit, không cộng vào số TC. Clock evidence ghi UTC; thời gian người đọc UTC+7.','',
    '| Run | Thời gian UTC+7 | Nội dung |','| --- | --- | --- |']
    def local(s): return datetime.fromisoformat(s).astimezone(timezone(timedelta(hours=7))).isoformat(timespec='seconds')
    for r in d['runs']:
        note={'FR02-RUN01':'Smoke dừng W01: locator tên Hồ sơ không tồn tại (UI dùng link Chào,…); không phải bug SUT.',
              'FR02-RUN02':'W01 passed, W03 failed lưu xong; dừng do stdout cp1252 không in được →; không mất entry.',
              'FR02-RUN03':'Chạy toàn45TC sau sửa locator và stdout UTF-8; Chromium '+r['browser']+'.'}[r['id']]
        text.append(f'| {r["id"]} | {local(r["started_at"])} | {note} |')
    for r in d['supplementary']: text.append(f'| {r["id"]} | {local(r["started_at"])} | Repro thật bằng API client harness; đo khoảng180s và request sau31s; không thêm TC/credit BVA. |')
    text += ['', 'Run lưu revision, hash design/TC/runner, DB và browser version. Thời gian kết thúc RUN01/RUN02 thiếu vì dừng harness; không tự dựng lại. Runner hiện giữ history và dừng ngay khi gặp lỗi harness bất ngờ.','',
    '| Lớp | Tổng | Passed | Failed | Blocked | Not run |','| --- | --- | --- | --- | --- | --- |']
    for layer, prefix in [('Web','FR02-W'),('API','FR02-A')]:
        counts=Counter(chosen(d,c)['status'] for c in d['cases'] if c['id'].startswith(prefix))
        text.append(f'| {layer} | {sum(counts.values())} | {counts["passed"]} | {counts["failed"]} | {counts["blocked"]} | 0 |')
    bounds=next(o['seconds_bounds'] for o in d['supplementary'][0]['observations'] if o['step']=='duration bounds from triggering request and stored deadline')
    elapsed=next(o['seconds_bounds'] for o in d['supplementary'][0]['observations'] if o['step']=='elapsed since trigger bracket')
    text += ['',f'15 blocked gồm9ca bị precondition/sequence SUT chặn và6ca thiếu clock control. VERIFY01: khoảng thời hạn deadline−request kích hoạt = {bounds[0]:.3f}–{bounds[1]:.3f}s; request đúng P sau {elapsed[0]:.3f}–{elapsed[1]:.3f}s vẫn403. Đây là bounds theo clock client/DB trên cùng máy, không phải trace thời điểm xử lý chính xác±1ms.','',
    '## Kết quả từng TC','',
    'U=test@eshop.com; P=Test1234!; Z=Wrong123!; V=admin@eshop.com. Fn cần đúng counter n sau n lần sai thật; lỗi counter làm Fn không đạt được nên không ép DB để báo pass. FL trực tiếp được thiết kế cho phép để cô lập kiểm tra khóa.','',
    'Link log ở từng dòng mở `results.json`: tìm `cases[id]`, entry `run_id=FR02-RUN03` (có observations/assertions từng bước). Đây là evidence riêng đúng TC/run dù dùng chung một file; không dùng fragment giả cho JSON.','',
    '| TC / kỹ thuật | Input / nội dung | Expected (nguồn giữ từ TC) | Actual | Kết luận / bug | Evidence |',
    '| --- | --- | --- | --- | --- | --- |']
    for c in d['cases']:
        r=chosen(d,c); key=c['id'][5:]; associated=[b['id'] for b in d['bugs'] if c['id'] in b['cases']]
        description=r['reason'] if r['status']=='blocked' else actual[key]
        evidence=f'[log {c["id"]}/{r["run_id"]}](results.json)'
        if r['images']: evidence+=f'; [JPG]({r["images"][0]["path"]})'
        verdict={'passed':'Đạt (passed)','failed':'Không đạt (failed)','blocked':'Bị chặn (blocked)'}[r['status']]
        if associated: verdict+='; '+', '.join(f'[{b}](#{b.lower()})' for b in associated)
        text.append('| '+ ' | '.join([f'[{c["id"]}](test-cases.md) / '+('Domain+BVA' if 'BVA' in c['trace'] else 'Domain'),cell(c['input_steps']),cell(c['expected']),cell(description),verdict,evidence])+' |')
    text += ['', '## Bug và finding đã tái hiện','',
    '3 defect có oracle FR-02 xác nhận (BUG01–03), 3 finding theo policy A01/A02/A04 đã ghi rõ trong thiết kế (BUG04–06). Finding assumption không tự trở thành vi phạm contract đã xác nhận. Priority là đề xuất. Screenshot API là **API client harness đang gọi SUT thật**, không phải giao diện Web EShop; JWT che ở client. Screenshot Web W07/W08 là UI EShop thật.','']
    if d.get('tracker_overview'):
        overview=d['tracker_overview']
        text += [f'[Tracker T05 — 6 issue]({overview["url"]}); [JPG tổng quan]({overview["image"]}), chụp {local(overview["captured_at"])}.','']
    for b in d['bugs']:
        image=b['symptom_image']; issue=b.get('issue')
        text += [f'<a id="{b["id"].lower()}"></a>',f'### {b["id"]} — {b["title"]}','',
                 f'**Loại / oracle:** {b["kind"]}; {b["oracle"]}. **Ảnh hưởng:** {b["priority"]}.',
                 f'**Môi trường:** revision4bb5158, Windows, source không đổi, Chromium/API ở trên. **TC:** '+(', '.join(b['cases']) or 'Supplementary VERIFY01; TC exact-boundary vẫn blocked')+'.',
                 f'**Precondition và steps:** {b["steps"]}',f'**Expected:** {b["expected"]}',f'**Actual:** {b["actual"]}',
                 f'**Tần suất thực đã thử:** {b["frequency"]}',
                 f'**Evidence:** [log TC và VERIFY01](results.json); chụp {local(image["captured_at"])}.',
                 f'![{b["id"]} symptom]({image["path"]})','']
        if issue:
            text += [f'**GitHub:** [{issue["number"]}]({issue["url"]}); {issue["verification"]}.',
                     f'Ảnh trang issue chụp {local(issue["captured_at"])}:',f'![{b["id"]} issue]({issue["image"]})','']
        else: text += ['**GitHub:** đang hoàn thiện đăng/kiểm tra và ảnh trang issue.','']
    text += ['## Coverage và giới hạn','',
    '- Thiết kế: 13/13 mục tiêu miền và 6/6 boundary items/lớp theo inventory đã công bố; đây không phải coverage runtime.',
    '- Exercise miền theo target: D01–D07, D09–D12 = 11/13; D08 chưa tới success để thử chuỗi mới, D13 không đạt F1 để thử concurrency. D07 mới exercise A11 theo FL trực tiếp; chưa đạt điểm thời gian sát30s.',
    '- BVA catalogue: 0/6 item cho Web và 0/6 cho API được thực hiện đầy đủ đúng precondition/timing của TC. Các ca ngưỡng2/3/4 bị Fn sai chặn; sáu ca±1ms bị thiếu server clock/trace. VERIFY01 quan sát khóa thực tế sau hai sai nhưng không đổi blocked của TC đã duyệt.',
    '- Duration supplementary: dùng bracket request thực kích hoạt khóa và stored deadline để suy khoảng180s; request đúng P sau hơn31s vẫn bị403. Không dùng sleep31s để nhận đã đạt equality30s. FL ở W11/A06 dùng mốc10s nominal, không claim chính xác10.000s.',
    '- Counter observation đọc sau response+60ms API / khoảng250ms UI; đây là delay quan sát, không phải SLA của SUT. State counter2/4/5 được xác minh lại ở các sequence độc lập; không suy bug từ một lần đọc quá sớm.',
    '- Những phần chưa chạy đủ: success-reset sequence, concurrency và BVA sát30s. Khi SUT sửa counter hoặc có clock control, rerun đúng ID với run ID mới. Không sửa SUT/expected để làm xanh.','',
    '## AI gaps và kiểm tra quy trình','',
    '| Loại | Nguồn / tác động | Xử lý |','| --- | --- | --- |',
    '| Execution gap — locator W01 | RUN01 dùng accessible name Hồ sơ, nhưng UI link là Chào,…; timeout trước target profile. | Sửa locator href /profile, đọc email từ disabled input; RUN02/RUN03 W01 passed. Giữ RUN01 blocked. |',
    '| Harness output | RUN02 stdout cp1252 lỗi khi in → sau khi đã lưu W03. | Cấu hình UTF-8; RUN03 chạy đủ catalogue, history không ghi đè. |',
    '| Khả thi timing | Bản đầu đã nêu cần clock/trace; môi trường thực thiếu control±1ms. | Giữ sáu TC blocked, dùng measurement bổ trợ riêng; không nhận là case gap mới. |',
    '| Model/case/oracle review | Đối chiếu v0.1 được duyệt và kết quả; chưa xác định thêm case gap hoặc oracle error trong phạm vi đã exercise. Counter/duration là nghi vấn đã biết từ thiết kế, không kể là bug AI bỏ sót. | Giữ assumption riêng; các miền bị chặn chưa đủ cơ sở kết luận coverage đầy đủ. |','',
    'Các lỗi mô tả trạng thái review thiết kế đã được sửa theo phản hồi thật của Vỹ trước run (commit4bb5158). Trạng thái review report lấy từ lời xác nhận thực tế của Vỹ; không suy sinh viên tự chạy test. Lượt execution không tự cập nhật AI Audit/Prompt Log, commit/push hoặc quay/upload demo; hồ sơ AI được cập nhật ở lượt riêng khi Vỹ giao.']
    (F/'report.md').write_text('\n'.join(text)+'\n',encoding='utf-8')
    print(dict(totals))

if __name__=='__main__': main()
