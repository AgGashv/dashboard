import plotly.express as px
import dash_bootstrap_components as dbc
from pages import graph_page
from data import df
from dash import Dash, html, dcc, Output, Input, callback

main_page_style = [dbc.themes.MATERIA]

app = Dash(__name__, external_stylesheets=main_page_style, use_pages=True)
app.config.suppress_callback_exceptions = True

SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": 'rgb(25, 191, 230)',
}

sidebar = html.Div(
    [
        html.H2("Меню", className="display-6"),
        html.Hr(),
        html.P(
            "Информация о количестве населения Земли (1960-2022)", className="lead"
        ),
        dbc.Nav(
            [
                dbc.NavLink("Гистограмма", href="/", active="exact", style={'color': 'black'}),
                dbc.NavLink("График", href="/graph", active="exact", style={'color': 'black'})
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

layout = html.Div(
    children=[
        html.Div(
            style={
                'padding': '0 0 0 10px'
            },
            children=[
                html.H4(children="Узнать количество населения:",
                        style={'margin-bottom': '5px'}),

                html.Div([
                    html.Label(["Год",
                                dcc.Dropdown(df.columns[1:], value='1960', id='years_print',
                                             style={'width': '100px'})],
                               style={'padding': '0 10px 0 0', 'margin-left': '20px'})
                ], style={'display': 'inline-block'}),

                html.Div([
                    html.Label("Часть света"),
                    dcc.Dropdown(df['Country Name'], value=df['Country Name'].values[0], id='countries',
                                 style={'width': '400px',
                                        'display': 'table'}),

                ], style={'display': 'inline-block'}),

                html.Div(id='population', style={'display': 'block', 'padding': '10px 0 0 20px',
                                                 'font-size': '20px'}),
            ]),

        html.Div(
            style={'margin-left': '10px'},
            children=[
                html.H4(children="Настройки гистограммы:", style={'margin-bottom': '5px'}),

                html.Div([html.Label("Год"),
                          dcc.Dropdown(df.columns[1:], id='years_hist', style={'width': '100px',
                                                                                             'display': 'table'})],
                         style={"display": 'inline-block', 'margin-left': '20px'}),

                html.Div([
                    html.Label("Части света",
                               style={'display': 'block', 'padding': '0 0 0 10px'}),
                    dcc.Dropdown(df['Country Name'], id='countries_selector',
                                 style={'width': '400px', 'display': 'table',
                                        'padding': '0 0 0 10px'},
                                 multi=True),
                ],
                    style={"display": 'inline-block'}),

                html.Div([
                    dcc.Graph(figure=px.histogram(y=[0], x=[0]).update_layout(
                        yaxis_title_text='Части света',
                        xaxis_title_text=f'Население в 1960 году'
                    ), id='hist')
                ]),
            ])
    ])

content = html.Div(id='content')

app.layout = html.Div([dcc.Location(id="url"), sidebar, content], style={'margin-left': '250px'})


@callback(
    Output(component_id='content', component_property='children'),
    Input(component_id='url', component_property='pathname')
)
def change_page(pathname):
    if pathname == '/':
        return layout
    elif pathname == '/graph':
        return graph_page.layout

    return html.Div(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"Страница {pathname} не найдена"),
        ],
        className="p-3 bg-light rounded-3",
    )


@callback(
    Output(component_id='population', component_property='children'),

    [Input(component_id='years_print', component_property='value'),
     Input(component_id='countries', component_property='value')]
)
def print_country(input_years, input_country):
    pop_count = 0
    if input_years is not None and input_country is not None:
        pop_count = df.loc[df['Country Name'] == input_country, input_years].values[0]

    return f'Население: {int(pop_count):,d} чел.'.replace(',', ' ')


@callback(
    Output(component_id='hist', component_property='figure'),

    [Input(component_id='years_hist', component_property='value'),
     Input(component_id='countries_selector', component_property='value')]
)
def print_hist(input_years, input_country):
    figure = px.histogram(y=[0], x=[0])

    if input_years is not None and input_country is not None:
        index_arr = []
        if input_country is not None:
            for elem in input_country:
                index_arr.append(df.loc[df['Country Name'] == elem].index[0])

            figure = px.histogram(df.iloc[index_arr], y='Country Name', x=input_years, color='Country Name')

    figure.update_layout(
        yaxis_title_text='Части света',
        xaxis_title_text=f'Население в {input_years} году'
    )

    return figure


if __name__ == '__main__':
    app.run(debug=True)
