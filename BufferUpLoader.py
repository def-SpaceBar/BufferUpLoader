import time
import pandas as pd
import requests
from selenium.webdriver import Keys
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import random
import hashtags_aliexpress as hashtags


max_posts = 10
base_folder = 'C:\\Users\\$\\$\\$\\$\\'
media_name = 'pin_image.png'
account_manager = 'acc_man.csv'
product_manager = 'prod_man.csv'

api = '' ## Str: API Key
channelid_updates = '' ## Str: Channel ID
baseurl_sendmsg = f'https://api.telegram.org/bot{api}/sendMessage'

# csv columns of prod_man.csv#
csv_product_link = 'Tracking url' ## Str: Destination URL for the affiliation post
csv_product_name = 'Product Name' ## Str: Name of the product for the post data

# csv columns of acc_man.csv#
csv_pinterest_username = 'Username' ## Str: Pinterest Account @Username
csv_buffer_email = 'Email'     ## Str: Buffer Account Email
csv_buffer_password = 'Password' ## Str: Buffer Account Password
csv_buffer_twitter = 'TwitterID' ## Str: The Twitter's account ID in Buffer.com
csv_target_board = 'Main Board' ## Str: Pinterest Board Selection

def sendUpdate(msg):
    update_payload = {
        'chat_id': channelid_updates,
        'text': msg,
    }
    requests.post(baseurl_sendmsg, data=update_payload)


def download_image(image_url, image_filename):
    response = requests.get(image_url)
    if response.status_code == 200:
        with open(image_filename, "wb") as file:
            file.write(response.content)
        print("Image downloaded successfully.")
    else:
        print(f"Failed to download image. Status code: {response.status_code}")

def slow_type(element, text, delay=0.22):
    for character in text:
        element.send_keys(character)
        time.sleep(delay)


def removed_used_entries(prod_man, entries_to_remove):
    for key in list(prod_man.keys())[:entries_to_remove]:
        prod_man.pop(key)
    new_keys = list(range(1, len(prod_man) + 1))
    old_keys = sorted(prod_man.keys())
    for new_key, old_key in zip(new_keys, old_keys):
        if new_key != old_key:
            prod_man[new_key] = prod_man.pop(old_key)
    return prod_man


def random_hashtags(hashtags1, hashtags2, hashtags3):
    rn = random.randint(0, 4)
    hashtags1 = hashtags1[rn]
    hashtags2 = hashtags2[rn]
    hashtags3 = hashtags3[rn]
    return hashtags1, hashtags2, hashtags3


