from phh_common import *
from phh_source import load_products,family,category,images,old_codes,extra
from phh_choose import choose

def select():
 ps=load_products();records=[];excluded=[];rejections=collections.Counter();previous=old_codes();used_eans=set();used_codes=set()
 for p in ps.values():
  fam=family(p);cid,cname=category(p);ims=images(p);reason=''
  if p['productType'] in ('Shipping Upgrade','Product Customization Service'):reason='service_or_shipping_upgrade'
  elif not ims:reason='no_eligible_image'
  valid=[];local_eans=set()
  for v in p['_variants']:
   e=str(v.get('barcode') or '').strip()
   if not valid_ean(e):rejections['missing_or_invalid_ean']+=1;continue
   if e in local_eans:rejections['duplicate_ean_within_source_product']+=1;continue
   if not v['inventoryItem'].get('requiresShipping',True):rejections['non_physical_variant']+=1;continue
   if not all(v.get(c,{}).get('price',{}).get('currencyCode')=='EUR' and Decimal(v[c]['price']['amount'])>0 for c in COUNTRIES):rejections['missing_country_eur_price']+=1;continue
   size=parse_size(v,p)
   if cid=='1001' and not size:rejections['required_decal_dimensions_not_found']+=1;continue
   local_eans.add(e);valid.append({'v':v,'ean':e,'size':size,'extra':extra(v)})
  has_ean=any(valid_ean(v.get('barcode')) for v in p['_variants'])
  if not valid and not reason:reason='missing_ean' if not has_ean else 'missing_required_dimensions'
  if reason:
   excluded.append({'source_product_id':p['id'].rsplit('/',1)[-1],'title':p['title'],'product_type':p['productType'],'reason':reason,'has_any_ean':has_ean});continue
  selected=choose(valid,fam)
  for c in selected:
   e=c['ean'];vid=c['v']['id'].rsplit('/',1)[-1]
   assert e not in used_eans,'Cross-product duplicate EAN '+e
   sku=previous.get(e) or str(c['v'].get('sku') or '').strip() or 'PHH-'+vid
   if sku in used_codes:sku='PHH-'+vid
   assert sku not in used_codes
   used_eans.add(e);used_codes.add(sku);c['sku']=sku
  records.append({'p':p,'family':fam,'category_id':cid,'category_name':cname,'images':ims,'variants':selected})
 audit={'source_products':len(ps),'source_variants':sum(len(p['_variants']) for p in ps.values()),'selected_products':len(records),'selected_variants':sum(len(r['variants']) for r in records),'excluded_products':len(excluded),'excluded_reasons':dict(collections.Counter(e['reason'] for e in excluded)),'variant_rejections':dict(rejections),'max_variants_per_product':max(len(r['variants']) for r in records),'stock':999,'collection_hours':120}
 (BASE/'selection_audit.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2))
 (BASE/'excluded_products.json').write_text(json.dumps(excluded,ensure_ascii=False,indent=2))
 print(json.dumps(audit,ensure_ascii=False),flush=True)
 return records,audit
