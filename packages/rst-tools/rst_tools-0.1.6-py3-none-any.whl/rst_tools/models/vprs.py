from models.roughsets import QuickReduct, RoughSets 

class VariablePrecisionRoughSet(RoughSets): 
  def __init__(self, df, beta):
    self.beta = beta;
    self.dataset = df
    

  def lower_approximation(self, parameter, keputusan):
    lower_approximation = dict()
    X = self.kelompokan_berdasarkan_keputusan(keputusan)
    ind = self.kelompokan_berdasarkan_parameter(parameter)
    for key, concept in X.items():
      lower_approximation[key] = []
      for g in ind:
        intr = set(concept).intersection(set(g))
        e = 1 - len(intr)/len(g)
        if e <= self.beta: 
          lower_approximation[key] += g

    return lower_approximation

class QuickReductVPRS(QuickReduct):
  def __init__(self, rs):
    self.model = rs 

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