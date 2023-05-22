import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pydeck as pdk

# Multipaging involving Page title and Icon.
# Note: The 1_📈_Data_Visualisation file name is for visual representation on Streamlit (Multipaging feature)
st.set_page_config(page_title="Data Visualisation", page_icon="📈")

# Sidebar
st.sidebar.header("📈 Data Visualisation")


# Loading the Dataset + Caching
# (data is sorted by the ID column in ascending order)
# encoding is set to "ISO-8859-1" because UTF8 encoding wasn't able to successfully analyze my dataset
@st.cache_data
def load_data():
    return pd.read_csv("https://docs.google.com/spreadsheets/d/e/2PACX-1vRpgZND22CxTxRyUdeRhMUgCVX8Pxph9NDb8_NE2lUKPyND4MsNYi62YNbrI1pU8g/pub?output=csv",
                       encoding="ISO-8859-1").set_index("ID").sort_values(by=['ID'])


# Filter the data. Default value for max_payment argument is 1000.
# Filters the data by selection
# Also filters out the rows that have no coordinates using & statement
def filter_data(license_type, sel_business_cities, max_payment=1000):
    df = load_data()
    df = df.loc[df['establishment_city'].isin(sel_business_cities)]
    df = df.loc[df["PMT_AMOUNT"] <= max_payment]
    df = df.loc[df['license_type'].isin(license_type)]
    df = df.loc[(df['latitude'].isna() == False) & (df['longitude'].isna() == False)]
    return df


# Generates a list of all cities
# Cities are sorted from most common to least common using lambda
# Values that don't have a establishment_city value are filtered out
def all_cities():
    df = load_data()
    lst = []
    all_occurrences_lst = []
    for ind, row in df.iterrows():
        all_occurrences_lst.append(str(row["establishment_city"]).title())
        if str(row["establishment_city"]).title() not in lst and str(row["establishment_city"]).title() != "Nan":
            lst.append(str(row["establishment_city"]).title())

    lst = sorted(lst, key=lambda x: all_occurrences_lst.count(x), reverse=True)
    return lst


# Generates a list of all license types:
# License Types are sorted from most common to least common using lambda
def all_license_types():
    df = load_data()
    lst = []
    all_occurrences_lst = []
    for ind, row in df.iterrows():
        all_occurrences_lst.append(row["license_type"])
        if row["license_type"] not in lst:
            lst.append(row["license_type"])

    lst = sorted(lst, key=lambda x: all_occurrences_lst.count(x), reverse=True)
    return lst


# Count the frequency of cities in data
def count_cities(cities, df):
    return [df.loc[df["establishment_city"].isin([city])].shape[0] for city in cities]


# Get license payment amounts for cities in the dataframe
def city_payments(df):
    payments = [row["PMT_AMOUNT"] for ind, row in df.iterrows()]
    cities = [row["establishment_city"].title() for ind, row in df.iterrows()]

    dict = {}
    for city in cities:
        dict[city] = []

    for i in range(len(payments)):
        dict[cities[i]].append(payments[i])

    return dict


# Get average payment amounts by city
def city_averages(dict_payments):
    dict = {}
    for key in dict_payments.keys():
        dict[key] = np.mean(dict_payments[key])

    return dict


# Generate a Pie Chart displaying the Market Share between cities
# Largest city is visually exploded on the Pie Chart
# Pie Chart generation is based on examples from the CIS Sandbox YouTube video with changes according to my code: https://www.youtube.com/watch?v=8G4cD7ofgCM&ab_channel=cissandbox
def generate_pie_chart(counts, sel_cities):
    plt.figure()
    explodes = [0 for i in range(len(counts))]
    maximum = counts.index(np.max(counts))
    explodes[maximum] = 0.10
    plt.pie(counts, labels=sel_cities, explode=explodes, autopct="%.2f")
    plt.title(f"Market Share of Cities: {', '.join(sel_cities)}")

    return plt


# Generate a Bar Chart displaying the average prices between cities
# X Labels are rotated by 45 degrees for more convenience
# Bar Chart generation is based on examples from the CIS Sandbox YouTube video with changes according to my code: https://www.youtube.com/watch?v=8G4cD7ofgCM&ab_channel=cissandbox
def generate_bar_chart(dict_averages):
    plt.figure()
    x = dict_averages.keys()
    y = dict_averages.values()
    plt.bar(x, y)
    plt.xticks(rotation=45)
    plt.ylabel("Average Payment")
    plt.xlabel("City")
    plt.title(f"Average License Payment in Cities: {', '.join(dict_averages.keys())}")

    return plt


