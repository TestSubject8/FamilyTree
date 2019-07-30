class Person:
    def __init__(self, inName, inMother, inSex):
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
    
    def get_child(self):
        if(self.get_sex() == 'M'):
            mom = self.get_spouse()
            return mom.get_child()
        else:
            return self.__children

    def add_child(self, child):
        self.__children.append(child)
        return child
    
    def find_relation(self, relationHops):
        if(relationHops == ''):
            return person
        elif(relationHops[0] == 'M'):
            return self.get_mother()
        elif(relationHops[0] == None):
            return "Invalid"
        else:
            self.find_relation(self, relationHops[1:])
        return

class Family:
    members = {}
    def __init__(self, inKingName, inQueenName):
        self.members[inKingName] = Person("King "+inKingName, None, 'M')
        self.members[inQueenName] = Person("Queen "+inQueenName, None, 'F')
        self.add_marriage("Shan","Anga")
        
    def get_members(self):
        return self.members

    def add_marriage(self, spouse1Name, spouse2Name):
        #   TODO - Add logic to create a person for the spouse that doesn't exist - make it the second one always
        #          Add the gender of the spouse to the function call and the input file
        spouse1 = self.members[spouse1Name]
        spouse2 = self.members[spouse2Name]
        spouse1.set_spouse(spouse2)
        spouse2.set_spouse(spouse1)

    def add_member(self, kid):
        self.members[kid.get_name()] = kid
        
    def add_birth(self, motherName, childName, sex):
        mother = self.members[motherName]
        if(mother.get_sex == 'M'):
            mother = mother.get_spouse()
        #print("adding kid to ", mother.get_name())
        kid = mother.add_child(Person(childName,mother,sex))
        self.add_member(kid)
    
    def __get_relation_path(self, relation):
        #print("For mother")
        return 'M'
    
    def get_relation(self, personName, relation):
        person = self.members[personName]
        relationPath = self.__get_relation_path(relation)
        result = person.find_relation(relationPath)
        if(result != "Invalid"):
            return result.get_name()
