from bs4 import BeautifulSoup
from selenium import webdriver
import time

def proxies_parser() :
    import requests
    from bs4 import BeautifulSoup
    list_of_proxies = []
    a = requests.get("https://sslproxies.org/")
    soup = BeautifulSoup(a.text, "html.parser")
    soup = soup.find("tbody")
    for row in soup.find_all("tr") :
        b = row.find_all("td")
        list_of_proxies.append(b[0].text + ":" + b[1].text)
    return list_of_proxies


def main() :
    name = None
    genre = None
    description = None
    actors = None
    director = None
    duration = None
    rating = None
    country = None
    kp_id = None
    images = None
    def get_name() :
        name = soup.find("span", attrs={"class" : "styles_title__2l0HH"})
        if name:
            return name.text
        return None

    def get_year() :
        year = soup.find("a", attrs={"class" : "styles_link__1N3S2"})
        if year:
            return year.text
        else:
            return None

    def get_poster() :
        poster = soup.find("img", attrs={"class" : "film-poster"})
        return poster["src"]

    def get_original_name() :
        original_name = soup.find("span", attrs={"class" : "styles_originalTitle__31aMS"})
        return original_name.text

    def get_all_countries() :
        testing = soup.find_all("div", attrs={"class" : "styles_row__2ee6F"})
        if len(testing) >= 2:
            testing = testing[1].find_all("a", attrs={"class" : "styles_link__1N3S2"})
        result = []
        if testing :
            for genre in testing :
                result.append(genre.text)
            return result
        return None

    def get_all_genres() :
        testing = soup.find_all("div", attrs={"class" : "styles_row__2ee6F"})
        if len(testing) >= 3:
            testing = testing[2].find_all("a", attrs={"class" : "styles_link__1N3S2"})
        result = []
        if testing :
            for genre in testing :
                result.append(genre.text)
            return result[:-2]
        return None

    def get_director() :
        result = []
        genres = soup.find_all("div", attrs={"class" : "styles_row__2ee6F"})
        if len(genres) >= 5:
            genres = genres[4].find_all("a", attrs={
                "class" : "styles_link__1N3S2"})
        if genres :
            for genre in genres :
                result.append(genre.text)
            return result
        return None

    def get_compositor() :
        result = []
        genres = soup.find_all("div", attrs={"class" : "styles_row__2ee6F"})
        if len(genres) > 8:
            for x in genres[8].find_all("a") :
                result.append(x.text)
            return result
        return None

    def get_rating() :
        if soup.find("span", attrs={"class" : "film-rating-value"}):
            return soup.find("span", attrs={"class" : "film-rating-value"}).text
        return None

    def get_time() :
        genres = soup.find_all("div", attrs={"class" : "styles_row__2ee6F"})

        if genres:
            genres = genres[-1].find("div", attrs={"class" : "styles_value__2F1uj"})
            return genres.text
        return None

    def get_description() :
        testing = soup.find("p", attrs={"class" : "styles_paragraph__2Otvx"})
        if testing :
            return testing.text.replace("\n","")

    def get_main_actors() :
        result = []
        actor_table = soup.find("ul", attrs={"class" : "styles_list__I97eu"})
        if actor_table:
            actors = actor_table.find_all("a")
            for x in actors :
                result.append(x.text)
            return result
        return None

    def get_film_img_url():
        result = []
        images = soup2.find_all("tr")[5]
        images = images.findAll("img")
        for image in images :
            result.append(image['src'])
        return result

    def get_cur_movie() :
        a = open("last_id.txt", "r").read()
        return int(a)

    def set_cur_movie(value) :
        open("last_id.txt", "w").write(value)

    movie = get_cur_movie()
    link = f"https://www.kinopoisk.ru/film/{movie}/"
    PATH = r"C:\Users\79508\bin\chromedriver.exe"
    driver = webdriver.Chrome(PATH)
    a = []
    with open("last_id.txt") as file :
        while 1 :
            while 1 :
                driver.get(link)
                if "404. Страница не найдена" in driver.page_source:
                    movie+=1
                    link = f"https://www.kinopoisk.ru/film/{movie}/"
                    continue
                if "Нам очень жаль, но запросы, поступившие с вашего IP-адреса, похожи на автоматические." in driver.page_source:
                    time.sleep(20)
                break
            try :
                a = driver.page_source
            except :
                pass
            try :
                soup = BeautifulSoup(a, "html.parser")
            except :
                continue
            name = get_name()
            year = get_year()
            genre = get_all_genres()
            description = get_description()
            actors = get_main_actors()
            director = get_director()
            duration = get_time()
            rating = get_rating()
            country = get_all_countries()
            kp_id = movie
            compositor = get_compositor()
            poster = get_poster()
            driver.get(f"https://www.kinopoisk.ru/film/{movie}/stills/")
            if not "404. Страница не найдена" in driver.page_source :
                soup2 = BeautifulSoup(driver.page_source,"html.parser")
                images = get_film_img_url()
            if not name and not genre:
                continue
            movie += 1
            set_cur_movie(str(movie))
            link = f"https://www.kinopoisk.ru/film/{movie}/"
            print(name,year, genre, description, actors, director, duration, rating, country, kp_id,compositor, poster,images)
            with open("result.txt","a",encoding="utf-8") as result_file:
                result_file.write("{}!-=-!{}!-=-!{}!-=-!{}!-=-!{}!-=-!{}!-=-!{}!-=-!{}!-=-!{}!-=-!{}!-=-!{}!-=-!{}!-=-!{}"
                                  .format(name, year, genre, description, actors, director, duration, rating, country, kp_id,compositor, poster,images))
                result_file.write("\n")


