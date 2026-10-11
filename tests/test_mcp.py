import json,unittest
from api.mcp import buscar_normas,ler_pagina,listar_documentos,DOCS
class CorpusTests(unittest.TestCase):
 def test_inventory(self):
  docs=listar_documentos()['documents'];self.assertEqual(len(docs),9);self.assertEqual(sum(d['page_count'] for d in docs),411)
 def test_page_and_search(self):
  doc='rgf-atualizado-26cd43f5';a=buscar_normas('admissão',doc);b=buscar_normas('admissao',doc)
  self.assertTrue(a['results']);self.assertEqual(a['results'],b['results'])
  for hit in a['results']:
   page=ler_pagina(hit['document_id'],hit['page']);self.assertIn(hit['excerpt'],page['text']);self.assertEqual(hit['source_sha256'],page['source_sha256'])
 def test_substantive_pages_rank_ahead_of_table_of_contents(self):
  pages=[hit['page'] for hit in buscar_normas('admissão','rgf-atualizado-26cd43f5',limit=5)['results']]
  self.assertIn(12,pages)
  self.assertNotIn(4,pages)
 def test_no_fabricated_results(self):self.assertEqual(buscar_normas('zzzxxyyqnonexistent')['results'],[])
 def test_boundaries(self):
  for doc,page in [('../secret',1),('rgf-atualizado-26cd43f5',110)]:
   with self.assertRaises(ValueError):ler_pagina(doc,page)
  with self.assertRaises(ValueError):buscar_normas('a o e')
 def test_redactions(self):
  for doc in DOCS.values():
   for p in doc['pages']:self.assertNotRegex(p['text'],r'(?<!\d)\d{11}(?!\d)')
if __name__=='__main__':unittest.main()
