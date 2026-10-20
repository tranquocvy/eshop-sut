"""Execute the reviewed FR-07 catalogue, without changing SUT or test design.

Run with the T03 Playwright venv and --execute --manifest <T04/services.json>.
UI fixtures use the public UI. No second click is used to bypass failed Add.
"""
import argparse
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
import uuid
from urllib.request import Request, urlopen
from urllib.error import HTTPError

FEATURE = Path(__file__).resolve().parents[1]
REPO = FEATURE.parents[2]
WEB = 'http://localhost:5173'
API = 'http://localhost:3000/api'
OUT = FEATURE / 'results.json'


def now():
    return datetime.now(timezone.utc).isoformat()


def catalogue():
    rows = []
    for line in (FEATURE / 'test-cases.md').read_text(encoding='utf-8').splitlines():
        if re.match(r'^\| CART-[WA]\d\d \|', line):
            cid, trace, pre, steps, expected = [x.strip() for x in line.split('|')[1:-1]]
            rows.append(dict(id=cid, trace=trace, precondition=pre, input_steps=steps, expected=expected))
    assert [r['id'] for r in rows] == [f'CART-W{i:02}' for i in range(1,35)]+[f'CART-A{i:02}' for i in range(1,27)]
    return rows


def request(method, path, body=None, token=None):
    headers = {'Content-Type': 'application/json'}
    if token is not None:
        headers['Authorization'] = 'Bearer ' + token
    req = Request(API + path, method=method, headers=headers,
                  data=json.dumps(body, ensure_ascii=False).encode() if body is not None else None)
    try:
        reply = urlopen(req, timeout=15)
    except HTTPError as exc:
        reply = exc
    with reply:
        text = reply.read().decode()
        try:
            value = json.loads(text)
        except ValueError:
            value = text
        return {'status': reply.status, 'body': value}


class Blocked(Exception):
    pass


class Case:
    def __init__(self, cid, run_id):
        self.data = dict(run_id=run_id, started_at=now(), status='not_run', assertions=[], observations=[], images=[])
        self.cid = cid

    def note(self, step, value):
        self.data['observations'].append({'step': step, 'at': now(), 'value': value})

    def check(self, condition, message):
        self.data['assertions'].append({'check': message, 'ok': bool(condition)})

    def shot(self, page, suffix):
        path = FEATURE / 'images' / f'{self.cid}-{self.data["run_id"]}-{suffix}.jpg'
        path.parent.mkdir(exist_ok=True)
        page.screenshot(path=str(path), type='jpeg', quality=85, full_page=True)
        self.data['images'].append({'path': str(path.relative_to(FEATURE)).replace('\\', '/'), 'captured_at': now(), 'state': suffix})


def cart_state(page):
    # Read rendered DOM only; no state injection, route mocking or API cart calls.
    rows = page.locator('main tbody tr').evaluate_all('(rs)=>rs.map(r=>Array.from(r.querySelectorAll("td")).slice(0,4).map(c=>c.innerText))')
    body = page.locator('main').inner_text()
    result = []
    for name, price, quantity, total in rows:
        num = lambda s: int(re.sub(r'[^0-9-]', '', s)) if re.search(r'\d', s) else None
        result.append({'name': name, 'price': num(price), 'quantity': num(quantity), 'line_total': num(total),
                       'display': [price, quantity, total]})
    match = re.search(r'Tổng[^:\n]*:\s*([^\n]+)', body)
    return {'rows': result, 'total': int(re.sub(r'\D', '', match[1])) if match and re.search(r'\d',match[1]) else None,
            'text': body, 'illustrations': page.locator('main img,main svg,main canvas').count(),
            'headers': page.locator('main th').all_text_contents(),
            'buttons': page.locator('main button').all_text_contents()}


def open_cart(page):
    page.get_by_role('link', name='Giỏ hàng', exact=True).click()
    page.wait_for_url('**/cart')
    page.get_by_role('heading', name=re.compile('^Giỏ')).wait_for()


def home(page):
    page.get_by_role('link', name='EShop', exact=True).click()
    page.get_by_role('heading', name='Danh sách sản phẩm', exact=True).wait_for()


