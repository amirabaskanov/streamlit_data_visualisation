import streamlit as st

# Multipaging involving Page title and Icon.
st.set_page_config(
    page_title="Welcome to Data Analysis with Python",
    page_icon="👋",
)

# Streamlit Text Title
st.title("# Welcome to Data Analysis with Python 👋")

# Sidebar Note
st.sidebar.header("Pages")
st.sidebar.success("Select a page above ⬆️")


url = "https://bentleyedu-my.sharepoint.com/:x:/r/personal/mfrydenberg_bentley_edu/_layouts/15/Doc.aspx?sourcedoc=%7BD58772AD-370E-4EEE-AA28-C85DC9EA0C88%7D&file=Cannabis_MA.csv&action=default&mobileredirect=true"
st.header('General Info:')
st.markdown(
    """
    **:green[Name:]** Amir Abaskanov
    \n**:green[CS230:]** Section 3
    \n**:green[Dataset:]** Medical Establishment License and Applications - Approved in Massachusetts
    \n
    \n**Description:**
    \nThis program uses data from :green[Hospitals_MA.csv] and displays establishments
    based in Massachusetts on a **map**, filters establishments by **license type**,
    and also filters these establishments by their **maximum license payment**. 
    \nThis program shows a **Map** of the establishments, **Pie Chart** displaying 
    the market share in different cities, and a **Bar Chart** comparing average 
    prices of license payments in cities
    """
)
st.header('Design:')
st.markdown(
    """
    **:green[Three examples of queries/questions about my dataset:]**
    1. Find all Establishments with license_type = Medicine Retailers
    located in Worcester, Boston, and Cambridge, with PMT_AMOUNT < 1500
    2. Find all Establishments that are located in Lowell with 
    license_type = Medicine Cultivators 
    3. Find all Medicine Product Manufacturers and Medicine Microbusinesses, 
    that are located in Holyoke, with PMT_AMOUNT less than 1200
    """
)

st.markdown(
    """
    **:green[Streamlit Widgets:]**
    1. Two MultiSelects for License Type and Establishment City
    2. Slider for PMT_AMOUNT
    3. Checkboxes to select what Data to view
    4. Button to generate additional information
    """
)

st.markdown(
    """
    **:green[Additional Implementations:]** 
    1. Streamlit Sidebar
    2. Streamlit Multipaging
    3. Streamlit Caching
    4. Lambda sorting function
    5. Streamlit text elements
    """
)

st.divider()
st.header('Bibliography:')
st.markdown(
    """
    \nStreamlit Text elements: https://docs.streamlit.io/library/api-reference/text
    \nStreamlit Chart elements: https://docs.streamlit.io/library/api-reference/charts
    \nStreamlit Input Widgets: https://docs.streamlit.io/library/api-reference/widgets
    \nStreamlit Cache: https://docs.streamlit.io/library/advanced-features/caching
    \nStreamlit Multipaging: https://docs.streamlit.io/library/get-started/multipage-apps/create-a-multipage-app
    \nPandas Documentation User Guide: https://pandas.pydata.org/docs/user_guide/index.html
    \nCIS Sandbox CS230 Final Project Example (YouTube): https://www.youtube.com/watch?v=8G4cD7ofgCM&ab_channel=cissandbox
    
    """
)
