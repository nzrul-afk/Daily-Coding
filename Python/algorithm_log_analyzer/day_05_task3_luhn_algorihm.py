def verify_card_number(id):
    id=id.replace(" ", "").replace("-","")

    ganjil=[]
    genap=[]
    for i in range(1, len(id)):
        if i % 2 == 0:
            genap.append(int(id[len(id) - i]))
        if i % 2 != 0:
            ganjil.append(int(id[len(id) - i]))
    for i in range(len(genap)):
        genap[i] = genap[i] * 2
        if genap[i] >= 10:
            genap[i] = str(genap[i])
            genap[i] = int(genap[i][0]) + int(genap[i][1])

    print(sum(genap))
    print(sum(ganjil))
    hasil = sum(genap) + sum(ganjil) 
    print(hasil)
    if hasil % 10 == 0:
        return "VALID!"
    else:
        return "INVALID"
        

print(verify_card_number('453914881'))
print(verify_card_number('4111-1111-1111-1111'))