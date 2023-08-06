# cvache
# 10/6/21
# upload.py


import json

#takes a single match and uploads it to DB
#def uploadSingleMatch(matchData, rankInfo=None):
    #dynamoDB = boto3.resource('dynamodb', endpoint_url=config('DYNAMO'))
    #matchData = cleanData(matchData, rankInfo)

    #matchesTable = dynamoDB.Table('matches')

    #matchesTable.put_item(Item=matchData)
        
#TODO:
#takes a set of matches and uploads them to DB
# def uploadSetOfMatches(matches)


'''
    create match table in Dynamo. 

    Helper function for uploadSingleMatch()
'''
# def initMatchTable():
#     dynamoDB = boto3.resource('dynamodb', endpoint_url=config('DYNAMO'))

#     matchesTable = dynamoDB.create_table(
#         TableName='matches',
#         KeySchema=[
#             {
#                 'AttributeName': 'matchId',
#                 'KeyType': 'HASH'
#             }
#         ],
#         AttributeDefinitions=[
#             {
#                 'AttributeName': 'matchId',
#                 'AttributeType': 'S'
#             }
#         ],
#         ProvisionedThroughput={
#             'ReadCapacityUnits': 10,
#             'WriteCapacityUnits': 10
#         }
#     )

#     return matchesTable

# initMatchTable()

#Cleans match data 
'''
Takes matchId and exposes it to root of data
Adds rankInfo to root

'''


def downloadLocal(matchData, rankInfo=None):
    #matchData = cleanData(matchData)

    with open("matches/" + str(matchData['matchId']) + ".json") as file:
        file.write(json.dumps(matchData, indent=4))

