import sys,familytreeDefinition
def main():
    #   Setting up the family
    family = Lengaburu.get_members()    # Reference for all operations
    with open('setupFile.txt','r') as setupFile:    
        for setup_command in setupFile.readlines():
            parse_input(setup_command, False)

    #   Starting the operations as specified in the input file
    with open(sys.argv[1],'r') as inFile:
        for command in inFile.readlines():
            parse_input(command, True)

def parse_input(command, isVerbose):
    if command == '' or command == '\n':
        pass
    params = command.split(' ')
    if(params[0] == "ADD_CHILD"):
        Lengaburu.add_birth(params[1], params[2], params[3])
        if isVerbose:
            print('CHILD_ADDITION_SUCCESSFUL')
    elif(params[0] == "GET_RELATIONSHIP"):
        #print("The ", params[2].strip(), " of ", params[1].strip(), " is : ", end='')
        relatives = Lengaburu.get_relation(params[1],params[2])
        if relatives == None or relatives == [] or relatives == [None]:
            print('NONE')
        elif(relatives == 'NOTFOUND'):
            print("PERSON_NOT_FOUND")
        else: 
            for person in relatives:
                print(person, end=' ')
            print()
    elif(params[0] == "ADD_SPOUSE"):
        Lengaburu.add_marriage(params[1],params[2],params[3])
    else:
        pass
        #print("You've given me a command I don't understand :(")

Lengaburu = familytreeDefinition.Family("Shan", "Anga")
main()
