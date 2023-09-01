import time
from sys import platform
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from gologin import GoLogin
import photoshop.api as ps




gl = GoLogin({
	"token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI2NGVmMzkzZjBkNDI3NGU5MmNlYTQ1YjkiLCJ0eXBlIjoiZGV2Iiwiand0aWQiOiI2NGYxNmUyMWQ0MWE5MzcwMjQ2ZWYyZmEifQ.BwjEX-nhPDwU07va5DURYQPPDN2hmz5f-W1UlUjTlWM",
	"profile_id": "64ef393f0d42748ec2ea45ed"
	})

if platform == "linux" or platform == "linux2":
	chrome_driver_path = "./chromedriver"
elif platform == "darwin":
	chrome_driver_path = "./mac/chromedriver"
elif platform == "win32":
	chrome_driver_path = "./chromedriver.exe"

debugger_address = gl.start()
chrome_options = Options()
chrome_options.add_experimental_option("debuggerAddress", debugger_address)
driver = webdriver.Chrome(options=chrome_options)
driver.get("http://www.python.org")
assert "Python" in driver.title
app = ps.Application()
doc = app.activeDocument
last_name = doc.artLayers["last_name"]
last_name.textItem.contents = 'Hello, World!'
options = ps.JPEGSaveOptions(quality=5)
# # save to jpg
jpg = 'd:/hello_world.jpg'
doc.saveAs(jpg, options, asCopy=True)
app.doJavaScript(f'alert("save to jpg: {jpg}")')

time.sleep(3)
driver.quit()
time.sleep(3)
gl.stop()
