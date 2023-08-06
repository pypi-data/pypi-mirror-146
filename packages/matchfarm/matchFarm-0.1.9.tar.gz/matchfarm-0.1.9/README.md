# Python match farm

Use python to scrape matches from the Riot APIs

## Sample usage

### Setup: 
```
from src.ingestor import Ingestor
from src.config import Config

API_KEY="<Riot API Key here>"

userConfig= Config(API_KEY)


test = Ingestor(userConfig)

print(test.REGION_NA1)

```


### Download fixed size
```
from src import ingestor
from src.config import Config
from src.download_Controller import Download_Controller
from src.local_download import Local_Download

configUser = Config("<Riot API Key here>")

downloadType = Local_Download()

ingestorEngine = ingestor.Ingestor(configUser)

downloader = Download_Controller(downloadType, ingestorEngine)

downloader.downloadFixed('Kascadian', 50)
```
