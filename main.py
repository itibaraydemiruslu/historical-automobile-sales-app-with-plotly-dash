from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd

# Load the data using pandas
df = pd.read_csv('historical_automobile_sales.csv')

# Initialize the Dash app
app = Dash(__name__)

# Set the title of the dashboard
app.title = "Historical Automobile Sales Statistics Dashboard"

# List of years 
year_list = [i for i in range(1980, 2024)]

#---------------------------------------------------------------------------------------
# Create the layout of the app

app.layout = html.Div([
    # Add title to the dashboard
    html.H1("Historical Automobile Sales Statistics Dashboard", style={'textAlign':'center', 'color':'#503D36', 'font-size':'24px', 'font-weight': 'bold'}),
    html.Hr(),
    # Add Select Statistics dropdown
    html.Div([
        html.Label("Select Statistics:"),
        dcc.Dropdown(
            id='dropdown-statistics',
            options=[
                    {'label': 'Yearly Statistics', 'value': 'Yearly Statistics'},
                    {'label': 'Recession Period Statistics', 'value': 'Recession Period Statistics'}
                ],
            value='Select Statistics',
            placeholder='Select a report type',
            style={'width': '100%', 'padding': '3px','font-size': '20px', 'text-align-last':'center'}
        )
    ]),
    # Add Select Year dropdown
    html.Div([
        html.Label("Select Year:"),
        dcc.Dropdown(
            id='dropdown-year',
            options=[{'label': i, 'value': i} for i in year_list],
            placeholder='Select a year',
            style={'width': '100%', 'padding': '3px','font-size': '20px', 'text-align-last':'center'}
        )
    ]),
    # Add a division for output display
    html.Div([
        html.Div(
            id='div-output-container', 
            className='chart-grid', 
            style={'width': '100%', 'padding': '3px','font-size': '20px', 'text-align-last':'center'}
        )
    ])
])
#---------------------------------------------------------------------------------------

# Creating Callbacks
# Define the callback function to update the dropdown-year's disabled property based on the selected statistics
@callback(
    Output(component_id='dropdown-year', component_property='disabled'),
    Input(component_id='dropdown-statistics', component_property='value')
)
def update_dropdown_year_status(selected_statistics):
    if selected_statistics == 'Yearly Statistics': 
        return False
    else: 
        return True

# Define the callback function to update the dropdown-year's value property based on the selected statistics
@callback(
    Output(component_id='dropdown-year', component_property='value'),
    Input(component_id='dropdown-statistics', component_property='value')
)
def update_dropdown_year_value(selected_statistics):
    if selected_statistics == 'Recession Period Statistics': 
        return ""

# Callback for plotting
# Define the callback function to update the output container based on the selected statistics and input year (if available)
@callback(
    Output(component_id='div-output-container', component_property='children'),
    [Input(component_id='dropdown-statistics', component_property='value'), Input(component_id='dropdown-year', component_property='value')]
)
def update_output_container(selected_statistics, input_year):
    if selected_statistics == 'Recession Period Statistics':
        # Create and display graphs for Recession Report Statistics

        # Filter the data for recession periods
        recession_data = df[df['Recession'] == 1]

        # Plot 1 Automobile sales fluctuate over Recession Period (year wise)
        # use groupby to create relevant data for plotting
        yearly_rec = recession_data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        R_chart1 = dcc.Graph(
            figure=px.line(yearly_rec,
            x='Year',
            y='Automobile_Sales',
            title="Average Automobile Sales fluctuation over Recession Period")
        )

        # Plot 2 Calculate the average number of vehicles sold by vehicle type       
        # use groupby to create relevant data for plotting
        average_sales = recession_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()                           
        R_chart2 = dcc.Graph(
            figure=px.bar(average_sales,
            x='Vehicle_Type',
            y='Automobile_Sales',
            title="Average Automobile Sales by Vehicle Type during Recession Period")
        )
    
        # Plot 3 Pie chart for total expenditure share by vehicle type during recessions
        # use groupby to create relevant data for plotting
        ad_exp = recession_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        R_chart3 = dcc.Graph(
            figure=px.pie(ad_exp,
            values='Advertising_Expenditure',
            names='Vehicle_Type',
            title="Total Expenditures by Vehicle Type during Recession Period")
        )

        # Plot 4 bar chart for the effect of unemployment rate on vehicle type and sales
        unemp_df = recession_data.groupby('Vehicle_Type')['unemployment_rate'].mean().reset_index()
        R_chart4 = dcc.Graph(
            figure=px.bar(unemp_df,
            x='Vehicle_Type',
            y='unemployment_rate',
            title="The Effect of Unemployment Rate on Automobile Type and Sales during Recession Period")
        )      

        # Returning the graphs for displaying recession periods data
        return [
            html.Div(className='chart-item', children=[html.Div(children=R_chart1),html.Div(children=R_chart2)],style={'display': 'flex'}),
            html.Div(className='chart-item', children=[html.Div(children=R_chart3),html.Div(children=R_chart4)],style={'display': 'flex'})
        ]                          
    elif (input_year and selected_statistics == 'Yearly Statistics'):
        # Create and display graphs for Yearly Report Statistics
        # Yearly Statistic Report Plots   

        # Filter the data for selected year
        yearly_data = df[df['Year'] == input_year]
                              
        # Creating Graphs Yearly data                       
        # Plot 1 Yearly Automobile sales using line chart for the whole period.
        yas = df.groupby('Year')['Automobile_Sales'].sum().reset_index()
        Y_chart1 = dcc.Graph(
            figure=px.line(yas,
            x='Year',
            y='Automobile_Sales',
            title="Yearly Automobile sales")
        )
            
        # Plot 2 Total Monthly Automobile sales using line chart.
        mas = yearly_data.groupby('Month')['Automobile_Sales'].sum().reset_index()
        Y_chart2 = dcc.Graph(
            figure=px.line(mas,
            x='Month',
            y='Automobile_Sales',
            title="Monthly Automobile sales")
        )

        # Plot3 Bar chart for average number of vehicles sold during the given year
        avr_vdata = yearly_data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        Y_chart3 = dcc.Graph(
            figure=px.bar(avr_vdata,
            x='Year',
            y='Automobile_Sales',
            range_x=[input_year, input_year],
            title='Average Vehicles Sold by Vehicle Type in the year {}'.format(input_year))
        )

        # Plot3 Total Advertisement Expenditure for each vehicle using pie chart
        exp_data = yearly_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        Y_chart4 = dcc.Graph(
            figure=px.pie(exp_data,
            values='Advertising_Expenditure',
            names='Vehicle_Type',
            title="Total Expenditures by Vehicle Type")
        )
            
        # Returning the graphs for displaying Yearly data
        return [
            html.Div(className='chart-item', children=[html.Div(children=Y_chart1),html.Div(children=Y_chart2)],style={'display': 'flex'}),
            html.Div(className='chart-item', children=[html.Div(children=Y_chart3),html.Div(children=Y_chart4)],style={'display': 'flex'})
        ]
    else:
        return None
    
# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)