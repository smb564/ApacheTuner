# ApacheTuner

This Flask REST server is used to tune/change parameter values of Apache web server in an online manner. That is, we can change the configuration (as of now only the MaxRequestWorkers and KeepAliveTimeout) without interrupting the service of these servers. However, we noticed that there is a significant perfomance drop (as it creates new processes with the new configuration) when the graceful reload signal is sent.


## Usage

The souce code is simple enough to be self-explanatory. You just have to install flask (using pip) and just run the python script. You can find the REST end points by looking at the source code.
