# Import python packages
import streamlit as st
from snowflake.connector import connect
from snowflake.snowpark.functions import col

# Write directly to the app
st.title("Customize your Smoothie!:cup_with_straw:")
st.write(
    """Choose the fruits you want in your custom Smoothie!
    """)

cnx = st.connection('snowflake',type='sql')
session = cnx.session()
#session = get_active_session()
my_dataframe = session.table('smoothies.public.fruit_options').select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe,use_container_width=True)

name_on_order = st.text_input('Name on the Order:')
ingredients_list = st.multiselect('Choose up to 5 ingredients:', my_dataframe, max_selections=5)

if ingredients_list:
    #st.write(ingredients_list)
    #st.text(ingredients_list)

    ingredients_string = ''

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '
    #st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
            values ('""" + ingredients_string + """','""" + name_on_order + """')"""

    #st.write(my_insert_stmt)
    time_to_insert = st.button("Submit Order")
    if(time_to_insert):
            if ingredients_string:
                session.sql(my_insert_stmt).collect()
                st.success("your smoothie is ordered " + name_on_order + "!!")
