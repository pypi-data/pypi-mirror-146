from jdw.kdutils.singleton import Singleton
from .. fetch_engine import FetchEngine
import pandas as pd
import six,os,pdb
os.environ
@six.add_metaclass(Singleton)
class FetchKNEngine(FetchEngine):
    def __init__(self, name=None, uri=None):
        if uri is None and name is None:
            super(FetchKNEngine, self).__init__('KN',os.environ['KN_MG'])
        else:
            super(FetchKNEngine, self).__init__(name, uri)
        
        self._factor_tables = {
            'factor_basis':self.automap(table_name='factor_basis'),
            'factor_fundamentals':self.automap(table_name='factor_fundamentals'),
            'factor_momentum':self.automap(table_name='factor_momentum'),
            'factor_position':self.automap(table_name='factor_position'),
            'factor_term_structure':self.automap(table_name='factor_term_structure')
        }

    
    def _map_factors(self, factors, used_factor_tables, diff_columns={'trade_date','code'}):
        factor_cols = {}
        factors = set(factors).difference(diff_columns)
        to_keep = factors.copy()
        for t in factors:
            for k,v in used_factor_tables.items():
                if t in v:
                    if k in factor_cols:
                        factor_cols[k].append(t)
                    else:
                        factor_cols[k] =  [t]
                    to_keep.remove(t)
                    break
        if to_keep:
            raise ValueError("factors in <{0}> can't be find".format(to_keep))
        return factor_cols

    def _general_query(self, **kwargs):
        query = {}
        if 'begin_date' in kwargs and 'end_date' in kwargs:
            query['trade_date'] = {"$gte": kwargs['begin_date'],
                                   "$lte": kwargs['end_date']
            }
        if 'codes' in kwargs:
            query['code'] = {'$in':kwargs['codes']}
        return query

    def _filter_columns(self, result):
        if not result.empty:
            result =  result.drop(['_id'],axis=1) if '_id' in result.columns else result
            result =  result.drop(['flag'],axis=1) if 'flag' in result.columns else result
            result =  result.drop(['timestamp'],axis=1) if 'timestamp' in result.columns else result
        return result

    def _base_dabase(self, **kwargs):
        query = self._general_query(**kwargs)
        columns = kwargs['columns'] if 'columns' in kwargs else None
        result = self.base(table_name=kwargs['table_name'],query=query,columns=columns)
        result = pd.DataFrame(result)
        return self._filter_columns(result)
        
    def market_pre_fut(self, **kwargs):
        return self._base_dabase(**kwargs)
    
    def fut_fundamenal(self, **kwargs):
        return self._base_dabase(**kwargs)
    
    def research(self, **kwargs):
        return self._base_dabase(**kwargs)

    def market_index_fut(self, **kwargs):
        return self._base_dabase(**kwargs)

    def fut_factor(self, **kwargs):
        res =[]
        factor_cols = self._map_factors(factors=kwargs['columns'],
                        used_factor_tables=self._factor_tables)
        for t,c in factor_cols.items():
            df = self._base_dabase(table_name=t, 
                begin_date=kwargs['begin_date'], end_date=kwargs['end_date'],
                codes=kwargs['codes'],columns=c + ['trade_date','code'])
            res.append(df.set_index(['trade_date','code']))
        return pd.concat(res, axis=1).reset_index()




        