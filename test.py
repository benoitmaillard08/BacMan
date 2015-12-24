import constantes

file = open(constantes.PLAYERS_DATAS, 'r')
t = file.read().split()

datas = []
for i in t:
    datas.append(tuple(i.split('%')))


    

print(datas)

file.close()


liste = [('nom1', 1, 'date1'), ('nom2',2,'date2'),('nom3', 3, 'date3'),
         ('nom4', 4, 'date4'),('nom5', 5, 'date5'),('nom6', 6, 'date6'),
         ('nom7', 7, 'date7'),('nom8', 8, 'date8'),('nom9', 9, 'date9'),
         ('nom10', 10, 'date10')]

