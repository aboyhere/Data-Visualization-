#packages 
import streamlit as st
from streamlit_option_menu import option_menu
import pymysql 
import pandas as pd
import plotly.express as px
import json
import requests
from PIL import Image

#Dataframe creation for visualizing


mydb = pymysql.connect(host="127.0.0.1", user="root", passwd="gabbu", port=3306,database="Phonepe_pulse_columns")

cursor = mydb.cursor()
#aggre_insurence_df
cursor.execute("SELECT * FROM aggregated_insurence")
mydb.commit()
table1 = cursor.fetchall()

Aggre_insurence = pd.DataFrame(table1 ,columns = ('States', 'Year', 
                                                  'Quarter', 'Transaction_type', 'Transaction_count',
                                                  'Transaction_amount'))

#aggre_transaction_df
cursor.execute("SELECT * FROM aggregated_transaction")
mydb.commit()
table2 = cursor.fetchall()

Aggre_transaction = pd.DataFrame(table2 ,columns = ('States', 'Year', 
                                                  'Quarter', 'Transaction_type', 'Transaction_count',
                                                  'Transaction_amount'))



#aggre_user_df
cursor.execute("SELECT * FROM aggregated_user")
mydb.commit()
table3 = cursor.fetchall()

Aggre_user = pd.DataFrame(table3 ,columns = ('States', 'Year', 
                                             'Quarter', 'Brands', 'Transaction_count',
                                             'Percentage'))



#map_insurence
cursor.execute("SELECT * FROM map_insurence")
mydb.commit()
table4 = cursor.fetchall()

map_insurence = pd.DataFrame(table4 ,columns = ('States', 'Year', 
                                             'Quarter','Districts', 
                                               'Transaction_count',
                                               'Transaction_amount'))



#map_transaction
cursor.execute("SELECT * FROM map_transaction")
mydb.commit()
table5 = cursor.fetchall()

map_transaction = pd.DataFrame(table5 ,columns = ('States', 'Year', 
                                             'Quarter','Districts', 
                                               'Transaction_count',
                                               'Transaction_amount'))


#map_user
cursor.execute("SELECT * FROM map_user")
mydb.commit()
table6 = cursor.fetchall()

map_user = pd.DataFrame(table6 ,columns = ('States', 'Year', 
                                             'Quarter','Districts', 
                                               'RegisteredUsers',
                                               'AppOpens'))

#top_insurence
cursor.execute("SELECT * FROM top_insurence")
mydb.commit()
table7 = cursor.fetchall()

top_insurence = pd.DataFrame(table7 ,columns = ('States', 'Year', 'Quarter', 'Pincodes', 'Transaction_count',
                                         'Transaction_amount'))



#top_transaction
cursor.execute("SELECT * FROM top_transaction")
mydb.commit()
table8 = cursor.fetchall()

top_transaction = pd.DataFrame(table8 ,columns = ('States', 'Year', 'Quarter', 'Pincodes', 'Transaction_count',
                                         'Transaction_amount'))


#top_user
cursor.execute("SELECT * FROM top_user")
mydb.commit()
table9 = cursor.fetchall()

top_user = pd.DataFrame(table9 ,columns = ('States', 'Year', 'Quarter', 
                                           'Pincodes', 'RegisteredUsers'))





#plot view
def Transaction_amount_count_Y(df,year):

    tacy =   df[df["Year"] == year]
    tacy.reset_index(drop = True,inplace = True)

    tacyg = tacy.groupby("States")[["Transaction_count","Transaction_amount"]].sum()
    tacyg.reset_index(inplace= True)

    col1,col2 = st.columns(2)
    with col1:


    #plot amount
        fig_amount = px.bar(tacyg, x = "States", y = "Transaction_amount", title = f"TRANSACTION AMOUNT {year}", 
                            color_discrete_sequence= px.colors.sequential.Blugrn, height= 600, width= 600)
        st.plotly_chart(fig_amount)
    with col2:
    #plot count
        fig_count = px.bar(tacyg, x = "States", y = "Transaction_count", title = f"TRANSACTION COUNT {year}", 
                        color_discrete_sequence= px.colors.sequential.Mint_r, height= 600, width = 600)
        st.plotly_chart(fig_count )

       
    url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
    responce = requests.get(url)
    states_name = []
    data1 = json.loads(responce.content)
    for feature in data1["features"]:
        states_name.append(feature["properties"]["ST_NM"])
    states_name.sort()


    col1,col2 = st.columns(2)

    with col1:
        # for transaction amt india map
        india_map_fig1 = px.choropleth(tacyg,geojson = data1, locations = "States", featureidkey="properties.ST_NM",
                                    color = "Transaction_amount", color_continuous_scale= "Rainbow",
                                    range_color = (tacyg["Transaction_amount"].min() , tacyg["Transaction_amount"].max()),
                                    hover_name= "States",title = f"{year} TRANSACTION AMOUNT ANALYSIS", fitbounds="locations",
                                    height = 600 ,width = 600)
        india_map_fig1.update_geos(visible =False)
        st.plotly_chart(india_map_fig1)

    with col2:
        # for count analysis    
        india_map_fig2 = px.choropleth(tacyg,geojson = data1, locations = "States", featureidkey="properties.ST_NM",
                                    color = "Transaction_count", color_continuous_scale= "Rainbow",
                                    range_color = (tacyg["Transaction_count"].min() , tacyg["Transaction_count"].max()),
                                    hover_name= "States",title = f"{year} TRANSACTION COUNT ANALYSIS", fitbounds="locations",
                                    height = 600 ,width = 600)
        india_map_fig2.update_geos(visible =False)
        st.plotly_chart(india_map_fig2)

    return tacy




