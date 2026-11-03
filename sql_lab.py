"""Scoped, bounded, read-only SQLite queries over the uploaded workbook."""
import sqlite3,time
import pandas as pd
from data_model import analytics

STARTERS={
 'products': 'SELECT p.name AS product, SUM(t.transactions) AS transactions\nFROM transactions t JOIN products p USING(product_id)\nGROUP BY p.product_id, p.name ORDER BY transactions DESC;',
 'customers': 'SELECT c.name AS customer, c.sector, SUM(t.transactions) AS transactions\nFROM transactions t JOIN customers c USING(customer_id)\nGROUP BY c.customer_id, c.name, c.sector ORDER BY transactions DESC LIMIT 10;',
 'monthly': 'SELECT month, SUM(transactions) AS transactions\nFROM transactions GROUP BY month ORDER BY month;',
}

def run_query(data,query,context=None,max_rows=500,timeout=2):
    started=time.perf_counter()
    if not isinstance(query,str) or not query.strip():return {'error':'Enter a SELECT query.','rows':[],'columns':[]}
    if len(query)>12000:return {'error':'Query is too long.','rows':[],'columns':[]}
    a=analytics(data,context);ids=a['customer_ids'];c=pd.DataFrame(data['Customers']);p=pd.DataFrame(data['Products']);l=a['links'];l=l[l.customer_id.isin(ids)]
    con=sqlite3.connect(':memory:')
    try:
        for name,df in [('customers',c[c.customer_id.isin(ids)]),('products',p[p.product_id.isin((context or {}).get('products') or p.product_id)]),('relationships',l),('transactions',a['rows'])]:df.to_sql(name,con,index=False,if_exists='replace')
        # Only database reads, SELECT and an allowlist of scalar/aggregate functions.
        funcs={'sum','count','avg','min','max','round','coalesce','ifnull','nullif','abs','lower','upper','length','substr','substring','date','strftime','printf','cast','total','typeof','trim','ltrim','rtrim','replace','row_number','rank','dense_rank'}
        def authorize(action,arg1,arg2,db,source):
            if action in (sqlite3.SQLITE_SELECT,sqlite3.SQLITE_READ,sqlite3.SQLITE_RECURSIVE):return sqlite3.SQLITE_OK
            if action==sqlite3.SQLITE_FUNCTION and (arg2 or arg1 or '').lower() in funcs:return sqlite3.SQLITE_OK
            return sqlite3.SQLITE_DENY
        con.set_authorizer(authorize)
        deadline=time.monotonic()+timeout
        con.set_progress_handler(lambda:int(time.monotonic()>deadline),1000)
        cur=con.execute(query)
        if cur.description is None:raise ValueError('Only SELECT queries are supported.')
        cols=[d[0] for d in cur.description]
        if len(set(cols))!=len(cols):raise ValueError('Use unique aliases for result columns.')
        values=cur.fetchmany(max_rows+1);truncated=len(values)>max_rows
        rows=[dict(zip(cols,r)) for r in values[:max_rows]]
        return {'rows':rows,'columns':cols,'truncated':truncated,'elapsed_ms':round((time.perf_counter()-started)*1000),'error':None,'context':context or {}}
    except (sqlite3.Error,ValueError) as exc:return {'error':str(exc),'rows':[],'columns':[],'elapsed_ms':round((time.perf_counter()-started)*1000),'context':context or {}}
    finally:con.close()
