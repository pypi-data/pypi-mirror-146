# cvache
# 10/6/21
# ingestor.py
from riotwatcher import LolWatcher, ApiError
from . config import Config


class Ingestor():
    def __init__(self, userConfig: Config):
        self.RIOT_API = LolWatcher(api_key=userConfig.getAPI_Key())
        self.REGION_NA1 = 'na1'
        self.REGION_AMERICAS= 'americas'





    #final function to call
    #returns an array of matchIds of size listSize of matchIds
    def createDownloadQueue(self, seedUsername, listSize=1000):
        downloadQueue = []
        matchlist = self.getMatchlist(self.getPuuidFromUsername(seedUsername))
        for match in matchlist:
            downloadQueue.append(match)
        
        while len(downloadQueue) < listSize:
            seedMatch = downloadQueue.pop()
            newUUIDS = self.getUUIDs(seedMatch)
            downloadQueue.append(seedMatch)
            for uuid in newUUIDS:
                for match in self.getMatchlist(uuid):
                    downloadQueue.append(match)
        
        return downloadQueue


    #----- Create download queue -----#
    # start with seed username
    # get uuid for the seed user
    # get matchlist for seed user
    # add matchIDs in matchlist to match download queue

    # once queue gets to len x...

    #----- Parse download -----#

    '''
    using tier and division, downloads matches for that rank until the program is stopped


    tier (string) - the tier to query, i.e. DIAMOND
    division (string) - the division to query, i.e. III
    page (int) - the page for the query to paginate to. Starts at 1.
    '''

    def createDownloadQueueV2(self, tier, division, page):

        #get list of summonerIds for specified tier and div
        leagueData = self.RIOT_API.league.entries(self.REGION_NA1, 'RANKED_SOLO_5x5', tier, division, page=page)
        summonerIds = []
        for summoner in leagueData:
            summonerIds.append(summoner['summonerId'])

        #use list of summonerIds to generate a puuid for each summonerId
        puuids = []
        for id in summonerIds:
            puuids.append( self.RIOT_API.summoner.by_id(self.REGION_NA1, id)['puuid'] )

        return self.matchlistFromPuuids(puuids)
        
        


    #using a list of puuids, generate a matchlist
    def matchlistFromPuuids(self, puuidList):

        matchList = []
        for puuid in puuidList:
            try:  
                matchList = matchList + self.RIOT_API.match.matchlist_by_puuid(  
                    self.REGION_AMERICAS, 
                    puuid, 
                    #Begin time currently unsupported by riotwatcher
                    #begin_time=float(1633546800), #12:00 PM on 10/6/21, start of patch 11.20
                    type='ranked',
                    start=0,
                    count=20
                )
            except ApiError:
                print('[ERROR] matchlist generation error. Bad puuid: ', puuid)
        return matchList
            
        
    #Using a username, returns the UUID for that username
    def getPuuidFromUsername(self, username):
        return self.RIOT_API.summoner.by_name(self.REGION_NA1, username)['puuid']

    #Using UUID, returns the last 20 matches for a given uuid
    def getMatchlist(self, puuid):
        return self.RIOT_API.match.matchlist_by_puuid(
            self.REGION_AMERICAS, 
            puuid, 
            type='ranked',
            start=0, 
            count=20
        )

    #Using a matchID, gets the match and returns the 10 uuids from the game
    def getUUIDs(self, matchId):
        uuids = []
        matchInfo = self.RIOT_API.match.by_id(region=self.REGION_AMERICAS, match_id=matchId)
        for participant in matchInfo['metadata']['participants']:
            uuids.append(participant)
        return uuids

