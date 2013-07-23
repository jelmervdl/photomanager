#!/bin/sh

coffee --watch --compile --bare --map --output ./static/lib ./static/lib/app.coffee &

/usr/local/bin/python2.7 ./server.py
