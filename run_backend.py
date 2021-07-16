from get_data import *
from ml_utils import *
import time

def update_db(filename, queries, qtd_videos):
	video_list = []

	for query in queries:
		video_list += download_data_youtubedl(query, qtd_videos)	
		
	video_list = [e for e in video_list if e is not None]
	df = pd.DataFrame(video_list)

	df['upload_date'] = pd.to_datetime(df["upload_date"])
	df['dias_desde_upload'] = (pd.to_datetime("2021-12-03") - df['upload_date']) / np.timedelta64(1, 'D')

	colunas = ['title', 'thumbnails', 'duration', 'like_count',
				'dislike_count', 'upload_date', 'view_count',
				'dias_desde_upload', 'description', 'channel_url',
				'webpage_url', '_query']

	df2 = df[colunas]
	df2 = df2.drop_duplicates(subset=['webpage_url'])
	df2.reset_index(inplace=True)

	df_feature = compute_features(df2)

	p = compute_predictions(df_feature)
	print(p)

	data_front = pd.DataFrame(index=df2.index)
	data_front['title'] = df2['title'].copy()
	data_front['score'] = p
	data_front['video_id'] = df2['webpage_url'].copy()

	with open(filename, "w+") as output:
		for index, row in data_front.iterrows():
			data_front_formated = {"title": row['title'], "score": row["score"], "video_id": row["video_id"]}
			data_front_formated['update_time'] = time.time_ns()

			output.write("{}\n".format(json.dumps(data_front_formated)))