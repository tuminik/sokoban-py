f = open('workfile', 'r')

list = []

for line in f:
    list.append(line)
	
table = []
for i in list:

	listAux = []
    for j in i:
        listAux.append(j)
	
    table.append(listAux)

f.close()
