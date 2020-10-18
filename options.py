
def commands(values):
    if values == "turnonscreen":
        print("Screen is turned on")
    elif values == "turnoffscreen":
        print("Screen is turned off")
    elif values == "turnonprojector":
        print("Projector is on")
    elif values == "turnoffprojector":
        print("Projector is off")
    else:
        options()

def options():
    print("Please note i am still learning a lot of things. My developers are still adding new features.")
    print("Since i have a lot to learn why don't you try the below commands for the time being:")
    print("1: Touch Panel Turn On Screen")
    print("2. Touch Panel Turn Off Screen")
    print("3. Touch Panel Turn on Projector")
    print("4. Touch Panel Turn off projector")
    print("Please Try again by saying Touch Panel")
    return