#Quarter analysis 
def Transaction_amount_count_Y_Q(df,quarter):
    tacy =   df[df["Quarter"] == quarter]
    tacy.reset_index(drop = True,inplace = True)

    tacyg = tacy.groupby("States")[["Transaction_count","Transaction_amount"]].sum()
    tacyg.reset_index(inplace= True)

    #plot amount
    col1,col2 = st.columns(2)

    with col1:

        fig_amount = px.bar(tacyg, x = "States", y = "Transaction_amount", title = f"{tacy['Year'].min()} YEAR {quarter} Quarter YEAR TRANSACTION AMOUNT ", 
                            color_discrete_sequence= px.colors.sequential.Bluered,height = 600 ,width = 600)
        st.plotly_chart(fig_amount)

    with col2:    

        #plot count
        fig_count = px.bar(tacyg, x = "States", y = "Transaction_count", title = f"{tacy['Year'].min()} YEAR {quarter} Quarter TRANSACTION COUNT ", 
                        color_discrete_sequence= px.colors.sequential.Sunsetdark_r,height = 600 ,width = 600)
        st.plotly_chart(fig_count)


    url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
    responce = requests.get(url)
    states_name = []
    data1 = json.loads(responce.content)
    for feature in data1["features"]:
        states_name.append(feature["properties"]["ST_NM"])
    states_name.sort()

    col1,col2 =st.columns(2)

    with col1:

    # for transaction amt india map
        india_map_fig1 = px.choropleth(tacyg,geojson = data1, locations = "States", featureidkey="properties.ST_NM",
                                    color = "Transaction_amount", color_continuous_scale= "Rainbow",
                                    range_color = (tacyg["Transaction_amount"].min() , tacyg["Transaction_amount"].max()),
                                    hover_name= "States",title = f"{tacy['Year'].min()} YEAR {quarter} Quarter TRANSACTION AMOUNT ", fitbounds="locations",
                                    height = 650 ,width = 650)
        india_map_fig1.update_layout (paper_bgcolor ="rgba(0,0,0,0)")
        india_map_fig1.update_geos(visible =False)
        st.plotly_chart(india_map_fig1)

    with col2:    

        # for count analysis   
        india_map_fig2 = px.choropleth(tacyg,geojson = data1, locations = "States", featureidkey="properties.ST_NM",
                                    color = "Transaction_count", color_continuous_scale= "Rainbow",
                                    range_color = (tacyg["Transaction_count"].min() , tacyg["Transaction_count"].max()),
                                    hover_name= "States",title = f"{tacy['Year'].min()} YEAR {quarter} Quarter TRANSACTION COUNT ", fitbounds="locations",
                                    height = 650 ,width = 650)
        india_map_fig2.update_layout (paper_bgcolor ="rgba(0,0,0,0)")
        india_map_fig2.update_geos(visible =False)
        st.plotly_chart(india_map_fig2)
    return tacy




#pie chart
def Aggre_tran_Transaction_type(df,state):


    tacy = df[df["States"] == state]
    tacy.reset_index(drop = True,inplace = True)
    tacyg = tacy.groupby("Transaction_type")[["Transaction_count","Transaction_amount"]].sum()
    tacyg.reset_index(inplace= True)

    col1,col2 = st.columns(2)
    with col1:
        tran_fig1 =  px.pie(data_frame=tacyg, names = "Transaction_type", values="Transaction_amount", width = 600,
                        title = f"{state.upper()} TRANSACTION AMOUNT", hole = 0.55 )
        st.plotly_chart(tran_fig1)

    with col2:
        tran_fig2 =  px.pie(data_frame=tacyg, names = "Transaction_type", values="Transaction_amount", width = 600,
                        title =f" {state.upper()} TRANSACTION COUNT", hole = 0.55 )
        st.plotly_chart(tran_fig2)

# Aggregated user analysis1
def Aggre_user_plot1(df,year):

    aguy =df[df["Year"] == year]
    aguy.reset_index(drop = True, inplace = True)
    aguyg = pd.DataFrame(aguy.groupby('Brands')["Transaction_count"].sum())
    aguyg.reset_index(inplace = True)


    fig_bar1 = px.bar(aguyg, x = "Brands", y = "Transaction_count",title = f"{year} Brands and Transaction count",
                    width= 1100, color_discrete_sequence=px.colors.sequential.haline_r, hover_name = "Brands" )

    st.plotly_chart(fig_bar1)
    return aguy

#Aggre user analysis plot 2
def Aggre_user_plot2(df,quarter):
    aguyq =df[df["Quarter"] == quarter]
    aguyq.reset_index(drop = True, inplace = True)

    aguyq_g =pd.DataFrame(aguyq.groupby("Brands")["Transaction_count"].sum())
    aguyq_g.reset_index(inplace = True)



    fig_bar1 = px.bar(aguyq_g, x = "Brands", y = "Transaction_count",title = f" {quarter} Quarter Brands and Transaction count",
                        width= 1100, color_discrete_sequence=px.colors.sequential.Oranges, hover_name = "Brands")

    st.plotly_chart(fig_bar1)

    return aguyq

