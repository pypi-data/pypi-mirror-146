from src.download import Download
import json


class Local_Download(Download):
    def __init__(self):
        pass

    def hello():
        return "hello from download"

    

    '''
    Download matches to local (matches) folder

    match
    
    '''
    def download(self, matchData):
        with open("./matches/" + str(matchData['matchId']) + ".json", mode="w") as file:
            file.write( json.dumps( matchData, indent=4 ) )  