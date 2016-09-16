from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

from pyvirtualdisplay import Display
display = Display(visible=0, size=(1024, 768))
display.start()

def crawler(name, date="today"):
	print name,date
	chromeOptions = webdriver.ChromeOptions()
	prefs = {"download.default_directory" : "data/" + name}
	chromeOptions.add_experimental_option("prefs",prefs)
	chromedriver = './chromedriver'

	driver = webdriver.Chrome(executable_path=chromedriver, chrome_options=chromeOptions)

	driver.get("https://idp.mynysmls.com/idp/Authn/UserPassword")
	driver.find_element_by_css_selector("a[onclick*='buffalo']").click()
	
	print "Logging in to MLS..."
	def login():
		time.sleep(3)

		inputElement = driver.find_element_by_id("j_username")
		inputElement.send_keys('smithray')

		driver.find_element_by_id("loginbtn").click()

		inputElement = driver.find_element_by_id("password")
		inputElement.send_keys('queen2016')

		driver.find_element_by_id("loginbtn").click()
		
		time.sleep(3)
	
	login()
	
	print "Moving to Matrix..."
	driver.get("http://nys.mlsmatrix.com/Matrix/Search/Residential/SingleFamily")

	time.sleep(2)
	print "Searching for expires..."
	
	if date == "today":
		driver.find_element_by_css_selector("a[id*='m_ucSearchButtons_m_lbSearch']").click()
	else:
		print "Setting date"
		driver.find_element_by_id("FmFm9_Ctrl42_106_Ctrl42_TB").clear()
		driver.find_element_by_id("FmFm9_Ctrl42_106_Ctrl42_TB").send_keys(date)
		time.sleep(2)
		driver.find_element_by_css_selector("a[id*='m_ucSearchButtons_m_lbSearch']").click()

	time.sleep(2)
	driver.find_element_by_css_selector("a[id*='m_lnkCheckAllLink']").click()

	time.sleep(2)
	driver.find_element_by_css_selector("a[id*='m_lbExport']").click()

	time.sleep(2)
	print "Exporting..."
	driver.find_element_by_css_selector("a[id*='m_btnExport']").click()
	
	print "Done!"
	time.sleep(5)
	driver.quit()

if __name__ == "__main__":
	for i in range(19,30):
		crawler("8_{}_2016".format(str(i)),"08/{}/2016".format(str(i)))
