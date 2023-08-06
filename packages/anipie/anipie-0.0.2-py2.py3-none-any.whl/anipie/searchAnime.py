import requests

class SearchAnime:

    def __init__(self, search):
        self.search = search
        self.animeSearch()


    def animeSearch(self):
        self.query = '''
        query ($search: String! $type: MediaType!) { 
            Media (search: $search type: $type) { 
                id
                title {
                    romaji
                    english
                }
                status
                description
                averageScore
                startDate {
                    year
                    month
                    day
                }
                endDate {
                    year
                    month
                    day
                }
                coverImage {
                    large  
                }
                genres
                siteUrl
                episodes
                season
                format
            }
        }
        '''
        self.variables = {
            'search' : self.search,
            'type' : 'ANIME',
        }
        self.url = 'https://graphql.anilist.co'
        self.response = requests.post(self.url, json={'query': self.query, 'variables': self.variables})
    

    def getAnimeData(self):
        return self.response.json()

    def getAnimeRomajiName(self):
        return self.response.json()['data']['Media']['title']['romaji']

    def getAnimeEnglishName(self):
        return self.response.json()['data']['Media']['title']['english']
    
    def getAnimeStatus(self):
        return self.response.json()['data']['Media']['status']
    
    def getAnimeDescription(self):
        des = self.response.json()['data']['Media']['description']
        for i in (('<br>',''), ('<i>', ''), ('<i/>', ''), ('<br/>', ''), ('</i>', '')):
          des = des.replace(*i)

        return  des
    
    def getAnimeEpisodes(self):
        if self.response.json()['data']['Media']['episodes'] == None:
            return "N/A"
        return self.response.json()['data']['Media']['episodes']

    def getAnimeCoverImage(self):
        return self.response.json()['data']['Media']['coverImage']['large']
    
    def getAnimeGenres(self):
        genres = ", ".join(self.response.json()['data']['Media']['genres'])
        return genres
    
    def getAnimeSiteUrl(self):
        return self.response.json()['data']['Media']['siteUrl']

    def getAnimeStartDate(self):
        if self.response.json()['data']['Media']['startDate']['day'] == None:
            return "N/A"
        media = self.response.json()['data']['Media']
        return str(media['startDate']['month']) + '/' + str(media['startDate']['day']) + '/' + str(media['startDate']['year'])

    def getAnimeEndDate(self):
        if self.response.json()['data']['Media']['endDate']['day'] == None:
            return "N/A"
        media = self.response.json()['data']['Media']
        return str(media['endDate']['month']) + '/' + str(media['endDate']['day']) + '/' + str(media['endDate']['year'])

    def getAnimeAverageScore(self):
        return int(self.response.json()['data']['Media']['averageScore']) / 10


    def getAnimeSeason(self):
        if self.response.json()['data']['Media']['season'] == None:
            return "N/A"
        return self.response.json()['data']['Media']['season']

    def getAnimeFormat(self):
        if self.response.json()['data']['Media']['format'] == None:
            return "N/A"
        return self.response.json()['data']['Media']['format']

    def getAnimeID(self):
        return self.response.json()['data']['Media']['id']