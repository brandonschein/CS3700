import sys
import socket
import ssl
import os
from urllib.parse import urlparse

# gets all the command line arguements and cuts off the name of the program
info = sys.argv[1:]

# parse the input 
operation = ""
unParsedUrl = ""
local_path = ""
urlFirst = True

if(len(info) == 2):
    operation = info[0]
    unParsedUrl = info[1]
    if("fttps://" not in unParsedUrl):
        print("no url")
elif(len(info) == 3):
    operation = info[0]
    if("fttps://" in info[1]):
        unParsedUrl = info[1]
        local_path = info[2]
    elif("fttps://" in info[2]):
        unParsedUrl = info[2]
        local_path = info[1]
        urlFirst = False
    else:
        print("no url")
else:
    print("wrong number of arguements")

# constant send messages
AUTH_MSG = "AUTH TLS\r\n"
PBSZ_MSG = "PBSZ 0\r\n"
PROT_MSG = "PROT P\r\n"
TYPE_MSG = "TYPE I\r\n"
MODE_MSG = "MODE S\r\n"
STRU_MSG = "STRU F\r\n"
QUIT_MSG = "QUIT\r\n"
PASV_MSG = "PASV\r\n"

# default values set before parsing the input url
hostname = ""
username = ""
password = ""
port = 21
path = "/"

# parse the url
parsedUrl = urlparse(unParsedUrl, scheme = "ftp")
hostname = parsedUrl.hostname
username = parsedUrl.username
password = parsedUrl.password
if(parsedUrl.port != None):
    port = parsedUrl.port
if(parsedUrl.path != ""):
    path = parsedUrl.path

# successfully creates a connection, was tested with print statement below
s = socket.create_connection((hostname, port))
print(s.recv(8192))

# sending the initial authentication message 
s.send(AUTH_MSG.encode())
print(s.recv(8192))

# wrapping the socket in a secure TLS connection
context = ssl.create_default_context()
s = context.wrap_socket(s, server_hostname=hostname)

#sending login/initializing messages
s.send(("USER " + username + "\r\n").encode())
print(s.recv(8192))

s.send(("PASS " + password + "\r\n").encode())
print(s.recv(8192))

s.send(PBSZ_MSG.encode())
print(s.recv(8192))

s.send(PROT_MSG.encode())
print(s.recv(8192))

s.send(TYPE_MSG.encode())
print(s.recv(8192))

s.send(MODE_MSG.encode())
print(s.recv(8192))

s.send(STRU_MSG.encode())
print(s.recv(8192))

if(operation == "ls"):
    # ls <URL>  Print out the directory listing from the FTPS server at the given URL

    # open a data channel 
    s.send(PASV_MSG.encode())
    recieved = s.recv(8192).decode()
    print(recieved)
    split_recieved = recieved.split("(")
    pruning_message = split_recieved[1].split(",")
    ip_address = pruning_message[0] + "." + pruning_message[1] + "." + pruning_message[2] + "." + pruning_message[3]
    port_numbers = [pruning_message[4], pruning_message[5].split(")")[0]]
    port_number = ((int(port_numbers[0]) * 256) + int(port_numbers[1]))
    
    print(ip_address)
    print(port_number)
    
    s.send(("LIST " + path +"\r\n").encode())
    
    data_connection_socket = socket.create_connection((ip_address, port_number))
    context = ssl.create_default_context()
    secure_s = context.wrap_socket(data_connection_socket, server_hostname=hostname)
    print(secure_s.recv(8192).decode())
    secure_s.close()
if(operation == "mkdir"):
    # mkdir <URL>            Create a new directory on the FTPS server at the given URL
    s.send(("MKD " + path + "\r\n").encode())
    print(s.recv(8192).decode())
if(operation == "rm"):
    # rm <URL>               Delete the file on the FTPS server at the given URL
    s.send("DELE " + path + "\r\n")
    print(s.recv(8192))
if(operation == "rmdir"):
    # rmdir <URL>            Delete the directory on the FTPS server at the given URL
    s.send(("RMD " + path + "\r\n").encode())
    print(s.recv(8192).decode())
