from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from apscheduler.schedulers.background import BackgroundScheduler
from scraper import scrape_all_jobs
import json

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

# Scheduler: scrape jobs every hour
scheduler = BackgroundScheduler()
scheduler.add_job(scrape_all_jobs, 'interval', minutes=60)
scheduler.start()

# Initial scrape
scrape_all_jobs()

@app.get("/jobs")
def get_jobs():
    with open("jobs.json", "r") as f:
        jobs = json.load(f)
    return jobs
