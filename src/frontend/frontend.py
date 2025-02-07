import streamlit as st

st.set_page_config(page_title="Analytics", layout="wide")

p1 = st.Page("pages/page1.py", title="Find Best Country match",
             icon=":material/query_stats:")
p2 = st.Page("pages/page2.py", title="Detailed Country analysis",
             icon=":material/query_stats:")
# p3 = st.Page("pages/page3.py", title="Page 3", icon=":material/query_stats:")

# install Multipage
pg = st.navigation({
    "Pages": [p1, p2],
})
pg.run()
