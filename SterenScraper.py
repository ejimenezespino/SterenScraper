from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import time
import csv

URL = 'https://www.steren.com.mx/'
header = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"}
driver_exe = '/Users/elianajimenezespinosa/Downloads/chromedriver'

response = requests.get(URL, headers=header)
print(response)
bs_container = BeautifulSoup(response.content, "html.parser")

catBanner = bs_container.select("div.col-level")[0]  # Raw Container with all links and categories/subcategories
subCatBanner = bs_container.select("div.col-xs-8")[0]  # Raw Container with all links and categories/subcategories

catBannerContainer = catBanner.select("div.col-xs-12")  # raw catLinks
catLink = [a["href"] for link in catBannerContainer for a in link.select("a[href]")]  # catLinks
catText = [cat.text.strip() for cat in catBannerContainer]  # catText

subCatBannerContainer = subCatBanner.select("div.form-group")  # raw subCatLinks
subCatLink = [a["href"] for link in subCatBannerContainer for a in link.select("a[href]")]  # subCatLinks
subCatText = [cat.text.strip() for cat in subCatBannerContainer] # subCatText

# subCatLink = ['https://www.steren.com.mx/audio/audifonos']

productLinks = []  # all links pages for each subcat
allProducts = []  # all products links
catAndSubcat = []
time.sleep(5)


page = 2
for link in subCatLink:
    lnk = link + "?p=" + str(page)
    productLinks.append(link)
    productLinks.append(lnk)


for l in productLinks:
    driver = webdriver.Chrome(driver_exe)
    driver.get(l)
    time.sleep(10)
    linkLocator = driver.find_elements_by_class_name('product-item-link')
    for lnk in linkLocator:
        lnk = lnk.get_attribute('href')
        if lnk not in allProducts:
            allProducts.append(lnk)
            cat = driver.find_elements_by_xpath('/html/body/div[3]/div[3]/ul/li[2]/a')[0]
            subCat = driver.find_elements_by_xpath('/html/body/div[3]/div[3]/ul/li[3]/strong')[0]
            if l not in catAndSubcat:
                catAndSubcat.append((lnk, cat.text, subCat.text))
    driver.close()

with open('catAndSubcat.csv', 'a') as csv_file:
    writer = csv.writer(csv_file)
    for cat, subCat, catAndScat in catAndSubcat:
        writer.writerow(([cat, subCat, catAndScat]))



with open('catAndSubcat.csv', 'r') as csvFile:
    csvReader = csv.reader(csvFile, delimiter=',')
    for row in csvReader:
        allProducts.append(row[0])
        print(allProducts)


for pl in allProducts:
    data = []
    driver = webdriver.Chrome(driver_exe)
    driver.get(pl)
    time.sleep(10)

    ean = ""


    try:
        productName = driver.find_elements_by_class_name('page-title')[0].text
    except IndexError:
        productName = ''

    try:
        productDesc = driver.find_elements_by_xpath('/html/body/div[3]/main/div[2]/div/div[3]/div[1]/div[2]/div/div')[0].text
    except IndexError:
        productDesc = ''


    try:
        producTechDesc = driver.find_elements_by_xpath('/html/body/div[3]/main/div[2]/div/div[3]/div[5]/div[2]/div/div/div')[0].text
    except:
        producTechDesc = ''


    department = ''
    hall = ''

    try:
        seller_sku = driver.find_elements_by_xpath('/html/body/div[3]/main/div[2]/div/div[1]/div[1]/div')[0].text
    except IndexError:
        seller_sku = ''

    height = ''
    wide = ''
    length = ''

    try:
        content = driver.find_elements_by_xpath('/html/body/div[3]/main/div[2]/div/div[3]/div[3]/div[2]/div/div[2]')[0].text
    except IndexError:
        continue

    measureUnit = ''

    try:
        regularPrice = driver.find_elements_by_xpath('/html/body/div[3]/main/div[2]/div/div[1]/div[5]/div[2]/div[1]/span[1]/span/span/span')[0].text
    except IndexError:
        regularPrice = driver.find_elements_by_xpath('/html/body/div[3]/main/div[2]/div/div[1]/div[5]/div[2]/div[1]/span/span')[0].text

    try:
        discountPrice = driver.find_elements_by_xpath('/html/body/div[3]/main/div[2]/div/div[1]/div[5]/div[2]/div[1]/span[2]/span/span/span')[0].text
    except IndexError:
        discountPrice = ''

    discountInitDate = ''
    discountEndDate = ''

    try:
        source1 = driver.find_elements_by_xpath('//*[@id="maincontent"]/div[2]/div/div[2]/div[2]/div[2]/div[2]/div[1]/div[3]/div/img')[0].get_attribute('src')
    except IndexError:
        source1 = ''

    try:
        source2 = driver.find_elements_by_xpath('//*[@id="maincontent"]/div[2]/div/div[2]/div[2]/div[2]/div[2]/div[1]/div[3]/div[2]/img')[0].get_attribute('src')
    except IndexError:
        source2 = ''

    try:
        source3 = driver.find_elements_by_xpath('//*[@id="maincontent"]/div[2]/div/div[2]/div[2]/div[2]/div[2]/div[1]/div[3]/div[3]/img')[0].get_attribute('src')
    except IndexError:
        source3 = ''

    data.append((ean, productName, (productDesc + '\n\n' + producTechDesc), department, hall, seller_sku,
                 height, wide, length, content, measureUnit, regularPrice, discountPrice, discountInitDate, discountEndDate, source1,
                 source2, source3))
    print(data)

    driver.close()

    with open('steren.csv', 'a') as csv_file:
        writer = csv.writer(csv_file)
        for ean, productName, productDesc, department, hall, seller_sku, height, wide, length, content, measureUnit, regularPrice, discountPrice, discountInitDate, discountEndDate, source1, source2, source3 in data:
            writer.writerow(
                [ean, productName, productDesc, department, hall, seller_sku, height, wide, length, content,
                 measureUnit, regularPrice, discountPrice, discountInitDate, discountEndDate, source1,
                 source2, source3])

    driver.quit()
