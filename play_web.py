import time
import os
from flask import Flask, render_template, request, make_response, redirect
import json
import random
import socket

app = Flask("chaoszone-tv-media")

APPROOT = '/'

class ReverseProxied(object):
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        script_name = environ.get('HTTP_X_SCRIPT_NAME', '')
        if script_name:
            environ['SCRIPT_NAME'] = script_name
            path_info = environ['PATH_INFO']
            if path_info.startswith(script_name):
                environ['PATH_INFO'] = path_info[len(script_name):]

        scheme = environ.get('HTTP_X_SCHEME', '')
        if scheme:
            environ['wsgi.url_scheme'] = scheme
        return self.app(environ, start_response)

app.wsgi_app = ReverseProxied(app.wsgi_app)




def to_dict(args):
    outdict = {}
    for key, val in args.items():
        outdict[key] = val
    return outdict
    
    
def list_files():
    filelist = os.listdir('storage/')
    return sorted(filelist)


def get_ninja_secrets():
    secrets = dict()
    for scr in ['S1', 'S2', 'S3']:
        with open(f'{scr}_ninjasecret') as infile:
            secret = infile.read()
        secrets[scr] = secret
    return secrets
    
    
def regenerate_secret(scr):
    new_secret = ''
    for i in range(24):
    	new_secret += random.choice('cHaOsZoNEtV')
    with open(f'{scr}_ninjasecret', 'w') as secfile:
        secfile.write(new_secret)


def request_time():
    byte_message = bytes("get_time", "utf-8")
    with socket.socket(socket. AF_INET, socket. SOCK_DGRAM) as opened_socket:
        opened_socket.sendto(byte_message, ("127.0.0.1", 7123))
    time.sleep(0.1)


@app.route('/get_time.json')
def get_time():
    request_time()
    res = {}
    for sid in ('S1', 'S2', 'S3'):
        if not os.path.isfile(f'curtime_{sid}.json'):
            continue
        with open(f'curtime_{sid}.json') as curtime:
            res[sid] = json.loads(curtime.read())
        if not os.path.isfile(f'{sid}_pause'):
            continue
        with open(f'{sid}_pause') as pause:
            res[sid]['pause'] = pause.read().strip()

    r = make_response(json.dumps(res))
    r.mimetype = 'application/json'
    return r


@app.route('/media.html')
def media():
    edit = False
    data = to_dict(request.args)
    if 'edit' in data:
        edit = True
    filelist = list_files()
    secrets = get_ninja_secrets()
    return render_template(
        'media.html', 
        filelist=filelist,
        secrets=secrets,
        screens=['S1', 'S2','S3'],
        edit=edit,
        approot=APPROOT)
        

@app.route('/obs_multiview.html')
def obs_multiview():
    return render_template(
        'obs_multiview.html', 
        approot=APPROOT)
        
        

@app.route('/programm.html')
def atem_multiview():
    return render_template(
        'programm.html', 
        approot=APPROOT)
        
@app.route('/get_media')
def get_media():
    with open('play.json') as playfile:
        jsn = playfile.read()
    r = make_response(jsn)
    r.mimetype = 'application/json'
    return r
    
@app.route('/set_media')
def set_media():
    filelist = list_files()
    to_set = to_dict(request.args)
    for s in ('S1', 'S2', 'S3'):
        if to_set[s] not in filelist:
            to_set[s] = ''
    with open('play.json', 'w') as playfile:
        playfile.write(json.dumps(to_set))
    return redirect('/media.html')
        
@app.route('/regenerate_ninja_link')
def regenerate_ninja_link():
    scr = to_dict(request.args).get('scr')
    regenerate_secret(scr)
    return redirect('/media.html')
      
        
 
