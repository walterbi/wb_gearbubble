# -*- coding: utf8 -*-
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import *
from PIL import Image
import os, sys, openpyxl, time, datetime


# check slash at the end of source file


# Waiting for modified
def gb_reading_template(__row__):
    path = sheet.cell(row=__row__, column=1).value
    filename = sheet.cell(row=__row__, column=2).value
    title = sheet.cell(row=__row__, column=3).value
    color = sheet.cell(row=__row__, column=4).value
    cost = sheet.cell(row=__row__, column=5).value
    url = sheet.cell(row=__row__, column=6).value
    tag = sheet.cell(row=__row__, column=7).value
    back_default = sheet.cell(row=__row__, column=8).value
    wrapped = sheet.cell(row=__row__, column=9).value
    x_offset = sheet.cell(row=__row__, column=10).value
    y_offset = sheet.cell(row=__row__, column=11).value
    file_width = sheet.cell(row=__row__, column=12).value

    return path, filename, title, color, cost, url, tag, back_default, wrapped, x_offset, y_offset, file_width


def gb_login(__login_link__):
    driver.get(__login_link__)

    # Reading config file
    config_file = open(os.path.dirname(repr(sys.argv[0])).strip("\'") + "/config", "r")
    config_data = config_file.readlines()
    __username__ = ""
    __pwd__ = ""
    for elm_config_data in config_data:
        if "username" in elm_config_data:
            __username__ = elm_config_data.split("=")[1]
        if "password" in elm_config_data:
            __pwd__ = elm_config_data.split("=")[1]

    input_email = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.ID, "user_email"))
    )
    input_email.send_keys(__username__)

    input_pwd = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.ID, "user_password"))
    )
    input_pwd.send_keys(__pwd__)
    print "[+] User information completed."

    # Submit to login
    btn_submit = driver.find_element_by_class_name("btn-success")
    btn_submit.click()
    print "[+] Submited."

    # Confirm to access
    alert_info = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.CLASS_NAME, "alert-info"))
    )
    print "[+] Access Granted."
    print "-------------------"

    return 1


def gb_check_uploaded(__file_name__):
    file_status = 0
    success_file = open(os.path.dirname(repr(sys.argv[0])).strip("\'") + "/success.log", "r")
    success_data = success_file.readlines()

    for elm in success_data:
        if __file_name__ in elm:
            file_status = 1
            break

    return file_status


def gb_check_step_1():
    # Checking step #1 loading status
    driver.get("https://www.gearbubble.com/campaigns/new")
    try:
        WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.CLASS_NAME, "products-wrapper"))
        )
        print "[+] Step #1 loaded."
        return 1
    except TimeoutException:
        print "[+] Timeout."
        fail_log.write(str(datetime.datetime.now()) + " " + "Timeout exception \n")


def gb_new_campaign_step_1():
    # Checking step #1 loading status
    products_wrapper = WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.CLASS_NAME, "products-wrapper"))
    )

    js_products = products_wrapper.find_elements_by_class_name("js-product")
    for elm_js_product in js_products:
        data_id = elm_js_product.get_attribute("data-id")
        if data_id == "5":
            elm_js_product.find_element_by_tag_name("div").click()
            print "[+] Coffee mug selected."
            break

    # Finding next button
    driver.find_element_by_class_name("btn-success").click()
    print "[+] Next step clicked."
    print "----------------------"


# Base cost can take 0 or blank for setting default price to $19.95
def gb_new_campaign_step_2(__upload_link__, __wrapped__, __color__, __base_cost__):
    # Checking step #2 loading status
    WebDriverWait(driver, 60).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "checkbox"))
    )

    for i in range(5):
        wait_str = "[+] Waiting: " + str(i + 1)
        sys.stdout.write("\r" + wait_str)
        sys.stdout.flush()
        time.sleep(1)
    print ""
    print "[+] Step #2 loaded."

    # Wrapped or not
    if int(__wrapped__) == 0:
        print "[+] Don\'t use Full Wrap Image"
    if int(__wrapped__) == 1:
        full_wrapped_option = driver.find_element_by_id("campaign_use_full_wrapped")
        full_wrapped_option.click()
        print "[+] Wrapped sticked."

    # Upload image
    btn_upload = driver.find_element_by_id("js-btn-upload-design")
    btn_upload.click()
    print "[+] Upload button clicked."
    input_upload = WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.ID, "js-file-upload-design"))
    )
    print "[+] Sending upload link..."
    input_upload.send_keys(__upload_link__)

    for i in xrange(sys.maxint):
        drop_zone = driver.find_element_by_id("js-dropzone")
        drop_zone_class = drop_zone.get_attribute("class")
        if "hide" in drop_zone_class:
            print ""
            break
        else:
            wait_str = "[+] Waiting: " + str(i + 1)
            sys.stdout.write("\r" + wait_str)
            sys.stdout.flush()
            time.sleep(1)

    for i in range(5):
        wait_str = "[+] Waiting: " + str(i + 1)
        sys.stdout.write("\r" + wait_str)
        sys.stdout.flush()
        time.sleep(1)
    print ""
    print "[+] Upload completed."

    # Setting colors
    color_file = open(os.path.dirname(repr(sys.argv[0])).strip("\'") + "/config", "r")
    color_data = color_file.readlines()
    for elm_color_data in color_data:
        if elm_color_data == "":
            continue
        else:
            color_text = elm_color_data.split("=")[0]
            color_value = elm_color_data.split("=")[1]
            if __color__ == color_text:
                color_section = driver.find_element_by_class_name("colors-section")
                selective_colors = color_section.find_elements_by_class_name("js-color-item")
                for elm_selective_color in selective_colors:
                    data_id = elm_selective_color.get_attribute("data-id")
                    if data_id == color_value:
                        elm_selective_color.click()
                        print "[+] Color selected."

    # Select prices
    converted_base_cost = str(__base_cost__)
    if converted_base_cost != "" or converted_base_cost != "0":
        base_cost = driver.find_element_by_id("cost")
        # Reset the base cost input form
        driver.execute_script("document.getElementById('cost').value = '';")
        base_cost.send_keys(converted_base_cost)
        print "[+] Base cost set: " + converted_base_cost

    # Next to step
    next_btn = driver.find_element_by_class_name("btn-success")
    next_btn.click()
    print "[+] Next step clicked."
    print "----------------------"


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


