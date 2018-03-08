from django.db import models
from bs4 import BeautifulSoup
from django.http import Http404
from urllib.error import HTTPError
from urllib.request import urlopen
import json

# Create your models here.

api_key = "RGAPI-fc643e9e-43ac-476b-b1f3-b0649cf5d2e5"


class Summoner(object):
    """documentation TODO"""

    def __init__(self, summoner_name):
        self.accountId = None
        self.name = None
        self.summoner = summoner_name
        self.raw_summoner = self.get_raw_data()
        self.Id = self.parse(self.raw_summoner, "id")
        self.level = self.parse(self.raw_summoner, "summonerLevel")


    def get_url(self):
        url = "https://euw1.api.riotgames.com/lol/summoner/v3/summoners/by-name/"
        url += self.summoner + "?api_key="
        url += api_key
        return url

    def get_raw_data(self):
        url = self.get_url()

        try:
            f = urlopen(url)
            raw_data = f.read()
            f.close()
            return raw_data

        except HTTPError:
            print("User does not exist")
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

    def get_id(self):
        return self.Id

    def get_level(self):
        return self.level



"""if __name__ == '__main__':
    requested_name = "traxx"
    sum = Summoner(requested_name.replace(" ", ""))

    if sum.Id != None: print(sum.Id)
    if sum.name != None: print(sum.name)
    # if sum.summonerLevel != None: print(sum.summonerLevel)
    # if sum.profileIconId != None: print(sum.profileIconId)
"""
