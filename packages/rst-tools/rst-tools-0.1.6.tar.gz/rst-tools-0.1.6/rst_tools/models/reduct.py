def reduct(model, attrs, dec) :
    k = model.konsistensi_tabel(attrs, dec)

    # print("Konsistensi Tabel %f" % k)

    visited = []
    remove = []

    remove = [] 
    for a in attrs:
        R = remove.copy()
        R.append(a) 
        S = set(attrs) - set(R)
        k_r = model.konsistensi_tabel(list(S), dec)
        if k_r == k:
            remove.append(a)

    # print(remove)

    reduct = list(set(attrs) - set(remove))
    reduct.sort()
    return reduct, k, remove
    # print("The reduct is %s" % reduct)