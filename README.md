#project 1
High level approach:
My approach to this project was to first get the information that the program was run with, then setup a connection with the specified server from the command line info (if the -s flag was given I made this connection TLS encrypted), then send the hello message to start the client/server conversation, then recieve the find message, then use the count function to find the amount of times the given ascii character was in the given string, then send a count message to the server and decide if the message back was either another count message or a bye message, if it is a count message I follow the same protocol as just stated, if it was a bye message I stripped the flag and printed it. 

Challenges:
Working with the socket library was something that was completely new to me and challenged me when trying to figure out syntax and how to debug. It's also been a few years since I've used python so while I understood the logic of what I was wanting to do, actually implementing those ideas using python proved to be challenging and had me doing lots of looking at the documentation. A big error that stumped me for a while was that I had missed in the FAQ about the find messages not fully being taken in by my program, resulting in lots of question marks when I was trying to debug and figure out why sometimes I would get a message that had the ex_string find ascii character syntax and why sometmies I was just getting a random string of characters.

Testing:
Testing for this program was done manually by trying each command line combination that would follow the given protocol. 
These tests resulted in the secret flags that are given for correctly following protocol for both an encrypted and non-encrypted
connection. These flags can be found in secret_flags for verification
