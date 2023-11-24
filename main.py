import json
import time
import colorama as cr
import json
import random
import pygetwindow as gw


from functions import clear
from pynput.keyboard import *
from selenium import webdriver
from selenium.webdriver.common.by import By

cr.init(autoreset=True)
Fore = cr.Fore

keyboard = Controller()

def set_new_user():
    username = input("Please enter your username: ")
    password = input("Please enter your password: ")

    browser = None
    while browser is None or browser not in ["Chrome", "Edge", "Safari", "Firefox"]:
        browser = input("Please input the name of a browser you have installed. Please enter the exact name you can see on the right! (Supported browsers: Chrome, Edge, Safari and Firefox):")

    data = {"username": username, "password": password, "browser": browser}

    with open("data/logindata.json", "w") as file:
        json.dump(data, file, indent=4)

    return username, password, browser


def get_login():
    print("-" * 50)
    print(Fore.CYAN + "Do you want to use the log-in data from the last session? ")
    answer = input("Type yes/y or no/n to continue: ").lower()

    if answer not in ["y", "yes", "n", "no"]:
        clear()
        print("-" * 50)
        print(Fore.RED + "This is not a valid answer, try again!")
        print("-" * 50)
        return get_login()

    if answer == "yes" or answer == "y":
        with open("data/logindata.json", "r") as file:
            data = json.load(file)
            username = data.get("username", None)
            password = data.get("password", None)
            browser = data.get("browser", None)

        if username is None or password is None or browser is None:
            print("-" * 50)
            print(Fore.RED + "There is no saved log-in data, please enter your credentials!")
            return set_new_user()

        return username, password, browser
    elif answer == "no" or answer == "n":
        data = set_new_user()
        username = data[0]
        password = data[1]
        browser = data[2]

        return username, password, browser


def set_time_and_error():
    print(Fore.CYAN + "Down below you can enter the typing speed and the % of error!")

    speed = None
    error = None
    num_of_units = None
    try:
        speed = float(input("How many characters per minute do you want to type?: ").replace(",", "."))
        error = float(
            input("How many mistakes do you want to make (in % - type without the % sign): ").replace(",", "."))
        speed = 1 / ((speed*1.1) / 60)
        num_of_units = int(input("How many units ('Lektionen') do you want to write?: "))
    except ValueError:
        clear()
        print("-" * 50)
        print(Fore.RED + "You have to input a valid number for all three values!")
        print("-" * 50)
        set_time_and_error()

    return speed, error, num_of_units


def main(login_data, typing_data):
    username = login_data[0]
    password = login_data[1]

    speed = typing_data[0]
    error = round(typing_data[1], 1)
    num_of_units = abs(typing_data[2])

    browser = login_data[2]

    match browser:
        case "Chrome":
            driver = webdriver.Chrome()
        case "Firefox":
            driver = webdriver.Firefox()
        case "Safari":
            driver = webdriver.Safari()
        case "Edge":
            driver = webdriver.Edge()
        case _:
            driver = None
            print(Fore.RED + "You current browser is not support or you entered the wrong name! Please try again!")
            login = get_login()
            typing = set_time_and_error()
            main(login, typing)

    driver.get('https://at4.typewriter.at/index.php')
    driver.maximize_window()

   
    time.sleep(2)
    driver.find_element(By.ID, "LoginForm_username").send_keys(username)
    driver.find_element(By.ID, "LoginForm_pw").send_keys(password)
    driver.find_element(By.NAME, 'yt0').click()
    
    for _ in range(num_of_units):
        time.sleep(2)
        driver.get("https://at4.typewriter.at/index.php?r=typewriter/runLevel")
        time.sleep(1)

        keyboard.tap(Key.space)
        time.sleep(1)

        text_field = driver.find_element(By.ID, "text_todo")
        text = text_field.text

        current = text[0]

        current_length = len(list(text))


        while current_length > 0:
            window = gw.getActiveWindow()
            window_title: str = window.title
            if not window_title.startswith("Typewriter") or window is None:
                time.sleep(3)
                continue

            mistake_index = random.randint(1, 1000)
            if mistake_index <= (error*10):
                keyboard.type('ẞ')
                continue
            keyboard.tap(current)
            text_field = driver.find_element(By.ID, "text_todo")
            text = text_field.text

            if current_length <= 1:
                break
            current = text[0]

            current_length = len(list(text))

            time.sleep(speed)


if __name__ == '__main__':
    login_data = get_login()
    typing_data = set_time_and_error()
    main(login_data, typing_data)

