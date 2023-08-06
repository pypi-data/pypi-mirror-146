import requests

class SearchUser:
    
    def __init__(self, name):
        self.name = name
        self.response = None
        self.userSearch()

    def userSearch(self):
        self.query = '''
        query ($search: String!) { 
            User(search: $search){
                name
                avatar {
                large
                }
                about
                siteUrl
                favourites{
                anime {
                    nodes{
                        title {
                            english
                        }
                    }
                }
                manga{
                    nodes{
                        title{
                            english
                        }
                    }
                }
                }
            }
        }
        '''
        self.variables = {
            'search' : self.name,
        }
        self.url = 'https://graphql.anilist.co'
        self.response = requests.post(self.url, json={'query': self.query, 'variables': self.variables})

    def getUserData(self):
        return self.response.json()


    def getUserName(self):
        return self.response.json()['data']['User']['name']
    
    def getUserAvatar(self):
        return self.response.json()['data']['User']['avatar']['large']
    
    def getUserAbout(self):
        return self.response.json()['data']['User']['about']

    def getUserFavouritesAnime(self):
        fav = self.response.json()['data']['User']['favourites']['anime']['nodes']
        aniFav = []
        for i in range(len(fav)):
            aniFav.append(str(fav[i]['title']['english']))
        ani = ", ".join(aniFav)
        return ani

    def getUserFavouritesManga(self):
        fav = self.response.json()['data']['User']['favourites']['manga']['nodes']
        manFav = []
        for i in range(len(fav)):
            manFav.append(fav[i]['title']['english'])
        man = ", ".join(manFav)
        return man

    def getUserEntriesFavAnime(self):
        fav = self.response.json()['data']['User']['favourites']['anime']['nodes']
        aniFav = []
        for i in range(len(fav)):
            aniFav.append(str(fav[i]['title']['english']))
        return len(aniFav)

    def getUserEntriesFavManga(self):
        fav = self.response.json()['data']['User']['favourites']['manga']['nodes']
        manFav = []
        for i in range(len(fav)):
            manFav.append(fav[i]['title']['english'])
        return len(manFav)

    def getUserSiteUrl(self):
        return self.response.json()['data']['User']['siteUrl']