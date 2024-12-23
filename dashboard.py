import dash
from dash import dcc, html
import pandas as pd
import plotly.express as px

# Initialize Dash app
app = dash.Dash(__name__)

# Load dataset
data = pd.read_csv('merged_dataset.csv')
print(data.columns)  # Debugging: Check column names

# Normalize column names (optional)
data.columns = data.columns.str.replace(' ', '_')

# Create a bar chart
fig = px.bar(data, x='Shelter', y='Anxiety_Lvl', title='Anxiety Levels by Shelter')

# Define app layout
app.layout = html.Div([
    html.H1("Homelessness Data Dashboard"),
    dcc.Graph(figure=fig)
])

# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=5000)
