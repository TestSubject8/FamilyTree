import sys,familytreeDefinition
def main():
    #   Checking if input file is present
    if len(sys.argv) != 2:
        print('Usage: python Lengabaru.py INPUT_FILE')
        exit()

    #   Setting up the family, using a similar input file to set up the existing family tree
    family = Lengaburu.get_members()    # Reference for all Person objects
    with open('setupFile.txt','r') as setupFile:
        for setup_command in setupFile.readlines():
            parse_input(setup_command, False)

    #   Starting the operations as specified in the input file - Second argument
    with open(sys.argv[1],'r') as inFile:
        for command in inFile.readlines():
            parse_input(command, True)

def parse_input(command, isVerbose):
    #   Reads the input file, and calls functions as required by the command
    #   Command line formats : COMMAND ARGUMENTS
    #   Arguments are expanded in the cases:
    if command == '' or command == '\n':
        pass
    params = command.split(' ')
    if(params[0] == "ADD_CHILD"):
        #   COMMAND MOTHER CHILD SEX
        Lengaburu.add_birth(params[1], params[2], params[3])
        if isVerbose:
            print('CHILD_ADDITION_SUCCESSFUL')
    elif(params[0] == "GET_RELATIONSHIP"):
        #   COMMAND PERSON RELATION
        relatives = Lengaburu.get_relation(params[1],params[2])
        if relatives == None or relatives == [] or relatives == [None]:
            #   No relatives match the search relation
            print('NONE')
        elif(relatives == 'NOTFOUND'):
            #   The source person does not exist
            print("PERSON_NOT_FOUND")
        else: 
            for person in relatives:
                print(person, end=' ')
            print()
    elif(params[0] == "ADD_SPOUSE"):
        #   COMMAND SPOUSE1 SPOUSE2 SPOUSE2_SEX
        #   SPOUSE_SEX is used when adding a marriage when one Person has to be created. 
        #   In such cases SPOUSE2 is the new Person to be created. 
        Lengaburu.add_marriage(params[1],params[2],params[3])
    else:
        pass

Lengaburu = familytreeDefinition.Family("Shan", "Anga")
main()
