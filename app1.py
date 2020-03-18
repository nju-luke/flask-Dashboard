from flask import Flask, render_template,request
import plotly
import plotly.graph_objs as go

import json

import pandas as pd
import string
import numpy as np
import plotly.express as px


app = Flask(__name__)


@app.route('/')
def index():
    feature = 'Bar'
    bar = create_plot(feature)
    return render_template('index.html', plot=bar)

def create_plot(feature):
    nums = 20
    df = pd.DataFrame(np.random.randn(nums, 2) * 10 + 70, dtype=np.int, columns=['x', 'y'], index=list(range(nums)))

    df['name'] = [f'员工_{string.ascii_uppercase[i]}' for i in range(nums)]
    df = df.groupby(['x', 'y'])['name'].agg(lambda x: ','.join(x)).reset_index()

    df_area = pd.DataFrame([[1, 1, 2, 2, 1], [1, 2, 2, 1, 1]]).T * 10

    df_area1 = df_area.copy()

    df_area[0] += 40
    df_area[1] += 40

    df_area1[0] += 70
    df_area1[1] += 70
    fig = go.Figure()

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(x=df_area[0], y=df_area[1], line_color='Coral', mode='lines', fill='toself', fillcolor='LightSalmon',
                   name='Warn'))
    fig.add_trace(
        go.Scatter(x=df_area1[0], y=df_area1[1], line_color='lightskyblue', mode='lines', fill='toself', name='Pef'))
    fig.add_trace(go.Scatter(x=df['x'], y=df['y'], text=df['name'], mode='markers + text', textposition='top center'))

    fig.update_layout(showlegend=False)

    # fig.show()


    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON

@app.route('/bar', methods=['GET', 'POST'])
def change_features():
    feature = request.args['selected']
    graphJSON= create_plot(feature)

    return graphJSON

if __name__ == '__main__':
    app.run()