#Aggregated user analysis 3
def Aggre_user_plot_3(df,state):
    auyqs = df[df["States"]== state]
    auyqs.reset_index(drop = True, inplace =True)

    fig_line1 = px.line(auyqs, x ="Brands", y ="Transaction_count", hover_data=["Percentage"],
                        title = f" {state.upper()} BRANDS, TRANSACTION COUNT, PERCENTAGE", width=1000,color_discrete_sequence= px.colors.sequential.thermal_r, markers=True )
    st.plotly_chart(fig_line1)


#map insurence districts
def map_insur_district(df,state):


    tacy = df[df["States"] == state]
    tacy.reset_index(drop = True,inplace = True)
    tacyg = tacy.groupby("Districts")[["Transaction_count","Transaction_amount"]].sum()
    tacyg.reset_index(inplace= True)
    col1,col2 =st.columns(2) 

    with col1:

        fig_bar1 =  px.bar(tacyg, x = "Transaction_amount", y = "Districts", orientation= "h",height = 600,         
                            title = f"{state.upper()} STATE AND ITS DISTRICTS AND TRANSACTION AMOUNT", color_discrete_sequence = px.colors.sequential.Oranges)
        st.plotly_chart(fig_bar1)
    with col2:


        fig_bar2 =  px.bar(tacyg, x = "Transaction_amount", y = "Districts", orientation= "h",height = 600,
                        title = f"{state.upper()} STATE AND ITS DISTRICTS AND TRANSACTION COUNT", color_discrete_sequence = px.colors.sequential.Mint_r)
        st.plotly_chart(fig_bar2)


# map user analysis
def  map_user_plot1(df,year):
    muy =df[df["Year"] == year]
    muy.reset_index(drop = True, inplace = True)

    muyg = muy.groupby('States')[["RegisteredUsers","AppOpens"]].sum()
    muyg.reset_index(inplace = True)
    fig_line_mu = px.line(muyg, x ="States", y = ["RegisteredUsers","AppOpens"], title = f"{year} REGISTERED USER AND APP OPENS",
                        width = 1000, height =800, markers=True )
    st.plotly_chart(fig_line_mu)
    return muy



# map user analysis quarter
def  map_user_plot2(df,quarter):
    muyq =df[df["Quarter"] == quarter]
    muyq.reset_index(drop = True, inplace = True)

    muyqg = muyq.groupby('States')[["RegisteredUsers","AppOpens"]].sum()
    muyqg.reset_index(inplace = True)
    fig_line_mu = px.line(muyqg, x ="States", y = ["RegisteredUsers","AppOpens"], title =  f"{df['Year'].min()} YEAR {quarter} Quarter REGISTERED USER AND APP OPENS",
                        width = 1000, height =800, markers=True,
                        color_discrete_sequence =px.colors.sequential.Rainbow_r  )
    st.plotly_chart(fig_line_mu)
    return muyq
    
# map user plot3
def map_user_plot3(df,state):
    muyqs =df[df["States"] == state]
    muyqs.reset_index(drop = True, inplace = True)
    
    col1,col2 =st.columns
    with col1:
        fig_map_user_bar1 =px.bar(muyqs, x ="RegisteredUsers" , y = "Districts", orientation ="h",
        title = f"{state.upper()} RegisteredUsers", height =800,color_discrete_sequence = px.colors.sequential.Rainbow )
        st.plotly_chart(fig_map_user_bar1)
    with col2:
        fig_map_user_bar2 =px.bar(muyqs, x ="AppOpens" , y = "Districts", orientation ="h",
        title = f"{state.upper()} AppOpens", height =800,color_discrete_sequence = px.colors.sequential.Rainbow_r )

        st.plotly_chart(fig_map_user_bar2)


# top insurence plot 1
def top_insur_plot1(df, state):
    tiy =df[df["States"] == state]
    tiy.reset_index(drop = True, inplace = True)
    col1,col2 = st.columns(2)
    with col1:
        #plot 1
        fig_top_insur_bar1 =px.bar(tiy, x ="Quarter" , y = "Transaction_amount", hover_data= ["Pincodes"],
        title = "Transaction amount", height =650,width = 600,color_discrete_sequence = px.colors.sequential.Cividis )
        st.plotly_chart(fig_top_insur_bar1)
 
    with col2:
        #plot 2
        fig_top_insur_bar2 =px.bar(tiy, x ="Quarter" , y = "Transaction_count", hover_data= ["Pincodes"],
        title = "Transaction count", height =650,width = 600,color_discrete_sequence = px.colors.sequential.Cividis )
        st.plotly_chart(fig_top_insur_bar2)

#top user plot1
def top_user_plot1(df,year):
    tuy =df[df["Year"] == year]
    tuy.reset_index(drop = True, inplace = True)
    tuyg = pd.DataFrame(tuy.groupby(["States","Quarter"])["RegisteredUsers"].sum())
    tuyg.reset_index(inplace = True)

    fig_top_user_plot1 = px.bar(tuyg , x ="States", y = "RegisteredUsers", color = "Quarter", width = 1000, height =800, hover_name = "States",
                                color_discrete_sequence = px.colors.sequential.Burgyl, title = f"No of Registered user for {year}")

    st.plotly_chart(fig_top_user_plot1)
    return tuy


