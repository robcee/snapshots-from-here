# -*- coding: utf-8 -*-
import os
import simplejson as json
import time

from httplib2 import Http
from urllib import urlencode

from flask import (Flask, jsonify, redirect,
     render_template, request, session, url_for)

import settings

from helper import *
from snappy import Snappy

app = Flask(__name__)
app.secret_key = settings.SESSION_SECRET

h = Http()
snappy = Snappy()


@app.route('/', methods=['GET'])
def main():
    """Default landing page"""
    return render_template('index.html')


@app.route('/your_snapshots', methods=['GET'])
@authenticated
def your_snapshots():
    """Your snapshots"""
    return render_template('your_snapshots.html')


@app.route('/set_email', methods=['POST'])
def set_email():
    """Verify via BrowserID and upon success, set
    the email for the user unless it already
    exists and return the token.
    """
    bid_fields = {'assertion': request.form['bid_assertion'],
                  'audience': settings.DOMAIN}
    headers = {'Content-type': 'application/x-www-form-urlencoded'}
    h.disable_ssl_certificate_validation=True
    resp, content = h.request('https://browserid.org/verify',
                              'POST',
                              body=urlencode(bid_fields),
                              headers=headers)
    bid_data = json.loads(content)
    if bid_data['status'] == 'okay' and bid_data['email']:
        # authentication verified, now get/create the
        # snappy email token
        snappy.get_or_create_email(bid_data['email'])
        session['snapshots_token'] = snappy.token
        session['snapshots_email'] = bid_data['email']
    return redirect(url_for('your_snapshots'))


@app.route('/upload', methods=['POST'])
@authenticated
def upload():
    """Upload a photo"""
    return redirect(url_for('snapshot'))


@app.route('/snapshot', methods=['GET'])
@authenticated
def snapshot():
    """Your snapshot"""
    # TODO: Add upload call to snappy
    return render_template('snapshot.html')


@app.route('/logout', methods=['GET'])
def logout():
    """Log the user out"""
    session['snapshots_email'] = None
    return redirect(url_for('main'))


if __name__ == '__main__':
    app.debug = settings.DEBUG
    app.env = 'dev'
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
