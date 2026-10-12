from phh_common import *

def validate(xml,offers,registry,records,audit):
 a=etree.fromstring(xml);b=etree.fromstring(offers)
 eans=a.xpath('//modification/attributes/barcodes/barcode/text()')
 codes=a.xpath('//modification/attributes/supplier-code/text()')
 assert len(eans)==len(set(eans))==len(codes)==len(set(codes))==len(registry)
 assert all(len(p.findall('.//modification'))==1 for p in a)
 assert set(eans)==set(b.xpath('product/ean/text()')) and set(codes)==set(b.xpath('product/sku/text()'))
 assert all(valid_ean(e) for e in eans)
 assert max(collections.Counter(r['product_id'] for r in registry).values())<=5
 for p in a:
  for lang in LANGS:
   title=p.findtext('title'+SUFFIX[lang]);desc=p.findtext('long-description'+SUFFIX[lang])
   assert title and desc
   assert 'decords' not in title.lower()
  for field in ('weight','length','height','width'):
   assert Decimal(p.findtext('.//modification/'+field))>0
  if p.findtext('category-id')=='1001':
   for field in ('Aukštis','Plotis','Raštai'):assert p.findtext(f"properties/property[id='{field}']/values/value")
 categories={r['category_id']:{'id':r['category_id'],'name':r['category_name']} for r in records if r['category_id']!='1001'}
 audit.update({'content_bytes':len(xml),'offers_bytes':len(offers),'content_sha256':hashlib.sha256(xml).hexdigest(),'offers_sha256':hashlib.sha256(offers).hexdigest(),'ean_duplicates':0,'supplier_code_duplicates':0,'product_offer_identifiers_match':True,'separate_card_per_selected_variant':True,'five_language_content_present':True,'fits_shopify_20MB_limit':len(xml)<=20000000,'xsd_validation':'not performed: official XSD unavailable','phh_import_status':'not verified','package_values':'calculated estimates, not warehouse measurements','categories_requiring_mapping':list(categories.values())})
 assert len(xml)<100000000,'Content exceeds individual GitHub file limit'
 return audit
