from datetime import datetime
import pandas as pd

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

df = pd.read_csv('data/testdata.csv', index_col=0)

stylesheet = 'style.assets'
app = dash.Dash(__name__, )

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
                dcc.RadioItems(
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
                    className="date-picker"
                )
            ], className="chart-options"),

        html.Div(
            id="main-plot",
            # className="run-chart"
        ),
    ], className="main-area")
])


@app.callback(
    Output('main-plot', 'children'),
    [Input('parameter-picker', 'value'),
     Input('machine', 'value')]
)
def plot_run_chart(trace, machine):
    if trace and machine:
        df = pd.read_csv('data/testdata.csv', index_col=0)
        df = df.loc[df.machine == machine].reset_index(drop=True)

        return dcc.Graph(
            figure={
                'data': [dict(x=df.index, y=df[trace], type='scatter', mode='lines+markers')],
                'layout': dict(title=f'{trace}  -  machine {machine}')
            },
            className="run-chart"
        )


app.css.append_css({"external_url": "/assets/{}".format(stylesheet)})

if __name__ == '__main__':
    app.run_server(debug=True)
