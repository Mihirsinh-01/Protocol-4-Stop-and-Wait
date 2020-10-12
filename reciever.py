# refer sender.py for refering the comments in the implementation

import socket
import os
import sys
import time
import pickle
import random

class frame:
	ack=0
	seq=0
	info=""

flag='*'
esc='^'

def encoding(s):
	st=flag
	for i in range(len(s)):
		if(s[i]==flag or s[i]==esc):
			st=st+esc+s[i]
		else:
			st=st+s[i]
	st=st+flag
	return st

def decoding():
	t=open("sender's_msg.txt","w")
	t.close()
	file1=open("m2_b.txt","r")
	tem=open("sender's_msg.txt","a+")
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


soc=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host=input("Enter Hostname: ")					# input the Hostname of the computer to be connected with
port=8093										# both sides should have same port
soc.connect((host,port))
print("Connected")

r=frame()
s=frame()

mid=open("i2_p.txt","r")
q=open("m2_b.txt","w")
q.close()

next_frame_to_send=0
frame_expected=0
ran=random.randint(1,6)
buf=mid.read(ran)
buf=encoding(buf)
s.info=buf
s.seq=next_frame_to_send
s.ack=1-frame_expected
ss=pickle.dumps(s)
soc.send(ss)

my_done=False
your_done=False
print("Transferring...")
try:
	while(my_done==False or your_done==False):
		time.sleep(1)
		r=soc.recv(1024)
		re=pickle.loads(r)
		if(re.info==flag*2):
			your_done=True
		if(re.seq==frame_expected):
			nl=open("m2_b.txt","a+")
			if(your_done==False):
				nl.write(re.info)
			nl.close()
			frame_expected^=1
		if(re.ack==next_frame_to_send):
			ran=random.randint(1,6)
			buf=mid.read(ran)
			if(buf==""):
				my_done=True
			buf=encoding(buf)
			next_frame_to_send^=1

		s.info=buf
		s.seq=next_frame_to_send
		s.ack=1-frame_expected
		ss=pickle.dumps(s)
		soc.send(ss)
	soc.close()
except ConnectionResetError:
	soc.close()
decoding()
print("Done")