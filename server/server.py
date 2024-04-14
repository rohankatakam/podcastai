from flask import Flask, jsonify, request
from flask_cors import CORS
from summarizer import getInsights

app = Flask(__name__)
CORS(app=app)

@app.route('/hello/', methods=['GET', 'POST'])
def welcome():
    return "Hello World!"

@app.route('/api/getinsights/', methods=['GET', 'POST'])
def testa():
    example = request.args.get('example')
    # url = request.args.get('url')

    examples = {
        "1": {
            "title" : "Inside the Department of Defense and its Vision for the Future",
            "url" : "https://pdst.fm/e/chtbl.com/track/85G57/cdn.simplecast.com/audio/3f86df7b-51c6-4101-88a2-550dba782de8/episodes/c1b0c6ac-e9f4-400a-92ee-3ea247cb0492/audio/1e7f869f-5f1e-4715-9a19-b1a7738981b9/default_tc.mp3"
        },
        "2": {
            "title" : "The Real Price of Healthcare with Mark Cuban",
            "url" : "https://pdst.fm/e/chtbl.com/track/85G57/cdn.simplecast.com/audio/3f86df7b-51c6-4101-88a2-550dba782de8/episodes/bba39c24-94d1-44d5-9539-878fa940030e/audio/fd97dd54-954f-450d-89a1-2f3ddaff96bd/default_tc.mp3"
        },
        "3": {
            "title" : "Building AI Models Faster And Cheaper Than You Think | Lightcone Podcast",
            "url" : "https://d3ctxlq1ktw2nl.cloudfront.net/staging/2024-2-28/372463304-44100-2-3ab3c3af139f4.mp3"
        }
    }
    
    return jsonify(getInsights(examples[example]["title"], examples[example]["url"]))


if __name__ == '__main__':
    app.run(debug=True, port=8080)