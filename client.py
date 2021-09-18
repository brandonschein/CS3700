#usr/bin/python
import sys
import socket
import ssl

def count(find, find_in):
    count = 0

    for i in find_in:
        if (i == find):
            count += 1

    return count


info = sys.argv[1:]

#print(info)

# how to tell what info is given? for the flag does it show up as -S in the stdin?
NUID = info[-1]
HOSTNAME = info[-2]

# can be overriten by the user if providing optional
# #information, if not this will be the default
port = 27993 #non encrypted port
encrypted = False

if(len(info) == 3):
    if(info[0] == "-s"):
        encrypted = True
        port = 27994
    else:
        print("invalid input")
if(len(info) == 4):
    if(info[0] == "-p"):
        port = int(info[1])
    else:
        print("invalid input")

if(len(info) == 5):
    if (info[2] == "-s"):
        encrypted = True
        port = 27994
    if(info[0] == "-p"):
        port = int(info[1])
    else:
        print("invalid input")

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
if encrypted:
    context = ssl.create_default_context()
    s = context.wrap_socket(s, server_hostname=HOSTNAME)

s.connect((HOSTNAME, port))

hello_message = "ex_string HELLO " + NUID + '\n'
s.sendall(hello_message.encode())

find_message = s.recv(8192).decode()

while find_message[-1] != "\n":
    find_message += s.recv(8192).decode()

find_arr = find_message.split(" ")

to_find = find_arr[2]
in_str = find_arr[3]

count_num = count(to_find, in_str)

count_message = "ex_string COUNT " + str(count_num) + '\n'

s.sendall(count_message.encode())

return_message = s.recv(8192).decode()

while return_message[-1] != "\n":
    return_message += s.recv(8192).decode()

return_message_arr = return_message.split(" ")


while(return_message_arr[1] == "FIND") :
    return_count_num = count(return_message_arr[2], return_message_arr[3])

    count_message= "ex_string COUNT " + str(return_count_num) + '\n'
    s.sendall(count_message.encode())

    return_message = s.recv(8192).decode()
    while return_message[-1] != "\n":
        return_message += s.recv(8192).decode()

    return_message_arr = return_message.split(" ")

flag = return_message_arr[2]

print(flag)

s.close()


