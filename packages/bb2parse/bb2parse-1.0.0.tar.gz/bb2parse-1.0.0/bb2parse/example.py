f = open('Coach.txt', 'r')
wordarr = []
word = ''
for i in f:
    readcheck = False
    for j in i:
        if j == '<':
            readcheck = True
            if word != '  :  ':
                wordarr.append(word)
            word = ''
            continue
        if j == '/':
            readcheck = False
        if j == '>':
            word += '  :  '
            continue
        if readcheck == True:
            word += j


for i in wordarr:
    print(i)