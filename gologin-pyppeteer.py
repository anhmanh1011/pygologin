import time
import asyncio
import pyppeteer
from sys import platform
from gologin import GoLogin

async def main():
	gl = GoLogin({
		"token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI2NGVmMzkzZjBkNDI3NGU5MmNlYTQ1YjkiLCJ0eXBlIjoiZGV2Iiwiand0aWQiOiI2NGYxNmUyMWQ0MWE5MzcwMjQ2ZWYyZmEifQ.BwjEX-nhPDwU07va5DURYQPPDN2hmz5f-W1UlUjTlWM",
		"profile_id": "64ef393f0d42748ec2ea45ed",
		})

	debugger_address = gl.start()
	browser = await pyppeteer.connect(browserURL="http://"+debugger_address)
	page = await browser.newPage()
	await gl.normalizePageView(page)
	await page.goto('https://gologin.com')
	await page.screenshot({'path': 'gologin.png'})
	await browser.close()
	gl.stop()

asyncio.get_event_loop().run_until_complete(main())
