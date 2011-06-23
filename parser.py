f = open('workfile', 'r')
list = []
listAux = []
table = []
for line in f:
    list.append(line)
for i in list:
    for j in i:
        listAux.append(j)
    table.append(listAux)
    listAux = []
print table
table.seek('@')
f.close()