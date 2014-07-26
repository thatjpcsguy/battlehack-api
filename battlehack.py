from flask import Flask
from flask import request
from flask import jsonify
from flask import url_for
from flask import render_template
import hashlib
import base64
import os
import PIL
from PIL import Image
from werkzeug.contrib.fixers import ProxyFix

import MySQLdb
import MySQLdb.cursors
from base64 import decodestring
from apns import APNs, Payload

from haversine import haversine

import json
import facebook
import _mysql
import urllib

import math

import sys
import smtplib
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import flask

app = Flask(__name__)
app.debug = True


app.wsgi_app = ProxyFix(app.wsgi_app)


db = MySQLdb.connect(host = "127.0.0.1", user = "sellular", passwd = "lolol1234", db = "sellular", cursorclass=MySQLdb.cursors.DictCursor)
#db = MySQLdb.connect(host = "127.0.0.1", user = "battlehack", passwd = "lolol1234", db = "battlehack", cursorclass=MySQLdb.cursors.DictCursor)
db_cur = db.cursor()


# apns = APNs(use_sandbox=True, cert_file='certs/caricatures_cert.pem', key_file='certs/caricatures_key.pem')


#given current lat and lon and a distance in meters, return the coordinates all listings should be within
def coordinate_bounds(lat, lon, dist):
    RAD = 6378137

    # //Coordinate offsets in radians
    yLat = dist/(RAD*math.cos(float(math.pi)*float(lat/180)))
    yLon = dist/(RAD*math.cos(float(math.pi)*float(lat/180)))

    xLat = -1*dist/(RAD*math.cos(float(math.pi)*float(lat/180)))
    xLon = -1*dist/(RAD*math.cos(float(math.pi)*float(lat/180)))

    return (lat + yLat * 180/math.pi, lat + xLat * 180/math.pi, lon + yLon * 180/math.pi , lon + xLon * 180/math.pi)



@app.route("/")
def hello():
    return render_template('index.html')


@app.route('/nearby/<lat>/<lon>/<dist>', methods=['GET'])
def nearby(lat, lon, dist):
    lat_upper, lat_lower, lon_upper, lon_lower = coordinate_bounds(float(lat), float(lon), float(dist))

    db_cur.execute("SELECT * FROM listings l WHERE status = 'OPEN' AND lat BETWEEN {0} AND {1} AND lon BETWEEN {2} AND {3}".format(min(lat_lower, lat_upper), max(lat_lower, lat_upper), min(lon_lower, lon_upper), max(lon_lower, lon_upper)))
    
    rows = db_cur.fetchall()

    out = {"data":[]}

    for row in rows:
        dist = haversine((float(lat), float(lon)), (float(row['lat']), float(row['lon'])))
        row['dist'] = dist*1000
        out["data"].append(row)


    return jsonify(out)


@app.route('/fetch/<user_id>')
def fetch(user_id):
    db_cur.execute("SELECT * FROM listings l WHERE user_id = '{0}' ORDER BY listing_time DESC".format(user_id))
    
    rows = db_cur.fetchall()

    out = {"data":[]}

    for row in rows:
        dist = haversine((float(lat), float(lon)), (float(row['lat']), float(row['lon'])))
        row['dist'] = dist*1000
        out["data"].append(row)


    return jsonify(out)


@app.route('/img/<path>')
def img(path):
    # send_static_file will guess the correct MIME type
    return app.send_static_file('images/'+path)


@app.route('/listing', methods=['POST'])
def listing():
    listing_info = json.loads(request.form['data'])
    # print listing_info

    #clean up image data
    image_data = listing_info['image_data'].encode('ascii').replace(' ', '+')
    while len(image_data) % 4 != 0:
        image_data += '='
    decoded_data = base64.b64decode(image_data)

    # generate image name
    m = hashlib.sha256()
    m.update(image_data)
    filename = m.hexdigest() + ".png"
    thumbname = m.hexdigest() + "_thumb.png"
    
    # save image to file
    fh = open("static/images/"+filename, "wb")
    fh.write(decoded_data)
    fh.close()

    size = 60, 60
    try:
        im = Image.open("static/images/"+filename)

        # print im.size
        w, h = im.size
        if w > h:
            h1 = 0;
            h2 = h;
            w1 = math.floor((w-h)/2);
            w2 = w1 + h;

        elif h > w:
            w1 = 0;
            w2 = w;
            h1 = math.floor((h-w)/2);
            h2 = h1 + w;

        else:
            h1 = 0;
            h2 = h;
            w1 = 0;
            w2 = w;

        new = im.crop((int(w1), int(h1), int(w2), int(h2)))
        new.thumbnail(size, Image.ANTIALIAS)

        new.save("static/images/"+thumbname)

    except IOError:
        print "cannot create thumbnail for '%s'" % infile

        

    db_cur.execute("INSERT INTO  listings (user_id, lat, lon, title, image_url, thumbnail_url, description, price, status) VALUES (%s, %s, %s, '%s', '%s', '%s', '%s', %s, 'OPEN')" % (listing_info['FBUser']['id'], listing_info['lat'], listing_info['long'], listing_info['title_data'], "http://sellular.co/img/"+filename, "http://sellular.co/img/"+thumbname, listing_info['desc'], listing_info['price']))
    db.commit()
    return jsonify(status=True)



@app.route('/users', methods=['POST'])
def users():
    if request.method == 'POST':
        user_info = json.loads(request.form['data'])
        db_cur.execute("INSERT INTO users (user_id, first_name, last_name, email) VALUES ('%s', '%s', '%s', '%s') ON DUPLICATE KEY UPDATE last_login_time = NOW()" % (user_info['id'], user_info['first_name'], user_info['last_name'], user_info['email']))
        db_cur.execute("INSERT INTO devices (user_id, token) VALUES ('%s', '%s') ON DUPLICATE KEY UPDATE token = '%s'" % (user_info['id'], user_info['device_token'], user_info['device_token']))
        return jsonify(status=True)
    elif request.method == 'GET':
        return jsonify(status=False)
    else:
        return jsonify(status=False)



if __name__ == "__main__":

    app.run(host='0.0.0.0')