if(operation == "cp"):
    # cp <ARG1> <ARG2>       Copy the file given by ARG1 to the file given by
    #                        ARG2. If ARG1 is a local file, then ARG2 must be a URL, and vice-versa.
    if(urlFirst):
        s.send(PASV_MSG.encode())
        recieved = s.recv(8192).decode()
        print(recieved)
        split_recieved = recieved.split("(")
        pruning_message = split_recieved[1].split(",")
        ip_address = pruning_message[0] + "." + pruning_message[1] + "." + pruning_message[2] + "." + pruning_message[3]
        port_numbers = [pruning_message[4], pruning_message[5].split(")")[0]]
        port_number = ((int(port_numbers[0]) * 256) + int(port_numbers[1]))
        
        print(ip_address)
        print(port_number)
        
        s.send(("RETR " + path +"\r\n").encode())
        
        data_connection_socket = socket.create_connection((ip_address, port_number))
        context = ssl.create_default_context()
        secure_s = context.wrap_socket(data_connection_socket, server_hostname=hostname)
        contents = secure_s.recv(8192)
        file = open(local_path, "wb")
        file.write(contents)
        file.close()
        secure_s.close()
    else:
        s.send(PASV_MSG.encode())
        recieved = s.recv(8192).decode()
        print(recieved)
        split_recieved = recieved.split("(")
        pruning_message = split_recieved[1].split(",")
        ip_address = pruning_message[0] + "." + pruning_message[1] + "." + pruning_message[2] + "." + pruning_message[3]
        port_numbers = [pruning_message[4], pruning_message[5].split(")")[0]]
        port_number = ((int(port_numbers[0]) * 256) + int(port_numbers[1]))
        
        print(ip_address)
        print(port_number)
        
        s.send(("STOR " + local_path +"\r\n").encode())
        
        
        data_connection_socket = socket.create_connection((ip_address, port_number))
        context = ssl.create_default_context()
        # giving an issue
        secure_s = context.wrap_socket(data_connection_socket, server_hostname=hostname)
        
        file = open(local_path, "rb")
        file_contents = file.read()
        secure_s.send(file_contents)
        secure_s.close()
        file.close()
if(operation == "mv"):
    #mv <ARG1> <ARG2>        Move the file given by ARG1 to the file given by
    #                        ARG2. If ARG1 is a local file, then ARG2 must be a URL, and vice-versa.
    if(urlFirst):
        s.send(PASV_MSG.encode())
        recieved = s.recv(8192).decode()
        print(recieved)
        split_recieved = recieved.split("(")
        pruning_message = split_recieved[1].split(",")
        ip_address = pruning_message[0] + "." + pruning_message[1] + "." + pruning_message[2] + "." + pruning_message[3]
        port_numbers = [pruning_message[4], pruning_message[5].split(")")[0]]
        port_number = ((int(port_numbers[0]) * 256) + int(port_numbers[1]))
        
        print(ip_address)
        print(port_number)
        
        s.send(("RETR " + path +"\r\n").encode())
        
        data_connection_socket = socket.create_connection((ip_address, port_number))
        context = ssl.create_default_context()
        secure_s = context.wrap_socket(data_connection_socket, server_hostname=hostname)
        contents = secure_s.recv(8192)
        file = open(local_path, "wb")
        file.write(contents)
        file.close()
        secure_s.close()
        s.send("DELE " + path + "\r\n")
        print(s.recv(8192).decode())
    else:
        s.send(PASV_MSG.encode())
        recieved = s.recv(8192).decode()
        print(recieved)
        split_recieved = recieved.split("(")
        pruning_message = split_recieved[1].split(",")
        ip_address = pruning_message[0] + "." + pruning_message[1] + "." + pruning_message[2] + "." + pruning_message[3]
        port_numbers = [pruning_message[4], pruning_message[5].split(")")[0]]
        port_number = ((int(port_numbers[0]) * 256) + int(port_numbers[1]))
        
        print(ip_address)
        print(port_number)
        
        s.send(("STOR " + path +"\r\n").encode())
        print("here")
        # giving an issue
        data_connection_socket = socket.create_connection((ip_address, port_number))
        
        context = ssl.create_default_context()
        
        secure_s = context.wrap_socket(data_connection_socket, server_hostname=hostname)
        contents = secure_s.recv(8192).decode()
        
        file = open(local_path, "rb")
        file_contents = file.read()
        secure_s.send(file_contents.encode())
        secure_s.close()
        file.close()
        os.remove(local_path)

s.send(QUIT_MSG.encode())
print(s.recv(8192))
