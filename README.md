# Protocol-4-Stop-and-Wait
An implementation of Stop and Wait Protocol (Protocol 4) using Socket programming in Python.

## About the Code:
1) The input files are being expected from the Network layer and the code does necessary framming using flag and escape character.
2) This encoded file is then transferreed using the Physial Layer which is Socket in our case.
3) The encoded file recieved on the other hand is than decoded and the original message is then sent to the above layer(Network Layer on other side).
4) According the Stop and Wait the code works for two way transmission.

## Steps:
1) Run sender.py on one computer and reciever.py on another computer.
2) Enter the Hostname provided in one computer into another for the Connection establishment.
3) The File given provided inside the code will then be transferred using the Physcal Layer(Socket in our case).
