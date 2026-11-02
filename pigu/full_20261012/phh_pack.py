from phh_common import Decimal,ROUND_CEILING,plain,re

def package(r,c):
 fam=r['family'];s=c['size'];v=c['v'];nom=s['nominal'] if s else 30
 w=v['inventoryItem']['measurement']['weight'];value=Decimal(str(w['value'] or 0))
 units={'KILOGRAMS':Decimal(1),'GRAMS':Decimal('.001'),'POUNDS':Decimal('.45359237'),'OUNCES':Decimal('.028349523125')}
 source=value*units.get(w['unit'],Decimal(1))
 if fam in ('decal','film','paper'):
  # Seller-approved standard packaging for rolled printed products.
  # Length 60 cm, width and height 6 cm, packaged weight 0.5 kg.
  # Not a measured value for arbitrary 3D printed items.
  return {'weight':'0.50','length':'0.60','width':'0.06','height':'0.06',
          'basis':'seller_approved_standard_60x6x6_cm_0_5_kg',
          'source_weight_kg':str(source),'measured':False}
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