def detail(page, product):
    home(page)
    page.locator(f'a[href="/product/{product["id"]}"]').click()
    page.get_by_role('heading', name=product['name'], exact=True, level=1).wait_for()


def add(page, product, quantity, case, label, target=False):
    detail(page, product)
    page.get_by_role('spinbutton').fill(str(quantity))
    case.note(label + ':input', {'product': product, 'requested': quantity, 'retained': page.get_by_role('spinbutton').input_value()})
    page.get_by_role('button', name='Thêm vào giỏ hàng', exact=True).click()
    # React updates happen synchronously for this click; observe feedback then route.
    main_text=page.locator('main').inner_text()
    case.note(label + ':feedback', {'button': page.get_by_role('button', name=re.compile('Thêm vào giỏ hàng|Đã thêm')).inner_text(),
                                 'validation_alerts':page.get_by_role('alert').all_text_contents(),
                                 'quantity_error':bool(re.search(r'[Ss]ố lượng[^\n]*(hợp lệ|nguyên dương|tối thiểu|bắt buộc)',main_text))})
    if target and case.cid in ('CART-W02','CART-W03','CART-W24','CART-W34'):
        case.shot(page, label + '-detail')
    open_cart(page)
    state = cart_state(page)
    case.note(label + ':cart', state)
    return state


def expected_rows(items, products):
    return [{'name': products[k]['name'], 'price': products[k]['price'], 'quantity': q,
             'line_total': products[k]['price'] * q} for k, q in items]


def match_cart(state, items, products):
    actual = [{k: r[k] for k in ('name','price','quantity','line_total')} for r in state['rows']]
    expected = expected_rows(items, products)
    sort = lambda x: (x['name'], x['price'], x['quantity'] if x['quantity'] is not None else -999)
    return sorted(actual,key=sort) == sorted(expected,key=sort) and (not items or state['total'] == sum(x['line_total'] for x in expected))


def setup(page, case, products, items):
    if not items:
        open_cart(page)
        case.note('precondition C0',cart_state(page))
        return
    for k, q in items:
        # C1 can be prepared through Home's separate, public Add button.
        # For q>1 use the documented detail Add exactly once; never bypass no-op.
        if q == 1:
            home(page)
            card = page.locator('div.border.rounded').filter(has=page.get_by_role('heading',name=products[k]['name'],exact=True))
            card.get_by_role('button',name='Thêm vào giỏ',exact=True).click()
            open_cart(page)
            case.note('fixture Home add '+k,cart_state(page))
        else:
            state=add(page,products[k],q,case,'fixture '+k)
            if not state['rows']:
                case.shot(page,'fixture-blocker')
                raise Blocked('Không đạt precondition: một click Add chi tiết không thêm sản phẩm; không bấm lần hai hoặc inject state để dựng giỏ.')
    if not match_cart(cart_state(page),items,products):
        case.shot(page,'fixture-mismatch')
        raise Blocked('Giỏ fixture qua UI không khớp precondition đã duyệt.')


