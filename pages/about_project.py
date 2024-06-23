from dash import html, dcc

link = "https://github.com/AgGashv/dashboard"

layout = html.Div([
    html.H1(
        "Добро пожаловать на сайт \"Информация о количестве населения Земли (1960-2022)\"!",
        style={'margin-bottom': '30px'}
    ),
    html.Div(
        """Здесь вы найдете интерактивные дашборды, которые визуализируют данные о количестве населения в мире с 1960
        по 2022 годы. Используйте дашборды, чтобы лучше понять динамику изменения населения на планете,
        выявить тенденции и сделать выводы о возможных сценариях развития событий в будущем. Надеюсь сайт будет
        интересен и полезен для Вас!\n"""
    ),
    html.Div(["Ссылка на GitHub: ", dcc.Markdown(f"[{link}]({link})", style={'display': 'inline-block'})],
             style={'margin-top': '40%'}),

],
    style={"margin-left": "10px"})


