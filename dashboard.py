import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
dash
from pymongo import MongoClient

## Get the access to our database in mongodb server :
client = MongoClient()
db = client['Covid19'] ## we choosed Covid19 as we nameed it there
table = db.summary ## store the collection summary in varable caled table

#################@@ START :FirstQuery @@####################
## First query to get the Total deaths in countries that have > 100 in Total:
getDeGt100 = { "TotalDeaths": { "$gt": 100 } }
query = table.find(getDeGt100)

## Create a lists to store the results
countriesdeathsGt100 = []
TotalDeathGt100 = []
## add results to lists using for loop on the query output:
for i in query:
    countriesdeathsGt100.append(i['Country'])
    TotalDeathGt100.append(i['TotalDeaths'])
#################@@ END : FirstQuery @@####################

#################@@ Start : SecondQuery @@####################
query2 = table.find({})
newConfirmed = dict()
for j in query2:
    newConfirmed[j['Country']] = j['NewConfirmed']
sortedNewConf = {k: v for k, v in sorted(newConfirmed.items(), key=lambda item: item[1],reverse=True)}
confirmedX = list(sortedNewConf.keys())
confirmedY = list(sortedNewConf.values())
#################@@ End : SecondQuery @@####################
def update_country_code():
    for i in df['Country']:
        for j in dfp['country']:
            if (j == i):
                new = dfp.loc[dfp['country'] == str(j), 'iso_alpha']
                if (new.index < 100):
                    df.loc[df['Country'] == str(i), 'CountryCode'] = str(new)[6:9]
                elif (new.index < 1000):
                    df.loc[df['Country'] == str(i), 'CountryCode'] = str(new)[7:10]
                else:
                    df.loc[df['Country'] == str(i), 'CountryCode'] = str(new)[8:11]

#### prepare Map to visualize ######
dfp = px.data.gapminder().query("year==2007")
df = pd.read_json("summ.json")
update_country_code()
df.loc[df['Country'] == 'United States of America', 'CountryCode'] = 'USA' ## Change US Iso code to USA
fig = px.choropleth(df, locations="CountryCode",
                    color="TotalConfirmed", # lifeExp is a column of gapminder
                    hover_name="Country", # column to add to hover information
                    color_continuous_scale=px.colors.sequential.Plasma)

############################Dashboard
app = dash.Dash()
colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}
app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    html.H1(
        children='Covid-19 Dashboard',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),
    html.Div(children='CoVid19 Daily Data', style={
        'textAlign': 'center',
        'color': colors['text']
    }),
    dcc.Graph(
        id='Graph1',
        figure={
            'data': [
                {'x': countriesdeathsGt100, 'y': TotalDeathGt100, 'type': 'bar', 'name': 'Countries'},
            ],
            'layout': {
                'title' : 'Total Deathes > 100',
                'plot_bgcolor': colors['background'],
                'paper_bgcolor': colors['background'],
                'font': {
                    'color': colors['text']
                }
            }
        }

    ),
    dcc.Graph(
        id='Graph2',
        figure={
            'data': [
                {'x': confirmedX, 'y': confirmedY, 'type': 'bar', 'name': 'Countries'},
            ],
            'layout': {
                'title' : 'Total Confirmed',
                'plot_bgcolor': colors['background'],
                'paper_bgcolor': colors['background'],
                'font': {
                    'color': colors['text']
                }
            }
        }

    ),
    dcc.Graph(
        id="Graph3",
        figure = fig,
    ),

])




if __name__ == '__main__':
    app.run_server(debug=True)



