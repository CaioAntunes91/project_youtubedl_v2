import os.path
from flask import Flask
import os
import json
import time
import run_backend

app = Flask(__name__)

queries = ["machine+learning", "data+science", "kaggle", "projeto+python"]
# queries = ["machine+learning", "data+science"]
qtd_videos = 20

def get_predictions(queries, qtd_videos):
	
	videos = []

	novos_videos_json = "novos_videos.json"
	if not os.path.exists(novos_videos_json):
		run_backend.update_db(novos_videos_json, queries, qtd_videos)

	last_update = os.path.getmtime(novos_videos_json) * 1e9# A função getmtime retorna o momento em que o arquivo foi modificado pela última vez (trazendo em segundos desde a data 01/01/1970)

	if time.time_ns() - last_update > (720 * 3600 * 1e9):# Aproximadamente 1 mês
		run_backend.update_db(novos_videos_json, queries, qtd_videos)

	with open("novos_videos.json", "r") as data_file:
		for line in data_file:
			line_json = json.loads(line)
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

if __name__ == '__main__':
	# app.run(debug=True, host='0.0.0.0')# Retirar o parâmetro debug quando for ser colocado em produção
	# app.run(host='localhost', port='5000')
	# Produção
	port = os.environ.get('PORT', 5000)
	app.run(host='0.0.0.0', port=port)