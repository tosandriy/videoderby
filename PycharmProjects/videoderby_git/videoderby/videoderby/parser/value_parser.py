def value_parser_func():
    from videoderby import models
    with open("videoderby/parser/result.txt",encoding='utf-8') as file:
        lines = file.readlines()
        for line in lines:
            split_list = line[:-1].split("!-=-!")
            for count in range(len(split_list)):
                if count == 0:
                    namee = split_list[0]
                elif count == 1:
                    yearr = split_list[1]
                elif count == 2:
                    genree = split_list[2]
                elif count == 3:
                    descriptionn = split_list[3]
                elif count == 4:
                    actorss = split_list[4]
                elif count == 5 :
                    directorr = split_list[5]
                elif count == 6 :
                    timee = split_list[6]
                elif count == 7 :
                    ratingg = split_list[7]
                elif count == 8 :
                    countriess = split_list[8]
                elif count == 9 :
                    idd = split_list[9]
                elif count == 10 :
                    compositorr = split_list[10]
                elif count == 11 :
                    posterr = split_list[11]
                elif count == 12 :
                    imagess = split_list[12]

            imagess = str(imagess).replace("[","").replace("]","").replace("'","").split(", ")[:8]
            countriess = str(countriess).replace("[","").replace("]","").replace("'","").split(", ")
            directorr = str(directorr).replace("[","").replace("]","").replace("'","").split(", ")
            genree = str(genree).replace("[","").replace("]","").replace("'","").split(", ")
            actorss = str(actorss).replace("[","").replace("]","").replace("'","").split(", ")
            directorr = str(directorr).replace("[","").replace("]","").replace("'","").split(", ")
            compositorr = str(compositorr).replace("[","").replace("]","").replace("'","").split(", ")
            models.create_movie("https:" + posterr, namee, yearr , genree, descriptionn, actorss,
                                directorr, timee.split()[0], ratingg, countriess, idd, imagess, compositorr)
            print(namee)
            print(directorr)
            print(actorss)