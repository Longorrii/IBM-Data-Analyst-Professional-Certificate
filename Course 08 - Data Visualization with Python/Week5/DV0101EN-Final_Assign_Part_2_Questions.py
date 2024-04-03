#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px

# Load the data using pandas
data = pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/historical_automobile_sales.csv')

# Initialize the Dash app
app = dash.Dash(__name__)

# Set the title of the dashboard
app.title = "Automobile Statistics Dashboard"

#---------------------------------------------------------------------------------
# Create the dropdown menu options
dropdown_options = [
    {'label': 'Yearly Statistics', 'value': 'Yearly Statistics'},
    {'label': 'Recession Period Statistics', 'value': 'Recession Period Statistics'}
]
# List of years 
year_list = [i for i in range(1980, 2024, 1)]
#---------------------------------------------------------------------------------------
# Create the layout of the app
app.layout = html.Div([
    html.H1("Automobile Sales Statistics Dashboard", style={'textAlign': 'center', 'color': '#503D36', 'font-size': '24px'}),
    html.Div([
        html.Label("Select Statistics:"),
        dcc.Dropdown(
            id='dropdown-statistics',
            options=dropdown_options,
            value='Yearly Statistics',
            placeholder='Select a report type...',
            style={'width': '80%', 'padding': '3px', 'font-size': '20px', 'text-align-last': 'center'}
        )
    ]),
    html.Div(dcc.Dropdown(
            id='select-year',
            options=[{'label': i, 'value': i} for i in year_list],
            placeholder='Select a year...',
            style={'width': '80%', 'padding': '3px', 'font-size': '20px', 'text-align-last': 'center'}
        )),
    html.Div([
        html.Div(id='output-container', className='chart-grid', style={'display': 'flex'}),
    ])
])
#TASK 2.4: Creating Callbacks
# Define the callback function to update the input container based on the selected statistics
# Callback for plotting Recession Report Statistics
@app.callback(
    Output(component_id='output-container', component_property='children'),
    [Input(component_id='select-year', component_property='value'), 
     Input(component_id='dropdown-statistics', component_property='value')])
def update_output_container(input_year, selected_statistics):
    if selected_statistics == 'Recession Period Statistics':
        # Filter the data for recession periods
        recession_data = data[data['Recession'] == 1]
        
        # Plot 1: Automobile sales fluctuate over recession period (year wise) using line chart
        yearly_rec = recession_data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        chart1 = dcc.Graph(figure=px.line(yearly_rec, x='Year', y='Automobile_Sales', 
                                           title="Average Automobile Sales Fluctuation over Recession Period"))
        
        # Plot 2: Calculate the average number of vehicles sold by vehicle type and represent as a Bar chart
        average_sales = recession_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
        chart2 = dcc.Graph(figure=px.bar(average_sales, x='Vehicle_Type', y='Automobile_Sales', 
                                          title="Average Vehicles Sold by Vehicle Type during Recession"))
        
        # Plot 3: Pie chart for total expenditure share by vehicle type during recessions
        exp_rec = recession_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        chart3 = dcc.Graph(figure=px.pie(exp_rec, values='Advertising_Expenditure', names='Vehicle_Type',
                                          title="Total Advertisement Expenditure Share by Vehicle Type during Recession"))
        
        # Plot 4: Develop a Bar chart for the effect of unemployment rate on vehicle type and sales
        unemployment_data = recession_data.groupby('Vehicle_Type')['unemployment_rate'].mean().reset_index()
        chart4 = dcc.Graph(figure=px.bar(unemployment_data, x='Vehicle_Type', y='unemployment_rate',
                                          title="Effect of Unemployment Rate on Vehicle Type and Sales during Recession"))
        
        return [
            html.Div(className='chart-item', children=[chart1, chart2]),
            html.Div(className='chart-item', children=[chart3, chart4])
        ]
    
    elif input_year and selected_statistics == 'Yearly Statistics':
        yearly_data = data[data['Year'] == input_year]
        
        # Plot 1: Yearly Automobile sales using line chart for the whole period.
        yearly_sales = data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        chart1 = dcc.Graph(figure=px.line(yearly_sales, x='Year', y='Automobile_Sales', 
                                           title='Yearly Automobile Sales Over the Whole Period'))
        
        # Plot 2: Total Monthly Automobile sales using line chart.
        monthly_sales = yearly_data.groupby('Month')['Automobile_Sales'].sum().reset_index()
        chart2 = dcc.Graph(figure=px.line(monthly_sales, x='Month', y='Automobile_Sales', 
                                           title='Total Monthly Automobile Sales'))
        
        # Plot 3: Bar chart for average number of vehicles sold during the given year
        average_sales_yearly = yearly_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
        chart3 = dcc.Graph(figure=px.bar(average_sales_yearly, x='Vehicle_Type', y='Automobile_Sales', 
                                          title='Average Vehicles Sold by Vehicle Type in {}'.format(input_year)))
        
        # Plot 4: Pie chart for total advertisement expenditure for each vehicle type
        exp_per_vehicle = yearly_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        chart4 = dcc.Graph(figure=px.pie(exp_per_vehicle, values='Advertising_Expenditure', names='Vehicle_Type',
                                          title='Total Advertisement Expenditure for Each Vehicle Type in {}'.format(input_year)))
        
        return [
            html.Div(className='chart-item', children=[chart1, chart2]),
            html.Div(className='chart-item', children=[chart3, chart4])
        ]
    
    else:
        return None

# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)

