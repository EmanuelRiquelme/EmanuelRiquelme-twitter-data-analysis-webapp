import pandas as pd
from keybert import KeyBERT
from sentiment_model import Sentiment 
import matplotlib.pyplot as plt
import numpy as np

class model:
    def __init__(self,tweet_df,**kwargs):
        self.df = tweet_df
        self.keyword_model = KeyBERT()
        self.keybert_args = kwargs
        self.sentiment_score = self.__sentimient_eval__()
        self.keyword_df = self.__attention_mech__()

    def __sentimient_eval__(self):
        return Sentiment(self.df['Tweet'])
    def __attention_mech__(self):
        raw_keywords = self.keyword_model.extract_keywords(
            self.df['Tweet'],
            keyphrase_ngram_range = self.keybert_args['keyphrase_ngram_range'],
            top_n = self.keybert_args['top_n']
        )
        keywords_set,attention= [],[]
        for keywords,num_retweet,num_fav,sent_pred in zip(raw_keywords,self.df['Retweet'],self.df['Favs'],self.sentiment_score):
            for keyword in keywords:
                keywords_set.append(keyword[0])
                attention.append((1+num_retweet/2+num_fav/4)*sent_pred)
        keyword_df = {
            'keywords':keywords_set,
            'attention':attention
            }
        keyword_df = pd.DataFrame(keyword_df).groupby(['keywords'], as_index=False).sum()
        return keyword_df.sort_values(by=['attention'],ascending=False)

    def plot_keywords(self):
        upper = self.keyword_df[:5]
        bottom = self.keyword_df[-5:]
        df_plot = pd.concat([upper,bottom])
        fig, ax = plt.subplots(figsize =(15, 15))
        ax.barh(df_plot['keywords'], df_plot['attention'])
        plt.rcParams.update({'font.size': 35})
        return fig

    def overall_emotion(self):
        labels = ['negative','neutral','positive']
        _, count= np.unique(self.sentiment_score, return_counts=True)
        percentages = count/np.sum(count)
        fig, ax = plt.subplots()
        colors = ['#cc0404','#698c91','#03ddff']
        ax.pie(percentages, labels=labels,colors = colors)
        return fig
