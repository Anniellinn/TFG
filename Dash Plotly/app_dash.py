# -*- coding: utf-8 -*-
"""
Created on Sun Apr  9 17:43:31 2023

@author: annal
"""


from dash import Dash, dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import base64
from dash import html
import dash_html_components as html
import plotly.express as px
import datetime as dt
import dash_bootstrap_components as dbc
##import DatePicker, MonthPicker from '@semcore/ui/date-picker'

#external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

dbc_css = "C:/Users/annal/OneDrive/Escriptori/TFG/dash/base2.ccs"
style = "C:/Users/annal/OneDrive/Escriptori/TFG/dash/style2.ccs"
app = Dash(__name__)

app.css.append_css({
    "external_url": "https://codepen.io/Markshall/pen/PoZJRve.css"
})


drop_options = [
    {'label': 'SO2 (µg/m³)', 'value': 'SO2'},
    {'label': 'CO (mg/m³)', 'value': 'CO'},
    {'label': 'Ozó (µg/m³)', 'value': 'O3'},
    {'label': 'NO (µg/m³)', 'value': 'NO'},
    {'label': 'NO2 (µg/m³)', 'value': 'NO2'},
    {'label': 'NOx (µg/m³)', 'value': 'NOx'},
    {'label': 'PM10 (µg/m³)', 'value': 'PM10'},
    {'label': 'PM2.5 (µg/m³)', 'value': 'PM25'}]

month_drop_options = [
    {'label': 'Gener', 'value': '1'},
    {'label': 'Febrer', 'value': '2'},
    {'label': 'Març', 'value': '3'},
    {'label': 'Abril', 'value': '4'},
    {'label': 'Maig', 'value': '5'},
    {'label': 'Junio', 'value': '6'},
    {'label': 'Julio', 'value': '7'},
    {'label': 'Agosto', 'value': '8'},
    {'label': 'Setembre', 'value': '9'},
    {'label': 'Octubre ', 'value': '10'},
    {'label': 'Novembre', 'value': '11'},
    {'label': 'Decembre', 'value': '12'}]


radio_options = [
    {'label': 'Variància', 'value': 'Variància'},
    {'label': 'Mitjana Artimètica', 'value': 'Mitjana Artimètica'},
    {'label': '% Faltants', 'value': '% Faltants'}]

app.title = "Qualitat de l'aire a la ciutat de València"
server = app.server


# Plotly mapbox public token
mapbox_access_token = "pk.eyJ1IjoicGxvdGx5bWFwYm94IiwiYSI6ImNrOWJqb2F4djBnMjEzbG50amg0dnJieG4ifQ.Zme1-Uzoi75IaFbieBDl3A"

# Diccionari amb les estacions de València

list_of_locations = {
    "Vivers": {"lat": 39.479653889163416, "lon": -0.3697121931960339},
    "Avinguda França": {"lat": 39.45754550951267, "lon": -0.34279057101811966},
    "Bulevard Sud": {"lat": 39.4504492319186, "lon": -0.39630566751679575},
    "Centre": {"lat": 39.47057375657113, "lon": -0.37641920323962136},
    "Molí del Sol": {"lat": 39.48215563893474, "lon": -0.4086328955568287},
    "Nazaret Meteo ": {"lat": 39.44850984378533, "lon": -0.33329781812147613},
    "Pista de Silla": {"lat": 39.45809701143551, "lon": -0.3766448858649288},
    "Politècnic": {"lat": 39.479447, "lon": -0.336622}

}

# estacions que no he trobat les coordenades:

# "Port Antic Llit Turia": {"lat": 40.7589, "lon": -73.9851},
# "Port Moll Trans Ponent": {"lat": 40.7589, "lon": -73.9851},
# "Conselleria Meteo": {"lat": 40.8075, "lon": -73.9626},
# "Olivereta": {"lat": 40.7489, "lon": -73.9680}

# Initialize data frame
desviacio = pd.read_csv(
    "C:/Users/annal/OneDrive/Escriptori/TFG/Exploración/Faltants data/desviacio_faltants.csv",

)

