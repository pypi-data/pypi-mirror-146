from pandas import DataFrame 

class RoughSets(): 
  def __init__(self, df):
    self.dataset = df
    pass 

  def kelompokan_berdasarkan_parameter(self, parameter):
    data1 = self.dataset[parameter]
    data2 = self.dataset[parameter]

    
    visited = [] 
    ind = []
    for index1, row1 in data1.iterrows():
      
      if index1 not in visited:
        g = []
        g.append(index1)
        visited.append(index1)
        for index2, row2 in data2.iterrows():
          if index2 not in visited and row1.equals(other=row2):
            visited.append(index2)
            # print(index1, index2)
            g.append(index2)
        ind.append(g)


    return ind

  def kelompokan_berdasarkan_keputusan(self, keputusan): 
    dfX = DataFrame()
    dfX[keputusan] = self.dataset[keputusan]

    X = dict() 

    for index, row in dfX.iterrows():
      if row[keputusan] in X: 
        l = X[row[keputusan]]
        l.append(index)
      else: 
        X[row[keputusan]] = [index]

    return X

  def lower_approximation(self, parameter, keputusan):
    lower_approximation = dict()
    X = self.kelompokan_berdasarkan_keputusan(keputusan)
    
    ind = self.kelompokan_berdasarkan_parameter(parameter)
    # print(ind)
    for key, concept in X.items():
      lower_approximation[key] = []
      for g in ind:
        if set(g) <= set(concept):
          lower_approximation[key] += g

    return lower_approximation

  def upper_approximation(self, parameter, keputusan):
    upper_approximation = dict()
    X = self.kelompokan_berdasarkan_keputusan(keputusan)
    
    ind = self.kelompokan_berdasarkan_parameter(parameter)
    # print(ind)
    for key, concept in X.items():
      upper_approximation[key] = []
      for g in ind:
        if len(set(g).intersection(set(concept))) != 0:
          upper_approximation[key] += g

    return upper_approximation

  def alpha(self, parameter, keputusan) :
    la = self.lower_approximation(parameter, keputusan)
    ua = self.upper_approximation(parameter, keputusan)

    total = dict()
    for key, pos in la.items():
      total[key] = len(la[key])/len(ua[key])

    return total

  def konsistensi_tabel(self, parameter, keputusan): 
      positive_regions = []
      lo = self.lower_approximation(parameter, keputusan)

      # print(lo)
      for key, pos in lo.items():
          positive_regions += pos

      dep = len(positive_regions)/len(self.dataset.index)
      # print(dep)
      return dep



class QuickReduct():
  def __init__(self, rs):
    self.model = rs 
    pass

  def reduct(self, attributes, decision):
    k_c = self.model.konsistensi_tabel(attributes, decision)

    R = []
    while True:
      T = R 
      S = set(attributes) - set(R)
      for x in list(S):
        k_r_plus_x = self.model.konsistensi_tabel(R+[x], decision)
        k_t = self.model.konsistensi_tabel(T, decision)

        if k_r_plus_x > k_t:
          T = R+[x]
      R = T

      k_r = self.model.konsistensi_tabel(R, decision)

      if k_r == k_c: 
        break

    return R 