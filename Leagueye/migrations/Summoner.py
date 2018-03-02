from django.db import models
from bs4 import BeautifulSoup
from django.http import Http404
from urllib.error import HTTPError
from urllib.request import urlopen
import json

# Create your models here.

api_key = "RGAPI-3090a5c4-fb21-418e-81ab-e780d70c7ae4"


class Summoner(object):
    """documentation TODO"""

    def __init__(self, summoner_name):
        self.accountId = None
        self.name = None
        #self.profileIconId = None
        # self.summonerLevel = None
        self.summoner = summoner_name
        self.raw_summoner = self.get_raw_data()
        self.accountId = self.parse(self.raw_summoner, "accountId")
        self.name = self.parse(self.raw_summoner, "name")
        #    #self.xml_match = self.get_xml_match()
        #    self.summonerLevel = self.parse(self.xml_summoner, "summonerLevel")
        #    self.profileIconId = self.parse(self.xml_summoner, "profileIconId")

    # self.level =
    # self.rank =
    # self.tier =
    # self.match =
    # self.champion =
    # self.spell1 =
    # self.spell2 =
    # self.keystone1 =
    # self.keystone2 =

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
            raise Http404(UserWarning)
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
        return self.accountId

    def get_name(self):
        return self.name

    def get_xml_match(self):
        url = "https://euw1.api.riotgames.com/lol/spectator/v3/active-games/by-summoner/"
        url += self.id + "?api_key="
        url += api_key
        return self.get_url(url)


if __name__ == '__main__':
    requested_name = "josepantoni4"
    sum = Summoner(requested_name.replace(" ", ""))

    if sum.accountId != None: print(sum.accountId)
    if sum.name != None: print(sum.name)
    # if sum.summonerLevel != None: print(sum.summonerLevel)
    # if sum.profileIconId != None: print(sum.profileIconId)

# sum.almanac()
