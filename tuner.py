import sys

param_count = len(sys.argv[1:])

assert param_count%2==0

config_file = open("/etc/apache2/apache2.conf").read()

params = {
    "MinSpareServers" : 5,
    "MaxSpareServers" : 10,
    "MaxRequestWorkers" : 256
}

for i in xrange(0, param_count, 2):
    params[sys.argv[i+1]] = str(sys.argv[i+2])

for param in params:
    config_file = config_file.replace("{{" + param + "}}", params[param])

with open("test.conf", "w")as f:
    f.write(config_file)
