from phh_common import Decimal,ROUND_CEILING,plain,re

def package(r,c):
 fam=r['family'];s=c['size'];v=c['v'];nom=s['nominal'] if s else 30
 w=v['inventoryItem']['measurement']['weight'];value=Decimal(str(w['value'] or 0))
 units={'KILOGRAMS':Decimal(1),'GRAMS':Decimal('.001'),'POUNDS':Decimal('.45359237'),'OUNCES':Decimal('.028349523125')}
 source=value*units.get(w['unit'],Decimal(1))
 if fam in ('decal','film','paper'):
  short=min(s['a'],s['b'] or s['a']) if s else 30
  length=Decimal(min(max(short+5,25),110))/100;width=height=Decimal('.12')
  area=Decimal(s['a']*(s['b'] or s['a']) if s else 900)/10000
  estimate=(area*Decimal('.22' if fam=='paper' else '.30')+Decimal('.35')).quantize(Decimal('.1'),rounding=ROUND_CEILING)
  weight=source+Decimal('.15') if 0<source<=5 else estimate
  basis='source_weight_plus_estimated_packaging' if 0<source<=5 else 'area_based_packaged_weight_estimate'
 else:
  length=width=height=Decimal(max(nom+4,12))/100
  estimate=(Decimal(nom**3)*Decimal('.000031')+Decimal('.20')).quantize(Decimal('.1'),rounding=ROUND_CEILING)
  weight=source+Decimal('.15') if source>0 else estimate
  basis='source_weight_plus_estimated_packaging' if source>0 else 'bounding_volume_packaged_weight_estimate'
 return {'weight':str(max(weight,Decimal('.1')).quantize(Decimal('.01'))),'length':str(length),'width':str(width),'height':str(height),'basis':basis,'source_weight_kg':str(source),'measured':False}

def pattern(p):
 t=(p['title']+' '+p['productType']).lower()
 if re.search(r'flower|floral|botan|leaf|leaves|tree|forest|monstera|plant|garden|nature',t):return 'Gamta ir gėlės'
 if re.search(r'tunnel|geometr|pattern|hexagon|circle|dot|triangle',t):return 'Geometriniai raštai'
 if re.search(r'quote|letter|text|words|saying|motivational|script',t):return 'Užrašai'
 if re.search(r'animal|cat|dog|bird|lion|tiger|wolf|dinosaur|dragon|kitten|puppy|horse|butterfly',t):return 'Gyvūnai'
 return 'Kiti'
