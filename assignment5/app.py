from flask import Flask, render_template, redirect, url_for
import pandas as pd

app = Flask(__name__)
    
################################################################################################################

# WEB ROUTES FOR CONTROLLING ACCESS TO TEMPLATE VIEWS

################################################################################################################

@app.route("/")
def index():
    return render_template('index.html')


@app.route("/movies")
def movies():
    df = pd.read_csv("base_info.csv",delimiter="\t")
    list = df.to_dict('records')
    return render_template('movies.html', entries = list)


if __name__ == '__main__':
    app.run()