# this works better than low_fre.py make sure to integrate it with the main
from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd

# Load and prepare the data
df = pd.read_excel('data/20250108LF.xlsx', header=None)

# Assign column names
df.columns = df.iloc[0]
df = df.drop(0).reset_index(drop=True)
df.columns = ['date', 'time', 'vr', 'ir', 'pf', 't1', 't2']

# Create datetime column
df['datetime'] = pd.to_datetime(df['date'].astype(str) + ' ' + df['time'].astype(str))

# Convert data columns to numeric
for col in ['vr', 'ir', 'pf', 't1', 't2']:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# Reorder columns
df = df[['datetime', 'vr', 'ir', 'pf', 't1', 't2']]

# Initialize Dash app
app = Dash(__name__)

# App layout
app.layout = html.Div([
    html.H1(children='Low Frequency Analysis', style={'textAlign': 'center'}),

    dcc.Dropdown(
        id='column-selector',
        options=[{'label': col.upper(), 'value': col} for col in ['vr', 'ir', 'pf', 't1', 't2']],
        value='vr',
        style={'width': '50%', 'margin': 'auto'}
    ),

    dcc.Graph(id='graph-content')
])

# Callback to update graph
@callback(
    Output('graph-content', 'figure'),
    Input('column-selector', 'value')
)
def update_graph(selected_col):
    fig = px.line(df, x='datetime', y=selected_col, title=f"{selected_col.upper()} Over Time")
    fig.update_layout(transition_duration=500)
    return fig

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
