import unittest,json,sys
from decimal import Decimal as D
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from tier_logic import *
class TierTests(unittest.TestCase):
    def test_boundaries(self):
        for q,expected in [(0,[]),(19999,[19999]),(20000,[20000]),(20001,[20000,1]),(40000,[20000,20000]),(40001,[20000,20000,1])]:
            self.assertEqual(marginal_allocation(q),list(map(D,expected)))
    def test_marginal_not_retroactive(self):
        self.assertEqual(capital_total(20001,100)-capital_total(20000,100),D(110))
        self.assertEqual(capital_total(40001,100)-capital_total(40000,100),D(121))
        self.assertEqual(capital_total(45000,100),D(4805000))
    def test_cross_zone_sum(self):
        rows=[dict(technology='CC',tier=1,new_mw=12000,zone=1),dict(technology='CC',tier=1,new_mw=8000,zone=2),dict(technology='CC',tier=2,new_mw=1,zone=9)]
        self.assertEqual(validate_allocation(rows)['CC',1],D(20000))
        rows[1]['new_mw']=8001
        with self.assertRaises(ValueError):validate_allocation(rows)
    def test_no_skipped_block(self):
        with self.assertRaises(ValueError):validate_allocation([dict(technology='CC',tier=2,new_mw=1)])
    def test_independent_technologies(self):
        validate_allocation([dict(technology=t,tier=1,new_mw=20000) for t in ['CC','PV']])
    def test_efficiency_product(self):
        for rte in ['0.85','0.80']:
            a,b=split_efficiency(rte);self.assertAlmostEqual(float(a*b),float(rte),places=14)
    def test_finance_once(self):
        self.assertEqual(annualize(1000,.08),D(80000))
        with self.assertRaises(ValueError):annualize(80000,.08,already_annualized=True)
    def test_candidates_and_gates(self):
        site=dict(candidate_id='X',technology='Battery',zone=1,site_group='one',site_limit_mw=25000,profile_source='TEST_ONLY',annual_capital_per_mw=100,annual_capital_per_mwh=50,earliest_online_year=2030)
        rows=expand_candidates([site],3,2030)
        self.assertEqual([r['annual_capital_per_mwh'] for r in rows],['50','55.0','60.50'])
        self.assertTrue(all(r['existing_mw']==0 and r['site_group']=='one' for r in rows))
        self.assertEqual(expand_candidates([site],3,2029),[])
        with self.assertRaises(ValueError):expand_candidates([site],3,None)
        with self.assertRaises(ValueError):expand_candidates([dict(site,requires_feedstock=True)],3,2030)
if __name__=='__main__':
    suite=unittest.defaultTestLoader.loadTestsFromTestCase(TierTests)
    result=unittest.TextTestRunner(verbosity=2).run(suite)
    Path(__file__).with_name('test-results.json').write_text(json.dumps(dict(tests=result.testsRun,failures=len(result.failures),errors=len(result.errors),solve_performed=False),indent=2))
    raise SystemExit(not result.wasSuccessful())
