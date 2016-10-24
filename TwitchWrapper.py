import re
import socket
import ssl


# Settings
# IRC
server = "irc.chat.twitch.tv"
port = 443
channel = "#itssofrosty"
nickname = "tdoshea90"
password = "oauth:gknrx6icpfpoveruanni9unrutuwrj"

irc_C = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # defines the socket
irc = ssl.wrap_socket(irc_C)

msg_regex = re.compile(".+PRIVMSG %s :" % channel)

print("Establishing connection to [%s]" % (server))
# Connect
irc.connect((server, port))
irc.setblocking(False)
irc.send("PASS %s\n" % (password))
irc.send("NICK " + nickname + "\n")
irc.send("JOIN " + channel + "\n")

while True:
    try:
        text = irc.recv(1024)
        print(re.sub(msg_regex, '', text))

        # Prevent Timeout
        if text.find('PING') != -1:
            irc.send('PONG ' + text.split()[1] + '\r\n')
    except Exception:
        continue
