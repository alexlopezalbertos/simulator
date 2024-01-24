import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
from sklearn.preprocessing import StandardScaler
import math
import numpy as np
import requests
from bs4 import BeautifulSoup


# Function to render the Supply Chain Resilience Calculator page
def render_calculator_page():
    st.title("Supply Chain Resilience Simulator")
    st.write("")
    # Get user inputs
    input1 = st.number_input("__Lead Time (:blue[days])__", value=None, placeholder="Introduce Lead Time", step=1)
    if input1 is not None and type(input1) != int:
        st.warning("Please enter a number in integer format")
    st.write("")
    input2 = st.number_input("__Distance from Supplier to CM (:blue[km])__", value=None, placeholder="Introduce Distance", step=.1, format="%.1f")
    if input2 is not None and type(input2) != float:
        st.warning("Please enter a number format")
    st.write("")
    input3 = st.selectbox("__BCP Risk__", ["LOW", "MEDIUM", "HIGH"], index=None, placeholder="Choose an option")
    with st.expander("Help"):
        st.write(":green[LOW]: A backup supplier is identified.")
        st.write(":orange[MEDIUM]: No backup supplier is identified but either:")
        st.write("                 1. The primary supplier has at least 1 plant in another location.")
        st.write("                 2. There is another material either used and qualified for CM internal production or qualified by another P&G plant.")
        st.write(":red[HIGH]: No backup supplier is identified.")
    st.write("")
    # input4 = st.number_input("Fragility Index of the country of the supplier", 0.0)
    # input5 = st.number_input("Natural Disaster Risk of the country of the supplier (%)", 0.0)
    input6 = st.selectbox("__Supplier Country__", ['Albania', 'Algeria', 'Angola', 'Antigua and Barbuda', 'Argentina', 'Armenia', 'Australia', 'Austria', 'Azerbaijan', 'Bahamas', 'Bahrain', 'Bangladesh', 'Barbados', 'Belarus', 'Belgium', 'Belize', 'Benin', 'Bhutan', 'Bolivia', 'Bosnia and Herzegovina', 'Botswana', 'Brazil', 'Brunei', 'Bulgaria', 'Burkina Faso', 'Burundi', 'Cambodia', 'Cameroon', 'Canada', 'Cape Verde', 'Central African Republic', 'Chad', 'Chile', 'China', 'Colombia', 'Comoros', 'Congo', 'Costa Rica', 'Croatia', 'Cuba', 'Cyprus', 'Czechia', 'Denmark', 'Djibouti', 'Dominica', 'Dominican Republic', 'DR Congo', 'East Timor', 'Ecuador', 'Egypt', 'El Salvador', 'Equatorial Guinea', 'Eritrea', 'Estonia', 'Eswatini', 'Ethiopia', 'Fiji', 'Finland', 'France', 'Gabon', 'Gambia', 'Georgia', 'Germany', 'Ghana', 'Greece', 'Grenada', 'Guatemala', 'Guinea', 'Guinea-Bissau', 'Guyana', 'Haiti', 'Honduras', 'Hungary', 'Iceland', 'India', 'Indonesia', 'Iran', 'Iraq', 'Ireland', 'Israel', 'Italy', 'Ivory Coast', 'Jamaica', 'Japan', 'Jordan', 'Kazakhstan', 'Kenya', 'Kiribati', 'Kuwait', 'Kyrgyzstan', 'Laos', 'Latvia', 'Lebanon', 'Lesotho', 'Liberia', 'Libya', 'Liechtenstein', 'Lithuania', 'Luxembourg', 'Madagascar', 'Malawi', 'Malaysia', 'Maldives', 'Mali', 'Malta', 'Marshall Islands', 'Mauritania', 'Mauritius', 'Mexico', 'Micronesia', 'Moldova', 'Monaco', 'Mongolia', 'Montenegro', 'Morocco', 'Mozambique', 'Myanmar', 'Namibia', 'Nauru', 'Nepal', 'Netherlands', 'New Zealand', 'Nicaragua', 'Niger', 'Nigeria', 'North Korea', 'North Macedonia', 'Norway', 'Oman', 'Pakistan', 'Palau', 'Panama', 'Papua New Guinea', 'Paraguay', 'Peru', 'Philippines', 'Poland', 'Portugal', 'Qatar', 'Romania', 'Russia', 'Rwanda', 'Saint Kitts and Nevis', 'Saint Lucia', 'Saint Vincent and the Grenadines', 'Samoa', 'San Marino', 'São Tomé and Príncipe', 'Saudi Arabia', 'Senegal', 'Serbia', 'Seychelles', 'Sierra Leone', 'Singapore', 'Slovakia', 'Slovenia', 'Solomon Islands', 'Somalia', 'South Africa', 'South Korea', 'South Sudan', 'Spain', 'Sri Lanka', 'Sudan', 'Suriname', 'Sweden', 'Switzerland', 'Syria', 'Tajikistan', 'Tanzania', 'Thailand', 'Togo', 'Tonga', 'Trinidad and Tobago', 'Tunisia', 'Turkey', 'Turkmenistan', 'Tuvalu', 'Uganda', 'Ukraine', 'United Arab Emirates', 'United Kingdom', 'United States', 'Uruguay', 'Uzbekistan', 'Vanuatu', 'Venezuela', 'Vietnam', 'Yemen', 'Zambia', 'Zimbabwe'], index=None, placeholder="Choose a country", help="The selected country will determine the _Fragility Index_ and _Natural Disaster Risk_ KPIs")
    st.write("")

    # Button to trigger the script
    if st.button("Simulate", type="primary"):
    # Check if any of the required inputs are None
        if input1 is None or input2 is None or input3 is None or input6 is None:
            # Identify which inputs are missing
            missing_inputs = []
            if input1 is None:
                missing_inputs.append(":red[Lead Time (days)]")
            if input2 is None:
                missing_inputs.append(":red[Distance from Supplier to CM (km)]")
            if input3 is None:
                missing_inputs.append(":red[BCP Risk]")
            if input6 is None:
                missing_inputs.append(":red[Supplier Country]")

            # Display a warning message
            st.warning(f"Please introduce: {', '.join(missing_inputs)}.", icon="⚠️")

        else:
            # Call the Python script with the user inputs
            try:
                run_script(input1, input2, input3, input6)
            except PermissionError as e:
                st.error(f"Please close the file in the following path: {e}")
            except IndexError:
                st.warning("Selected country is not currently in the database so _Fragility Index_ and _Natural Disaster Risk_ cannot be retrieved, please select a different one.")

