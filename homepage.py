import urllib.request, json 
import subprocess
from json2html import *
from os import listdir
from os.path import isfile, join

class Page:
    def __init__(self, handler, body=''):
        self.handler = handler
        self.handler.send_response(200)
        self.handler.send_header("Content-type", "text/html")
        self.handler.end_headers()

        self.refreshDetails()

        if body == 'Stop':
            print('Requesting to close all Wireguard connection')
            subprocess.check_output('wg-quick down /tmp/wg.conf', shell=True)
            subprocess.check_output('/app/stop.sh', shell=True)
        elif body != '' and body != self.connection:
            print('Requesting a new connection. Was set to ' + self.connection + ' now requested ' + body)
            if self.connection != '':
                subprocess.check_output('wg-quick down /tmp/wg.conf && cp /etc/wireguard/' + body + '.conf /tmp/wg.conf && wg-quick up /tmp/wg.conf', shell=True)
            else:
                subprocess.check_output('cp /etc/wireguard/' + body + '.conf /tmp/wg.conf && wg-quick up /tmp/wg.conf', shell=True)
                subprocess.check_output('/app/start.sh', shell=True)

        self.onlyfiles = [f for f in listdir('/etc/wireguard') if isfile(join('/etc/wireguard', f))]
        self.refreshDetails()

    def refreshDetails(self):
        bashCommand = 'wg'
        process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
        boutput, error = process.communicate()

        wg=boutput.decode('ascii')
        self.wgDict={}
        self.connection=''
        for line in wg.split('\n'):
            if ':' in line:
                key,value = line.split(': ')
                self.wgDict[key.strip()] = value.strip()
        if len(self.wgDict)>0:
            bashCommand = 'basename $(grep -H "' + self.wgDict['peer'] + '" /etc/wireguard/* | cut -d: -f1 | head -1) .conf'
            self.connection=subprocess.check_output(bashCommand, shell=True).decode('ascii').split('\n')[0]

    def print(self):
        output = '''
<html>
  <head>
    <meta name="viewport" content="width=device-width,initial-scale=1.0,maximum-scale=1.0,user-scalable=0" />
    <meta name="apple-mobile-web-app-capable" content="yes" />
    <meta name="apple-mobile-web-app-title" content="Wireguard">

    <link href="icon/apple-touch-icon.png" rel="apple-touch-icon" />
    <link href="icon/apple-touch-icon-76x76.png" rel="apple-touch-icon" sizes="76x76" />
    <link href="icon/apple-touch-icon-120x120.png" rel="apple-touch-icon" sizes="120x120" />
    <link href="icon/apple-touch-icon-152x152.png" rel="apple-touch-icon" sizes="152x152" />
    <link href="icon/apple-touch-icon-180x180.png" rel="apple-touch-icon" sizes="180x180" />
    <link href="icon/icon-hires.png" rel="icon" sizes="192x192" />
    <link href="icon/icon-normal.png" rel="icon" sizes="128x128" />
  </head>
  <body>
    <div id="result"></div>
    <form action='' method='post'>
'''
        for f in self.onlyfiles:
            if '.conf' in f:
                f = f.split('.')[0]
                output += "<button name='submit' value='" + f + "'>" + f + "</button>"
        output += '''
      <button name='submit' value='Stop'>Stop</button>
    </form>
'''

        if self.connection != '':
            output += 'Wireguard is currently connected using the connection: ' + self.connection + '<br />'
            output += '<p>Latest handshake: ' + self.wgDict['latest handshake'] + '<br />'
            output += 'Usage: ' + self.wgDict['transfer'] + '</p>'
        else:
            output += 'There is currently no connection open, you need to start one...'
        try:
            with urllib.request.urlopen("http://ipinfo.io") as url:
                data = json.loads(url.read().decode())
                output += json2html.convert(json=data)
        except:
            print("An exception occured while trying to connect to ipinfo...")
        output += '''
  </body>
</html>
'''
        self.handler.wfile.write(output.encode(encoding='utf8'))
