"""Render the readable report from the one results.json source; never runs SUT."""
from collections import Counter
from datetime import datetime, timezone, timedelta
import json
from pathlib import Path

FEATURE=Path(__file__).resolve().parents[1]


def cell(value):
    return str(value).replace('|','\\|').replace('<','&lt;').replace('\n',' ')


def selected(data, case):
    return next(r for r in reversed(case['results']) if r['run_id']==data['selected_results'][case['id']])


def actual(case, result):
    obs=result['observations']; cid=case['id']
    if result['status']=='blocked': return result['reason']
    if cid=='CART-W09': return 'P×1, tổng 30.000.000 đúng; header Giá, không có +/−, nhãn Tổng tạm tính.'
    if cid=='CART-W20': return 'P×1→0 dòng ngay sau Xóa; dialogs=[]; thông báo trống, không có minh họa.'
    if cid=='CART-W23': return 'C0 và C1 đều đi về /; C0 có thông báo nhưng thiếu hình minh họa.'
    if cid.startswith('CART-W'):
        states=[o['value'] for o in obs if isinstance(o['value'],dict) and 'rows' in o['value']]
        state=states[-1] if states else {}
        if cid=='CART-W01': return '0 dòng; có thông báo giỏ trống, không có img/svg/canvas hoặc minh họa nhìn thấy.'
        return 'Sau một click mỗi lần Add: '+str(len(state.get('rows',[])))+' dòng; giỏ trống, chưa có thành tiền/tổng. '+result['reason']
    if int(cid[-2:])>=15:
        summaries={
            'CART-A15':'POST 200; GET một P×3 đúng giá, tích 90.000.000.',
            'CART-A16':'P×2 + P×3: POST 200; GET hai dòng P×2/P×3. Tổng suy ra 150.000.000 đúng nhưng không gộp thành một dòng q=5.',
            'CART-A17':'POST 200; GET giữ P×2, thêm Q×3; hai ID/dòng đúng, tổng suy ra 144.000.000.',
            'CART-A18':'AP3 + P×3: GET bốn dòng P×2,Q×3,H×4,P×3, không gộp P×5; tổng suy ra vẫn 258.000.000.',
            'CART-A19':'Ba POST đều 200; GET sau từng bước có 1/2/3 dòng P×1 thay vì một dòng P×1/2/3.',
            'CART-A20':'Năm POST/GET đều đúng; mỗi ID mới giữ dòng cũ, cuối đủ năm sản phẩm, tổng suy ra 113.000.000.',
            'CART-A21':'X/Y cùng tên tách được theo ID sau hai bước; bước thêm X×1 tạo dòng thứ ba, không gộp X×3. Giá/tên giữ đúng; tổng suy ra 1.200.000.',
            'CART-A22':'POST 200; GET H×1000, price=6000000, tích chính xác 6.000.000.000; không nhận đây là max nghiệp vụ.',
            'CART-A23':'POST 200, message Added to cart; GET lưu Q.quantity=9007199254740992, không từ chối/cảnh báo giới hạn an toàn theo A08.',
            'CART-A24':'Hai mẫu q=0.5 và -0.5 đều POST 200, GET thêm dòng Q với quantity phân số; không giữ nguyên AP2.',
            'CART-A25':'Ba mẫu string rỗng/abc/ba dấu cách đều POST 200 và được giữ nguyên trong dòng Q của GET.',
            'CART-A26':'Cùng TU: Q×0 bị nhận 200, rồi Q×2 cũng 200; cuối P×2,Q×0,Q×2 — ba dòng, không phải chỉ P×2,Q×2 dù tổng suy ra vẫn 116.000.000.'}
        return summaries[cid]
    targets=[o['value'] for o in obs if o['step'].startswith('target')]
    if cid in ('CART-A01','CART-A02'):
        x=next(o['value'] for o in obs if o['step']=='auth requests')
        return f"GET {x['GET']['status']}, POST {x['POST']['status']}; giỏ TU giữ nguyên."
    if cid=='CART-A03': return 'GET 200, body=[] với nominal user token.'
    x=targets[-1]; rows=x.get('after',[])
    if cid=='CART-A14': return 'POST TU 200; TU có P×2 đúng giá, GET TV=[]; không ghi chéo user.'
    if cid in ('CART-A04','CART-A05'): return 'POST 200; GET đúng một P, quantity='+str(rows[0]['quantity'])+', price=30000000.'
    if cid=='CART-A06': return 'POST 200; GET hai dòng cùng ID6: quantity 1 và 3, không gộp thành 4.'
    if cid=='CART-A13': return 'POST 200; GET lưu price=1,quantity=2 cho P giá thật 30000000.'
    if cid=='CART-A12': return 'ID999999 vắng trong products; POST 200 và GET cart vẫn có hàng ảo đó.'
    return 'Mọi mẫu đã gửi đều POST 200 và thêm dòng trái AR; '+json.dumps([t['body'] for t in targets],ensure_ascii=False,separators=(',',':'))