def web_case(page, case, products):
    n=int(case.cid[-2:])
    C1=[('P',1)]; C2=[('P',2)]; C3=[('P',2),('Q',3),('H',4)]
    fixture = C2 if n in (4,5,10,11,12,13,14,15,17,25,26,32,33) else C3 if n in (6,19,21,22,29,30,31) else C1 if n in (9,16,18,20) else []
    setup(page,case,products,fixture)
    if n == 1:
        s=cart_state(page)
        case.check(not s['rows'] and 'trống' in s['text'],'Giỏ trống có thông báo, không có dòng cũ')
        case.check(s['illustrations']>0,'R08: có hình minh họa giỏ trống')
    elif n in (2,3,34,24):
        k,q={2:('P',1),3:('P',3),34:('P',2),24:('H',1000)}[n]
        s=add(page,products[k],q,case,'target-add',True)
        case.check(match_cart(s,[(k,q)],products),f'Add một click đạt {k}×{q}, đúng thành tiền/tổng')
        case.check(case.data['observations'][-2]['value']['button']=='Đã thêm','R01/FR06: phản hồi trực quan sau thêm')
    elif n in (4,5,6):
        k='Q' if n==5 else 'P'; s=add(page,products[k],3,case,'target-add',True)
        want={4:[('P',5)],5:[('P',2),('Q',3)],6:[('P',5),('Q',3),('H',4)]}[n]
        case.check(match_cart(s,want,products),'Cộng/gộp đúng ID và tổng, giữ dòng khác')
    elif n in (7,8,28):
        sequence = [('P',1)]*3 if n==7 else [(k,1) for k in 'PQMHK'] if n==8 else [('X',2),('Y',3),('X',1)]
        want=[]
        for i,(k,q) in enumerate(sequence):
            s=add(page,products[k],q,case,'sequence-'+str(i+1),True)
            found=next((j for j,x in enumerate(want) if x[0]==k),None)
            if found is None: want.append((k,q))
            else: want[found]=(k,want[found][1]+q)
            case.check(match_cart(s,want,products),'Sequence '+str(i+1)+' đúng dòng/quantity/tổng')
        if n==28: case.check(page.locator('main td b').count()==0,'A07: tên là văn bản, không chạy markup')
    elif n==9:
        s=cart_state(page); case.note('schema',s)
        case.check(s['headers']==['Sản phẩm','Đơn giá','Số lượng','Thành tiền','Thao tác'],'R03: đúng năm cột gồm Đơn giá')
        case.check('+' in s['buttons'] and any(x.strip() in ('-','−') for x in s['buttons']),'R03: có nút + và −')
        case.check('Tổng cộng' in s['text'] and 'Tổng tạm tính' not in s['text'],'R07: nhãn Tổng cộng')
    elif n in (10,11,12,13,14,15,25):
        q={10:'0',11:'-1',12:'0.5',13:'1.5',14:'-0.5',15:'',25:'9007199254740992'}[n]
        s=add(page,products['Q'],q,case,'invalid-add',True)
        case.check(match_cart(s,C2,products),'Reject: giỏ và tổng giữ nguyên')
        feedback=next(x['value'] for x in reversed(case.data['observations']) if x['step']=='invalid-add:feedback')
        case.check(bool(feedback['validation_alerts']) or feedback['quantity_error'],'Có feedback validation rõ; không dùng no-op làm bằng chứng reject')
    elif n in (16,17,18,31,33):
        operations={16:[('P','+',1)],17:[('P','-',1)],18:[('P','-',1)],31:[('Q','+',1),('H','-',1)],33:[('P','+',3),('P','-',2)]}[n]
        for k,sign,count in operations:
            row=page.locator('tbody tr').filter(has_text=products[k]['name'])
            button=row.get_by_role('button',name=re.compile(r'^\+$' if sign=='+' else r'^[-−]$'))
            if not button.count():
                case.note('missing quantity control',cart_state(page)); case.shot(page,'missing-control')
                raise Blocked('Không có nút '+sign+' để thực hiện bước chỉnh quantity (schema R03 được đánh giá tại W09).')
            for _ in range(count): button.click()
            case.note('quantity action '+k+sign,cart_state(page))
        want={16:[('P',2)],17:C1,18:C1,31:[('P',2),('Q',4),('H',3)],33:[('P',3)]}[n]
        case.check(match_cart(cart_state(page),want,products),'Quantity/tổng đúng sau chuỗi +/−')
    elif n in (19,20,21,22):
        target='Q' if n in (19,21) else 'P'; dialogs=[]
        def on_dialog(d):
            dialogs.append({'type':d.type,'message':d.message}); d.dismiss() if n==19 else d.accept()
        page.on('dialog',on_dialog)
        page.locator('tbody tr').filter(has_text=products[target]['name']).get_by_role('button',name='Xóa',exact=True).click()
        s=cart_state(page); case.note('after delete',{'dialogs':dialogs,'cart':s})
        case.check(any(x['type']=='confirm' for x in dialogs),'R05: dialog xác nhận trước xóa')
        if n==19: case.check(match_cart(s,C3,products),'Hủy không xóa hoặc thay tổng')
        elif n==20:
            case.check(not s['rows'] and 'trống' in s['text'],'Xóa dòng cuối về giỏ trống')
            case.check(s['illustrations']>0,'R08: minh họa sau xóa dòng cuối')
        else:
            want=[('P',2),('H',4)] if n==21 else [('Q',3),('H',4)]
            case.check(match_cart(s,want,products),'Chỉ xóa đúng dòng đích và cập nhật tổng')
            if n==22:
                s=add(page,products['P'],1,case,'readd',True)
                case.check(match_cart(s,want+[('P',1)],products),'Thêm lại không giữ q cũ')
    elif n in (23,29):
        states=[[],C1] if n==23 else [C3]
        for i,state in enumerate(states):
            if n==23 and i==1: setup(page,case,products,C1)
            before=cart_state(page); case.note('before continue',before)
            if not state: case.check(before['illustrations']>0,'R08: giỏ trống có minh họa trước continue')
            page.locator('main a[href="/"]').click()
            case.check(page.url.rstrip('/')==WEB,'R06: Tiếp tục mua sắm về /')
            case.note('continue destination',page.url)
            if n==29:
                open_cart(page); page.go_back(); page.go_forward(); case.note('back forward',cart_state(page))
                case.check(match_cart(cart_state(page),C3,products),'A02: điều hướng nội bộ giữ giỏ')
    elif n==30:
        page.reload(); page.get_by_role('heading', name=re.compile('^Giỏ')).wait_for(); s=cart_state(page); case.note('after reload',s)
        case.check(match_cart(s,C3,products),'A02: reload giữ giỏ')
    elif n in (26,27):
        samples=['abc','   '] if n==26 else ['2.0','2e0','+2','02',' 2 ']
        for value in samples:
            detail(page,products['Q']); field=page.get_by_role('spinbutton'); field.fill(''); field.press_sequentially(value)
            retained=field.input_value(); page.get_by_role('button',name='Thêm vào giỏ hàng',exact=True).click()
            feedback=page.get_by_role('button',name=re.compile('Thêm vào giỏ hàng|Đã thêm')).inner_text()
            open_cart(page); s=cart_state(page); case.note('lexical sample',{'input':value,'retained':retained,'feedback':feedback,'cart':s})
            if n==27 and not s['rows']:
                # No verdict about lexical acceptance when every first click is a no-op.
                continue
            case.check(match_cart(s,C2 if n==26 else [('Q',2)],products),'Lexical invariant')
        if n==27: raise Blocked('Khảo sát lexical chưa phân biệt được validation với lỗi click đầu không thêm; không có verdict nhận/từ chối cú pháp.')
    elif n==32:
        bad=add(page,products['Q'],0,case,'invalid',True); case.check(match_cart(bad,C2,products),'Input sai giữ nguyên giỏ')
        good=add(page,products['Q'],2,case,'corrected',True)
        case.check(match_cart(good,C2+[('Q',2)],products),'Sửa q=2 thêm đúng một lần')
    else:
        raise RuntimeError('Unimplemented case '+case.cid)
    case.note('final UI',cart_state(page) if page.url.endswith('/cart') else {'url':page.url})


