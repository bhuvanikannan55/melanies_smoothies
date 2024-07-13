# Import python packages
import streamlit as st

from snowflake.snowpark.functions import col

# Write directly to the app
st.title(":cup_with_straw: Customise Your Smoothie!:cup_with_straw:")
st.write(
    """Choose the fruit you want in the custom smoothie
    """
)
Name_on_order = st.text_input('Name on Smoothie:')
st.write('The name on smoothie is :', Name_on_order)

session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
ingredients_list = st.multiselect(
    "choose upto 5 ingredients",my_dataframe)


if ingredients_list:  
   ingredients_string =''
   for fruit_chosen in ingredients_list:
       ingredients_string+=fruit_chosen +' '
   st.write(ingredients_string)


my_insert_stmt = """ insert into smoothies.public.orders(ingredients,Name_on_order)
            values ('""" + ingredients_string + """','""" + Name_on_order + """')"""

st.write(my_insert_stmt)
time_to_insert =st.button('submit_order')

if time_to_insert:
   session.sql(my_insert_stmt).collect()
   st.success('Your Smoothie is ordered!', icon="✅")

cnx = st.connection("snowflake")
session = cnx.session()

