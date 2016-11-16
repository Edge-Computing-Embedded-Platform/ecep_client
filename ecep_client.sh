#!/bin/sh


# Change the parameters according to the configuration of wamp server, the port number should be same as the server
ip="ec2-52-39-130-106.us-west-2.compute.amazonaws.com"
port="8096"
realm="realm1"
path="/home/chinmayi/"
# Do not edit the below line
python -m ecep_endNode.ecep_wampClient.deviceRegister $ip $port $realm $path