def new_user(case, suffix):
    email='t04-'+uuid.uuid4().hex+'-'+suffix+'@example.com'
    r=request('POST','/register',{'name':'T04 Runtime User','email':email,'password':'T04Test123!'})
    if r['status']!=200: raise Blocked('Không tạo được user runtime độc lập')
    auth=request('POST','/login',{'email':email,'password':'T04Test123!'})
    token=auth['body'].get('token'); user=auth['body'].get('user',{})
    if not token or user.get('role')!='user': raise Blocked('Không xác minh được nominal user token')
    case.note('API fixture user',{'id':user['id'],'role':user['role'],'fresh_cart':request('GET','/cart',token=token)})
    return token


def api_case_extended(case, products):
    """A15..26: independent API realizations, never preparing Web state."""
    n=int(case.cid[-2:]); token=new_user(case,'TU-extension')
    def body(k,q): return {**products[k],'quantity':q}
    def get(): return request('GET','/cart',token=token)['body']
    def matches(rows,items):
        keys=('id','name','price','quantity')
        if not isinstance(rows,list) or any(not isinstance(x,dict) or not all(k in x for k in keys) for x in rows): return False
        if any(isinstance(x['quantity'],bool) for x in rows): return False
        actual=[{k:x[k] for k in keys} for x in rows]; expected=[body(k,q) for k,q in items]
        encode=lambda xs: sorted(json.dumps(x,sort_keys=True,ensure_ascii=False) for x in xs)
        return encode(actual)==encode(expected)
    def prepare(items):
        if get()!=[]: raise Blocked('API extension requires fresh empty user cart')
        for k,q in items:
            reply=request('POST','/cart',body(k,q),token)
            case.note('API fixture POST',{'body':body(k,q),'response':reply})
            if reply['status']!=200: raise Blocked('API fixture POST refused')
        state=get(); case.note('API fixture verified',state)
        if not matches(state,items): raise Blocked('API fixture AP2/AP3 does not match before target')
    def target(payload, label):
        before=get(); reply=request('POST','/cart',payload,token); after=get()
        case.note('target '+label,{'body':payload,'response':reply,'before':before,'after':after,'auth':'TU'})
        return before,reply,after
    def arithmetic(rows,items,total,label):
        numeric=isinstance(rows,list) and all(isinstance(x,dict) and type(x.get('price')) is int and type(x.get('quantity')) is int for x in rows)
        lines=[x['price']*x['quantity'] for x in rows] if numeric else None
        observed=sum(lines) if numeric else None
        case.note('arithmetic '+label,{'observed_line_totals_vnd':lines,'observed_total_vnd':observed,'expected_total_vnd':total,'note':'Computed from GET data; no API total field assumed'})
        case.check(matches(rows,items) and observed==total,'API rows/identity/quantity/price and arithmetic: '+label)
    fixtures={15:[],16:[('P',2)],17:[('P',2)],18:[('P',2),('Q',3),('H',4)],19:[],20:[],21:[],22:[],23:[('P',2)],24:[('P',2)],25:[('P',2)],26:[('P',2)]}
    prepare(fixtures[n])
    if n in (15,16,17,18):
        k='Q' if n==17 else 'P'; _,reply,after=target(body(k,3),'POST')
        want={15:[('P',3)],16:[('P',5)],17:[('P',2),('Q',3)],18:[('P',5),('Q',3),('H',4)]}[n]
        total={15:90000000,16:150000000,17:144000000,18:258000000}[n]
        case.check(reply['status']==200,'POST valid input accepted')
        arithmetic(after,want,total,'A'+str(n))
    elif n in (19,20,21):
        sequence=[('P',1)]*3 if n==19 else [(k,1) for k in 'PQMHK'] if n==20 else [('X',2),('Y',3),('X',1)]
        want=[]
        for i,(k,q) in enumerate(sequence):
            _,reply,after=target(body(k,q),'sequence '+str(i+1))
            old=next((j for j,x in enumerate(want) if x[0]==k),None)
            if old is None: want.append((k,q))
            else: want[old]=(k,want[old][1]+q)
            total=sum(products[x]['price']*qty for x,qty in want)
            case.check(reply['status']==200,'Sequence POST '+str(i+1)+' accepted')
            arithmetic(after,want,total,'step '+str(i+1))
    elif n==22:
        before,reply,after=target(body('H',1000),'POST')
        if reply['status']>=400:
            text=reply['body']; feedback=isinstance(text,dict) and bool(text.get('error') or text.get('message'))
            case.check(after==before and feedback,'Large quantity rejected clearly without mutation; no business max inferred')
        else:
            arithmetic(after,[('H',1000)],6000000000,'H×1000')
    elif n==23:
        before,reply,after=target(body('Q',9007199254740992),'POST')
        warning=bool(re.search(r'safe|an toàn|precision|giới hạn',json.dumps(reply['body'],ensure_ascii=False),re.I))
        case.check((reply['status']>=400 and after==before) or warning,'A08: reject unsafe quantity or report processing limitation explicitly')
    elif n in (24,25):
        samples=[0.5,-0.5] if n==24 else ['', 'abc','   ']
        for i,q in enumerate(samples):
            if i:
                token=new_user(case,'reset-extension-'+str(i)); prepare([('P',2)])
            before,reply,after=target(body('Q',q),'sample '+str(i+1))
            case.check(reply['status']>=400 and after==before,'AR input '+repr(q)+' rejected; AP2 unchanged')
    elif n==26:
        before,reply,after=target(body('Q',0),'invalid Q0')
        case.check(reply['status']>=400 and after==before,'AR invalid step preserves AP2')
        _,reply,after=target(body('Q',2),'corrected Q2 same session')
        case.check(reply['status']==200,'Corrected input accepted in same session')
        arithmetic(after,[('P',2),('Q',2)],116000000,'recovery final state')
    return token


