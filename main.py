from functions import *
print("""





""")
# Update this path to where Tesseract-OCR is installed
pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
allow_auto_get_locked_upgrades = True
firstTime = True

def mainMenu(firstTime):
    global allow_auto_get_locked_upgrades
    all_upgrades_dictionary = create_upgrade_dictionary_from_txt("upgrades.txt")    
    if firstTime == False:
        print_fun_fact()
    userInput = input("""
    Welcome to the BSS RBC Blue Hive Helper! 
    Please type the number of the option you want to choose:
        [1] Start helper program (currently only works on upgrade selection screen) (make sure you're in fullscreen on roblox and that it's on your main monitor)
        [2] View upgrades and whether they are listed as good or bad upgrades
        [3] Re-create upgrade list (use if you added a new upgrade manually)
        [4] Review settings (these reset if you close the program)
        [5] Extra notes
    ---------------------------------------------------------------------------
    """)
    print("\n")
    if userInput == "1":
        all_upgrades_dictionary = create_upgrade_dictionary_from_txt("upgrades.txt")
        DO_UPGRADES(all_upgrades_dictionary, allow_auto_get_locked_upgrades)
        time.sleep(0.5)
        mainMenu(False)
    elif userInput == "2":
        print("\nFound upgrades: \n")

        with open("upgrades.txt", 'r') as file:
            for line in file:
                print(f"            {line}", end='')  # 'end' parameter avoids adding extra newlines

        print("")
        time.sleep(0.5)
        mainMenu(False)
    elif userInput == "3":
        all_upgrades_dictionary = create_upgrade_dictionary_from_txt("upgrades.txt")
        print("   Recreated upgrade dictionary. \n    Going back to main menu...")
        time.sleep(0.5)
        mainMenu(False)
    elif userInput == "4":
        userInput = input(f"""        
        Type a number to toggle the setting.
            [1] Auto Allow Get Locked Upgrades: {allow_auto_get_locked_upgrades}
            """)
        if str(userInput) == "1":
            allow_auto_get_locked_upgrades = not allow_auto_get_locked_upgrades
        time.sleep(0.5)
        mainMenu(False)
    elif userInput == "5":
        print("""
        THIS UPGRADE CHOOSING SYSTEM IS FLAWED.
        It is not perfect, I made it myself. Most of them should be right, but it is likely a couple of them are wrong.
        I tried to be conservative and put the some of the ones I thought were "good" as "bad" so you don't get any bad upgrades on accident.
            
        Sometimes, the upgrade list will show the wrong upgrade name, but still end up getting the name right.
        This is due to using a very simplified form of autocorrect.
        
        An upgrade not taken by the program does not necessarily mean that it is bad.
        It may just be a medium tier upgrade that the user should choose for themselves.
        """)
        time.sleep(0.5)
        mainMenu(False)


mainMenu(firstTime)