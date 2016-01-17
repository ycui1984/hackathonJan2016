from flask import request, make_response, render_template
from flask import Flask
from flask import Response
from db import get_basic_client

from config import setup_logging, track_stats, setup_sso
#from hpc.sso.flask_client import exempt_from_sso

import logging
import requests
import endpoints

setup_logging()
app = Flask(__name__)
app.debug = True
app.db_client = get_basic_client()

hulu_sso = setup_sso(app)

logger = logging.getLogger(__name__)


@app.route('/')
@track_stats.timed("ResponseTimeByEndpoint.index")
def index():
    return render_template('index.html')

@app.route('/static/<path:path>')
@track_stats.timed("ResponseTimeByEndpoint.static_proxy")
def static_proxy(path):
    return app.send_static_file(path)



@app.route("/current_user")
@track_stats.timed("ResponseTimeByEndpoint.current_user")
def current_user():
    user = request.hulu_sso_user
    return jsonify(user)

@app.route("/health_check")
#@exempt_from_sso
@track_stats.timed("ResponseTimeByEndpoint.health_check")
def health_check():
    return Response("OK", content_type="text/plain")

#/convert_video?videoname=<name>&frames=<frames>
@app.route('/convert_video')
@track_stats.timed("ResponseTimeByEndpoint.convert_video")
def convert_video():
    video_name, frames = request.args.get('videoname'), request.args.get('frames')
    if video_name == None or frames == None:
        raise Exception("video or frames cannot be none")
    try:
        frames = int(frames)
    except:
        raise Exception("frames are not number")

    print video_name, frames
    endpoints.convert_one_video(video_name, frames)
    return Response("OK", content_type="text/plain")

#/publish_video?videoname=<name>
@app.route("/publish_video")
@track_stats.timed("ResponseTimeByEndpoint.publish_video")
def publish_video():
    video_name = request.args.get('videoname')
    if video_name == None:
        raise Exception("video cannot be none")
    endpoints.publish_one_video(video_name)
    return Response("OK", content_type="text/plain")

### Your Buisness Logic ###

@app.route("/vote/<key>")
@track_stats.timed("ResponseTimeByEndpoint.vote")
def vote(key):
    app.db_client.incrVote(key)
    result = app.db_client.getVote(key)
    return Response(result, content_type="text/plain")


@app.route("/clear", methods=["POST"])
@track_stats.timed("ResponseTimeByEndpoint.clear")
def clear():
    key = request.form['key']
    app.db_client.clearVote(key)
    return Response("OK", content_type="text/plain")


@app.route("/proxy_hulu")
@track_stats.timed("ResponseTimeByEndpoint.test_hulu")
def test_hulu():
    resp = requests.get("http://www.hulu.com")
    return Response(str(resp.status_code), content_type="text/plain")



### Necessary Flask Setup ###

from hpc.requeststore import setup_tracking_id, get_tracking_id, set_trace

@app.before_request
def before_request():
    setup_tracking_id(request.headers.get('Tracking-Id', None))

@app.errorhandler(Exception)
def handle_exception(ex):
    logger.exception("Unhandled Exception: %s" % ex)
    return make_response("Server Error", 500, {'Content-Type': 'text/plain'})

@app.after_request
def apply_tracking_id(response):
    response.headers["Tracking-ID"] = get_tracking_id()
    return response

### Debugging Endpoints ###

@app.route("/test_fail")
@track_stats.timed("ResponseTimeByEndpoint.test_fail")
def test_fail():
    raise Exception("manual-fail-test")

@app.route("/test_environ_logging")
@track_stats.timed("ResponseTimeByEndpoint.test_environ_logging")
def test_environ_logging():
    set_trace({"user_id" : 1, "value" : 2})
    logger.error("Test Logging Environ")
    return Response("OK", content_type="text/plain")
