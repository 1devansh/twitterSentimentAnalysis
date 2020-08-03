import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
import Untitled



topics = Untitled.topics

app = dash.Dash()

app.layout = html.Div([
    html.H2("Sentiment Analysis"),
    html.Div(
        [
            dcc.Dropdown(
                id="Topics",
                options=[{
                    'label': i,
                    'value': i
                } for i in topics],
                value='All Topics'),
        ],
        style={'width': '25%',
               'display': 'inline-block'}),
    dcc.Graph(id='funnel-graph'),
])


@app.callback(
    dash.dependencies.Output('funnel-graph', 'figure'),
    [dash.dependencies.Input('Topics', 'value')])
def update_graph(Topics):
    if Topics in topics:
        df_plot = Untitled.databases[Topics]
    else:
        df_plot = Untitled.databases['coronavirus_covid']
    pv = pd.pivot_table(
        df_plot,
        index=['country'],
        )

    trace1 = go.Bar(x=pv.index, y=pv['positive'], name='Positive')
    trace2 = go.Bar(x=pv.index, y=pv['neutral'], name='Neutral')
    trace3 = go.Bar(x=pv.index, y=pv['negative'], name='Negative')


    return {
        'data': [trace1, trace2, trace3],
        'layout':
        go.Layout(
            title='Sentiments for {}'.format(Topics),
            barmode='stack')
    }


if __name__ == '__main__':
    app.run_server(debug=True)