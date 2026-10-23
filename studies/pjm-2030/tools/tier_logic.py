"""Pure preparation logic; no optimizer, cloud access, or default planning year."""
from decimal import Decimal as D
from collections import defaultdict
BLOCK=D(20000)
def marginal_allocation(new_mw):
    q=D(str(new_mw))
    if q<0:raise ValueError('New MW cannot be negative')
    out=[]
    while q:
        x=min(q,BLOCK);out.append(x);q-=x
    return out
def capital_total(new_mw,base_annual_cost):
    return sum((x*D(str(base_annual_cost))*D('1.1')**k for k,x in enumerate(marginal_allocation(new_mw))),D(0))
def validate_allocation(rows):
    totals=defaultdict(lambda:D(0))
    for r in rows:
        if r['tier']<1 or D(str(r['new_mw']))<0:raise ValueError('Invalid tier/MW')
        totals[r['technology'],r['tier']]+=D(str(r['new_mw']))
    for (tech,k),mw in totals.items():
        if mw>BLOCK:raise ValueError('Shared PJM tier cap exceeded')
        if mw>0 and any(totals[tech,j]!=BLOCK for j in range(1,k)):
            raise ValueError('Earlier marginal block must fill first')
    return dict(totals)
def annualize(capex_per_kw,fcr,*,already_annualized=False):
    if already_annualized:raise ValueError('Do not annualize an annual cost twice')
    if capex_per_kw is None or fcr is None:raise ValueError('Documented capital basis and FCR required')
    if D(str(capex_per_kw))<=0 or not 0<D(str(fcr))<1:raise ValueError('Invalid finance inputs')
    return D(str(capex_per_kw))*1000*D(str(fcr))
def split_efficiency(rte):
    r=D(str(rte))
    if not 0<r<=1:raise ValueError('Invalid RTE')
    return r.sqrt(),r.sqrt()
def expand_candidates(sites,tiers,planning_year):
    if planning_year is None:raise ValueError('Planning year must be confirmed')
    if not isinstance(tiers,int) or tiers<1:raise ValueError('Explicit finite tier coverage required')
    result=[]
    for site in sites:
        for key in ['candidate_id','technology','zone','site_group','site_limit_mw','profile_source','annual_capital_per_mw','earliest_online_year']:
            if site.get(key) is None or site.get(key)=='':raise ValueError('Missing '+key)
        if site['site_limit_mw']<=0 or site['annual_capital_per_mw']<=0:raise ValueError('Positive documented cost and site limit required')
        if site.get('requires_feedstock') and (not site.get('feedstock_group') or not site.get('annual_feedstock_mmbtu')):raise ValueError('Feedstock budget required')
        if planning_year<site['earliest_online_year']:continue
        for k in range(1,tiers+1):
            row=dict(site,resource=f"NEW_{site['candidate_id']}_T{k:02d}",tier=k,existing_mw=0,capital_multiplier=str(D('1.1')**(k-1)))
            for cost in ['annual_capital_per_mw','annual_capital_per_mwh','annual_capital_charge_per_mw']:
                if cost in site:row[cost]=str(D(str(site[cost]))*D(row['capital_multiplier']))
            result.append(row)
    return result
