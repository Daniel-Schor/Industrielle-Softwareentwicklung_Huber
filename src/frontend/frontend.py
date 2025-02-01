import streamlit as st

st.set_page_config(page_title="Analytics", layout="wide")

p1 = st.Page("pages/page1.py", title="Page 1", icon=":material/query_stats:")
p2 = st.Page("pages/page2.py", title="Page 2", icon=":material/query_stats:")
p3 = st.Page("pages/page3.py", title="Page 3", icon=":material/query_stats:")

# install Multipage
pg = st.navigation({
    "Page 1": [p1],
    "Page 2": [p2, p3],
})
pg.run()

