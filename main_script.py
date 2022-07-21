'''Selenium functional testing of amazon web app

Selenium webdriver triggers a browser driver to execute the set of operations we expect 
a user to do while using the amazon web app features. This module handles the
non-login case in which user simply visits the amazon web app (homepage) then clicks on the 
search box then inputs random search data and performs search operation. The user views the 
first item of the search results then adds it to the cart if the item is available. Lastly, 
the viewed product and the product that has been added to the cart are checked to match. '''

import time
import random
import selenium
from selenium import webdriver
from pdb import set_trace
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


Amazon = 'https://www.amazon.com/'
search_box_xpath = '//input[@id="twotabsearchtextbox"]'
search_button_xpath = '//input[@id="nav-search-submit-button"]'
search_results_xpath = '//div[@data-index="1"]'
add_to_cart_button_xpath = '//input[@id="add-to-cart-button" and @name="submit.add-to-cart"]'
add_to_list_button_xpath = '//span[@id="wishListMainButton" and @class="a-button a-button-groupfirst a-spacing-none a-button-base a-declarative"]'
cart_icon_xpath = '//div[@id="nav-cart-count-container"]'
selected_product_id_xpath =  '//*[@id="ASIN"]'

try:

  def find_html_element(xpath, wait_time=None, click=False):

    if wait_time:
      element = WebDriverWait(browser, wait_time).until(EC.element_to_be_clickable((By.XPATH, xpath)))	
    else:  
       element = browser.find_element(By.XPATH, xpath)

    if click:
      element.click()

    return element
    
 

  # Manage/install drivers for chrome browser
  browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
  
  # Visit the main amazon web app home page
  browser.get(Amazon)

  # Defining random input data for search
  Searchbox_input_list = ['moisturizer', 'lipstick', 'perfume']

  
  # Locate the search box and give a click on it
  search_box = find_html_element(search_box_xpath, 30, True)
  search_box.clear()

  # Randomly choose a value from the random input data list then pass it as an input in the search box
  input_text = random.choice(Searchbox_input_list)
  search_box.send_keys(input_text)
  print('Input Search Data : SUCCESS')

  # Locate and click on the search button/perform search
  find_html_element(search_button_xpath, 25, True)
  print('Click on the Search button : SUCCESS')

  # Open the 1st item of the search result's list
  find_html_element(search_results_xpath, 30, True)
  print('Fetch search result and open the 1st item of the list : SUCCESS')

  
  selected_product_id = ""

  try:

    # Store the selected product's id value 
    # selected_product_id_element = find_html_element(selected_product_id_xpath, 30, False) #This didnt work for input DOM.
    selected_product_id_element = browser.find_element(By.ID, "ASIN")
    selected_product_id = str(selected_product_id_element.get_attribute("value")).strip()
    print("Selected product's id value:", selected_product_id)

  except Exception as e:
    print("Unable to locate the selected product's id value. Error: ", str(e))
  
  try:
    # Click on the add to cart button
    add_to_cart_btn = find_html_element(add_to_cart_button_xpath, 30, False)
    browser.execute_script("arguments[0].click();", add_to_cart_btn)
    print('Item add to the Cart : SUCCESS')
    
    try:
      # Click on the cart icon from the header menu
      cart_icon = find_html_element(cart_icon_xpath, 25, False)
      browser.execute_script("arguments[0].click();", cart_icon)
      print('Click on the Cart icon : SUCCESS')

      # Check products in cart.
      cart_products = browser.find_elements(By.XPATH, "//div[@class='a-row sc-list-item sc-list-item-border sc-java-remote-feature']")
      product_exists = False

      for cart_product in cart_products:
        product_id = str(cart_product.get_attribute("data-asin")).strip()
        if product_id == selected_product_id:
          product_exists = True
          break
      if product_exists:
        print(f"Product '{selected_product_id}' exists in basket.")
      else:
        print(f"Product '{selected_product_id}' doesn't exists in basket.")

    except Exception as e:
      print('Cart page could not be opened. Error: ', str(e))

  except Exception as e:
    # Show error message if the item cannot be added to the cart
    print('STATUS : The item is out of stock! Error: ', str(e))  
  

finally:

  time.sleep(6)

  print("Script Execution : COMPLETED")
  browser.quit()   

