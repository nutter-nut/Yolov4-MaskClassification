import pandas as pd #pip insatll pandas คือ library สำหรับจัดการ dataframe
import plotly.express as px #pip install plotly-express คือ นำข้อมูลมาแสดงผลในรูปแบบของแผนภูมิหรือกราฟต่างๆ
import streamlit as st #pip install streamlit คือ Library API อื่นเป็นตัวช่วยในการติดต่อ ทำให้สามารถเขียน Web Application ได้โดยตรง
import mysql.connector #pip install mysql.connector เชื่อม sql

#การสร้างหน้าเว็บเพจ
st.set_page_config(page_title="DataMaskType Dashboard",
                   page_icon=":bar_chart:",
                   layout="wide"
)

#-----------------------------เชื่อม sql ---------------------------
df = mysql.connector.connect(
    host="us-cdbr-east-05.cleardb.net",
    user="bee2562bca911c",
    password="41039f7c",
    database="heroku_c24e1a9450f3bbd"
    )
query = 'select * from datamask' #เลือกตารางที่ต้องการ
df = pd.read_sql(query, con = df) #ใช้ pandas ในการจัดการตาราง
print(df)

#-------------------------------ดึงข้อมูลหน้ากากประเภท KN95---------------------------------
n95=(df.query('masktype == "N95"'))
n95 = n95.sum()[["amount"]]
n95 = pd.array(n95)
n95 = n95[0]
# print(kn)

#-------------------------------ดึงข้อมูลหน้ากากประเภท Cloth---------------------------------
cloth = (df.query('masktype == "Cloth"'))
cloth = cloth.sum()[["amount"]]
cloth = pd.array(cloth)
cloth = cloth[0]

#-------------------------------ดึงข้อมูลหน้ากากประเภท Surgical---------------------------------
surgical = (df.query('masktype == "Surgical"'))
surgical = surgical.sum()[["amount"]]
surgical = pd.array(surgical)
surgical = surgical[0]

#-------------------------------ดึงข้อมูลหน้ากากประเภท NoMask---------------------------------
nomask = (df.query('masktype == "NoMask"'))
nomask = nomask.sum()[["amount"]]
nomask = pd.array(nomask)
nomask = nomask[0]

#-------------------------------ดึงข้อมูลหน้ากากประเภท Wearing---------------------------------
wearing = (df.query('masktype == "Wearing incorrectly"'))
wearing = wearing.sum()[["amount"]]
wearing = pd.array(wearing)
wearing = wearing[0]

#-------ตัวแปรจำนวนคนที่วสวมหน้ากาก----
select_mask = df.loc[df['masktype'].isin(["N95", "Cloth","Surgical"])]
select_mask = select_mask.sum()[["amount"]]
select_mask = pd.array(select_mask)
select_mask = select_mask[0]
# # print(select_mask)

#-------ตัวแปรจำนวนคนที่ไม่สวมหน้ากาก----
select_nomask = df.loc[df['masktype'].isin(["NoMask", "Wearing incorrectly"])]
select_nomask = select_nomask.sum()[["amount"]]
select_nomask = pd.array(select_nomask)
select_nomask = select_nomask[0]
# print(select_nomask)

#---------SIDEBAR-------------
st.sidebar.header ("Please Filter Here:")
Type=st.sidebar.multiselect(
    "เลือกประเภทหน้ากาก:",
    options=df["masktype"].unique(),
    default=df["masktype"].unique ()
)

Date=st.sidebar.multiselect(
    "เลือกวันที่:",
    options=df["date_d"].unique (),
    default=df["date_d"].unique ()
)

#------------ฟังก์ชั่น sidebar-------------
df_selection = df.query(
    "masktype ==@Type & date_d ==@Date"
)

#----------mainpage-------------
st.title(":bar_chart: DataMask Dashboard")

#----------------ส่วนหัวแสดงจำนวนของหน้ากากทุกชนิด---------------
st.markdown ("---")

c_top1, c_top2, c_top3, c_top4, c_top5 = st.columns(5)
with c_top1:
    # img=Image.open("surgical.png")
    # st.image(img,width=300,caption="Simple Image")
    new_title = (f'<h1 style="font-size:50px; padding:10px; text-align:center;">{n95:,}</h1>')
    st.info(f"จำนวนหน้ากาก N95")
    st.markdown(new_title, unsafe_allow_html=True)
    # st.subheader (f"={kn95:,}")
with c_top2:
    new_title = (f'<h1 style="font-size:50px; padding:10px; text-align:center;">{cloth:,}</h1>')
    st.info("จำนวนหน้ากาก Cloth")
    st.markdown(new_title, unsafe_allow_html=True)
    # st.subheader (f"= {cloth:,}")
with c_top3:
    new_title = (f'<h1 style="font-size:50px; padding:10px; text-align:center;">{surgical:,}</h1>')
    st.info ("จำนวนหน้ากาก Surgical")
    st.markdown(new_title, unsafe_allow_html=True)
    # st.info (f" {surgical:,}")
with c_top4:
    new_title = (f'<h1 style="color:#e8c100; font-size:50px; padding:10px; text-align:center;">{wearing:,}</h1>')
    st.warning ("จำนวนหน้ากาก Wearing")
    st.markdown(new_title, unsafe_allow_html=True)
    # st.subheader (f"= {wearing:,}")
