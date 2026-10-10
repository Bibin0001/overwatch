import asyncio
from spider import Spider
from telegramScraper import TelegramCollector



async def main():
    '''
    spider = Spider("https://example.com")
    await spider.start_browser()
    hits = await spider.extract_socials("https://au.seek.com/fifo-jobs?jobId=95144010&type=promoted")
    await spider.getFindings()
    await spider.close_browser()
    '''

    tlgr = TelegramCollector()
    await tlgr.start_client() 
    fifo = "@offshorevacancies"
    links = await tlgr.check_link(fifo)
    print(links)


if __name__ == "__main__":
	asyncio.run(main())

