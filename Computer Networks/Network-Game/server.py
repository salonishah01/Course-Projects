import socket
from _thread import *
from player import Player
import pickle

red = (255,0,0)
green = (0,255,0)
cyan = (0,183,235)
yellow = (255,255,0) 
purple = (75,0,130)

maxNoOfPlayers = 4
radius = 40 # Radius of the player circle

server = "localhost"
port = 5555

socket.SOCK_STREAM.allow_reuse_address = True
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    print(str(e))
 
s.listen()
print("Waiting for a connection, Server Started")


# Currently support 4 player game. For more players, keep appending Player object in players list with different color

players = [ Player(70,70,radius,red,0,True,maxNoOfPlayers), # Infected
            Player(130,130,radius,green,5,False,maxNoOfPlayers), 
            Player(190,190,radius,cyan,5,False,maxNoOfPlayers),
            Player(250,250,radius,purple,5,False,maxNoOfPlayers)
            #Player(x,y,radius,someColor,health,infected?,maxNoOfPlayers),
            #.....
            #.....
        ]

# Input: Index of current player
# Return: All the player object except the current one
def makeReply(currentPlayerID):
    return players[:currentPlayerID] + players[currentPlayerID+1:totalPlayers]

# Input: connection object and player ID
# Return None
# Description: Initially send the starting position for the player which initiates the connection.
# Later, recieve the information sent by the player, update it and send other players' information.
def threaded_client(conn, playerID):
    conn.send(pickle.dumps(players[playerID]))
    reply = ""
    while True:
        try:
            data = pickle.loads(conn.recv(2048))
            players[playerID] = data

            if not data:
                print("Disconnected")
                break
            else:
                reply = makeReply(playerID)   

                print("Received: ", data)
                print("Sending : ", reply)

            conn.sendall(pickle.dumps(reply))
        except:
            break

    print("Lost connection")
    conn.close()

# Input: None
# Return: None
# Description: Starts a new thread whenever a new client connects to the server.
def acceptConnections():
    conn, addr = s.accept()
    print("Connected to:", addr)

    start_new_thread(threaded_client, (conn, totalPlayers))

totalPlayers = 0
while True:
    if totalPlayers <= maxNoOfPlayers:
        acceptConnections()
        totalPlayers += 1
    else:
        print("Server reached the number of players limit!!")
        break
