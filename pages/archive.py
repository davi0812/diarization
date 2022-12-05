import dash
from dash import html, dcc
import mysql.connector

dash.register_page(__name__)

mydb = mysql.connector.connect(
    host="159.223.207.111",
    user="sql_dev_mavmedia",
    password="acDf7XtRxeibxyJw",
    database="sql_dev_mavmedia"
)
hijos = []
mycursor = mydb.cursor()
mycursor.execute("SELECT distinct(video) FROM transcript")
myresult = mycursor.fetchall()
for x in myresult:
    hijos.append(dcc.Link("Visit "+x[0], href="http://159.223.207.111/downloader/list.php?id="+x[0]))
    hijos.append(html.Br())

layout = html.Div(children=[
    html.Div(
        children=hijos
    ),
])

