from plotly.subplots import make_subplots
import plotly.graph_objects as go
import pandas as pd


def get_intervals(df_state, columns):
    gantt_list = []

    for column in columns:
        df_state[column] = df_state[column].astype(str)
        df_state[column].fillna(0, inplace=True)

        start_date = "2020-01-01"
        last_level = '0.0'
        for index, row in df_state.iterrows():
            if row[column] != last_level:
                gantt_list.append(
                    dict(Name=column, Start=start_date, Finish=row['Date'], Intensity=last_level))
                last_level = row[column]
                start_date = row["Date"]
        gantt_list.append(dict(Name=column, Start=start_date,
                               Finish=pd.to_datetime('today'), Intensity=last_level))

    return pd.DataFrame(gantt_list)


def create_state_graph(df, state):
    df_state = df[df['RegionCode'].isin([state])]

    # gantt_list = get_intervals(state, ['C1_School closing', 'C2_Workplace closing', 'C3_Cancel public events', 'C4_Restrictions on gatherings', 'C5_Close public transport', 'C6_Stay at home requirements', 'C7_Restrictions on internal movement', 'C8_International travel controls', 'H6_Facial Coverings'])
    df_gantt = get_intervals(df_state, ['H6_Facial Coverings'])

    df_gantt['Interval'] = (pd.to_datetime(df_gantt['Finish']) -
                            pd.to_datetime(df_gantt['Start'])).astype("timedelta64[ms]")

    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.01,
                        row_heights=[0.9, 0.1])

    fig.append_trace(go.Scatter(x=df_state['Date'], y=df_state['ConfirmedCases'],
                                name='Confirmed Cases', showlegend=False), row=1, col=1)

    colors = {'0.0': "#FFFFFF",
              '1.0': "#FFC300",
              '2.0': "#FF5733",
              '3.0': "#C70039",
              '4.0': '#900C3F',
              'nan': '#909090'}

    legend = {'0.0': "No policy",
              '1.0': "Recommended",
              '2.0': "Required in specific shared spaces",
              '3.0': "Required in all shared spaces",
              '4.0': 'Required outside home at all times',
              'nan': 'No data'
              }

    # add each timeline bar individually
    for index, row in df_gantt.iterrows():
        fig.append_trace(go.Bar(
            y=[''],
            x=[row['Interval']],
            base=row['Start'],
            width=[0.5],
            marker_color=colors[row['Intensity']],
            name=legend[row['Intensity']],
            orientation='h',
        ), row=2, col=1)

    # layout changes
    fig.update_layout(barmode='overlay', template='simple_white',
                      autosize=True,
                      title_text=f"Confirmed cases and mask policy in <b>{df_state['RegionName'].iloc[0]}</b>",
                      legend=dict(
                          traceorder='normal',
                          bordercolor='black',
                          x=0,
                          y=1,
                      ))

    # update x-axes to avoid empty space at start and end of graph
    fig.update_xaxes(range=[pd.to_datetime("2020-01-22"),
                            pd.to_datetime('today')], type='date')
    return fig
