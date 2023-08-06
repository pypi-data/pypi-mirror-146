class MDA():
    def __init__(self, df, attrs):
        self.dataset = df 
        self.attributes = attrs

    def __group(self, attr):
        g = dict()

        for index, row in self.dataset[[attr]].iterrows():
            if row[attr] not in g:
                g[row[attr]] = list() 
            g[row[attr]].append(index)
        
        return g
    
    def group(self):
        ind = dict()
        for attr in self.attributes:
            ind[attr] = self.__group(attr)

        return ind

    def calculate_dependency_attributes(self):
        m = dict()
        for val, glumps in self.group().items():
            m[val] = list()
            for val2, glumps2 in self.group().items():
                if val2 == val:
                    continue
                # m[val][val2] = 0

                # print(val2, val)
                ns = 0
                for ka, a in glumps.items():
                    set_a = set(a)
                    for kb, b in glumps2.items():
                        set_b = set(b)
                        if set_b.issubset(set_a):
                            ns = ns + len(set_b)
                m[val].append(ns/len(self.dataset))
            m[val].sort(reverse=True)
        
        return m
    
    def sort_attributes_by_dependency(self):
        remove = list()
        # identic = list()
        for attr, val in self.calculate_dependency_attributes().items():
            if attr in remove:
                continue

            for attr2, val2 in self.calculate_dependency_attributes().items():
                if attr2 in remove:
                    continue
                if attr == attr2:
                    continue
                i = 0 

                is_remove = False
                if val[i] == val2[i]:
                    is_remove= True

                while True:
                    if val[i] != val2[i]:
                        break; 

                    if i >= len(val)-1:
                        break
                    i = i + 1
                
                if is_remove == True:
                    if val[i] < val2[i]:
                        remove.append(attr)
                    else :
                        remove.append(attr2)
                        # if val[i] == val2[i]:
                        #     identic.append(attr)
        
        # print(identic)
        ''' Creating new list of attributes without the redundant one '''
        attr_order = dict()
        for attr, val in self.calculate_dependency_attributes().items():
            if attr not in remove:
                attr_order[attr] = val[0]

        ''' Mengurutkan dictionary '''
        return sorted(attr_order.items(), key=lambda x: x[1], reverse=True)    
    
    def run(self):
        return self.sort_attributes_by_dependency(), self.calculate_dependency_attributes()