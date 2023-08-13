from flask import Flask, render_template, request, jsonify, Response
import requests
import json
import base64

from trending import fetch_and_save_tiktok_data, fetch_and_save_tiktok_data_method2

app = Flask(__name__)



@app.route('/')
def index():
    try:
        with open('jsonresponse.json', 'r', encoding='utf-8') as file:
            video_data = json.load(file)
    except json.JSONDecodeError:
        video_data = []
    return render_template('index.html', videos=video_data)

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
    response = requests.get(f'https://api.tiktokv.com/aweme/v1/feed/?aweme_id={myid}')

    myjson = json.loads(response.text)
    videourl = myjson['aweme_list'][0]['video']['play_addr']['url_list'][0]
    
    return jsonify({"video_url": videourl})


@app.route('/fetchvideosregion', methods=['POST', 'GET'])
def get_tiktok_video_by_region():
    region = request.args.get('region')

    # fetch_and_save_tiktok_data(region=region,priority_region=region,sys_region=region)
    fetch_and_save_tiktok_data_method2(region=region,priority_region=region)
    
    return jsonify({"message": "done","status":200}) 


@app.template_filter('formatNumber')
def format_number( number):
    if number >= 1e9:
        return f"{number / 1e9:.1f}B"
    elif number >= 1e6:
        return f"{number / 1e6:.1f}M"
    elif number >= 1e3:
        return f"{number / 1e3:.1f}K"
    return str(number)


if __name__ == '__main__':
    app.run(debug=True)
