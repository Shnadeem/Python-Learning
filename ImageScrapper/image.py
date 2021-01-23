from selenium import webdriver
from utils.utils import image_url, apps_param, get_driver, get_image_url, image_download, create_path, get_attributes
import sys

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
start = 0
driver = webdriver.Firefox(executable_path = './geckodriver.exe')
driver = get_driver(driver, apps_param['search_url'],apps_param['search'])
image_url,driver = get_image_url(driver,start, apps_param['limit'], apps_param['result_locator'], apps_param['image_url_locator'] )
download = image_download(driver,image_url, apps_param['dpath'], apps_param['limit'])

print("{} images of {} downloaded successfully.".format(download,apps_param['search']))


## Execution
#1. Create project in PyCharm with conda (virtual environment) python 3.8
#2. Open terminal of this new environment and run requirements.txt file (pip install -r requirements.txt)
#3. download the files and folder structure as given here. Place it at home folder of your new vertual environment
#4. Default configurations:
# 4.1 Seach: Dog
# 4.2 Limit: 5
#5. Below are syntax to be executed for this code to run
# 5.1 With default parameter
#     python image.py
# 5.2 With override parameter
#     python image.py -s Cat -l 10  (download 10 images of Cat)
# Sample Execution
#   (imageScrapper) E:\Python\iNeuron\Scrapper\Image\imageScrapper>python image.py -l 10 -s Lion
#   ./image/Lion/ Directory created successfully
#   10 images of Lion downloaded successfully.
