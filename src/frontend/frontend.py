import streamlit as st

st.set_page_config(page_title="MoveSmart", layout="wide")

# Hide Streamlit menu
# hide_streamlit_style = """
#    <style>
#    #MainMenu {visibility: hidden;}
#    footer {visibility: hidden;}
#    header {visibility: hidden;}
#    </style>
# """
# st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# Load pages
recommendations = st.Page("pages/recommendations.py", title="Find Best Country match",
                          icon=":material/query_stats:")
analysis = st.Page("pages/analysis.py", title="Detailed Country analysis",
                   icon=":material/query_stats:")
homepage = st.Page("pages/homepage.py", title="Homepage",
                   icon=":material/query_stats:")

# Navigation
pg = st.navigation({
    "Insights": [homepage, recommendations, analysis],
})
pg.run()
