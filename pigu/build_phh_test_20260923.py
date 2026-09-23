"""Create a separate-card PHH content-only test. No offers are activated.
Product second sides are user-authorized 1:1 estimates for circular compositions.
Packaging is an explicit proposed estimate, not a measurement: confirm before sale.
"""
from pathlib import Path
from decimal import Decimal, ROUND_CEILING
import argparse, csv, hashlib, json, re
from lxml import etree

SIZE_CM = [60, 100, 140, 180, 220]
CDN = 'https://cdn.shopify.com/s/files/1/0608/0888/8570/files/'
LANGS = ['', '-ru', '-lv', '-ee', '-fi']
DATA = [
 {'key':'tunnel','product_id':'10520768479570',
  'variants':['52437119926610','52437119992146','52437120057682','52437120123218','52437120188754'],
  'eans':['7341146853048','7341146853062','7341146853086','7341146853109','7341146853123'],
  'pattern':'Geometriniai raštai',
  'titles':[
   'Sienų lipdukas su plytų tuneliu ir oranžinėmis akimis, 3D optinė iliuzija',
   'Наклейка на стену «Кирпичный туннель с оранжевыми глазами», оптическая 3D-иллюзия',
   'Sienas uzlīme ar ķieģeļu tuneli un oranžām acīm, 3D optiskā ilūzija',
   'Seinakleebis tellistunneli ja oranžide silmadega, 3D optiline illusioon',
   'Seinätarra, tiilitunneli ja oranssit silmät, 3D-illuusio'],
  'intro':[
   'Dekoratyvinis vinilo sienų lipdukas vaizduoja apskritą plytų tunelį su tamsoje matomomis oranžinėmis akimis. Perspektyva ir šešėliai sukuria gylio iliuziją, tačiau pats lipdukas yra plokščias.',
   'Декоративная виниловая наклейка изображает круглый кирпичный туннель с оранжевыми глазами в темноте. Перспектива и тени создают иллюзию глубины, при этом сама наклейка плоская.',
   'Dekoratīvā vinila sienas uzlīme attēlo apaļu ķieģeļu tuneli ar oranžām acīm tumsā. Perspektīva un ēnas rada dziļuma ilūziju, taču pati uzlīme ir plakana.',
   'Dekoratiivne vinüülist seinakleebis kujutab ümmargust tellistunnelit, mille pimedusest paistavad oranžid silmad. Perspektiiv ja varjud loovad sügavuse illusiooni, kuid kleebis ise on tasapinnaline.',
   'Koristeellinen vinyyliseinätarra esittää pyöreää tiilitunnelia, jonka pimeydessä näkyy oranssit silmät. Perspektiivi ja varjot luovat syvyysvaikutelman, mutta itse tarra on tasainen.'],
  'images':[
   'il_fullxfull.7629039803_x8tm_e8245e13-4315-4b81-abf4-a470e3f59c73.jpg?v=1768471963',
   'il_fullxfull.7629267857_iloq.jpg?v=1768471964',
   'il_fullxfull.7629269183_ejgn.jpg?v=1768471964']},
 {'key':'monstera','product_id':'10527084216658',
  'variants':['52456112914770','52456112980306','52456113045842','52456113111378','52456113176914'],
  'eans':['7341146857145','7341146857169','7341146857183','7341146857206','7341146857220'],
  'pattern':'Gamta ir gėlės',
  'titles':[
   'Sienų lipdukas su monsteros lapais, tropinė mandala ir botaninis dekoras',
   'Наклейка на стену «Листья монстеры», тропическая мандала, растительный декор',
   'Sienas uzlīme ar monsteras lapām, tropu mandala un botānisks dekors',
   'Monstera lehtedega seinakleebis, troopiline mandala ja taimemustriga seinakaunistus',
   'Seinätarra peikonlehden lehdillä, trooppinen mandala ja kasviaiheinen seinäkoriste'],
  'intro':[
   'Dekoratyvinis vinilo sienų lipdukas su žaliais monsteros lapais, išdėstytais mandalos raštu. Sluoksniuota botaninė kompozicija tinka svetainei, miegamajam, darbo kambariui ar jogos erdvei.',
   'Декоративная виниловая наклейка с зелёными листьями монстеры, расположенными в форме мандалы. Многослойная растительная композиция подходит для гостиной, спальни, кабинета или пространства для йоги.',
   'Dekoratīva vinila sienas uzlīme ar zaļām monsteras lapām, kas izkārtotas mandalas rakstā. Daudzslāņainā botāniskā kompozīcija piemērota viesistabai, guļamistabai, darba telpai vai jogas zonai.',
   'Dekoratiivne vinüülist seinakleebis roheliste monstera lehtedega, mis on paigutatud mandalamustrisse. Kihiline taimemotiiv sobib elutuppa, magamistuppa, kodukontorisse või joogaruumi.',
   'Koristeellinen vinyyliseinätarra, jossa vihreät peikonlehden lehdet muodostavat mandalakuvion. Kerroksellinen kasviaihe sopii olohuoneeseen, makuuhuoneeseen, työhuoneeseen tai joogatilaan.'],
  'images':[
   'il_fullxfull.7591134638_khu4_8817ed62-9b5b-47a0-9b5a-c5d254b17ae4.jpg?v=1768471226',
   'il_fullxfull.7639089661_fu9q_64d11a8b-a8b9-4239-a662-4cef03a80146.jpg?v=1768471226',
   'il_fullxfull.7591134684_rdcf.jpg?v=1768471228']}
]
SIZING = [
 'Pasirinktas dydis pagal ilgiausią viso dizaino kraštinę: {s} cm. Orientaciniai bendri matmenys, plotis × aukštis: apie {s} × {s} cm. Antroji kraštinė įvertinta pagal apytikriai apskritą kompoziciją. Gaminant ji nustatoma proporcingai nuotraukoje matomam dizainui, jo neištempiant; tikslus antrosios kraštinės matmuo gali skirtis nuo pateikto orientacinio skaičiaus. Visi matmenys suapvalinti iki sveikų centimetrų.',
 'Выбранный размер по большей стороне всего рисунка: {s} см. Ориентировочные габариты, ширина × высота: около {s} × {s} см. Вторая сторона оценена исходя из приблизительно круглой композиции. При изготовлении она определяется пропорционально дизайну на фотографии, без растяжения рисунка; её точный размер может отличаться от указанного ориентировочного значения. Все размеры округлены до целых сантиметров.',
 'Izvēlētais izmērs pēc visa dizaina garākās malas: {s} cm. Aptuvenie kopējie izmēri, platums × augstums: apmēram {s} × {s} cm. Otrā mala novērtēta pēc aptuveni apaļās kompozīcijas. Izgatavošanas laikā to nosaka proporcionāli fotogrāfijā redzamajam dizainam, neizstiepjot attēlu; precīzs otrās malas izmērs var atšķirties no norādītā aptuvenā lieluma. Visi izmēri noapaļoti līdz veseliem centimetriem.',
 'Valitud suurus kogu kujunduse pikima külje järgi: {s} cm. Ligikaudsed üldmõõtmed, laius × kõrgus: umbes {s} × {s} cm. Teise külje hinnang põhineb ligikaudu ümmargusel kompositsioonil. Valmistamisel määratakse see proportsionaalselt fotol oleva kujundusega, pilti venitamata; teise külje täpne mõõt võib esitatud hinnangust erineda. Kõik mõõdud on ümardatud täissentimeetriteni.',
 'Valittu koko koko kuvion pisimmän sivun mukaan: {s} cm. Arvioidut kokonaismitat, leveys × korkeus: noin {s} × {s} cm. Toisen sivun arvio perustuu suunnilleen pyöreään sommitelmaan. Valmistuksessa toinen sivu määräytyy valokuvan kuvion mittasuhteiden mukaan ilman kuvan venyttämistä; sen tarkka mitta voi poiketa ilmoitetusta arviosta. Kaikki mitat on pyöristetty kokonaisiin senttimetreihin.'
]
APPLICATION = [
 'Komplekte vienas pasirinkto dydžio dizainas. Dideli dydžiai gali būti pateikiami suderinamomis dalimis. Klijuokite ant lygaus, švaraus, visiškai sauso ir tvirto paviršiaus. Šviežiai dažytam paviršiui leiskite visiškai sukietėti ir pirmiausia išbandykite nepastebimoje vietoje.',
 'В комплекте один дизайн выбранного размера. Большие размеры могут поставляться совмещаемыми частями. Наносите на гладкую, чистую, полностью сухую и прочную поверхность. Свежей краске дайте полностью затвердеть и сначала выполните тест на незаметном участке.',
 'Komplektā ir viens izvēlētā izmēra dizains. Lieli izmēri var tikt piegādāti savienojamās daļās. Uzstādiet uz gludas, tīras, pilnīgi sausas un stabilas virsmas. Ļaujiet svaigai krāsai pilnībā sacietēt un vispirms pārbaudiet neuzkrītošā vietā.',
 'Komplektis on üks valitud suuruses kujundus. Suuremad mõõdud võivad olla tarnitud omavahel sobitatavate osadena. Paigaldage siledale, puhtale, täiesti kuivale ja stabiilsele pinnale. Laske värskel värvil täielikult kõveneda ja tehke esmalt katse varjatud kohal.',
 'Pakkauksessa on yksi valitun kokoinen kuvio. Suuret koot voidaan toimittaa toisiinsa kohdistettavina osina. Kiinnitä sileälle, puhtaalle, täysin kuivalle ja kestävälle pinnalle. Anna tuoreen maalin kovettua täysin ja kokeile ensin huomaamattomassa kohdassa.'
]

