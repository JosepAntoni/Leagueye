from bs4 import BeautifulSoup
from urllib.error import HTTPError
from urllib.request import urlopen
from Leagueye.Summoner import Summoner
import json
from Leagueye.League import League
from Leagueye.SummonerId import SummonerId
import time
# Create your models here.

api_key = "RGAPI-fc643e9e-43ac-476b-b1f3-b0649cf5d2e5"


class Match(object):
    """documentation TODO"""

    def __init__(self, summoner_name = object):
        #self.players = []
        self.summoner_id = Summoner(summoner_name).get_id()
        self.match_data = self.get_match_data()
        self.players = self.parse(self.match_data, "participants")
        self.bans = self.parse(self.match_data, "bannedChampions")
        self.left_team, self.right_team = self.get_players(self.players)
        self.left_bans, self.right_bans = self.get_bans(self.bans)

    def get_url(self):
        url = "https://euw1.api.riotgames.com/lol/spectator/v3/active-games/by-summoner/"
        url += str(self.summoner_id) + "?api_key="
        url += api_key
        return url

    def get_match_data(self):
        url = self.get_url()

        try:
            f = urlopen(url)
            raw_data = f.read()
            f.close()
            return raw_data

        except HTTPError:
            #raise Exception("El usuario no esta en partida")
            return None

    def parse(self, raw, attribute):
        # parse
        if raw != None:
            soup = BeautifulSoup(raw, "html.parser")
            newDictionary = json.loads(str(soup))
            attr = newDictionary[attribute]
            return attr
        return None

    def get_players(self, list):
        left = []
        right = []
        if list != None:
            for dict in list:
                #time.sleep(1)
                aux = {}
                #summonerName = dict["summonerName"]
                aux["championId"] = dict["championId"]
                aux["summonerName"] = dict["summonerName"]
                aux["summonerId"] = dict["summonerId"]
                aux["spell1Id"] = dict["spell1Id"]
                aux["spell2Id"] = dict["spell2Id"]
                aux["perks"] = dict["perks"]
                aux = self.get_league_data(aux)
                if dict["teamId"] == 100:
                    left.append(aux)
                else: right.append(aux)
        return left, right

    def get_league_data(self, aux):
        league = League(aux["summonerId"])
        tier, rank, win_rate = league.get_data()
        aux["tier"] = tier
        aux["rank"] = rank
        aux["winrate"] = win_rate
        return aux

    def get_bans(self, list):
        left = []
        right = []
        if list != None:
            for dict in list:
                if dict["teamId"] == 100:
                    left.append(dict["championId"])
                else:
                    right.append(dict["championId"])
        return left, right

    def get_data(self):
        return self.left_team, self.right_bans, self.left_bans, self.right_bans

if __name__ == '__main__':
    match = Match("fourmarta")
    print(match.left_team)
    print(match.right_team)
    #print(match.left_bans)
    #print(match.right_bans)
