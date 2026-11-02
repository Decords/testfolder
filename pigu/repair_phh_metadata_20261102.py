#!/usr/bin/env python3
"""Repair PHH feed metadata without changing EANs, supplier codes, photos, prices or packages.
This script is intentionally conservative: it cannot invent product attributes or physical sizes.
"""
from collections import Counter,defaultdict
from decimal import Decimal
from pathlib import Path
from lxml import etree
import argparse,datetime,hashlib,json,re

CONTENT=Path('pigu/PHH_PRODUCTS.xml')
OFFERS=Path('pigu/PHH_STOCK_PRICES.xml')
REPORT=Path('pigu/PHH_REPAIR_REPORT_20261102.json')
EXPECTED_GIT_BLOB='75027284388b4da5c33dc9f11a2056c74c5caf31'
FI_FIVE=('6012940535553','6012937279279','6012927578580','7341146629643','7341146630687')
BRAND='Decords'
PACKAGE={'weight':Decimal('.5'),'length':Decimal('.60'),'height':Decimal('.06'),'width':Decimal('.06')}
SIZE=re.compile(r'(?<!\d)(\d{1,4}(?:[.,]\d+)?)\s*[×xXхХ]\s*(\d{1,4}(?:[.,]\d+)?)\s*(?:cm|см)\b',re.I)
def gitblob(b):
 return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
def xtext(p,name):
 return (p.findtext(name) or '').strip()
def cdata(p,name,value):
 e=etree.SubElement(p,name);e.text=etree.CDATA(str(value));return e
def property_value(props,key):
 if props is None:return None
 for p in props.findall('property'):
  if xtext(p,'id')==key:
   return (p.findtext('./values/value') or '').strip()
 return None
def add_prop(props,key,value):
 p=etree.SubElement(props,'property')
 cdata(p,'id',key)
 vs=etree.SubElement(p,'values')
 cdata(vs,'value',value)
def material(p,category):
 title=xtext(p,'title')
 words=title.lower()
 if category=='1001':return 'Vinilas','interior decals are vinyl'
 if 'petg' in words:return 'PETG','material explicit in title'
 if re.search(r'\bpla\b',words):return 'PLA','material explicit in title'
 if 'vinil' in words:return 'Vinilas','material explicit in title'
 if 'drob' in words:return 'Drobė','canvas explicitly identified'
 if 'popier' in words:return 'Popierius','paper explicitly identified'
 if category=='SH-hg-3-4-2':return 'Drobė','Shopify category is canvas artwork'
 if category=='SH-hg-3-4-2-1':return 'Popierius','Shopify category is posters'
 return None,None
def art_size(p):
 m=SIZE.search(xtext(p,'title'))
 if m:
  a=Decimal(m.group(1).replace(',','.'))
  b=Decimal(m.group(2).replace(',','.'))
  if 1<=a<=1500 and 1<=b<=1500:return str(a.normalize()),str(b.normalize())
 return None
def identifiers(root):
 result=[]
 for p in root.findall('product'):
  for m in p.findall('./colours/colour/modifications/modification'):
   result.append(((m.findtext('./attributes/barcodes/barcode') or '').strip(),(m.findtext('./attributes/supplier-code') or '').strip()))
 return result
