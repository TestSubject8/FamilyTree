class Person:
    def __init__(self, inName, inMother, inSex):
        inSex = inSex.strip()
        #print(inName,'#',inSex,'#')
        self.__name=inName
        self.__mother=inMother
        self.__sex=inSex
        self.__spouse=None
        if(inSex == 'F'):
            self.__children=[]
        # TODO: Add validation and cleanup, type and capitalization
        return
    
    def get_name(self):
        return self.__name
    
    def get_mother(self):
        return self.__mother

    def get_sex(self):
        return self.__sex
    
    def get_spouse(self,sex='A'):
        if sex == 'A':
            #print(self.__spouse.get_name(), 'spouse of', self.get_name())
            return self.__spouse
        elif self.__spouse.get_sex() == sex:
            #print(self.__spouse.get_name(), 'spouse of', self.get_name())
            return self.__spouse
        else:
            return None
    
    def set_spouse(self, spouse):
        if(self.get_spouse() == None):
            self.__spouse = spouse
        else:
            print("Already set spouse to ", self.get_spouse())
        
    def get_child(self,sex='A'):
        if(self.get_sex() == 'M'):  #   Handles case of being called on Father
            mother = self.get_spouse()
        else:
            mother = self
        #print(sex,'Child(s)','of',mother.get_name())
        required_children = []
        for child in self.__children:
            #print("Match:",child.get_name(),child.get_sex())
            if sex == 'A':
                required_children.append(child)
            elif child.get_sex() == sex:
#                print(child.get_sex())
                required_children.append(child)
        return required_children

    def get_sibling(self,sex):
        #print('Sibling',sex,'of',self.get_name())
        mother = self.get_mother()
        if mother == None:
            #print('Outsider')
            return None
        all_siblings = mother.get_child(sex)
        if self in all_siblings:
            all_siblings.remove(self)
#        print('Siblings:', all_siblings)
        return all_siblings

    def add_child(self, child):
        #print("Adding",child.get_name(),"to ",self.get_name())
        self.__children.append(child)
        return child        

    def find_relation(self, relationHops):
#        print('Relative: ',self.get_name(), 'to fetch:', relationHops)
        all_relatives = []
        resultSet = []
        if(relationHops == []):
            result = [self]
        elif(relationHops[0] == 'Mother'):
            result = [self.get_mother()]
        elif(relationHops[0][:-1] == 'Spouse'):
            result = [self.get_spouse(relationHops[0][-1])]
        elif(relationHops[0] == 'Child'):
            result = self.get_child()
        elif(relationHops[0][:-1] == 'Sibling'):    #   Compressing three comparisions into one, as the last character is actually a function parameter
            result = self.get_sibling(relationHops[0][-1])
        elif(relationHops[0] == 'Daughter'):
            result = self.get_child('F')
        elif(relationHops[0] == 'Son'):
            result = self.get_child('M')
        else:
            pass
#            print('find_relation missing: ',relationHops)
        if result != None:
            resultSet.extend(result)
#        print('resultset:', len(resultSet))
        if relationHops == []:
            if resultSet != []:
                all_relatives.extend(resultSet)
        else:
            if resultSet != [None] and resultSet != None and resultSet != []:
                for person in resultSet:
    
                    all_relatives.extend(person.find_relation(relationHops[1:]))
        return all_relatives

class Family:
    members = {}
    def __init__(self, inKingName, inQueenName):
        self.members[inKingName] = Person("King "+inKingName, None, 'M')
        self.members[inQueenName] = Person("Queen "+inQueenName, None, 'F')
        self.add_marriage("Shan","Anga")
        
    def get_members(self):
        return self.members

    def add_member(self, kid):
        self.members[kid.get_name()] = kid

    def add_marriage(self, spouse1Name, spouse2Name, spouseSex='N'):
        if spouse2Name not in self.members.keys():
            self.add_member(Person(spouse2Name,None,spouseSex))
        spouse1 = self.members[spouse1Name]
        spouse2 = self.members[spouse2Name]
        #print("Marry", spouse1Name, "and", spouse2Name)
        spouse1.set_spouse(spouse2)
        spouse2.set_spouse(spouse1)

        
    def add_birth(self, motherName, childName, sex):
        mother = self.members[motherName]
        if(mother.get_sex == 'M'):
            mother = mother.get_spouse()
        #print("adding kid to ", mother.get_name())
        kid = mother.add_child(Person(childName,mother,sex))
        self.add_member(kid)
    
    def __get_relation_path(self, relation):
        rel = relation.strip().lower()
        path = rel.split('-')
        all_paths = []
        path_steps = []
        if rel == 'sister-in-law':  #   Handling wives of siblings
            all_paths.append(['SiblingA','SpouseF'])
        if rel == 'brother-in-law':
            all_paths.append(['SiblingA','SpouseM'])
        for step in path:
            if step == 'mother' or step == 'maternal':
                path_steps.extend(['Mother'])
            elif step == 'father' or step == 'paternal':
                path_steps.extend(['Mother','SpouseA'])  #   Assuming father is always mother's husband
            elif step == 'brother' or step == 'uncle':  #   Assuming uncle always has maternal or paternal specified, so the parent hop is implied
                path_steps.extend(['SiblingM'])
            elif step =='sister' or step == 'aunt': #   Assuming parent hop is specified
                path_steps.extend(['SiblingF'])
            elif step == 'sibling' or step == 'siblings':
                path_steps.extend(['SiblingA'])
            elif step == 'in':
                path_steps.extend(['SpouseA'])
            elif step == 'law':
                path_steps.reverse()    #   Handling spouse's siblings within the path traversal by reversing the order 
            elif step == 'son':
                path_steps.extend(['Son'])
            elif step == 'daughter':    #   These two are added to maintain a standard. They are funtionally useless lines
                path_steps.extend(['Daughter'])
            elif step == 'son':
                path_steps.extend(['Son'])
            else:
                pass
            #path_steps.extend(step)
        all_paths.append(path_steps)
        #print('Follow: ',all_paths)
        return all_paths
    
    def get_relation(self, personName, relation):
        person = self.members[personName]
        relationPath = self.__get_relation_path(relation)
#        print(relationPath)
        all_relatives = []
        for path in relationPath:
            relativeList = person.find_relation(path) 
            if relativeList != None:
                all_relatives.extend(relativeList)
        #print(all_relatives)
        if(all_relatives != []):
            relative_names = []
            for relative in all_relatives:
                relative_names.append(relative.get_name())
            return relative_names
        else:
            return None
