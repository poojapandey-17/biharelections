
import unittest
from selenium import webdriver
from selenium.webdriver.support.select import Select
from time import sleep
import pandas as pd
import sys
 
path = "C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe"

all_df = []
file_cnt = 0
driver = webdriver.Chrome(path)
driver.maximize_window()
driver.get('http://sec.bihar.gov.in/Contesting.aspx')
post = int(sys.argv[1])
distr= int(sys.argv[2])
s1=Select(driver.find_element_by_name('ddlPostName'))
pst = s1.options[int(post)].text
file = "Output_{}_{}.xlsx".format(sys.argv[1],sys.argv[2])
s1.select_by_index(post)
sleep(2)
s2=Select(driver.find_element_by_name('ddlDistrict'))
dist = s2.options[int(distr)].text
s2.select_by_index(distr)
sleep(2)
s3=Select(driver.find_element_by_name('ddlBlok'))
#for j in range(1,len(s3.options)):
for j in range(1,3):
    block = s3.options[j].text
    s3.select_by_index(j)
    sleep(2)
    s4=Select(driver.find_element_by_name('ddlPanchayat'))
    #for k in range(1,len(s4.options)):
    for k in range(1,3):
        panch = s4.options[k].text
        s4.select_by_index(k)
        sleep(2)
        s5=Select(driver.find_element_by_name('ddlWard'))
        #for l in range(1,len(s5.options)):
        for l in range(1,3):
            ward = s5.options[l].text
            s5.select_by_index(l)
            driver.find_element_by_name('btnSubmit').click()
            sleep(2)
            try:
                tbl = driver.find_element_by_class_name("Grid").get_attribute('outerHTML')
                dfs = pd.read_html(tbl)
                df = dfs[0]    
                cnt= df.shape[0]
                file_cnt = file_cnt + cnt
                df["COUNTER"] =cnt
                df["Post"] = pst
                df["District"] = dist
                df["Block"] = block
                df["Panchayat"] = panch
                df["Ward"] = ward
                print(df)
                all_df.append(df)
                print("COUNTER {}".format(file_cnt))
                with open('Output_Log.txt', 'a') as f: 
                    print("{}|{}|{}|{}|{}|{}".format(post, dist, block, panch, ward, cnt), file=f)
            except:
                print("NO RECORD FOUND")
                with open('Output_Log.txt', 'a') as f:
                    print("{}|{}|{}|{}|{}|{}".format(post, dist, block, panch, ward, "No Rec"), file=f)
            

            s5=Select(driver.find_element_by_name('ddlWard')) 
        s4=Select(driver.find_element_by_name('ddlPanchayat'))
    s3=Select(driver.find_element_by_name('ddlBlok'))
s2=Select(driver.find_element_by_name('ddlDistrict'))


all_df = pd.concat(all_df)
all_df.to_excel(file)
driver.quit()
                                        
