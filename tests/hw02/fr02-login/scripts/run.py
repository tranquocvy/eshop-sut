"""Run the reviewed FR02 catalogue. Explicit --execute required; no SUT edits."""
import argparse
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import sqlite3
import subprocess
import sys
import time
from urllib.request import Request, urlopen
from urllib.error import HTTPError

FEATURE = Path(__file__).resolve().parents[1]
REPO = FEATURE.parents[2]
U, P, V, VP, Z = 'test@eshop.com', 'Test1234!', 'admin@eshop.com', 'Admin123!', 'Wrong123!'
API, WEB = 'http://localhost:3000/api', 'http://localhost:5173'

def now(): return datetime.now(timezone.utc).isoformat()
def iso(ms): return datetime.fromtimestamp(ms/1000, timezone.utc).isoformat(timespec='milliseconds').replace('+00:00','Z')
def rows():
    out=[]
    for line in (FEATURE/'test-cases.md').read_text(encoding='utf-8').splitlines():
        if re.match(r'^\| [WA]\d\d \|', line):
            cid, trace, pre, steps, expected = [s.strip() for s in line.split('|')[1:-1]]
            out.append(dict(id='FR02-'+cid,trace=trace,precondition=pre,input_steps=steps,expected=expected,results=[]))
    assert len(out)==45 and len({r['id'] for r in out})==45
    return out

def http(path, body=None, token=None):
    headers={'Content-Type':'application/json'}
    if token: headers['Authorization']='Bearer '+token
    req=Request(API+path,data=json.dumps(body).encode() if body is not None else None,headers=headers)
    start=time.time()*1000
    try: response=urlopen(req,timeout=15)
    except HTTPError as e: response=e
    with response:
        raw=response.read().decode(); status=response.status
    try: value=json.loads(raw)
    except ValueError: value=raw[:500]
    return dict(status=status,body=value,request_interval_ms=[start,time.time()*1000])

def safe(value):
    if isinstance(value,dict):
        return {k:('[present]' if k=='token' and v else v) if k=='token' else safe(v) for k,v in value.items()}
    if isinstance(value,list): return [safe(x) for x in value]
    return value

class Blocked(Exception): pass
class Case:
    def __init__(self,cid,run):
        self.cid=cid; self.r=dict(run_id=run,started_at=now(),status='not_run',observations=[],assertions=[],images=[])
    def note(self,step,value): self.r['observations'].append(dict(at=now(),step=step,value=safe(value)))
    def check(self,condition,label): self.r['assertions'].append(dict(check=label,ok=bool(condition)))
    def shot(self,page,label):
        name=f'{self.cid}-{self.r["run_id"]}-{label}.jpg'
        page.screenshot(path=str(FEATURE/'images'/name),type='jpeg',quality=85,full_page=True)
        self.r['images'].append(dict(path='images/'+name,captured_at=now(),state=label))

