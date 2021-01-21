import requests, json

def fetch_all_apps_steamspy():
    url = "https://steamspy.com/api.php?request=all"
    response = requests.request("GET", url).json()
    resp = response.values()
    return list(resp)

def fetch_all_apps():
    url = "http://api.steampowered.com/ISteamApps/GetAppList/v0002/?key=264F85DF8998D2B69F9CA82C2DEF7A9B&format=json"
    response = requests.request("GET", url).json()
    apps = response['applist']['apps']
    return apps[0:100]

def fetch_details(appid):
    url = f"http://store.steampowered.com/api/appdetails?appids={appid}"
    response = requests.request("GET", url).json()
    apps = response
    return apps

def fetch_details_steamspy(appid):
    url = f"https://steamspy.com/api.php?request=appdetails&appid={appid}"
    response = requests.request("GET", url).json()
    return dict(response)