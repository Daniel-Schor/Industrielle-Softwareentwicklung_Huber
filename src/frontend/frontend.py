import streamlit as st

st.set_page_config(page_title="Analytics", layout="wide")

recommendations = st.Page("pages/recommendations.py", title="Find Best Country match",
                          icon=":material/query_stats:")
analysis = st.Page("pages/analysis.py", title="Detailed Country analysis",
                   icon=":material/query_stats:")
homepage = st.Page("pages/homepage.py", title="Homepage",
                   icon=":material/query_stats:")

# install Multipage
pg = st.navigation({
    "Insights": [homepage, recommendations, analysis],
})
pg.run()
