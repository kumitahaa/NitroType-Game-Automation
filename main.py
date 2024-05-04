# ------------- Import -------------
import undetected_chromedriver as uc
# from selenium import webdriver as uc
import time,yaml, random, os
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC




driver = ""
captcha_controller = 1
captcha_count = 0
race_count = 0


def init():
    global driver
    driver = uc.Chrome()


def add_extension(extension_dir='extension'):
    global driver
    options = Options()
    # Get the absolute path of the extension directory
    extension_path = os.path.abspath(extension_dir)
    options.add_argument("--disable-notifications")
    options.add_argument(f"--load-extension={extension_path}")
    driver = uc.Chrome(options=options)
    print("Extension Added...")
    print("="*50)



# ------------------- Opening WebPage ----------------------------------
def start():
    # driver.maximize_window()
    url = "https://www.nitrotype.com/login"
    driver.get(url)

    print("Opened webpage...")
    print("="*50)

# ---------------------------- Login User -----------------------------------
def login(username, password):
    print("Start of LOGIN function")
    if login_check():
        print("Logged In Successfully...")
        print("="*50)
        return 0
    try:
        user_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID,
        "username")))
        password_input = driver.find_element(By.ID,
        "password")
        login_btn = driver.find_element(By.XPATH,
        "/html/body/div[1]/div/div/main/div/section/div[2]/div/div[3]/form/button")
        try:
            user_input.clear()
            user_input.send_keys(username)
            password_input.clear()
            password_input.send_keys(password)
            try:
                login_btn.click()
                # print("Tried to Logged In...")
                check_captcha()
                # Check if Logged in properly
                if login_check():
                    print("Logged In Successfully...")
                    print("="*50)
                else:
                    login(username,password)
            except:
                print("Couldn't Click Login Btn")
                login(username,password)
        except:
            print("Couldn't send keys to Fields")
            login(username,password)
    except:
        print(f"Couldn't Find Login Fields..   :/   :(")
        print("=" * 50)
        login()
    
    print("End of LOGIN function")

    

def login_check():
    print("Start of CHECK_LOGIN function")
    try:
        race_btn =  WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.XPATH,
        "/html/body/div[1]/div/main/section/div[3]/div[2]/div[3]/div[1]")))
        print("End of CHECK_LOGIN function")
        return True
    # else:
    except:
        print("Not Logged In")

    print("End of CHECK_LOGIN function")
    return False
    
        

def check_captcha():
    print("Start of LOGIN function")
    try:
        captcha_appeared = WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.ID,"recaptcha-anchor-label")))
        print("Captcha Found...")
        print("Sleeping for 2 Seconds")
        time.sleep(2)
    except:
        print("No Capthca yet..")
    print("End of LOGIN function")
    
    
# ---------------------------- Open Game -----------------------------------
def start_race():
    global race_count
    race_count = race_count + 1
    print("=="*50)
    print(f"Starting Race# {race_count}...")
    print("=="*50)

    # print("Start of start_race function")
    driver.get("https://www.nitrotype.com/race")
    print("Race Started")
    # print("End of start_race function")


# ---------------------------- Play Game -----------------------------------
def play():
    print("Start of PLAY function")
    print("="*60)
    while True:
        # print("While Loop...")
        try:
            try:
                popup = WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.XPATH,"/html/body/div[4]/div/div[1]/div")))
                print("Found Error Popup at race.")
                print("Starting New Race")
                if race_count < max_race:
                    start_race()
                    continue
            except:
                try:
                    race_result = WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.XPATH,"/html/body/div[1]/div[2]/main/div/section/div/div[1]/div[2]/div[2]/div[1]/div")))
                    print("Race Results appeared.")
                    print("Starting New Race")
                    if race_count < max_race:
                        start_race()
                        continue
                except:
                    pass
            input_field = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH,"/html/body/div/div/main/div/section/div/div[3]/div[1]/div[1]/div[2]/input")))
            try:
                try:
                    text_type = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME,"dash"))).text.split("SITION")[1].strip()
                except:
                    print("The text couldn't be cleaned from the start.")
                
                print("="*15)
                print(f"Formatted:: {text_type.replace("\n", "")}")
                print("="*15)

                text_list = [text_type.replace("\n","")[i:i+chunk_size] for i in range(0, len(text_type), chunk_size)]

                for _ in range(disturb_accuracy + 20):
                    source_index = random.randint(0, len(text_list) - 1)
                    target_index = random.randint(0, len(text_list))
                    element_to_copy = text_list[source_index]
                    text_list.insert(target_index, element_to_copy)

                print(text_list) #========
                type_now(text_list)
            except:
                print("Can't Find All the text from the input field...")
        except:
            try:
                popup = WebDriverWait(driver, 0.5).until(EC.presence_of_element_located((By.XPATH,"/html/body/div[4]/div/div[1]/div")))
                print("End of race, starting again.")
                print("Starting New Race")
                if race_count < max_race:
                    start_race()
                    continue
                else:
                    print("REACHED TOTAL NUMBER OF RACES.... STOPPING NOW...")
                    break
            except:
                try:
                    input_field = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH,"/html/body/div/div/main/div/section/div/div[3]/div[1]/div[1]/div[2]/input")))
                    continue
                except:
                    print("Didn't Find The Input filed containing the Text")
                    print("Starting New Race")
                    if race_count < max_race:
                        start_race()
                        continue
                    else:
                        print("REACHED TOTAL NUMBER OF RACES.... STOPPING NOW...")
                        break


def type_now(text_list):
    print("Start of TYPING function")
    try:
        input_field = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH,"/html/body/div/div/main/div/section/div/div[3]/div[1]/div[1]/div[2]/input")))
        print(text_list)
        for chunk in text_list:
            try:
                input_field.send_keys(chunk)
                time.sleep(typing_wait_seconds)
            except Exception as e:
                print("="*15)
                print("Can't send keys.")
                print(f"Error: {e}")
                print("="*15)
    except:
        print("Can't find Input Field")

    print("End of TYPING function")

# --------------------- Getting User Input Details --------------------------------
def load_config(file_path = "config.yaml"):
    with open (file_path, "r") as file:
        data = yaml.safe_load(file)
    return data


def driver():
    global chunk_size, max_race, typing_wait_seconds, disturb_accuracy

#     # ------------------ Driver Function ---------------------
    config = load_config()
    user = config.get("user", None)
    password = config.get("password", None)
    chunk_size = config.get("chunk_size", None)
    typing_wait_seconds = config.get("typing_wait_seconds", None)
    max_race = config.get("max_race", None)
    disturb_accuracy = config.get("disturb_accuracy", None)

    print(f"""
    User:   "{user}"  ... 
    Password:   "{password}"  ...
    Chunk Size: "{chunk_size}" ...
    Typing Wait Seconds: "{typing_wait_seconds}" ...
    Max Race: "{max_race}" ...
    Disturb Accuracy: "{disturb_accuracy}" ...

""")
    print("=" * 50)

    # ---------- Start Function Here
    add_extension()
    start()

    # ---------- Login functions Here
    login(user, password)

    # ---------- Plat Game function
    start_race()

    play()

    print("Out of Main Loop")
    time.sleep(100)


# -------------- Driver Call --------------
try:
    driver()
finally:
    print("Quitting")
    driver.quit()