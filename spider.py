
from reqHandler import StealthBrowserManager
import re

SOCIAL_PATTERNS = {
	"telegram": r'https?://(?:www\.)?t\.me/[^\s"\'<>]+',
	"instagram": r'https?://(?:www\.)?instagram\.com/[^\s"\'<>]+',
	"facebook": r'https?://(?:www\.)?facebook\.com/[^\s"\'<>]+',
	"whatsapp": r'https?://(?:wa\.me/[^\s"\'<>]+|(?:www\.)?whatsapp\.com/[^\s"\'<>]+)',
	"linkedin": r'https?://(?:www\.)?linkedin\.com/[^\s"\'<>]+',
	"web": r'https?://[^\s"\'<>]+',
	"email": r'\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b',
	"phone": r'(?<!\w)\+?\d[\d\s().-]{5,}\d(?!\w)',
    #"domain": r'\b(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}\b',
}
class Spider:
	def __init__(self, website):
		self.website = website
		self.browser = StealthBrowserManager()

		self.page = 0
		self.emails = []
		self.foundLinks = []
		self.socials = {
			"web": [],
			"telegram": [],
			"instagram": [],
			"facebook": [],
			"whatsapp": [],
			"linkedin": [],
			"email": [],
			"phone": [],
		}

	async def start_browser(self):
		await self.browser.start()

	async def get_html_page(self, link=None):
		if link is None:
			link = self.website

		page = await self.browser.get_page(link)
		html_page = await page.content()
		return html_page

    
	async def extract_socials(self, link):
		html = await self.get_html_page(link)

		for platform, pattern in SOCIAL_PATTERNS.items():
			if platform == "web":
				continue

			matches = re.findall(pattern, html, re.IGNORECASE)
			self.socials[platform].extend(matches)

		for url in re.findall(SOCIAL_PATTERNS["web"], html, re.IGNORECASE):
			url = url.rstrip(".,;!?)\]")

			if not any(
				re.fullmatch(pattern, url, re.IGNORECASE)
				for platform, pattern in SOCIAL_PATTERNS.items()
				if platform not in ("web", "email", "phone")
			):
				self.socials["web"].append(url)

		for category in self.socials:
			self.socials[category] = list(dict.fromkeys(self.socials[category]))

		return self.socials


	async def getFindings(self):
		print("Found socials: ")
		print(self.socials)

	async def close_browser(self):
		await self.browser.close()

