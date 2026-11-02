#!/usr/bin/env python3
"""Read-only per-category PHH attributes and maker diagnostic."""
from collections import Counter,defaultdict
from pathlib import Path
import xml.etree.ElementTree as ET,json
f=Path("pigu/PHH_PRODUCTS.xml")
t=defaultdict(lambda:{"products":0,"attributes":Counter(),"manufacturers":Counter(),"examples":[]})
stats=Counter()
it=ET.iterparse(str(f),events=("start","end"));_,root=next(it)
for ev,p in it:
 if ev!="end" or p.tag!="product":continue
 cat=(p.findtext("category-id") or "").strip()
 d=t[cat];d["products"]+=1
 props={}
 for prop in p.findall("./properties/property"):
  k=(prop.findtext("id") or "").strip()
  val=[(v.text or "").strip() for v in prop.findall("./values/value")]
  if k and any(val):d["attributes"][k]+=1;props[k]=val
 if not props:stats["products_no_attributes"]+=1
 if "Prekės ženklas" not in props:stats["products_no_brand_attribute"]+=1
 if "Medžiaga" not in props:stats["products_no_material_attribute"]+=1
 if "Aukštis" not in props:stats["products_no_height_attribute"]+=1
 m=(p.findtext("manufacturer-name") or "").strip()
 d["manufacturers"][m]+=1
 if len(d["examples"])<2:
  d["examples"].append({"title":p.findtext("title"),"ean":p.findtext(".//modification/attributes/barcodes/barcode"),"props":props})
 root.clear()
obj={"total":sum(x["products"] for x in t.values()),"global":stats,"categories":[{"id":k,**{"products":v["products"],"attributes":dict(v["attributes"]),"manufacturers":dict(v["manufacturers"]),"examples":v["examples"]}} for k,v in sorted(t.items(),key=lambda z:-z[1]["products"])]}
Path("pigu/attribute_diagnostic_20261102.json").write_text(json.dumps(obj,ensure_ascii=False,indent=2))
print("TOTAL",obj["total"],"CATEGORIES",len(t),"GLOBAL",dict(stats))
for x in obj["categories"][:80]:print("CAT",x["id"],x["products"],"ATTR",json.dumps(x["attributes"],ensure_ascii=False),"EX",str(x["examples"][0].get("title"))[:45])