def api_case(browser,case,products):
    n=int(case.cid[-2:]); token=None if n>=15 else new_user(case,'TU')
    def body(k,q): return {**products[k],'quantity':q}
    def get(t=token): return request('GET','/cart',token=t)['body']
    def call(payload, t=token):
        before=get(); reply=request('POST','/cart',payload,t); after=get()
        case.note('target POST',{'body':payload,'auth':'TU' if t==token else str(t), 'response':reply,'before':before,'after':after})
        return before,reply,after
    if n>=15:
        token=api_case_extended(case,products)
    elif n in (1,2):
        t=None if n==1 else 'invalid-token'; before=get()
        a=request('GET','/cart',token=t); b=request('POST','/cart',body('P',1),t); after=get()
        case.note('auth requests',{'auth':'missing' if t is None else t,'GET':a,'POST':b,'before':before,'after':after})
        case.check(a['status'] in (401,403) and b['status'] in (401,403) and after==before,'R10: GET/POST từ chối auth và không thay giỏ')
    elif n==3:
        reply=request('GET','/cart',token=token); case.note('target GET',reply)
        case.check(reply['status']==200 and reply['body']==[],'Nominal user GET cart rỗng')
    elif n in (4,5,13,14):
        q=1 if n==4 else 2; payload=body('P',q)
        if n==13: payload['price']=1
        tv=new_user(case,'TV') if n==14 else None
        before,reply,after=call(payload)
        if n==13:
            case.check((reply['status']>=400 and after==before) or (after==[body('P',2)]),'A06: từ chối giá giả hoặc dùng giá thật')
        else:
            case.check(reply['status']==200 and after==[body('P',q)],'API thêm đúng dòng/q/giá')
        if n==14:
            other=get(tv); case.note('TV after TU mutation',other); case.check(other==[],'A06: giỏ user độc lập')
    else:
        request('POST','/cart',body('P',1),token)
        if get()!=[body('P',1)]: raise Blocked('AP1 không đạt')
        payloads=[]
        if n==6: payloads=[body('P',3)]
        elif n in (7,8,9): payloads=[body('Q',{7:0,8:-1,9:1.5}[n])]
        elif n==10:
            missing=body('Q',1); missing.pop('quantity'); payloads=[missing,body('Q',None)]
        elif n==11: payloads=[body('Q',q) for q in ('2',True,[],{})]
        elif n==12:
            z=999999; existing=request('GET','/products')['body']; assert all(p['id']!=z for p in existing)
            payloads=[{'id':z,'name':'T04 Unknown','price':28000000,'quantity':1}]
        else: raise RuntimeError('Unimplemented API '+case.cid)
        for i,payload in enumerate(payloads):
            if i:
                token=new_user(case,'reset'+str(i)); request('POST','/cart',body('P',1),token)
                if get(token)!=[body('P',1)]: raise Blocked('Reset AP1 không đạt')
            before=get(token); reply=request('POST','/cart',payload,token); after=get(token)
            case.note('target POST '+str(i+1),{'body':payload,'auth':'TU','response':reply,'before':before,'after':after})
            if n==6: case.check(after==[body('P',4)],'A03: cùng ID gộp q=4 một dòng')
            else: case.check(reply['status']>=400 and after==before,'AR: từ chối và giữ AP1')
    # Capture the real authenticated JSON response in the browser for API failures.
    if any(not x['ok'] for x in case.data['assertions']) and (n<15 or n in (16,23)):
        ctx=browser.new_context(extra_http_headers={'Authorization':'Bearer '+token},viewport={'width':1280,'height':760})
        p=ctx.new_page(); p.goto(API+'/cart'); case.shot(p,'actual-api-cart'); ctx.close()