#top user plot 2
def top_user_plot2(df,state):
    tuys =df[df["States"] == state]
    tuys.reset_index(drop = True, inplace = True)
    fig_top_user_plot2 = px.bar(tuys, x = "Quarter", y = "RegisteredUsers",title = "Registered user & pincodes", 
                                width =1000, height =800 , color = "RegisteredUsers", hover_data = ["Pincodes"],color_continuous_scale = px.colors.sequential.Magenta)

    st.plotly_chart(fig_top_user_plot2)


# sql connenction
def top_chart_trans_amount(table_name):
    mydb = pymysql.connect(host ="127.0.0.1", user ="root", passwd ="gabbu", port = 3306, database="Phonepe_pulse_columns")
    cursor =mydb.cursor()
    #query for top 10 states with highest transaction amount in insurence
    query1 = f'''select States, sum(Transaction_amount) as Sum_Of_Tran from {table_name}
    group by States
    order by Sum_Of_Tran desc
    limit 10 '''
    

    cursor.execute(query1)
    table1 = cursor.fetchall()
    mydb.commit()

    df_1 = pd.DataFrame(table1 ,columns = ('States', 'Sum_Of_Tran'))

    col1,col2= st.columns(2)
    with col1:

        fig_barchart = px.bar(df_1, x ="States", y = "Sum_Of_Tran", title = "Top 10 States with highest Transaction Amount",
                            hover_name ="States",color='States', color_discrete_sequence=px.colors.qualitative.Plotly,
                            height =650, width = 600)
        st.plotly_chart(fig_barchart)


    #query for top 10 states with highest transaction amount in transaction in ascending order
    query2 = f'''select States, sum(Transaction_amount) as Sum_Of_Tran from {table_name}
    group by States
    order by Sum_Of_Tran 
    limit 10 '''
    

    cursor.execute(query2)
    table2 = cursor.fetchall()
    mydb.commit()

    df_2 = pd.DataFrame(table2 ,columns = ('States', 'Sum_Of_Tran'))

    with col2:
        fig_barchart2 = px.bar(df_2, x ="States", y = "Sum_Of_Tran", title = "Top 10 States with lowest Transaction Amount",
                            hover_name ="States",color='States', color_discrete_sequence=px.colors.qualitative.Plotly,
                            height =650, width = 600)
        st.plotly_chart(fig_barchart2)
    # average value of transaction amount in insurence

    query3 = f'''select States, avg(Transaction_amount) as avg_Of_Tran from {table_name}
    group by States
    order by avg_Of_Tran  '''
    

    cursor.execute(query3)
    table3 = cursor.fetchall()
    mydb.commit()

    df_3 = pd.DataFrame(table3 ,columns = ('States', 'avg_Of_Tran'))

    fig_barchart3 = px.bar(df_3, y ="States", x = "avg_Of_Tran", title = "States with average Transaction Amount", orientation= 'h',
                        hover_name ="States",color='States', color_discrete_sequence=px.colors.qualitative.Plotly,
                        height =800, width = 1000)
    st.plotly_chart(fig_barchart3)



# sql connenction to fetch data for top chart
def top_chart_trans_count(table_name):
    mydb = pymysql.connect(host ="127.0.0.1", user ="root", passwd ="gabbu", port = 3306, database="Phonepe_pulse_columns")
    cursor =mydb.cursor()
    #query for top 10 states with highest transaction amount in insurence
    query1 = f'''select States, sum(Transaction_count) as Sum_Of_count from {table_name}
    group by States
    order by Sum_Of_count desc
    limit 10 '''
    

    cursor.execute(query1)
    table1 = cursor.fetchall()
    mydb.commit()
        
    df_1 = pd.DataFrame(table1 ,columns = ('States', 'Sum_Of_count'))
 
    col1,col2 =st.columns(2)
    with col1:
        fig_barchart = px.bar(df_1, x ="States", y = "Sum_Of_count", title = "Top 10 States with highest Transaction Count",
                            hover_name ="States",color='States', color_discrete_sequence=px.colors.qualitative.Plotly,
                            height =650, width = 600)
        st.plotly_chart(fig_barchart)


    #query for top 10 states with highest transaction amount in transaction in ascending order
    query2 = f'''select States, sum(Transaction_count) as Sum_Of_count from {table_name}
    group by States
    order by Sum_Of_count 
    limit 10 '''
    

    cursor.execute(query2)
    table2 = cursor.fetchall()
    mydb.commit()

    df_2 = pd.DataFrame(table2 ,columns = ('States', 'Sum_Of_count'))

    with col2:
        fig_barchart2 = px.bar(df_2, x ="States", y = "Sum_Of_count", title = "Top 10 States with lowest Transaction Count ",
                            hover_name ="States",color='States', color_discrete_sequence=px.colors.qualitative.Plotly,
                            height =650, width = 600)
        st.plotly_chart(fig_barchart2)

    # average value of transaction count in insurence

    query3 = f'''select States, avg(Transaction_count) as avg_Of_count from {table_name}
    group by States
    order by avg_Of_count desc'''
    

    cursor.execute(query3)
    table3 = cursor.fetchall()
    mydb.commit()

    df_3 = pd.DataFrame(table3 ,columns = ('States', 'avg_Of_count'))

    fig_barchart3 = px.bar(df_3, y ="States", x = "avg_Of_count", title = "States with average Transaction Count", orientation= 'h',
                        hover_name ="States",color='States', color_discrete_sequence=px.colors.qualitative.Plotly,
                        height =800, width = 1000)
    st.plotly_chart(fig_barchart3)



