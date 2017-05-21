# encoding=utf8
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import *
from PIL import Image
import os, sys, openpyxl, time, datetime


def login():
    # Trying loading seller center portal
    # Benchmark loading
    start_counter = time.time()

    for i in range(3):
        try:
            driver.get("https://www.gearbubble.com/users/sign_in")
            WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.CLASS_NAME, "form-title"))
            )
            print "[+] gearbubble loaded."
            break
        except (TimeoutException, NoSuchElementException) as err:
            print "[-] try again."

        if i == 3:
            print "[-] try another time."

    __user__ = ""
    __pwd__ = ""
    setting_read = open("config.txt", "r")
    login_data = setting_read.readlines()
    for elm_login_data in login_data:
        if "username" in elm_login_data:
            __user__ = elm_login_data.split("=")[1]
        elif "password" in elm_login_data:
            __pwd__ = elm_login_data.split("=")[1]
        else:
            continue

    print "-------------------"
    print "[+] site loading time: " + str(time.time() - start_counter)
    print "-------------------"
    #
    # --------------------------------------------------------------

    # Login
    # Benchmark login
    start_counter = time.time()

    usr = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.ID, "user_email"))
    )
    print "[+] username box found."
    usr.send_keys(__user__)
    print "[+] username filled."

    pwd = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.ID, "user_password"))
    )
    print "[+] password box found."
    pwd.send_keys(__pwd__)
    print "[+] password filled."

    btnLogin = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.CLASS_NAME, "btn-success"))
    )
    print "[+] submit button found."
    btnLogin.click()
    print "[+] submit clicked."

    WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.ID, "campaigns-list"))
    )
    print "[+] access granted."
    print "-------------------"
    setting_read.close()

    print "[+] login loading time: " + str(time.time() - start_counter)
    print "-------------------"


#
# --------------------------------------------------------------


# SELECT YOUR PRODUCT
def step_1():
    driver.get("https://www.gearbubble.com/campaigns/new")
    try:
        # CHECKING STEP 1 STATUS
        product_wrapper = WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.CLASS_NAME, "products-wrapper"))
        )
        print "[+] product wrapper found."
        print "[+] step 1 loaded."
        #
        # --------------------------------------------------------------

        # FINDING COFFEE MUG
        js_product = product_wrapper.find_elements_by_class_name("js-product")
        print "[+] js-product found."
        for elm in js_product:
            data_id = elm.get_attribute("data-id")
            if data_id == "5":
                elm.find_element_by_tag_name("div").click()
                print "[+] coffee mug clicked."
                break
        #
        # --------------------------------------------------------------

        # CLICKING TO NEXT STEP
        btn_next = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CLASS_NAME, "btn-success"))
        )
        print "[+] next step button found."
        btn_next.click()
        print "[+] next step button clicked."
    #
    # --------------------------------------------------------------

    except TimeoutException:
        print "[-] timeout happended."
        fail_log.write(str(datetime.datetime.now()) + " " + "timeout exception \n")


def step_2(__upload_link__, __wrapped__, __color__, __base_cost__):
    # CHECKING STEP 2 STATUS
    checkbox = WebDriverWait(driver, 60).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "checkbox"))
    )
    print "[+] checkbox found."
    print "[+] waiting 5 sec."
    time.sleep(5)
    print "[+] step 2 loaded."
    #
    # --------------------------------------------------------------

    # CHECKING WRAPPED IMAGE
    if int(__wrapped__) == 0:
        print "[+] dont use full wrap."
    if int(__wrapped__) == 1:
        full_wrapped_option = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.ID, "campaign_use_full_wrapped"))
        )
        print "[+] full wrap option found."
        full_wrapped_option.click()
        print "[+] full wrap option clicked."
    #
    # --------------------------------------------------------------

    # UPLOADING IMAGE
    #
    # [START] ABOUT UPLOAD BUTTON

    btn_upload = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.ID, "js-btn-upload-design"))
    )
    print "[+] upload button found."
    btn_upload.click()
    print "[+] upload button clicked."

    # [END] ABOUT UPLOAD BUTTON

    # [START] SENDING UPLOAD LINK

    input_upload = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.ID, "js-file-upload-design"))
    )
    print "[+] sending upload link found."
    input_upload.send_keys(__upload_link__)
    print "[+] sending upload link completed."

    # [END] SENDING UPLOAD LINK

    # [START] WAITING FOR UPLOAD

    for i in xrange(sys.maxint):
        drop_zone = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.ID, "js-dropzone"))
        )
        print "[+] drop zone found."
        drop_zone_class = drop_zone.get_attribute("class")
        if "hide" in drop_zone_class:
            print "[+] drop zone hide."
            break
        else:
            print "[+] waiting more."
            time.sleep(1)
    print "[+] waiting for more 5 sec."
    time.sleep(5)
    print "[+] upload completed."

    # [END] WAITING FOR UPLOAD
    #
    # --------------------------------------------------------------

    # CONFIGURE COLOR
    color_file = open(os.path.dirname(repr(sys.argv[0])).strip("\'") + "/config", "r")
    color_data = color_file.readlines()
    for elm_color_data in color_data:
        if elm_color_data == "":
            continue
        else:
            color_text = elm_color_data.split("=")[0]
            color_value = elm_color_data.split("=")[1]
            if __color__ == color_text:
                color_section = WebDriverWait(driver, 30).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "colors-section"))
                )
                print "[+] color section found."
                selective_colors = color_section.find_elements_by_class_name("js-color-item")
                print "[+] color items found."
                for elm_selective_color in selective_colors:
                    data_id = elm_selective_color.get_attribute("data-id")
                    if data_id == color_value:
                        elm_selective_color.click()
                        print "[+] color selected."
    #
    # --------------------------------------------------------------

    # CONFIGURE PRICE
    converted_base_cost = str(__base_cost__)
    if converted_base_cost != "" or converted_base_cost != "0":
        base_cost = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.ID, "cost"))
        )
        print "[+] base cost found"
        # Reset the base cost input form
        driver.execute_script("document.getElementById('cost').value = '';")
        base_cost.send_keys(converted_base_cost)
        print "[+] base cost set: " + converted_base_cost
    #
    # --------------------------------------------------------------

    # CLICKING TO NEXT STEP
    #
    # --------------------------------------------------------------


if __name__ == "__main__":

    driver = webdriver.Firefox()
    driver.set_window_size(1366, 800)

    try:

        login()
        print ""

        step_1()
        print ""

        step_2("/Users/pwnux90/MEGA/workplace/gearbubble/source/img/spod-1.png", "0", "b", 30)
        print ""

        os.system("pkill geckodriver")
        print "[+] geckodriver killed."

    except Exception:
        os.system("pkill geckodriver")
        print "[+] geckodriver killed."
