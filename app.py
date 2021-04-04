from flask import Flask, render_template, request, redirect
import requests
import simplejson as json
import pandas as pd
import bokeh
from bokeh.plotting import figure, output_file, show
from bokeh.models import CheckboxGroup
from bokeh.plotting import figure
from bokeh.embed import components

#create form and button classes
app = Flask(__name__)
app.vars = {}

@app.route('/', methods = ["GET", "POST"])
def index():
	if request.method == 'GET':
		return render_template('index.html')
	else:
		#request was a post
		return ticker(request.form["symbull"])

@app.route('/about')
def about():
  return render_template('about.html')

@app.route('/ticker/<string:symb>', methods = ["GET", "POST"])
def ticker(symb):
	#get API
	query_params = {'function': 'TIME_SERIES_DAILY_ADJUSTED', 'symbol': symb, 'outputsize': "compact",'apikey':'GIPEBXGZOPJLSY3H'}
	r = requests.get("https://www.alphavantage.co/query", params = query_params)
	stock_data_json_str = json.dumps(r.json()['Time Series (Daily)'])
	stock_df = pd.read_json(stock_data_json_str)
	time_stock = stock_df.transpose().reset_index()

	#Plot Stock line graph with bokeh

	x = time_stock['index']
	y1 = time_stock['1. open']
	y2 = time_stock['2. high']
	y3 = time_stock['3. low']
	y4 = time_stock['4. close']
	y5 = time_stock['5. adjusted close']

	p = figure(title = 'Daily Stock Price', x_axis_type='datetime', x_axis_label = 'Date', y_axis_label = 'Stock Price', )
	p.line(x, y1, legend_label ="opening price", line_color="blue", line_width=2)
	p.line(x, y2, legend_label ="high price", line_color="green", line_width=2)
	p.line(x, y3, legend_label ="low price", line_color="red", line_width=2)
	p.line(x, y4, legend_label ="closing price", line_color="cyan", line_width=2)
	p.line(x, y5, legend_label ="adj. closing price", line_color="black", line_width=2)

	#show(p)
	script, div = components(p)
	return render_template("ticker.html", symbol=symb, the_div=div, the_script=script)

	# get bokeh result for symb
	# insert bokeh result into html generating function

if __name__ == '__main__':
  app.run(port=33507)
