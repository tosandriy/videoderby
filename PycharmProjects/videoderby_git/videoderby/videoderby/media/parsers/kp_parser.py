from bs4 import BeautifulSoup
import requests
def actor_parser(file_to_parse="file.txt", actor_kp_id=None):
    from bs4 import BeautifulSoup
    import requests
    def career_func(text) :
        nonlocal career
        for x in text.findAll("a", text=True) :
            career.append(x.findAll(text=True)[0].split()[-1])
        return career

    def height_func(text) :
        return text.findAll("span", text=True)[0].findAll(text=True)[0]

    def birth_day_func(text) :
        nonlocal birth_day
        x = text.findAll("a", text=True)
        birth_day["day_month"] = x[0].findAll(text=True)[0]
        birth_day["year"] = x[1].findAll(text=True)[0]
        return birth_day

    def place_of_birth_func(text) :
        nonlocal place_of_birth
        x = text.findAll("a", text=True)
        for place in x :
            place_of_birth.append(place.findAll(text=True)[0])
        return place_of_birth

    def movie_count_func(text) :
        nonlocal movie_count
        movie_count = int(text.findAll("td")[1].findAll(text=True)[0].split()[0][:-1])
        return movie_count

    career = []
    height = ""
    birth_day = {}
    place_of_birth = []
    movie_count = 0
    if file_to_parse == "file.txt":
        with open(file_to_parse, "rb") as f:
            if actor_kp_id:
                a = requests.get(f"https://www.kinopoisk.ru/name/{actor_kp_id}/")
                soup = BeautifulSoup(a.text, "html.parser")
                a = soup.find_all("table", attrs={"class" : "info"})[0]
                a = list(a.find_all("tr"))
            else:
                a = f.read().decode("utf8")
                soup = BeautifulSoup(a, "html.parser")
                a = list(soup.find_all("tr"))
    else:
        a = file_to_parse
        soup = BeautifulSoup(a, "html.parser")
        a = list(soup.find_all("tr"))
        for part in a:
            if 'карьера' in str(part):
                career = career_func(part)
            elif '<td class="type">рост</td>' in str(part):
                height = height_func(part)
            elif '<td class="type">дата рождения</td>' in str(part):
                birth_day = birth_day_func(part)
            elif '<td class="type">место рождения</td>' in str(part):
                place_of_birth = place_of_birth_func(part)
            elif '<td class="type">всего фильмов</td>' in str(part):
                movie_count = movie_count_func(part)
    return career, height, birth_day, place_of_birth, movie_count


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


def table_parser(actor_kp_id=None) :
    from bs4 import BeautifulSoup
    import requests
    with open("file.txt", "rb") as f :
        if actor_kp_id :
            a = requests.get(f"https://www.kinopoisk.ru/name/{actor_kp_id}/")
            soup = BeautifulSoup(a.text, "html.parser")
            a = soup.find_all("table", attrs={"class" : "info"})[0]
            a = list(a.find_all("tr"))
        else :
            a = f.read().decode("utf8")
            soup = BeautifulSoup(a, "html.parser")
            a = list(soup.find_all("tr"))
    return a


def main():
    list_of_proxies = proxies_parser()
    career = []
    height = ""
    birth_day = {}
    place_of_birth = []
    movie_count = 0

    def career_func(text) :
        if text.findAll("a", text=True) :
            for xx in text.findAll("a", text=True) :
                career.append(xx.findAll(text=True)[0].split()[-1])
            return career
        else :
            return 0

    def height_func(text) :
        if text.findAll("span", text=True) :
            return text.findAll("span", text=True)[0].findAll(text=True)[0]
        else :
            return 0

    def birth_day_func(text) :
        xxx = text.findAll("a", text=True)
        if xxx :
            birth_day["day_month"] = xxx[0].findAll(text=True)[0]
            birth_day["year"] = xxx[1].findAll(text=True)[0]
            return birth_day
        else :
            return 0

    def place_of_birth_func(text) :
        xxxx = text.findAll("a", text=True)
        if xxxx :
            for place in xxxx :
                place_of_birth.append(place.findAll(text=True)[0])
            return place_of_birth
        else :
            return 0

    def movie_count_func(text) :
        if text.findAll("td") :
            movie_count = int(text.findAll("td")[1].findAll(text=True)[0].split()[0][:-1])
            return movie_count
        else :
            return 0

    def get_cur_movie() :
        a = open("last_id.txt", "r").read()
        return int(a)

    def set_cur_movie(value) :
        open("last_id.txt", "w").write(value)

    movie = get_cur_movie()
    cur_proxy = 1
    link = f"https://www.kinopoisk.ru/name/{movie}/"
    proxies = {
            "https" : list_of_proxies[cur_proxy],
            "http" : list_of_proxies[cur_proxy]
    }
    a = []
    with open("last_id.txt") as file:
        while 1:
            while 1:
                try :
                    a = requests.get(link, proxies=proxies)
                    print("connected")
                except :
                    proxies = {
                            "https" : list_of_proxies[cur_proxy],
                            "http" : list_of_proxies[cur_proxy],
                    }
                    cur_proxy += 1
                if a:
                    break
            if not type(a) == type(list()):
                a = a.text
            try:
                soup = BeautifulSoup(a, "html.parser")
            except:
                continue
            soup = soup.find("")
            a = list(soup.find_all("tr"))

            # Сам парсер
            for part in a :
                if 'карьера' in str(part) :
                    career = career_func(part)
                elif '<td class="type">рост</td>' in str(part) :
                    height = height_func(part)
                elif '<td class="type">дата рождения</td>' in str(part) :
                    birth_day = birth_day_func(part)
                elif '<td class="type">место рождения</td>' in str(part) :
                    place_of_birth = place_of_birth_func(part)
                elif '<td class="type">всего фильмов</td>' in str(part) :
                    movie_count = movie_count_func(part)
            if not career and not height and not birth_day and not place_of_birth and not movie_count :
                proxies = {
                        "https" : list_of_proxies[cur_proxy],
                        "http" : list_of_proxies[cur_proxy],
                }
                cur_proxy += 1
                continue
            movie += 1
            set_cur_movie(str(movie))
            link = f"https://www.kinopoisk.ru/name/{movie}/"
            print(career, height, birth_day, place_of_birth, movie_count,get_cur_movie())
            career = []
            height = ""
            birth_day = {}
            place_of_birth = []
            movie_count = 0
if __name__ == "__main__":
    main()