def run_script(input1, input2, input3, input6):
    # Your Python script logic here

    
    # ======================================== COUNTRY RISKS ======================================================= #
    

    # Replace with the URL of the Wikipedia page containing the table
    url1 = "https://en.wikipedia.org/wiki/List_of_countries_by_Fragile_States_Index"
    url2 = "https://en.wikipedia.org/wiki/List_of_countries_by_natural_disaster_risk"

    response1 = requests.get(url1, verify=False)
    soup1 = BeautifulSoup(response1.text, "html.parser")
    response2 = requests.get(url2, verify=False)
    soup2 = BeautifulSoup(response2.text, "html.parser")
 
    # # Find and extract the table containing the country data
    table1 = soup1.find("table", {"class": "wikitable sortable"})
    table2 = soup2.find("table", {"class": "wikitable sortable"})
   
    # # # Initialize empty dictionaries to store data
    country_data1 = {}
    country_data2 = {}
    
    # # Loop through rows in the table and extract data
    for row in table1.find_all("tr")[1:]:      #<tr> is table row, <td> is table cell and <th> is table header
        columns1 = row.find_all("td")
        country1 = columns1[1].text.strip()
        score1 = columns1[2].text.strip()
        country_data1[country1] = score1
    for row in table2.find_all("tr")[1:]:      #<tr> is table row, <td> is table cell and <th> is table header
        columns2 = row.find_all("td")
        country2 = columns2[1].text.strip()
        score2 = columns2[2].text.strip()
        country_data2[country2] = score2
 
    # # # Create a DataFrame from the dictionary
    df_fragility = pd.DataFrame(list(country_data1.items()), columns=["Manufacturer Country", "Fragility Index"])
    df_naturaldisaster = pd.DataFrame(list(country_data2.items()), columns=["Manufacturer Country", "Natural Disaster Risk"])
    df_naturaldisaster['Natural Disaster Risk'] = df_naturaldisaster['Natural Disaster Risk'].str.replace('%', '').astype(float)

    # Get Fragility Index and Natural Disaster Risk for the selected country
    input9 = df_fragility[df_fragility["Manufacturer Country"] == input6]["Fragility Index"].values[0]
    input10 = df_naturaldisaster[df_naturaldisaster["Manufacturer Country"] == input6]["Natural Disaster Risk"].values[0]


    st.metric("","")

    with st.expander("See Explanation"):
        st.divider()
        st.write("__Current KPIs:__ Current values for all 5 introduced KPIs.")
        st.divider()
        st.write("__Current Supply Chain Strength:__ (:green[HIGH], :orange[MEDIUM] or :red[LOW]) How strong the current supply chain is, with a percentage orientation that ranks the result against all scores in the current portfolio.", unsafe_allow_html=True)
        st.divider()
        st.write("__Target KPIs:__ Target KPI values to go up to the next level of supply chain strength. For example, :orange[MEDIUM] > :green[HIGH].")
        st.divider()
        st.write("__Target Supply Chain Strength:__ How strong the supply chain for that supplier would be if you made one of the suggested changes.")
        st.write("")
    st.metric("","")

    st.subheader("Current KPIs", anchor=None, help=None, divider="grey")

    c1, c2, c3 = st.columns(3)
    c1.metric("Lead Time", f"{input1} days")
    c2.metric("Distance", f"{input2:.1f} km")
    c3.metric("BCP Risk", input3)

    c4, c5 = st.columns(2)
    c4.metric(f"Fragility Index for :blue[{input6}]", input9)
    c5.metric(f"Natural Disaster Risk for :blue[{input6}]", f"{input10:.1f}%")

    st.metric("","")



    # Convert BCP_risk to numerical values
    bcp_mapping = {"LOW": 0, "MEDIUM": 1, "HIGH": 2}

    df0 = pd.DataFrame({
        'Lead Time': [input1],
        'Distance (km)': [input2],
        'BCP_risk': [input3],
        'Fragility Index': [input9],
        'Natural Disaster Risk': [input10]
    })

    df0['BCP_risk'] = df0['BCP_risk'].map(bcp_mapping)

    
