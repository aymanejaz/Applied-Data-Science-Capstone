# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                
                                dcc.Dropdown(id='site-dropdown',
                                             options=[
                                                  {'label': 'All Sites', 'value': 'ALL'},
                                                  {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                                  {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
                                                  {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                                  {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                                              ],
                                              value='ALL',
                                              placeholder="Select a Launch Site here",
                                              searchable=True
                                              ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)
                                
                                dcc.RangeSlider(
				                    id='range-slider', min=0, max=10000, step=1000,
                                    marks={0: '0', 10000: '10000'},
                                    value=[min_payload, max_payload]
		                		),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                # html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                # ])
                                html.Div(dcc.Graph(id='scatter-plot')),
                                 ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    filtered_df = spacex_df[spacex_df['Launch Site']==str(entered_site)]
    grouped_fdf = filtered_df.groupby(['class'])['Launch Site'].count().reset_index()
    if entered_site == 'ALL':
        fig = px.pie(spacex_df, values='class', 
        names='Launch Site', 
        title='% Success Per Luanch Site')
        return fig
    else:
        fig = px.pie(grouped_fdf, 
        values='Launch Site', 
        names='class', 
        title='x`', 
        color='class')
        return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output("scatter-plot", "figure"), 
    [Input("range-slider", "value"),
    Input("site-dropdown", "value")])
def update_bar_chart(slider_range,entered_site):
    low, high = slider_range
    mask = (spacex_df['Payload Mass (kg)'] > low) & (spacex_df['Payload Mass (kg)'] < high)
    filtered_df = spacex_df[spacex_df['Launch Site']==str(entered_site)]
    mask1 = (filtered_df['Payload Mass (kg)'] > low) & (filtered_df['Payload Mass (kg)'] < high)    
    if entered_site == 'ALL': 
    
        fig = px.scatter(
        spacex_df[mask], x="Payload Mass (kg)", y="class", 
        color="Booster Version Category")
        return fig
    else:
        fig = px.scatter(
        filtered_df[mask1], x="Payload Mass (kg)", y="class", 
        color="Booster Version Category")
        return fig


# Run the app
if __name__ == '__main__':
    app.run_server()
