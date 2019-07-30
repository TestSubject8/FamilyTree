import sys,familytreeDefinition
def main():
    #   Setting up the family
    Lengaburu = familytreeDefinition.Family("Shan", "Anga")
    family = Lengaburu.get_members()    # Reference for all operations
    with open(setupFile.txt,'r') as setupFile:
        for setup_command in setupFile.readlines()
            parse_input(setup_command)

    #   Starting the operations as specified in the input file
    with inFile as open(sys.argv[1],'r'):
        for command in inFile.readlines():
            parse_input(command)

    print("Setup of tree done. Here they are:")
    for children in family["Shan"].get_child():
        print(children.get_name(),end=', ') #   TODO: Add a tree traversal here
    print()

def parse_input(command):
    if command == '':
        pass
    params = command.split(' ')
    if(params[0] == "ADD_CHILD"):
        Lengaburu.add_birth(params[1], params[2], params[3])
    elif(params[0] == "FIND_RELATIONSHIP"):
        print("The ", params[2], " of ", params[1], " is : ", end='')
        print(Lengaburu.get_relation(params[1],params[2]))
    elif(params[0] == "ADD_SPOUSE"):
        Lengaburu.add_marriage(params[1],params[2])
    else:
        print("You've given me a command I don't understand :(")


main()