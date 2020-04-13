from datetime import datetime
import pandas as pd

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objects as go

df = pd.read_csv('data/testdata.csv', index_col=0)

app = dash.Dash(__name__)

app.layout = html.Div([

    html.Nav(
        html.Ul([
            html.Li('Intelligent Process Control', className="main-logo"),
            html.Li('Dashboards'),
            html.Li('Input sheets'),
            html.Li('Help')
        ])
    ),

    html.Div(
        html.Aside(
            html.Ul([
                html.Li('OVERVIEW', className="overview"),
                html.Li('Process One'),
                html.Li('Process Two'),
                html.Li('Process Three'),
                html.Li('Process Four')
            ])
        )
    ),

    html.Div([

        html.Div([
                dcc.Dropdown(
                    id='parameter-picker',
                    options=[
                        {'label': 'Temperature', 'value': 'temperature'},
                        {'label': 'Pressure 1', 'value': 'pressure_1'},
                        {'label': 'Pressure 2', 'value': 'pressure_2'},
                        {'label': 'Measurement A', 'value': 'measurement_A'}
                    ],
                    className="dropdown",
                    placeholder="select trace"
                ),
                dcc.Checklist(
                    id='machine',
                    options=[
                        {'label': 'Machine A', 'value': 'A'},
                        {'label': 'Machine B', 'value': 'B'},
                        {'label': 'Machine C', 'value': 'C'},
                    ],
                    labelStyle={'padding': '20px'},
                    style={'margin-left': '40px'},
                    className="machine-options"
                ),
                dcc.DatePickerRange(
                    id='date-picker',
                    initial_visible_month=datetime.now(),
                    end_date=datetime.now(),
                    display_format='DD-MMM-YYYY',
                    className="date-picker"
                )
            ], className="chart-options"),

        html.Div(
            id="main-plot",
            # className="main-chart"
        ),

        # html.Div(
        #     id="main-hist"
        # )
    ], className="main-area")
])


@app.callback(
    Output('main-plot', 'children'),
    [Input('parameter-picker', 'value'),
     Input('machine', 'value'),
     Input('date-picker', 'start_date'),
     Input('date-picker', 'end_date')]
)
def plot_run_chart(trace, machines, start_date, end_date):
    if trace and machines:
        df = pd.read_csv('data/testDataWithDateIndex.csv', index_col=0)
        if start_date:
            df = df[start_date:]
        if end_date:
            df = df[: end_date]

        plot_data = []
        hist_data = []
        opac = 1 if len(machines) == 1 else 0.6
        for machine in machines:
            df_machine = df.loc[df.machine == machine, :]
            plot_data.append(dict(
                x=df_machine.index,
                y=df_machine.loc[:, trace],
                type='scatter',
                mode='lines+markers',
                name=machine
            ))
            hist_data.append(dict(
                y=df_machine.loc[:, trace],
                type='histogram',
                name=machine,
                opacity=opac,
                nbins=20
            ))

        return html.Div(
            className="main-chart",
            children=[
                dcc.Graph(
                    figure={
                        'data': plot_data,
                        'layout': dict(title=f'{trace} for machines {machines}')
                    },
                    className="run-chart"
                ),

                dcc.Graph(
                    figure={
                        'data': hist_data,
                        'layout': dict(barmode='overlay')
                    },
                    className="main-hist"
                )
            ]
        )


if __name__ == '__main__':
    app.run_server(debug=True)