def text(parent, tag, value):
    e=etree.SubElement(parent,tag); e.text=etree.CDATA(str(value)); return e

def numeric(parent, tag, value):
    e=etree.SubElement(parent,tag); e.text=str(value); return e

def property_value(parent, key, value):
    p=etree.SubElement(parent,'property'); text(p,'id',key)
    text(etree.SubElement(p,'values'),'value',value)

def valid_ean(s):
    return bool(re.fullmatch(r'\d{13}',s)) and sum(int(c)*(1 if i%2==0 else 3) for i,c in enumerate(s))%10==0

def generate(out):
    out.mkdir(parents=True,exist_ok=True)
    root=etree.Element('products'); registry=[]
    for d in DATA:
      for s,vid,ean in zip(SIZE_CM,d['variants'],d['eans']):
        assert valid_ean(ean)
        p=etree.SubElement(root,'product')
        text(p,'category-id','1001')
        text(p,'category-name','Baldai ir namų interjeras / Namų interjeras / Interjero lipdukai')
        # Keep the verified nominal longest side in the title; disclose both estimated dimensions below.
        for j,lang in enumerate(LANGS):
            text(p,'title'+lang,d['titles'][j]+f', {s} '+('см' if lang=='-ru' else 'cm'))
        for j,lang in enumerate(LANGS):
            desc=''.join('<p>'+v+'</p>' for v in (d['intro'][j],SIZING[j].format(s=s),APPLICATION[j]))
            text(p,'long-description'+lang,desc)
        area=(Decimal(s)/100)**2
        weight=(area*Decimal('0.30')+Decimal('0.35')).quantize(Decimal('0.1'),rounding=ROUND_CEILING)
        text(p,'comments',f'TEST CONTENT ONLY. Source Shopify product {d["product_id"]}; variant {vid}. '
             f'Nominal longest side {s} cm. Product width and height are provisional 1:1 estimates authorized by the seller, not measured artwork dimensions; the customer description discloses this. '
             'PACKAGE_ESTIMATE_NOT_MEASURED: proposed 65 x 12 x 12 cm tube, assuming aligned print sections no wider than 60 cm; '
             'estimated packed mass = enclosing square area x 0.30 kg per square metre + 0.35 kg packaging, rounded upward to 0.1 kg. '
             'The package proposal requires seller confirmation before offer activation. No offer activation is included in this feed. '
             'Supplier code derived from the source variant ID; Shopify SKU not changed.')
        numeric(p,'guarantee',0)
        text(p,'manufacturer-name','AnOL OÜ')
        text(p,'manufacturer-address','Madara 33/1 - S1, 10613 Tallinn, Estonia')
        text(p,'manufacturer-email','info@decords.com')
        props=etree.SubElement(p,'properties')
        for k,v in [('Aukštis',s),('Plotis',s),('Raštai',d['pattern']),('Medžiaga','Vinilas')]: property_value(props,k,v)
        colour=etree.SubElement(etree.SubElement(p,'colours'),'colour')
        images=etree.SubElement(colour,'images')
        for url in d['images']: text(etree.SubElement(images,'image'),'url',CDN+url)
        m=etree.SubElement(etree.SubElement(colour,'modifications'),'modification')
        text(m,'modification-title','')
        for k,v in [('weight',weight),('length','0.65'),('height','0.12'),('width','0.12')]: numeric(m,k,v)
        attrs=etree.SubElement(m,'attributes')
        text(etree.SubElement(attrs,'barcodes'),'barcode',ean)
        code='PHH-'+vid; text(attrs,'supplier-code',code)
        registry.append({'design_key':d['key'],'source_product_id':d['product_id'],'source_variant_id':vid,'ean':ean,'supplier_code':code,
           'nominal_longest_side_cm':s,'estimated_width_cm':s,'estimated_height_cm':s,'package_length_cm':65,'package_width_cm':12,
           'package_height_cm':12,'estimated_packaged_weight_kg':str(weight),'package_status':'PROPOSED_ESTIMATE_CONFIRM_BEFORE_SALE','phh_import_status':'NOT_VERIFIED'})
    dest=out/'PHH_TEST_TUNNEL_MONSTERA_10_CARDS_20260923.xml'
    etree.ElementTree(root).write(str(dest),encoding='UTF-8',xml_declaration=True,standalone=True,pretty_print=True)
    check=etree.parse(str(dest)); ps=check.findall('product'); ms=check.findall('.//modification')
    assert len(ps)==10 and len(ms)==10 and all(len(p.findall('.//modification'))==1 for p in ps)
    assert len({r['ean'] for r in registry})==10 and len({r['supplier_code'] for r in registry})==10
    for p,r in zip(ps,registry):
      for lang in LANGS:
        t=p.findtext('title'+lang)
        assert 'decords' not in t.lower() and t.endswith(str(r['nominal_longest_side_cm'])+(' см' if lang=='-ru' else ' cm'))
      for k in ['Aukštis','Plotis','Raštai']:
        assert p.findtext(f"properties/property[id='{k}']/values/value")
      for k in ['weight','length','height','width']:
        assert Decimal(p.findtext('.//modification/'+k))>0
    assert not re.search(r'\binches?\b|дюйм|\btolli\b|\btuumaa\b|\bcollas\b',dest.read_text(),re.I)
    with (out/'PHH_TEST_REGISTRY_20260923.csv').open('w',encoding='utf-8-sig',newline='') as f:
      w=csv.DictWriter(f,fieldnames=list(registry[0]));w.writeheader();w.writerows(registry)
    audit={'product_cards':10,'modifications':10,'designs':2,'sizes_cm':SIZE_CM,'languages':['LT','RU','LV','EE','FI'],
           'duplicate_ean':0,'duplicate_supplier_code':0,'package_values_measured':False,'product_second_dimension_measured':False,
           'source_identifiers':'rechecked in Shopify on 2026-09-23','offer_import_included':False,'xsd_validation':'not available',
           'phh_semantic_validation':'pending','sha256':hashlib.sha256(dest.read_bytes()).hexdigest(),'bytes':dest.stat().st_size}
    (out/'PHH_TEST_AUDIT_20260923.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(audit,ensure_ascii=False,indent=2));return dest

def download_images(out):
    import urllib.request
    from PIL import Image
    assets=out/'assets'; assets.mkdir(exist_ok=True); checks=[]
    for d in DATA:
      for i,url in enumerate(d['images'],1):
        full=CDN+url; info={'design':d['key'],'position':i,'url':full}
        try:
          req=urllib.request.Request(full,headers={'User-Agent':'PHH-Feed-Validation/1.0'})
          with urllib.request.urlopen(req,timeout=30) as resp:
            info.update(status=resp.status,final_url=resp.url,content_type=resp.headers.get('Content-Type'))
            body=resp.read(40*1024*1024+1)
          assert len(body)<=40*1024*1024
          file=assets/f'{d["key"]}-{i}.jpg';file.write_bytes(body)
          with Image.open(file) as im: info.update(width=im.width,height=im.height,format=im.format)
          info.update(bytes=len(body),minimum_resolution_met=min(info['width'],info['height'])>=1000,
                      direct_url=info['final_url']==full)
        except Exception as e: info['error']=str(e)
        checks.append(info)
    (out/'PHH_IMAGE_CHECKS_20260923.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2),encoding='utf-8')

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--out',default='pigu/test_20260923');parser.add_argument('--download-images',action='store_true')
    args=parser.parse_args();out=Path(args.out);generate(out)
    if args.download_images: download_images(out)