def main():
    data=json.loads((FEATURE/'results.json').read_text(encoding='utf-8')); s=data['summary']
    total=s['designed']; api_count=sum(c['id'].startswith('CART-A') for c in data['cases'])
    pass_rate=100*s['passed']/s['executed'] if s['executed'] else 0
    lines=['# T04 — FR-07 Shopping Cart: execution và report','',
           f'**20/10/2026 (UTC+7).** [Design](design.md), [{total} TC](test-cases.md). 48 TC v0.1 đã được Vỹ duyệt tại commit `475165e`; v0.2 thêm A15–A26 theo yêu cầu bổ sung API và kiểm thử, Vỹ đã xác nhận kiểm tra hồ sơ T04 và chốt hoàn tất ngày 20/10/2026. Baseline source execution `46e4715`, hash từng phiên bản trong run; không sửa nghiệp vụ SUT.','',
           f"**Kết quả unique: {s['passed']} passed, {s['failed']} failed, {s['blocked']} blocked, {s['not_run']} not_run.** Executed = passed+failed = {s['executed']}/{total}; not_executed = blocked+not_run = {s['not_executed']}/{total}. Pass rate trên executed = {s['passed']}/{s['executed']} = {pass_rate:.2f}%; đây không phải coverage. Giữ nguyên 48 kết quả đã chọn trước mở rộng; RUN04 chỉ chạy 12 TC API mới (4 passed, 8 failed).",'',
           '## Môi trường, fixture và cách đếm','',
           '- Windows, Chromium '+data['runs'][-1]['browser']+' qua Playwright Python; Web `http://localhost:5173`, API `http://localhost:3000/api`. Backend T03 đang chạy được tái sử dụng, không reset/restart. Dữ liệu chuẩn bị chỉ trong SQLite runtime `HW02/.runtime/T03-execution-20261020/backend/database.sqlite`; đã backup trước fixture tại runtime T04. Không ghi database trong repo.',
           '- P/Q/M/H/K giữ đúng tên/giá seed, ID runtime lần lượt 6/7/8/9/10; X/Y là hai sản phẩm fixture cùng tên, ID11/12, giá 125000/275000. Fixture được GET products xác nhận trước run. API dùng user thử độc lập qua register/login bình thường; không ghi JWT/password vào kết quả.',
           '- Web context mới mỗi TC; C1 chuẩn bị bằng nút Home “Thêm vào giỏ” một click. C2/C3 cần quantity >1: Add chi tiết một click không tạo hàng nên ghi blocked, không bấm lần hai, dùng API hoặc inject state để vượt precondition. W16/W18 tới C1 nhưng thiếu control nên blocked.',
           '- Một nguồn chung [results.json](results.json): `runs[]`, `cases[].results[]`, `selected_results`, `bugs`. Chọn lần mới nhất được chỉ định cho từng unique ID; giữ cả smoke và harness failure cũ. Run và thời gian chỉ lưu một lần/run, observation có timestamp thật. Mỗi link log ở bảng dưới chỉ rõ TC/run; tìm entry `cases[id] → results[run_id]` trong JSON, không dùng fragment giả cho JSON.','',
           '| Run | Phạm vi / trạng thái | 20/10/2026 (UTC+7) |','| --- | --- | --- |']
    layer_rows=['| Lớp | TC | Passed | Failed | Blocked | Not run |','| --- | ---: | ---: | ---: | ---: | ---: |']
    for prefix,name in [('CART-W','Web'),('CART-A','API')]:
        cases=[c for c in data['cases'] if c['id'].startswith(prefix)]
        count=Counter(selected(data,c)['status'] for c in cases)
        layer_rows.append(f"| {name} | {len(cases)} | {count['passed']} | {count['failed']} | {count['blocked']} | {count['not_run']} |")
    at=lines.index('## Môi trường, fixture và cách đếm'); lines[at:at]=layer_rows+['']
    for r in data['runs']:
        recorded=[c['id'] for c in data['cases'] if any(x['run_id']==r['id'] for x in c['results'])]
        scope={'CART-RUN-01':'Smoke W01/W02/W09/W16/W20','CART-RUN-02':'Yêu cầu cả suite v0.1, dừng tại W28','CART-RUN-03':'W28–W34 và A01–A14','CART-RUN-04':'Bổ sung v0.2: A15–A26, giữ Web cũ'}.get(r['id'],', '.join(r['chosen']))
        clock=lambda value: datetime.fromisoformat(value.replace('Z','+00:00')).astimezone(timezone(timedelta(hours=7))).strftime('%H:%M:%S')
        times=clock(r['started_at'])+' → '+clock(r['finished_at']) if r.get('finished_at') else clock(r['started_at'])
        lines.append(f"| {r['id']} | {scope}; {len(recorded)} entry. {r['state']}. {cell(r.get('harness_note',''))} | {times} |")
    lines+=['','## Kết quả từng TC','',
            'Expected giữ nguồn và assumption trong thiết kế; “không đạt” ở A03/A06 chỉ có nghĩa không đáp ứng oracle bổ sung. Input trong ca blocked là **dự kiến**, chưa được đưa tới bước mục tiêu.','']
    status={'passed':'Đạt (passed)','failed':'Không đạt (failed)','blocked':'Bị chặn (blocked)','not_run':'Chưa chạy (not_run)'}
    for group,title in [('W','Web — 34 TC'),('A',f'API bổ trợ — {api_count} TC')]:
        lines += ['### '+title,'','| TC / input và bước chính | Expected / nguồn | Actual | Kết luận / bug | Evidence đúng TC/run |','| --- | --- | --- | --- | --- |']
        for c in data['cases']:
            if not c['id'].startswith('CART-'+group): continue
            r=selected(data,c); bugs=' '.join('[%s](#%s)'%(b,b.lower()) for b in c.get('bug_ids',[]))
            evidence=f"[Log {c['id']} / {r['run_id']}](results.json)"
            if r['images']: evidence+=f"; [JPG]({r['images'][0]['path']})"
            lines.append('| '+f"[{c['id']}](test-cases.md) — {cell(c['input_steps'])}"+' | '+cell(c['expected'])+' | '+cell(actual(c,r))+' | '+status[r['status']]+' '+bugs+' | '+evidence+' |')
    lines+=['','## Coverage đã exercise và phần bị chặn','',
            'Coverage thiết kế nằm tại design.md; bảng dưới chỉ nhận các điểm thực sự tới được. Không lấy API thay bằng chứng Web và không lấy blocked thành coverage rule mục tiêu.','',
            '| Inventory | Đã exercise / giới hạn |','| --- | --- |',
            '| B01 q_add Web 0/1/2 | q=1 và q=2 đã nhập, bấm một lần ở W02/W34: 2/3 input items; cả hai không thêm được. q=0 của W10 chưa tới do C2 không đạt. Đây không chứng minh validation q hợp lệ đúng. |',
            '| B02 q_cart 0/1/2 (assumption) | 0/3 thao tác biên mục tiêu; W16/W18 không có +/−; W17 không đạt C2. Giá trị q=1 của fixture không thay cho thao tác − đạt 1. |',
            '| B03 số dòng 0/1 | 2/2 items khả thi đã quan sát: W01 C0; W09 C1; W20 1→0 khi Xóa. −1 không biểu diễn. |',
            '| B04 API q_add 0/1/2 (A03) | 3/3 items đã gửi/GET: A07/A04/A05; q=0 bị nhận sai oracle. |',
            '| D01/D02 | Đã xem C0/C1, thêm từ chi tiết q=1/3 bị lỗi. |',
            '| D03/D04 | Gộp Web chưa exercise vì precondition lỗi hoặc sequence không thêm; W08 đã mở đủ năm seed và click nhưng không tạo C5. W28 đã mở X/Y và nhập 2/3/1, chưa credit nhận diện cùng tên khi giỏ vẫn trống. |',
            '| D05–D08 | q=1/2/3/1000 có thao tác Add; invalid âm/0/phân số/rỗng/chữ chưa tới do C2 bị chặn; không kết luận validation Web. |',
            '| D09/D10 | Chưa thao tác +/−; xóa dòng cuối đã exercise, hủy và xóa dòng giữa chưa tới. |',
            '| D11/D12/D16 | Continue C0/C1 đã đi về /; Back/Forward/reload, phục hồi invalid, thao tác nhanh blocked; lexical W27 bị click đầu che nên không verdict cú pháp. |',
            '| D13–D15 | API auth, empty/add/duplicate/invalid q/type/ID/price/isolation đã có request/GET; policy A03/A06 tách requirement R10. |','',
            'Mở rộng RUN04: A15–A26 đều đã thực thi; thêm coverage API cho P2+P3, AP3+P3, thêm ID khác, năm seed, X/Y cùng tên, q=1000, unsafe integer A08, phân số ±0.5, string sai kiểu và recovery cùng phiên. Inventory biên cũ không đổi; kết quả này không tăng coverage Web. Xem ánh xạ mục tiêu/layer tại design.md §6.','',
            'Không công bố “100% rule/miền”: R02 Web, R09 invalid Web và số học nhiều dòng R04 còn chưa kiểm chứng. Dữ liệu nhiều sản phẩm không có nghĩa đã tính được tổng C5 trên Web.','',
            '## Bugs và findings','',
            '5 lỗi requirement Web và 4 finding API theo assumption. Không tạo issue cho từng blocked TC; chúng dẫn dependency về lỗi click đầu hoặc control thiếu. Ảnh raw JSON ở API là response thật mở bằng browser với token trong header; không dựng ảnh log. Request/response đầy đủ nằm trong TC tương ứng, ảnh chỉ minh họa mẫu được nêu.','']
    if data.get('github_overview'):
        o=data['github_overview']
        lines += [f"[Tracker T04 — {o['count']} kết quả]({o['url']})",'',f"![Tracker T04]({o['image']})",'',f"Ảnh danh sách chụp {o['captured_at']} (UTC). Từng issue có ảnh trang riêng bên dưới.",'']
    for b in data['bugs']:
        lines += [f'<a id="{b["id"].lower()}"></a>','',f"### {b['id']} — {b['title']}",'',
                  f"**Loại/oracle:** {b['kind']} — {b['oracle']}. **Priority:** {b['priority']}. **TC/run:** {', '.join(b['cases'])}; {b['run']}.",'',
                  f"**Precondition / steps:** {b['steps']}",'',f"**Expected:** {b['expected']}",'',f"**Actual:** {b['actual']}",'',
                  f"**Tác động / tần suất:** {b['impact']} {b['frequency']}.",'',f"![{b['id']} — SUT]({b['image']})",'']
        image_record=next((im for c in data['cases'] for r in c['results'] for im in r['images'] if im['path']==b['image']),None)
        if image_record: lines += [f"Ảnh SUT chụp {image_record['captured_at']} (UTC), {image_record['state']}; log mục tiêu tại TC/run trên.",'']
        g=b['github']
        if g.get('url'):
            lines += [f"**GitHub:** [{g['url'].split('/')[-1]}]({g['url']}) — {g['state']}; kiểm tra nội dung/ảnh: {g.get('verified_at','')} (UTC).",'']
            if g.get('issue_image'): lines += [f"![{b['id']} — trang issue thật]({g['issue_image']})",'',f"Ảnh trang issue chụp {g.get('captured_at','')} (UTC); khác ảnh SUT của run.",'']
        else: lines += ['**GitHub:** chưa đăng; không nhận hồ sơ Issues hoàn tất.','']
        for extra in b.get('additional_executions',[]):
            lines += [f"**Bổ sung {extra['run_id']} — {', '.join(extra['cases'])}:** {extra['actual']}",'',f"Oracle: {extra['oracle']}. Không đếm thành bug mới khi cùng thiếu xử lý merge/validation đã xác nhận.",'']
            if extra.get('image'): lines += [f"![{b['id']} — SUT run bổ sung]({extra['image']})",'']
        for update in g.get('updates',[]):
            lines += [f"[Bình luận bổ sung]({update['url']}) — nội dung và ảnh hiển thị đã kiểm tra lúc {update['verified_at']} (UTC).",'']
            if update.get('issue_image'): lines += [f"![{b['id']} — trang issue sau bổ sung]({update['issue_image']})",'']
            if update.get('comment_image'): lines += [f"[Ảnh cận phần bình luận bổ sung]({update['comment_image']})",'']
    lines+=['## Giới hạn và bước tiếp theo','',
            '23 TC blocked cần chạy lại khi precondition/control có thể đạt đúng bước. Không sửa SUT trong task testing, không đổi expected hoặc tự tạo kết quả xanh. Harness sửa chờ render route và locator h1 đã ghi trong run history. Khoảng thiếu TC API tương ứng trong bản v0.1 đã được Vỹ chỉ ra và xử lý bằng A15–A26 ở v0.2 (design.md §6); nguồn góp ý và sửa sai nằm trong AI log P-034–P-036. Các ca bị chặn không tự là test bị AI bỏ sót.','',
            'Implementation: [hướng dẫn và mapping](IMPLEMENTATION.md), [runner](scripts/run.py), [report renderer](scripts/report.py). Implementation/execution đã commit tại `ee8e477`; AI Audit và Prompt Log P-034–P-036 đã được cập nhật tại [hồ sơ AI](../../../docs/hw02/ai/artifacts.md). Vỹ xác nhận đã kiểm tra hồ sơ và chốt T04 ngày 20/10/2026; PLAN local đã đánh dấu hoàn tất. Việc chạy lại blocked phụ thuộc sửa SUT, không phải yêu cầu review còn chờ.']
    (FEATURE/'report.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    print('Rendered report:',data['summary'])


if __name__=='__main__': main()