# top chart question
def top_chart_registered_user(table_name,state):
    mydb = pymysql.connect(host ="127.0.0.1", user ="root", passwd ="gabbu", port = 3306, database="Phonepe_pulse_columns")
    cursor =mydb.cursor()
    #query for top 10 states with highest transaction amount in insurence
    query1 = f'''select Districts, sum(RegisteredUsers) as RegisteredUsers  from {table_name}
                where States = '{state}'
                group by Districts
                order by RegisteredUsers desc
                limit 10;'''
    

    cursor.execute(query1)
    table1 = cursor.fetchall()
    mydb.commit()

    df_1 = pd.DataFrame(table1 ,columns = ('Districts', 'RegisteredUsers'))
    col1,col2 =st.columns(2)
    with col1:

        fig_barchart = px.bar(df_1, x ="Districts", y = "RegisteredUsers", title = "Top 10 registered user",
                            hover_name ="Districts",color = "Districts",color_discrete_sequence = px.colors.qualitative.Plotly ,
                            height =650, width = 600)
        st.plotly_chart(fig_barchart)

    #plot 2

    query2 = f'''select Districts, sum(RegisteredUsers) as RegisteredUsers  from {table_name}
                where States = '{state}'
                group by Districts
                order by RegisteredUsers 
                limit 10;'''

    cursor.execute(query2)
    table2 = cursor.fetchall()
    mydb.commit()

    df_2 = pd.DataFrame(table2 ,columns = ('Districts', 'RegisteredUsers'))

    with col2:
        fig_barchart2 = px.bar(df_2, x ="Districts", y = "RegisteredUsers", title = "Sum of last 10 RegisteredUsers",
                            hover_name ="Districts",color = "Districts",color_discrete_sequence = px.colors.qualitative.Plotly ,
                            height =650, width = 600)
        st.plotly_chart(fig_barchart2)

    # average value of transaction amount in insurence

    query3 = f'''select Districts, avg(RegisteredUsers) as RegisteredUsers  from {table_name}
                where States = '{state}'
                group by Districts 
                order by RegisteredUsers desc ;'''
    

    cursor.execute(query3)
    table3 = cursor.fetchall()
    mydb.commit()

    df_3 = pd.DataFrame(table3 ,columns = ('Districts', 'RegisteredUsers'))

    fig_barchart3 = px.bar(df_3, y ="Districts", x = "RegisteredUsers", title = " Average Registered user", orientation= 'h',
                        hover_name ="Districts",color = "Districts" ,color_discrete_sequence = px.colors.qualitative.Pastel,
                        height =650, width = 650)
    st.plotly_chart(fig_barchart3)




# lst ques
def top_chart_appopen(table_name,state):
    mydb = pymysql.connect(host ="127.0.0.1", user ="root", passwd ="gabbu", port = 3306, database="Phonepe_pulse_columns")
    cursor =mydb.cursor()
    #plot 1
    query1 = f'''select Districts, sum(AppOpens) as AppOpens  from {table_name}
                where States = '{state}'
                group by Districts
                order by AppOpens desc
                limit 10;'''
    

    cursor.execute(query1)
    table1 = cursor.fetchall()
    mydb.commit()

    df_1 = pd.DataFrame(table1 ,columns = ('Districts', 'AppOpens'))
    col1,col2 =st.columns(2)
    with col1:
        fig_barchart = px.bar(df_1, x ="Districts", y = "AppOpens", title = "Top 10 Sum of AppOpens",
                            hover_name ="Districts",color = "Districts",color_discrete_sequence = px.colors.qualitative.Plotly ,
                            height =650, width = 600)
        st.plotly_chart(fig_barchart)

    #plot 2

    query2 = f'''select Districts, sum(AppOpens) as AppOpens  from {table_name}
                where States = '{state}'
                group by Districts
                order by AppOpens 
                limit 10;'''

    cursor.execute(query2)
    table2 = cursor.fetchall()
    mydb.commit()

    df_2 = pd.DataFrame(table2 ,columns = ('Districts', 'AppOpens'))
    with col2:
        fig_barchart2 = px.bar(df_2, x ="Districts", y = "AppOpens", title = "Sum of last 10 AppOpens",
                            hover_name ="Districts",color = "Districts",color_discrete_sequence = px.colors.qualitative.Plotly ,
                            height =650, width = 600)
        st.plotly_chart(fig_barchart2)

    # average value of transaction amount in insurence

    query3 = f'''select Districts, avg(AppOpens) as AppOpens  from {table_name}
                where States = '{state}'
                group by Districts 
                order by AppOpens desc ;'''
    

    cursor.execute(query3)
    table3 = cursor.fetchall()
    mydb.commit()

    df_3 = pd.DataFrame(table3 ,columns = ('Districts', 'AppOpens'))

    fig_barchart3 = px.bar(df_3, y ="Districts", x = "AppOpens", title = " Average of AppOpens", orientation= 'h',
                        hover_name ="Districts",color = "Districts" ,color_discrete_sequence = px.colors.qualitative.Pastel,
                        height =650, width = 650)
    st.plotly_chart(fig_barchart3)



