def reduct(model, attributes, dec) :
    k = model.konsistensi_tabel(attrs, dec)

    remove_attributes = [] 
    for a in attributes:
        R = remove_attributes.copy()
        R.append(a) 
        S = set(attributes) - set(R)
        k_s = model.konsistensi_tabel(list(S), dec)
        if k_s == k:
            remove_attributes.append(a)

    reduct = list(set(attributes) - set(remove_attributes))
    reduct.sort()
    return reduct, k, remove_attributes