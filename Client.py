# -*- coding: utf-8 -*-
"""
Created on Fri Apr 28 10:17:59 2023


"""

import socket
import sys
from termcolor import colored

buffer_size = 10000



# Define variables
HOST = socket.gethostname()  # Replace with the IP address of the server
PORT = 8000  # Replace with the port number used by the server


try:
    # Set up socket and connect to server
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))

except ConnectionRefusedError: 
    print("Connection to server failed!")
    sys.exit(1)


try:
    
    # Wait for welcome message from server
    welcome_msg = sock.recv(buffer_size).decode()
    print(welcome_msg)

except (socket.error, ConnectionResetError) :
    print("Error receiving welcome message from server:")
    sys.exit(1)
    

print(sock.recv(buffer_size).decode()) 
    



# Start game loop

for round_num in range(1,4):
    # Receive random number from server and display it
    try:
        # will do a 3 second countdown 
        print(sock.recv(buffer_size).decode())
        print(sock.recv(buffer_size).decode())
        print(sock.recv(buffer_size).decode())
        
        
        rand_num = sock.recv(buffer_size).decode()
        rand_num_=(colored(rand_num,"yellow"))

        print(f"Round {round_num}: The random number is {rand_num_} YALLA!!!!")
        
    except (socket.error,ConnectionResetError) :
        print("Lost Connection with server")
        sys.exit(1)

       
    

    
        
    # prompt the user for input

    player_num = input("Enter the number as fast as possible: ")
    if player_num != rand_num:
        print("\nWRONG! YOU TYPED WRONG NUMBER!\n")
    else:
        print("Correct!")

            
    try: 
        sock.send(player_num.encode())
            
    except :
        print("The server has disconnected")
        sys.exit(1)


 
    # Results of the current round in descending order from server but i don't know if we need to display them
    table = sock.recv(buffer_size).decode()
    print(table)
    
    cumulative_table = sock.recv(buffer_size).decode()
    inbet = sock.recv(buffer_size).decode()

    print(cumulative_table)
    print(inbet)

# Receive final results and declare winner

winner = sock.recv(buffer_size).decode()
print(winner)

# Close the connection
sock.close()
