from phh_common import *
from phh_card_text import card_text
from phh_pack import package,pattern

def card(root,r,c,cache):
 p=r['p'];s=c['size'];v=c['v'];node=etree.SubElement(root,'product')
 text(node,'category-id',r['category_id']);text(node,'category-name',r['category_name'])
 card_text(node,r,c,cache)
 pack=package(r,c)
 comment=f'Shopify product {p["id"].rsplit("/",1)[-1]}; variant {v["id"].rsplit("/",1)[-1]}. Package dimensions are planning estimates, not warehouse measurements. Weight basis: {pack["basis"]}.'
 if s and s['approx'] and r['family'] in ('decal','film'):comment+=' Second artwork dimension is an equal-side estimate; see customer description.'
 text(node,'comments',comment)
 text(node,'manufacturer-name','AnOL OÜ')
 text(node,'manufacturer-address','Madara 33/1 - S1, 10613 Tallinn, Estonia')
 text(node,'manufacturer-email','info@decords.com')
 props=etree.SubElement(node,'properties')
 prop(props,'Prekės ženklas','Decords')
 if r['category_id']=='1001':
  assert s
  prop(props,'Aukštis',s['b'] or s['a']);prop(props,'Plotis',s['a']);prop(props,'Raštai',pattern(p))
 elif s and s.get('b'):
  prop(props,'Aukštis',s['b']);prop(props,'Plotis',s['a'])
 material=(p['title']+' '+plain(p['descriptionHtml'])).lower()
 if re.search(r'\bpla\b',material):prop(props,'Medžiaga','PLA')
 elif re.search(r'\bpetg\b',material):prop(props,'Medžiaga','PETG')
 elif r['family'] in ('decal','film') and re.search(r'vinyl|pvc|vinil',material):prop(props,'Medžiaga','Vinilas')
 elif r['family']=='paper' and 'canvas' in (p['productType']+' '+p['title']).lower():prop(props,'Medžiaga','Drobė')
 elif r['family']=='paper' and ('paper' in material or re.search(r'poster|printed flyer',p['productType'],re.I)):prop(props,'Medžiaga','Popierius')
 elif r['family']=='decal':prop(props,'Medžiaga','Vinilas')
 if len(props)==0:node.remove(props)
 colour=etree.SubElement(etree.SubElement(node,'colours'),'colour')
 ims=etree.SubElement(colour,'images')
 for url in r['images']:text(etree.SubElement(ims,'image'),'url',url)
 mod=etree.SubElement(etree.SubElement(colour,'modifications'),'modification')
 for field in ('weight','length','height','width'):etree.SubElement(mod,field).text=pack[field]
 attrs=etree.SubElement(mod,'attributes')
 text(etree.SubElement(attrs,'barcodes'),'barcode',c['ean']);text(attrs,'supplier-code',c['sku'])
 return pack
