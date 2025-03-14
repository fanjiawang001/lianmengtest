import requests

url = "https://kim-robot.kwaitalk.com/api/robot/send?key=49ea1f95-98ac-45bf-9a90-9823887f45fe"

payload={
	"groupIds":["5079161946416949"],
    "msgtype1111": "image",
    "image": {
        "media_id": "ks://k0ko9cz6eie5ux2430450ccpkjaozm3wti372ohdt.png/7"
   },
   "msgtype": "text",
    "text": {
        "content": "<@=username(wb_fanjiawang)=>干饭机器人"
   }
}

headers = {
  'Content-Type': 'application/json',
  'Cookie': 'apdid=8e3fc168-a85d-4914-a461-fc339905ad487bbe1df62a573a06f3bfe7dfbbb321f9:1686131922:1; accessproxy_session=ba511a2d-6d39-447a-a022-5750f5d064a2'
}

response = requests.request("POST", url, headers=headers, json=payload)

