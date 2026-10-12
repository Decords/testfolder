from phh_common import *
from urllib.parse import urlsplit

def load_products():
 products={};pending=[]
 with gzip.open(BASE/'shopify_source.jsonl.gz','rt') as f:
  for line in f:
   n=json.loads(line)
   if n['id'].startswith('gid://shopify/Product/'):
    n['_variants']=[];n['_images']=[];products[n['id']]=n
   else:pending.append(n)
 for n in pending:
  p=products.get(n.get('__parentId'))
  if p is None:continue
  if n['id'].startswith('gid://shopify/ProductVariant/'):p['_variants'].append(n)
  elif n.get('image'):p['_images'].append(n)
 return products

def family(p):
 t=(p.get('productType','')+' '+(p.get('category') or {}).get('fullName','')).lower()
 if 'window film' in t:return 'film'
 if 'mask' in t or 'costume' in t:return 'mask'
 if any(x in t for x in ['poster','canvas print','shooting target','printed flyer','sublimation','iron-on','transfer paper']):return 'paper'
 if any(x in t for x in ['decal','sticker','wallpaper','mural','label','vehicle wrap','chrome vinyl','sign']):return 'decal'
 return '3d'

def category(p):
 c=p.get('category') or {};cid=c.get('id','').rsplit('/',1)[-1]
 if cid=='hg-3-38':return '1001','Baldai ir namų interjeras / Namų interjeras / Interjero lipdukai'
 return 'SH-'+cid if cid else 'SH-other',c.get('fullName') or p.get('productType') or 'Other physical products'

def images(p):
 out=[];seen=set();bad=re.compile(r'color chart|colour chart|size chart|installation|instruction|paint compatibility|sizing guide',re.I)
 eligible=[m['image'] for m in p['_images'] if m.get('image') and min(m['image'].get('width') or 0,m['image'].get('height') or 0)>=1000]
 eligible.sort(key=lambda i:bool(bad.search(i.get('altText') or '')))
 for i in eligible:
  u=i.get('url','');path=urlsplit(u).path.lower()
  if not u.startswith('https://') or not path.endswith(('.jpg','.jpeg','.png')) or path in seen:continue
  seen.add(path);out.append(u)
  if len(out)==5:break
 return out

def old_codes():
 result={};root=BASE.parent
 for name in ['generated/PiguProducts-master.xml','PiguProducts-batch-001.xml','test_20260923/PHH_TEST_TUNNEL_MONSTERA_10_CARDS_20260923.xml']:
  path=root/name
  if not path.exists():continue
  for m in etree.parse(str(path)).findall('.//modification'):
   e=m.findtext('attributes/barcodes/barcode');s=m.findtext('attributes/supplier-code')
   if e and s:result[e]=s
 return result

def extra(v):
 return ' / '.join(convert_units(o['value']) for o in v.get('selectedOptions',[]) if not SIZE_NAMES.search(o.get('name','')) and o.get('value') and o['value'].lower() not in ('default title','default'))
