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
    
    def get_spouse(self):
        return self.__spouse
    
    def set_spouse(self, spouse):
        if(self.get_spouse() == None):
            self.__spouse = spouse
        else:
            print("Already set spouse to ", self.get_spouse())
    
#    def get_child(self):
#        if(self.get_sex() == 'M'):
#            mom = self.get_spouse() #   Handles searching for a males children
#            return mom.get_child()
#        else:
#            return self.__children
        
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
                required_children.append(child)
        return required_children

    def get_sibling(self,sex):
        #print('Sibling',sex,'of',self.get_name())
        mother = self.get_mother()
        if mother == None:
            return None
        all_siblings = mother.get_child(sex)
        if self in all_siblings:
            all_siblings.remove(self)
        #print(all_siblings)
        return all_siblings

    def add_child(self, child):
        #print("Adding",child.get_name(),"to ",self.get_name())
        #print('CHILD_ADDITION_SUCCESSFUL')
        self.__children.append(child)
        return child

    def find_relation(self, relationHops):
        #print('Relative: ',self.get_name())
        if(relationHops == []):
            return [self]
        elif(relationHops[0] == 'Mother'):
            return self.get_mother().find_relation(relationHops[1:])
        elif(relationHops[0] == 'Spouse'):
            return self.get_spouse().find_relation(relationHops[1:])
        elif(relationHops[0] == 'Child'):
            return self.get_child()
        elif(relationHops[0][:-1] == 'Sibling'):    #   Compressing three comparisions into one, as the last character is actually a function parameter
            return self.get_sibling(relationHops[0][-1])
        elif(relationHops[0] == 'Daughter'):
            return self.get_child('F')
        elif(relationHops[0] == 'Son'):
            return self.get_child('M')
        else:
            pass
            print('find_relation missing: ',relationHops)

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
        path_steps = []
        for step in path:
            if step == 'mother' or step == 'maternal':
                step = ['Mother']
            elif step == 'father' or step == 'paternal':
                step = ['Mother','Spouse']
            elif step == 'brother' or step == 'uncle':  #   Assuming uncle always has maternal or paternal specified, so the parent hop is implied
                step = ['SiblingM']
            elif step =='sister' or step == 'aunt': #   Assuming parent hop is specified
                step = ['SiblingF']
            elif step == 'sibling' or step == 'siblings':
                step = ['SiblingA']
            elif step == 'In' or step == 'Law':
                pass    #   TODO - handle in-laws
            elif step == 'son':
                step = ['Son']
            elif step == 'daughter':    #   These two are added to maintain a standard. They are funtionally useless lines
                step = ['Daughter']
            elif step == 'son':
                step = ['Son']
            else:
                pass
            path_steps.extend(step)
        #print('Follow: ',path_steps)
        return path_steps
    
    def get_relation(self, personName, relation):
        person = self.members[personName]
        relationPath = self.__get_relation_path(relation)
        result = person.find_relation(relationPath)
        if(result != None):
            for relative in result:
                return relative.get_name()
        else:
            return "PERSON_NOT_FOUND"
