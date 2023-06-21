import asyncio
import concurrent.futures
import datetime
import logging
import re
from time import sleep
from typing import List, Dict, Tuple, Union, Optional

from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from settings import env
from schemas import ProjectManager
'''
ランサーズウェブサイトスクレイピング

【URL】
https://www.lancers.jp/
'''


BASE_DIR = Path(__file__).resolve().parent.parent
print('BASE_DIR: ' + str(BASE_DIR))       # debug

LANCERS_USER = env.LANCERS_USERNAME
LANCERS_PASSWORD = env.LANCERS_PASSWORD

### log ###
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class Scraper:
    def __init__(self, url=''):
        logger.info({
            'action': 'Scraper', 
            'status': 'run'
        })
        self.url = url
        try:
            logger.info({
                'action': 'Scraper', 
                'status': 'driver_get: run', 
                'env.SELENIUM_URL': env.SELENIUM_URL, 
            })
            self.driver = webdriver.Remote(
                command_executor='http://selenium:4444/wd/hub',     # selenium = 172.17.0.2
                options=webdriver.ChromeOptions()
            )       # <- docker
#           options = Options()     # ヘッドレスモード時, driverのoptionsに渡す.
#           options.add_argument('--headless')          
#           self.driver = webdriver.Chrome(
#               executable_path="C:\Users\user\Desktop\div\__on_going\Lancers_businesstool\chromedriver",
#               options=options
#           )       # <- local
            self.driver.implicitly_wait(5)      # 暗黙的待機. つまり次の要素が見つかるまで最大(arg秒)待つ. 
                                                # 複数パターンの要素を条件分岐で探す場合, 先の処理で要素が見つからないとimplicitly_waitで指定した分待ち処理に時間がかかってしまう点注意.
            self.driver.get(self.url)
        except Exception as e:
            logger.error({
                'action': 'Scraper', 
                'status': 'driver-settings: exception', 
                'message': e
            })
            self.driver.quit()
        finally:
            logger.info({
                'action': 'Scraper', 
                'status': 'driver-settings: success'
            })

    async def _asy_scrape(self, executor, url: str, *, loop):
        logger.info({
            'action': 'LancersScraper().asy_scrape()', 
            'status': 'run'
        })
        await loop.run_in_executor(executor, self._asy_get_url, url)

    def _asy_get_url(self, url: str):
        logger.info({
            'action': 'LancersScraper().asy_get_url()', 
            'status': 'run'
        })
        try:
            asy_driver = webdriver.Remote(
                    command_executor='http://selenium:4444/wd/hub', 
                    options=webdriver.ChromeOptions()
            )
            asy_driver.get(url)
        except Exception as e:
            logger.error({
                'action': 'Scraper', 
                'status': 'as_get_url(): exception', 
                'message': e
            })
            self.driver.quit()


