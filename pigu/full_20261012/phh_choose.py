from phh_common import integer

def choose(candidates,family):
 candidates=sorted(candidates,key=lambda x:(x['v'].get('position',0),int(x['v']['id'].rsplit('/',1)[-1])))
 if len(candidates)<=5:return candidates
 sized=[c for c in candidates if c['size']]
 if not sized:return candidates[:5]
 targets=[60,100,140,180,220] if family in ('decal','film') else [13,18,23,28,33] if family=='3d' else []
 selected=[];used_sizes=set()
 for target in targets:
  remaining=[c for c in sized if c not in selected and c['size']['nominal'] not in used_sizes]
  if not remaining:break
  c=min(remaining,key=lambda c:(abs(c['size']['nominal']-target),c['v'].get('position',0)))
  selected.append(c);used_sizes.add(c['size']['nominal'])
 if not targets:
  ordered=sorted(sized,key=lambda c:(c['size']['nominal'],c['v'].get('position',0)))
  for idx in [integer(i*(len(ordered)-1)/4) for i in range(5)]:
   c=ordered[idx]
   if c not in selected:selected.append(c)
 for c in candidates:
  if len(selected)==5:break
  if c not in selected:selected.append(c)
 return sorted(selected,key=lambda c:c['v'].get('position',0))