class Runner:
    def __init__(self,db,browser): self.db=db; self.browser=browser
    def sql(self,query,args=()):
        with sqlite3.connect(self.db,timeout=10) as db:
            db.row_factory=sqlite3.Row
            cur=db.execute(query,args)
            return [dict(r) for r in cur.fetchall()]
    def state(self,email=U):
        return self.sql('SELECT email,login_attempts,locked_until FROM users WHERE email=?',(email,))[0]
    def reset(self):
        self.sql('UPDATE users SET login_attempts=0,locked_until=NULL,reset_token=NULL WHERE email IN (?,?)',(U,V))
    def lock(self,c):
        # Independent FL fixture allowed in reviewed design; t0 is nominal 10s ago.
        current=time.time()*1000; t0=current-10000; deadline=t0+30000
        self.sql('UPDATE users SET login_attempts=3,locked_until=? WHERE email=?',(iso(deadline),U))
        c.note('FL direct fixture (not natural three-failure sequence)',dict(t0_ms=t0,deadline_ms=deadline,state=self.state()))
        return deadline
    def post(self,c,email=U,password=Z,body=None):
        payload=dict(email=email,password=password) if body is None else body
        result=http('/login',payload); time.sleep(.06)
        c.note('POST /api/login',dict(request=payload,response=result,state=self.state()))
        return result
    def form(self,page):
        page.goto(WEB+'/login'); page.locator('main form input').nth(0).wait_for()
    def submit(self,c,page,email=U,password=Z):
        self.form(page)
        fields=page.locator('main form input'); fields.nth(0).fill(email); fields.nth(1).fill(password)
        requests=[]
        def collect(response):
            if response.url==API+'/login':
                try: requests.append(dict(status=response.status,body=response.json()))
                except Exception: requests.append(dict(status=response.status))
        page.on('response',collect)
        started=now(); page.get_by_role('button',name='Sign In',exact=True).click()
        if email and password:
            page.wait_for_timeout(250)
        else: page.wait_for_timeout(100)
        page.remove_listener('response',collect)
        token=page.evaluate('localStorage.getItem("token")')
        result=dict(started_at=started,email=email,password=password,url=page.url,responses=requests,
                    text=page.locator('main').inner_text(),token_present=bool(token),
                    fields=fields.evaluate_all('(xs)=>xs.map(x=>({type:x.type,required:x.required,valid:x.validity.valid,message:x.validationMessage}))') if '/login' in page.url else [],state=self.state())
        c.note('UI submit',result)
        return result
    def denied(self,result): return result['status']!=200 and not (isinstance(result.get('body'),dict) and result['body'].get('token'))
    def success(self,result): return result['status']==200 and isinstance(result['body'],dict) and bool(result['body'].get('token'))
    def pre_n(self,c,n,submit):
        for i in range(n):
            submit()
            state=self.state()
            if state['login_attempts']!=i+1 or state['locked_until']:
                raise Blocked(f'Fn không đạt sau lần sai {i+1}: counter={state["login_attempts"]}, lock={state["locked_until"]}; chưa chạy request mục tiêu.')
    def api(self,c,k):
        if k in (8,9,10):
            raise Blocked('Không có server clock/trace điều khiển và xác minh được ±1ms; chưa gửi request tại điểm biên yêu cầu.')
        if k in (3,4,7,26): self.pre_n(c,{3:1,4:2,7:3,26:1}[k],lambda:self.post(c))
        if k==1:
            r=self.post(c,password=P); c.check(self.success(r),'200 JWT login')
            if self.success(r):
                me=http('/users/me',token=r['body']['token']); c.note('GET /users/me with Bearer',me)
                c.check(me['status']==200 and me['body'].get('email')==U,'Bearer authenticates U')
        elif k==2:
            r=self.post(c); st=self.state(); c.check(self.denied(r) and st['login_attempts']==1 and not st['locked_until'],'0→1, rejected and unlocked')
        elif k in (3,4,7):
            r=self.post(c); target={3:2,4:3,7:3}[k]; st=self.state()
            c.check(st['login_attempts']==target,'counter target')
            rr=self.post(c,password=P); c.check(self.success(rr) if k==3 else self.denied(rr),'correct P allowed only below 3')
        elif k==5:
            a=self.post(c); self.reset(); b=self.post(c,email='fr02.absent@example.com',password=P)
            c.check(self.denied(a) and self.denied(b) and a['body']==b['body'],'generic failure body')
        elif k==6:
            self.lock(c); before=self.state(); r=self.post(c,password=P)
            c.check(self.denied(r) and self.state()==before,'locked correct P rejected, no counter/deadline mutation')
        elif k==11:
            # FL created now, expiry genuinely waited for 31s; no fake server clock.
            t0=time.time()*1000; self.sql('UPDATE users SET login_attempts=3,locked_until=? WHERE email=?',(iso(t0+30000),U))
            c.note('FL at real t0',dict(t0_ms=t0,state=self.state()))
            time.sleep(31)
            r=self.post(c); a=self.state(); r2=self.post(c); b=self.state(); r3=self.post(c,password=P)
            c.check(a['login_attempts']==1 and not a['locked_until'],'first failure after expiry starts fresh at 1 (A01)')
            c.check(b['login_attempts']==2 and not b['locked_until'],'second failure stays unlocked')
            c.check(self.success(r3),'P succeeds after two new failures')
        elif 12<=k<=19:
            bodies={12:dict(password=P),13:dict(email=U),14:dict(email='',password=P),15:dict(email=U,password=''),
                    16:dict(email=None,password=P),17:dict(email=U,password=None),18:dict(email=[U],password=P),19:dict(email=U,password={'value':P})}
            before=self.state(); r=self.post(c,body=bodies[k]);
            c.check(self.denied(r) and r['status']<500,'controlled rejection without token/500')
            c.check(self.state()==before,'invalid payload does not mutate counter (A02)')
        elif k==20:
            for i,pw in enumerate([Z,Z,P,Z,Z,P]):
                r=self.post(c,password=pw)
                if pw==P and not self.success(r): raise Blocked(f'Success bước {i+1} bị khóa sớm chặn; chưa tới chuỗi sau success.')
                if pw==P: c.check(self.state()['login_attempts']==0,'success resets stored counter')
        elif k==21:
            self.lock(c); before=self.state(); a=self.post(c,password=P); b=self.post(c,email=V,password=VP)
            c.check(self.denied(a) and self.success(b) and self.state()==before,'account isolation and new HTTP client cannot bypass')
        elif k in (22,23):
            r=self.post(c,password='test1234!' if k==22 else ' Test1234! ')
            c.check(self.denied(r),'case/space P rejected'); c.check(self.state()['login_attempts']==1,'wrong credential increments by 1')
        elif k==24:
            r=self.post(c,email="' OR 1=1 --")
            c.check(self.denied(r) and r['status']<500 and not re.search('SQLITE|stack|SELECT',str(r['body'])),'no SQL bypass or SQL/stack exposure')
        elif k==25:
            self.sql('UPDATE users SET reset_token=? WHERE email=?',('FR02_PRIVATE',U))
            r=self.post(c,password=P); user=r['body'].get('user',{})
            c.check(self.success(r),'success'); c.check('password' not in user and 'reset_token' not in user,'no password/reset_token fields in response (A04)')
        elif k==26:
            raise Blocked('F1 không đạt; chưa phát hai request chồng lấn.')
        else: raise RuntimeError(k)
    def web(self,c,k):
        if k in (13,14,15):
            raise Blocked('Không có server clock/trace đủ chính xác ±1ms; chưa submit Web tại điểm biên yêu cầu.')
        context=self.browser.new_context(viewport={'width':1280,'height':900}); page=context.new_page()
        try:
            if k in (4,5,12): self.pre_n(c,{4:1,5:2,12:3}[k],lambda:self.submit(c,page))
            if k in (1,2,19):
                email,pw=(V,VP) if k==2 else ('short.fr02@example.com','Ab1!') if k==19 else (U,P)
                if k==1:
                    auth=[]
                    page.on('request',lambda req: auth.append({'path':req.url,'authorization_present':req.headers.get('authorization','').startswith('Bearer ')}) if req.url==API+'/users/me' else None)
                r=self.submit(c,page,email,pw); c.check(r['token_present'] and '/login' not in r['url'],'UI success and token stored')
                if k==1:
                    page.locator('a[href="/profile"]').click(); page.wait_for_timeout(250)
                    profile_email=page.locator('main input[disabled]').input_value()
                    c.note('profile UI and authenticated request',dict(profile_email=profile_email,requests=auth))
                    c.check(bool(auth) and all(x['authorization_present'] for x in auth),'GET me carries Bearer')
                    c.check(profile_email==U,'profile identifies U')
            elif k==3:
                r=self.submit(c,page); c.check(not r['token_present'] and r['state']['login_attempts']==1 and not r['state']['locked_until'],'0→1, no lock/token')
            elif k in (4,5,12):
                r=self.submit(c,page); c.check(r['state']['login_attempts']==(2 if k==4 else 3),'counter boundary target')
                r2=self.submit(c,page,password=P); c.check(r2['token_present'] if k==4 else not r2['token_present'],'lock boundary')
            elif k==6:
                a=self.submit(c,page); self.reset(); b=self.submit(c,page,'fr02.absent@example.com',P)
                c.check(not a['token_present'] and not b['token_present'] and a['text']==b['text'],'generic UI error for known/unknown account')
            elif k in (7,8,9,10):
                email='plainaddress' if k==7 else 'a@' if k==8 else '' if k==9 else U
                r=self.submit(c,page,email,P if k!=10 else '')
                c.check(not r['responses'] and not r['token_present'],'browser blocks submit; no login request')
                c.check(r['state']['login_attempts']==0,'counter unchanged')
                if k in (7,8): c.check(r['fields'][0]['type']=='email' and not r['fields'][0]['valid'],'HTML5 email type and format validation')
            elif k==11:
                self.lock(c); before=self.state(); r=self.submit(c,page,password=P)
                c.check(not r['token_present'] and r['responses'] and self.state()==before,'locked correct P rejected; state unchanged')
            elif k==16:
                for i,pw in enumerate([Z,Z,P,Z,Z,P]):
                    r=self.submit(c,page,password=pw)
                    if pw==P and not r['token_present']: raise Blocked(f'Success bước {i+1} bị khóa sớm, chưa tới chuỗi sau success.')
                    if pw==P:
                        c.check(self.state()['login_attempts']==0,'success resets counter')
                        context.clear_cookies(); page.evaluate('localStorage.clear()'); page.goto(WEB+'/login')
            elif k==17:
                self.lock(c); before=self.state(); r=self.submit(c,page,V,VP)
                c.check(r['token_present'] and self.state()==before,'V success while U remains locked')
            elif k==18:
                self.lock(c); self.form(page); page.reload(); a=self.submit(c,page,password=P)
                other=self.browser.new_context(viewport={'width':1280,'height':900})
                try: b=self.submit(c,other.new_page(),password=P)
                finally: other.close()
                c.check(not a['token_present'] and not b['token_present'],'reload and independent browser session cannot bypass')
            else: raise RuntimeError(k)
            if any(not x['ok'] for x in c.r['assertions']): c.shot(page,'symptom')
        finally: context.close()

