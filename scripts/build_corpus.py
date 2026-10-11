"""Build the public page index from a supplied, audited plugin source."""
import hashlib,json,re,sys
from pathlib import Path
source=Path(sys.argv[1]);dest=Path(__file__).resolve().parents[1]/'corpus';dest.mkdir(exist_ok=True)
manifest=json.loads((source/'manifest.json').read_text(encoding='utf-8'));docs=[]
for item in manifest:
 ref=source/'skills'/item['id']/'references';md=(ref/'fonte-integral.md').read_text(encoding='utf-8');coverage=json.loads((ref/'cobertura.json').read_text(encoding='utf-8'));pages=[]
 assert hashlib.sha256((source/'originals'/item['filename']).read_bytes()).hexdigest()==item['sha256']
 for p in coverage['pages']:
  section=md.split(f'<!-- PDF2SKILL_PAGE_START:{p["page"]} -->',1)[1]
  text=section.split(p['fence']+'text\n',1)[1][:p['text_characters']]
  assert hashlib.sha256(text.encode()).hexdigest()==p['rendered_markdown_text_sha256']
  # Do not expose personal tax identifiers embedded in signature blocks.
  text,n=re.subn(r'(?<!\d)(?:\d{3}\.\d{3}\.\d{3}-\d{2}|\d{11})(?!\d)','[identificador pessoal omitido]',text)
  pages.append({'page':p['page'],'text':text,'method':p['method'],'flags':p['flags'],'personal_identifiers_redacted':n})
 document={'id':item['id'],'title':item['filename'].removesuffix('.pdf'),'source_sha256':item['sha256'],'page_count':item['pages'],'currency':'Não verificada; o nome ATUAL/ATUALIZADO não comprova vigência.','pages':pages}
 (dest/(item['id']+'.json')).write_text(json.dumps(document,ensure_ascii=False,separators=(',',':'))+'\n', encoding='utf-8')
 docs.append({k:v for k,v in document.items() if k!='pages'})
(dest/'catalog.json').write_text(json.dumps(docs,ensure_ascii=False,indent=2)+'\n', encoding='utf-8')
print(json.dumps({'documents':len(docs),'pages':sum(d['page_count'] for d in docs),'bytes':sum(p.stat().st_size for p in dest.glob('*.json'))}))