def gb_new_campaign_step_3(__title__, __url__, __tag__, __back_default__):
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

    # Set tags
    if __tag__ != "none":
        tags_input = driver.find_element_by_class_name("bootstrap-tagsinput")
        tags_input.find_element_by_tag_name("input").send_keys(__tag__)
        print "[+] Tags set."

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


def gb_new_campaign_step_finish(__file_name__):
    # Checking step #4 loading status
    WebDriverWait(driver, 120).until(
        EC.presence_of_element_located((By.CLASS_NAME, "alert-success"))
    )

    # Logging successfull product to file
    success_log.write(str(datetime.datetime.now()) + " " + __file_name__ + "\n")
    print "[+] Uploading finished."


def gb_wrap_image(__path__, __filename__, __x_offset__, __y_offset__, __file_width__):
    # Check slash at the end of file
    if __path__[len(__path__) - 1] != "/":
        new_path = __path__ + "/"
    else:
        new_path = __path__

    # Check wrapped_mug foler exist or not
    if not os.path.isdir(new_path + "full_mugs"):
        os.mkdir(new_path + "full_mugs")

    config_link = os.path.dirname(repr(sys.argv[0]).strip("\'"))
    background_mug = Image.open(config_link + "/background_mug.png")
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


if __name__ == "__main__":

    __basename__ = os.path.dirname(repr(sys.argv[0])).strip("\'")

    if not os.path.isfile(__basename__ + "/success.log"):
        os.system("touch " + __basename__ + "/success.log")
    if not os.path.isfile(__basename__ + "/fail.log"):
        os.system("touch " + __basename__ + "/success.log")

    success_log = open(__basename__ + "/success.log", "r+")
    fail_log = open(__basename__ + "/fail.log", "r+")

    # Reading template file
    excel_template = openpyxl.load_workbook(os.path.dirname(repr(sys.argv[0])).strip("\'") + "/GB-template-list.xlsx",
                                            "r")
    sheet = excel_template.get_sheet_by_name("Sheet1")
    __max_row__ = sheet.max_row

    driver = webdriver.Firefox()
    # Login processing
    # If try to 3 times, timeout
    for timeout_count in range(3):
        try:
            status = gb_login("https://www.gearbubble.com/users/sign_in")
            if status == 1:
                break
        except TimeoutException:
            if timeout_count + 1 == 3:
                print "[-] Too long to response!"
                fail_log.write(str(datetime.datetime.now()) + " " + "Too long to response exception \n")
                fail_log.close()
                os.system("pkill geckodriver")
            else:
                print "[-] Timeout exception!"
                # Writing to log file
                fail_log.write(str(datetime.datetime.now()) + " " + "Timeout exception \n")
                continue

    # Loop file in excel template
    for template_row in range(2, __max_row__ + 1):

        # Checking uploaded file already
        template_data = gb_reading_template(template_row)

        # tmp = template_data[2].replace(u"\u2019", "'")
        # print "[+] " + tmp
        # sys.exit()

        upload_status = gb_check_uploaded(template_data[1])
        if upload_status == 1:
            print "[-] File uploaded already!"
            fail_log.write(str(datetime.datetime.now()) + " " + template_data[1] + " already uploaded \n")
            continue
        else:
            # Step 1: choose coffee mug
            for timeout_count in range(3):
                step_1_status = gb_check_step_1()
                if step_1_status == 1:
                    break
                elif timeout_count + 1 == 3:
                    print "[-] Step 1: Choose coffee mug too long to response!"
                    fail_log.write(str(datetime.datetime.now()) + " " + "Step#1 Too long to response exception \n")
                    fail_log.close()
                    os.system("pkill geckodriver")
                else:
                    print "[-] Step 1: Timeout exception!"
                    fail_log.write(str(datetime.datetime.now()) + " " + "Step#1 Timeout exception \n")
            gb_new_campaign_step_1()

            # Step 2: uploading design
            upload_link = gb_wrap_image(template_data[0], template_data[1], template_data[9], template_data[10],
                                        template_data[11])
            try:
                gb_new_campaign_step_2(upload_link, template_data[8], template_data[3], template_data[4])
            except (NoSuchElementException, ElementNotVisibleException) as err:
                fail_log.write(str(datetime.datetime.now()) + " " + err + "\n")

            # Step 3: filled information
            title_url = gb_title_validate(template_data[2])
            print "[+] Title validated."
            url_element = WebDriverWait(driver, 60).until(
                EC.presence_of_element_located((By.ID, "campaign_slug"))
            )
            print "[+] URL element founded."
            product_url = gb_url_validate(template_data[2], url_element)
            print "[+] URL validated."
            gb_new_campaign_step_3(title_url, product_url, template_data[6], template_data[7])

            # Step 4: report and logging
            gb_new_campaign_step_finish(template_data[1])

    success_log.close()
    fail_log.close()
