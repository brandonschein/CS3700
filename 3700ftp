#!/usr/bin/python3

# packages used to complete program
import sys
import socket
import ssl
import os
from urllib.parse import urlparse

# gets all the command line arguements and cuts off the name of the program 
info = sys.argv[1:]

# sets up variable defaults for keeping the info of the command line arguements
operation = ""
unParsedUrl = ""
local = ""
urlFirst = True

# parsing the info from the command line
# if the length of the info is 2, the first parameter must be a url as the protocol always calls for a url, if there is no url
# let the user know
if(len(info) == 2):
    operation = info[0]
    unParsedUrl = info[1]
    if("fttps://" not in unParsedUrl):
        print("no url")
# if the length of the info is 3, check to see which of the parameters is the url, if neither are urls, let the user know
elif(len(info) == 3):
    operation = info[0]
    if("fttps://" in info[1]):
        unParsedUrl = info[1]
        local = info[2]
    elif("fttps://" in info[2]):
        unParsedUrl = info[2]
        local = info[1]
        urlFirst = False
    else:
        print("no url")
# if there are more or less arguements, the user has inputed incorrectly as there are only 1 or 2 parameters given with any command
else:
    print("wrong number of arguements")

# defining constant send messages to be used in intializing connection to the server and the environment of the server 
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
recv_message_initial = s.recv(8192)
#print((recv_message_initial).decode())

# sending the initial authentication message 
s.send(AUTH_MSG.encode())
recv_message_auth = s.recv(8192)
#print((recv_message_auth).decode())

# wrapping the socket in a secure TLS connection
context = ssl.create_default_context()
s = context.wrap_socket(s, server_hostname=hostname)

#sending login and initializing environment messages below
s.send(("USER " + username + "\r\n").encode())
recv_user_msg = s.recv(8192)
# print((recv_usr_msg).decode())

s.send(("PASS " + password + "\r\n").encode())
recv_pass_msg = s.recv(8192)
#print(recv_pass_msg.decode())

s.send(PBSZ_MSG.encode())
recv_pbsz_msg = s.recv(8192)
#print(recv_pbsz_msg.decode())

s.send(PROT_MSG.encode())
recv_prot_msg = s.recv(8192)
#print(recv_prot_msg.decode())

s.send(TYPE_MSG.encode())
recv_type_msg = s.recv(8192)
#print(recv_type_msg.decode())

s.send(MODE_MSG.encode())
recv_mode_msg = s.recv(8192)
#print(recv_mode_msg.decode())

s.send(STRU_MSG.encode())
recv_stru_msg = s.recv(8192)
#print(recv_stru_msg.decode())

# if statements that delegate what the program will do based on what the operation from the command line was 
if(operation == "ls"):
    # ls <URL>  Print out the directory listing from the FTPS server at the given URL

    # open a data channel 
    s.send(PASV_MSG.encode())
    recieved = s.recv(8192).decode()
    #print(recieved)

    # parsing the recieved message for the IP address and port number that will be used to securely connect to the server
    split_recieved = recieved.split("(")
    pruning_message = split_recieved[1].split(",")
    ip_address = pruning_message[0] + "." + pruning_message[1] + "." + pruning_message[2] + "." + pruning_message[3]
    port_numbers = [pruning_message[4], pruning_message[5].split(")")[0]]
    port_number = ((int(port_numbers[0]) * 256) + int(port_numbers[1]))
    
    #print(ip_address)
    #print(port_number)
    
    #sending the list command to the server
    s.send(("LIST " + path +"\r\n").encode())
    
    #creating the TLS wrapped socket
    data_connection_socket = socket.create_connection((ip_address, port_number))
    context = ssl.create_default_context()
    secure_s = context.wrap_socket(data_connection_socket, server_hostname=hostname)
    
    print(secure_s.recv(8192).decode())
    secure_s.close()

if(operation == "mkdir"):
    # mkdir <URL>            Create a new directory on the FTPS server at the given URL

    # sending the mkdir command to the server and printing the output 
    s.send(("MKD " + path + "\r\n").encode())
    print(s.recv(8192).decode())
if(operation == "rm"):
    # rm <URL>               Delete the file on the FTPS server at the given URL

    # sending the delete command to the server and printing the output 
    s.send(("DELE " + path + "\r\n").encode())
    print(s.recv(8192).decode())
if(operation == "rmdir"):
    # rmdir <URL>            Delete the directory on the FTPS server at the given URL

    # sending the rmdir command to the server and printing the output
    s.send(("RMD " + path + "\r\n").encode())
    print(s.recv(8192).decode())
