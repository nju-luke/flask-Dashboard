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

    fig = px.scatter(df, x="x", y="y", text="name", size_max=60)

    fig.update_traces(textposition='top center')

    fig.update_layout(
        height=800,
        title_text='员工测评、积分综合分布图'
    )

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
