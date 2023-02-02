import streamlit as st
from datetime import date
from extract_tweets import extract_tweets
from net import model 

app = st.container()

with app:
    with st.form("app_form"):
        text = st.text_input(label = 'Insert text',
                    value = 'It is the oldest mummy, complete and covered in gold, ever found in Egypt.')
        num_keywords = st.slider('number of keywords', 1, 3, 1)
        set_keywords = st.slider('set of keywords', 1, 3, 1)
        current_date = date.today()
        date_since = st.date_input('from which date:',current_date)
        date_until = st.date_input('until which date:',current_date)
        submitted = st.form_submit_button("Submit")
        if submitted:
            tweet_df = extract_tweets(text,date_since,date_until)
            info = model(tweet_df,
                keyphrase_ngram_range = (1,num_keywords),top_n=set_keywords)
            st.pyplot(info.overall_emotion())
            st.pyplot(info.plot_keywords())