mitjana = pd.read_csv(
    "C:/Users/annal/OneDrive/Escriptori/TFG/Exploración/Faltants data/mitjana_faltants.csv",

)
proporcio = pd.read_csv(
    "C:/Users/annal/OneDrive/Escriptori/TFG/Exploración/Faltants data/proporcio_faltants.csv",

)

variancia = pd.read_csv(
    "C:/Users/annal/OneDrive/Escriptori/TFG/Exploración/Faltants data/variancia_faltants.csv",
)

## imagenes usadas 
logo = 'C:/Users/annal/OneDrive/Escriptori/TFG/dash/logo_gris.png'
periode = 'C:/Users/annal/OneDrive/Escriptori/TFG/dash/select_periodde.png'
contaminant = 'C:/Users/annal/OneDrive/Escriptori/TFG/dash/select_cont.png'

test_base64 = base64.b64encode(open(logo, 'rb').read()).decode('ascii')
test_base64_periode = base64.b64encode(open(periode, 'rb').read()).decode('ascii')
test_base64_contaminant = base64.b64encode(open(contaminant, 'rb').read()).decode('ascii')


app.layout = html.Div(
    children=[
        html.Div(
            className="row",
            children=[
                # Column for user controls
                html.Div(
                    className="three columns div-user-controls",
                    children=[
                        html.A(
                            html.Img(
                                className="logo",
                                src='data:image/png;base64,{}'.format(test_base64),height=50
                            ),
                           # href="https://plotly.com/dash/",
                        ),
                        #html.H5("A les diverses estacions de medició"),
                        html.P(
                            """Selecciona un contaminant en un període temporal concret."""
                            ),
                        html.Div(
                            className="div-for-dropdown",
                            children=[
                                dcc.DatePickerSingle(
                                    id='my-date-picker-single',
                                    date=dt.datetime(2022, 10, 1),
                                    display_format='MMMM Y',
                                    month_format='MMMM Y',
                                    
                                    max_date_allowed=dt.datetime(2022, 12, 31),
                                    min_date_allowed=dt.datetime(2018, 1, 1),
                                    persistence=True,
                                    persistence_type='session',
                                    className='date-picker'
                                   #style={'border-radius': '5px', 'background-color': 
                                    #  'white', 'opacity':'1','color': 'white'})
                                    )
                            ],
                        ),
                        # Change to side-by-side for mobile layout
                        html.Div(
                            
                            children=[
                                html.Div(
                                    className="div-for-dropdown",
                                    children=[
                                        # Dropdown for locations on map
                                        dcc.Dropdown(
                                            id='crossfilter-xaxis-column',
                                            options=drop_options,
                                            value='SO2' )
                                            #className='dropdown')
                                            #style={'border-radius': '5px', 'background-color': 
                                            #   'white', 'opacity':'1','color': 'white'})
                                    ],
                                ),
                                html.P(
                                    """Selecciona una mesura."""
                                    ),
                                html.Div(
                                    className='div-for-dropdown',
                                    children=[
                                        # Dropdown to select times
                                        dbc.RadioItems(
                                            id='crossfilter-xaxis-type',
                                            options=radio_options,
                                            value='% Faltants',
                                            inline=True,
                                            className='btn-group-vertical',
                                            #inputClassName="btn-check",
                                            labelClassName='btn btn-outline-secondary',
                                            labelCheckedClassName="active"
                                          
                                           
                                        )
                                    ],
                                ),
                            ],
                        ),
                       
                    ],
                ),
                # Column for app graphs and plots
                html.Div(className="seven columns",
                    children=[
                        dcc.Graph(
                        id='crossfilter-indicator-mapbox'),
                        
                            
                    ],
                ),
            ],
          
        )
            
    ]
        
)

@app.callback(Output(component_id='crossfilter-indicator-mapbox', component_property='figure'),
              [Input(component_id='crossfilter-xaxis-column',
                     component_property='value')],
              [Input(component_id='crossfilter-xaxis-type',
                     component_property='value')],
              [Input(component_id='my-date-picker-single', component_property='date')]
              #[Input(component_id='crossfilter-xaxis-month', component_property='value')]
              )
