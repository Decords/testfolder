from phh_common import *
from phh_copy import NOTES,SIZE_LABEL,APPROX_LABEL,CUSTOM_NOTE

def card_text(node,r,c,cache):
 p=r['p'];s=c['size'];titles={};descriptions={}
 for lang in LANGS:
  loc=r['localized'][lang]
  title=clean_title(loc['title'] or cache[loc['title_key']])
  body=convert_units(loc['intro'] or cache[loc['intro_key']])
  if c['extra']:title+=', '+cache[key(lang,c['extra'])]
  label=''
  if s:
   label=(f"{s['a']} × {s['b']}" if s['b'] else str(s['nominal']))+(' см' if lang=='ru' else ' cm')
   title+=', '+label
  parts=[body]
  if label:parts.append(SIZE_LABEL[lang]+': '+label+'.')
  if s and s['approx'] and r['family'] in ('decal','film'):parts.append(APPROX_LABEL[lang])
  parts.append(cache[key(lang,NOTES[r['family']])])
  if re.search(r'custom|personaliz|personalised',p['title'],re.I):parts.append(CUSTOM_NOTE[lang])
  titles[lang]=title
  descriptions[lang]=''.join('<p>'+html.escape(value)+'</p>' for value in parts if value)
 for lang in LANGS:text(node,'title'+SUFFIX[lang],titles[lang])
 for lang in LANGS:text(node,'long-description'+SUFFIX[lang],descriptions[lang])
