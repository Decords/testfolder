from phh_common import BASE,json,re,time
from concurrent.futures import ThreadPoolExecutor,as_completed
from collections import defaultdict
import requests

def translate_batch(lang,items):
 query='\n'.join(f'[[{i+100001}]] '+v['text'] for i,(_,v) in enumerate(items))
 params={'client':'gtx','sl':'en','tl':'et' if lang=='ee' else lang,'dt':'t','q':query}
 last=None
 for attempt in range(4):
  try:
   response=requests.get('https://translate.googleapis.com/translate_a/single',params=params,timeout=80)
   response.raise_for_status();data=response.json()
   out=''.join(x[0] for x in data[0] if x and x[0])
   matches=list(re.finditer(r'\[\s*\[\s*(\d+)\s*\]\s*\]',out))
   found={int(m[1]):out[m.end():matches[j+1].start() if j+1<len(matches) else len(out)].strip() for j,m in enumerate(matches)}
   if set(found)!=set(range(100001,100001+len(items))) or not all(found.values()):raise ValueError('Translation segment count mismatch')
   return {k:found[100001+i] for i,(k,_) in enumerate(items)}
  except Exception as exc:last=exc;time.sleep(2**attempt)
 raise RuntimeError(f'{lang}: {len(items)} segments: {last}')

def translate(tasks,cache):
 grouped=defaultdict(list)
 for k,v in tasks.items():grouped[v['language']].append((k,v))
 batches=[]
 for lang,items in grouped.items():
  part=[];chars=0
  for item in items:
   n=len(item[1]['text'])+16
   if chars+n>3300 and part:batches.append((lang,part));part=[];chars=0
   part.append(item);chars+=n
  if part:batches.append((lang,part))
 failures=[]
 with ThreadPoolExecutor(max_workers=4) as pool:
  futures=[pool.submit(translate_batch,*batch) for batch in batches]
  for i,future in enumerate(as_completed(futures),1):
   try:cache.update(future.result())
   except Exception as exc:failures.append(str(exc))
   if i%20==0 or i==len(futures):
    (BASE/'translation_cache.json').write_text(json.dumps(cache,ensure_ascii=False))
    print('Translated batches',i,'/',len(futures),'failed',len(failures),flush=True)
 if failures:
  (BASE/'translation_failures.json').write_text(json.dumps(failures,ensure_ascii=False,indent=2))
  raise RuntimeError(f'{len(failures)} translation batches failed; incomplete content is not published')
 return cache
