import socket
import json
import pymongo

dbhost = "localhost"
dbport = 27017
client = pymongo.MongoClient('mongodb://' + dbhost + ':' + str(dbport))
db = client.HoPPS
coll = db.data

def getData(sock):
    BUFF = 4096
    data = ""
    parts = []
    while True:
        part = sock.recv(BUFF)
        if not part:
            break
        parts.append(part)
    return "".join(parts)

srvsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
srvsocket.bind((socket.gethostname(), 4677))
srvsocket.listen(5)
conn, client = srvsocket.accept()
result = getData(conn)
conn.close()
coll.insert_one(json.loads(result))

