import requests
from config import API_TOKEN
URL="https://api.football-data.org/v4/competitions/PL/matches"
def get_matches(status=None):
 headers={"X-Auth-Token":API_TOKEN}
 params={}
 if status: params["status"]=status
 r=requests.get(URL,headers=headers,params=params,timeout=30)
 if r.status_code!=200:return []
 return r.json().get("matches",[])
