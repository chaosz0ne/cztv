import subprocess
import sys
import json

screen_mapping = dict(S1='1', S2='2', S3='3')

scr = sys.argv[1]

info = dict()


def dump_info(info):
    with open(f'curtime_{scr}.json', 'w') as curtime:
        curtime.write(json.dumps(info))


def execute(command):
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    # Poll process for new output until finished
    for line in iter(process.stdout.readline, ""):
        line = line.decode('utf8')
        print(line)
        if line.startswith('ANS_TIME_POSITION'):
            info['elapsed'] = float(line[18:].strip())
            dump_info(info)
        elif line.startswith('ANS_LENGTH'):
            info['length'] = float(line[11:].strip())
            dump_info(info)


    process.wait()
    exitCode = process.returncode

    if (exitCode == 0):
        return 1
    else:
        raise Exception(command, exitCode, output)



execute([f'mplayer -xineramascreen {screen_mapping[scr]} -fs -idle -quiet -slave -input file=/tmp/mplayerctrl{scr}'])
