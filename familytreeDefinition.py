class Person:
    def __init__(self, inName, inMother, inSex):
        #   Creates a person object. 
        #   Inputs: 
        #       inName: Name string
        #       inMother: Person object
        #       inSex: Sex character - M / F
        #   Output:
        #       Returns the person object
        inSex = inSex.strip()
        self.__name=inName
        self.__mother=inMother
        self.__sex=inSex
        self.__spouse=None
        if(inSex == 'F'):
            self.__children=[]
        return
    
    #   Interfaces:
    def get_name(self):
        return self.__name
    
    def get_mother(self):
        return self.__mother

    def get_sex(self):
        return self.__sex
    
    def get_spouse(self,sex='A'):
        #   Sex 'A' returns any spouse
        #   Sex 'M' or 'F' returns spouse of matching sex. 
        #   Sex parameter is for in-law traversal
        #   Input: Sex of the required spouse, 'A'ny, 'M'ale or 'F'emale
        #   output: Spouses Person object, (None if self is unmarried)
        if sex == 'A':
            return self.__spouse
        elif self.__spouse.get_sex() == sex:
            return self.__spouse
        else:
            return None
    
    def set_spouse(self, spouse):
        if(self.get_spouse() == None):
            self.__spouse = spouse
        else:
            print("Already set spouse to ", self.get_spouse())
        
    def get_child(self,sex='A'):
        #   Sex 'A' returns any children 
        #   Sex 'M' or 'F' returns children of matching sex. 
        #   If self is male, spouse is fetched, and children accessed through spouse.
        #   If female spouse does not exist, returns None
        #   Input : Sex of children required
        #   Output: List of childrens Person objects
        if(self.get_sex() == 'M'):  #   Handles case of being called on Father
            mother = self.get_spouse()
            if mother == None:
                return None
        else:
            mother = self
        required_children = []
        for child in mother.__children:
            if sex == 'A':
                required_children.append(child)
            elif child.get_sex() == sex:
                required_children.append(child)
        return required_children

    def get_sibling(self,sex):
        #   Sex 'A' returns any siblings
        #   Sex 'M' or 'F' returns siblings of matching sex. 
        #   Operates by fetching children of mother, calling get_child()
        #   Persons who are in the tree by way of marriage have no mother or siblings, so the function return None. 
        #   Input: Sex of siblings required
        #   Output: List of siblings Person objects
        mother = self.get_mother()
        if mother == None:
            return None
        all_siblings = mother.get_child(sex)
        if self in all_siblings:
            all_siblings.remove(self)
        return all_siblings

    def add_child(self, child):
        #   Adds a child object to the selfs __children list
        #   Input: Child object
        #   Output: Child object, to be added to the family's dict of members
        self.__children.append(child)
        return child        

    def find_relation(self, relationHops):
        #   Recursively traverses the list of relation hops to fetch family member(s)
        #   Input:
        #       relationHops: List of hops to reach the required relative(s)
        #           eg: Sister is : self-> Mother-> Daughters
        #   Output: 
        #       List of Person objects that reside at the end of the hops
        #   This function takes converts the list items to specific relation sequences.
        #   The name of the relation is translated into a sequence of function calls.
        #   These calls further traverse the list and return the person list at the end of the line. 
        #   Possible enhancement: 
        #   The relationHops list can be made into an object to aggregate all the parameters of the functions called within this function.
        #   Currently the function parameters are encoded into the relation names in the list. This can be improved by having Hop objects.   
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
        if result != None:
            resultSet.extend(result)
        if relationHops == []:
            if resultSet != []:
                all_relatives.extend(resultSet)
        else:
            if resultSet != [None] and resultSet != None and resultSet != []:
                for person in resultSet:
                    all_relatives.extend(person.find_relation(relationHops[1:]))
        return all_relatives

