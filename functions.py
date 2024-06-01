import pyautogui # type: ignore
import pytesseract # type: ignore
from PIL import Image, ImageChops # type: ignore
import pytesseract # type: ignore
import time
import re
import numpy as np # type: ignore
import random

def print_fun_fact():
    fun_facts = [
        "This program uses the levenshtein distance function!",
        "The Robo Bear Challenge can give you Turpentine (more likely past round 20)!",
        "Make sure to save up those quest rerolls! You'll need them on the boss rounds...",
        "When in the quest picking menu, your bees are frozen in place.",
        "When you complete a round, your balloon blessing will refresh.",
        "Your final score is (5000 x Round Reached) + (1000 x Progress % made in round you lost) + (Total number of earned cogs)"
    ]
    print(f"\n     Fun Fact: {random.choice(fun_facts)}")

def get_image_size(picture):
    width, height = picture.size
    return [width, height]

def show_upgrade_dictionary(upgrade_dictionary):
    print("All documented upgrades:", "\n")
    for upgrade, value in upgrade_dictionary.items():
        print(f"'{upgrade}' is a {value} upgrade.")
    print("")

def click_on_pos(sleep, position):
    time.sleep(sleep)
    pyautogui.click(position)

def take_screenshot():
    screenshot = pyautogui.screenshot()
    screenshot.save("pics/current_screen.png")
    screenshot = Image.open("pics/current_screen.png")

def create_cropped_image(image_path, image_name, left, top, right, bottom):
    # Open the image
    image = Image.open(image_path)
    # Crop the image
    cropped_image = image.crop((left, top, right, bottom))
    cropped_image.save("pics/" + (f"{image_name}.png"))

def find_cog_amount():
    create_cropped_image("pics/current_screen.png", "cog_amount", 550, 720, 730, 800)
    cog_amount = find_picture_text(Image.open("pics/cog_amount.png"))
    return int(re.search(r'\d+', cog_amount).group())

def create_lock_images():
    for i in range(3):
        create_cropped_image("pics/current_screen.png", f"lock{i+1}", 1170, 300 + ((i+1) * 85), 1210, 350 + ((i+1) * 85))

def check_for_equal_image(img1_path, img2_path):
    img1 = Image.open(img1_path)
    img2 = Image.open(img2_path)
    # Check if the images have the same size and mode
    if img1.size != img2.size or img1.mode != img2.mode:
        return False

    # Check if the images are the same
    diff = ImageChops.difference(img1, img2)
    if diff.getbbox() is None:
        # Images are identical
        return True
    else:
        # Images are different
        return False

def contains_rgb_value(image_path, target_rgb):
    # Open the image
    img = Image.open(image_path)

    # Ensure the image is in RGB mode
    img = img.convert('RGB')

    # Get the dimensions of the image
    width, height = img.size

    # Iterate through each pixel
    for x in range(width):
        for y in range(height):
            # Get the RGB value of the current pixel
            current_rgb = img.getpixel((x, y))
            # Check if it matches the target RGB value
            if current_rgb == target_rgb:
                return True


    return False

def get_upgrade_name_pictures():
    create_cropped_image("pics/current_screen.png", "upgrades", 700, 270, 1215, 710)

    upgrade_name_top = 100
    upgrade_name_bottom = 130

    for upgradeNum in range(3):
        create_cropped_image("pics/upgrades.png", f"upgrade{upgradeNum+1}_name", 5, upgrade_name_top, 460, upgrade_name_bottom)
        upgrade_name_top += 85
        upgrade_name_bottom += 85

def find_picture_text(picture):
    text = pytesseract.image_to_string(picture)
    return text

def get_upgrade_names():
    upgrade_name_list = []
    for upgradeNum in range(3):
        try:
            upgrade_name_list.append(find_picture_text(Image.open(f"pics/upgrade{upgradeNum+1}_name.png")).split('[')[1].split(']')[0])
        except Exception:
            upgrade_name_list.append("No Upgrade Found")
    print(f"Upgrades found: {upgrade_name_list}", "\n")
    return upgrade_name_list

def create_upgrade_dictionary_from_txt(file_path):
    dictionary = {}
    with open(file_path, 'r') as file:
            
            for line in file:
                try:
                    # Remove leading/trailing whitespaces and newline characters
                    line = line.strip()
                    # Split the line at the '=' character
                    key, value = line.split('=')
                    # Add key-value pair to the dictionary
                    dictionary[key.strip()] = value.strip()
                except:
                    print("Error while creating upgrade list. Continuing... \n")

    return dictionary

