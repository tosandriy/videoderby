
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


def table_parser(actor_kp_id=None):
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