class Family:
    #   members is a static dictionary that maintains the names and objects of all the members of a given family. 
    #   This is how we can call functions on a particular person
    members = {}
    def __init__(self, inKingName, inQueenName):
        #   The family is defined with the King and Queen
        self.members[inKingName] = Person("King "+inKingName, None, 'M')
        self.members[inQueenName] = Person("Queen "+inQueenName, None, 'F')
        self.add_marriage("Shan","Anga")
    
    #Interfaces

    def get_members(self):
        return self.members

    def add_member(self, kid):
        self.members[kid.get_name()] = kid

    def add_marriage(self, spouse1Name, spouse2Name, spouseSex='N'):
        #   Marriage link is through the spouse relation of the Person objects
        #   Both spouses refer to each other
        #   When a spouse is to be created for the marriage, Spouse2 is the new Person, and an object is created.
        if spouse2Name not in self.members.keys():
            self.add_member(Person(spouse2Name,None,spouseSex))
        spouse1 = self.members[spouse1Name]
        spouse2 = self.members[spouse2Name]
        spouse1.set_spouse(spouse2)
        spouse2.set_spouse(spouse1)

        
    def add_birth(self, motherName, childName, sex):
        #   Adds a new child to the family. New Person object is added to the mothers __children list, and to the familys members dictionary
        #   Input:  Mothers name, Childs name, Childs Sex
        mother = self.members[motherName]
        if(mother.get_sex == 'M'):
            mother = mother.get_spouse()
        #print("adding kid to ", mother.get_name())
        kid = mother.add_child(Person(childName,mother,sex[0]))
        self.add_member(kid)
    
    def __get_relation_path(self, relation):
        #   This is called by Family.get_relation(), and given to Person.find_relation().
        #   It defines the path to be taken by Person.find_relation() to find the required family member(s). 
        #   Input:
        #       The name of the relation, the parts of the name seperated by '-' 
        #   Output:
        #       The list of hops to be taken to reach the required relation
        #   One case of In-Laws are handled specially, as they do not fit neatly into the translation structure of the other relations. The same traversal logic is still followed. 
        #   The other case is handled in the structure by reversing the language of the relation. This way the same translation logic can be followed. 
        #   Two hop-paths are generated for In-Laws, as there are two definitions for the relation. 
        #   Multiple paths are handled in Family.get_relation()
        #   This can be improved with the associated functions by making the hops Object based. 
        rel = relation.strip().lower()
        path = rel.split('-')
        all_paths = []
        path_steps = []
        if rel == 'sister-in-law':  #   Handling wives of siblings
            all_paths.append(['SiblingA','SpouseF'])
        if rel == 'brother-in-law': #   Handling brothers of siblings
            all_paths.append(['SiblingA','SpouseM'])
        for step in path:
            if step == 'mother' or step == 'maternal':
                path_steps.extend(['Mother'])
            elif step == 'father' or step == 'paternal':
                path_steps.extend(['Mother','SpouseA'])  #   Assuming father is always mother's husband
            elif step == 'brother' or step == 'uncle':  #   Assuming uncle always has maternal or paternal specified, so the parent hop is implied
                path_steps.extend(['SiblingM'])
            elif step =='sister' or step == 'aunt': #   Assuming parental hop is specified for aunt
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
        all_paths.append(path_steps)
        return all_paths
    
    def get_relation(self, personName, relation):
        #   Finds the relation of the person specified. 
        #   Starts the search on the Person object matching the name in the members object
        #   Input: 
        #       Persons name, whose relation is required (the source)
        #       The name of the relation required, names seperated by '-'
        #   Output:
        #       The list of names of people who satisfy the relation constraint on the given source
        #   This function is called by the main(), calls Family.__get_relation_path() to fetch the traversal path, then calls Person.find_relation() on all the path lists returned
        person = self.get_members().get(personName)
        if person == None:
            return 'NOTFOUND'
        relationPath = self.__get_relation_path(relation)
        all_relatives = []
        for path in relationPath:
            relativeList = person.find_relation(path) 
            if relativeList != None:
                all_relatives.extend(relativeList)
        if(all_relatives != []):
            relative_names = []
            for relative in all_relatives:
                relative_names.append(relative.get_name())
            return relative_names
        else:
            return None
