from urllib.request import urlopen
import json
import plotly.express as px
import pandas as pd

with urlopen('https://raw.githubusercontent.com/johan/world.geo.json/master/countries.geo.json') as response:
    countries = json.load(response)

df = pd.read_pickle("/Users/maanas/Documents/twitter_proj/geo/res_geo.pkl")

fig = px.choropleth(df, geojson=countries, locations='country code', color='score',
                           color_continuous_scale="sunset",
                           range_color=(0, 1),
                           scope="world",
                           labels={'score':'sentiment score'},
                           projection="orthographic",
                           hover_data=["number of tweets","country name"]
                          )
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig.show()
