from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd
from datetime import datetime, timedelta

# Load Excel file
file_path = 'data/202501081835HF.xlsx'
df_raw = pd.read_excel(file_path, header=0)

# Extract starting date and time from specific cells (C1 and D1)
start_date = pd.read_excel(file_path, header=None).iloc[0, 2]
start_time = pd.read_excel(file_path, header=None).iloc[0, 3]
start_datetime = pd.to_datetime(f"{start_date} {start_time}")

# Retain only 'Vb' and 'Ct' columns and generate datetime column
df = df_raw[['Vb', 'Ct']].copy()
df['datetime'] = [start_datetime + timedelta(seconds=i) for i in range(len(df))]

# Initialize Dash app
app = Dash(__name__)

# Layout
app.layout = html.Div([
    html.H1("High Frequency Analysis", style={'textAlign': 'center'}),

    dcc.Dropdown(
        id='column-selector',
        options=[
            {'label': 'VB', 'value': 'Vb'},
            {'label': 'CT', 'value': 'Ct'}
        ],
        value='Vb',
        style={'width': '50%', 'margin': 'auto'}
    ),

    dcc.Graph(id='graph-content')
])

# Callback for dynamic plotting
@callback(
    Output('graph-content', 'figure'),
    Input('column-selector', 'value')
)
def update_graph(selected_col):
    fig = px.line(df, x='datetime', y=selected_col, title=f"{selected_col.upper()} Over Time (High Frequency)")
    fig.update_layout(transition_duration=500)
    return fig

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
