import familytreeDefinition
def main():
    Lengaburu = familytreeDefinition.Family("Shan", "Anga")
    Lengaburu.add_marriage("Shan","Anga")

    family = Lengaburu.get_members()

    print("Marriages:", family["Shan"].get_name(), " to ", family["Shan"].get_spouse().get_name())

    print("Adding a kid")
    Lengaburu.add_birth('Anga','Chit','M')
    print("Adding another kid")
    #Lengaburu.add_birth('Shan','Ish','M')
    Lengaburu.add_birth('Anga','Ish','M')

    print("These are the kids: ")
    for children in family["Shan"].get_child():
        print(children.get_name(),end=', ')
    print()


    print("Mother of first son: ", Lengaburu.get_relation("Chit",'Mother'))
    #print("Mother in law of first son: ", Lengaburu.get_relation("Chit",'Mother-in-law'))

main()