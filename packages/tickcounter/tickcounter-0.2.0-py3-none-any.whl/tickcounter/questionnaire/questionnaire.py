import pandas as pd
from itertools import combinations
from scipy.stats import ttest_ind, chisquare
from ..util import generate_name

from tickcounter import plot, statistics

class Questionnaire(object):
    def __init__(self, data, scoring, descrip=None):
        self.data = data.copy() # Original data
        self.descrip = descrip # Used for plotting and analysis, takes a Description object
        self._cached = {
            "transform": None, # Will only contain transformed columns
            "score": None,
            "label": None,
            "data": self.data,
        }
        self.scoring = scoring if isinstance(scoring, list) else [scoring] # Used for calculating score
    
    def transform(self):
        if self._cached['transform'] is not None:
            return self._cached['transform']

        else:
            data = None
            # Will change this to support MultiEncoder in the future.
            for i in self.scoring:
                cur_data = i.transform(self.data[i.columns])
                if data is None:
                    data = cur_data
                else:
                    data = pd.concat([data, cur_data], axis=1)
            self._cached['transform'] = data
            return data

    def score(self):
        if self._cached['score'] is not None:
            return self._cached['score']
        
        else:
            result_df = None
            for i in self.scoring:
                score_ss = i.score(self.data)
                
                if result_df is None:
                    result_df = pd.DataFrame([score_ss]).T
                
                else:
                    result_df = pd.concat([result_df, score_ss], axis=1)
            
            self._cached['score'] = result_df
            self._cached['data'] = pd.concat([self._cached['data'], self._cached['score']], axis=1)
            return result_df

    def label(self):
        if self._cached['label'] is not None:
            return self._cached['label']

        else:
            data = None
            if self._cached['score'] is not None:
                data = self._cached['data']
            
            else:
                self.score()
                data = self._cached['data']

            label_df = None
            for scoring in self.scoring:
                cur_label_df = scoring.label(data, scoring.score_col)
                
                if label_df is None:
                    label_df = cur_label_df 
                
                else:
                    label_df = pd.concat([label_df, cur_label_df], axis=1)
            self._cached['label'] = label_df
            self._cached['data'] = pd.concat([self._cached['data'], label_df], axis=1)
            return label_df

    def _plot(self, columns, kind, transformed, **kwargs):
        data = None
        if self._cached['label'] is not None:
            data = self._cached['data']
        
        else:
            self.label()
            data = self._cached['data']
        if transformed:
            data[self.item_col] = self._cached['transform']
        plot.plot_each_col(data, col_list = columns, plot_type=kind, **kwargs)

    def hist_label(self, *, transformed=True, separated=False, **kwargs):
        self._plot(columns = self.label_col, kind='hist', transformed=transformed, **kwargs)

    def hist_item(self, *, transformed=True, separated=False, **kwargs):
        self._plot(columns = self.item_col, kind='hist', transformed=transformed, **kwargs)
    
    def hist_score(self, *, transformed=True, separated=False, **kwargs):
        self._plot(columns = self.score_col, kind='hist', transformed=transformed, **kwargs)

    def boxplot_score(self, *, transformed=True, separated=False, **kwargs):
        self._plot(columns = self.score_col, kind='box', transformed=transformed, **kwargs)
    
    def boxplot_item(self, *, transformed=True, separated=False, **kwargs):
        self._plot(columns = self.item_col, kind='box', transformed=transformed, **kwargs)
    
    def count_label(self, *, transformed=True, separated=False, **kwargs):
        self._plot(columns = self.label_col, kind='count', transformed=transformed, **kwargs)
    
    def diff_item(self, col, transformed=True):
        if col not in self._cached['data'].columns:
            self.label()
        
        if transformed:
            df = self._cached['data'].copy()
            df[self.item_col] = self.transform()
        
        else:
            df = self._cached['data']

        return statistics._diff_group(df, group_col=col, num_col=self.item_col)
    
    def crosstab(self, index, col):
        # Should be a label paired with an info columns
        self.label()
        return pd.crosstab(self._cached["data"][index], self._cached["data"][col])
    
    def t_test_group(self, item, info_col, **kwargs):
        df = self._cached['data']
        if info_col not in self._cached['data'].columns:
            self.label()
            df = self._cached['data']
        return statistics._t_test_group(data=df, group_col=info_col, num_col=item, **kwargs)
    
    def t_test(self, num_col, group_col, group_1, group_2, **kwargs):
        self.label()
        df = self._cached['data']
        return statistics._t_test(df, num_col, group_col, group_1, group_2, **kwargs)
        
    def chi_squared_dependence(self, col_1, col_2, min_sample=None):
        self.label()
        df = self._cached['data']

        if min_sample is None:
            group_1 = df[col_1].value_counts().index
            group_2 = df[col_2].value_counts().index
        
        else:
            group_1, _ = statistics._filter_sparse_group(df, col_1, min_sample)
            group_2, _ = statistics._filter_sparse_group(df, col_2, min_sample)

        return statistics._chi_squared_dependence(df, col_1, col_2, group_1, group_2)

    def cluster(self, scoring):
        # Use KMeans clustering to cluster the response to something
        pass

    def drop(self, idx):
        self.data.drop(idx, inplace=True)
        self.reset_cache()

    def reset_cache(self):
        self._cached = {
            "transform": None,
            "score": None,
            "label": None,
            "data": self.data,
        }
    
    @property
    def score_col(self):
        if self._cached['score'] is not None:
            return self._cached['score'].columns
        
        else:
            self.score()
            return self._cached['score'].columns
    
    @property
    def label_col(self):
        if self._cached['label'] is not None:
            return self._cached['label'].columns
        
        else:
            self.label()
            return self._cached['label'].columns
    
    @property
    def item_col(self):
        if self._cached['transform'] is not None:
            return self._cached['transform'].columns
        
        else:
            self.transform()
            return self._cached['transform'].columns
    
    def __getitem__(self, col):
        try:
            return self._cached['data'][col]

        except KeyError:
            self.label()
            return self._cached['data'][col]

    