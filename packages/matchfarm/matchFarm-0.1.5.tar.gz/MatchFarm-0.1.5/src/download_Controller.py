# cvache
# 10/6/21
# downloader.py

from . ingestor import Ingestor, ApiError
from . download import Download


class Download_Controller:
    
    def __init__(self, downloadConfig: Download, ingestorEngine: Ingestor):

        self.downloadConfig = downloadConfig
        self.REGION_AMERICAS = 'americas'
        self.ing = ingestorEngine


    #downloads matches infintly, stop by keyboard interrupt
    def downloadInfinite(self, tier, division):
        
        page = 1
        try:
            while(True):
                rankInfo = {
                    'tier' : tier,
                    'division' : division
                }
                print('[INFO] Downloading matches from ', tier, ' ', division, 'Page ', page)
                matchlist = self.ing.createDownloadQueueV2(tier, division, page)
                print('[INFO] Finished building list. Starting download...')
                self.downloadConfig.downloadMatchlist(matchlist, rankInfo=rankInfo)
                print('[INFO] Download finished.')
                page += 1


        except KeyboardInterrupt:
            print('Program ended')
            print('Tier: ', tier)
            print('Division: ', division)
            print('Current page: ', page)


    '''
    using a seed username and size, downloads that many matches

    seedUser (string) - a username to use as a seed i.e. Kascadian
    size (int) - the amount of matches to download
    '''
    def downloadFixed(self, seedUser, size):

        print('[INFO] Starting list creation')
        list = self.ing.createDownloadQueue(seedUser, listSize=size)
        print('[INFO] Finished creating list')

        self.downloadMatchlist(list)

    '''
    Given a matchlist, parse and clean it
    sends every match to another funtion, thus not breakign the stackflow
    
    matchlist (list) - list of matchIds to download
    '''
    def downloadMatchlist(self, matchlist, rankInfo=None):
        for match in matchlist:
            isMatch = True
            try:
                matchData = self.ing.RIOT_API.match.by_id(self.REGION_AMERICAS, match)
            except ApiError:
                print("[ERROR1] Error in downloading match ", match)
                isMatch=False
            except ConnectionError:
                print("[ERROR2] Error in downloading match ", match)
                isMatch=False
            
            if isMatch:
                #move matchId from metadata to root of object to expose for use as hash key
                matchData['matchId'] = matchData['metadata']['matchId']
                matchData['rankInfo'] = rankInfo
                del matchData['metadata']['matchId']

                #this needs to be a function call
                self.downloadConfig.download( matchData )
            else:
                #not sure if I need this but my c++ says add it anyway
                del matchData