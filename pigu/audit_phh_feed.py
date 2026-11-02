#!/usr/bin/env python3
"""PHH XML read-only diagnostic. Does not modify production feeds."""
from collections import Counter, defaultdict
from decimal import Decimal, InvalidOperation
from pathlib import Path
import argparse, datetime, json, re, xml.etree.ElementTree as ET

LANGS=('', '-ru', '-lv', '-ee', '-fi')
FI_TARGETS=('6012940535553','6012937279279','6012927578580','7341146629643','7341146630687')
HIDDEN_SAMPLES=('7341147052006','4903773107661','4903773107692','4903773107715','4903773119718','6012927095087','6012927426423')
TARGETS=set(FI_TARGETS+HIDDEN_SAMPLES)
REQ=('category-id','category-name','manufacturer-name','manufacturer-address','manufacturer-email')
METER=('weight','length','height','width')
def text(n,k):return ((n.findtext(k) or '').strip() if n is not None else '')
def number(s):
    try:return Decimal(s)
    except (InvalidOperation,ValueError):return None
def ean_ok(e):
    if not re.fullmatch(r'\d{11,13}',e):return False
    if len(e)==11:return True
    x=list(map(int,e))
    return (sum(v*(3 if i%2==0 else 1) for i,v in enumerate(reversed(x[:-1])))+x[-1])%10==0
def read_products(filename):
    with Path(filename).open('rb') as f:
        it=ET.iterparse(f,events=('start','end'))
        _,root=next(it)
        if root.tag!='products':raise ValueError('Unexpected root: '+root.tag)
        for event,node in it:
            if event=='end' and node.tag=='product':
                yield node
                root.clear()
def main():
    p=argparse.ArgumentParser()
    p.add_argument('content');p.add_argument('offers');p.add_argument('--json')
    a=p.parse_args()
    c=Counter(); samples=defaultdict(list)
    eans=Counter();skus=Counter();brands=Counter();category=Counter();packs=Counter()
    n=0; mods=0; fi_products={}; fi_offers={};targeted_products={};targeted_offers={};offer_stocks={}
    def issue(k,ean):
        c[k]+=1
        if len(samples[k])<8:samples[k].append(ean)
    for product in read_products(a.content):
        n+=1
        cat=text(product,'category-id')
        category[(cat,text(product,'category-name'))]+=1
        for f in REQ:
            if not text(product,f):issue('missing_'+f,'product-'+str(n))
        brands[(text(product,'manufacturer-name') or '(EMPTY)',text(product,'manufacturer-address'),text(product,'manufacturer-email'))]+=1
        for suf in LANGS:
            if not text(product,'title'+suf):issue('missing_title'+suf,'product-'+str(n))
            if not text(product,'long-description'+suf):issue('missing_description'+suf,'product-'+str(n))
        images=product.findall('./colours/colour/images/image/url')
        if not any((x.text or '').startswith('https://') for x in images):issue('missing_https_image','product-'+str(n))
        if cat=='1001':
            props={}
            for x in product.findall('./properties/property'):
                props[text(x,'id')]=[v.text for v in x.findall('./values/value') if v.text and v.text.strip()]
            for f in ('Aukštis','Plotis','Raštai'):
                if not props.get(f):issue('missing_wall_attribute_'+f,'product-'+str(n))
        modifications=product.findall('./colours/colour/modifications/modification')
        if not modifications:issue('missing_modifications','product-'+str(n))
        for m in modifications:
            mods+=1
            e=text(m.find('./attributes/barcodes'),'barcode')
            s=text(m.find('./attributes'),'supplier-code')
            if e in TARGETS:targeted_products[e]={'product_title':text(product,'title'),'category_id':cat,'package_m_kg':{k:text(m,k) for k in METER}}
            if e:eans[e]+=1
            else:issue('missing_ean','product-'+str(n))
            if s:skus[s]+=1
            else:issue('missing_supplier_code',e)
            if e and not ean_ok(e):issue('invalid_ean',e)
            values=[]
            for f in METER:
                v=number(text(m,f))
                if v is None or v<=0:issue('missing_or_invalid_'+f,e)
                values.append(v)
            if all(v is not None and v>0 for v in values):
                w,l,h,b=values
                packs[(str(l*100),str(h*100),str(b*100),str(w))]+=1
        if len(modifications)>1 and any(not text(m,'modification-title') for m in modifications):
            issue('missing_multi_modification_title','product-'+str(n))
    pe=Counter();ps=Counter();pn=0
    for o in read_products(a.offers):
        pn+=1
        e=text(o,'ean');s=text(o,'sku')
        if e:
            pe[e]+=1
            offer_stocks[e]=text(o,'stock')
        else:issue('offer_missing_ean','offer-'+str(pn))
        if e in TARGETS:targeted_offers[e]={'stock':text(o,'stock'),'price_fi':text(o,'price_fi'),'collection_hours_fi':text(o,'collection_hours_fi')}
        if s:ps[s]+=1
        else:issue('offer_missing_sku',e)
        if number(text(o,'stock')) is None:issue('offer_missing_stock',e)
    co=set(eans);po=set(pe)
    report={
       'date_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
       'live_content_bytes':Path(a.content).stat().st_size,
       'live_stock_prices_bytes':Path(a.offers).stat().st_size,
       'products':n,'modifications':mods,'price_stock_offers':pn,
       'unique_product_eans':len(co),'unique_offer_eans':len(po),
       'issues_count':dict(c),'issues_examples':dict(samples),
       'manufacturer_profiles':[{'name':k[0],'address':k[1],'email':k[2],'count':v} for k,v in brands.most_common(15)],
       'ean_duplicate_count':sum(v>1 for v in eans.values()),
       'ean_duplicate_examples':[k for k,v in eans.items() if v>1][:12],
       'supplier_code_duplicate_count':sum(v>1 for v in skus.values()),
       'supplier_code_duplicate_examples':[k for k,v in skus.items() if v>1][:12],
       'content_eans_absent_in_stock_prices_count':len(co-po),
       'content_eans_absent_in_stock_prices_examples':sorted(co-po)[:12],
       'stock_price_eans_absent_in_content_count':len(po-co),
       'stock_price_eans_absent_in_content_examples':sorted(po-co)[:12],
       'most_common_packaging':[{'length_cm':k[0],'height_cm':k[1],'width_cm':k[2],'weight_kg':k[3],'count':v} for k,v in packs.most_common(25)],
       'unique_packaging_combinations':len(packs),
       'top_categories':[{'id':k[0],'name':k[1],'count':v} for k,v in category.most_common(25)],
       'historical_suspended_fi_five':[{'ean':e,'in_live_products':e in targeted_products,'in_live_stock_prices':e in targeted_offers,'product':targeted_products.get(e),'offer':targeted_offers.get(e)} for e in FI_TARGETS],
       'historical_hidden_samples':[{'ean':e,'in_live_products':e in targeted_products,'in_live_stock_prices':e in targeted_offers,'product':targeted_products.get(e),'offer':targeted_offers.get(e)} for e in HIDDEN_SAMPLES],
       'extra_stock_offer_counts_by_stock':dict(Counter(offer_stocks[e] for e in (po-co))),
       'limitation':'XML cannot prove PHH activation state or whether warehouse dimensions are measured.'
    }
    if a.json:Path(a.json).write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(report,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
