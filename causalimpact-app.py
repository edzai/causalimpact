import pandas as pd
from causalimpact import CausalImpact
import streamlit as st
import datetime

st.markdown("""
<style>
.big-font {
    font-size:50px !important;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<p class="big-font">Measure Causal Impact</p>
<p>Predict the click outcome as if an SEO change/event never took place. Helpful to understand impact in lou of an experiment</p>
<b>Directions: </b></ br><ol>
<li>Read the tutorial on <a href="https://importsem.com/measure-causal-impact-from-gsc-data-using-python">importSEM</a></li>
<li>Upload GSC date data sheet export</li>
<li>Identify the exact date of a major SEO event or change</li>
<li>Identify the pre-period range and post-period range. X days before and matching X days after</li>
</ol>
""", unsafe_allow_html=True)

st.set_option('deprecation.showPyplotGlobalUse', False)

with st.form("user-details"):
    getdata = st.file_uploader("Upload your GSC Date CSV",type=['csv'])
    
    pre_start = st.date_input("Pre Period Start Date")
    pre_end = st.date_input("Pre Period End Date")
        
    post_start = st.date_input("Post Period Start Date")
    post_end = st.date_input("Post Period End Date")

    
    submitted = st.form_submit_button("Process")
    if submitted:
        st.markdown("Processing data and graphs... :sunglasses:")
        
        if pre_start > pre_end:
            st.error("Pre-Period Range Invalid")
    
        if post_start > post_end:
            st.error("Post-Period Range Invalid")
        
        data = pd.read_csv(getdata, 
                         usecols=[0,1,2,4], 
                         header=0,
                         encoding="utf-8-sig",
                         index_col='Date')

        data = data.groupby(['Date'], as_index=True, sort=False, group_keys=True)[["Clicks", "Impressions"]].sum().reset_index()
        data_new = data.set_index('Date')
        data = data_new

        data.sort_values(by=['Date'], inplace=True, ascending=True)

        #pre_period = ["2021-06-20", "2021-06-27"]
        #post_period = ["2021-06-28", "2021-07-05"]
        
        pre_period = [str(pre_start), str(pre_end)]
        post_period = [str(post_start), str(post_end)]

        #ci = CausalImpact(data.iloc[:, 0], pre_period, post_period, nseasons=[{'period': 52}])
        ci = CausalImpact(data, pre_period, post_period, prior_level_sd=None)
        st.title("Causal Impact Data")
        summary = ci.summary()
        summary = summary.replace("Posterior Inference {Causal Impact}","")
        summary = summary.replace("For more details run the command: print(impact.summary('report'))","")
        st.markdown("<pre>" + summary + "</pre>", unsafe_allow_html=True)
        st.title("Causal Impact Graphs")
        ci.plot()
        st.pyplot()
        st.title("Causal Impact Summary")
        st.write(ci.summary(output='report'))

st.write('App Author: [Greg Bernhardt](https://twitter.com/GregBernhardt4) | Friends: [Rocket Clicks](https://www.rocketclicks.com) and [Physics Forums](https://www.physicsforums.com)')
