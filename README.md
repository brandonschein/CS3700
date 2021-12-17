Project 6: Implemeting a simple consensus algorithm, Raft

High Level Approach: Implementing this project required implementing the features of the Raft Protocol, such as leaders, elections, nominations, timeouts, etc. 
The event loop acts as the main of this function, constantly looking for any incoming messages to the replica and dealing with them accordingly. Because every 
replica can be a follower, candidate, and leader, and there is only one program that is replicated for all states, the program must handle working with all 
possibilites. In the event loop, if the message recieved is a get or put message, it is redirected to the leader by followers and is dealt with by the leader, 
ultimately either sending the value info, or putting the info into the log, or failing. If a vote-request is recieved, the replica decides whether or not it should
be voting and if it is who it is voting for. If a vote accept or reject message is recieved, it is dealt with to update the replicas global variables. If the 
message is an append-entries message, the entries are appended. if the replica is a leader, we check if the message is append-reply as we are the only one with 
authority to deal with this reply. After dealing with the incoming message, update if possible the highest index. Then we check that the applied index is up to 
date. Then we check if it is time for a new election. And finally we send a heartbeat to replicas. 

Challenges Faced: There were many challenges faced in this project from both an understanding and implementing point of view. From an understanding point of view,
working with and understanding raft took an intensive read through of the provided raft paper, website explanation, and other resources. Even once we felt we had a 
base understanding of the protocol, there was still a lot of difficulty in mapping out the pseudocode for how to approach the project. Coding the project as well
proved to be very challenging. Wrapping our heads around the distributed system portion of coding this took some time as we figured out how we were going to 
communicate with the other replicas of the program. Another challenge faced during programming was that we were running into issues with our put and it took 
taking a relook through the section about log updating to realize we needed to be sending an AppendRC message to followers after doing this as to keep consensus. 
A challenge that we felt we were not able to overcome was that we are unsure as to why passsing the tests can feel a bit random at time, as in we pass 17 of 17 
tests, but randomly will fail a test or two on an all run. Running the failed test in this case usually resulted in the test case that had failed passing but 
we were unable to figure out what was causing it, with the problem ultimately still remaining. Another similar challenge is that we could not figure out why on some
runs, the performance tests would pass or be better and other times, would fail with some failures being horrible (ie 30,000 Failures/unanswered responses). 

Testing: Testing was done throughout development, using print statements to check input, calculations, and output. This was also coupled with the usage of provided
tests in the tests folder. Running ./sim.py all or ./sim.py tests/<specific-test> allowed us to be confident in the success of our implementation. 
