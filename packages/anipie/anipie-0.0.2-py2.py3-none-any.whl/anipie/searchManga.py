import requests

class SearchManga:
    
    def __init__(self, search):
        self.search = search
        self.response = None
        self.mangaSearch()

    def mangaSearch(self):
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
                chapters
                volumes
                format
            }
        }
        '''
        self.variables = {
            'search' : self.search,
            'type' : 'MANGA',
        }
        self.url = 'https://graphql.anilist.co'
        self.response = requests.post(self.url, json={'query': self.query, 'variables': self.variables})

    def getMangaData(self):
        return self.response.json()

    def getMangaRomajiName(self):
        return self.response.json()['data']['Media']['title']['romaji']
    
    def getMangaEnglishName(self):
        return self.response.json()['data']['Media']['title']['english']

    def getMangaStatus(self):
        return self.response.json()['data']['Media']['status']
    
    def getMangaDescription(self):
        des = self.response.json()['data']['Media']['description']
        for i in (('<br>',''), ('<i>', ''), ('<i/>', ''), ('<br/>', ''), ('</i>', '')):
          des = des.replace(*i)

        return  des

    def getMangaStartDate(self):
        if self.response.json()['data']['Media']['startDate']['day'] == None:
            return "N/A"
        media = self.response.json()['data']['Media']
        return str(media['startDate']['month']) + '/' + str(media['startDate']['day']) + '/' + str(media['startDate']['year'])

    def getMangaEndDate(self):
        if self.response.json()['data']['Media']['endDate']['day'] == None:
            return "N/A"
        media = self.response.json()['data']['Media']
        return str(media['endDate']['month']) + '/' + str(media['endDate']['day']) + '/' + str(media['endDate']['year'])

    def getMangaCoverImage(self):
        return self.response.json()['data']['Media']['coverImage']['large']

    def getMangaGenres(self):
        genres = ", ".join(self.response.json()['data']['Media']['genres'])
        return genres
    
    def getMangaSiteUrl(self):
        return self.response.json()['data']['Media']['siteUrl']

    def getMangaVolumes(self):
        if self.response.json()['data']['Media']['volumes'] == None:
            return "N/A"
        return self.response.json()['data']['Media']['volumes']

    def getMangaChapters(self):
        if self.response.json()['data']['Media']['chapters'] == None:
            return "N/A"
        return self.response.json()['data']['Media']['chapters']

    def getMangaAverageScore(self):
        if self.response.json()['data']['Media']['averageScore'] == None:
            return "N/A"
        return int(self.response.json()['data']['Media']['averageScore']) / 10

    def getMangaFormat(self):
        if self.response.json()['data']['Media']['format'] == None:
            return "N/A"
        return self.response.json()['data']['Media']['format']

    def getMangaID(self):
        return self.response.json()['data']['Media']['id']