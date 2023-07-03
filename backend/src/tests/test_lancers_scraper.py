from time import sleep
from scraper import LancersScraper
# from scraper import TestLancersScraper


LS = LancersScraper()
LS.start()
# LS.get_page_projects()
# LS._get_multiple_pages_urls(3)
LS.get_multiple_pages_projects(page=1) 
# LS.scrape(page=1) 
# LS.get_project_detail(page=3)
sleep(2)       # debug
# LS.quit()