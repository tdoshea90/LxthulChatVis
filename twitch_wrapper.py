import os
import re
import socket
import ssl


class TwitchWrapper:
    """ Stream the chat """

    msg_queue = None

    def __init__(self, msg_queue):
        self.msg_queue = msg_queue

    def start_chat(self):
        """ https://github.com/justintv/Twitch-API/blob/master/IRC.md """

        server = 'irc.chat.twitch.tv'
        port = 443
        channel = '#halo'
        nickname = 'tdoshea90'
        auth_token = os.environ.get('TWITCH_TOKEN')

        irc_C = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # defines the socket
        irc = ssl.wrap_socket(irc_C)

        msg_regex = re.compile('.+PRIVMSG %s :' % channel)

        irc.connect((server, port))
        irc.setblocking(False)
        irc.send(('PASS %s\n' % auth_token).encode('utf-8'))
        irc.send(('NICK ' + nickname + '\n').encode('utf-8'))
        irc.send(('JOIN ' + channel + '\n').encode('utf-8'))

        while True:
            try:
                data_encoded = irc.recv(1024)
                data = data_encoded.decode('utf-8')
                if (len(data) < 1):
                    break

                if data.find('PRIVMSG') != -1:
                    msg = re.sub(msg_regex, '', data)
                    self.msg_queue.put(msg)
                    # print(msg)

                # Prevent Timeout
                if data.find('PING') != -1:
                    irc.send(('PONG ' + data.split()[1] + '\r\n').encode('utf-8'))
            except Exception:
                continue