class TestLancersScraper(Scraper):
    def __init__(self, url='https://www.lancers.jp/'):
        logger.info({
            'action': 'LancersScraper', 
            'status': 'run',
        })
        super().__init__(url)
        self.projects = []

    def login(self):
        try:
            logger.info({
                'action': 'LancersScraper().login()', 
                'status': 'run'
            })
            if self.driver.current_url == self.url:
                logger.info({
                    'action': 'LancersScraper().login()', 
                    'status': 'url checked', 
                    'current_url': self.driver.current_url
                })

                login_button = self.driver.find_element(By.CLASS_NAME, 'css-1eti57o')
                login_button.click()
                sleep(1)       # debug

                login_user_form = self.driver.find_element(By.NAME, 'data[User][email]')
                login_password_form = self.driver.find_element(By.NAME, 'data[User][password]')
                login_user_form.send_keys(LANCERS_USER)
                login_password_form.send_keys(LANCERS_PASSWORD)
                login_user_form.submit()
                sleep(1)       # debug
                logger.info({
                    'action': 'LancersScraper().login()', 
                    'status': 'success'
                })
                ### モーダルウインドウがあれば ###
                # try:
                #     close_button = self.driver.find_element(By.CSS_SELECTOR, 'button.c-modal__close.js-mypage-modal-close')
                #     close_button.click()
                # except Exception as e:
                #     logger.info({
                #         'action': 'login', 
                #         'status': 'no modalwindow', 
                #         'message': e
                #     })
            else:
                logger.info({
                    'action': 'LancersScraper().login()', 
                    'status': 'already logged in', 
                    'current_url': str(self.driver.current_url)
                })
        except Exception as e:
            logger.error({
                'action': 'LancersScraper().login()', 
                'status': 'exception', 
                'message': e
            })
            self.driver.quit()

    def search_projects(self):
        logger.info({
            'action': 'LancersScraper().search_projects()', 
            'status': 'run'
        })
        try:
            self.driver.find_element(By.CSS_SELECTOR, 'span.css-v694h7').click()
            print('仕事を探す', self.driver.find_element(By.CSS_SELECTOR, 'span.css-v694h7')) #
            sleep(1)

            project_search_box = self.driver.find_element(By.CSS_SELECTOR, 'div.p-search-job__search-bar-inner.c-search-bar__inner.c-basic-search > input#Keyword')
            submit_button = self.driver.find_element(By.CSS_SELECTOR, 'div.p-search-job__search-bar-inner.c-search-bar__inner.c-basic-search > button#Search')
            project_search_box.send_keys('スクレイピング')
            submit_button.click()
        
        except Exception as e:
            logger.error({
                'action': 'LancersScraper().search_projects()', 
                'status': 'exception', 
                'message': e
            })
            self.driver.quit()

        finally:
            logger.info({
                'action': 'LancersScraper().search_projects()', 
                'status': 'success'
            })
            sleep(1)

    def start(self):
        self.login()
        self.search_projects()

    def get_page_projects(self, page_num: int=1, urls: Union[str, List[str]]='') -> List[Dict]:
        projects = []
        try:
            if not urls == '':
                logger.info({
                    'action': 'LancersScraper().get_page_projects(): if not urls == ""', 
                    'status': 'run'
                })
                # self.driver.get(url)
                loop = asyncio.get_event_loop()
                with concurrent.futures.ProcessPoolExecutor() as pool:
                    gathers = [asyncio.gather(_asy_scrape(url, executor=pool, loop=loop)) for url in urls]
                loop.run_until_complete(gathers)

            elems = self.driver.find_elements(By.CSS_SELECTOR, 'div.c-media__content__right > a.c-media__title') 
            project_name_list_db = ProjectManager().select_all_name()     # project_name_list_db = session.query(Project.name).all()

            for i, elem in enumerate(elems):
                project_name = elem.find_element(By.CSS_SELECTOR, 'span.c-media__title-inner').text
                pattern = re.compile(r'￥n|\n|\r\n')
                if pattern.search(project_name):
                    project_name = re.sub('￥n|\n|\r\n', ' ', project_name)

                if project_name not in project_name_list_db:
                    project_url = elem.get_attribute('href')
                
                    projects[i] = {
                        'name': project_name,
                        'url': project_url, 
                        'page': page_num, 
                    }

                    print(f'projects[{i}]: ', projects[i])

            else:
                print('条件に一致するプロジェクトがみつかりませんでした.')
                self.driver.quit()

        except Exception as e:
            logger.error({
                'action': 'LancersScraper().get_page_projects()', 
                'status': 'exception', 
                'message': e
            })
            self.driver.quit()

        finally:
            print('projects: ', projects)
            return projects
    
    def _get_multiple_pages_urls(self, page: Union[int, bool]=True) -> List[Dict[str, Union[str, int]]]:
        try:
            logger.info({
                'action': '_get_multiple_pages_urls()', 
                'status': 'run', 
            })

            page_num = 0
            page_urls = []
            while page:
                page_num += 1
                url = ""
                page_urls.append({'url': url, 'page_num': page_num})
                next_button = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, 'pager__item__anchor')))
                # next_button = self.driver.find_element(By.CLASS_NAME, 'pager__item__anchor')
                if page == page_num:
                    '''
                    指定ページ数に達したら, 値を返しループを抜ける.
                    '''
                    logger.info({
                        'action': '_get_multiple_pages_urls()', 
                        'status': 'success', 
                        'message': f'_get_multiple_pages_urls() acquired {page}pages urls'
                    })
                    print(page_urls)    #
                    return page_urls
                
                if next_button:
                    next_button.click()
                else:
                    '''
                    最後のページに達したら, 値を返しループを抜ける.
                    '''
                    logger.info({
                        'action': '_get_multiple_pages_urls()', 
                        'status': 'success', 
                        'message': '_get_multiple_pages_urls() acquired all urls'
                    })
                    print(page_urls)    #
                    return page_urls

        except Exception as e:
            logger.error({
                'action': '_get_multiple_pages_urls()', 
                'status': 'exception', 
                'message': e
            })
            self.driver.quit()

    
    def get_multiple_pages_projects(self, page: Union[int, bool]=True) -> List[Dict[str, Union[str, int]]]:
        try:
            urls = _get_multiple_pages_urls(page)
            tasks = []
            projects = []
            
            for url in urls:
                tasks.append(self.get_page_projects(page_num=url['page_num'], url=url['url']))

            get_page_projects = asyncio.gather(*tasks)
            loop = asyncio.get_event_loop()
            result = projects.append(*loop.run_until_complete(get_page_projects))

            return result
            
        except Exception as e:
            logger.error({
                'action': 'get_multiple_pages_projects()', 
                'status': 'exception', 
                'message': e
            })
            self.driver.quit()

        finally:
            loop.close()

    async def _get_detail_page_patternA(self) -> Union[Tuple[str], bool]:
        try:
            logger.info({
                'action': '_get_detail_page_patternA', 
                'status': 'run', 
            })

            low_price = await self.driver.find_elements(By.CSS_SELECTOR, 'span.workprice__text > span.price-block.workprice__text--low > span.price-number').text
            description = self.driver.find_element(By.CSS_SELECTOR, 'dl.c-definitionList.definitionList--holizonalA01 > dd.definitionList__description').text
            return {'low_price': low_price, 'description': description}
        except:
            return False
        finally:
            logger.info({
                'action': '_get_detail_page_patternA', 
                'status': 'success', 
            })

    async def _get_detail_page_patternB(self) -> Union[Tuple[str], bool]:
        try:
            logger.info({
                'action': '_get_detail_page_patternB', 
                'status': 'run', 
            })

            low_price = await self.driver.find_element(By.CSS_SELECTOR, 'div.cp-projectView__compensation').text
            if re_match := re.match(r'^(0|[1-9]\d{0,2}(,\d{3})+)', low_price):
                low_price = re_match.group()
            elif re_match := re.match(r'^([1-9]\d*)', low_price):
                low_price = re_match.group()
            description = self.driver.find_element(By.CSS_SELECTOR, 'dl.cp-projectView__dltable__list > dd.cp-projectView__dltable__detail').text
            return {'low_price': low_price, 'description': description}
        except:
            return False
        finally:
            logger.info({
                'action': '_get_detail_page_patternB', 
                'status': 'success', 
            })
    
    async def _get_detail_page_patternC(self) -> Union[Tuple[str], bool]:
        try:
            logger.info({
                'action': '_get_detail_page_patternC', 
                'status': 'run', 
            })

            low_price = await self.driver.find_element(By.CSS_SELECTOR, 'span.workprice__text > span.price-block.workprice__text--high > span.price-number').text
            description = self.driver.find_element(By.CSS_SELECTOR, 'dl.c-definitionList.definitionList--holizonalA01 > dd.definitionList__description').text
            return {'low_price': low_price, 'description': description}
        except:
            return False
        finally:
            logger.info({
                'action': '_get_detail_page_patternC', 
                'status': 'success', 
            })

    def get_multiple_pages_projects_detail(self, page: Union[int, str]="all") -> List[Dict]:
        logger.info({
            'action': 'get_multiple_pages_projects_detail()', 
            'status': 'run'
        })
        
        try:
            projects = self.get_multiple_pages_projects(page)
            for i, project in enumerate(projects):
                url = project['url']
                self.driver.get(url)
                logger.info({
                    'action': 'get_multiple_pages_projects_detail()', 
                    'status': 'transition to URL',
                    'url': url
                })
                self.driver.implicitly_wait(2)
                ### reward ###  #
                loop = asyncio.get_event_loop()
                get_details = asyncio.gather(
                    self._get_detail_page_patternA(),
                    self._get_detail_page_patternB(),
                    self._get_detail_page_patternC(),
                )
                results = await get_details
                loop.close()

                for result in results:
                    if type(result) == dict:
                        print('result: ', type(result), result)
                        details = result
                
                if details:
                    project.update(details)

                projects_with_detail[i] = [project]
                
                # if len(self.driver.find_elements(By.CSS_SELECTOR, 'span.workprice__text > span.price-block.workprice__text--low > span.price-number')) > 0:
                #     low_price = self.driver.find_element(By.CSS_SELECTOR, 'span.workprice__text > span.price-block.workprice__text--low > span.price-number').text
                #     description = self.driver.find_element(By.CSS_SELECTOR, 'dl.c-definitionList.definitionList--holizonalA01 > dd.definitionList__description').text
                #     print('page-pattern: a')    # debug
                # elif len(self.driver.find_elements(By.CSS_SELECTOR, 'div.cp-projectView__compensation')) > 0:
                #     low_price = self.driver.find_element(By.CSS_SELECTOR, 'div.cp-projectView__compensation').text
                #     if re.match(r'^(0|[1-9]\d{0,2}(,\d{3})+)', low_price):
                #         low_price = re.match(r'^(0|[1-9]\d{0,2}(,\d{3})+)', low_price).group()
                #     elif re.match(r'^([1-9]\d*)', low_price):
                #         low_price = re.match(r'^([1-9]\d*)', low_price).group()
                #     description = self.driver.find_element(By.CSS_SELECTOR, 'dl.cp-projectView__dltable__list > dd.cp-projectView__dltable__detail').text
                #     print('page-pattern: b')    # debug
                # elif len(self.driver.find_elements(By.CSS_SELECTOR, 'span.workprice__text > span.price-block.workprice__text--high > span.price-number')) > 0:
                #     low_price = self.driver.find_element(By.CSS_SELECTOR, 'span.workprice__text > span.price-block.workprice__text--high > span.price-number').text
                #     description = self.driver.find_element(By.CSS_SELECTOR, 'dl.c-definitionList.definitionList--holizonalA01 > dd.definitionList__description').text
                #     print('page-pattern: c')    # debug

                # self.projects[i] = {
                #     'low_price': low_price, 
                #     'descriptin': description, 
                # }

            print(projects_with_detail)
            # return projects_with_detail

        except Exception as e:
            logger.error({
                'action': 'get_project_detail()', 
                'status': 'exception', 
                'message': e
            })
            self.driver.quit()

    def quit(self):
        self.driver.quit()


if __name__ == "__main__":
    LS = LancersScraper()
    LS.login()
    LS.search_projects()
    get_page_projects()
    # LS.get_multiple_pages_projects(pages=3) 
    # LS.get_project_detail(pages=3)
    print(LS.projects)       # debug
    sleep(2)       # debug
    LS.quit()