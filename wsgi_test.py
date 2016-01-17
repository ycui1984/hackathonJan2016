#!/usr/bin/env python

import os, sys
sys.path.append("src")
os.environ["HULU_ENV"] = "test"
os.environ["HULU_DC"] = "els"

from app import app as application

if __name__ == '__main__':
    application.run(host='0.0.0.0', debug=True)
