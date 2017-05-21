# encoding=utf8
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import *
from PIL import Image
import os, sys, openpyxl, time, datetime, getopt


driver = webdriver.Firefox()
driver.set_page_load_timeout(3000)
driver.set_window_size(1366, 800)


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


def step_2(__upload_link__, __wrapped__, __base_cost__):
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
    next_btn = driver.find_element_by_class_name("btn-success")
    next_btn.click()
    print "[+] Next step clicked."
    print "----------------------"
    #
    # --------------------------------------------------------------


def wrap(__path__, __filename__, __x_offset__, __y_offset__, __file_width__):
    # Check slash at the end of file
    if __path__[len(__path__) - 1] != "/":
        new_path = __path__ + "/"
    else:
        new_path = __path__

    # Check wrapped_mug foler exist or not
    if not os.path.isdir(new_path + "full_mugs"):
        os.mkdir(new_path + "full_mugs")

    background_mug = Image.open("background_mug.png")
    real_instance = Image.open(new_path + __filename__)

    instance_size = real_instance.size
    instance_width = instance_size[0]
    instance_height = instance_size[1]

    background_size = background_mug.size
    background_width = background_size[0]
    background_height = background_size[1]

    print "Instance"
    print "----------------------------"
    print "[+] Width: " + str(instance_width)
    print "[+] Height: " + str(instance_height)

    print "Background"
    print "----------------------------"
    print "[+] Width: " + str(background_width)
    print "[+] Height: " + str(background_height)

    instance_ratio = instance_height / instance_width
    new_instance_width = __file_width__
    new_instance_height = __file_width__ * instance_ratio
    for i in xrange(sys.maxint):
        if new_instance_height > 830:
            new_instance_width -= 10
            new_instance_height = new_instance_width * instance_ratio
        if new_instance_height <= 830:
            break

    # combine two image
    x_offset = __x_offset__
    y_offset = __y_offset__
    paste_instance = real_instance.resize((new_instance_width, new_instance_height))

    new_image = Image.new('RGBA', (background_width, background_height))
    new_image.paste(paste_instance, (x_offset, y_offset))
    new_image_path_name = new_path + "full_mugs/wrapped_" + __filename__ + ".png"
    new_image.save(new_image_path_name, 'PNG')

    return new_image_path_name


# Check error url
def gb_check_url_err():
    url_err = driver.find_element_by_id("js-slug-error")
    display_err = url_err.get_attribute("style")
    return display_err


# Validate url for fit requirement
# No capital letter
# No special letter like .
def gb_url_validate(__title_name__, __element_url__):
    print "==========================================="
    print "[+] loading url validate"
    useful_url = ""
    special_character = u"~!@#$%ˆ&*()+=`:;/.,<>?|\\"
    tmp_url = __title_name__.lower()
    # Replace white space
    tmp_url = tmp_url.replace(" ", "_")
    # Replace special character
    for elm in special_character:
        if elm in tmp_url:
            tmp_url = tmp_url.replace(elm, "_")

    # print "[+] last modified url: " + tmp_url
    # print "[+] type of url " + str(type(tmp_url))

    tmp_url = tmp_url.replace(u"\u2019", "_")
    tmp_url = tmp_url.replace(u"\u201D", "_")

    print "[+] " + tmp_url
    # sys.exit()
    # note about single quote and double quote

    base_len_url = len(__title_name__)
    # Checking length
    for i in xrange(sys.maxint):
        if len(tmp_url) < 28:
            __element_url__.clear()
            __element_url__.send_keys(tmp_url)
            err = gb_check_url_err()
            if "block" in err:
                # Adding number to the last
                # Clear url first
                tmp_url = tmp_url[:base_len_url]
                tmp_url = tmp_url + str(i)
            else:
                break
        else:
            # Cutting to 28 and re-check
            tmp_url = tmp_url[:28]
            __element_url__.clear()
            __element_url__.send_keys(tmp_url)
            err = gb_check_url_err()
            if "block" in err:
                tmp_url = tmp_url[:25]
                # Adding number to the last
                tmp_url = tmp_url + str(i)
            else:
                break

    useful_url = tmp_url
    return useful_url


