#!/bin/sh -l

locust --headless -u 5000 -t 2m -r 200 -f load_testing.py --host=http://localhost:80 --processes 4