if(operation == "cp"):
    # cp <ARG1> <ARG2>       Copy the file given by ARG1 to the file given by
    #                        ARG2. If ARG1 is a local file, then ARG2 must be a URL, and vice-versa.

    #checking to see if the url is the first parameter or not in order to tell if the program should be copying something from the 
    # server to the local directory or vise versa
    if(urlFirst):
        # establishing a data channel
        s.send(PASV_MSG.encode())
        recieved = s.recv(8192).decode()
        # print(recieved)

        # parsing the recieved message for the IP address and port number that will be used to create a secure TLS message
        split_recieved = recieved.split("(")
        pruning_message = split_recieved[1].split(",")
        ip_address = pruning_message[0] + "." + pruning_message[1] + "." + pruning_message[2] + "." + pruning_message[3]
        port_numbers = [pruning_message[4], pruning_message[5].split(")")[0]]
        port_number = ((int(port_numbers[0]) * 256) + int(port_numbers[1]))
        
        #print(ip_address)
        #print(port_number)
        
        #sending the download command to the server
        s.send(("RETR " + path +"\r\n").encode())
        
        # creating the secure socket
        data_connection_socket = socket.create_connection((ip_address, port_number))
        context = ssl.create_default_context()
        secure_s = context.wrap_socket(data_connection_socket, server_hostname=hostname)
        contents = secure_s.recv(8192)

        # writing the downloaded contents into a file and then closing the file and the secure socket
        file = open(local, "wb")
        file.write(contents)
        file.close()
        secure_s.close()
    # if the url was not the first parameter, then the program should be copying something from the local directory to the server
    else:
        # establishing a data channel
        s.send(PASV_MSG.encode())
        recieved = s.recv(8192).decode()
        #print(recieved)

        # parsing the recieved message for the IP address and port number that will be used for creating a secure connection
        split_recieved = recieved.split("(")
        pruning_message = split_recieved[1].split(",")
        ip_address = pruning_message[0] + "." + pruning_message[1] + "." + pruning_message[2] + "." + pruning_message[3]
        port_numbers = [pruning_message[4], pruning_message[5].split(")")[0]]
        port_number = ((int(port_numbers[0]) * 256) + int(port_numbers[1]))
        
        #print(ip_address)
        #print(port_number)
        
        # sending the upload command to the server
        s.send(("STOR " + local +"\r\n").encode())
        
        # creating a secure TLS socket connection 
        data_connection_socket = socket.create_connection((ip_address, port_number))
        context = ssl.create_default_context()
        secure_s = context.wrap_socket(data_connection_socket, server_hostname=hostname)
        
        # opening the local file and reading the contents to another variable to be sent to the server via the secure connection 
        # and then closing both the file and the secure connection
        file = open(local, "rb")
        file_contents = file.read()
        secure_s.send(file_contents)
        secure_s.close()
        file.close()
if(operation == "mv"):
    #mv <ARG1> <ARG2>        Move the file given by ARG1 to the file given by
    #                        ARG2. If ARG1 is a local file, then ARG2 must be a URL, and vice-versa.

    # checks to see if the program should be moving something server to local or vise versa
    if(urlFirst):
        # establishing data channel
        s.send(PASV_MSG.encode())
        recieved = s.recv(8192).decode()
        #print(recieved)

        # parsing the recieved message for the IP address and port number used to create a secure connection with the server
        split_recieved = recieved.split("(")
        pruning_message = split_recieved[1].split(",")
        ip_address = pruning_message[0] + "." + pruning_message[1] + "." + pruning_message[2] + "." + pruning_message[3]
        port_numbers = [pruning_message[4], pruning_message[5].split(")")[0]]
        port_number = ((int(port_numbers[0]) * 256) + int(port_numbers[1]))
        
        #print(ip_address)
        #print(port_number)
        
        # sending the download command to the server 
        s.send(("RETR " + path +"\r\n").encode())
        
        # creating a secure connection with the server 
        data_connection_socket = socket.create_connection((ip_address, port_number))
        context = ssl.create_default_context()
        secure_s = context.wrap_socket(data_connection_socket, server_hostname=hostname)
        contents = secure_s.recv(8192)

        # opening the file and writing the contents of the file from the server into it and then closing the file and the connection
        file = open(local, "wb")
        file.write(contents)
        file.close()
        secure_s.close()

        # sending the delte command to the server, effectively "moving" the file from the server to local
        s.send(("DELE " + path + "\r\n").encode())
        print(s.recv(8192).decode())
    # handling the case that the url came second in which we want the program to move from local to the server 
    else:
        # establishing a data channel 
        s.send(PASV_MSG.encode())
        recieved = s.recv(8192).decode()
        # print(recieved)

        # parsing the recieved message for the IP address and port number used to create a secure connection with the server
        split_recieved = recieved.split("(")
        pruning_message = split_recieved[1].split(",")
        ip_address = pruning_message[0] + "." + pruning_message[1] + "." + pruning_message[2] + "." + pruning_message[3]
        port_numbers = [pruning_message[4], pruning_message[5].split(")")[0]]
        port_number = ((int(port_numbers[0]) * 256) + int(port_numbers[1]))
        
        #print(ip_address)
        #print(port_number)
        
        # sending the upload command to the server 
        print(path)
        s.send(("STOR " + path + "\r\n").encode())
        print(s.recv(8192))
        # giving an issue
        data_connection_socket = socket.create_connection((ip_address, port_number))
        context = ssl.create_default_context()
        secure_s = context.wrap_socket(data_connection_socket, server_hostname=hostname)
        
        # reading the contents of the file into a variable and sending it to the server and then closing 
        # the file and the connection to the server
        file = open(local, "rb")
        file_contents = file.read()
        secure_s.send(file_contents)
        secure_s.close()
        file.close()

        # deleting the file from the local machine, effectively "moving" the file 
        os.remove(local)

# asking the FTP server to close the connection and then disconnecting our socket
s.send(QUIT_MSG.encode())
print(s.recv(8192))
s.close()
