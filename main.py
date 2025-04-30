import requests
from bs4 import BeautifulSoup
import json

MODERATED_MUSIC_URL="https://www.smwcentral.net/?p=section&s=sm64music"
WAITING_MUSIC_URL="https://www.smwcentral.net/?p=section&a=list&s=sm64music&u=1&g=0"
allMusicData = list()
id = 0

def getMusicDataForPage(n=None):
    if n == None:
        r = requests.get(WAITING_MUSIC_URL)
    else:
        r = requests.get(f"https://www.smwcentral.net/?p=section&s=sm64music&u=0&g=0&n={n}&o=date&d=desc")
    soup = BeautifulSoup(r.content, 'html.parser')
    table = soup.find('table', class_='list')
    rows = table.find_all('tr')
    
    for row in rows:
        data = getMusicDataFromRow(row)
        global allMusicData
        allMusicData.append(data)

def getMusicDataFromRow(row):
    data = row.find_all('td')
    if len(data) > 0:
        global id
        id = id + 1
        name = data[0].find('a').text
        # splitName = re.split("[-~]", name, 1)
        # gameName = splitName[0]
        # try: 
        #     areaName = splitName[1]
        # except:
        #     areaName = None
        time = data[0].find('time').text
        nlist = data[1].text
        description = data[2].text
        authors = data[3].text
        downloadLink = data[5].find('a')['href']
        downloads = data[5].find('span').text.replace(' downloads', '').replace(' download', '').replace(',', '')
        music_data = {
            'id': id,
            'name': name,
            # 'game': gameName,
            # 'area': areaName,
            'time': time,
            'nlist': nlist,
            'description': description,
            'authors': authors,
            'downloads': int(downloads)
        }
        downloadMusicFile(name, downloadLink)
        return music_data

def downloadMusicFile(filename, link):
    r = requests.get(link, allow_redirects=True)
    filename = filename.replace(":", " ").replace("/", " ").replace("\\", " ").replace("\"", " ")
    
    try:
        open(f"{filename}.zip", "wb").write(r.content)
    except Exception as e:
        print(f"{e}: {filename} could not be created")
        
# Making a GET request
r = requests.get(MODERATED_MUSIC_URL)

# Parsing the HTML
soup = BeautifulSoup(r.content, 'html.parser')

pageList = soup.find('ul', class_='page-list')
pageListElements = pageList.find_all('li')

for pageListElement in pageListElements:
    n = pageListElement.text
    if n.isnumeric():
        getMusicDataForPage(n)
getMusicDataForPage()
allMusicData = list(filter(None, allMusicData))
jsonString = {
    'data': allMusicData
}
json_object = json.dumps(jsonString, indent=4)
with open('music.json', 'a+') as file:
    file.write(json_object)