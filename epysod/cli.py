import os
import json
import glob
import sqlite3
import urllib.request
import datetime
from pytz import timezone

LOCAL_STORAGE_PATH = f"{os.environ['HOME']}/.local/share/epysod"

def get_url_data(url):
    with urllib.request.urlopen(url) as req:
        info = req.read()

    loaded_info = json.loads(info)
    return loaded_info


def create_db():
    pass

def read_db():
    pass


def configure():
    if not glob.glob(f"{LOCAL_STORAGE_PATH}/"):
        os.makedirs(LOCAL_STORAGE_PATH)

    if not glob.glob(f"{LOCAL_STORAGE_PATH}/db.sqlite"):
        with sqlite3.connect(f"{LOCAL_STORAGE_PATH}/db.sqlite") as conn:
            conn.execute("""create table if not exists fav (eid integer primary key);""")

    return sqlite3.connect(f"{LOCAL_STORAGE_PATH}/db.sqlite")


def all_favs(conn):
    return conn.execute('select * from fav').fetchall()


def register_show(conn, eid):
    result = conn.execute(f"select * from fav where eid = {eid}").fetchall()
    if not result:
        conn.execute(f"insert into fav (eid) values ({eid}) ")
        conn.commit()
        

def search_show(conn, name):
    url = f"https://www.episodate.com/api/search?q={name}"

    info = get_url_data(url)
    results = info['tv_shows']
    if not results:
        print("not found")
        return
    
    eid = results[0]['id']
    register_show(conn, eid)
       

def countdown(eid):
    detail_url = f"https://www.episodate.com/api/show-details?q={eid}"
    info = get_url_data(detail_url)

    name = info['tvShow']['name']
    next_ep = info['tvShow']['countdown']

    air_date = datetime.datetime.strptime(next_ep['air_date'], '%Y-%m-%d %H:%M:%S')
    air_date_utc = air_date.replace(tzinfo=timezone('UTC'))

    now_date_utc = datetime.datetime.utcnow().replace(tzinfo=timezone('UTC'))

    diff = air_date_utc - now_date_utc
    days = diff.days
    hours = diff.seconds // 3600
    mins = diff.seconds // 60 - hours * 60 
    secs = diff.seconds // 1 - mins * 60 
    diff_str = f"{days:>2} days,{hours:>2}h {mins:>2}m"
    print(f"\033[31;1m{name:>10} \033[0m\033[37;7m air in {diff_str} \033[0m {next_ep['name']} S{next_ep['season']}E{next_ep['episode']}\033[0m")



def status():
    with configure() as conn:
        for e,  in all_favs(conn):
            countdown(e)

def add_command(name):
    name = '-'.join(name)
    with configure() as conn:
        search_show(conn, name)
        for e,  in all_favs(conn):
            countdown(e)