def main():
 ap=argparse.ArgumentParser()
 ap.add_argument('--apply',action='store_true')
 args=ap.parse_args()
 raw=CONTENT.read_bytes()
 old_sha=gitblob(raw)
 if old_sha!=EXPECTED_GIT_BLOB:
  raise RuntimeError('Live feed changed since last audit: expected '+EXPECTED_GIT_BLOB+' got '+old_sha+'. Do not overwrite.')
 offers_sha=hashlib.sha256(OFFERS.read_bytes()).hexdigest()
 parser=etree.XMLParser(strip_cdata=False,resolve_entities=False,no_network=True,huge_tree=True)
 tree=etree.fromstring(raw,parser)
 if tree.tag!='products':raise RuntimeError('Bad root')
 old_ids=identifiers(tree)
 if len(old_ids)!=11892 or len(set(old_ids))!=len(old_ids):raise RuntimeError('Unexpected EAN/SKU inventory')
 counts=Counter();by_category=defaultdict(Counter);remaining=Counter();materials=Counter()
 for product in tree.findall('product'):
  cat=xtext(product,'category-id')
  ean=xtext(product,'.//modification/attributes/barcodes/barcode')
  for tag in ('manufacturer-name','manufacturer-address','manufacturer-email'):
   if not xtext(product,tag):
    raise RuntimeError('Unknown manufacturer for EAN '+ean+', refusing to invent')
  if cat=='1001':
   for field in ('Plotis','Aukštis','Raštai'):
    if not property_value(product.find('properties'),field):
     raise RuntimeError('Missing essential wall decal '+field+' EAN '+ean)
  modifications=product.findall('./colours/colour/modifications/modification')
  if len(modifications)!=1:raise RuntimeError('Unexpected modification count '+ean)
  mod=modifications[0]
  for fld,val in PACKAGE.items():
   current=Decimal(xtext(mod,fld))
   if current!=val:
    raise RuntimeError('Package differs from previously approved default for '+ean+': '+fld+' '+str(current)+', refused automatic overwrite')
  counts['approved_packages_unchanged']+=1
  props=product.find('properties')
  if props is None:
   colours=product.find('colours')
   if colours is None:raise RuntimeError('No colours for '+ean)
   props=etree.Element('properties')
   product.insert(list(product).index(colours),props)
   counts['new_properties_blocks']+=1
  if property_value(props,'Prekės ženklas') is None:
   add_prop(props,'Prekės ženklas',BRAND)
   counts['brand_added']+=1;by_category[cat]['brand']+=1
  if not property_value(props,'Medžiaga'):
   value,why=material(product,cat)
   if value:
    add_prop(props,'Medžiaga',value)
    counts['material_added']+=1;materials[value]+=1;by_category[cat]['material']+=1
   else:remaining[cat]+=1
  dimensions=art_size(product)
  if dimensions:
   for field,val in (('Plotis',dimensions[0]),('Aukštis',dimensions[1])):
    if not property_value(props,field):
     add_prop(props,field,val)
     counts['artwork_dimension_added']+=1;by_category[cat]['dimension']+=1
  counts['products']+=1
 new_ids=identifiers(tree)
 if new_ids!=old_ids:raise RuntimeError('EANs or supplier codes changed')
 out=etree.tostring(tree,encoding='UTF-8',xml_declaration=True,standalone=True,pretty_print=False)
 if len(out)>=100_000_000:raise RuntimeError('GitHub individual file size would exceed limit')
 if out.count(b'<![CDATA[')<raw.count(b'<![CDATA[')+2*sum(v for k,v in counts.items() if k in ('brand_added','material_added','artwork_dimension_added')):
  raise RuntimeError('CDATA protection lost')
 validate=etree.fromstring(out,etree.XMLParser(strip_cdata=False,resolve_entities=False,no_network=True,huge_tree=True))
 if identifiers(validate)!=old_ids:raise RuntimeError('Validation lost identifiers')
 if hashlib.sha256(OFFERS.read_bytes()).hexdigest()!=offers_sha:raise RuntimeError('Price file changed during run')
 report={
  'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
  'source_git_blob_sha':old_sha,'source_content_sha256':hashlib.sha256(raw).hexdigest(),
  'updated_content_sha256':hashlib.sha256(out).hexdigest(),
  'published_products':len(old_ids),'action_counts':dict(counts),
  'materials_added':dict(materials),
  'remaining_without_supported_material_by_category':dict(remaining),
  'edited_categories':{k:dict(v) for k,v in by_category.items()},
  'manufacturer_name_preserved':'AnOL OÜ',
  'brand_value':BRAND,'packaging_cm_kg':[60,6,6,.5],
  'barcodes_unchanged':True,'supplier_codes_unchanged':True,'product_count_unchanged':True,
  'photo_urls_unchanged':True,'category_mappings_unchanged':True,
  'offers_sha256_unchanged':offers_sha,
  'historic_suspended_fi_missing_from_feed':list(FI_FIVE),
  'limitations':[
    'Exact PHH mandatory fields and accepted values for each category require the Categories fields and values file from PMP.',
    'All package values were already set to 60x6x6cm and 0.5kg. Nonstandard articles require measured dimensions.',
    'Not found EANs can only be created by PHH product content import; stock/price import does not create products.',
    'Existing Hidden listings may require a content refresh/review by PHH support.',
    'Not all Shopify active products are present in the feed. No EANs or new SKUs were invented.'
  ]}
 REPORT.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
 if args.apply:CONTENT.write_bytes(out)
 print('SOURCE',old_sha,'UPDATED_SHA256',report['updated_content_sha256'],'APPLIED',args.apply)
 print('COUNTS',json.dumps(counts,ensure_ascii=False))
 print('MATERIALS',json.dumps(materials,ensure_ascii=False),'REMAINING',sum(remaining.values()))
 print('PACKAGE', '60 x 6 x 6 cm, 0.5 kg for',counts['approved_packages_unchanged'],'products; unchanged')
 print('UNIQUE_IDENTIFIERS',len(old_ids),'PRICES_SHA256',offers_sha)
if __name__=='__main__':main()
