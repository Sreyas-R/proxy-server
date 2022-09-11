from decimal import MAX_EMAX
from logging.config import listen
import socket ,sys
from _thread import *

try:
    listening_port = int(input("[*] Enter Listening Port Number:"))
except KeyboardInterrupt:
    print("\n User requested an Interrupt")
    print("Application Exiting...")
    sys.exit()

max_conn =5
buffer_size = 8192

def start():
    try:
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM) #initiate socket
        s.bind('',listening_port) #Biind socket for listening
        s.listen(max_conn)  #Starts listening for connections

        print("Initializing Sockets ... Done")
        print("Sockets binded successfully")
        print("Server started successfully")

    except Exception as e:
        print("Unable to initialize socket")
        sys.exit(2)
    
    while 1:
        try:
            conn, addr = s.accept()
            data = conn.recv(buffer_size)
            start_new_thread(conn_string, (conn,data,addr))
        except KeyboardInterrupt:
            s.close()
            print("Proxy server shutting down")
            sys.exit(1)
    s.close()

def conn_string(conn,data,addr):

    try:
        first_line = data.split('\n')[0]
        url = first_line.split(' ')[1]

        http_pos = url.find("://")

        if(http_pos== -1):
            temp = url
        else:
            temp = url[(http_pos+3):]
        
        port_pos = temp.find(":")

        webserver_pos = temp.find("/")

        if(webserver_pos==-1):
            webserver_pos= len(temp)

        webserver = ""
        port =-1
        if(port_pos==-1 or webserver_pos <port_pos):
            port = 80
            webserver = temp[:webserver_pos]
        else:
            port = int((temp[(port_pos+1):])[:webserver_pos-port_pos-1])
            webserver = temp[:port_pos]

            proxy_server(webserver,port,conn,addr,data)
    except Exception as e:
        pass

def proxy_server(webserver, port, conn, data , addr):
    try:
        s =socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host,port))
        s.send(data)

        while 1:
            reply = s.recv(buffer_size)

            if(len(reply)>0):
                conn.send(reply)
                dar = float(len(reply))
                dat= float(dar/1024)
                dar = "%.3s" % (str(dar))
                dar = "%s KB" % (dar)
                print("request done")

            else:
                break

        s.close()
        conn.close()
    except socket.error (value,message):
        s.close()
        conn.close()
        sys.exit(1)

start()