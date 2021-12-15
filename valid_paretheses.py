       tmp = [] # store ']})'
        dict = {'[':']', '{':'}','(':')'}
        for e in s:
            if e in dict.keys():
                tmp.append(dict[e])

            elif e in dict.values():
                if not tmp:
                    return False
                if e != tmp.pop():
                    return False
            else:
                return False
            
        return tmp ==[]
