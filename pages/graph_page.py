import plotly.express as px
from data import df
from dash import html, dcc, callback, Output, Input

figure = px.line(x=[0], y=[0]).update_layout(
    xaxis_title="Годы",
    yaxis_title="Количество населения"
)

layout = html.Div([
    html.H4(children="Настройки графика:", style={'margin-left': '10px'}),
    html.Div([
        html.Label("Часть света", style={'display': 'block'}),
        dcc.Dropdown(df['Country Name'], id='country_selector',
                     style={'width': '400px', 'display': 'table'}, value='Aruba'),
    ],
        style={'margin-left': '30px'}),
    html.Div(
        dcc.Graph(figure=figure, id='line', style={'margin-left': '10px'})
    )
]
)


@callback(
    Output(component_id='line', component_property='figure'),
    Input(component_id='country_selector', component_property='value')
)
def show_line_figure(country_name):
    if country_name is not None:
        df_country = df[df['Country Name'] == country_name]

        figure_new = px.line(x=df_country.columns[1:].tolist(), y=df_country.values.tolist()[0][1:]).update_layout(
            xaxis_title="Годы",
            yaxis_title="Количество населения"
        )

        figure_new.update_traces(mode='lines+markers')
        figure_new.update_xaxes(showgrid=False)
        return figure_new
    else:
        return figure