# ======================== Read Data ===================================================== #
    
    # data = {
    #     'Lead Time': [38.5, 23.1, 21.0, 28.0, 35.0, 21.0, 10.5, 28.0, 14.0, 119.0, 49.0, 21.0, 14.0, 14.0, 14.0, 14.0, 38.5, 23.1, 21.0, 28.0, 35.0, 21.0, 21.0, 10.5, 14.0, 119.0, 280.0, 14.0, 14.0, 21.0, 21.0, 21.0, 21.0, 21.0, 84.0, 35.0, 35.0, 35.0, 35.0, 35.0, 35.0, 35.0, 35.0, 21.0, 21.0, 21.0, 21.0, 21.0, 21.0, 21.0, 21.0, 35.0, 35.0, 21.0, 21.0, 28.0, 28.0, 28.0, 28.0, 28.0, 28.0, 35.0, 35.0, 35.0, 35.0, 35.0, 35.0, 14.0, 14.0, 14.0, 14.0, 14.0, 14.0, 14.0, 14.0, 14.0, 14.0, 14.0, 14.0, 14.0, 14.0, 14.0, 14.0, 14.0, 14.0, 14.0, 14.0, 14.0, 14.0, 14.0, 14.0, 14.0, 14.0, 14.0, 14.0, 14.0, 14.0, 14.0, 14.0, 14.0, 14.0, 14.0, 14.0, 14.0, 14.0, 14.0, 14.0, 14.0, 14.0, 14.0, 14.0, 14.0, 14.0, 14.0, 14.0, 14.0, 14.0, 14.0, 14.0, 14.0, 14.0, 14.0, 14.0, 14.0, 14.0, 14.0, 14.0, 14.0, 14.0, 14.0, 14.0, 14.0, 14.0, 14.0, 14.0, 14.0, 14.0, 14.0, 14.0, 14.0, 14.0, 14.0, 14.0, 14.0, 14.0, 28.0, 42.0, 42.0, 42.0, 42.0, 28.0, 28.0, 35.0, 84.0, 84.0, 28.0, 28.0, 28.0, 28.0, 28.0, 28.0, 28.0, 42.0, 42.0, 84.0, 28.0, 56.0, 56.0, 84.0, 42.0, 7.0, 7.0, 25.0, 21.0, 20.0, 31.0, 4.0, 21.0, 21.0, 28.0, 28.0, 42.0, 28.0, 28.0, 49.0, 70.0, 14.0, 84.0, 14.0, 21.0, 21.0, 21.0, 21.0, 28.0, 4.0, 21.0, 21.0, 28.0, 7.0, 14.0, 25.0, 11.0, 15.0, 7.0, 21.0, 23.0, 38.0, 15.0, 10.0, 9.0, 42.0, 18.0, 4.0, 10.0, 10.0, 4.0, 10.0, 4.0, 10.0, 3.0, 3.0, 3.0, 4.0, 14.0, 21.0, 28.0, 10.0, 21.0, 21.0, 21.0, 21.0, 14.0, 4.0, 20.0, 20.0, 20.0, 20.0, 60.0, 20.0, 20.0, 20.0, 10.0, 35.0, 14.0, 10.0, 21.0, 15.0, 25.0, 21.0, 56.0, 56.0, 14.0, 10.0, 28.0, 21.0, 21.0, 14.0, 18.0, 22.0, 22.0, 28.0, 31.0, 10.0],
    #     'Distance (km)': [837.4335666015143, 1178.634559348008, 818.5507495071594, 872.360735047979, 690.2515511155124, 1205.174194376991, 1124.107031313811, 724.8807027919593, 1205.174194376991, 7359.206415767943, 3.842769462022032, 1168.007274606258, 1157.2079517412, 1159.067403085367, 1138.270677427018, 1138.270677427018, 837.4335666015143, 1178.634559348008, 818.5507495071594, 872.360735047979, 690.2515511155124, 1205.174194376991, 1205.174194376991, 1124.107031313811, 1205.174194376991, 7359.206415767943, 367.8764159114132, 1157.2079517412, 1159.067403085367, 1168.007274606258, 15.2521020010495, 15.2521020010495, 15.2521020010495, 15.2521020010495, 6719.749062264338, 644.1499825941465, 644.1499825941465, 644.1499825941465, 644.1499825941465, 644.1499825941465, 644.1499825941465, 644.1499825941465, 644.1499825941465, 487.8109146803064, 487.8109146803064, 487.8109146803064, 487.8109146803064, 487.8109146803064, 487.8109146803064, 487.8109146803064, 487.8109146803064, 644.1499825941465, 644.1499825941465, 15.2521020010495, 14.37338479691394, 274.6650653782571, 701.3625870144721, 701.3625870144721, 701.3625870144721, 701.3625870144721, 701.3625870144721, 518.5399416630631, 518.5399416630631, 518.5399416630631, 518.5399416630631, 518.5399416630631, 518.5399416630631, 434.0179090059719, 434.0179090059719, 434.0179090059719, 434.0179090059719, 434.0179090059719, 434.0179090059719, 434.0179090059719, 434.0179090059719, 434.0179090059719, 434.0179090059719, 434.0179090059719, 434.0179090059719, 434.0179090059719, 434.0179090059719, 434.0179090059719, 434.0179090059719, 434.0179090059719, 434.0179090059719, 434.0179090059719, 434.0179090059719, 434.0179090059719, 434.0179090059719, 434.0179090059719, 434.0179090059719, 434.0179090059719, 434.0179090059719, 434.0179090059719, 434.0179090059719, 434.0179090059719, 434.0179090059719, 434.0179090059719, 434.0179090059719, 434.0179090059719, 434.0179090059719, 434.0179090059719, 434.0179090059719, 434.0179090059719, 434.0179090059719, 434.0179090059719, 434.0179090059719, 434.0179090059719, 434.0179090059719, 434.0179090059719, 434.0179090059719, 434.0179090059719, 434.0179090059719, 434.0179090059719, 434.0179090059719, 434.0179090059719, 434.0179090059719, 434.0179090059719, 434.0179090059719, 434.0179090059719, 434.0179090059719, 434.0179090059719, 434.0179090059719, 434.0179090059719, 434.0179090059719, 434.0179090059719, 434.0179090059719, 434.0179090059719, 434.0179090059719, 434.0179090059719, 434.0179090059719, 434.0179090059719, 434.0179090059719, 434.0179090059719, 434.0179090059719, 434.0179090059719, 434.0179090059719, 434.0179090059719, 434.0179090059719, 434.0179090059719, 434.0179090059719, 434.0179090059719, 434.0179090059719, 434.0179090059719, 434.0179090059719, 597.9568859208574, 699.6956914953937, 529.1227625676603, 1014.15298009191, 7560.481489978036, 971.2738842035701, 7560.481489978036, 315.2016464543039, 6692.331763491034, 6692.331763491034, 106.1048990342129, 106.1048990342129, 106.1048990342129, 196.168954471668, 196.168954471668, 196.168954471668, 106.1048990342129, 602.7055811370002, 790.4893408380376, 665.9940592864795, 45.13524591444322, 1220.48857715661, 7726.109635106045, 7696.967044683911, 4.927253680745152, 837.4040893391528, 276.2639411993372, 738.0068747713857, 780.994157226469, 208.3589004895512, 736.2421438329204, 647.7858623267582, 641.0783697551121, 1192.757148061072, 195.2963218323391, 352.0099531054563, 982.4472225396281, 352.0099531054563, 1033.000044931536, 1482.383392563958, 8010.853082471393, 410.2096332497158, 939.2583605924024, 112.1052873130918, 990.8903919002469, 1714.917225863134, 875.4877598899199, 927.9723651503791, 620.974712609509, 804.6000604844877, 855.658255676155, 1425.372660129265, 1244.186551977826, 1049.95538088895, 1048.908450543781, 2800.089753821535, 27.63353734191086, 1740.768416219719, 531.700445086605, 1346.211699216832, 1346.211699216832, 1339.551669421216, 1195.89564972591, 1189.114596795793, 1048.908450543781, 742.7718554926944, 37.87889487773086, 531.700445086605, 824.9164228112168, 1371.40531868246, 513.4906606297532, 523.6457985381546, 8093.585485385148, 905.6418871979532, 1049.95538088895, 531.700445086605, 529.1955829616849, 15.57426274070816, 207.7989927573335, 387.2345709203736, 2.902417929334273, 1.881902455581899, 480.3136660101411, 387.2345709203736, 43.95837434008209, 453.2667441086086, 451.2636913105088, 15.57426274070816, 361.4581152443967, 361.4581152443967, 361.4581152443967, 361.4581152443967, 361.4581152443967, 361.4581152443967, 361.4581152443967, 361.4581152443967, 1740.768416219719, 2214.825252493896, 1048.908450543781, 801.327339726479, 435.3134356036826, 26.08257939303482, 453.2667441086086, 435.3134356036826, 1149.802430316858, 669.9723368095175, 600.8924465851845, 435.3134356036826, 551.8092961120688, 1944.619039569345, 28.79095579599661, 687.0394847375309, 1190.572504148789, 1066.073041289835, 1449.18240336355, 1028.044417804685, 1339.551669421216, 38.35793303920683],
    #     'Fragility Index': [24.6, 41.9, 28.8, 21.0, 24.6, 51.8, 51.8, 48.8, 51.8, 45.3, 42.6, 51.8, 51.8, 51.8, 51.8, 51.8, 24.6, 41.9, 28.8, 21.0, 24.6, 51.8, 51.8, 51.8, 51.8, 45.3, 24.6, 51.8, 51.8, 51.8, 42.6, 42.6, 42.6, 42.6, 45.3, 42.6, 42.6, 42.6, 42.6, 42.6, 42.6, 42.6, 42.6, 42.6, 42.6, 42.6, 42.6, 42.6, 42.6, 42.6, 42.6, 42.6, 42.6, 42.6, 42.6, 24.4, 31.4, 31.4, 31.4, 31.4, 31.4, 24.6, 24.6, 24.6, 24.6, 24.6, 24.6, 24.6, 24.6, 24.6, 24.6, 24.6, 24.6, 24.6, 24.6, 24.6, 24.6, 24.6, 24.6, 24.6, 24.6, 24.6, 24.6, 24.6, 24.6, 24.6, 24.6, 24.6, 24.6, 24.6, 24.6, 24.6, 24.6, 24.6, 24.6, 24.6, 24.6, 24.6, 24.6, 24.6, 24.6, 24.6, 24.6, 24.6, 24.6, 24.6, 24.6, 24.6, 24.6, 24.6, 24.6, 24.6, 24.6, 24.6, 24.6, 24.6, 24.6, 24.6, 24.6, 24.6, 24.6, 24.6, 24.6, 24.6, 24.6, 24.6, 24.6, 24.6, 24.6, 24.6, 24.6, 24.6, 24.6, 24.6, 24.6, 24.6, 24.6, 24.6, 24.6, 24.6, 24.6, 24.6, 24.6, 24.6, 24.6, 24.6, 28.8, 24.6, 28.8, 45.3, 28.8, 45.3, 24.6, 45.3, 45.3, 45.2, 45.2, 45.2, 45.2, 45.2, 45.2, 45.2, 24.4, 21.0, 31.4, 42.6, 41.9, 45.3, 45.3, 42.6, 48.8, 42.6, 21.0, 43.5, 17.8, 24.6, 24.6, 24.6, 41.9, 17.8, 24.4, 42.6, 24.4, 31.4, 41.9, 45.3, 48.8, 42.6, 45.2, 21.0, 43.5, 17.8, 42.6, 24.6, 24.6, 24.6, 41.9, 28.8, 31.4, 24.6, 16.0, 43.5, 17.9, 43.5, 41.9, 41.9, 24.6, 21.0, 21.0, 24.6, 42.6, 43.5, 43.5, 28.8, 41.9, 28.8, 28.8, 28.8, 24.6, 31.4, 42.6, 43.5, 43.5, 43.5, 43.5, 43.5, 43.5, 43.5, 43.5, 43.5, 43.5, 28.8, 43.5, 43.5, 43.5, 43.5, 43.5, 43.5, 43.5, 43.5, 43.5, 17.9, 81.2, 24.6, 17.8, 43.5, 43.5, 43.5, 43.5, 24.6, 42.6, 28.8, 43.5, 43.5, 53.0, 43.5, 42.6, 41.9, 24.6, 24.6, 24.6, 24.6, 43.5],
    #     'Natural Disaster Risk': [3.92, 5.78, 6.67, 4.04, 3.92, 2.15, 2.15, 0.97, 2.15, 22.73, 9.37, 2.15, 2.15, 2.15, 2.15, 2.15, 3.92, 5.78, 6.67, 4.04, 3.92, 2.15, 2.15, 2.15, 2.15, 22.73, 3.92, 2.15, 2.15, 2.15, 9.37, 9.37, 9.37, 9.37, 22.73, 9.37, 9.37, 9.37, 9.37, 9.37, 9.37, 9.37, 9.37, 9.37, 9.37, 9.37, 9.37, 9.37, 9.37, 9.37, 9.37, 9.37, 9.37, 9.37, 9.37, 1.14, 4.16, 4.16, 4.16, 4.16, 4.16, 3.92, 3.92, 3.92, 3.92, 3.92, 3.92, 3.92, 3.92, 3.92, 3.92, 3.92, 3.92, 3.92, 3.92, 3.92, 3.92, 3.92, 3.92, 3.92, 3.92, 3.92, 3.92, 3.92, 3.92, 3.92, 3.92, 3.92, 3.92, 3.92, 3.92, 3.92, 3.92, 3.92, 3.92, 3.92, 3.92, 3.92, 3.92, 3.92, 3.92, 3.92, 3.92, 3.92, 3.92, 3.92, 3.92, 3.92, 3.92, 3.92, 3.92, 3.92, 3.92, 3.92, 3.92, 3.92, 3.92, 3.92, 3.92, 3.92, 3.92, 3.92, 3.92, 3.92, 3.92, 3.92, 3.92, 3.92, 3.92, 3.92, 3.92, 3.92, 3.92, 3.92, 3.92, 3.92, 3.92, 3.92, 3.92, 3.92, 3.92, 3.92, 3.92, 3.92, 3.92, 3.92, 6.67, 3.92, 6.67, 22.73, 6.67, 22.73, 3.92, 22.73, 22.73, 4.63, 4.63, 4.63, 4.63, 4.63, 4.63, 4.63, 1.14, 4.04, 4.16, 9.37, 5.78, 22.73, 22.73, 9.37, 0.97, 9.37, 4.04, 9.68, 1.03, 3.92, 3.92, 3.92, 5.78, 1.03, 1.14, 9.37, 1.14, 4.16, 5.78, 22.73, 0.97, 9.37, 4.63, 4.04, 9.68, 1.03, 9.37, 3.92, 3.92, 3.92, 5.78, 6.67, 4.16, 3.92, 1.3, 9.68, 1.03, 9.68, 5.78, 5.78, 3.92, 4.04, 4.04, 3.92, 9.37, 9.68, 9.68, 6.67, 5.78, 6.67, 6.67, 6.67, 3.92, 4.16, 9.37, 9.68, 9.68, 9.68, 9.68, 9.68, 9.68, 9.68, 9.68, 9.68, 9.68, 6.67, 9.68, 9.68, 9.68, 9.68, 9.68, 9.68, 9.68, 9.68, 9.68, 1.03, 16.23, 3.92, 1.03, 9.68, 9.68, 9.68, 9.68, 3.92, 9.37, 6.67, 9.68, 9.68, 3.19, 9.68, 9.37, 5.78, 3.92, 3.92, 3.92, 3.92, 9.68],
    #     'BCP_risk': [0, 0, 0, 0, 0, 0, 1, 0, 0, 2, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 2, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 1, 0, 2, 1, 1, 1, 0, 2, 2, 2, 2, 1, 1, 1, 0, 1, 0, 0, 0, 1, 2, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 1, 0, 1, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 2, 0, 0, 0, 0, 0, 1, 0, 1, 1, 2, 0, 1, 2, 0, 2, 0, 0, 1, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 1, 0, 0, 0, 0, 0, 0],
    #     'SCR_score': [0.300215088482756, 0.3231793716768303, 0.41457604414927, 0.4041042301051361, 0.3435910786270949, 0.3361537175320962, -0.3223101576804844, 0.3366000086585924, 0.3986475047438835, -2.739080303080233, 0.1509347840389478, -1.178553811293828, 0.4026003463026495, 0.402447111107524, 0.4041609447736874, 0.4041609447736874, 0.300215088482756, 0.3231793716768303, 0.41457604414927, 0.4041042301051361, 0.3435910786270949, 0.3361537175320962, 0.3361537175320962, 0.4365750477731757, 0.3986475047438835, -2.739080303080233, -1.817124918601573, 0.4026003463026495, 0.402447111107524, -1.178553811293828, -0.3589155022236669, -0.3589155022236669, -0.3589155022236669, -0.3589155022236669, -1.615029234247725, -1.294615015695692, -1.294615015695692, -1.294615015695692, -1.294615015695692, -1.294615015695692, -1.294615015695692, -1.294615015695692, -1.294615015695692, 0.3610266880786284, 0.3610266880786284, 0.3610266880786284, 0.3610266880786284, 0.3610266880786284, 0.3610266880786284, 0.3610266880786284, 0.3610266880786284, -1.294615015695692, -1.294615015695692, -0.3589155022236669, -0.3588430881738677, -0.2906063489162484, -0.3828808600701055, -0.3828808600701055, -0.3828808600701055, -0.3828808600701055, -0.3828808600701055, -1.160028780795091, -1.160028780795091, -1.160028780795091, -1.160028780795091, -1.160028780795091, -1.160028780795091, 0.5521883529049199, 0.5521883529049199, 0.5521883529049199, 0.5521883529049199, 0.5521883529049199, 0.5521883529049199, 0.5521883529049199, 0.5521883529049199, 0.5521883529049199, 0.5521883529049199, 0.5521883529049199, 0.5521883529049199, 0.5521883529049199, 0.5521883529049199, 0.5521883529049199, 0.5521883529049199, 0.5521883529049199, 0.5521883529049199, 0.5521883529049199, 0.5521883529049199, 0.5521883529049199, 0.5521883529049199, 0.5521883529049199, 0.5521883529049199, 0.5521883529049199, 0.5521883529049199, 0.5521883529049199, 0.5521883529049199, 0.5521883529049199, 0.5521883529049199, 0.5521883529049199, 0.5521883529049199, 0.5521883529049199, 0.5521883529049199, 0.5521883529049199, 0.5521883529049199, 0.5521883529049199, 0.5521883529049199, 0.5521883529049199, 0.5521883529049199, 0.5521883529049199, 0.5521883529049199, 0.5521883529049199, 0.5521883529049199, 0.5521883529049199, 0.5521883529049199, 0.5521883529049199, 0.5521883529049199, 0.5521883529049199, 0.5521883529049199, 0.5521883529049199, 0.5521883529049199, 0.5521883529049199, 0.5521883529049199, 0.5521883529049199, 0.5521883529049199, 0.5521883529049199, 0.5521883529049199, 0.5521883529049199, 0.5521883529049199, 0.5521883529049199, 0.5521883529049199, 0.5521883529049199, 0.5521883529049199, 0.5521883529049199, 0.5521883529049199, 0.5521883529049199, 0.5521883529049199, 0.5521883529049199, 0.5521883529049199, 0.5521883529049199, 0.5521883529049199, 0.5521883529049199, 0.5521883529049199, 0.5521883529049199, 0.5521883529049199, 0.5521883529049199, 0.5521883529049199, -1.104079650418654, -1.280881023055624, 0.2943757250946283, -0.547909872372926, -0.5504650746378541, -1.178273887615827, -1.18436270566794, -0.3843867059344853, -1.612769806949174, -0.8538846014955137, -1.151732473493121, -1.151732473493121, -1.151732473493121, -1.159154546220129, -0.4002693407664688, -0.4002693407664688, -0.3928472680394604, 0.3162578495913861, -0.4730216246071561, -0.1210312735993607, 0.3350132813260463, 0.02600943147141266, -1.447987074870631, -2.454445822620237, 0.2133392001836257, 0.514808450543827, 0.5034475994170018, 0.4419592251445605, 0.3302877307719329, 0.572270639955764, 0.3755117836006842, -0.8939215843758443, -1.045139453899178, -1.177006728968562, -0.2569595648756475, 0.4619049554401841, -0.626102274535657, 0.4619049554401841, 0.3486744930944806, 0.06692077541725527, -2.355325226861298, 0.4875192552890658, -0.2386206491094806, 0.4905310269072457, 0.4568301279054165, 0.2533242307031863, 0.508365652540276, 0.3247535013878173, 0.4117938885027111, -0.9068444577430383, 0.4549476813514612, -1.196176299332839, 0.3170061117893254, 0.5347585854643676, 0.501515947623187, 0.3185126769560352, 0.4816481309877679, -0.2686546265119349, 0.4758193063833386, -0.4307675323298106, -0.448622900104607, -1.254470441916411, 0.4935019893970268, -0.2201859780347079, -0.9716160438471425, 0.1525342956156556, -1.099460374978413, 0.5026023580455332, 0.512255979271446, -0.3346391860743876, 0.5914863128456044, 0.5370833365673731, -0.03318037347771013, -0.9687372989951674, 0.5704693210139604, 0.518108113546123, 0.5117364646703041, 0.5451357088154714, 0.4400178563519591, 0.3627369944912432, 0.3319155673233377, 0.492697976774687, 0.3550664558977404, 0.3627369944912432, 0.3910259815249115, 0.3572953608745355, 0.5073375252194312, 0.5451357088154714, -1.143981525177118, -1.143981525177118, -1.143981525177118, -1.143981525177118, -1.501088880673046, -1.143981525177118, -1.143981525177118, -1.143981525177118, -0.9829014125286042, -0.1255408638263757, 0.501515947623187, 0.612681648177767, 0.3587748718821928, 0.4460652080559523, 0.3215846253249427, 0.3587748718821928, 0.1182386703169398, 0.03354604378013576, 0.4950067957368841, 0.4569793946435729, 0.286680798020099, -1.25744599294523, 0.3922759106222455, -0.3517829219610752, 0.3677267675325899, 0.4286799628178646, 0.3971083715332201, 0.3782477535630226, 0.3257937562026968, 0.4896920300574391]
    # }

    # df1 = pd.DataFrame(data)
    
    df1 = pd.read_excel(r"streamlit_data_for_scaler.xlsx")
    df = pd.concat([df0, df1], ignore_index=True)

    scaler = StandardScaler()
    df[["Lead_Time_T", "Distance_T", "Fragility_Index_T", "Natural_Disaster_Risk_T", "BCP_Risk_T"]] = scaler.fit_transform(df[["Lead Time", "Distance (km)", "Fragility Index", "Natural Disaster Risk", "BCP_risk"]])

    #============== ACTUAL TOOL ==============#
    # Weights
    leadtime_weight = 0.205
    distance_weight = 0.117
    fragilityindex_weight = 0.042
    naturaldisasterrisk_weight = 0.042
    bcprisk_weight = 0.595

    df["SCR_score"] = -(leadtime_weight * df['Lead_Time_T']) - (distance_weight * df['Distance_T']) - (fragilityindex_weight * df['Fragility_Index_T']) - (naturaldisasterrisk_weight * df['Natural_Disaster_Risk_T']) - (bcprisk_weight * df['BCP_Risk_T'])

    # Scores 0, 1 or 2 for SCR
    df['SCR_Strength'] = df['SCR_score'].apply(lambda x: 0 if x <= -0.75 else (1 if -0.75 < x < -0.19 else 2))

    # selected_columns = df.loc[:, ['Lead Time', 'Distance (km)', 'Fragility Index', 'Natural Disaster Risk', 'BCP_risk', 'Lead_Time_T', 'Distance_T', 'Fragility_Index_T', 'Natural_Disaster_Risk_T', 'BCP_Risk_T', 'SCR_score', 'SCR_Strength']]
    # st.dataframe(selected_columns)



    # Display the value of "SCR_Strength" for the first row
    # st.write("SCR_Strength for the first row:", df.loc[0, 'SCR_Strength'])

    # Display the corresponding label for "SCR_Strength" for the first row
    strength_labels = {0: 'LOW', 1: 'MEDIUM', 2: 'HIGH'}

    st.subheader("Current Supply Chain Strength", anchor=None, help=None, divider="grey")

    c6, c7 = st.columns(2)
    if df.loc[0, 'SCR_Strength'] == 0:
        c6.metric(":red_circle: :red[Supply Chain Strength]", strength_labels[0])
    elif df.loc[0, 'SCR_Strength'] == 1:
        c6.metric(":large_orange_circle: :orange[Supply Chain Strength]", strength_labels[1])
    else:
        c6.metric(":large_green_circle: :green[Supply Chain Strength]", strength_labels[2])







    df_score = df['SCR_score']
    # Progress bar based on SCR_score
    progress_value = df.loc[0, 'SCR_score']
    progress_min = df1['SCR_score'].min()
    progress_max = df1['SCR_score'].max()
    if progress_max > progress_value and progress_min < progress_value:
        supply_chain_strength_percentage = abs(progress_value - progress_min) / abs(progress_max - progress_min)
    else:
        # Set supply_chain_strength_percentage to 0 if progress_value < progress_min
        # Set supply_chain_strength_percentage to 1 if progress_value > progress_max
        supply_chain_strength_percentage = 0 if progress_value < progress_min else 1

    if df.loc[0, 'SCR_Strength'] == 0:
        c7.metric(":red_circle: :red[Supply Chain Strength as a Percentage]", f"{supply_chain_strength_percentage:.1%}")
    elif df.loc[0, 'SCR_Strength'] == 1:
        c7.metric(":large_orange_circle: :orange[Supply Chain Strength as a Percentage]", f"{supply_chain_strength_percentage:.1%}")
    else:
        c7.metric(":large_green_circle: :green[Supply Chain Strength as a Percentage]", f"{supply_chain_strength_percentage:.1%}")  
    
    st.metric("","")
    


    # st.data_editor(
    #     df_score,
    #     column_config={
    #         "SCR_score": st.column_config.ProgressColumn(
    #             "Supply Chain Strength",
    #             help="Shows how strong the supply chain is for the simulated material as opposed to all the other supply chain in the portfolio.",
    #             format="%.2f",
    #             min_value=progress_min,
    #             max_value=progress_max,
    #         ),
    #     },
    #     hide_index=True,
    # )
   
   

   
    # ======= Change in criteria required ======== #
    # LeadTime
    df['Lead Time Required Scaled'] = df.apply(lambda row: ((-0.75) - (-distance_weight * row['Distance_T'] - fragilityindex_weight * row['Fragility_Index_T'] - naturaldisasterrisk_weight * row['Natural_Disaster_Risk_T'] - bcprisk_weight * row['BCP_Risk_T'])) / (-leadtime_weight) if row['SCR_Strength'] == 0 else (((-0.19) - (-distance_weight * row['Distance_T'] - fragilityindex_weight * row['Fragility_Index_T'] - naturaldisasterrisk_weight * row['Natural_Disaster_Risk_T'] - bcprisk_weight * row['BCP_Risk_T'])) / (-leadtime_weight) if row['SCR_Strength'] == 1 else ""), axis=1)
    # Distance
    df['Distance Required Scaled'] = df.apply(lambda row: ((-0.75) - (-leadtime_weight * row['Lead_Time_T'] - fragilityindex_weight * row['Fragility_Index_T'] - naturaldisasterrisk_weight * row['Natural_Disaster_Risk_T'] - bcprisk_weight * row['BCP_Risk_T'])) / (-distance_weight) if row['SCR_Strength'] == 0 else (((-0.19) - (-leadtime_weight * row['Lead_Time_T'] - fragilityindex_weight * row['Fragility_Index_T'] - naturaldisasterrisk_weight * row['Natural_Disaster_Risk_T'] - bcprisk_weight * row['BCP_Risk_T'])) / (-distance_weight) if row['SCR_Strength'] == 1 else ""), axis=1)
    # Fragility
    df['Fragility Required Scaled'] = df.apply(lambda row: ((-0.75) - (-distance_weight * row['Distance_T'] - leadtime_weight * row['Lead_Time_T'] - naturaldisasterrisk_weight * row['Natural_Disaster_Risk_T'] - bcprisk_weight * row['BCP_Risk_T'])) / (-fragilityindex_weight) if row['SCR_Strength'] == 0 else (((-0.19) - (-distance_weight * row['Distance_T'] - leadtime_weight * row['Lead_Time_T'] - naturaldisasterrisk_weight * row['Natural_Disaster_Risk_T'] - bcprisk_weight * row['BCP_Risk_T'])) / (-fragilityindex_weight) if row['SCR_Strength'] == 1 else ""), axis=1)
    # Natural Disaster Risk
    df['Natural Disaster Required Scaled'] = df.apply(lambda row: ((-0.75) - (-distance_weight * row['Distance_T'] - fragilityindex_weight * row['Fragility_Index_T'] - leadtime_weight * row['Lead_Time_T'] - bcprisk_weight * row['BCP_Risk_T'])) / (-naturaldisasterrisk_weight) if row['SCR_Strength'] == 0 else (((-0.19) - (-distance_weight * row['Distance_T'] - fragilityindex_weight * row['Fragility_Index_T'] - leadtime_weight * row['Lead_Time_T'] - bcprisk_weight * row['BCP_Risk_T'])) / (-naturaldisasterrisk_weight) if row['SCR_Strength'] == 1 else ""), axis=1)
    # BCP Risk
    df['BCP Risk Required Scaled'] = df.apply(lambda row: ((-0.75) - (-distance_weight * row['Distance_T'] - fragilityindex_weight * row['Fragility_Index_T'] - naturaldisasterrisk_weight * row['Natural_Disaster_Risk_T'] - leadtime_weight * row['Lead_Time_T'])) / (-bcprisk_weight) if row['SCR_Strength'] == 0 else (((-0.19) - (-distance_weight * row['Distance_T'] - fragilityindex_weight * row['Fragility_Index_T'] - naturaldisasterrisk_weight * row['Natural_Disaster_Risk_T'] - leadtime_weight * row['Lead_Time_T'])) / (-bcprisk_weight) if row['SCR_Strength'] == 1 else ""), axis=1)

    # df1 = df[df['Lead Time Required Scaled'] != ""]

    # Convert empty strings to NaN in the required scaled columns
    df['Lead Time Required Scaled'] = pd.to_numeric(df['Lead Time Required Scaled'], errors='coerce')
    df['Distance Required Scaled'] = pd.to_numeric(df['Distance Required Scaled'], errors='coerce')
    df['Fragility Required Scaled'] = pd.to_numeric(df['Fragility Required Scaled'], errors='coerce')
    df['Natural Disaster Required Scaled'] = pd.to_numeric(df['Natural Disaster Required Scaled'], errors='coerce')
    df['BCP Risk Required Scaled'] = pd.to_numeric(df['BCP Risk Required Scaled'], errors='coerce')

    # Reverse the scaling for all criteria
    df[['Lead Time Required', 'Distance Required', 'Fragility Required', 'Natural Disaster Required', 'BCP Risk Required']] = scaler.inverse_transform(df[['Lead Time Required Scaled', 'Distance Required Scaled', 'Fragility Required Scaled', 'Natural Disaster Required Scaled', 'BCP Risk Required Scaled']])

    # Pone un "0" si es negativo y deja el valor como esta (x) si es positivo.
    df['Distance Required'][df['Distance Required'] < 0] = 0
    df['Lead Time Required'][df['Lead Time Required'] < 0] = 0
    df['Fragility Required'][df['Fragility Required'] < 0] = 0
    df['Natural Disaster Required'][df['Natural Disaster Required'] < 0] = 0
    # df['BCP Risk Required'][df['BCP Risk Required'] < 0] = -1

    # Round down BCP Risk Required to nearest whole number.
    df['BCP Risk Required'] = df['BCP Risk Required'].apply(lambda x: math.floor(x) if x >= 0 else 0)

    # Assuming AB2 is a variable 'bcprisk_required_scaled' and AG2 is a variable 'bcprisk_required'.  -0.956438593999987 is the scaled value for BCP_Risk = 0.
    df['BCP Risk Required with negative'] = np.where(df['BCP Risk Required Scaled'] < -0.956438593999987, -1, df['BCP Risk Required'])

    # st.dataframe(df)


    def display_kpi_cards(df):
        # Assuming df is the DataFrame from your run_script function
        # Display KPI cards for Lead Time Required, Distance Required, Fragility Required, Natural Disaster Required, and BCP Risk Required with negative

        lead_time_value = df.loc[0, 'Lead Time Required']
        distance_value = df.loc[0, 'Distance Required']
        fragility_value = df.loc[0, 'Fragility Required']
        natural_disaster_value = df.loc[0, 'Natural Disaster Required']
        bcp_risk_value = df.loc[0, 'BCP Risk Required with negative']


        if df.loc[0, 'SCR_Strength'] != 2:
            st.subheader("Target KPIs", anchor=None, help=None, divider="grey")
            
            c8, c9, c10 = st.columns(3)
            # Display "-" if the value is 0 for the first 4 metrics
            c8.metric("Lead Time Required", "-" if lead_time_value == 0 else f"{lead_time_value:.1f} days", delta=f"{(lead_time_value - input1):.1f} days" if lead_time_value != 0 else None, delta_color="inverse")
            c9.metric("Distance Required", "-" if distance_value == 0 else f"{distance_value:.1f} km", delta=f"{(distance_value - input2):.1f} km" if distance_value != 0 else None, delta_color="inverse")

            # Map the values to labels for "BCP Risk Required with negative"
            bcp_risk_labels = {0: 'LOW', 1: 'MEDIUM', 2: 'HIGH'}
            # Display "-" if the value is -1, otherwise display the label
            bcp_risk_display = "-" if bcp_risk_value == -1 else bcp_risk_labels.get(bcp_risk_value, f"{bcp_risk_value:.1f}")
            c10.metric("BCP Risk Required", bcp_risk_display)


            c11, c12 = st.columns(2)
            c11.metric("Fragility Index Required", "-" if fragility_value == 0 else f"{fragility_value:.1f}", delta=f"{(fragility_value - float(input9)):.1f}" if fragility_value != 0 else None, delta_color="inverse")
            c12.metric("Natural Disaster Risk Required", "-" if natural_disaster_value == 0 else f"{natural_disaster_value:.1f} %", delta=f"{(natural_disaster_value - float(input10)):.1f} %" if natural_disaster_value != 0 else None, delta_color="inverse")

            st.metric("","")

        # Map the values to labels for "Supply Chain Strength"
        supply_chain_strength_labels = {0: 'LOW', 1: 'MEDIUM', 2: 'HIGH'}
        supply_chain_strength_value = df.loc[0, 'SCR_Strength']

        # Map the "Supply Chain Strength" value to "New Supply Chain Strength" label
        new_strength_label = {
            0: 'MEDIUM',
            1: 'HIGH',
            2: 'ALREADY HIGH'
        }

        st.subheader("Target Supply Chain Strength", anchor=None, help=None, divider="grey")
        # Assuming supply_chain_strength_value is the variable containing the strength value
        if supply_chain_strength_value == 0:
            st.metric(":large_orange_circle: :orange[New Supply Chain Strength]", new_strength_label.get(0, "UNKNOWN"))
        elif supply_chain_strength_value == 1:
            st.metric(":large_green_circle: :green[New Supply Chain Strength]", new_strength_label.get(1, "UNKNOWN"))
        else:
            st.metric(":heavy_check_mark: :green[New Supply Chain Strength]", new_strength_label.get(2, "UNKNOWN"))




    # Call the display_kpi_cards function with the DataFrame
    display_kpi_cards(df)