# sql connenction last 3 q
def top_chart_registered_users(table_name):
    mydb = pymysql.connect(host ="127.0.0.1", user ="root", passwd ="gabbu", port = 3306, database="Phonepe_pulse_columns")
    cursor =mydb.cursor()
    #query for top 10 states with highest transaction amount in insurence
    query1 = f'''select States, sum(RegisteredUsers) as RegisteredUsers  from {table_name}
                group by States
                order by RegisteredUsers desc
                limit 10;'''
    

    cursor.execute(query1)
    table1 = cursor.fetchall()
    mydb.commit()

    df_1 = pd.DataFrame(table1 ,columns = ('States', 'RegisteredUsers'))
    col1,col2 =st.columns(2)
    with col1:
        fig_barchart = px.bar(df_1, x ="States", y = "RegisteredUsers", title = "Top 10 Registered user",
                            hover_name ="States",color_discrete_sequence = px.colors.qualitative.Light24_r ,
                            height =650, width = 600)
        st.plotly_chart(fig_barchart)

    #plot 2

    query2 = f'''select States, sum(RegisteredUsers) as RegisteredUsers  from {table_name}
                group by States
                order by RegisteredUsers
                limit 10;'''

    cursor.execute(query2)
    table2 = cursor.fetchall()
    mydb.commit()

    df_2 = pd.DataFrame(table2 ,columns = ('States', 'RegisteredUsers'))
    with col2:
        fig_barchart2 = px.bar(df_2, x ="States", y = "RegisteredUsers", title = "Sum of last 10 RegisteredUsers",
                            hover_name ="States",color_discrete_sequence = px.colors.sequential.Plotly3,
                            height =650, width = 600)
        st.plotly_chart(fig_barchart2)

    # average 

    query3 = f'''select States, avg(RegisteredUsers) as RegisteredUsers from {table_name}
                group by States
                order by RegisteredUsers;'''
    

    cursor.execute(query3)
    table3 = cursor.fetchall()
    mydb.commit()

    df_3 = pd.DataFrame(table3 ,columns = ('States', 'RegisteredUsers'))

    fig_barchart3 = px.bar(df_3, y ="States", x = "RegisteredUsers", title = " Average of Registered user", orientation= 'h',
                        hover_name ="States",color = "States" ,color_discrete_sequence = px.colors.qualitative.Pastel,
                        height =650, width = 650)
    st.plotly_chart(fig_barchart3)




#streamli implementation

st.set_page_config(layout = "wide")
st.title("Phonepe Pulse Data Visualization")
with st.sidebar: 
    select = option_menu("Menu",["Home", "Data Exploration", "Top Charts"])
    
if select == "Home":
    
        
    st.markdown("## :violet[A User-Friendly Tool Using Streamlit and Plotly]")
    col1,col2 = st.columns([3,2],gap="medium")
    with col1:
        st.write(" ")
        st.write(" ")
        st.markdown("### :violet[Domain :] Fintech")
        st.markdown("### :violet[Technologies used :] Github Cloning, Python, Pandas, MySQL, pymysql, Streamlit, and Plotly.")
        st.markdown("### :violet[Overview :] In this streamlit web app you can visualize the phonepe pulse data and gain lot of insights on transactions, number of users, top 10 states, district, pincode and which brand has most number of users and so on. Bar charts, Pie charts and Geo map visualization are used to get some insights.")
        st.download_button("Download the app Now","https://www.phonepe.com/app-download/")

    with col2:
    
        st.image(Image.open(r"C:\Users\Manir\Desktop\Phonepe_pulse\phonepe_660_050221042103.webp"),width =500)


    col3,col4= st.columns(2)
    
    with col3:
        st.image(Image.open(r"C:\Users\Manir\Desktop\Phonepe_pulse\phonepe.jfif"),width =500)

    with col4:
        st.write("****Easy Transactions****")
        st.write("****One App For All Your Payments****")
        st.write("****Your Bank Account Is All You Need****")
        st.write("****Multiple Payment Modes****")
        st.write("****PhonePe Merchants****")
        st.write("****Multiple Ways To Pay****")
        st.write("****1.Direct Transfer & More****")
        st.write("****2.QR Code****")
        st.write("****Earn Great Rewards****")



