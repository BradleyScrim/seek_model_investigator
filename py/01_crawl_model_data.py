from typing import Dict

import requests
import json

from py import *

import urllib.request

BASE_URL = 'https://www.fairdomhub.org'


def json_for_resource(type, id):
    headers = {
        "Accept": "application/vnd.api+json",
        "Accept-Charset": "ISO-8859-1"
    }

    r = requests.get(BASE_URL + "/" + type + "/" + str(id), headers=headers)
    r.raise_for_status()
    return r.json()


stats_models: int = 0
stats_files: int = 0

"""
# get data
- data.id
- data.attributes.latest_version
- data.attributes.content_blobs.*.orginal_filename
- data.attributes.content_blobs.*.content_type
- data.attributes.content_blobs.*.link
- data.attributes.content_blobs.*.url
"""
with open("data/models.json", "a") as file:
    for model_id in range(0, 1000):
        if model_id % 50 is 0:
            # print("current id: {0}".format(model_id))
            pass
        try:
            result = json_for_resource("models", model_id)
        except Exception as e:
            # print("no data for #{0}".format(model_id),e)
            continue

        # write meta data to file
        collector: Dict = dict(id=result["data"]["id"],
                               latest_version=result["data"]["attributes"]["latest_version"],
                               content_blobs=result["data"]["attributes"]["content_blobs"])
        file.write(json.dumps(collector) + "\n")
        stats_models += 1

        # download models
        try:
            for content in result["data"]["attributes"]["content_blobs"]:
                if content["content_type"] in MIME_TYPES_YES \
                        or content["content_type"] in MIME_TYPES_MAYBE:
                    download_link: str = content["link"]

                    filename: str = "data/f_" + \
                                    str(content["content_type"]).replace("/", "-") + \
                                    "_" + \
                                    result["data"]["id"] + \
                                    "_" + \
                                    download_link.rpartition("/")[2]

                    if DOMAIN_TO_CHECK in content["link"]:
                        download_link = content["link"] + "/download"
                    else:
                        print("download from: " + download_link)

                    print(download_link + " → " + filename)
                    urllib.request.urlretrieve(download_link, filename)
                    stats_files += 1

        except Exception as e:
            print("skip download for model {0}:".format(result["data"]["id"]), e)

print("done, found {0} models and downloaded {1} files".format(stats_models, stats_files))
