import figures
import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from flask_caching import Cache
from base64 import b64encode

pd.options.mode.chained_assignment = None

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
cache = Cache(app.server, config={
    'CACHE_TYPE': 'filesystem',
    'CACHE_DIR': 'cache'
})
server = app.server


TIMEOUT = 8460


@cache.memoize(timeout=TIMEOUT)
def create_figure_list():
    state_list = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DC", "DE", "FL", "GA",
                  "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD",
                  "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ",
                  "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC",
                  "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]
    figure_list = []
    for state in state_list:
        fig = figures.create_state_graph(df, state)
        img_bytes = fig.to_image(format="png")
        encoding = b64encode(img_bytes).decode()
        img_b64 = "data:image/png;base64," + encoding
        img = html.Img(src=img_b64, style={'width': '100%'})
        figure_list.append(img)
        # html.Div(dcc.Graph(figure=fig)))
    return figure_list


# @cache.memoize(timeout=TIMEOUT)
def create_rows(figure_list):
    div_list = []
    it = iter(figure_list)
    for x in it:
        try:
            row = html.Div(
                dbc.Row(
                    [dbc.Col(html.Div(x), width=12, lg=6),
                     dbc.Col(html.Div(next(it)), width=12, lg=6)]

                )
            )
        except StopIteration as e:
            row = html.Div(
                dbc.Row(
                    [dbc.Col(html.Div(x), width=12, lg=6)]

                )
            )

        div_list.append(row)
    return div_list


@cache.memoize(timeout=TIMEOUT)
def get_dataframe():
    df = pd.read_csv(
        'assets/usa.csv')
    return df


df = get_dataframe()
figure_list = create_figure_list()
div_list = create_rows(figure_list)


legend_html = html.Div(html.Dl([
    html.Dt(className='zero'),
    html.Dd('No policy'),
    html.Dt(className='one'),
    html.Dd('Recommended'),
    html.Dt(className='two'),
    html.Dd('Required in specific shared spaces'),
    html.Dt(className='three'),
    html.Dd('Required in all shared spaces'),
    html.Dt(className='four'),
    html.Dd('Required outside home at all times'),
    html.Dt(className='none'),
    html.Dd('No data'),
], className='legend'))

row = html.Div(dbc.Row(dbc.Col(legend_html)))

div_list = [row] + div_list

app.layout = html.Div([
    dbc.Container(div_list
                  )
])

if __name__ == '__main__':
    app.run_server(debug=True)