elif select == "Data Exploration":

    tab1,tab2,tab3 = st.tabs(["Aggregated Analysis", "Map Analysis", "Top Analysis"])
    with tab1:
        method = st.radio("Select the Method", ["Insurence Analysis", "Transaction Analysis", "User Analysis"])
        if method == "Insurence Analysis":

            col1,col2 = st.columns(2)
            with col1:

                years = st.slider("Select the Year", Aggre_insurence["Year"].min(),Aggre_insurence["Year"].max(),Aggre_insurence["Year"].min())
            tac_Y = Transaction_amount_count_Y(Aggre_insurence,years)

            col1,col2 = st.columns(2)
            with col1:
                                

                quarter = st.slider("Select the quarter", tac_Y["Quarter"].min(),tac_Y["Quarter"].max(),tac_Y["Quarter"].min())
            Transaction_amount_count_Y_Q(tac_Y,quarter)


        elif method == "Transaction Analysis":
            col1,col2 = st.columns(2)
            with col1:

                years = st.slider("Select the Year", Aggre_transaction["Year"].min(),Aggre_transaction["Year"].max(),Aggre_transaction["Year"].min())
            aggre_tran_tac_Y = Transaction_amount_count_Y(Aggre_transaction,years)

            col1,col2 = st.columns(2)
            with col1:
                states = st.selectbox("Select the State to view" ,aggre_tran_tac_Y["States"].unique())

            Aggre_tran_Transaction_type(aggre_tran_tac_Y,states)

            col1,col2 = st.columns(2)
            with col1:
                                

                quarter = st.slider("Select the quarter", aggre_tran_tac_Y["Quarter"].min(),aggre_tran_tac_Y["Quarter"].max(),aggre_tran_tac_Y["Quarter"].min())
            aggre_tran_tac_Y_Q = Transaction_amount_count_Y_Q(aggre_tran_tac_Y,quarter)

           
            col1,col2 = st.columns(2)
            with col1:
                states = st.selectbox("Select the State to view transsaction type" ,aggre_tran_tac_Y["States"].unique())

            Aggre_tran_Transaction_type(aggre_tran_tac_Y,states)


        elif method == "User Analysis":

            col1,col2 = st.columns(2)
            with col1:

                years = st.slider("Select the Year", Aggre_user["Year"].min(),Aggre_user["Year"].max(),Aggre_user["Year"].min())
            Aggre_user_Y = Aggre_user_plot1(Aggre_user,years)
            
            
            col1,col2 = st.columns(2)
            with col1:
                                

                quarter = st.slider("Select the quarter", Aggre_user_Y["Quarter"].min(),Aggre_user_Y["Quarter"].max(),Aggre_user_Y["Quarter"].min())
            Aggre_user_Y_Q = Aggre_user_plot2(Aggre_user_Y, quarter)
            

            col1,col2 = st.columns(2)
            with col1:
                states = st.selectbox("Select the State to view user history" ,Aggre_user_Y_Q["States"].unique())

            Aggre_user_plot_3(Aggre_user_Y_Q, states)





    with tab2:
        method2 =st.radio("Select the Method", ["Map Insurence", "Map Transaction", "Map user"])
        if method2 == "Map Insurence":


            col1,col2 = st.columns(2)
            with col1:

                years = st.slider("Select the Year Map insurence", map_insurence["Year"].min(),map_insurence["Year"].max(),map_insurence["Year"].min())
            map_insur_tac_Y = Transaction_amount_count_Y(map_insurence,years)
            

            col1,col2 = st.columns(2)
            with col1:
                states = st.selectbox("Select the State_map insurence" ,map_insur_tac_Y["States"].unique())

            map_insur_district(map_insur_tac_Y,states)

            col1,col2 = st.columns(2)
            with col1:
                                

                quarter = st.slider("choose the quarter", map_insur_tac_Y["Quarter"].min(),map_insur_tac_Y["Quarter"].max(),map_insur_tac_Y["Quarter"].min())
            map_insur_tac_Y_Q = Transaction_amount_count_Y_Q(map_insur_tac_Y,quarter)
            

            col1,col2 = st.columns(2)
            with col1:
                states = st.selectbox("choose state" ,map_insur_tac_Y_Q["States"].unique())

            map_insur_district(map_insur_tac_Y_Q,states)




             
        elif method2 == "Map Transaction":
            
            col1,col2 = st.columns(2)
            with col1:

                years = st.slider("Select the Year Map transaction", map_transaction["Year"].min(),map_transaction["Year"].max(),map_transaction["Year"].min())
            map_trans_tac_Y = Transaction_amount_count_Y(map_transaction,years)
            

            col1,col2 = st.columns(2)
            with col1:
                states = st.selectbox("Select the State_map transaction" ,map_trans_tac_Y["States"].unique())

            map_insur_district(map_trans_tac_Y,states)

            col1,col2 = st.columns(2)
            with col1:
                                

                quarter = st.slider("choose the quarter_MT", map_trans_tac_Y["Quarter"].min(),map_trans_tac_Y["Quarter"].max(),map_trans_tac_Y["Quarter"].min())
            map_trans_tac_Y_Q = Transaction_amount_count_Y_Q(map_trans_tac_Y,quarter)
            

            col1,col2 = st.columns(2)
            with col1:
                states = st.selectbox("choose state_MT" ,map_trans_tac_Y_Q["States"].unique())

            map_insur_district(map_trans_tac_Y_Q,states)




        elif method2 == "Map user":
            col1,col2 = st.columns(2)
            with col1:

                years = st.slider("Select the Year M_U", map_user["Year"].min(),map_user["Year"].max(),map_user["Year"].min())
            map_user_Y = map_user_plot1(map_user,years)

            
            col1,col2 = st.columns(2)
            with col1:
                                

                quarter = st.slider("choose the quarter_MU", map_user_Y["Quarter"].min(),map_user_Y["Quarter"].max(),map_user_Y["Quarter"].min())
            map_user_Y_Q = map_user_plot2(map_user_Y,quarter)

            
            col1,col2 = st.columns(2)
            with col1:
                states = st.selectbox("choose state to view map user" ,map_user_Y_Q["States"].unique())

            map_user_plot3(map_user_Y_Q,states)

            
                         
    

    with tab3:
        method3 =st.radio("Select the Method", ["Top Insurence", "Top Transaction", "Top user"])
        if method3 == "Top Insurence":  

            col1,col2  = st.columns(2)
            with col1:
                years = st.slider("Select the Year ", top_insurence["Year"].min(),top_insurence["Year"].max(),top_insurence["Year"].min())
            top_insur_tac_Y = Transaction_amount_count_Y(top_insurence,2023)
            
            col1,col2  = st.columns(2)
            with col1:
                state = st.selectbox("Select state", top_insur_tac_Y["States"].unique())
                
            top_insur_plot1(top_insur_tac_Y, state)

            col1,col2 = st.columns(2)
            with col1:
                                

                quarter = st.slider("select the quarter ", top_insur_tac_Y["Quarter"].min(),top_insur_tac_Y["Quarter"].max(),top_insur_tac_Y["Quarter"].min())
            top_insur_tac_Y_Q = Transaction_amount_count_Y_Q(top_insur_tac_Y,quarter)



        elif method3 == "Top Transaction":

            col1,col2  = st.columns(2)
            with col1:
                years = st.slider("Select the Year ", top_transaction["Year"].min(),top_transaction["Year"].max(),top_transaction["Year"].min())
            top_trans_tac_Y = Transaction_amount_count_Y(top_transaction,2023)
            
            col1,col2  = st.columns(2)
            with col1:
                state = st.selectbox("click to Select the state", top_trans_tac_Y["States"].unique())
                
            top_insur_plot1(top_trans_tac_Y, state)

            col1,col2 = st.columns(2)
            with col1:
                                

                quarter = st.slider("click to select the quarter ", top_trans_tac_Y["Quarter"].min(),top_trans_tac_Y["Quarter"].max(),top_trans_tac_Y["Quarter"].min())
            top_trans_tac_Y_Q = Transaction_amount_count_Y_Q(top_trans_tac_Y,quarter)




             
        elif method3 == "Top user":
 
            col1,col2  = st.columns(2)
            with col1:
                years = st.slider("Selece Year", top_user["Year"].min(),top_user["Year"].max(),top_user["Year"].min())
            top_user_Y = top_user_plot1(top_user,years)

            col1,col2  = st.columns(2)
            with col1:
                state = st.selectbox("Select State", top_user_Y["States"].unique())
                
            top_user_plot2(top_user_Y, state)
            
        
        
