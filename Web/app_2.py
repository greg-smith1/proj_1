import dash
import dash_core_components as dcc
import dash_html_components as html
import flask
from flask import render_template, Flask
import pandas as pd
import plotly.graph_objs as go


app_flask = flask.Flask(__name__)
app_dash = dash.Dash(__name__, server=app_flask, url_base_pathname='/projections')


@app_flask.route('/')
def home():
    return render_template('homepage.html')

@app_flask.route('/about')
def about():
    return render_template('about.html')

@app_flask.route('/tech')
def tech():
    return render_template('tech.html')

@app_flask.route('/author')
def author():
    return render_template('author.html')

app_dash.title='NHL Projections'

colors = {
    'background': '#F3F5D8',
    'text': '#1E567C'
}

df = pd.read_csv('https://raw.githubusercontent.com/greg-smith1/proj_1/master/all_current_players.csv')

app_dash.css.append_css({'external_url': 'https://getbootstrap.com/docs/4.0/dist/css/bootstrap.min.css'})
app_dash.css.append_css({'external_url': 'https://getbootstrap.com/docs/4.0/examples/sticky-footer-navbar/sticky-footer-navbar.css'})

teams = sorted(df['Team'].unique())

team_names = {'BOS':'Boston Bruins', 'CAR':'Carolina Hurricanes', 'DET':'Detroit Red Wings',
              'WPG':'Winnipeg Jets', 'BUF':'Buffalo Sabres', 'FLA':'Florida Panthers',
              'MTL':'Montreal Canadiens', 'OTT':'Ottawa Senators', 'TBL':'Tampa Bay Lightning',
              'TOR':'Toronto Maple Leafs', 'CBJ':'Columbus Blue Jackets', 'NJD':'New Jersey Devils',
              'NYI':'New York Islanders', 'NYR':'New York Rangers', 'PHI':'Philadelphia Flyers',
              'PIT':'Pittsburgh Penguins', 'WSH':'Washington Capitals', 'CHI':'Chicago Blackhawks',
              'COL':'Colorado Avalanche', 'DAL':'Dallas Stars', 'MIN':'Minnesota Wild',
              'NSH':'Nashville Predators', 'STL':'St. Louis Blues', 'ANA':'Anaheim Ducks',
              'ARI':'Arizona Coyotes', 'CGY':'Calgary Flames', 'EDM':'Edmonton Oilers',
              'LAK':'Los Angeles Kings', 'SJS':'San Jose Sharks', 'VAN':'Vancouver Canucks',
              'VEG':'Vegas Golden Knights'}

app_dash.layout = html.Div(style={}, children=[
    
    html.Span(html.A(html.Button('Homepage', className='homepage', style={
    'backgroundColor': '#272C31',
    'border': 'none',
    'color': 'white',
    'textAlign': 'center',
    'textDecoration': 'none',
    'display': 'block',
    'fontSize': '20px'}),
    href='/'),
    style={'backgroundColor': '#272C31', 'padding': '10px', 'display':'block'}
    ),

  
    html.Div(id='output-a',
        style={
            'textAlign': 'center',
            'color':'#1D2125',
            'font-size':'150%',
            'margin-top':'45'
        }
    ),

    html.Div([
        dcc.Dropdown(
            id='xaxis-column',
            options=[{'label': i, 'value': i} for i in teams],
            value='DET',
            clearable=False
            ),
        ],
        style={'width': '15%', 'margin':'auto', 'display':'block'}),

        html.P(children='Click and drag to select/zoom, double click to reset view',
        style={'textAlign': 'center', 'margin-top':'20'}
    ),



    dcc.Graph(id='nhl_goals', config={"displayModeBar": False}),

])


@app_dash.callback(
    dash.dependencies.Output('nhl_goals', 'figure'),
    [dash.dependencies.Input('xaxis-column', 'value')])
def update_figure(selected_team):
    filtered_df = df[df.Team == selected_team]
    traces = []
    for i in filtered_df.Full_Name.unique():
        df_by_player = filtered_df[filtered_df['Full_Name'] == i]
        traces.append(go.Scatter(
            x=df_by_player['Season'],
            y=df_by_player['G'],
            text=df_by_player['Team'],
            mode='lines+markers',
            opacity=0.8,
            marker={
                'size': 4.5,
                'line': {'width': 0.5, 'color': 'white'}
            },
            name=i
        ))

    return {
        'data': traces,
        'layout': go.Layout(
            xaxis={'type': 'linear', 'title': 'Season', 'autotick': 'False'},
            yaxis={'title': 'Goals'},
            margin={'l': 100, 'b': 40, 't': 23, 'r': 100},
            #legend={'x': 0, 'y': 1},
            hovermode='compare'
        )
    }

@app_dash.callback(
    dash.dependencies.Output('output-a', 'children'),
    [dash.dependencies.Input('xaxis-column', 'value')])
def callback_a(dropdown_value):
    return '{} Goals by Season'.format(team_names[dropdown_value])



if __name__ == '__main__':
    app_flask.run(host='0.0.0.0', debug=True)


