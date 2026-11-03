import unittest
from pathlib import Path
from data_model import load_workbook
from sql_lab import run_query,STARTERS

class SQLLabTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.data=load_workbook(Path(__file__).parent/'data/customer_journey.xlsx')
 def test_reconcile(self):
  r=run_query(self.data,STARTERS['products']);self.assertIsNone(r['error']);self.assertEqual(sum(x['transactions'] for x in r['rows']),546530)
 def test_customer_scope(self):
  r=run_query(self.data,'SELECT SUM(transactions) AS n FROM transactions',{'customer':'C001','start':'2025-10-01','end':'2026-09-01'});self.assertEqual(r['rows'][0]['n'],390000)
 def test_no_writes_or_external_data(self):
  for q in ['DELETE FROM transactions','DROP TABLE customers',"ATTACH DATABASE '/tmp/x' AS x",'PRAGMA database_list',"SELECT load_extension('x')",'SELECT 1; SELECT 2']:
   with self.subTest(q=q):self.assertTrue(run_query(self.data,q)['error'])
 def test_cte_read(self):self.assertIsNone(run_query(self.data,'WITH c AS (SELECT count(*) AS n FROM customers) SELECT * FROM c')['error'])
 def test_city_scope(self):
  import json
  d=dict(self.data);d['Locations']=json.loads((Path(__file__).parent/'data/demo_locations.json').read_text())
  ctx={'city':'Riyadh','start':'2025-10-01','end':'2026-09-01'}
  from data_model import analytics
  a=analytics(d,ctx);r=run_query(d,'SELECT SUM(transactions) AS n FROM transactions',ctx)
  self.assertEqual(r['rows'][0]['n'],a['total']);self.assertEqual(len(a['customer_ids']),15)
 def test_arabic_assistant(self):
  from assistant import answer
  out=answer('Total transactions',self.data,{'customer':'C001','language':'ar','start':'2025-10-01','end':'2026-09-01'})
  self.assertIn('إجمالي المعاملات',out);self.assertIn('390,000',out)
 def test_limit(self):
  r=run_query(self.data,'SELECT * FROM transactions',max_rows=3);self.assertEqual(len(r['rows']),3);self.assertTrue(r['truncated'])
 def test_timeout(self):
  r=run_query(self.data,'WITH RECURSIVE t(n) AS (SELECT 1 UNION ALL SELECT n+1 FROM t) SELECT SUM(n) FROM t',timeout=.01);self.assertTrue(r['error'])
if __name__=='__main__':unittest.main()
