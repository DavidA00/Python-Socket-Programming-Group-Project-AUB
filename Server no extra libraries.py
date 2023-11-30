# -*- coding: utf-8 -*-
"""
Created on Fri Apr 28 16:51:47 2023

@author: ahmad
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Apr 28 11:07:23 2023

@author: mfa78
"""

"""
Created on Fri Apr 28 00:17:07 2023


"""

#This is the server code with no extra libraries (Music and colors)
import socket
import random
import time
import sys
from math import ceil




server_socket = socket.socket()
try:
    #retrieve name of device on which server is set
    hostname = socket.gethostname()
    #we choose this port number
    portnumber = 8000
    #bind the server socket to a port
    server_socket.bind((hostname, portnumber))

except socket.error as e:
    print("Error: ", str(e))
    sys.exit(1)
#chose number of players
num_players = int(input("Please enter the number of players that will join this game: ")) #chosen number of players
#listen for connections
server_socket.listen(num_players)






# Set up the lists to store the client connections and scores
clients = []
scores = [] #will contain the cumulative score for the player 
print("Awaiting connections...")
player_number= 0
for i in range(num_players):
    try:
        #Accept connection from client
        connection, address = server_socket.accept()
        #get player number
        player_number+=1
        
        welcome_msg= "Welcome, Player "+ str(player_number)+"\nYou have successfully connected to the game Server!"
        connection.send(welcome_msg.encode())
        #add client connection to the list of clients
        clients.append(connection)
        scores.append([player_number,0])
        #we add i+1 since players are numbered from 1 to num_players-1
        print("Player " + str(player_number) + " has connected")
        
        
    except socket.error as e:
        print("Error in accepting the client: ", str(e))
    
   
#message to indicate game is about to start and indicate error in case player has left
for i in range(len(clients)):
    try:
        clients[i].send("THE GAME WILL START SHORTLY!".encode())
    except ( ConnectionResetError) :
        
         endofgame = ("Sorry!!!! \n Player" + str(i+1)+ " has left, the game has ended!" )
         print("end of game")

         for j in range(len(clients)):
             if j!= (i-1):
                 clients[j].send((endofgame).encode())
                 
         sys.exit(1)
         
#wait for 3 seconds before starting the game
time.sleep(3)

