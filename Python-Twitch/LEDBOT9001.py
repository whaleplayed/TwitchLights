import socket, string, serial, re, binascii #add libraries


# Create Serial port object called arduinoSerialData and read the serial data
Arduino_Serial = serial.Serial('com5', 9600)
print Arduino_Serial.readline()

 
# Set all the variables necessary to connect to Twitch IRC
HOST = "irc.twitch.tv"
NICK = "LEDBOT9001"
PORT = 6667
PASS = "oauth:j11eqv9bblfy6a2o2r82ryw8zbzw3f"
readbuffer = ""
MODT = False
 
# Connecting to Twitch IRC by passing credentials and joining a certain channel
s = socket.socket()
s.connect((HOST, PORT))
s.send("PASS " + PASS + "\r\n")
s.send("NICK " + NICK + "\r\n")
s.send("JOIN #theleastchadchadyouknow \r\n")
 
# Method for sending a message
def Send_message(message):
    s.send("PRIVMSG #theleastchadchadyouknow :" + message + "\r\n")
 
 
while True:
    readbuffer = readbuffer + s.recv(1024)
    temp = string.split(readbuffer, "\n")
    readbuffer = temp.pop()
 
    for line in temp:
        # Checks whether the message is PING because its a method of Twitch to check if you're afk
        if (line[0] == "PING"):
            s.send("PONG %s\r\n" % line[1])
        else:
            # Splits the given string so we can work with it better
            parts = string.split(line, ":")
 
            if "QUIT" not in parts[1] and "JOIN" not in parts[1] and "PART" not in parts[1]:
                try:
                    # Sets the message variable to the actual message sent
                    message = parts[2][:len(parts[2]) - 1]
                except:
                    message = ""
                # Sets the username variable to the actual username
                usernamesplit = string.split(parts[1], "!")
                username = usernamesplit[0]
               
                # Only works after twitch is done announcing stuff (MODT = Message of the day)
                if MODT:
                    print username + ": " + message
                   
                    # You can add all your plain commands here
                    # if message == "Hey":
                    #     Send_message("Welcome to my stream, " + username)


                    # Events
                    if username == "streamlabs" and "Thank you for following" in message:
                        Arduino_Serial.write('9')
                        print ("YOU JUST GOT A FOLLOW")
                    
                    # Interesting Combinations
                    if message == "!CRAZYCATERPILLAR":
                        Arduino_Serial.write('1')
                        print ("SENDING CRAZY CATERPILLAR")

                    if message == "!FLAMES":
                        Arduino_Serial.write('2')
                        print ("SENDING FLAMES")

                    # Many different colors
                    if message == "!RED":
                        Arduino_Serial.write('4')
                        print ("SENDING RED")

                    if message == "!BLUE":
                        Arduino_Serial.write('5')
                        print ("SENDING BLUE")

                    if message == "!GREEN":
                        Arduino_Serial.write('3')
                        print ("SENDING GREEN")
                        
                    if message == "!TWINKLE":
                        Arduino_Serial.write('6')
                        print ("SENDING TWINKLE")

                    if message == "!BLASTS":
                        Arduino_Serial.write('7')
                        print ("SENDING BLASTS")
                    
                    if message == "!FIREWORKS":
                        Arduino_Serial.write('8')
                        print ("SENDING FIREWORKS")

                    if message == "!CHAD":
                        Arduino_Serial.write('b')
                        print ("SENDING CHAD?")

                    if message == "!TRANS":
                        Arduino_Serial.write('d')
                        print ("SENDING TRANS")

                    if message == "!PINGPONG":
                        Arduino_Serial.write('e')
                        print ("SENDING PINGS AND PONGS")

                    if "nut" in message.lower():
                        Arduino_Serial.write('a')
                        print("NUTTING")

                    colorList = re.findall("^!COLORS? #?([0-9,A-F,a-f]){6}$", message)
                    if len(colorList) > 0:
                        colors = message[-6:]
                        Arduino_Serial.write('c')
                        print("SENDING COLOR")
                        buf = binascii.unhexlify(colors)
                        Arduino_Serial.write(buf[0])
                        Arduino_Serial.write(buf[1])
                        Arduino_Serial.write(buf[2])

                    # Just the little baby OFF button (very valuable and important)
                    if message == "!OFF":
                        Arduino_Serial.write('0')
                        print ("TURN THAT SHIT OFF")
 
                for l in parts:
                    if "End of /NAMES list" in l:
                        MODT = True
