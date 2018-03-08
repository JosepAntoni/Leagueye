from django.db import models
from bs4 import BeautifulSoup
from django.http import Http404
from urllib.error import HTTPError
from urllib.request import urlopen
import json

# Create your models here.

api_key = "RGAPI-fc643e9e-43ac-476b-b1f3-b0649cf5d2e5"


class League(object):
    """documentation TODO"""

    def __init__(self, summoner_id):
        self.tier = None
        self.rank = None
        self.win_rate = None
        self.summoner_id = summoner_id
        self.league_data = self.get_league_data()
        self.solo = self.get_solo(self.league_data)
        if self.solo != None:
            self.tier = self.solo["tier"]
            self.rank = self.solo["rank"]
            self.win_rate = self.get_winrate(self.solo)

    def get_url(self):
        url = "https://euw1.api.riotgames.com/lol/league/v3/positions/by-summoner/"
        url += str(self.summoner_id) + "?api_key="
        url += api_key
        return url

    def get_league_data(self):
        url = self.get_url()

        try:
            f = urlopen(url)
            raw_data = f.read()
            f.close()
            return raw_data

        except HTTPError:
            print("League error")
            #raise Http404(UserWarning)
            # return None

    def parse(self, raw, attribute):
        # parse
        if raw != None:
            soup = BeautifulSoup(raw, "html.parser")
            newDictionary = json.loads(str(soup))
            attr = newDictionary[attribute]
            # print results
            return attr
        return None

    def get_winrate(self, league_data):
        wins = league_data["wins"]
        losses = league_data["losses"]
        win_rate = float(wins/(wins + losses) * 100)
        return win_rate

    def get_solo(self, league_data):
        soup = BeautifulSoup(league_data, "html.parser")
        newDictionary = json.loads(str(soup))
        if (len(newDictionary) == 2):
            for dict in newDictionary:
                if dict["queueType"] == "RANKED_SOLO_5x5":
                    return dict
            return None
        elif len(newDictionary) == 1:
            aux = "RANKED_SOLO_5x5"
            if newDictionary[0]["queueType"] == aux:
                print(newDictionary[0])
                return newDictionary[0]
            else:
                return None
        else:
            return None




if __name__ == '__main__':

    league = League(24743501)
    print(league.win_rate)
    print(league.tier)
    print(league.rank)

