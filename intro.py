import pandas as pd
import plotly.express as px  # (version 4.7.0 or higher)
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
from dash import Dash, dcc, html, Input, Output  # pip install dash (version 2.0.0 or higher)





app = Dash(__name__)

# -- Import and clean data (importing csv into pandas)
# df = pd.read_csv("intro_bees.csv")
df = pd.read_csv("intro_bees.csv")

df = df.groupby(['State', 'ANSI', 'Affected by', 'Year', 'state_code'])[['Pct of Colonies Impacted']].mean()
df.reset_index(inplace=True)
print(df[:5])

# ------------------------------------------------------------------------------
# App layout

body = dbc.Container([
        html.Br(),
        dbc.Row(
                [
                dbc.Col(

                    html.Div(
                        [   html.Br([]),
                            html.H5("Bienvenue!",style={'color':'red','backgroundColor':'white'}),
                            html.Br([]),
                            html.P(
                                "\
                           Ce projet se concentre sur la visualisation de l'impact de divers facteurs (maladies, pesticides, etc) sur les colonies d'abeilles   aux États-Unis à travers un tableau de bord Web dynamique et interactif. \En utilisant Dash, Plotly et Pandas, l'application présente les données recueillies par le département américain de l'agriculture, permettant aux utilisateurs d'explorer les pourcentages de colonies d'abeilles affectées par les maladies ou les pesticides au fil des ans.\
Grâce à une interface intuitive et des graphiques interactifs, les utilisateurs peuvent sélectionner une année spécifique et obtenir des visualisations géographiques montrant les colonies touchées dans chaque État. \ Ce projet démontre mes compétences en analyse de données, en développement d'applications web, et en visualisation de données interactives avec des outils modernes comme Dash et Plotly.",

                                style={"color": "#000406"},

                            ),
                            html.P(
                                "\
                            Ces données seront par la suite transformées pour interagir dynamiquement avec des graphiques. \
                            On y affiche des informations telles que: .",


                                style={"color": "#000406"},

                            ),
                
                        ]

                         )

                ,style={'color':'red','backgroundColor':'white'})
                    ], justify="center", align="center"
                    ),
     html.Br(),
],style={"height": "100vh"}
)
app.layout = html.Div([

    html.H1("Web Application Dashboards with Dash", style={'text-align': 'center'}),
    html.Div([body],style={'background-image': 'url("Datamining\ bg.jpg")'}),

    dcc.Dropdown(id="slct_year",
                 options=[
                     {"label": "2015", "value": 2015},
                     {"label": "2016", "value": 2016},
                     {"label": "2017", "value": 2017},
                     {"label": "2018", "value": 2018}],
                 multi=False,
                 value=2015,
                 style={'width': "40%"}
                 ),

    html.Div(id='output_container', children=[]),
    
    html.Br(),

    dcc.Graph(id='my_bee_map', figure={})

])



# ------------------------------------------------------------------------------
# Connect the Plotly graphs with Dash Components
@app.callback(
    [Output(component_id='output_container', component_property='children'),
     Output(component_id='my_bee_map', component_property='figure')],
    [Input(component_id='slct_year', component_property='value')]
)
def update_graph(option_slctd):
    print(option_slctd)
    print(type(option_slctd))

    container = "The year chosen by user was: {}".format(option_slctd)

    dff = df.copy()
    dff = dff[dff["Year"] == option_slctd]
    dff = dff[dff["Affected by"] == "Varroa_mites"]

    # Plotly Express
    fig = px.choropleth(
        data_frame=dff,
        locationmode='USA-states',
        locations='state_code',
        scope="usa",
        color='Pct of Colonies Impacted',
        hover_data=['State', 'Pct of Colonies Impacted'],
        color_continuous_scale=px.colors.sequential.YlOrRd,
        labels={'Pct of Colonies Impacted': '% of Bee Colonies'},
        template='plotly_dark'
    )

    # Plotly Graph Objects (GO)
    # fig = go.Figure(
    #     data=[go.Choropleth(
    #         locationmode='USA-states',
    #         locations=dff['state_code'],
    #         z=dff["Pct of Colonies Impacted"].astype(float),
    #         colorscale='Reds',
    #     )]
    # )
    #
    # fig.update_layout(
    #     title_text="Bees Affected by Mites in the USA",
    #     title_xanchor="center",
    #     title_font=dict(size=24),
    #     title_x=0.5,
    #     geo=dict(scope='usa'),
    # )

    return container, fig


# ------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True)