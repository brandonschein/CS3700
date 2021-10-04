#usr/bin/python
import sys
import socket
import ssl

# a function that given a character and string, will return how many times the character appears
def count(find, find_in):
    count = 0

    for i in find_in:
        if (i == find):
            count += 1

    return count

# gets all the command line arguements and cuts off the name of the program
info = sys.argv[1:]

# these two will always be at the end in this order according to the protocol so
# we can set these without having to look at the string specifically
NUID = info[-1]
HOSTNAME = info[-2]

# can be overriten by the user if providing optional information, if not this will be the default
port = 27993 #non-encrypted port
encrypted = False 

# if the length is three, this means the user inputted the -s flag, check that this is true and set variables
if(len(info) == 3):
    if(info[0] == "-s"):
        encrypted = True
        port = 27994
    else:
        print("invalid input")
# if the length is four, this means the user inputed -p portnumber, check that this is true and set variables
if(len(info) == 4):
    if(info[0] == "-p"):
        port = int(info[1])
    else:
        print("invalid input")
# if the length is 5, this means the user inputed all optional info(-p portnumber -s), 
# check this is the case and set variables
if(len(info) == 5):
    if (info[2] == "-s"):
        encrypted = True
        port = 27994
    if(info[0] == "-p"):
        port = int(info[1])
    else:
        print("invalid input")

# prime the socket for usage
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# check to see if we need to establish an encrypted TLS connection or not 
if encrypted:
    context = ssl.create_default_context()
    s = context.wrap_socket(s, server_hostname=HOSTNAME)

# connect to the server
s.connect((HOSTNAME, port))

# send the hello message
hello_message = "ex_string HELLO " + NUID + '\n'
s.sendall(hello_message.encode())

# recieve what is known to be a find message
find_message = s.recv(8192).decode()

# keep recieiving from the server until we have gotten the full message
while find_message[-1] != "\n":
    find_message += s.recv(8192).decode()

# parsing message for information needed to find the count
find_arr = find_message.split(" ")
to_find = find_arr[2]
in_str = find_arr[3]

# sending info to count to get the number of times the character appeared
count_num = count(to_find, in_str)

# send the count to the server
count_message = "ex_string COUNT " + str(count_num) + '\n'
s.sendall(count_message.encode())

# recieve the message from the server
return_message = s.recv(8192).decode()

# keep recieving from the server until we have the entire message
while return_message[-1] != "\n":
    return_message += s.recv(8192).decode()

# prime the message for parsing
return_message_arr = return_message.split(" ")

# use this while loop to keep reciving a message, finding the count, sending the count, until a bye message is recieved
while(return_message_arr[1] == "FIND") :
    # get the count
    return_count_num = count(return_message_arr[2], return_message_arr[3])

    # send the count to the server
    count_message= "ex_string COUNT " + str(return_count_num) + '\n'
    s.sendall(count_message.encode())

    # recieve the message
    return_message = s.recv(8192).decode()
    while return_message[-1] != "\n":
        return_message += s.recv(8192).decode()

    # setup for the while loop to continue or break
    return_message_arr = return_message.split(" ")

# if the while loop has broken, we have a bye message so strip the flag from thiss message
flag = return_message_arr[2]

# print the flag 
print(flag)

# close the connection with the server
s.close()


