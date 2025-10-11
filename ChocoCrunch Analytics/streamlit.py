import pandas as pd
import streamlit as st
import numpy as np
import pymysql
import altair as alt
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import os


conn=pymysql.connect(
    # host='chococrunch.c1eg6mc4azh2.ap-south-1.rds.amazonaws.com',
    # user='admin',
    # password='Guvi1234',
    # database='Chococruch'
    # host='localhost',        # or your host
    # user='root',
    # password='12345678',
    # database='guviprojects',
    DB_USER = os.getenv("DB_USER"),
    DB_PASS = os.getenv("DB_PASS"),
    DB_HOST = os.getenv("DB_HOST"),
    DB_NAME = os.getenv("DB_NAME")
)

# cursor = conn.cursor()
select_table=['Product Info','Nutrient Info','Derived Metrics','Join-Based Queries']
choose=st.selectbox("Select and Option",select_table)
try:
    cursor = conn.cursor()
    if choose==select_table[0]:
        choose_query=['Count products per brand','Count unique products per brand','Top 5 brands by product count','Products with missing product name',
                      'Number of unique brands','Products with code starting with 3']
        selected_query=st.selectbox("Choose an Query to view Answers",choose_query)

        if selected_query==choose_query[0]:
            query='''select brand,count(product_name) `Total Products` from product_info group by brand order by `Total Products` desc;'''
            cursor.execute(query)
            results=cursor.fetchall()
            results_columns = [desc[0] for desc in cursor.description]
            results_df = pd.DataFrame(results, columns=results_columns,index=None)
            n = st.slider("Select number of top brands to view", 1, len(results_df), 10)
            top_brands = results_df.sort_values("Total Products", ascending=False).head(n)
            st.dataframe(top_brands.reset_index(drop=True))
            # st.bar_chart(top_brands,x='brand',y='Total Products',x_label='Brand')

            # Altair chart (keeps order!)
            bar_chart = (
                alt.Chart(top_brands)
                .mark_bar()
                .encode(
                    x=alt.X("brand", sort=top_brands["brand"].tolist()),  # keep order
                    y="Total Products"
                )
            )

            st.altair_chart(bar_chart, use_container_width=True)

        if selected_query==choose_query[1]:
            query='''select brand,count(distinct product_name) `Unique Products` from product_info 
            group by brand order by `Unique Products` desc;'''
            cursor.execute(query)
            results=cursor.fetchall()
            results_columns = [desc[0] for desc in cursor.description]
            results_df = pd.DataFrame(results, columns=results_columns,index=None)
            n = st.slider("Select number of top brands to view",min_value= 10, max_value=len(results_df),value= 10,step=5)
            top_brands = results_df.sort_values("Unique Products", ascending=False).head(n)
            st.dataframe(top_brands.reset_index(drop=True))
            # st.bar_chart(top_brands,x='brand',y='Total Products',x_label='Brand')

            # Altair chart (keeps order!)
            bar_chart = (
                alt.Chart(top_brands)
                .mark_bar()
                .encode(
                    x=alt.X("brand", sort=top_brands["brand"].tolist()),  # keep order
                    y="Unique Products"
                )
            )

            st.altair_chart(bar_chart, use_container_width=True)

        if selected_query==choose_query[2]:
            query='''select brand Brand,count(product_name) `Count of Products` from product_info 
            group by brand order by `Count of Products` desc Limit 5;'''
            cursor.execute(query)
            results=cursor.fetchall()
            results_columns = [desc[0] for desc in cursor.description]
            results_df = pd.DataFrame(results, columns=results_columns,index=None)
            st.dataframe(results_df.reset_index(drop=True))
            # st.bar_chart(top_brands,x='brand',y='Total Products',x_label='Brand')

            # Altair chart (keeps order!)
            bar_chart = (
                alt.Chart(results_df)
                .mark_bar()
                .encode(
                    y=alt.Y("Brand", sort=results_df["Brand"].tolist()),  # keep order
                    x="Count of Products",
                    color="Brand"
                )
            )

            st.altair_chart(bar_chart, use_container_width=True)

        if selected_query==choose_query[3]:
            query='''select brand `Brand`,count(*) `No Product Names` from product_info
              where product_name is null group by brand order by `No Product Names` desc;'''
            cursor.execute(query)
            results=cursor.fetchall()
            results_columns = [desc[0] for desc in cursor.description]
            results_df = pd.DataFrame(results, columns=results_columns,index=None)
            n = st.slider("Select number of top brands to view",min_value= 10, max_value=len(results_df),value= 10,step=5)
            top_brands = results_df.sort_values("No Product Names", ascending=False).head(n)
            st.dataframe(top_brands.reset_index(drop=True))
            # st.bar_chart(top_brands,x='brand',y='Total Products',x_label='Brand')

            # Altair chart (keeps order!)
            bar_chart = (
                alt.Chart(top_brands)
                .mark_bar()
                .encode(
                    x=alt.X("Brand", sort=top_brands["Brand"].tolist()),  # keep order
                    y="No Product Names"
                )
            )

            st.altair_chart(bar_chart, use_container_width=True)




        if selected_query==choose_query[4]:
            query='''select count(distinct brand) `Unique Brands` from product_info;'''
            cursor.execute(query)
            results=cursor.fetchall()
            results_columns = [desc[0] for desc in cursor.description]
            # results_df = pd.DataFrame(results, columns=results_columns,index=None)
            # st.write(
            # results[0][0])
            st.metric(results_columns[0],results[0][0],border=True,label_visibility="visible")

        if selected_query==choose_query[5]:
            query='''select product_name from product_info where product_code like '3%' and product_name is not null;'''
            cursor.execute(query)
            results=cursor.fetchall()
            results_columns = [desc[0] for desc in cursor.description]
            results_df = pd.DataFrame(results, columns=results_columns,index=None)
            st.dataframe(results_df.reset_index(drop=True))
            text = " ".join(results_df['product_name'])
            wordcloud = WordCloud(width=800, height=400, background_color="white").generate(text)

            fig, ax = plt.subplots()
            ax.imshow(wordcloud, interpolation="bilinear")
            ax.axis("off")

            st.pyplot(fig)


    if choose==select_table[1]:
        choose_query=['Top 10 products with highest energy-kcal_value','Average sugars_value per nova-group',
                      'Count products with fat_value > 20g','Average carbohydrates_value per product',
                      'Products with sodium_value > 1g','Count products with non-zero fruits-vegetables-nuts content',
                      'Products with energy-kcal_value > 500']
        selected_query=st.selectbox("Choose an Query to view Answers",choose_query)

        if selected_query==choose_query[0]:
            query='''select p.product_name `Product Name`,n.energy_kcal_value `Energy Kcal Value` from product_info p 
            join nutrient_info n on n.product_code=p.product_code where p.product_name is not null order by energy_kcal_value desc limit 10;'''
            cursor.execute(query)
            results=cursor.fetchall()
            results_columns = [desc[0] for desc in cursor.description]
            results_df = pd.DataFrame(results, columns=results_columns,index=None)
            st.dataframe(results_df.reset_index(drop=True))
            # st.bar_chart(top_brands,x='brand',y='Total Products',x_label='Brand')

            # Altair chart (keeps order!)
            bar_chart = (
                alt.Chart(results_df)
                .mark_bar()
                .encode(
                    y=alt.Y("Product Name", sort=results_df["Product Name"].tolist()),  # keep order
                    x="Energy Kcal Value"
                )
            )

            st.altair_chart(bar_chart, use_container_width=True)

        if selected_query==choose_query[1]:
            query='''select nova_group `Nova Group`,avg(sugars_value) `Average Sugar Value` from nutrient_info 
            group by nova_group order by nova_group;'''
            cursor.execute(query)
            results=cursor.fetchall()
            results_columns = [desc[0] for desc in cursor.description]
            results_df = pd.DataFrame(results, columns=results_columns,index=None)
            st.dataframe(results_df.reset_index(drop=True))
            # st.bar_chart(top_brands,x='brand',y='Total Products',x_label='Brand')

            # Altair chart (keeps order!)
            bar_chart = (
                alt.Chart(results_df)
                .mark_bar()
                .encode(
                    y=alt.Y(
            "Nova Group:O",  # ordinal axis
            sort=results_df["Nova Group"].tolist(), 
            axis=alt.Axis(
                tickMinStep=1   # force step size of 1
            )
        ),
                    x="Average Sugar Value"
                )
            )

            st.altair_chart(bar_chart, use_container_width=True)

        if selected_query==choose_query[2]:
            query='''select count(p.product_name) `Products with Fat Value > 20g` from product_info p 
            join nutrient_info n on n.product_code=p.product_code where n.fat_value>20;'''
            cursor.execute(query)
            results=cursor.fetchall()
            results_columns = [desc[0] for desc in cursor.description]
            # results_df = pd.DataFrame(results, columns=results_columns,index=None)
            # st.write(
            # results[0][0])
            st.metric(results_columns[0],results[0][0],border=True,label_visibility="visible")    

        if selected_query==choose_query[3]:
            query='''select p.product_name `Product Name`,avg(n.carbohydrates_value) `Average Carbs Value` from product_info p 
            join nutrient_info n on n.product_code=p.product_code 
            group by p.product_name order by `Average Carbs Value` desc;'''
            cursor.execute(query)
            results=cursor.fetchall()
            
            results_columns = [desc[0] for desc in cursor.description]
            results_df = pd.DataFrame(results, columns=results_columns,index=None)
            n = st.slider("Select number of top Product Name to view",min_value= 10, max_value=len(results_df),value= 10,step=5)
            top_brands = results_df.sort_values("Average Carbs Value", ascending=False).head(n)
            st.dataframe(top_brands.reset_index(drop=True))
            # st.bar_chart(top_brands,x='brand',y='Total Products',x_label='Brand')

            # Altair chart (keeps order!)
            bar_chart = (
                alt.Chart(top_brands)
                .mark_bar()
                .encode(
                    x=alt.X("Product Name", sort=top_brands["Average Carbs Value"].tolist()),  # keep order
                    y="Average Carbs Value"
                )
            )

            st.altair_chart(bar_chart, use_container_width=True)
        
        if selected_query==choose_query[4]:
            query='''select p.product_name from product_info p 
            join nutrient_info n on n.product_code=p.product_code where n.sodium_value>1
            and p.product_name is not null;'''
            cursor.execute(query)
            results=cursor.fetchall()
            results_columns = [desc[0] for desc in cursor.description]
            results_df = pd.DataFrame(results, columns=results_columns,index=None)
            st.dataframe(results_df.reset_index(drop=True))
            text = " ".join(results_df['product_name'])
            wordcloud = WordCloud(width=800, height=400, background_color="white").generate(text)

            fig, ax = plt.subplots()
            ax.imshow(wordcloud, interpolation="bilinear")
            ax.axis("off")

            st.pyplot(fig)
        
        if selected_query==choose_query[5]:
            query='''select count(product_code)as `Non zero fruits vegetables nuts content` 
            from nutrient_info where fruits_vegetables_nuts_estimate_from_ingredients_100g!=0;'''
            cursor.execute(query)
            results=cursor.fetchall()
            results_columns = [desc[0] for desc in cursor.description]
            # results_df = pd.DataFrame(results, columns=results_columns,index=None)
            # st.write(
            # results[0][0])
            st.metric(results_columns[0],results[0][0],border=True,label_visibility="visible")   

        if selected_query==choose_query[6]:
            query='''select p.product_name `Product Name`,n.energy_kcal_value from product_info p 
                    join nutrient_info n on n.product_code=p.product_code where n.energy_kcal_value>500 
                    and p.product_name is not null order by n.energy_kcal_value desc;
                    '''
            cursor.execute(query)
            results=cursor.fetchall()
            
            results_columns = [desc[0] for desc in cursor.description]
            results_df = pd.DataFrame(results, columns=results_columns,index=None)
            n = st.slider("Select number of top Product Name to view",min_value= 10, max_value=len(results_df),value= 10,step=5)
            top_brands = results_df.sort_values("energy_kcal_value", ascending=False).head(n)
            st.dataframe(top_brands.reset_index(drop=True))
            # st.bar_chart(top_brands,x='brand',y='Total Products',x_label='Brand')

            # Altair chart (keeps order!)
            bar_chart = (
                alt.Chart(top_brands)
                .mark_bar()
                .encode(
                    x=alt.X("Product Name", sort=top_brands["Product Name"].tolist()),  # keep order
                    y="energy_kcal_value"
                )
            )
            st.altair_chart(bar_chart, use_container_width=True)
    if choose==select_table[2]:
        choose_query=['Count products per calorie_category','Count of High Sugar products',
                      'Average sugar_to_carb_ratio for High Calorie products','Products that are both High Calorie and High Sugar',
                      'Number of products marked as ultra-processed','Products with sugar_to_carb_ratio > 0.7',
                      'Average sugar_to_carb_ratio per calorie_category']
        selected_query=st.selectbox("Choose an Query to view Answers",choose_query)
        if selected_query==choose_query[0]:
            query='''select calorie_category,count(product_code) as countno from derived_metrics group by calorie_category;
                    '''
            cursor.execute(query)
            results=cursor.fetchall()
            results_columns = [desc[0] for desc in cursor.description]
            results_df = pd.DataFrame(results, columns=results_columns,index=None)
            st.dataframe(results_df.reset_index(drop=True))
            st.subheader("Calorie Category Distribution")
            fig, ax = plt.subplots()
            ax.pie(results_df["countno"], labels=results_df["calorie_category"], autopct="%1.1f%%", startangle=90)
            ax.axis("equal")  # Equal aspect ratio makes the pie circular
            st.pyplot(fig)

        if selected_query==choose_query[1]:
            query='''select count(product_code) as `Total High Sugar Products` from derived_metrics where sugar_category='High Sugar';'''
            cursor.execute(query)
            results=cursor.fetchall()
            results_columns = [desc[0] for desc in cursor.description]
            # results_df = pd.DataFrame(results, columns=results_columns,index=None)
            # st.write(
            # results[0][0])
            st.metric(results_columns[0],results[0][0],border=True,label_visibility="visible")   

        if selected_query==choose_query[2]:
            query='''select round(avg(sugar_to_carb_ratio),1) `Average Sugar to Carb Ratio` from derived_metrics where calorie_category='High';'''
            cursor.execute(query)
            results=cursor.fetchall()
            results_columns = [desc[0] for desc in cursor.description]
            # results_df = pd.DataFrame(results, columns=results_columns,index=None)
            # st.write(
            # results[0][0])
            st.metric(results_columns[0],results[0][0],border=True,label_visibility="visible")   
        
        if selected_query==choose_query[3]:
            query='''select p.product_name from derived_metrics d join product_info p on p.product_code=d.product_code
                    where d.sugar_category='High Sugar' and d.calorie_category='High' and p.product_name is not null;'''
            cursor.execute(query)
            results=cursor.fetchall()
            results_columns = [desc[0] for desc in cursor.description]
            results_df = pd.DataFrame(results, columns=results_columns,index=None)
            st.dataframe(results_df.reset_index(drop=True))
            text = " ".join(results_df['product_name'])
            wordcloud = WordCloud(width=800, height=400, background_color="white").generate(text)

            fig, ax = plt.subplots()
            ax.imshow(wordcloud, interpolation="bilinear")
            ax.axis("off")

            st.pyplot(fig)

        if selected_query==choose_query[4]:
            query='''select count(product_code) `Ultra Processed Products`from derived_metrics where is_ultra_processed='yes';'''
            cursor.execute(query)
            results=cursor.fetchall()
            results_columns = [desc[0] for desc in cursor.description]
            # results_df = pd.DataFrame(results, columns=results_columns,index=None)
            # st.write(
            # results[0][0])
            st.metric(results_columns[0],results[0][0],border=True,label_visibility="visible")   

        if selected_query==choose_query[5]:
            query='''select p.product_name,d.sugar_to_carb_ratio from derived_metrics d join product_info p on p.product_code=d.product_code 
                    where d.sugar_to_carb_ratio>0.7 and p.product_name is not null;'''
            cursor.execute(query)
            results=cursor.fetchall()
            results_columns = [desc[0] for desc in cursor.description]
            results_df = pd.DataFrame(results, columns=results_columns,index=None)
            st.dataframe(results_df.reset_index(drop=True))
            bubble_chart = (
                alt.Chart(results_df)
                .mark_circle()
                .encode(
                    x=alt.X("sugar_to_carb_ratio", title="Sugar-to-Carb Ratio"),
                    y=alt.Y("product_name", sort=None, title=""),
                    size=alt.value(500),
                    color=alt.Color("product_name", legend=None),
                    tooltip=["product_name", "sugar_to_carb_ratio"]
                )
                .properties(
                    width=700,
                    height=400,
                    title="Products with High Sugar-to-Carb Ratio (> 0.7)"
                )
            )

            st.altair_chart(bubble_chart, use_container_width=True)

        if selected_query==choose_query[6]:
            query='''select calorie_category,avg(sugar_to_carb_ratio) avg_ratio from derived_metrics group by calorie_category;'''
            cursor.execute(query)
            results=cursor.fetchall()
            results_columns = [desc[0] for desc in cursor.description]
            results_df = pd.DataFrame(results, columns=results_columns,index=None)
            st.dataframe(results_df.reset_index(drop=True))
            results_df["angle"] = results_df["avg_ratio"] * 360

            radial = (
                alt.Chart(results_df)
                .mark_arc(innerRadius=60)
                .encode(
                    theta=alt.Theta("avg_ratio", stack=True),
                    radius=alt.Radius("avg_ratio", scale=alt.Scale(type="sqrt", zero=True, rangeMin=20, rangeMax=150)),
                    color=alt.Color("calorie_category", legend=None),
                    tooltip=["calorie_category", "avg_ratio"]
                )
                .properties(title="Radial View of Avg Sugar-to-Carb Ratio by Calorie Category")
            )
            st.altair_chart(radial, use_container_width=True)
    
    if choose==select_table[3]:
        choose_query=['Top 5 brands with most High Calorie products','Average energy-kcal_value for each calorie_category',
                      'Count of ultra-processed products per brand','Products with High Sugar and High Calorie along with brand',
                      'Average sugar content per brand for ultra-processed products','Number of products with fruits/vegetables/nuts content in each calorie_category',
                      'Top 5 products by sugar_to_carb_ratio with their calorie and sugar category']
        selected_query=st.selectbox("Choose an Query to view Answers",choose_query)
        if selected_query==choose_query[0]:
            query='''select p.brand,count(p.product_name) as high_cal_products from derived_metrics d 
            join product_info p on p.product_code=d.product_code
            where d.calorie_category='High' group by p.brand order by high_cal_products desc limit 5;
                    '''
            cursor.execute(query)
            results=cursor.fetchall()
            results_columns = [desc[0] for desc in cursor.description]
            results_df = pd.DataFrame(results, columns=results_columns,index=None)
            st.dataframe(results_df.reset_index(drop=True))
            bar_chart = (
                alt.Chart(results_df)
                .mark_bar(cornerRadiusTopLeft=8, cornerRadiusBottomLeft=8)
                .encode(
                    y=alt.Y("brand", sort='-x', title="Brand"),
                    x=alt.X("high_cal_products", title="High-Calorie Products"),
                    color=alt.Color("brand", legend=None),
                    tooltip=["brand", "high_cal_products"]
                )
                .properties(
                    title="Top 5 Brands by High-Calorie Products",
                    width=700,
                    height=400
                )
            )
            st.altair_chart(bar_chart, use_container_width=True)
        if selected_query==choose_query[1]:
            query='''select d.calorie_category,avg(n.energy_kcal_value) as avg_energy_kcal_value from derived_metrics d 
            join product_info p on p.product_code=d.product_code
            join nutrient_info n  on n.product_code=d.product_code group by d.calorie_category;
                    '''
            cursor.execute(query)
            results=cursor.fetchall()
            results_columns = [desc[0] for desc in cursor.description]
            results_df = pd.DataFrame(results, columns=results_columns,index=None)
            st.dataframe(results_df.reset_index(drop=True))
            st.subheader("Calorie Category Distribution for Average Energy Kcal Values")
            fig, ax = plt.subplots()
            ax.pie(results_df["avg_energy_kcal_value"], labels=results_df["calorie_category"], autopct="%1.1f%%", startangle=90)
            ax.axis("equal")  # Equal aspect ratio makes the pie circular
            st.pyplot(fig)

        if selected_query==choose_query[2]:
            query='''select p.brand,count(d.is_ultra_processed) as count_of_ultra_processed from derived_metrics d 
                    join product_info p on p.product_code=d.product_code where d.is_ultra_processed='yes' 
                    group by p.brand order by count_of_ultra_processed desc;
                    '''
            cursor.execute(query)
            results=cursor.fetchall()
            results_columns = [desc[0] for desc in cursor.description]
            results_df = pd.DataFrame(results, columns=results_columns,index=None)
            n = st.slider("Select number of top brands to view",min_value= 10, max_value=len(results_df),value= 10,step=5)
            top_df = results_df.sort_values("count_of_ultra_processed", ascending=False).head(n)  # ascending for horizontal

            st.dataframe(top_df.reset_index(drop=True))
            # st.bar_chart(top_brands,x='brand',y='Total Products',x_label='Brand')

            # Altair chart (keeps order!)
            bar_chart = (
                alt.Chart(top_df)
                .mark_bar()
                .encode(
                    x=alt.X("brand", sort=top_df["brand"].tolist()),  # keep order
                    y="count_of_ultra_processed"
                )
            )

            st.altair_chart(bar_chart, use_container_width=True)
        if selected_query==choose_query[3]:
            query='''select p.brand,p.product_name from derived_metrics d 
            join product_info p on p.product_code=d.product_code
            where d.sugar_category='High Sugar' and d.calorie_category='High'; 
                    '''
            cursor.execute(query)
            results=cursor.fetchall()
            results_columns = [desc[0] for desc in cursor.description]
            results_df = pd.DataFrame(results, columns=results_columns,index=None)
            st.dataframe(results_df.reset_index(drop=True))
            st.subheader("Expandable List by Brand")
            for brand in results_df['brand'].unique():
                with st.expander(f"{brand}"):
                    products = results_df[results_df['brand'] == brand]['product_name'].tolist()
                    st.write(products)

        if selected_query==choose_query[4]:
            query=''' select p.brand,avg(n.sugars_value) as avg_sugars_content from derived_metrics d 
            join product_info p on p.product_code=d.product_code
            join nutrient_info n  on n.product_code=d.product_code where d.is_ultra_processed='yes' group by p.brand; 
                    '''
            cursor.execute(query)
            results=cursor.fetchall()
            results_columns = [desc[0] for desc in cursor.description]
            results_df = pd.DataFrame(results, columns=results_columns,index=None)
            st.dataframe(results_df.reset_index(drop=True))
            chart = alt.Chart(results_df).mark_circle(size=100, color='red').encode(
                x='avg_sugars_content:Q',
                y=alt.Y('brand:N', sort='-x'),
                tooltip=['brand', 'avg_sugars_content']
            ).properties(title='Average Sugar Content by Brand (Ultra-Processed Products)')

            st.altair_chart(chart, use_container_width=True)

        if selected_query==choose_query[5]:
            query=''' select d.calorie_category,count(p.product_code) as count_products from nutrient_info n 
                    join derived_metrics d on d.product_code=n.product_code 
                    join product_info p on p.product_code=n.product_code 
                    where n.fruits_vegetables_nuts_estimate_from_ingredients_100g>0
                    group by d.calorie_category; 
                    '''
            cursor.execute(query)
            results=cursor.fetchall()
            results_columns = [desc[0] for desc in cursor.description]
            results_df = pd.DataFrame(results, columns=results_columns,index=None)
            st.dataframe(results_df.reset_index(drop=True))
            fig, ax = plt.subplots()
            ax.pie(results_df["count_products"], labels=results_df["calorie_category"], autopct="%1.1f%%", startangle=90)
            ax.axis("equal")  # Equal aspect ratio makes the pie circular
            st.pyplot(fig)


        
        
        if selected_query==choose_query[6]:
            query='''select p.product_name,d.calorie_category,d.sugar_category,d.sugar_to_carb_ratio from nutrient_info n 
                        join derived_metrics d on d.product_code=n.product_code 
                        join product_info p on p.product_code=n.product_code
                        order by d.sugar_to_carb_ratio desc limit 5;
                    '''
            cursor.execute(query)
            results=cursor.fetchall()
            results_columns = [desc[0] for desc in cursor.description]
            results_df = pd.DataFrame(results, columns=results_columns,index=None)
            st.dataframe(results_df.reset_index(drop=True))
            chart = (
                alt.Chart(results_df)
                .mark_circle(size=150, color='crimson')
                .encode(
                    x=alt.X('sugar_to_carb_ratio', title='Sugar-to-Carb Ratio'),
                    y=alt.Y('product_name', sort=results_df['product_name'].tolist()),
                    tooltip=['product_name', 'calorie_category', 'sugar_category', 'sugar_to_carb_ratio']
                )
            ) + (
                alt.Chart(results_df)
                .mark_rule(color='gray')
                .encode(
                    x='sugar_to_carb_ratio',
                    y='product_name',
                    y2='product_name'
                )
            )

            st.altair_chart(chart, use_container_width=True)


finally:
    cursor.close()
    conn.close()
