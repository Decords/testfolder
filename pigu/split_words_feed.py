from copy import deepcopy
from pathlib import Path
import requests
from lxml import etree

SRC='https://cdn.shopify.com/s/files/1/0608/0888/8570/files/PiguProducts-batch-001-11-products.xml?v=1788702429'
OUT=Path('pigu/PiguProducts-batch-001-split-words-16-products.xml')
SIZES=[('61','18'),('99','30'),('140','43'),('180','56'),('221','69'),('259','79')]
TITLE_TAGS=['title','title-ru','title-lv','title-ee','title-fi']
DESC_TAGS=['long-description','long-description-ru','long-description-lv','long-description-ee','long-description-fi']

def cd(el,text): el.text=etree.CDATA(text)

def props(product,w,h):
    old=product.find('properties')
    if old is not None: product.remove(old)
    node=etree.Element('properties')
    for k,v in [('Aukštis',h),('Plotis',w),('Medžiaga','Vinilas'),('Raštai','Tekstai'),('Tipas','Užrašai')]:
        p=etree.SubElement(node,'property'); cd(etree.SubElement(p,'id'),k)
        vals=etree.SubElement(p,'values'); cd(etree.SubElement(vals,'value'),v)
    colours=product.find('colours'); product.insert(list(product).index(colours),node)

def main():
    r=requests.get(SRC,timeout=60); r.raise_for_status()
    root=etree.fromstring(r.content,etree.XMLParser(remove_blank_text=True,strip_cdata=False))
    words=None; others=[]
    for p in root.findall('product'):
        if p.findtext('.//barcode')=='7341147056448': words=p
        else: others.append(p)
    if words is None: raise RuntimeError('pilot product not found')
    mods=words.findall('.//modification')
    if len(mods)!=6: raise RuntimeError(f'expected 6 mods, got {len(mods)}')

    title_base={
      'title':'Motyvacinis vinilo sienų lipdukas Decords „Words Are Powerful“, juodas',
      'title-ru':'Мотивационная виниловая наклейка Decords «Words Are Powerful», чёрная',
      'title-lv':'Motivējoša vinila sienas uzlīme Decords “Words Are Powerful”, melna',
      'title-ee':'Motiveeriv vinüülist seinakleebis Decords „Words Are Powerful“, must',
      'title-fi':'Motivoiva vinyyliseinätarra Decords “Words Are Powerful”, musta'}
    size_label={'title':'cm','title-ru':'см','title-lv':'cm','title-ee':'cm','title-fi':'cm'}
    desc_intro={
      'long-description':'Juodo polimerinio vinilo sienų lipdukas „Words Are Powerful“. Tikslus dydis: {w} × {h} cm.',
      'long-description-ru':'Чёрная виниловая наклейка на стену «Words Are Powerful». Точный размер: {w} × {h} см.',
      'long-description-lv':'Melna vinila sienas uzlīme “Words Are Powerful”. Precīzs izmērs: {w} × {h} cm.',
      'long-description-ee':'Must vinüülist seinakleebis „Words Are Powerful“. Täpne mõõt: {w} × {h} cm.',
      'long-description-fi':'Musta vinyyliseinätarra “Words Are Powerful”. Tarkka koko: {w} × {h} cm.'}

    split=[]
    for mod,(w,h) in zip(mods,SIZES):
        p=deepcopy(words)
        for tag in TITLE_TAGS: cd(p.find(tag),f"{title_base[tag]}, {w} × {h} {size_label[tag]}")
        for tag in DESC_TAGS:
            old=p.findtext(tag) or ''
            tail=old[old.find('</p>')+4:] if '</p>' in old else ''
            cd(p.find(tag),'<p>'+desc_intro[tag].format(w=w,h=h)+'</p>'+tail)
        props(p,w,h)
        mroot=p.find('.//modifications')
        for x in list(mroot): mroot.remove(x)
        m=deepcopy(mod)
        for tag in ['modification-title','modification-title-lv','modification-title-ee','modification-title-fi']:
            if m.find(tag) is not None: cd(m.find(tag),f'{w} × {h} cm')
        if m.find('modification-title-ru') is not None: cd(m.find('modification-title-ru'),f'{w} × {h} см')
        mroot.append(m); split.append(p)

    out=etree.Element('products',nsmap={'xsi':'http://www.w3.org/2001/XMLSchema-instance'})
    for p in split: out.append(p)
    for p in others: out.append(deepcopy(p))
    OUT.parent.mkdir(parents=True,exist_ok=True)
    etree.ElementTree(out).write(str(OUT),encoding='UTF-8',xml_declaration=True,standalone=True,pretty_print=True)
    chk=etree.parse(str(OUT)); cards=chk.findall('.//product'); allmods=chk.findall('.//modification')
    assert len(cards)==16 and len(allmods)==22
    assert len([p for p in cards if 'Words Are Powerful' in (p.findtext('title') or '')])==6
    print('OK',len(cards),len(allmods),OUT)

if __name__=='__main__': main()
