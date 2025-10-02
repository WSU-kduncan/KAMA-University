
def authenticate(username, password):
    
    # studnet auth
    if username == "jacksonv" and password == "JacksonV123!":  # Jackson Vail
        return "student"
    elif username == "perryson" and password == "PerrySon@456":  # Perry Soni
        return "student"
    elif username == "fischerr" and password == "FischerR*909":  # Fischer Ray
        return "student"
    elif username == "panthera" and password == "PatheraL23?":  # Panthera Leon
        return "student"
    elif username == "elliotcr" and password == "ElliotC501!?":  # Elliot Cross
        return "student"
    # faculty auth
    elif username == "calumous" and password == "CalumOut%10%":  # Calum Oust
        return "faculty"
    elif username == "milespar" and password == "Milespara11!":  # Miles Pardalis
        return "faculty"
    elif username == "oliverme" and password == "OliverMe1234@":  # Oliver Meller
        return "faculty"
    # admin auth
    elif username == "lowdylkr" and password == "LowdyLake24&":  # Lowdy Laker
        return "admin"
    elif username == "rowdyrdr" and password == "RowdyRad617#":  # Rowdy Raider
        return "admin"

    else:
        return None
