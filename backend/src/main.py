from typing import List, Dict, Union

from fastapi import FastAPI, Depends

from scraper import LancersScraper


app = FastAPI(
    title="scraing example",
    description="",
    version="0.0.1",
    docs_url=None,
    redoc_url=None,
    openapi_url=None,
)

ls = LancersScraper()

@app.get("/scraping/test")
def get_latest_page_projects():
    ls.start()
    projects = ls.get_page_projects()
    ls.quit()

    return projects

@app.get("/scraping/one-page")
def get_latest_page_projects():
    ls.start()
    projects = ls.get_page_projects()
    ls.quit()

    return projects

@app.get("/scraping/all")
def get_all_projects():
    ls.start()
    projects = ls.get_multiple_pages_projects()
    ls.quit()

    return projects

@app.post("/scraping/")
def post_projects(obj:Dict, pk:int):
    return

@app.put("/scraping/")
def update_projects(obj:Dict, pk:int):
    return

@app.delete("/scraping/delete")
def delete_projects(pk:int):
    return
