
def authenticate(username, password):
    
    # studnet auth
    if username == "jacksonv" and password == "JacksonV123!":  # Jackson Vail
        return ("student", "Jackson Vail")
   
    elif username == "perryson" and password == "PerrySon@456":  # Perry Soni
        return ("student", "Perry Soni")
    
    elif username == "fischerr" and password == "FischerR*909":  # Fischer Ray
        return ("student", "JFischer Ray")
    
    elif username == "panthera" and password == "PatheraL23?":  # Panthera Leon
        return ("student", "Panthera Leon")
   
    elif username == "elliotcr" and password == "ElliotC501!?":  # Elliot Cross
        return ("student", "Elliot Cross")
    
    # faculty auth
    elif username == "calumous" and password == "CalumOut%10%":  # Calum Oust
        return ("faculty", "Calum Oust")
    
    elif username == "milespar" and password == "Milespara11!":  # Miles Pardalis
        return ("faculty", "Miles Pardalis")
   
    elif username == "oliverme" and password == "OliverMe1234@":  # Oliver Meller
        return ("faculty", "Oliver Meller")
    
    # admin auth
    elif username == "lowdylkr" and password == "LowdyLake24&":  # Lowdy Laker
        return ("admin", "Lowdy Laker")
   
    elif username == "rowdyrdr" and password == "RowdyRad617#":  # Rowdy Raider
        return ("admin", "Rowdy Raider")

    # testing auth
    elif username == "test" and password == "test":
        return ("loading", "test test")

    else:
        return (None, None)
