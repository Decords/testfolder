from phh_common import *
from phh_copy import NOTES

def prepare_translations(records):
 path=BASE/'translation_cache.json'
 cache=json.loads(path.read_text()) if path.exists() else {}
 tasks={}
 for r in records:
  p=r['p'];r['localized']={}
  source_title=clean_title(p['title']);source_intro=intro(p['descriptionHtml']) or source_title
  for lang in LANGS:
   title=clean_title(existing_translation(p,lang,'title'))
   body=intro(existing_translation(p,lang,'body_html'))
   loc={};r['localized'][lang]=loc
   for kind,existing,source in [('title',title,source_title),('intro',body,source_intro)]:
    k=key(lang,source);loc[kind]=existing or cache.get(k,'');loc[kind+'_key']=k
    if not existing and k not in cache:tasks[k]={'language':lang,'text':source}
 for lang in LANGS:
  for source in list(NOTES.values())+sorted({c['extra'] for r in records for c in r['variants'] if c['extra']}):
   k=key(lang,source)
   if k not in cache:tasks[k]={'language':lang,'text':source}
 (BASE/'translation_tasks.json').write_text(json.dumps(tasks,ensure_ascii=False,indent=2))
 print('Missing translation units',len(tasks),'characters',sum(len(v['text']) for v in tasks.values()),flush=True)
 return tasks,cache