# Validate title for fit requirement (not more 40 characters)
def gb_title_validate(__raw_title__):
    useful_title = ""

    # Checking length 40 (for raw), but we just need 30
    if len(__raw_title__) > 40:
        useful_title = __raw_title__[:40]
    else:
        useful_title = __raw_title__

    return useful_title


def step_3(__title__, __url__, __back_default__):
    for i in xrange(sys.maxint):
        freeze_pattern = driver.find_element_by_class_name("freeze-section")
        freeze_pattern_class = freeze_pattern.get_attribute("class")
        if "hide" in freeze_pattern_class:
            print ""
            break
        else:
            wait_str = "[+] Waiting: " + str(i + 1)
            sys.stdout.write("\r" + wait_str)
            sys.stdout.flush()
            time.sleep(1)

    # Checking step #3 loading status
    WebDriverWait(driver, 120).until(
        EC.presence_of_element_located((By.CLASS_NAME, "js-btn-flip"))
    )
    print "[+] Step #3 loaded."

    # Campaign title
    campaign_title = driver.find_element_by_id("campaign_title")
    campaign_title.send_keys(__title__)
    print "[+] Campaign title filled."

    # Campaign url
    campaign_url = WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.ID, "campaign_slug"))
    )
    campaign_url.clear()
    campaign_url.send_keys(__url__)
    print "[+] Campaign url filled."

    # Back default checking
    if int(__back_default__) == 1:
        driver.execute_script("document.getElementById('campaign_default_side').click();")
        print "[+] Back default is set."

    # Campaign term
    driver.execute_script("document.getElementById('campaign_agreement').click();")
    print "[+] Term and conditions agreed."

    for i in range(5):
        wait_str = "[+] Waiting: " + str(i + 1)
        sys.stdout.write("\r" + wait_str)
        sys.stdout.flush()
        time.sleep(1)
    print ""
    # Next to step
    # next_btn = driver.find_element_by_id("btn-add-description")
    # next_btn.click()
    driver.execute_script("document.getElementById('btn-add-description').click();")
    print "[+] Next step clicked."
    print "----------------------"


def step_4(__file_name__):
    # Checking step #4 loading status
    WebDriverWait(driver, 120).until(
        EC.presence_of_element_located((By.CLASS_NAME, "alert-success"))
    )

    # Logging successfull product to file
    success_log.write(str(datetime.datetime.now()) + " " + __file_name__ + "\n")
    print "[+] Uploading finished."


def main(argv):

    image_link = ""

    try:
        opts, args = getopt.getopt(argv, "hn:l:", ["name=", "link="])
    except getopt.GetoptError:
        print "[-] Error"
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print "Usage: python gear.py [-n] [-l]"
            sys.exit()
        if opt in ("-l", "--link="):
            image_link = arg

    # Getting file in folder
    all_file = os.listdir(image_link)

    try:

        login()
        print ""

        for item in all_file:
            if "png" in item:

                step_1()
                print ""

                new_wrap_image = wrap(image_link, item, 40, 300, 4500)
                step_2(new_wrap_image, "1", 9.95)
                print ""

                split_name = item.split(".")[0]
                title_url = gb_title_validate(split_name)

                url_element = WebDriverWait(driver, 60).until(
                    EC.presence_of_element_located((By.ID, "campaign_slug"))
                )
                print "[+] URL element founded."
                product_url = gb_url_validate(split_name, url_element)
                print "[+] URL validated."

                step_3(title_url, product_url, 0)

                # Step 4: report and logging
                step_4(item)

    except Exception:
        os.system("pkill geckodriver")
        print "[+] geckodriver killed."


if __name__ == "__main__":

    main(sys.argv[1:])