def levenshtein_distance(s1, s2):
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)

    # len(s1) >= len(s2)
    if len(s2) == 0:
        return len(s1)

    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row

    return previous_row[-1]

def create_upgrade_dictionary_from_txt(file_path):
    dictionary = {}
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if '=' in line:
                key, value = line.split('=')
                dictionary[key.strip()] = value.strip()
    return dictionary

def determine_if_choosing_upgrade(upgrade_name_list, all_upgrades_dictionary):
    should_upgrade = []
    upgrade_true_names = []
    for upgrade_name in upgrade_name_list:
        found = False

        for upgrade, value in all_upgrades_dictionary.items():
            if upgrade.lower() == upgrade_name.lower() or levenshtein_distance(upgrade.lower(), upgrade_name.lower()) <= 1:
                found = True
                if value == "Good":
                    print(f"Marked upgrade '{upgrade}' to be taken.'")
                elif value == "Bad":
                    print(f"Marked upgrade '{upgrade}' to not be taken.")
                upgrade_true_names.append(upgrade)
                should_upgrade.append(value)
        
        if not found:
            print(f"Upgrade '{upgrade_name}' not found in the dictionary. As of the Retro Swarm Challenge Update all upgrades have been added, please check if this is an error or if there is just a new upgrade.")
            should_upgrade.append("Bad")
    print("")
    return should_upgrade, upgrade_true_names

def get_upgrade(upgrade_num_minus_one,cog_amount,upgrade_true_names):

    cog_amount = find_cog_amount()
    upgrade_cost = int(get_upgrade_costs()[upgrade_num_minus_one])
    down_upgrade_multiplier = (upgrade_num_minus_one*85)
    lock_x_value = 1191
    upgrade_x_value = 1000
    y_value = (415 + down_upgrade_multiplier)

    lock_pos = (lock_x_value, y_value)
    upgrade_pos = (upgrade_x_value, y_value)

    if cog_amount >= upgrade_cost:
        click_on_pos(0.5, upgrade_pos)
        pass
    elif cog_amount < upgrade_cost:
        click_on_pos(0.5, lock_pos)
        print(f"Not enough cogs to get '{upgrade_true_names[upgrade_num_minus_one]}', locking it to get it next round.")

def get_upgrades(cog_amount,should_upgrade, upgrade_true_names):
    for index,value in enumerate(should_upgrade):
        if value == "Good":
            get_upgrade(index, cog_amount, upgrade_true_names)

def get_upgrade_costs():
    text = ""
    for i in range(3):
        text += find_picture_text(f"pics/upgrade{i+1}_name.png")
    # Split the text into lines
    lines = text.split('\n')

    # Initialize an empty list to store the cost values
    upgrade_costs = []

    # Regular expression to find the "Cost: <number>" pattern
    cost_pattern = re.compile(r'Cost:\s*(\d+)')

    # Iterate over each line and search for the pattern
    for line in lines:
        match = cost_pattern.search(line)
        if match:
            # Extract the numeric value and convert it to an integer
            cost = int(match.group(1))
            # Add the cost to the list
            upgrade_costs.append(cost)

    return upgrade_costs

def get_locked_upgrades(all_upgrades_dictionary,allow_auto_get_locked_upgrades):
    cog_amount = find_cog_amount()
    print(f"Cogs: {cog_amount}")
    upgrade_name_list = get_upgrade_names()
    should_upgrade, upgrade_true_names = determine_if_choosing_upgrade(upgrade_name_list, all_upgrades_dictionary)
    if allow_auto_get_locked_upgrades:
        for i in range(3):
            if contains_rgb_value(f"pics/lock{i+1}.png", (232,232,232)) == True:
                print("Found lock in use. Getting upgrade...")
                get_upgrade(i, cog_amount, upgrade_true_names)

def DO_UPGRADES(all_upgrades_dictionary, allow_auto_get_locked_upgrades):
    cog_amount = find_cog_amount()
    get_locked_upgrades(all_upgrades_dictionary,allow_auto_get_locked_upgrades) #this has much of the same as the lines below but i wanted the non-lock upgrade picking code to be clear

    take_screenshot()
    create_lock_images()
    get_upgrade_name_pictures()
    upgrade_name_list = get_upgrade_names()
    should_upgrade, upgrade_true_names = determine_if_choosing_upgrade(upgrade_name_list, all_upgrades_dictionary)

    get_upgrades(cog_amount,should_upgrade,upgrade_true_names)