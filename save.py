#!/usr/bin/python

import urllib

from os import listdir
import os,sys,shutil
import json

saved_objects_endpoint = "http://127.0.0.1:5701/api/saved_objects?page={page}"
output="./out"
try:
  os.mkdir(output)
except:
  pass


def fetch_saved_objects():
	saved_types={}

	page_num = 1
	found_data = True
	while found_data:
		request_url = saved_objects_endpoint.format(page=page_num)
		response = urllib.urlopen(request_url)
		page = response.read()
		page_json = json.loads(page)
		saved_objects = page_json["saved_objects"]
		if ["type"] == "config":
			continue
		count = len(page_json["saved_objects"])
		for saved_object in saved_objects:
			type = saved_object["type"]
			attributes = saved_object["attributes"]	
			if type not in saved_types:
				saved_types[type]=[]
			for bad_key in ["version","type","id","updated_at"]:
				del(saved_object[bad_key])
			saved_types[type].append(json.dumps(saved_object))
		else:
			found_data=False
		page_num = page_num + 1
	return saved_types

saved_objects = fetch_saved_objects()
for saved_type in saved_objects:
  i = 0
  for saved_object in saved_objects[saved_type]:
    out = output + "/" + saved_type + str(i) + ".json"
    f = open(out, 'w')
    f.write(saved_object)
    f.close()
    i += 1

