"""Publish only the validated artifacts selected in publish_request.json."""
from pathlib import Path
import hashlib,json,shutil
from lxml import etree
base=Path('pigu/full_20261012');request=json.loads((base/'publish_request.json').read_text())
audit=json.loads((base/'build_audit.json').read_text())
for filename,field in [('PHH_PRODUCTS_FULL.xml','content_sha256'),('PHH_STOCK_PRICES.xml','offers_sha256')]:
 data=(base/filename).read_bytes()
 assert hashlib.sha256(data).hexdigest()==request[field]==audit[field]
 assert etree.fromstring(data).tag=='products'
 assert len(data)<100000000
old=Path('pigu/PHH_STOCK_PRICES.xml')
blob=old.read_bytes();git_hash=hashlib.sha1(b'blob '+str(len(blob)).encode()+b'\0'+blob).hexdigest()
assert git_hash==request['expected_existing_prices_blob_sha'],'Live price file changed; review before overwriting'
backup=base/'before_full_publication';backup.mkdir(exist_ok=True)
shutil.copy2(old,backup/'PHH_STOCK_PRICES.xml')
for filename in ['PHH_PRODUCTS_FULL.xml','PHH_STOCK_PRICES.xml']:
 shutil.copy2(base/filename,Path('pigu')/filename)
status={'status':'published_to_github','source_products':audit['source_products'],'selected_products':audit['selected_products'],'selected_variants':audit['selected_variants'],'excluded_products':audit['excluded_products'],'content_sha256':audit['content_sha256'],'offers_sha256':audit['offers_sha256'],'content_url':'https://raw.githubusercontent.com/Decords/testfolder/main/pigu/PHH_PRODUCTS_FULL.xml','price_url':'https://raw.githubusercontent.com/Decords/testfolder/main/pigu/PHH_STOCK_PRICES.xml','pmp_settings_changed':False,'pmp_import_result':'not_verified','shopify_cdn_replacement':'not_completed'}
(base/'publication_status.json').write_text(json.dumps(status,ensure_ascii=False,indent=2))
print(json.dumps(status,ensure_ascii=False))
