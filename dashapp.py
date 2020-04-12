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
def plot_run_chart(trace, machines):
    if trace and machines:
        df = pd.read_csv('data/testdata.csv', index_col=0)
        data = []
        for machine in machines:
            df_machine = df.loc[df.machine == machine, :].reset_index(drop=True)
            data.append(dict(
                x=df_machine.loc[:, trace].index,
                y=df_machine.loc[:, trace],
                type='scatter',
                mode='lines+markers',
                name=machine
            ))

        return dcc.Graph(
            figure={
                'data': data,
                'layout': dict(title=f'{trace}  -  machine {machines}')
            },
            className="run-chart"
        )


app.css.append_css({"external_url": "/assets/{}".format(stylesheet)})

if __name__ == '__main__':
    app.run_server(debug=True)
