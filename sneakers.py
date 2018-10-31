import time
import json
import requests
import sys

from selenium import webdriver

from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
driver = webdriver.Chrome('./chromedriver')

if sys.argv[1] is '1':
    site = "footlocker"
elif sys.argv[1] is '2':
    site = "footaction"
elif sys.argv[1] is '3':
    site = "eastbay"
elif sys.argv[1] is '4':
    site = "champssports"

model = '267991'
sku   = 'BB1169'

shoeloop = True
while shoeloop:
    driver.get('http://www.'+site+'.com/product/model:267991/sku:BB1169/');
    print("Opening Page")
    shoereq = driver.find_elements_by_name('requestKey')[0].get_attribute('value')
    shoesku = driver.find_elements_by_name('sku')[0].get_attribute('value')
    shoemodel = driver.find_elements_by_name('the_model_nbr')[0].get_attribute('value')
    if shoereq is None:
        driver.refresh()
    if shoesku is None:
        driver.refresh()
    if shoemodel is None:
        driver.refresh()
    print("SHOE REQUESTKEY: "+shoereq)
    print("SHOE SKU: "+shoesku)
    print("SHOE MODEL: "+shoemodel)

    data = {}
    data["the_model_nbr"]=shoemodel
    data["inlineAddToCart"]="1"
    data["model"]=shoemodel
    data["qty"]="1"
    data["quantity"]="1"
    data["requestKey"]=shoereq
    data["size"]="11.5"
    data["sku"]=shoesku
    data["the_model_nbr"]=shoemodel

    #data["model_name"]="adidas Originals Tubular Invader Strap - Men's"
    #data["skipISA"]="no"
    #data["sameDayDeliveryConfig"]="false"
    #data["selectedPrice"]="$0.00"
    #data["lineItemId"]=""
    #data["storeCostOfGoods"]="0.00"
    #data["storeNumber"]="00000"
    #data["coreMetricsCategory"]="Add to Wish List - PDP"
    #data["coreMetricsDo"]="true"
    #data["fulfillmentType"]="SHIP_TO_HOME"
    #data["hasXYPromo"]="false"

    atcURL="http://www."+site+".com/catalog/miniAddToCart.cfm?secure=0&"
    script="""
    $.ajax({
      url: '"""+atcURL+"""',
      data: """+json.dumps(data,indent=2)+""",
      method: 'POST',
      crossDomain: true,
      contentType: 'application/x-www-form-urlencoded',
      xhrFields: {
          withCredentials: true
      },
      complete: function(data, status, xhr) {
        console.log(status);
        console.log(data);
      }
    });"""
    #driver.refresh()
    driver.execute_script(script)
    time.sleep(0.1)
    driver.get('http://www.'+site+'.com/shoppingcart/default.cfm')
    time.sleep(0.1)
    if driver.current_url=="http://www."+site+".com/catalog/emptyCart.cfm?cartIsEmpty=1":
        shoeloop=True
    elif driver.find_elements_by_id('Error403') is None:
        print("ayy")
    else:
        shoeloop=None
        print("You're welcome")


