
import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.graph_objs as go

# Dados estáticos tratados
data = {
    "Conta Contábil": ["Receita Líquida", "Impostos Incidetes sobre Recita", "Despesas com Pessoal",
                       "Despesas com Utilidades e Serviços", "Despesas Tributárias"],
    "Jan": [10000, -3000, None, -8667, -2000],
    "Fev": [11000, -5000, -7000, None, -833],
    "Mar": [12000, -5000, -7000, -8667, -833],
    "Abr": [13000, -5000, None, None, -833],
    "Mai": [14000, -5000, None, None, -833],
    "Jun": [15000, -8000, -7000, None, None],
    "Jul": [16000, -9000, -7000, -8667, -833],
    "Ago2": [17000, -8000, None, -8667, None],
    "Set": [18000, -2000, None, -8667, -833],
    "out": [19000, -3000, None, -8667, -833],
    "Nov": [20000, -3000, -7000, None, -833],
    "Dez": [21000, -3000, -7000, -8667, None],
}

df = pd.DataFrame(data)
df_plot = df.set_index("Conta Contábil").transpose()

# Totais para cards
soma = df_plot.sum()
resultado_geral = soma.sum()
total_receitas = soma[soma > 0].sum()
total_despesas = soma[soma < 0].sum()

# App
app = dash.Dash(__name__)

app.layout = html.Div(style={"backgroundColor": "white", "padding": "20px"}, children=[
    html.Div(style={"display": "flex", "gap": "20px", "marginBottom": "30px"}, children=[
        html.Div([
            html.H4("Resultado Geral"),
            html.H2(f"R$ {resultado_geral:,.2f}")
        ], style={"boxShadow": "0 4px 6px rgba(0,0,0,0.1)", "padding": "20px", "background": "white", "borderRadius": "12px"}),

        html.Div([
            html.H4("Total das Receitas"),
            html.H2(f"R$ {total_receitas:,.2f}")
        ], style={"boxShadow": "0 4px 6px rgba(0,0,0,0.1)", "padding": "20px", "background": "white", "borderRadius": "12px"}),

        html.Div([
            html.H4("Total das Despesas"),
            html.H2(f"R$ {total_despesas:,.2f}")
        ], style={"boxShadow": "0 4px 6px rgba(0,0,0,0.1)", "padding": "20px", "background": "white", "borderRadius": "12px"}),
    ]),

    html.Div([
        dcc.Dropdown(
            id='conta-dropdown',
            options=[{'label': c, 'value': c} for c in df_plot.columns],
            value=list(df_plot.columns),
            multi=True,
            placeholder="Selecione contas contábeis...",
            style={"marginBottom": "20px"}
        ),
        dcc.Graph(id='line-chart')
    ])
])

@app.callback(
    Output('line-chart', 'figure'),
    Input('conta-dropdown', 'value')
)
def update_graph(selected_contas):
    fig = go.Figure()
    for conta in selected_contas:
        fig.add_trace(go.Scatter(
            x=df_plot.index,
            y=df_plot[conta],
            mode='lines+markers',
            name=conta,
            line=dict(width=0.2)
        ))
    fig.update_layout(
        title="Evolução Mensal das Contas Contábeis",
        plot_bgcolor="white",
        paper_bgcolor="white",
        xaxis_title="Mês",
        yaxis_title="Valor (R$)",
        legend_title="Conta Contábil"
    )
    return fig

if __name__ == "__main__":
    app.run_server(debug=False)