# the connection is secure (TCP LIKE )
# and handle errors 
for round_num in range(1,4):
    
    #this array will contain the round scores for all players
    #scores are stored as a list where (i= player number, j= score)
    #if wrong number is pressed
    #if error on any client,end game
    
    
   
    round_scores = []
    print("started round",round_num)
    
    
    t= 1
    #now, we insert a t second delay to give players time to be ready for next round
    
    worst_score_this_round=0  # just a counter that will be updated to the largest RTT this round
    
    # after player_number players connect, keep these players in the game 
    #we generate random number of each player between 0 and 9
    for i in range(1,player_number+1):
        
        random_num = random.randint(0, 9)
        message=str(random_num) 
        clients[i-1].settimeout(12)
        
        try:
            #send the random numbers to the client
            clients[i-1].send("THREE".encode())
            time.sleep(t)
            clients[i-1].send("TWO".encode())
            time.sleep(t)
            clients[i-1].send("ONE".encode())
            time.sleep(t)
            print( " Sending random number to Player", i)
            clients[i-1].send((message).encode())
            print( " Sent random number to Player", i)

            #print on client side 
            start= time.time()
            
        except ( ConnectionResetError) :
             endofgame = ("Error receiving data from player" + str(i)+ " the game has ended." )
             winner = scores[0][0]
             endofgame+= ("\nThe winner is Player " + str(winner)+ "!!!\n Good Game!")
             print("end of game")
             
             for j in range(len(clients)):
                 if j!= (i-1):
                     clients[j].send((endofgame).encode())
                     
             sys.exit(1)
             

            
            
    
        try:
            recvd_num = clients[i-1].recv(1024).decode()
            end= time.time()
                    
            try: 
                recv = int(recvd_num)
                if recv == random_num:
                    score = end-start
                    score= round(score,3)
                    round_scores.append([i,score])
                    if max(score, worst_score_this_round) == score:
                        worst_score_this_round = score
                    
                else:
                    round_scores.append([i,None])
                
            except ValueError: 
                round_scores.append([i,None])
                
            
    #Indicate error and end game in case player lost connection
        except ConnectionResetError :
           
             endofgame = ("Error receiving data from player" + str(i)+ " the game has ended." )
             winner = scores[0][0]
             endofgame+= ("\nThe winner is Player " + str(winner)+ "!!!\n Good Game!")
             print("end of game")
             
             for j in range(len(clients)):
                 if j!= (i-1):
                     clients[j].send((endofgame).encode())
                     
             sys.exit(1)
                #indicate timeout in case player took too much time to respond and end game
        except( socket.timeout):
             endofgame = (" Player " + str(i)+ " timed out! \n The game has ended" )
             winner = scores[0][0]
             endofgame+= ("\nThe winner is Player " + str(winner)+ "!!!\n Good Game!")
             print("end of game")

             for j in range(len(clients)):
                 if j!= (i-1):
                     clients[j].send((endofgame).encode())
                     
             sys.exit(1)
    

       #In case the player enters a wrong input he will get a score
    for score in round_scores:
        if score[1] == None: score[1] = ceil(worst_score_this_round) # takes care of it like David described above
            

    
    # Update the scores list with the scores for the current round
    
    for score in scores:
        client_number = score[0] 
        for l in round_scores:
            if l[0]== client_number:    
                score[1] += l[1]
                score[1]= round(score[1],3)
                break
        

    # we are asked to display results in descending order; we will take this to mean : the best players on top, worst on bottom (in our case this is increasing order not descending)
    round_scores.sort(reverse=False,key=lambda T: T[1])
        
    scores.sort(reverse=False,key=lambda T: T[1] )
    
    
    table= ""
    # Display the results for the current round in descending order(from lowest score/shortest time to top)
    table+= ("\n Round " + str(round_num) + " scores:\n")

        
    
    table+= ("| {:<8} | {:<6} | {:<0} |\n".format("PLAYER", "SCORE", "RANK"))
    table+= ("|----------|--------|------|\n")
    

    
    r=0
    for s in round_scores :
        r+=1
        table+= ("| {:<7} | {:<6} | {:<2}   |\n".format("Player " + str(s[0]), str(s[1]), r))
        

    

    
    for i in range(len(clients)):
        clients[i].send((table).encode())
        
        
    cumulative_table= "" 
    cumulative_table+= ("\n Cumulative Leaderboard:\n")
    
  
    cumulative_table+=("| {:<8} | {:<6} | {:<0} |\n".format("PLAYER", "SCORE", "RANK"))
    cumulative_table+=("|----------|--------|------|\n")
    r=0
    for s in scores :
        r+=1
        cumulative_table+=("| {:<7} | {:<6} | {:<2}   |\n".format("Player " + str(s[0]), str(s[1]), r))
        
        


    inbet= "________________________________________________\n"

    if round_num !=3 :
        inbet+="\n"
        inbet+= "             GET READY FOR NEXT ROUND!"
    else:
        inbet+="\n"
        inbet += "                     THE END\n"

    inbet+= "________________________________________________\n"

    
    print( "sent results successfully for round",round_num )
    for i in range(len(clients)):
        clients[i].send((cumulative_table).encode())
        clients[i].send(inbet.encode())

    


        
#the winner is one with smallest score/ shortest time
winner = scores[0][0]
for client in clients:
    client.send(("\nThe winner is Player " + str(winner)+ "!!!\n Good Game!").encode())

#close my connections
for client in clients:
    client.close()

#close the server
server_socket.close()
