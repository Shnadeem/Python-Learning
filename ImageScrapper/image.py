from selenium import webdriver
from utils.utils import apps_param, get_image_url, image_download, create_path, get_attributes
import getopt, sys, os

# Get full command-line arguments and reset the default values (if passed)
full_cmd_arguments = sys.argv
argument_list = full_cmd_arguments[1:]
short_options = "hs:l:"
long_options = ["help", "s=", "l="]

get_attributes(full_cmd_arguments[0], argument_list, short_options, long_options)

# Creating path for image download
apps_param['dpath'] += apps_param['search'] + "/"
create_path(apps_param['dpath'])

# Opening the browser and downloading the image
driver = webdriver.Firefox(executable_path = '.\geckodriver.exe')
url_images = get_image_url(driver,apps_param['search_url'],
                           apps_param['result_locator'],
                           apps_param['image_url_locator'],
                           apps_param['search'])
download = image_download(driver,url_images, apps_param['limit'], apps_param['dpath'])

print("{} images of {} downloaded successfully.".format(download,apps_param['search']))

## Execution
#1. Create project in PyCharm with conda (virtual environment) python 3.8
#2. Open terminal of this new invironment and run requirements.txt file (pip install -r requirements.txt)
#3. download the files and folder structure as given here. Place it at home foolder of your new vertual environment
#4. Default configurations:
# 4.1 Seach: Eagle
# 4.2 Limit: 10
#5. Below are syntax to be executed for this code to run
# 5.1 With default parameter
#     python image.py
# 5.2 With override parameter
#     python image.py -s Dog -l 5  (download 5 images of Dog)

