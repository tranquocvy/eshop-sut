"""Prepare only product fixtures in an explicitly selected .runtime database.

This is setup outside TC actions. It neither starts SUT nor clears cart/users.
The live backend must already be serving this database on localhost:3000.
"""
import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import sqlite3
from urllib.request import urlopen

PRODUCTS=[('P','iPhone 15 Pro Max',30000000),('Q','Samsung Galaxy S24 Ultra',28000000),
          ('M','MacBook Pro M3',45000000),('H','Tai nghe AirPods Pro 2',6000000),
          ('K','Bàn phím cơ Keychron Q1',4000000),
          ('X','T04 <b>Hàng thử</b> tên dài tiếng Việt',125000),
          ('Y','T04 <b>Hàng thử</b> tên dài tiếng Việt',275000)]


def main():
    p=argparse.ArgumentParser(); p.add_argument('--database',required=True,type=Path); p.add_argument('--output-dir',required=True,type=Path)
    args=p.parse_args(); dbpath=args.database.resolve(); out=args.output_dir.resolve()
    repo=Path(__file__).resolve().parents[4]
    if not dbpath.is_file() or '.runtime' not in dbpath.parts or dbpath.is_relative_to(repo):
        raise SystemExit('Only an existing external .runtime database is allowed; repository database refused.')
    if '.runtime' not in out.parts or out.is_relative_to(repo): raise SystemExit('Output must be outside repo in .runtime.')
    out.mkdir(parents=True,exist_ok=True)
    if (out/'services.json').exists(): raise SystemExit('Manifest exists: preserve it; use a new setup output directory.')
    stamp=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ'); backup=out/('before-fixture-'+stamp+'.sqlite')
    fixtures={}
    with sqlite3.connect(dbpath) as db:
        with sqlite3.connect(backup) as copy: db.backup(copy)
        category=db.execute('SELECT id FROM categories ORDER BY id LIMIT 1').fetchone()
        if not category: raise SystemExit('Need an existing category; no category changes are made.')
        for key,name,price in PRODUCTS:
            row=db.execute('SELECT id,name,price FROM products WHERE name=? AND price=?',(name,price)).fetchone()
            if not row:
                db.execute('INSERT INTO products(name,price,description,imageUrl,category_id) VALUES (?,?,?,?,?)',
                           (name,price,'T04 controlled product fixture','https://placehold.co/300x300/png?text=T04',category[0]))
                row=db.execute('SELECT id,name,price FROM products WHERE id=last_insert_rowid()').fetchone()
            fixtures[key]=dict(zip(('id','name','price'),row))
    remote=json.load(urlopen('http://localhost:3000/api/products',timeout=15))
    if not all(any(all(r[k]==x[k] for k in ('id','name','price')) for r in remote) for x in fixtures.values()):
        raise SystemExit('GET products does not match prepared DB; no manifest written. Keep backup and diagnose service/database selection.')
    manifest=dict(runtime_database=str(dbpath),fixture_backup=str(backup),products=fixtures,
                  backend_source='Existing unchanged backend reused; no restart/reset by fixture script')
    (out/'services.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('Fixture ready:',out/'services.json')


if __name__=='__main__': main()
