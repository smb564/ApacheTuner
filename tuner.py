import sys
import os

from flask import Flask
from flask import request

app = Flask(__name__)

# TODO: We should read the current modul from mods-available
# let's always put mpm_event as the initial one
model = ""
mpmModel("mpm_event")


@app.route("/setParam")
def getParam():
    with open(model + ".conf") as f:
        config_file = f.read()
        
    config_file = config_file.replace("{{MaxRequestWorkers}}", request.args.get("MaxRequestWorkers"))

    with open("/etc/apache2/mods-available/" + model + ".conf", "w") as f:
        f.write(config_file)

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
        os.system("ln -s /etc/apache2/mods-available/" + model + ".conf /etc/apache2/modes-enabled/" + model + ".conf")
        os.system("ln -s /etc/apache2/mods-available/" + model + ".load /etc/apache2/modes-enabled/" + model + ".load")

    else:
        return "Already using the same model"


@app.route("/default")
def setDefault():
    '''
    This does not reset the mpm module type to the default type, but change current module's param to default
    '''
    os.system("cp " + model + ".default.conf /etc/apache2/mods-available/" + model + ".conf")
    return "Done"

    

@app.route("/")
def hello():
    return "Hello, Server is runing.."

app.run(host="0.0.0.0", port=5001)