with c_top5:
    new_title = (f'<h1 style="color:red; font-size:50px; padding:10px; text-align:center;">{nomask:,}</h1>')
    st.error ("จำนวนหน้ากาก NoMask")
    st.markdown(new_title, unsafe_allow_html=True)
    # st.subheader (f"= {nomask:,}")

#----------------ส่วนคำนวนจำนวนหน้ากากทั้งหมด------------------
total_amount = int (df_selection["amount"].sum())
# average_rating =round (df_selection["amount"].mean(), 1)
# star_rating = ":star:" * int(round(average_rating, 0))
# average_sale_by_transaction = round(df_selection["Total"].mean(), 2)

st.markdown ("---")
new_title = (f'<h2 style="color:green; background-color:#bce0d4; font-size:50px; padding:15px; text-align:center; border-radius:8px;">จำนวนหน้ากากทั้งหมด = {total_amount:,}</h2>')
st.markdown(new_title, unsafe_allow_html=True)
    # st.subheader("จำนวนหน้ากากทั้งหมด = "f"{total_amount:,}")

#----------------------กราฟแท่งแสดงจำนวนคนที่สวมหน้ากากและไม่สวมหน้ากาก------------------
data2 = pd.DataFrame({
"type" : ['คนที่สวมหน้ากาก','คนที่ไม่สวมหน้ากาก'],
"value" :  [select_mask,select_nomask]})
chart_data = px.bar(data2,
    x="type",
    y="value",
    title="<b>กราฟแท่งแสดงจำนวนคนที่สวมหน้ากาก/ไม่สวมหน้ากาก</b>",
    color="type",
    color_discrete_map={'คนที่สวมหน้ากาก':'blue','คนที่ไม่สวมหน้ากาก':'red',},
    template="plotly_white",
    )
chart_data.update_layout(
   plot_bgcolor="rgba (0,0,0,0)",
    xaxis=(dict(showgrid=False))
)
# st.plotly_chart(chart_data)#แสดงกราฟแท่งแสดงจำนวนคนที่สวมหน้ากาก

#-------------------กราฟแท่งแสดงประเภทหน้ากาก---------------
mask_type_bar=(
    df_selection.groupby(by=["masktype"]).sum()[["amount"]] #.sort_value(by="amount")เรียงจากมากไปหาน้อย
    )
fig_compare_mask = px.bar(
    mask_type_bar,
    x="amount",
    y=mask_type_bar.index,
    title="<b>กราฟแท่งแสดงประเภทหน้ากาก</b>",
    orientation="h",
    # color='mask_type_bar',
    color_discrete_map={'Cloth':'blue', 'N95':'red', 'NoMask':'red', 'Surgical':'red', 'Wearing incorrectly':'red',},
    # color_discrete_sequence=["SandyBrown","pink","blue","red","yellow"] * len(mask_type_bar),
    template="plotly_white",
)
fig_compare_mask.update_layout(
   plot_bgcolor="rgba (0,0,0,0)",
    xaxis=(dict(showgrid=False))
)
#st.plotly_chart(fig_compare_mask)#แสดงกราฟแท่งแนวนอน

#----------------------------PIE CHART-----------------
data3 = pd.DataFrame({
"type" : ['n95','cloth','surgical','nomask','wearing'],
"value" :  [n95,cloth,surgical,nomask,wearing]})
pie_chart = px.pie(data3,
                title='<b>กราฟวงกลมแสดงจำนวนหน้ากากทั้งหมด</b>',
                values='value',
                names='type',
                color="type",
                color_discrete_sequence=["SandyBrown","pink","blue","red","yellow"],)
# st.plotly_chart(pie_chart) #แสดง pie chart

#----------------------------line CHART-----------------
data_type_mask=df_selection.groupby(by=["date_d"]).sum()[["amount"]]
line_chart = px.line(data_type_mask,
                        title='<b>กราฟเส้นแสดงจำนวนหน้ากากทั้งหมดในแต่ละวัน</b>',
                        # color_discrete_sequence=["#0083B8"]
                        # template="plotly_white",
                        )
line_chart.update_layout(
   plot_bgcolor="rgba (0,0,0,0)",
    xaxis=(dict(showgrid=False))
)
# st.plotly_chart(line_chart) #แสดง line chart

#-----------------จัดตำแหน่งกราฟให้อยู่ซ้าย ขวา--------------
left_column, right_column = st.columns (2)
left_column.plotly_chart(chart_data, use_container_width=True)
right_column.plotly_chart(fig_compare_mask, use_container_width=True)
left_column_1, right_column_2 = st.columns (2)
left_column_1.plotly_chart(pie_chart, use_container_width=True)
right_column_2.plotly_chart(line_chart, use_container_width=True)

#----- HIDE STREAMLIT STYLE-------------------
hide_st_style ="""
            <style>
            #MainMenu {visibility: hidden;}
            footer (visibility: hidden;}
            header (visibility: hidden;}
            </style>
            """
st.markdown (hide_st_style, unsafe_allow_html=True)

st.dataframe(df_selection) #แสดงตารางข้อมูลทั้งหมด