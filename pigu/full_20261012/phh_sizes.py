"""Validate source identifiers and normalize existing dimensions; create no identifiers."""
import re
from decimal import Decimal, ROUND_HALF_UP
PAIR=re.compile(r'(\d+(?:[.,]\d+)?)\s*[x×х]\s*(\d+(?:[.,]\d+)?)\s*(cm|см|mm|мм|inches|inch|in\b|"|m\b)?',re.I)
ONE=re.compile(r'(\d+(?:[.,]\d+)?)\s*(cm|см|mm|мм|inches|inch|in\b|"|m\b)',re.I)
SIZE_NAMES=re.compile(r'size|dimension|measurement|height|width|length|mõõt|suurus|izmērs|dydis|размер|koko',re.I)
def integer(n):return int(Decimal(str(n)).quantize(Decimal('1'),rounding=ROUND_HALF_UP))
def valid_ean(value):
 s=str(value or '').strip()
 if not re.fullmatch(r'\d{12,13}',s):return False
 return (sum(int(x)*(3 if i%2==0 else 1) for i,x in enumerate(reversed(s[:-1])))+int(s[-1]))%10==0

def factor(unit):
 return {'cm':1,'см':1,'mm':.1,'мм':.1,'m':100}.get((unit or '').lower(),2.54)

def parse_size(v,p):
 opts=[o['value'] for o in v.get('selectedOptions',[]) if SIZE_NAMES.search(o.get('name',''))]
 if not opts:opts=[v.get('title','')]
 for value in opts:
  for metric in (True,False):
   for m in PAIR.finditer(value):
    if ((m[3] or '').lower() in ('cm','см','mm','мм','m'))!=metric:continue
    a=integer(float(m[1].replace(',','.'))*factor(m[3]));b=integer(float(m[2].replace(',','.'))*factor(m[3]))
    if 1<=a<=1500 and 1<=b<=1500:return {'a':a,'b':b,'nominal':max(a,b),'approx':False,'source':'variant'}
   for m in ONE.finditer(value):
    if (m[2].lower() in ('cm','см','mm','мм','m'))!=metric:continue
    a=integer(float(m[1].replace(',','.'))*factor(m[2]))
    if 1<=a<=1500:return {'a':a,'b':None,'nominal':a,'approx':True,'source':'variant'}
  if re.fullmatch(r'\s*\d+(?:[.,]\d+)?\s*(?:\([A-Za-z]+\))?\s*',value):
   a=integer(float(re.search(r'\d+(?:[.,]\d+)?',value)[0].replace(',','.'))*2.54)
   if a>0:return {'a':a,'b':None,'nominal':a,'approx':True,'source':'variant_unitless_inches'}
 for value in [p.get('title',''),re.sub('<[^>]+>',' ',p.get('descriptionHtml',''))]:
  for m in PAIR.finditer(value):
   if not m[3]:continue
   a=integer(float(m[1].replace(',','.'))*factor(m[3]));b=integer(float(m[2].replace(',','.'))*factor(m[3]))
   if 1<=a<=1500 and 1<=b<=1500:return {'a':a,'b':b,'nominal':max(a,b),'approx':False,'source':'fixed_product_text'}
 return None