def buffer_loader(prod_man, max_posts, email, password, base_folder, pinterest_username, target_board,
                  twitter_buffer_id, media_name):
    def get_Image(image_url, media_name):
        response = requests.get(image_url)
        if response.status_code == 200:
            with open(f'{base_folder}media\\{media_name}', "wb") as file:
                file.write(response.content)
            print("ok")
        else:
            print(f"failed {response.status_code}")

    chrome_options = Options()
    chrome_options.add_argument("--lang=en-US")
    # chrome_options.add_argument(f'--proxy-server={proxy}:{port}')
    chrome_options.add_argument(
        f'User-Agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36')
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(f'https://buffer.com/')
    WebDriverWait(driver, 1000).until(
        lambda driver: driver.find_element(By.XPATH, "//a[contains(., 'Log in')]")).click()
    email_input = WebDriverWait(driver, 10).until(
        lambda driver: driver.find_element(By.XPATH, "//input[contains(@type, 'email')]"))
    slow_type(email_input, email)
    time.sleep(0.3)
    password_input = WebDriverWait(driver, 10).until(
        lambda driver: driver.find_element(By.XPATH, "//input[contains(@type, 'password')]"))
    slow_type(password_input, password)
    time.sleep(3)
    WebDriverWait(driver, 1000).until(
        lambda driver: driver.find_element(By.XPATH, "//button[contains(., 'Log In')]")).click()
    time.sleep(3)

    pc = 0
    for p in prod_man:
        imported_hashtags_list = random_hashtags(hashtags.hashtags_1, hashtags.hashtags_2, hashtags.hashtags_3)
        hashtag_list = f'{imported_hashtags_list[0]} {imported_hashtags_list[1]} {imported_hashtags_list[2]} #Affiliate #Aliexpress'
        print(pc)
        if pc == max_posts:
            break
        else:
            get_Image(prod_man[p]['Product Image Url'], media_name)
            driver.get(f'https://publish.buffer.com/profile/{twitter_buffer_id}')
            time.sleep(2)
            WebDriverWait(driver, 1000).until(
                lambda driver: driver.find_element(By.XPATH, "//button[contains(., 'Create Post')]")).click()
            WebDriverWait(driver, 1000).until(
                lambda driver: driver.find_element(By.XPATH, "//div[contains(@role, 'textbox')]")).send_keys(
                prod_man[p]['Product Name'], ' ', hashtag_list, Keys.ENTER, Keys.ENTER, prod_man[p]['Tracking url'])
            time.sleep(3)
            WebDriverWait(driver, 3000).until(lambda driver: driver.find_element(By.XPATH,
                                                                                 "//input[contains(@data-testid, 'uploads-dropzone-input')]")).send_keys(
                f'{base_folder}media\\pin_image.png')
            time.sleep(25)
            WebDriverWait(driver, 10).until(lambda driver: driver.find_element(By.XPATH,
                                                                               f"//button[contains(@aria-label, '{pinterest_username} pinterest Business')]")).click()
            time.sleep(1.5)
            WebDriverWait(driver, 1000).until(
                lambda driver: driver.find_element(By.XPATH, f"//button[contains(@title, '{target_board}')]")).click()
            time.sleep(5)

            WebDriverWait(driver, 1000).until(
                lambda driver: driver.find_element(By.XPATH, "//div[contains(@data-draftid, 'pinterest')]")).click()
            time.sleep(3)

            WebDriverWait(driver, 1000).until(
                lambda driver: driver.find_elements(By.XPATH, "//span[contains(@data-slate-leaf, 'true')]"))[3].clear()
            time.sleep(3)
            WebDriverWait(driver, 3000).until(
                lambda driver: driver.find_element(By.XPATH, "//input[contains(@name, 'pinTitle')]")).send_keys(
                prod_man[p]['Product Name'][:99])
            WebDriverWait(driver, 3000).until(
                lambda driver: driver.find_element(By.XPATH, "//input[contains(@name, 'destinationLink')]")).send_keys(
                prod_man[p]['Tracking url'])
            WebDriverWait(driver, 10).until(
                lambda driver: driver.find_element(By.XPATH, f"//button[contains(., 'Add to Queue')]")).click()
            print(f'uploaded {p}')
            time.sleep(10)
            pc = pc + 1
            driver.refresh()
    driver.delete_all_cookies()
    driver.close()

df = pd.read_csv(f'{base_folder}\\{product_manager}')
prod_man = df.to_dict(orient='index')
prod_man = {k + 1: v for k, v in prod_man.items()}

df2 = pd.read_csv(f'{base_folder}\\{account_manager}')
acc_man = df2.to_dict(orient='index')
acc_man = {k + 1: v for k, v in acc_man.items()}
print(acc_man)

for i in acc_man:
    sendUpdate(f"---------\nRunning.\n---------\nUploading to {acc_man[i][csv_pinterest_username]} \n Account Number: {i}")
    print(prod_man[1])
    buffer_loader(prod_man, max_posts,
                  acc_man[i][csv_buffer_email], acc_man[i][csv_buffer_password],
                  base_folder,
                  acc_man[i][csv_pinterest_username], acc_man[i][csv_target_board], acc_man[i][csv_buffer_twitter],
                  media_name)
    prod_man = removed_used_entries(prod_man, max_posts)
sendUpdate('done')
