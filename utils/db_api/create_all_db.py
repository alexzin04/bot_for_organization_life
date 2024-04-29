from asyncio import tasks
from utils.db_api.tasks_db import create as create_task
from utils.db_api.sport_db import create as create_sport
from utils.db_api.finance_db import create as create_finance
import os



def create_new_db():
    if  os.path.exists('./all.db'):
        os.remove('./all.db')
    create_task()
    create_sport()
    create_finance()