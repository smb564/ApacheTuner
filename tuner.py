import sys
import os

from flask import Flask
from flask import request

app = Flask(__name__)

with open("mpm_prefork.conf") as f:
    config_file = f.read()

@app.route("/setParam")
def getParam():
    config_file_updated = config_file.replace("{{MaxRequestWorkers}}", request.args.get("MaxRequestWorkers"))

    with open("/etc/apache2/mods-available/mpm_prefork.conf", "w") as f:
        f.write(config_file_updated)

    os.system("sudo /etc/init.d/apache2 reload")
    return "Done"


@app.route("/")
def hello():
    return "Hello, Server is runing.."

app.run(host="0.0.0.0", port=5001)