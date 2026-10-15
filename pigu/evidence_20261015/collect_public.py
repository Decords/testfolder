"""Read public Shopify catalog and collect image evidence as an artifact only."""
import json,gzip,time,io,hashlib
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor,as_completed
import requests
from PIL import Image
OUT=Path('phh_evidence');OUT.mkdir(exist_ok=True)
PIDS=set('7347937607930 7348076904698 7717998166266 7718006882554 7718009635066 7718010159354 7718011666682 7718020841722 8568352375122 8568363680082 8568370889042 8568455692626 8609937981778 8747148968274 8747172757842 8747222958418 8747310580050 8747316773202 8747358028114 8747358355794 8747402395986 8747461411154 8755000901970 8755004866898 8755064865106 8755072827730 8755077153106 8755103531346 8755104186706 8755575947602 8755576996178 8755593019730 8755596099922 8755596099922 8755599638866 8755624149330 8755625722194 8755627491666 8755629424978 8755630670162 8755638174034 8755650036050 8755687948626 8764407284050 9295386706258 9295393653074 9295393849682 9295413346642 9295422292306 9295428125010 9295428288850 9295441953106 9295442248018 9295458009426 9295464333650 9295486845266 9302806692178 9302822846802 9302822879570 9694817386834 9745189142866 9745201791314 9745201824082 9758674485586 9780018184530 9862310363474 9869889700178 9870956822866 9870989132114 9881105563986 9881116836178 9881116868946 9881116967250 9882676887890 9882789118290 9883080720722 9883080753490 9883080819026 9883094712658 9883094745426 9887082479954 9887332663634 9887444631890 9891216884050 9894724469074 9894746390866 9905537352018 9909177909586 9909601567058 9946572849490 9946627572050 9946627604818 9946627637586 9946676298066 9946709262674 9946709328210 9946732233042 9947890418002 9952326549842 9952326582610 9957200068946 9957200101714 9957200134482 9957204492626 9957204558162 10043062124882 10043069432146 10043082834258 10043088437586 10143351210322 10143356617042 10145915437394 10145915502930 10145928446290 10145953677650 10170634600786 10300419998034 10300426682706 10542500381010 10659460088146 10659629072722 10659629171026 10659629203794'.split())
s=requests.Session();s.headers['User-Agent']='Decords-Catalog-Export/1.0'
products={};errors=[]
for page in range(1,30):
 for attempt in range(4):
  try:
   r=s.get('https://www.decords.com/products.json',params={'limit':250,'page':page},timeout=90);r.raise_for_status();batch=r.json()['products'];break
  except Exception:
   if attempt==3:raise
   time.sleep(5*(attempt+1))
 if not batch:break
 before=len(products)
 for p in batch:products[str(p['id'])]=p
 if len(products)==before:raise RuntimeError('Pagination did not advance')
 print('page',page,'products',len(products),flush=True);time.sleep(.6)
with gzip.open(OUT/'current_public_catalog.json.gz','wt',encoding='utf-8') as f:json.dump(products,f,ensure_ascii=False)
# Recover any specifically requested items absent from the public listing via exact original handles.
source=Path('pigu/full_20261012/shopify_source.jsonl.gz');handles={}
if source.exists():
 with gzip.open(source,'rt') as f:
  for line in f:
   n=json.loads(line)
   if n['id'].startswith('gid://shopify/Product/'):handles[n['id'].rsplit('/',1)[-1]]=n['handle']
for pid in PIDS-set(products):
 try:
  r=s.get('https://www.decords.com/products/'+handles[pid]+'.json',timeout=60);r.raise_for_status();products[pid]=r.json()['product']
 except Exception as e:errors.append({'product_id':pid,'error':str(e)})
with gzip.open(OUT/'current_public_catalog.json.gz','wt',encoding='utf-8') as f:json.dump(products,f,ensure_ascii=False)
tasks=[]
for pid in PIDS:
 for idx,image in enumerate(products.get(pid,{}).get('images',[])):
  tasks.append((pid,idx,image))
assets=OUT/'images';assets.mkdir(exist_ok=True)
def get_image(t):
 pid,idx,image=t;url=image['src'];row={'product_id':pid,'position':idx+1,'source_url':url,'source_image_id':image['id'],'source_width':image.get('width'),'source_height':image.get('height')}
 try:
  # Request a bounded inspection image; original URL is retained for feed and evidence.
  response=requests.get(url,params={'width':1400},timeout=45);response.raise_for_status()
  im=Image.open(io.BytesIO(response.content));im.load();im.thumbnail((1400,1400))
  path=assets/f'{pid}_{idx+1:03d}.jpg';im.convert('RGB').save(path,quality=88)
  row.update(file=str(path.relative_to(OUT)),http_status=response.status_code,inspection_width=im.width,inspection_height=im.height)
 except Exception as e:row['error']=str(e)
 return row
rows=[]
with ThreadPoolExecutor(max_workers=10) as pool:
 for i,future in enumerate(as_completed([pool.submit(get_image,t) for t in tasks]),1):
  rows.append(future.result())
  if i%100==0:print('image evidence',i,'/',len(tasks),flush=True)
(OUT/'image_index.json').write_text(json.dumps(sorted(rows,key=lambda x:(x['product_id'],x['position'])),ensure_ascii=False,indent=2))
summary={'catalog_products':len(products),'requested_products':len(PIDS),'requested_found':len(PIDS&set(products)),'gallery_image_total':sum(len(p.get('images',[])) for p in products.values()),'inspection_images':len(rows),'image_errors':sum('error' in r for r in rows),'missing_products':sorted(PIDS-set(products)),'errors':errors}
(OUT/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2));print(json.dumps(summary),flush=True)