def render_ahp_page():
    st.title("Weight Calculation")
    st.write("This section describes the process followed to calculate the weights asigned to each KPI prior to calculating the Supply Chain Strength for a given supplier.")
    st.header("AHP Matrix", anchor=None, help="For more information about the matrix construction process, check out the Wikipedia article below.", divider="grey")
    st.image('AHP.png')

    st.header("Analytic hierarchy process", anchor=None, help=None, divider="grey")
    # Add more code specific to the Natural Disaster Risk page if needed
    st.markdown(
    """
    <iframe src="https://en.wikipedia.org/wiki/Analytic_hierarchy_process" width="100%" height="800"></iframe>
    """,
    unsafe_allow_html=True
    )

# Function to render the Fragility Index page
def render_fragility_index_page():
    st.title("Fragility Index")
    st.write("In the below Wikipedia article there is a table containing latest Fragility Indexes for every country. The tool accesses the website and retrieves the values for the selected supplier country.")
    st.header("", anchor=None, help=None, divider="grey")
    # Add more code specific to the Fragility Index page if needed
    st.markdown(
    """
    <iframe src="https://en.wikipedia.org/wiki/List_of_countries_by_Fragile_States_Index" width="100%" height="800"></iframe>
    """,
    unsafe_allow_html=True
    )

