#importing necessary python API
import socket
import os
import sys
import time
import pickle
import random

# defining class for creating frame
class frame:
	ack=0
	seq=0
	info=str("")

# flag and Escape character for encoding and decoding
flag='*'
esc='^'

# encoding function for converting message in the form of encoded message
def encoding(s):
	st=flag
	for i in range(len(s)):
		if(s[i]==flag or s[i]==esc):
			st=st+esc+s[i]
		else:
			st=st+s[i]
	st=st+flag
	return st

# decoding function converted encoded message to original text
def decoding():
	t=open("recv_msg.txt","w")
	t.close()
	file1=open("m1_b.txt","r")
	tem=open("recv_msg.txt","a+")
	s = file1.read()
	e=0
	for i in range(len(s)):
	    if(s[i]==flag):
	        if(e%2!=0):
	            tem.write(s[i])
	            e=0
	        else:
	            continue
	    elif(s[i]==esc):
	        if(e%2!=0):
	            tem.write(s[i])
	        e+=1
	    else:
	        e=0
	        tem.write(s[i])
	file1.close()
	tem.close()



soc=socket.socket(socket.AF_INET, socket.SOCK_STREAM)	# creating Socket
print("waiting for connection")
host=socket.gethostname()		# getting hostname of own computer for connection
print("Hostname: ",host)
port=8093						# defining port address
soc.bind((host,port))
soc.listen(1)					# Opening socket for 1 connection
conn,addr=soc.accept()			# Connecting to other PC
print("Connection Accepted")


# Protocol 4 - One Bit Sliding Window Protocol
next_frame_to_send=0
frame_expected=0
r=frame()
s=frame()
mid=open("i1_p.txt","r") 		# file message to be sent
q=open("m1_b.txt","w")			# file message to be recieved
q.close()


ran=random.randint(1,6)			# genarting random frame size
buf=mid.read(ran)
buf=encoding(buf)				# encoding the string using above declared functions
r.info=buf
r.seq=next_frame_to_send
r.ack=1-frame_expected
rr=pickle.dumps(r)				# pickle library for sending objects through socket
conn.send(rr)					# pickle converts objects into sendable format

my_done=False					# my data is left for sending
your_done=False					# the other side of sender will still send the message
print("Transferring...")
try:
	while(my_done==False or your_done==False):
		# time.sleep(1)
		r=conn.recv(1024)		# Socket recieving input from other program
		re=pickle.loads(r)		# converting sendable object back to usable object format
		if(re.info==flag*2):
			your_done=True		# empty frame recieved means other side is done sending
		if(re.seq==frame_expected):
			nl=open("m1_b.txt","a+")
			if(your_done==False):
				nl.write(re.info)	# means this is not an empty file
			nl.close()
			frame_expected^=1
		if(re.ack==next_frame_to_send):
			ran=random.randint(1,6)
			buf=mid.read(ran)
			if(buf==""):
				my_done=True		# my_done = true means i have done sending
			buf=encoding(buf)
			next_frame_to_send^=1

		s.info=buf
		s.seq=next_frame_to_send
		s.ack=1-frame_expected
		ss=pickle.dumps(s)
		conn.send(ss)
	soc.close()
except ConnectionResetError:		# if other side terminates the socket than it should not cause a error
	soc.close()						# closing the socket

decoding()							# decoding back the encrypted file to original message
print("Done")