import sys
import os

from flask import Flask
from flask import request

app = Flask(__name__)


@app.route("/setParam")
def getParam():
    with open(model + ".conf") as f:
        config_file = f.read()

    max_request_workers = 256
    min_spare_servers = 5
    max_spare_servers = 10

    if "MaxRequestWorkers" in request.args:
        max_request_workers = request.args.get("MaxRequestWorkers")

    if "MinSpareServers" in request.args:
        min_spare_servers = request.args.get("MinSpareServers")
    
    if "MaxSpareServers" in request.args:
        max_spare_servers = request.args.get("MaxSpareServers")

    config_file = config_file.replace("{{MaxRequestWorkers}}", str(max_request_workers))
    config_file = config_file.replace("{{MinSpareServers}}", str(min_spare_servers))
    config_file = config_file.replace("{{MaxSpareServers}}", str(max_spare_servers))

    with open("/etc/apache2/mods-available/" + model + ".conf", "w") as f:
            f.write(config_file)
    
    # check if keepAliveTimeout param is passed
    if "KeepAliveTimeout" in request.args:
        with open("apache2.conf") as f:
            apache2conf = f.read()
        apache2conf = apache2conf.replace("{{KeepAliveTimeout}}", request.args.get("KeepAliveTimeout"))

        with open("/etc/apache2/apache2.conf", "w") as f:
            f.write(apache2conf)

    os.system("sudo /etc/init.d/apache2 reload")
    return "Done"


@app.route("/setModel")
def setModel():
    return mpmModel(request.args.get("model"))


def mpmModel(new_model):
    global model
    if not new_model in ["mpm_prefork", "mpm_event", "mpm_worker"]:
        return "False"

    if model!=new_model:
        model = new_model
        # load default confs to the correct folder
        setDefault()

        # update the symbolic links in mods-enabled
        os.system("rm /etc/apache2/mods-enabled/mpm_*.*")
        os.system("ln -s /etc/apache2/mods-available/" + model + ".conf /etc/apache2/mods-enabled/" + model + ".conf")
        os.system("ln -s /etc/apache2/mods-available/" + model + ".load /etc/apache2/mods-enabled/" + model + ".load")

        return "Done"
    else:
        setDefault()
        return "Already using the same model"


@app.route("/default")
def setDefault():
    '''
    This does not reset the mpm module type to the default type, but change current module's param to default
    '''
    os.system("cp " + model + ".default.conf /etc/apache2/mods-available/" + model + ".conf")
    os.system("cp apache2.default.conf /etc/apache2/apache2.conf")
    return "Done"


@app.route("/reload")
def reload():
    os.system("sudo /etc/init.d/apache2 reload")
    return "Done"

@app.route("/")
def hello():
    return "Hello, Server is runing.."


# TODO: We should read the current modul from mods-available
# let's always put mpm_prefork as the initial one (rather than reading the existing one)
model = ""
mpmModel("mpm_prefork")

app.run(host="0.0.0.0", port=5001)
