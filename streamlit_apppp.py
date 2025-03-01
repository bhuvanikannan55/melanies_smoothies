# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests

# Write directly to the app
st.title(":cup_with_straw: Customise Your Smoothie!:cup_with_straw:")
st.write(
    """Choose the fruit you want in the custom smoothie
    """
)
Name_on_order = st.text_input('Name on Smoothie:')
st.write('The name on smoothie is :', Name_on_order)

cnx = st.connection("snowflake")
session = cnx.session()


#session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'),col('search_on'))
#st.dataframe(data=my_dataframe,use_container_width =True)
#st.stop()

pd_df = my_dataframe.to_pandas()
#st.dataframe(pd_df)
#st.stop()
ingredients_list = st.multiselect(
    "choose upto 5 ingredients",my_dataframe)


if ingredients_list:  
   ingredients_string = ''
   for fruit_chosen in ingredients_list:
       ingredients_string+=fruit_chosen +' '
       search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
       st.write('The search value for ', fruit_chosen,' is ', search_on, '.')
       st.subheader(fruit_chosen + 'Nutrition Information')
       fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+fruit_chosen)
       fv_df = st.dataframe(data=fruityvice_response.json(),use_container_width =True)
  # st.write(ingredients_string)

   my_insert_stmt = """ insert into smoothies.public.orders(ingredients,Name_on_order)
            values ('""" + ingredients_string + """','""" + Name_on_order + """')"""
   st.write(my_insert_stmt)
time_to_insert =st.button('submit_order')

if time_to_insert:
   session.sql(my_insert_stmt).collect()
   st.success('Your Smoothie is ordered!', icon="✅")







