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

def parse_input(command):
    if command == '':
        pass


main()