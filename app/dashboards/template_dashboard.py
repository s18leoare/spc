from dash import Dash
import dash_core_components as dcc
import dash_html_components as html
from utils import get_html_string
from datetime import datetime
from dash.dependencies import Input, Output
import pandas as pd


def add_dash(server):
    dashapp = Dash(server=server, routes_pathname_prefix='/template-dashboard/')
    dashapp.index_string = get_html_string('app/templates/base.html')

    dashapp.layout = html.Div(className='outer-container', children=[

        html.Div(className='main-chart-options', children=[
            dcc.Dropdown(
                className='main-chart-dropdown',
                id='parameter-picker',
                placeholder='select trace',
                options=[
                    {'label': 'Temperature', 'value': 'temperature'},
                    {'label': 'Pressure 1', 'value': 'pressure_1'},
                    {'label': 'Pressure 2', 'value': 'pressure_2'},
                    {'label': 'Measurement A', 'value': 'measurement_A'}
                ],
            ),
            dcc.Checklist(
                className='machine-options',
                id='machine',
                options=[
                    {'label': 'Machine A', 'value': 'A'},
                    {'label': 'Machine B', 'value': 'B'},
                    {'label': 'Machine C', 'value': 'C'},
                ]
            ),
            dcc.DatePickerRange(
                className='date-picker',
                id='date-picker',
                initial_visible_month=datetime.now(),
                end_date=datetime.now(),
                display_format='DD-MMM-YYYY'
            )
        ]),

        html.Div(
            id='main-plot',
            className='main-plot'
        )
    ])


    init_callbacks(dashapp)

def init_callbacks(dashapp):
    @dashapp.callback(
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



    # dashapp = Dash(server=server, routes_pathname_prefix='/template-dashboard/')
    #
    # dashapp.layout = html.Div([
    #     dcc.Dropdown(
    #         id='dropdown',
    #         options=[
    #             {'label': 'option 1', 'value': 'option 1'},
    #             {'label': 'option 2', 'value': 'option 2'}
    #             ]
    #         ),
    #     html.Div(id='display')
    # ])
    #
    # @dashapp.callback(
    #     Output('display', 'children'),
    #     [Input('dropdown', 'value')])
    # def display(value):
    #     return f'{value}'

    return dashapp.server
