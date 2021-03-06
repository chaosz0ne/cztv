import os
import json
import socket
import subprocess

UDP_IP_ADDRESS = "127.0.0.1"
UDP_PORT_NO = 7123
serverSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serverSock.bind((UDP_IP_ADDRESS, UDP_PORT_NO))


SIDS = ('S1', 'S2', 'S3')
mplayers = dict(S1=None, S2=None, S3=None)

import io
PIPE = io.StringIO()

SOUNDS = dict(blubber='/home/kombinat/player/test.mp3', short='/home/kombinat/player/cough.mp3')



#for sid in SIDS:
#    if os.path.isdir(f'/tmp/mplayerctrl{sid}'):
#        os.unlink(f'/tmp/mplayerctrl{sid}')
#    os.mkfifo(f'/tmp/mplayerctrl{sid}')
    

def _get_current():
    res = []
    with open('play.json') as playconf:
        for screen_id, filepath in json.loads(playconf.read()).items():
            if filepath == '':
                continue
            res.append((screen_id, filepath))
    return res


def _mplayer_command(screen_id, mplayercmd):
    with open(f'/tmp/mplayerctrl{screen_id}', 'a') as ctrl:
        ctrl.write(mplayercmd)


def get_time():
    for screen_id, filepath in _get_current():
        _mplayer_command(screen_id, 'pausing_keep_force get_time_pos\n')

def load_current():
    for screen_id, filepath in _get_current():
        cmd = f'loadfile storage/{filepath}\npause\npausing_keep get_time_length\n'
        _mplayer_command(screen_id, cmd)
        _mplayer_command(screen_id, f'pausing_keep_force run "echo ${{pause}} > {screen_id}_pause"\n')

def play_sound(cmd):
    cmd = cmd[6:]
    if cmd.startswith('kill'):
    	snd = cmd[5:]
    	os.system(f'kill -9 `cat {snd}.pid`')
    	os.unlink(f'{snd}.pid')
    	return
    cmd, addr = cmd.split('#') 
    bank, btn = addr.split('_')
    os.system(f'./play_sound.sh {SOUNDS[cmd]} {cmd} {int(bank)} {int(btn)} &')



def play_current():
    for screen_id, filepath in _get_current():
        _mplayer_command(screen_id, f'pause\n')
        _mplayer_command(screen_id, f'pausing_keep_force run "echo ${{pause}} > {screen_id}_pause"\n')


def stop_current():
    for screen_id, filepath in _get_current():
        with open(f'/tmp/mplayerctrl{screen_id}', 'a') as ctrl:
            ctrl.write("stop\n")
        os.unlink(f'curtime_{screen_id}.json')

def ninja(cmd):
    for sid in SIDS:
        if f'{sid}' in cmd:
            scr = sid
            break
    scr = scr[1]
    if cmd.endswith('start'):
        os.system(f'./start_ninja.sh {scr}')
    elif cmd.endswith('stop'):
        os.system(f'./stop_ninja.sh {scr}')


while True:
    data, addr = serverSock.recvfrom(1024)
    commands = data.decode("utf8").splitlines()
    for cmd in commands:
        if cmd == 'load_current':
            load_current()
        elif cmd == 'play_current':
            play_current()
        elif cmd == 'stop_current':
            stop_current()        
        elif cmd == 'get_time':
            get_time()
        elif cmd.startswith('sound'):
            play_sound(cmd)
        elif cmd.startswith('ninja'):
            ninja(cmd)
        else:
            print(f"{cmd} not found!")