def main2() :
    name = None
    genre = None
    description = None
    actors = None
    director = None
    duration = None
    rating = None
    country = None
    kp_id = None
    images = None
    def get_name() :
        name = soup.find("span", attrs={"class" : "styles_title__2l0HH"})
        if name:
            return name.text
        return None

    def get_year() :
        year = soup.find("a", attrs={"class" : "styles_link__1N3S2"})
        if year:
            return year.text
        else:
            return None

    def get_poster() :
        poster = soup.find("img", attrs={"class" : "film-poster"})
        return poster["src"]

    def get_original_name() :
        original_name = soup.find("span", attrs={"class" : "styles_originalTitle__31aMS"})
        return original_name.text

    def get_all_countries() :
        testing = soup.find_all("div", attrs={"class" : "styles_row__2ee6F"})
        if len(testing) >= 2:
            testing = testing[1].find_all("a", attrs={"class" : "styles_link__1N3S2"})
        result = []
        if testing :
            for genre in testing :
                result.append(genre.text)
            return result
        return None

    def get_all_genres() :
        testing = soup.find_all("div", attrs={"class" : "styles_row__2ee6F"})
        if len(testing) >= 3:
            testing = testing[2].find_all("a", attrs={"class" : "styles_link__1N3S2"})
        result = []
        if testing :
            for genre in testing :
                result.append(genre.text)
            return result[:-2]
        return None

    def get_director() :
        result = []
        genres = soup.find_all("div", attrs={"class" : "styles_row__2ee6F"})
        if len(genres) >= 5:
            genres = genres[4].find_all("a", attrs={
                "class" : "styles_link__1N3S2"})
        if genres :
            for genre in genres :
                result.append(genre.text)
            return result
        return None

    def get_compositor() :
        result = []
        genres = soup.find_all("div", attrs={"class" : "styles_row__2ee6F"})
        if len(genres) > 8:
            for x in genres[8].find_all("a") :
                result.append(x.text)
            return result
        return None

    def get_rating() :
        if soup.find("span", attrs={"class" : "film-rating-value"}):
            return soup.find("span", attrs={"class" : "film-rating-value"}).text
        return None

    def get_time() :
        genres = soup.find_all("div", attrs={"class" : "styles_row__2ee6F"})

        if genres:
            genres = genres[-1].find("div", attrs={"class" : "styles_value__2F1uj"})
            return genres.text
        return None

    def get_description() :
        testing = soup.find("p", attrs={"class" : "styles_paragraph__2Otvx"})
        if testing :
            return testing.text.replace("\n","")

    def get_main_actors() :
        result = []
        actor_table = soup.find("ul", attrs={"class" : "styles_list__I97eu"})
        if actor_table:
            actors = actor_table.find_all("a")
            for x in actors :
                result.append(x.text)
            return result
        return None

    def get_film_img_url():
        result = []
        images = soup2.find_all("tr")[5]
        images = images.findAll("img")
        for image in images[:8] :
            result.append(image['src'])
        return result

    def get_cur_movie() :
        a = open("last_id.txt", "r").read()
        return int(a)

    def set_cur_movie(value) :
        open("last_id.txt", "w").write(value)

    movie = 505851
    link = f"https://www.kinopoisk.ru/film/{movie}/"
    PATH = r"C:\Users\79508\bin\chromedriver.exe"
    driver = webdriver.Chrome(PATH)
    a = []
    with open("last_id.txt") as file :
        for film in [505851,18102,689066,512673, 77443, 843650, 1235260, 1045582, 1042726, 1007842, 726753, 1025082, 462465,
                     472386, 1108683, 1007049, 20378, 494839, 1112539, 822709] :
            while 1 :
                link = f"https://www.kinopoisk.ru/film/{film}/"
                driver.get(link)
                if "404. Страница не найдена" in driver.page_source:

                    continue
                if "Нам очень жаль, но запросы, поступившие с вашего IP-адреса, похожи на автоматические." in driver.page_source:
                    time.sleep(20)
                break
            try :
                a = driver.page_source
            except :
                pass
            try :
                soup = BeautifulSoup(a, "html.parser")
            except :
                continue
            name = get_name()
            year = get_year()
            genre = get_all_genres()
            description = get_description()
            actors = get_main_actors()
            director = get_director()
            duration = get_time()
            rating = get_rating()
            country = get_all_countries()
            kp_id = film
            compositor = get_compositor()
            poster = get_poster()
            driver.get(f"https://www.kinopoisk.ru/film/{film}/stills/")
            if not "404. Страница не найдена" in driver.page_source :
                soup2 = BeautifulSoup(driver.page_source,"html.parser")
                images = get_film_img_url()
            if not name and not genre:
                continue
            print(name,year, genre, description, actors, director, duration, rating, country, kp_id,compositor, poster,images)
            with open("result.txt","a",encoding="utf-8") as result_file:
                result_file.write("{}!-=-!{}!-=-!{}!-=-!{}!-=-!{}!-=-!{}!-=-!{}!-=-!{}!-=-!{}!-=-!{}!-=-!{}!-=-!{}!-=-!{}"
                                  .format(name, year, genre, description, actors, director, duration, rating, country, kp_id,compositor, poster,images))
                result_file.write("\n")


if __name__ == "__main__" :
    main2()