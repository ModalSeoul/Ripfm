import requests
import json
from time import sleep

# Don't touch these
Auth = 'https://modal.moe/api/api-token-auth/'
Scrobble = 'https://modal.moe/api/scrobbles/'
Key = '7d25207fefda375df7db633eae91ef88'
Secret = 'be6ad97265f13b44efba96859d75c01d'

# Aliases
post = requests.post
get = requests.get


class Wilt:

    def __init__(self):
        self.user = input('Username: ')
        self.password = input('Password: ')
        self.last_fm = input('Last.fm Username: ')
        self.logged_in = False
        self.header = {'Authorization': 'Token {}'.format(self.login())}
        self.last_played = ''  # Clarity

    def login(self):
        r = post(Auth, data={'username': self.user, 'password': self.password})
        if 'token' in r.text:
            self.logged_in = True
        else:
            print('Something went wrong - Not loggined in!')
            return None
        return json.loads(r.text)['token']

    def scrobble(self, scrobble):
        if scrobble['song'] != self.last_played:
            r = post(Scrobble, data=scrobble, headers=self.header)
            self.last_played = scrobble['song']
        else:
            return None

# Instantiating our Wilt class
Wilt = Wilt()


def recent_url(user):
    return ('http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks'
            '&user={}&api_key={}&format=json'.format(user, Key))


def rip():
    r = get(recent_url(Wilt.last_fm))
    track_info = []
    response = json.loads(r.text)['recenttracks']['track'][0]

    # Encoding for the weebs
    song = response['name'].encode('utf-8')
    artist = response['artist']['#text'].encode('utf-8')
    Wilt.scrobble({'song': song, 'artist': artist})

if __name__ == '__main__':
    while 1:
        rip()
        sleep(15)