def update_graph(xaxis_column, xaxis_type,date):
    if date is not None:
        date = date.split("T")[0]
        date = dt.datetime.strptime(date, '%Y-%m-%d')
        month = date.month
        year = date.year

    if xaxis_type == '% Faltants':
        d = proporcio[proporcio['Year'] == year]
       
        df=d[d['Mes'] == month]
        dff = df.dropna(subset=[xaxis_column])

                # Agregar columna "color" a "dff" según el valor de "xaxis_column"
       #dff['Proporció de faltants'] = dff[xaxis_column].apply(lambda x: '+ 20% faltants' if x > 20 else '- 20% faltants')
        dff['Proporció de faltants'] = dff[xaxis_column].apply(lambda x: '<= 5% faltants' if x <= 5 else ('<= 10% faltants' if (x>5 and x<=10) else ('<= 20% faltants' if (x<=20 and x>10) else ('<= 30% faltants' if (x<=30 and x>20) else '>30% faltants') )))
                                                               

        # Definir mapa de colores para "color_discrete_map"
        color_map = {'<= 5% faltants': '#5b9b14', '<= 10% faltants': '#a7b726', '<= 20% faltants':'#e2cb0e', '<= 30% faltants':'#ec933e','>30% faltants':'#df3f0c' }
        
        # Crear gráfico con opción "color_discrete_map"
        sizes=[20 for i in range(0,len(dff))]
        fig = px.scatter_mapbox(dff, lat='lat', lon='long',size=sizes,height=560, hover_name='Estacion',
                                opacity=0.80, zoom=12,mapbox_style='stamen-terrain',
                        color='Proporció de faltants', color_discrete_map=color_map)
        fig.update_layout(margin={'l': 0, 'b': 0, 't': 0, 'r': 0},mapbox=dict(
            bearing=0,
            center=dict(
                lat=39.47057375657113,
                lon=-0.37641920323962136
            )), hovermode='closest')
        fig.update_traces(marker=dict(sizemode='area', sizemin=15),  # Establecer tamaño mínimo de 10
                              hovertemplate='<b>%{hovertext}</b>')
        
    elif xaxis_type == 'Mitjana Artimètica':
        d = mitjana[mitjana['Year'] == year]
       
        df=d[d['Mes'] == month]
        dff = df.dropna(subset=[xaxis_column])
        fig = px.scatter_mapbox(dff, lat='lat', lon='long', size=xaxis_column,height=560, hover_name='Estacion',
                                opacity=0.80, size_max=30, zoom=12, mapbox_style='stamen-terrain',color_discrete_sequence=['#5b9b14'],hover_data={'lat':False, 'long':False})
        
                
        
        
        fig.update_layout(margin={'l': 0, 'b': 0, 't': 0, 'r': 0},mapbox=dict(
            bearing=0,
            center=dict(
                lat=39.47057375657113,
                lon=-0.37641920323962136

            )), hovermode='closest')
        fig.update_traces(marker=dict(sizemode='area', sizemin=6))

    elif xaxis_type == 'Variància':

        d = variancia[variancia['Year'] == year]
       
        df=d[d['Mes'] == month]
        dff = df.dropna(subset=[xaxis_column])
        # , size_max=30, text='Estacion',color_discrete_sequence=['red'], opacity=0.25, zoom=12,
        fig = px.scatter_mapbox(dff, lat='lat', lon='long', size=xaxis_column,height=560,hover_name='Estacion',
                                opacity=0.80, size_max=30, zoom=12, mapbox_style='stamen-terrain',color_discrete_sequence=['#5b9b14'],hover_data={'lat':False, 'long':False})
        
                
        
        
        fig.update_layout(margin={'l': 0, 'b': 0, 't': 0, 'r': 0},mapbox=dict(
            bearing=0,
            center=dict(
                lat=39.47057375657113,
                lon=-0.37641920323962136
            )), hovermode='closest')
        fig.update_traces(marker=dict(sizemode='area', sizemin=6))


    else:
        pass

    # df=d.loc[d.loc[:,'Mes']==month_value]

   # dff = d.dropna(subset=[xaxis_column])

    # Crear la figura con Plotly Express

    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
