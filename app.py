from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder_unfiltered.csv')

def create_bar_chart(df, year):
 dff = df[df.year == year]
 top_15 = dff.groupby('country')['pop'].sum().nlargest(15).reset_index()
 fig = go.Figure(data=go.Bar(x=top_15['country'], y=top_15['pop']),
 layout=go.Layout(title=f'Столбчатая диаграмма ({year})', xaxis=dict(title='Страна'), yaxis=dict(title='Популяция')))
 return fig

def create_pie_chart(df, year):
 dff = df[df.year == year]
 continent_pop = dff.groupby('continent')['pop'].sum().reset_index()
 fig = go.Figure(data=go.Pie(labels=continent_pop['Континент'], values=continent_pop['Популяция']))
 return fig

app = Dash(__name__)
server=app.server

app.layout = html.Div([
html.H1(children=' ', style={'textAlign': 'center'}),

dcc.Tabs(id='tabs', value='scatter', children=[
dcc.Tab(label='Линейная диаграмма', value='scatter', children=[
dcc.Dropdown(options=[{'label': country, 'value': country} for country in df.country.unique()],value=['Canada'], multi=True, id='scatter-dropdown-selection'),
dcc.Dropdown(options=[{'label': col, 'value': col} for col in df.columns[3:]],value='pop', id='scatter-y-axis-selection')]),

dcc.Tab(label='Пузырьковая диаграмма', value='bubble', children=[
dcc.Dropdown(options=[{'label': col, 'value': col} for col in df.columns[3:]],value='gdpPercap', id='bubble-x-axis-selection'),
dcc.Dropdown(options=[{'label': col, 'value': col} for col in df.columns[3:]],value='pop', id='bubble-y-axis-selection'),
dcc.Dropdown(options=[{'label': col, 'value': col} for col in df.columns[3:]],value='lifeExp', id='bubble-radius-selection'),
dcc.Dropdown(options=[{'label': year, 'value': year} for year in df.year.unique()],value=df.year.min(), id='bubble-year-selection')]),
    
dcc.Tab(label='Столбчатая диаграмма', value='top-15', children=[
dcc.Dropdown(options=[{'label': year, 'value': year} for year in df.year.unique()],value=df.year.min(), id='top15-year-selection')]),
    
dcc.Tab(label='Круговая диаграмма', value='population-by-continent', children=[
dcc.Dropdown(options=[{'label': year, 'value': year} for year in df.year.unique()],value=df.year.min(), id='continent-year-selection')])]),
dcc.Graph(id='graph-content'),
html.H3(id='graph-title')
])

@app.callback(
Output('graph-content', 'figure'),
Output('graph-title', 'children',allow_duplicate=True),
Input('tabs', 'value'),
Input('scatter-dropdown-selection', 'value'),
Input('scatter-y-axis-selection', 'value'),
Input('bubble-x-axis-selection', 'value'),
Input('bubble-y-axis-selection', 'value'),
Input('bubble-radius-selection', 'value'),
Input('bubble-year-selection', 'value'),
Input('top15-year-selection', 'value'),
Input('continent-year-selection', 'value'),
prevent_initial_call='initial_duplicate'
)
def update_graph(selected_tab, scatter_selected_countries, scatter_selected_y,
 bubble_selected_x, bubble_selected_y, bubble_selected_radius,
 bubble_selected_year, top15_selected_year,continent_selected_year):
 if selected_tab == 'scatter':
  dff_scatter = df[df.country.isin(scatter_selected_countries)]
  fig_scatter = px.line(dff_scatter, x='Год', y=scatter_selected_y, color='Страна')
  return fig_scatter, f'Selected Tab: {selected_tab}, Selected Countries: {", ".join(scatter_selected_countries)}, Y-Axis: {scatter_selected_y}'

 elif selected_tab == 'bubble':
  dff_bubble = df[df.year == bubble_selected_year]
  fig_bubble = px.scatter(dff_bubble, x=bubble_selected_x, y=bubble_selected_y, size=bubble_selected_radius)
  return fig_bubble, f'Selected Tab: {selected_tab}, X-Axis: {bubble_selected_x}, Y-Axis: {bubble_selected_y}, Bubble Size: {bubble_selected_radius}, Year: {bubble_selected_year}'

 elif selected_tab == 'top-15':
  dff_top15 = df[df.year == top15_selected_year]
  fig_top15 = create_bar_chart(dff_top15, top15_selected_year)
  return fig_top15, f'Selected Tab: {selected_tab}, Year: {top15_selected_year}'
    
 elif selected_tab == 'population-by-continent':
  dff_continent = df[df.year == continent_selected_year]
  fig_continent = create_pie_chart(dff_continent, continent_selected_year)
  return fig_continent, f'Selected Tab: {selected_tab}, Year: {continent_selected_year}'
@app.callback(
Output('graph-title', 'children'),
Input('tabs', 'value'),
Input('scatter-dropdown-selection', 'value'),
Input('scatter-y-axis-selection', 'value'),
Input('bubble-x-axis-selection', 'value'),
Input('bubble-y-axis-selection', 'value'),
Input('bubble-radius-selection', 'value'),
Input('bubble-year-selection', 'value'),
Input('top15-year-selection', 'value'),
Input('continent-year-selection', 'value'),
)
def update_graph_title(selected_tab, scatter_selected_countries, scatter_selected_y,
 bubble_selected_x, bubble_selected_y, bubble_selected_radius,
 bubble_selected_year, top15_selected_year, continent_selected_year):
 if selected_tab == 'scatter':
  return f'Selected Tab: {selected_tab}, Selected Countries: {", ".join(scatter_selected_countries)}, Y-Axis: {scatter_selected_y}'

 elif selected_tab == 'bubble':
  return f'Selected Tab: {selected_tab}, X-Axis: {bubble_selected_x}, Y-Axis: {bubble_selected_y}, Bubble Size: {bubble_selected_radius}, Year: {bubble_selected_year}'

 elif selected_tab == 'top-15':
  return f'Selected Tab: {selected_tab}, Year: {top15_selected_year}'
    
 elif selected_tab == 'population-by-continent':
  return f'Selected Tab: {selected_tab}, Year: {continent_selected_year}'
    
if __name__ == '__main__':
 app.run_server(debug=False)
