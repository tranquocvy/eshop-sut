"""Supplementary runtime reproductions, not additional catalogue TC or boundary credits.
Screenshots use a functioning API client harness, displaying live SUT responses and
read-only SQLite observations. They are labelled harness views, never SUT Web UI.
"""
import argparse
import json
from pathlib import Path
import time
from run import FEATURE, Runner, Case, U, P, Z, API, iso, now

CLIENT='''<!doctype html><meta charset="utf-8"><title>T05 live API client</title>
<style>body{font:17px Consolas,monospace;margin:28px;color:#14202d}h1{font:26px sans-serif}pre{white-space:pre-wrap;background:#eef3f8;padding:14px;border:1px solid #b6c5d4}small{color:#435269}button{padding:10px}textarea{width:96%;height:60px}</style>
<h1>T05 — Live API client (test harness)</h1><small>Actual HTTP response from localhost:3000; DB observer read-only. This is not the EShop Web UI. JWT redacted.</small>
<h2 id="label"></h2><textarea id="payload"></textarea><button id="send">POST /api/login</button><div id="log"></div>
<script>
document.querySelector('#send').onclick=async()=>{
const body=JSON.parse(document.querySelector('#payload').value),start=Date.now();
const r=await fetch('http://localhost:3000/api/login',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(body)});
const value=await r.json();if(value.token)value.token='[JWT present, redacted]';
const entry={request:body,status:r.status,body:value,clientIntervalMs:[start,Date.now()]};
const pre=document.createElement('pre');pre.textContent=JSON.stringify(entry,null,2);document.querySelector('#log').appendChild(pre);window.last=entry;};
</script>'''

def main():
    parser=argparse.ArgumentParser(); parser.add_argument('--db',required=True); parser.add_argument('--id',required=True); args=parser.parse_args()
    from playwright.sync_api import sync_playwright
    result_path=FEATURE/'results.json'; data=json.loads(result_path.read_text(encoding='utf-8'))
    assert args.id not in [r['id'] for r in data['supplementary']]
    record=dict(id=args.id,started_at=now(),purpose='Runtime reproductions and JPG symptoms; no additional TC or precise boundary credit',observations=[],images=[])
    data['supplementary'].append(record)
    def save(): result_path.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
    with sync_playwright() as pw:
        browser=pw.chromium.launch(); runner=Runner(Path(args.db),browser); page=browser.new_page(viewport={'width':1280,'height':1050})
        def start(label):
            page.set_content(CLIENT); page.locator('#label').evaluate('(el,text)=>el.textContent=text',label)
        def post(body,label):
            before=runner.state(); page.locator('#payload').fill(json.dumps(body)); page.evaluate('window.last=null')
            page.locator('#send').click(); page.wait_for_function('window.last!==null'); time.sleep(.08)
            r=page.evaluate('window.last'); after=runner.state(); observation=dict(at=now(),step=label,before=before,response=r,after=after)
            record['observations'].append(observation)
            page.locator('#log').evaluate('(el,value)=>{let p=document.createElement("pre");p.textContent=JSON.stringify(value,null,2);el.appendChild(p)}',dict(step=label,db_before=before,db_after=after))
            save(); return r
        def shot(bug):
            name=f'images/{bug}-{args.id}.jpg'; page.screenshot(path=str(FEATURE/name),type='jpeg',quality=88,full_page=True)
            record['images'].append(dict(path=name,captured_at=now(),bug=bug,kind='live API client harness + read-only DB observer')); save()
        # Counter/early lock: two real failures, then correct password.
        runner.reset(); start('FR02-BUG01 — counter +2; lock after two failures')
        post(dict(email=U,password=Z),'wrong #1'); post(dict(email=U,password=Z),'wrong #2')
        post(dict(email=U,password=P),'correct password immediately after two failures'); shot('FR02-BUG01')
        # Duration measured against real triggering request bracket, independent of incorrect threshold.
        runner.reset(); start('FR02-BUG02 — configured lock interval and actual denial after 31 seconds')
        post(dict(email=U,password=Z),'wrong #1'); trigger=post(dict(email=U,password=Z),'wrong #2 triggers actual lock')
        state=runner.state(); locked_ms=__import__('datetime').datetime.fromisoformat(state['locked_until'].replace('Z','+00:00')).timestamp()*1000
        lo,hi=trigger['clientIntervalMs']; observation=dict(step='duration bounds from triggering request and stored deadline',at=now(),seconds_bounds=[(locked_ms-hi)/1000,(locked_ms-lo)/1000],trigger_interval_ms=[lo,hi],locked_until=state['locked_until'])
        record['observations'].append(observation); save(); print(json.dumps(observation),flush=True)
        time.sleep(31)
        late=post(dict(email=U,password=P),'correct P after real 31-second wait')
        record['observations'].append(dict(step='elapsed since trigger bracket',at=now(),seconds_bounds=[(late['clientIntervalMs'][0]-hi)/1000,(late['clientIntervalMs'][1]-lo)/1000]))
        shot('FR02-BUG02')
        runner.reset(); start('FR02-BUG04 — missing password mutates account counter (A02)')
        post(dict(email=U),'missing password'); shot('FR02-BUG04')
        runner.reset(); runner.sql('UPDATE users SET reset_token=? WHERE email=?',('FR02_PRIVATE',U))
        start('FR02-BUG05 — sensitive credential fields returned (A04)')
        post(dict(email=U,password=P),'successful login'); shot('FR02-BUG05')
        runner.reset(); runner.sql('UPDATE users SET login_attempts=3,locked_until=? WHERE email=?',(iso(time.time()*1000-1000),U))
        start('FR02-BUG06 — expired lock counter reused (A01; direct expired FL fixture)')
        post(dict(email=U,password=Z),'first wrong attempt after expired FL'); shot('FR02-BUG06')
        runner.reset(); record['ended_at']=now(); save(); browser.close()

if __name__=='__main__': main()
