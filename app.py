from flask import Flask, render_template, request, jsonify, Response
import requests
import json
import base64
from db_stuff import VideoDatabase
from trending import *

app = Flask(__name__)


@app.route('/')
def index():
    try:
        with open('jsonresponse.json', 'r', encoding='utf-8') as file:
            video_data = json.load(file)
    except json.JSONDecodeError:
        video_data = []
    return render_template('index.html', videos=video_data)


@app.route('/analytics')
def analytics():
    try:
        db = VideoDatabase()
        db.connect()
        video_data = []

        selected_data = db.select_all()
        if selected_data:
            for row in selected_data:
                if row:
                    json_data = {
                        'video_id': row[1],
                        'username': row[2],
                        'likes': row[3],
                        'shares': row[4],
                        'plays': row[5],
                        'thumbnail': row[6],
                        'description': row[7],
                        'hashtags': ','.join([tag.strip() for tag in row[8].split(',') if tag.strip()]),
                        'region': row[9]
                    }
                    video_data.append(json_data)
        else:
            video_data = []

        db.close()
    except json.JSONDecodeError:
        video_data = []

    return render_template('analytics.html', video_data=video_data)


@app.route('/allvideos')
def all_videos():
    try:
        db = VideoDatabase()
        db.connect()
        video_data = []

        selected_data = db.select_all()
        if selected_data:
            for row in selected_data:
                if row:
                    json_data = {
                        'video_id': row[1],
                        'username': row[2],
                        'likes': row[3],
                        'shares': row[4],
                        'plays': row[5],
                        'thumbnail': row[6],
                        'description': row[7],
                        'hashtags': ','.join([tag.strip() for tag in row[8].split(',') if tag.strip()]),
                        'region': row[9]
                    }
                    video_data.append(json_data)
        else:
            video_data = []

        db.close()
    except json.JSONDecodeError:
        video_data = []

    return render_template('allvideos.html', videos=video_data)


@app.route('/stream', methods=['POST', 'GET'])
def stream_video():
    url_base64 = request.args.get('url_base64')  # Retrieve base64-encoded URL
    url = base64.b64decode(url_base64).decode('utf-8')  # Decode the base64 URL
    print(url)
    response = requests.get(url)

    if response.status_code == 200:
        remote_audio_data = response.content
        return Response(response=remote_audio_data, content_type="video/mp4")
    else:
        return "Error fetching remote video", 500


@app.route('/tiktok', methods=['POST', 'GET'])
def get_tiktok_video_url():
    myid = request.args.get('id')
    response = requests.get(
        f'https://api.tiktokv.com/aweme/v1/feed/?aweme_id={myid}')

    myjson = json.loads(response.text)
    videourl = myjson['aweme_list'][0]['video']['play_addr']['url_list'][0]

    return jsonify({"video_url": videourl})


@app.route('/fetchvideosregion', methods=['POST', 'GET'])
def fetch_tiktok_videos_by_region():
    region = request.args.get('region')

    # fetch_and_save_tiktok_data(region=region,priority_region=region,sys_region=region)
    fetch_and_save_tiktok_data_method2(region=region, priority_region=region)

    try:
        with open('jsonresponse.json', 'r', encoding='utf-8') as file:
            video_data = json.load(file)
    except json.JSONDecodeError:
        video_data = []

    db = VideoDatabase()
    db.connect()
    db.create_table()

    for video in video_data:
        video_id = video.get('id', '12345')
        username = video.get('author', {}).get('uniqueId', 'nousername')
        likes = video.get('stats', {}).get('diggCount', 0)
        shares = video.get('stats', {}).get('shareCount', 0)
        plays = video.get('stats', {}).get('playCount', 0)
        thumbnail = video.get('video', {}).get(
            'dynamicCover', 'https://corporate.bestbuy.com/wp-content/uploads/2022/06/Image-Portrait-Placeholder-768x777.jpg')
        description = video.get('desc', 'no description')
        hashtags = ''

        if 'contents' in video and len(video['contents']) > 0:
            for hashtag in video['contents'][0].get('textExtra', []):
                hashtags = str(hashtags) + \
                    str(hashtag.get('hashtagName', '')) + ','

        data = {
            'video_id': video_id,
            'username': username,
            'likes': likes,
            'shares': shares,
            'plays': plays,
            'thumbnail': thumbnail,
            'description': description,
            'hashtags': hashtags,
            'region': region
        }

        db.insert_data(data)

    db.close()

    return jsonify({"message": "done", "status": 200})


@app.template_filter('formatNumber')
def format_number(number):
    if number >= 1e9:
        return f"{number / 1e9:.1f}B"
    elif number >= 1e6:
        return f"{number / 1e6:.1f}M"
    elif number >= 1e3:
        return f"{number / 1e3:.1f}K"
    return str(number)


if __name__ == '__main__':
    app.run(debug=True)