# Function to render the Natural Disaster Risk page
def render_natural_disaster_page():
    st.title("Natural Disaster Risk")
    st.write("In the below Wikipedia article there is a table containing the latest scores for Natural Disaster Risk for every country. The tool accesses the website and retrieves the values for the selected supplier country.")
    st.header("", anchor=None, help=None, divider="grey")
    # Add more code specific to the Natural Disaster Risk page if needed
    st.markdown(
    """
    <iframe src="https://en.wikipedia.org/wiki/List_of_countries_by_natural_disaster_risk" width="100%" height="800"></iframe>
    """,
    unsafe_allow_html=True
    )



# Main function
def main():
    with st.sidebar:
        selected = option_menu(
            menu_title="Navigation",
            options=["Simulator", "Weight Calculation", "Fragility Index", "Natural Disaster Risk"],
            icons=["calculator", "123", "wikipedia", "wikipedia"],
            menu_icon="list",
            default_index=0,
        )

    # Render the selected page
    if selected == "Simulator":
        render_calculator_page()
    elif selected == "Fragility Index":
        render_fragility_index_page()
    elif selected == "Natural Disaster Risk":
        render_natural_disaster_page()
    elif selected == "Weight Calculation":
        render_ahp_page()

if __name__ == "__main__":
    main()
