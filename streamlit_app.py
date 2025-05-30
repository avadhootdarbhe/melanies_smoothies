# Import python packages
import streamlit as st
import requests
from snowflake.snowpark.functions import col
import pandas as pd

# Write directly to the app
st.title(f"Customize Your Smoothie! :cup_with_straw:")
st.write(
  """Choose the fruits you want in your custom Smoothie."""
)


conn = st.connection("snowflake")
session = conn.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'), col('SEARCH_ON'))
# st.dataframe(data=my_dataframe, use_container_width=True)

# st.dataframe(data=pd_df, use_container_width=True)
# st.stop()


name_on_order = st.text_input("Name of Smoothie: ")
st.write("The name of the Smoothie will be:", name_on_order)

pd_df = my_dataframe.to_pandas()
# st.dataframe(data=pd_df)
# st.stop()


ingredient_list = st.multiselect(
    "Choose upto 5 ingredients",
    my_dataframe,
    max_selections=5
   ,
)





if ingredient_list:
    ingredient_string = ''
    for fruit_chosen in ingredient_list:
        ingredient_string += fruit_chosen + ' '
        search_on = pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        # st.write("The search value for ", fruit_chosen, 'is', search_on, '.')
        st.subheader(fruit_chosen + " Nutritional Information") 
        # smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/" + search_on)
        # sf_df = st.dataframe(smoothiefroot_response.json(), use_container_width=True)

    my_insert_stmt = """ insert into SMOOTHIES.PUBLIC.ORDERS(ingredients, name_on_order)
            values ('""" + ingredient_string + """', '""" + name_on_order + """')"""

    # st.write(my_insert_stmt)
    # st.stop()

    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success("Your Smoothie is ordered!",icon="✅")

    