def main():
    sys.stdout.reconfigure(encoding='utf-8')
    parser=argparse.ArgumentParser(); parser.add_argument('--execute',action='store_true'); parser.add_argument('--db'); parser.add_argument('--run-id'); parser.add_argument('--case',action='append')
    args=parser.parse_args(); catalogue=rows()
    if not args.execute: print('45 reviewed cases; pass --execute --db ... --run-id ... to run'); return
    db=Path(args.db).resolve(); assert db.is_file() and '.runtime' in db.parts
    assert args.run_id
    out=FEATURE/'results.json'
    data=json.loads(out.read_text(encoding='utf-8')) if out.exists() else dict(cases=catalogue,runs=[],selected_results={},supplementary=[],bugs=[])
    assert args.run_id not in [r['id'] for r in data['runs']]
    (FEATURE/'images').mkdir(exist_ok=True)
    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        browser=pw.chromium.launch(headless=True)
        run=dict(id=args.run_id,started_at=now(),timezone='Asia/Bangkok (UTC+7)',revision=subprocess.check_output(['git','rev-parse','HEAD'],cwd=REPO,text=True).strip(),
                 browser=browser.version,web=WEB,api=API,runtime_database=str(db),fixture='isolated T05 DB; reset only U/V between TC; FL direct fixture explicitly logged',
                 timestamp_precision='client wall-clock intervals, not server processing trace; exact ±1ms cases blocked',
                 hashes={f:hashlib.sha256((FEATURE/f).read_bytes()).hexdigest() for f in ['design.md','test-cases.md','scripts/run.py']})
        data['runs'].append(run); runner=Runner(db,browser)
        runner.sql('DELETE FROM users WHERE email=?',('fr02.absent@example.com',))
        if not runner.sql('SELECT id FROM users WHERE email=?',('short.fr02@example.com',)):
            runner.sql('INSERT INTO users(name,email,password,role,login_attempts) VALUES(?,?,?,?,0)',('FR02 short credential','short.fr02@example.com','Ab1!','user'))
        for row in data['cases']:
            cid=row['id']
            if args.case and cid not in args.case: continue
            c=Case(cid,args.run_id); runner.reset(); c.note('F0',runner.state())
            try:
                if '-W' in cid: runner.web(c,int(cid[-2:]))
                else: runner.api(c,int(cid[-2:]))
                c.r['status']='failed' if any(not a['ok'] for a in c.r['assertions']) else 'passed'
                c.r['reason']='; '.join(a['check'] for a in c.r['assertions'] if not a['ok']) or 'All target assertions satisfied.'
            except Blocked as e: c.r.update(status='blocked',reason=str(e))
            except Exception as e:
                c.r.update(status='blocked',reason='Harness/environment error: '+repr(e))
                c.note('interruption',repr(e))
                # Persist and stop on unexpected harness failure, rather than propagating across suite.
                c.r['ended_at']=now(); row['results'].append(c.r); data['selected_results'][cid]=args.run_id
                out.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8'); raise
            c.r['ended_at']=now(); row['results'].append(c.r); data['selected_results'][cid]=args.run_id
            out.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
            print(cid,c.r['status'],c.r['reason'],flush=True)
        runner.reset(); run['ended_at']=now(); browser.close()
    out.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
    print(Counter(c['results'][-1]['status'] for c in data['cases'] if c['results']))

if __name__=='__main__': main()
