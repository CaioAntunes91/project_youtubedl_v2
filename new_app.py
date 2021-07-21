import os.path
from flask import Flask, request #
import os
import json
import time
import new_run_backend

import sqlite3 as sql #
import get_data #
import ml_utils #

app = Flask(__name__)

# queries = ["machine+learning", "data+science", "kaggle", "projeto+python"]
queries = ["machine+learning", "data+science"]
qtd_videos = 5

def get_predictions(queries, qtd_videos):
	
	videos = []

	with sql.connect(new_run_backend.db_name) as conn:
		c = conn.cursor()
		for line in c.execute("SELECT * FROM videos"):
			#(title, video_id, score, update_time)
			line_json = {
			"title": line[0],
			"video_id": line[1],
			"score": line[2],
			"update_time": line[3]
			}
			videos.append(line_json)

	predictions = []
	for video in videos:
		predictions.append((video['video_id'], video['title'], float(video['score'])))

	predictions = sorted(predictions, key=lambda x: x[2], reverse=True)[:30]

	predictions_formatted = []
	for e in predictions:
		predictions_formatted.append(
			"<tr><th><a href=\"{link}\">{title}</a></th><th>{score}</th></tr>".format(
				title=e[1],
				link=e[0],
				score=e[2]
				)
			)

	last_update = videos[0]["update_time"]

	return '\n'.join(predictions_formatted), last_update

@app.route('/')#Pesquisar decorator do Python @ e outros
def main_page():
	preds, last_update = get_predictions(queries, qtd_videos)
	return """<head><h1>Recomendador de vídeo do Youtube</h1></head>
	<body>
	Segundos desde a última atualização: {}
	<table>
		{}
	</table>
	</body>""".format((time.time_ns() - last_update) / 1e9, preds)

@app.route('/update')
def update_database():
	with sql.connect(new_run_backend.db_name) as conn:
		c = conn.cursor()
		# Create table
		c.execute("""CREATE TABLE videos (title text, video_id text, score real, update_time integer)""")
		conn.commit()

	new_run_backend.update_db(queries, qtd_videos)

	return """<head><h1>Recomendador de vídeo do Youtube</h1></head>
	<body>
	<p>Atualização realizada em: {}/{}/{}</p>
	</body>""".format(time.localtime().tm_mday,time.localtime().tm_mon,time.localtime().tm_year)

@app.route('/delete')
def delete_database():
	with sql.connect(new_run_backend.db_name) as conn:
		c = conn.cursor()
		# Create table
		c.execute("""DROP TABLE videos""")
		conn.commit()

	return """<head><h1>Recomendador de vídeo do Youtube</h1></head>
	<body>
	<p>Tabela deletada em: {}/{}/{}</p>
	</body>""".format(time.localtime().tm_mday,time.localtime().tm_mon,time.localtime().tm_year)

if __name__ == '__main__':
	# app.run(debug=True, host='0.0.0.0')# Retirar o parâmetro debug quando for ser colocado em produção
	# app.run(host='localhost', port='5000')
	# Produção
	port = os.environ.get('PORT', 5000)
	app.run(host='0.0.0.0', port=port)