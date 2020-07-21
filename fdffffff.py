def shtuka():
    import requests
    from bs4 import BeautifulSoup
    import re
    data = []
    count = 0
    a = requests.get("https://geo.koltyrin.ru/strany_mira.php?cont=")
    soup = BeautifulSoup(a.text, 'html.parser')
    aa = soup.find_all("table", attrs={"class" : "list"})
    soup2 = BeautifulSoup(str(aa), 'html.parser')
    soup3 = BeautifulSoup(str(soup2.find_all("tr")[1 :]), 'html.parser')
    soup4 = BeautifulSoup(str(soup3.find_all("td")), 'html.parser')
    soup5 = BeautifulSoup(str(soup4.find_all("a", attrs={"href" : re.compile(r"country*")})), 'html.parser')
    soup6 = BeautifulSoup(str(soup5), "html.parser")
    for x in soup6.strings :
        if x not in "[, ]" :
            data.append((x,count))
            count += 1
    print(data)


if __name__ == "__main__":
    shtuka()