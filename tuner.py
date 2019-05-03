import sys
import os

from flask import Flask
from flask import request

app = Flask(__name__)

@app.route("/setParam")
def getParam():
    config_file = open("/etc/apache2/mods-available/mpm_prefork.conf").read()
    config_file = config_file.replace("{{MaxRequestWorkers}}", request.args.get("MaxRequestWorkers"))

    with open("/etc/apache2/mods-available/mpm_prefork.conf", "w")as f:
        f.write(config_file)

    os.system("sudo /etc/init.d/apache2 reload")
    return True

app.run(port=5001)