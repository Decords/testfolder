"""Read public catalog export and collect image evidence into an Actions artifact.
No Shopify products, marketplace settings or published feed paths are modified.
"""
import collections,gzip,hashlib,io,json,math,re,time
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor,as_completed
from urllib.parse import urlsplit,urlunsplit,parse_qsl,urlencode
import requests
from PIL import Image,ImageOps,ImageDraw,ImageFont
BASE=Path('pigu/staging_20261015');OUT=Path('phh_gallery_evidence');OUT.mkdir(exist_ok=True)
IDS='7347937607930 7348076904698 7717998166266 7718006882554 7718009635066 7718010159354 7718011666682 7718020841722 8568352375122 8568363680082 8568370889042 8568455692626 8609937981778 8747148968274 8747172757842 8747222958418 8747310580050 8747316773202 8747358028114 8747358355794 8747402395986 8747461411154 8755000901970 8755004866898 8755064865106 8755072827730 8755077153106 8755103531346 8755104186706 8755575947602 8755576996178 8755593019730 8755596099922 8755599638866 8755599638866 8755624149330 8755625722194 8755627491666 8755629424978 8755630670162 8755638174034 8755650036050 8755687948626 8764407284050 9295386706258 9295393653074 9295393849682 9295413346642 9295422292306 9295428125010 9295428288850 9295441953106 9295442248018 9295458009426 9295464333650 9295486845266 9302806692178 9302822846802 9302822879570 9694817386834 9745189142866 9745201791314 9745201824082 9758674485586 9780018184530 9862310363474 9869889700178 9870956822866 9870989132114 9881105563986 9881116836178 9881116868946 9881116967250 9882676887890 9882789118290 9883080720722 9883080753490 9883080819026 9883094712658 9883094745426 9887082479954 9887332663634 9887444631890 9891216884050 9894724469074 9894746390866 9905537352018 9909177909586 9909601567058 9946572849490 9946627572050 9946627604818 9946627637586 9946676298066 9946709262674 9946709328210 9946732233042 9947890418002 9952326549842 9952326582610 9957200068946 9957200101714 9957200134482 9957204492626 9957204558162 10043062124882 10043069432146 10043082834258 10043088437586 10143351210322 10143356617042 10145915437394 10145915502930 10145928446290 10145953677650 10145953677650 10170634600786 10300419998034 10300426682706 10542500381010 10659460088146 10659629072722 10659629171026 10659629203794'.split();IDS=list(dict.fromkeys(IDS))
url=(BASE/'public_source_url.txt').read_text().strip()
r=requests.get(url,timeout=180);r.raise_for_status();raw=r.content
with gzip.open(OUT/'current_public_source.jsonl.gz','wb') as f:f.write(raw)
ps={};pending=[]
for line in raw.splitlines():
 n=json.loads(line)
 if n['id'].startswith('gid://shopify/Product/'):
  n['_media']=[];ps[n['id'].rsplit('/',1)[-1]]=n
 else:pending.append(n)
for n in pending:
 p=ps.get(n.get('__parentId','').rsplit('/',1)[-1])
 if p is not None:p['_media'].append(n)
images=[]
for pid in IDS:
 p=ps.get(pid)
 if not p:continue
 for i,m in enumerate(p['_media'],1):
  if m.get('image'):images.append((pid,i,m['image']))
asset=OUT/'previews';asset.mkdir(exist_ok=True)
def download(item):
 pid,pos,im=item;u=im['url'];s=urlsplit(u);q=dict(parse_qsl(s.query));q['width']='1000';q['format']='jpg';preview=urlunsplit((s.scheme,s.netloc,s.path,urlencode(q),''));dest=asset/f'{pid}_{pos:02}.jpg'
 info={'product_id':pid,'position':pos,'source_url':u,'source_width':im['width'],'source_height':im['height'],'local_file':str(dest.relative_to(OUT))}
 for attempt in range(2):
  try:
   response=requests.get(preview,timeout=25,headers={'Accept':'image/jpeg,image/png'},allow_redirects=False)
   info.update(http_status=response.status_code,content_type=response.headers.get('Content-Type'),bytes=len(response.content))
   response.raise_for_status();assert response.status_code==200
   image=Image.open(io.BytesIO(response.content)).convert('RGB');image.save(dest,'JPEG',quality=92)
   info.update(width=image.width,height=image.height);return info
  except Exception as e:
   info['error']=str(e)
   if attempt==0:time.sleep(1)
 return info
checks=[]
with ThreadPoolExecutor(max_workers=12) as pool:
 for i,result in enumerate(pool.map(download,images),1):
  checks.append(result)
  if i%100==0:print('Image previews',i,'of',len(images),flush=True)
(OUT/'preview_checks.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2))
sheets=OUT/'contact_sheets';sheets.mkdir(exist_ok=True)
try:font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',17)
except Exception:font=ImageFont.load_default()
for ix,pid in enumerate(IDS,1):
 group=[c for c in checks if c['product_id']==pid];cols=4;cw=350;ch=375
 sheet=Image.new('RGB',(cols*cw,65+ch*math.ceil(len(group)/cols)), 'white');draw=ImageDraw.Draw(sheet)
 draw.text((8,6),f'{ix}. Shopify {pid}',font=font,fill='black');draw.text((8,30),ps[pid]['title'][:120],font=font,fill='black')
 for j,c in enumerate(group):
  x=(j%cols)*cw;y=65+(j//cols)*ch;f=OUT/c['local_file']
  if f.exists():
   image=Image.open(f);image.thumbnail((cw-8,ch-30));sheet.paste(image,(x+(cw-image.width)//2,y))
  draw.text((x+5,y+ch-26),str(c['position'])+': '+str(c.get('source_width'))+' x '+str(c.get('source_height')),font=font,fill='black')
 sheet.save(sheets/f'{ix:03}_{pid}.jpg',quality=90)
summary={'source_products':len(ps),'source_media':sum(len(p['_media']) for p in ps.values()),'problem_products':len(IDS),'preview_count':len(checks),'preview_success':sum('error' not in c for c in checks),'source_bytes':len(raw),'source_sha256':hashlib.sha256(raw).hexdigest(),'production_changes':False}
(OUT/'summary.json').write_text(json.dumps(summary,indent=2));print(json.dumps(summary))
