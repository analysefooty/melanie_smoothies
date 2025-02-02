# Import python packages
import streamlit as st
import pandas as pd
from snowflake.connector import connect
from snowflake.snowpark.functions import col
import requests
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/")

# Write directly to the app
st.title("Customize your Smoothie!:cup_with_straw:")
st.write(
    """Choose the fruits you want in your custom Smoothie!
    """)

cnx = st.connection('snowflake')
session = cnx.session()
#session = get_active_session()
my_dataframe = session.table('smoothies.public.fruit_options').select(col('FRUIT_NAME'),col('SEARCH_ON'))
pd_df = my_dataframe.to_pandas()
#st.dataframe(data=my_dataframe,use_container_width=True)

name_on_order = st.text_input('Name on the Order:')
ingredients_list = st.multiselect('Choose up to 5 ingredients:', my_dataframe, max_selections=5)

if ingredients_list:
    ingredients_string = ''
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '
        search_on = pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        st.write ('the search value for ', fruit_chosen,' is ', search_on, ' . ')
        st.subheader(fruit_chosen + ' Nutrition Information')
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + search_on)
        fv_df = st.dataframe(data=fruityvice_response.json(),use_container_width=True)
    #st.write(ingredients_stri

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
            values ('""" + ingredients_string + """','""" + name_on_order + """')"""

    #st.write(my_insert_stmt)
    time_to_insert = st.button("Submit Order")
    if(time_to_insert):
            if ingredients_string:
                session.sql(my_insert_stmt).collect()
                st.success("your smoothie is ordered " + name_on_order + "!!")


#st.text(fruityvice_response.json())

