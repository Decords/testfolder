from phh_common import *
from phh_card import card
from phh_validate import validate

def render(records,cache,audit):
 root=etree.Element('products');offers=etree.Element('products');registry=[]
 for r in records:
  p=r['p']
  for c in r['variants']:
   v=c['v'];pack=card(root,r,c,cache)
   offer=etree.SubElement(offers,'product');text(offer,'sku',c['sku']);text(offer,'ean',c['ean']);prices={}
   for country in COUNTRIES:
    price=str(Decimal(v[country]['price']['amount']).quantize(Decimal('1'),rounding=ROUND_HALF_UP))
    assert Decimal(price)>0
    prices[country]=price;etree.SubElement(offer,'price_'+country).text=price
   etree.SubElement(offer,'stock').text='999'
   for country in COUNTRIES:etree.SubElement(offer,'collection_hours_'+country).text='120'
   registry.append({'product_id':p['id'].rsplit('/',1)[-1],'variant_id':v['id'].rsplit('/',1)[-1],'source_title':p['title'],'source_variant_title':v['title'],'ean':c['ean'],'supplier_code':c['sku'],'category_id':r['category_id'],'category_name':r['category_name'],'dimensions_cm':c['size'],'prices_eur':prices,'packaging':pack,'image_count':len(r['images'])})
 xml=etree.tostring(root,encoding='UTF-8',xml_declaration=True,standalone=True,pretty_print=False)
 price_xml=etree.tostring(offers,encoding='UTF-8',xml_declaration=True,standalone=True,pretty_print=False)
 audit=validate(xml,price_xml,registry,records,audit)
 (BASE/'PHH_PRODUCTS_FULL.xml').write_bytes(xml)
 (BASE/'PHH_STOCK_PRICES.xml').write_bytes(price_xml)
 (BASE/'variant_registry.json').write_text(json.dumps(registry,ensure_ascii=False,indent=2))
 fields=['product_id','variant_id','source_title','source_variant_title','ean','supplier_code','category_id','category_name','price_lt','price_lv','price_ee','price_fi','stock','collection_hours','package_basis']
 with (BASE/'variant_registry.csv').open('w',newline='',encoding='utf-8-sig') as f:
  writer=csv.DictWriter(f,fieldnames=fields);writer.writeheader()
  for row in registry:
   writer.writerow({**{k:row[k] for k in fields if k in row},**{'price_'+c:row['prices_eur'][c] for c in COUNTRIES},'stock':999,'collection_hours':120,'package_basis':row['packaging']['basis']})
 (BASE/'build_audit.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2))
 print('FEEDS_BUILT',len(registry),'cards;',len(xml),'content bytes;',len(price_xml),'offer bytes',flush=True)
