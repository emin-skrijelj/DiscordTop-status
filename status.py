import requests
import psutil
import json
import time
import math
import re

headers = {"Authorization":"YOUR TOKEN GOES HERE"}
data = {
    "custom_status" : {
        "text":"test"
    }
}
regex_match = r"total=(\d+).+percent=(.+),.+used=(\d+)"
def convert_bytes(size_bytes):
   if size_bytes == 0:
       return "0B"
   size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
   i = int(math.floor(math.log(size_bytes, 1024)))
   p = math.pow(1024, i)
   s = round(size_bytes / p, 2)
   return "%s %s" % (s, size_name[i])
while True:
    try:

        # gets ram usage converts it to readable 
        ram_usage = str(psutil.virtual_memory())
        usage_v1 = re.findall(regex_match,ram_usage)
        total_ram = convert_bytes(int(usage_v1[0][0]))
        free_ram = convert_bytes(int(usage_v1[0][2]))
        usage_proc = str(usage_v1[0][1])
        cpu_usage_total = str(psutil.cpu_percent())
        total_res = f"RAM|{str(free_ram)}/{str(total_ram)} {usage_proc}%|CPU|{cpu_usage_total}%"
        # sets status to ram usage

        data["custom_status"]["text"] = total_res
        response = requests.patch("https://discord.com/api/v8/users/@me/settings",json=data,headers=headers)
        print(response)
        time.sleep(5)
    except Exception as f:
        print(f)
