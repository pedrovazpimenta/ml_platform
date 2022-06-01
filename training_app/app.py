import datetime
import flask
import logging
import datetime
import json
import imp
import hashlib
import time
import concurrent.futures

file = logging.handlers.RotatingFileHandler(filename="app.log", maxBytes=50000)
imp.reload(logging)
logging.basicConfig(level=logging.INFO, handlers=[file])
logging.getLogger().setLevel(logging.INFO)


def logger(message, run_hash, service="training_app"):
    timestamp = datetime.datetime.utcnow().isoformat()
    log_dict = {
        "message": message,
        "timestamp": timestamp,
        "run_hash": run_hash,
        "service": service,
    }
    log_message = json.dumps(log_dict)
    logging.log(logging.INFO, f"{log_message}")
    print(log_message)


def get_run_hash():
    hash_seed = str(time.time()).encode("utf-8")
    run_hash = hashlib.md5()
    run_hash.update(hash_seed)
    return run_hash.hexdigest()


application = flask.Flask(__name__)


@application.before_first_request
def initialize():
    application.poolExecutor = concurrent.futures.ProcessPoolExecutor(
        max_workers=2
    )
    logger("APPLICATION_STARTED", "")


@application.route("/train", endpoint="1", methods=["POST"])
def train():
    run_hash = get_run_hash()

    parameters = {
        "training_dataset": flask.request.form.get("training_dataset", ""),
    }
    try:
        application.poolExecutor.submit(print, parameters["training_dataset"])
        logger("TRAINING_STARTED", run_hash)
    except Exception as e:
        logger("ERROR: " + str(e), run_hash)

    responde_dict = {
        "message": "END_REQUEST",
        "timestamp": datetime.datetime.utcnow().isoformat(),
        "run_hash": run_hash,
        "service": "training_app",
    }
    return flask.make_response(flask.jsonify(responde_dict), 200)


if __name__ == "__main__":
    application.run()
