from searchAnime import SearchAnime as sa
from searchManga import SearchManga as sm
from searchUser import SearchUser as su


def testSearchAnime(name):
    anime = sa(name)
    # # print(anime.getAnimeData())

    print(anime.getAnimeEnglishName())
    print(anime.getAnimeRomajiName())
    print(anime.getAnimeDescription())
    print(anime.getAnimeEpisodes())
    print(anime.getAnimeStatus())
    print(anime.getAnimeStartDate())
    print(anime.getAnimeEndDate())
    print(anime.getAnimeAverageScore())
    print(anime.getAnimeGenres())
    print(anime.getAnimeCoverImage())
    print(anime.getAnimeSiteUrl())
    print(anime.getAnimeSeason())
    print(anime.getAnimeFormat())

    print("=========================================")

def testSearchManga(name):
    manga = sm(name)
    # print(manga.getMangaData())
    print(manga.getMangaEnglishName())
    print(manga.getMangaRomajiName()) 
    print(manga.getMangaDescription()) 
    print(manga.getMangaStatus())
    print(manga.getMangaStartDate())
    print(manga.getMangaEndDate())
    print(manga.getMangaAverageScore())
    print(manga.getMangaGenres())
    print(manga.getMangaCoverImage())
    print(manga.getMangaSiteUrl())
    print(manga.getMangaChapters())
    print(manga.getMangaVolumes())
    print(manga.getMangaFormat())

    print("=========================================")

def testSearchUser(name):
    user = su(name)
    # print(user.getUserData())
    print(user.getUserAvatar())
    print(user.getUserAbout())
    print(user.getUserName())
    print(user.getUserFavouritesAnime())
    print(user.getUserFavouritesManga())

    print("=========================================")

def statisticTestAnime():
    a = sa("Ano hana")
    count = 0
    if a.getAnimeEnglishName().startswith("Anohana"): count += 1
    if a.getAnimeRomajiName() == 'Ano Hi Mita Hana no Namae wo Bokutachi wa Mada Shiranai.': count += 1
    if a.getAnimeDescription().startswith('Jinta'): count += 1
    if a.getAnimeEpisodes() == 11: count += 1
    if a.getAnimeStatus() == 'FINISHED': count += 1
    if a.getAnimeStartDate() == '4/15/2011': count += 1
    if a.getAnimeEndDate() == '6/24/2011': count += 1
    if a.getAnimeAverageScore() == 8.1: count += 1
    if a.getAnimeGenres() == 'Drama, Romance, Slice of Life, Supernatural': count += 1
    if a.getAnimeCoverImage() == 'https://s4.anilist.co/file/anilistcdn/media/anime/cover/medium/bx9989-qCd2RgAL0P8I.png': count += 1
    if a.getAnimeSiteUrl() == 'https://anilist.co/anime/9989': count += 1
    if a.getAnimeSeason() == 'SPRING': count += 1
    if a.getAnimeFormat() == 'TV': count += 1

    print("Anime Test Passed : Ano hana") if count == 13 else print("Anime Test Failed")

def statisticTestManga():
    m = sm("Citrus")
    count = 0
    if m.getMangaEnglishName().startswith("Citrus"): count += 1
    if m.getMangaRomajiName() == 'Citrus': count += 1
    if m.getMangaDescription().startswith('Citrus'): count += 1
    if m.getMangaStatus() == 'FINISHED': count += 1
    if m.getMangaStartDate() == '11/17/2012': count += 1
    if m.getMangaEndDate() == '8/18/2018': count += 1
    if m.getMangaAverageScore() == 7.1: count += 1
    if m.getMangaGenres() == 'Drama, Romance': count += 1
    if m.getMangaCoverImage() == 'https://s4.anilist.co/file/anilistcdn/media/manga/cover/medium/nx80145-PeU7lVLC4d4Z.jpg': count += 1
    if m.getMangaSiteUrl() == 'https://anilist.co/manga/80145': count += 1
    if m.getMangaChapters() == 50: count += 1
    if m.getMangaVolumes() == 10: count += 1
    if m.getMangaFormat() == 'MANGA': count += 1

    print ("Manga Test Passed : Citrus") if count == 12 else print("Manga Test Failed")