# Generate a PyDeck Map
# Zoom is set to 8 to cover most of Massachusetts
# Map Generation was changed a lot due to the complexity of my dataset. PyDeck was having errors with some rows in my dataset having no values.
# So, had to additionally filter out rows with no coordinates to solve the JSON "Nan" errors (Look: filter_data() function)
def generate_map(df):
    map_df = df.filter(["business_name", "latitude", "longitude"])

    # map_df = pd.DataFrame(map_df, columns=["business_name", "latitude", "longitude"])

    view_state = pdk.ViewState(latitude=map_df["latitude"].mean(),
                               longitude=map_df["longitude"].mean(),
                               zoom=8)

    layer = pdk.Layer("ScatterplotLayer",
                      data=map_df,
                      get_position="[longitude, latitude]",
                      get_radius=400,
                      get_color=[20, 175, 250],
                      pickable=True)

    tool_tip = {'html': 'Establishment Name:<br/> <b>{business_name}</b>',
                'style': {'backgroundColor': 'steelblue', 'color': 'white'}}

    map = pdk.Deck(map_style='mapbox://styles/mapbox/light-v9',
                   initial_view_state=view_state,
                   layers=[layer],
                   tooltip=tool_tip, )

    map.to_html()
    st.pydeck_chart(map)


# Generate a chart of cities with the most establishments
# X Labels are rotated by 45 degrees for more convenience
def generate_most_establishments_chart():
    # n_cities = st.slider(0, 100)
    most_popular_cities = all_cities()[0:8]
    df = load_data()
    dict_cities_count = {most_popular_cities[i]: 0 for i in range(0, len(most_popular_cities), 1)}
    for ind, row in df.iterrows():
        if str(row["establishment_city"]).title() in most_popular_cities:
            dict_cities_count[str(row["establishment_city"]).title()] += 1
    print(dict_cities_count)

    plt.figure()

    x = dict_cities_count.keys()
    y = dict_cities_count.values()

    plt.bar(x, y)
    plt.xticks(rotation=45)
    plt.ylabel("Number of Establishments")
    plt.xlabel("City")
    plt.title("Cities with the Highest Number of Establishments")

    st.pyplot(plt)


# Main function that displays and runs all information on the Data Visualisation Page
def main():
    st.title("# Data Visualisation with Python 📈")
    st.write('View the data on Medicine Establishment License and Applications - Approved in Massachusetts!')
    st.write('Open the **:green[sidebar]** to start!')
    st.sidebar.write("Please select your options to display data")

    # Streamlit Checkboxes to choose which Data to View
    filtered_licenses = all_license_types()
    for item in filtered_licenses:
        if "Marijuana" in item:
            item = item.replace("Marijuana", '')
    
    license_type = st.sidebar.multiselect("Select License Type: ", filtered_licenses)
    
    
    cities = st.sidebar.multiselect("Select a City: ", all_cities())
    max_payment = st.sidebar.slider("Maximum License Payment: ", 0, 2000, 1000)

    data = filter_data(license_type, cities, max_payment)
    series = count_cities(cities, data)

    # Only Shows Checkboxes if the User selected the options on the Sidebar
    if len(license_type) > 0 and len(cities) > 0 and max_payment > 0:

        st.header('Select the Data You Want to View:')
        map_select = st.checkbox('View Map')
        pie_chart_select = st.checkbox('View Pie Chart')
        bar_chart_select = st.checkbox('View Bar Chart')

        if map_select:
            st.subheader("Map of Medicine Business Locations in Massachusetts: ")
            generate_map(data)

        if pie_chart_select:
            st.subheader("Market Share Pie Chart: ")
            st.pyplot(generate_pie_chart(series, cities))

        if bar_chart_select:
            st.subheader("Average License Payment Bar Chart: ")
            st.pyplot(generate_bar_chart(city_averages(city_payments(data))))

        st.divider()
        # Additional Bar Chart based General Data using Streamlit Button
        st.write("\n")
        st.subheader("\nGenerate Additional Information:")
        if st.button('View cities with most establishments'):
            generate_most_establishments_chart()
        else:
            st.write("")


main()
