import time
import re
import flask
import flask_cors
import requests
import threading

# Use a session to help trick Google into not blocking me :(
req_sess = requests.session()

app = flask.Flask(__name__)
cors = flask_cors.CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/wfrWHvc5GatzGTP3yuLu')
@flask_cors.cross_origin()
def wfrWHvc5GatzGTP3yuLu():
  """ Return number of hits on google for given query """
  q = flask.request.args.get('q')
  errdict = {"type": "error"}
  if q is None:
    return flask.jsonify(errdict)
  else:
    hitcount = hits(q)
    if hitcount is None:
      return flask.jsonify(errdict)
    return flask.jsonify({"type": "success", "hitcount": hitcount})

def hits(query):
  text = google(query)
  if not text:
    return
  reg = "About (?P<hits>[0-9,]*) results"
  res = re.search(reg, text)
  if res is None:
    return
  return int(''.join(filter(lambda c: c in '1234567890', res['hits'])))

search_lock = threading.Lock()
last_search_time = 0
wait_time = 2.5  # wait time [s] between google requests
def google(query):
  global last_search_time

  search_lock.acquire()
  time.sleep(max(0, wait_time - (time.time() - last_search_time)))
  response = req_sess.get("http://google.com/search?q=" + query)
  last_search_time = time.time()
  search_lock.release()

  if not hasattr(response, 'text'):
    return
  return response.text

if __name__ == "__main__":
  app.run(host='0.0.0.0')