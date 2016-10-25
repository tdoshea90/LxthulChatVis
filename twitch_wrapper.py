import os
import re
import socket
import ssl


class TwitchWrapper:
    """ Stream the chat """

    def start_chat(self):
        # IRC Settings
        server = 'irc.chat.twitch.tv'
        port = 443
        channel = '#lxthul'
        nickname = 'tdoshea90'
        auth_token = os.environ.get('TWITCH_TOKEN')

        irc_C = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # defines the socket
        irc = ssl.wrap_socket(irc_C)

        msg_regex = re.compile('.+PRIVMSG %s :' % channel)

        print('Establishing connection to [%s]' % (server))
        irc.connect((server, port))
        irc.setblocking(False)
        irc.send(('PASS %s\n' % auth_token).encode('utf-8'))
        irc.send(('NICK ' + nickname + '\n').encode('utf-8'))
        irc.send(('JOIN ' + channel + '\n').encode('utf-8'))

        while True:
            try:
                data = irc.recv(1024)
                if (len(data) < 1):
                    print('Connection terminated')
                    break

                print(re.sub(msg_regex, '', data.decode('utf-8')))

                # Prevent Timeout
                if data.find('PING') != -1:
                    irc.send(('PONG ' + data.split()[1] + '\r\n').encode('utf-8'))
            except Exception:
                continue
