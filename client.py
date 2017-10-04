import json
import socket
import sys
import os
import plistlib
from subprocess import Popen, PIPE

def getDate(data):
    date = Popen(['date', "+%Y%m%d%H%M%S"], stdout=PIPE)
    data['date'] = date.communicate()[0].rstrip()
    
def getIP(data):
    p1 = Popen(['ifconfig'], stdout=PIPE)
    p2 = Popen(['grep', 'inet '], stdout=PIPE, stdin=p1.stdout)
    p3 = Popen(['grep', '-Fv', '127.0.0.1'], stdout=PIPE, stdin=p2.stdout)
    p4 = Popen(['awk',"{print $2}"], stdout=PIPE, stdin=p3.stdout)
    data['IP'] = p4.communicate()[0].rstrip()
    
def getHost(data):
    host = Popen(['hostname'], stdout=PIPE, stderr=PIPE)
    data['host'] = host.communicate()[0].rstrip()

def getProcs(data):
    procs = Popen(['ps', 'auxc'], stdout=PIPE, stderr=PIPE)
    proc = procs.communicate()[0].split('\n')
    x = 1
    while x < (len(proc)-1):    
        process = {}
        dictname = "proc%d" % x
        line2 = proc[x].split()
        process['user'] = line2[0]
        process['proc'] = line2[10]
        process['time'] = line2[9]
        process['cpu%'] = line2[2]
        data[dictname] = process
        process.clear
        x += 1

def getConns(data):
    conns = Popen(['netstat', '-f', 'inet', '-p', 'tcp'], bufsize=1, universal_newlines=True, stdout=PIPE, stderr=PIPE)

    out = conns.communicate()[0].split('\n')  
    i = 2
    while i < (len(out)-1):
        conn = {}
        dictname2 = "net%d" % i
        line = out[i].split()
        conn['remoteIP'] = line[4]
        conn['status'] = line[5]
        data[dictname2] = conn
        conn.clear
        i += 1

def main():
    if len(sys.argv) > 1:
        confile = sys.argv[1]
    else:
        confile = "hopps.conf"
    
    try:    
        conf = open(confile, "r")
        server = conf.readline().strip()
        port = int(conf.readline().strip())
        interval = int(conf.readline().strip())
    except IOError:
        print("FILE NOT FOUND!")
        
    if sys.platform == 'darwin':
        plfile = open("/Library/LaunchAgents/dadsec.hopps.plist", "w")
        pl = dict(
            label = "dadsec.hopps",
            ProgramArguments = "/Library/Application Support/HoPPS/client.py",
            KeepAlive = dict(NetworkState = "true"),
            StartInterval = interval
        )
        plistlib.writePlist(pl, plfile)
    elif sys.platform == 'linux':
        cron = Popen(['crontab', '-l'])
        mins = interval/60
        cronstring = "*/", mins, " * * * * /usr/local/bin/client.py"
        cron += cronstring
        Popen(['crontab', cron])
        
    data={}

    getHost(data) 
    getProcs(data)
    getDate(data)
    getIP(data)
    getConns(data)
 
    export = json.dumps(data)
    #read server ip and port from config file
    svraddr = (server, port)
    print export
    svrconn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    svrconn.connect(svraddr)
    svrconn.send(export)
    svrconn.close()
    #print export
    #print server
    #print interval
  
if __name__ == '__main__':
    main()


    