elif select == "Top Charts":
    
    questions = st.selectbox("Select the question",
                             ["1. Transaction Amount and count of Aggregated Insurence",
                                "2. Transaction Amount and count of Map Insurence",
                                "3. Transaction Amount and count of Top Insurence",
                                "4. Transaction Amount and count of Aggregated Transaction",
                                "5. Transaction Amount and count of Map Transaction",
                                "6. Transaction Amount and count of Top Transaction",
                                "7. Transaction Count of Aggregated user",
                                "8. Registered users of Map User",
                                "9. App opens of Map User",
                                "10. Registered user of Top User"])

    if questions == "1. Transaction Amount and count of Aggregated Insurence":

        st.subheader("TRANSACTION AMOUNT")
        top_chart_trans_amount("aggregated_insurence")
        st.subheader("TRANSACTION COUNT")
        top_chart_trans_count("aggregated_insurence")
    


    elif questions == "2. Transaction Amount and count of Map Insurence":

        st.subheader("TRANSACTION AMOUNT")
        top_chart_trans_amount("map_insurence")
        st.subheader("TRANSACTION COUNT")
        top_chart_trans_count("map_insurence")


    elif questions == "3. Transaction Amount and count of Top Insurence":

        st.subheader("TRANSACTION AMOUNT")
        top_chart_trans_amount("top_insurence")
        st.subheader("TRANSACTION COUNT")
        top_chart_trans_count("top_insurence")
    
    elif questions == "4. Transaction Amount and count of Aggregated Transaction":

        st.subheader("TRANSACTION AMOUNT")
        top_chart_trans_amount("aggregated_transaction")
        st.subheader("TRANSACTION COUNT")
        top_chart_trans_count("aggregated_transaction")
    
    elif questions == "5. Transaction Amount and count of Map Transaction":

        st.subheader("TRANSACTION AMOUNT")
        top_chart_trans_amount("map_transaction")
        st.subheader("TRANSACTION COUNT")
        top_chart_trans_count("map_transaction")
    
    elif questions == "6. Transaction Amount and count of Top Transaction":

        st.subheader("TRANSACTION AMOUNT")
        top_chart_trans_amount("top_transaction")
        st.subheader("TRANSACTION COUNT")
        top_chart_trans_count("top_transaction")
    
      

    elif questions == "7. Transaction Count of Aggregated user":

        st.subheader("TRANSACTION COUNT")
        top_chart_trans_count("aggregated_user")
    

    elif questions == "8. Registered users of Map User":
        states = st.selectbox("Select the State", map_user["States"].unique())
        st.subheader("REGISTERED USER")
        top_chart_registered_user("map_user", states)
     

    elif questions == "9. App opens of Map User":
        states = st.selectbox("Select the State", map_user["States"].unique())
        st.subheader("APPS OPEN")
        top_chart_appopen("map_user", states)

    
    elif questions == "10. Registered user of Top User":
        st.subheader("REGISTERED USER")
        top_chart_registered_users("top_user")

    
