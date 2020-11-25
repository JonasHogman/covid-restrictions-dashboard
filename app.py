import preprocess
import figures
import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

pd.options.mode.chained_assignment = None

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

df = preprocess.preprocess_data(
    pd.read_csv(
        'https://github.com/OxCGRT/USA-covid-policy/raw/master/data/OxCGRT_US_latest.csv',
        dtype={'E4_Notes': str}))


state_list = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DC", "DE", "FL", "GA",
              "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD",
              "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ",
              "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC",
              "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]

figure_list = []
for state in state_list:
    fig = figures.create_state_graph(df, state)
    figure_list.append(
        html.Div(dcc.Graph(id=state, figure=fig)))


def create_rows(figure_list):
    div_list = []
    it = iter(figure_list)
    for x in it:
        try:
            row = html.Div(
                dbc.Row(
                    [dbc.Col(html.Div(x), width=6),
                     dbc.Col(html.Div(next(it)), width=6)]

                )
            )
        except StopIteration as e:
            row = html.Div(
                dbc.Row(
                    [dbc.Col(html.Div(x), width=6)]

                )
            )

        div_list.append(row)
    return div_list


# print(create_rows(figure_list)[0])
div_list = create_rows(figure_list)

app.layout = dbc.Container(children=div_list,
                           # fluid=True,
                           # style={'width': '85%'}
                           )

if __name__ == '__main__':
    app.run_server(debug=True)