def save(data):
    selected=[next((x for x in reversed(c['results']) if x['run_id']==data['selected_results'].get(c['id'])),{'status':'not_run'}) for c in data['cases']]
    counts=Counter(r['status'] for r in selected)
    data['summary']={'designed':len(data['cases']),**{k:counts[k] for k in ('passed','failed','blocked','not_run')},'executed':counts['passed']+counts['failed'],'not_executed':counts['blocked']+counts['not_run']}
    tmp=OUT.with_suffix('.json.tmp'); tmp.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8'); tmp.replace(OUT)


def main():
    parser=argparse.ArgumentParser(); parser.add_argument('--execute',action='store_true'); parser.add_argument('--manifest',type=Path); parser.add_argument('--run-id'); parser.add_argument('--case',nargs='+')
    args=parser.parse_args(); cat=catalogue()
    if not args.execute:
        print('\n'.join(c['id']+' '+c['trace'] for c in cat)); return
    assert args.manifest and args.run_id
    manifest=json.loads(args.manifest.read_text(encoding='utf-8')); products=manifest['products']
    remote=request('GET','/products')['body']
    assert all(any(all(p[k]==v[k] for k in ('id','name','price')) for p in remote) for v in products.values())
    data=json.loads(OUT.read_text(encoding='utf-8')) if OUT.exists() else dict(schema_version=1,feature='T04 FR-07 Shopping Cart',design_commit='475165e35a7c13988abf86bc10a988ab7a6b34f1',runs=[],cases=[{**c,'results':[]} for c in cat],selected_results={},bugs=[])
    existing={c['id']:c for c in data['cases']}
    for c in cat:
        if c['id'] not in existing:
            data['cases'].append({**c,'results':[]})
        else:
            assert all(existing[c['id']][k]==v for k,v in c.items()), 'Existing TC changed: '+c['id']
    data['design_version']='0.2'
    assert args.run_id not in {r['id'] for r in data['runs']}
    chosen=args.case or [c['id'] for c in cat]; assert set(chosen)<=set(c['id'] for c in cat)
    run={'id':args.run_id,'started_at':now(),'state':'running','chosen':chosen,'revision':subprocess.check_output(['git','rev-parse','HEAD'],cwd=REPO,text=True).strip(),'web':WEB,'api':API,'fixture':manifest,'executor':'Codex / Python Playwright and HTTP','source_hashes':{str(p.relative_to(REPO)).replace('\\','/'):hashlib.sha256(p.read_bytes()).hexdigest() for p in [FEATURE/'design.md',FEATURE/'test-cases.md',Path(__file__),REPO/'frontend-web/src/context/CartContext.jsx',REPO/'frontend-web/src/pages/Cart.jsx',REPO/'frontend-web/src/pages/ProductDetail.jsx',REPO/'backend/server.js']}}
    data['runs'].append(run); save(data)
    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        browser=pw.chromium.launch(headless=True); run['browser']=browser.version
        for entry in data['cases']:
            if entry['id'] not in chosen: continue
            case=Case(entry['id'],args.run_id); ctx=None
            try:
                if '-W' in entry['id']:
                    ctx=browser.new_context(viewport={'width':1440,'height':1000}); p=ctx.new_page(); p.set_default_timeout(7000); p.goto(WEB)
                    web_case(p,case,products)
                    if any(not x['ok'] for x in case.data['assertions']): case.shot(p,'final-failure')
                else: api_case(browser,case,products)
                case.data['status']='failed' if any(not x['ok'] for x in case.data['assertions']) else 'passed'
                case.data['reason']='; '.join(x['check'] for x in case.data['assertions'] if not x['ok']) or 'Các assertion đã thực hiện đều đạt'
            except Blocked as exc:
                case.data.update(status='blocked',reason=str(exc))
            except Exception as exc:
                case.data.update(status='blocked',reason='Harness/environment: '+type(exc).__name__+': '+str(exc)[:350])
                run['state']='stopped_harness'; case.note('harness exception',case.data['reason'])
            finally:
                case.data['finished_at']=now(); entry['results'].append(case.data); data['selected_results'][entry['id']]=args.run_id; save(data)
                if ctx: ctx.close()
                print(entry['id'],case.data['status'],case.data['reason'],flush=True)
            if run['state']=='stopped_harness': break
        else: run['state']='finished_selected_cases'
        run['finished_at']=now(); save(data); browser.close()
    print(json.dumps(data['summary']),flush=True)


if __name__=='__main__':
    if hasattr(sys.stdout,'reconfigure'): sys.stdout.reconfigure(encoding='utf-8')
    main()
