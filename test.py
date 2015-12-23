import constantes

file = open(constantes.PLAYERS_DATAS, 'r')
t = file.read().split()

datas = []
for i in t:
    datas.append(tuple(i.split('%')))


    

print(datas)

file.close()
