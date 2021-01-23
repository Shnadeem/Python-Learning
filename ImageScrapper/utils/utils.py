import time
from urllib.request import urlretrieve
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import os, getopt

image_url = set()

# Default parameters, which either can be change during the execution (search and limit) or manually (rest)
apps_param = {
    'search_url':'https://www.google.com.sa/imghp?',
    'result_locator':'img.Q4LuWd',
    'image_url_locator':'img.n3VNCb',
    'search':'Dog',
    'limit':5,
    'dpath':'./image/'
}

# Accepting the command line arguments and resetting default parameters (search string and image download limit)
def get_attributes(main, argument, options, loptions):
    try:
        arguments, values = getopt.getopt(argument, options, loptions)
    except getopt.error as err:
        # Output error, and return with an error code
        print(str(err) + ".", " Use -h to see the available parameters")
        return

    for current_argument, current_value in arguments:
        if current_argument in ("-s"):
            apps_param['search'] = current_value
        elif current_argument in ("-l"):
            apps_param['limit'] = current_value
        elif current_argument in ("-h"):
            run = "-h [for help] -s <SearchString> -l <number of images>"
            print("Usage : ", main, run)
            print("   All Parameters are OPTIONAL")
            return


# Creating path for downloading the images
def create_path(path):
    try:
        if os.path.exists(path):
            print("{} Directory already present, proceeding further".format(path))
        else:
            os.makedirs(path, exist_ok=True)
            print("{} Directory created successfully".format(path))
    except OSError as error:
        print(error, "{} Directory can not be created".format(apps_param['search']))
        return
    except Exception as e:
        print(str(e))
        return


# Get the search result page
def get_driver(driver, search_url,search):
    driver.get(search_url)
    search_elem = driver.find_element_by_name("q")
    search_elem.clear()
    search_elem.send_keys(search)
    search_elem.submit()

    # Wait, until the search completes
    WebDriverWait(driver, 10).until( EC.visibility_of_element_located((By.CSS_SELECTOR, 'img.Q4LuWd')))
    return driver

# Fetching the final url for image after searching over google image
def get_image_url(driver, start, limit,result_loc, image_loc):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    result_urls = driver.find_elements(By.CSS_SELECTOR, result_loc)
    end = len(result_urls)

    for result in result_urls[start:end]:  # looping through results
        try:
            result.click()
            time.sleep(1)
        except:
            continue
        image_block = driver.find_elements(By.CSS_SELECTOR, image_loc)
        for image in image_block:
            if image.get_attribute('src') and 'http' in image.get_attribute('src') and '.jpg' in image.get_attribute('src'):
                image_url.add(image.get_attribute('src'))
                #print("URL:", image.get_attribute('src'))
        url_found = len(image_url)
        if url_found >= int(limit):  # this is to get one extra url
            #print("{} images found".format(url_found))
            break
    else:
        print("{} images has been found. Loading more images".format(url_found))
        driver.execute_script("document.querySelector('.mye4qd').click();")
        time.sleep(1)
        start = len(image_url)
        get_image_url(driver, start, limit, result_loc, image_loc)
    return image_url, driver

# Downloding the image and saving it to created path
def image_download(driver,image_url,location,limit):
    i=0
    for img in image_url:
        try:
            if i < int(limit): # This is an extra check (even though it is not needed)
                urlretrieve(img, location + str(int(time.time())) + "_" + str(i) + ".jpg")
                i += 1
        except:
            continue
    driver.quit()
    return i

