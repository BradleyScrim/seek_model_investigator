import json
from typing import Dict, Tuple, List

from py import *


lines: int = 0
models_without_content: int = 0
models_with_fairdomhub_link: int = 0
models_without_fairdomhub_link: int = 0
models_with_non_fairdomhub_link: int = 0
models_without_null_url: int = 0
models_with_valid_mime: int = 0
models_with_maybe_mime: int = 0
models_with_invalid_mime: int = 0
models_with_more_then_one_valid_content: int = 0
models_valid: int = 0
download_links_by_mime: Dict[str, List[str]] = {}

with open("data/models_20200916.json", "r") as file:
    for line in file.readlines():
        if len(line.strip()) is 0:
            continue
        lines += 1
        data: json = json.loads(line)

        id: int = data["id"]
        latest_version: int = data["latest_version"]
        content_blobs: json = data["content_blobs"]

        check_domain_link: bool = False
        check_non_fairdom_link: bool = False
        check_null_url: bool = False
        check_mime_yes: bool = False
        check_mime_maybe: bool = False
        check_mime_no: bool = False
        count_valid_blobs_found: int = 0

        try:
            for content in content_blobs:

                blob_valid: bool = True

                # # check URL
                # if content["url"] is not None:
                #     # print(content["url"])
                #     if check_null_url is False:
                #         check_null_url = True
                #         models_without_null_url += 1

                # check MIME
                if content["content_type"] in MIME_TYPES_YES:
                    check_mime_yes = True
                elif content["content_type"] in MIME_TYPES_MAYBE:
                    check_mime_maybe = True
                    blob_valid = False
                    # save download link for later
                    download_link: str = content["link"]
                    if DOMAIN_TO_CHECK in content["link"]:
                        download_link = content["link"] + "/download"
                    download_links_by_mime.setdefault(content["content_type"], []).append(
                        download_link)

                elif content["content_type"] in MIME_TYPES_NO:
                    check_mime_no = True
                    blob_valid = False
                else:
                    print("ERROR: found NEW mime type: {0}".format(content["content_type"]))

                # check, if LINK contains defined domain
                if (DOMAIN_TO_CHECK) in content["link"]:
                    if check_domain_link is False:
                        check_domain_link = True
                        models_with_fairdomhub_link += 1
                else:  # DOMAIN_TO_CHECK not in content["link"]:
                    # print(content["link"])
                    if check_non_fairdom_link is False:
                        check_non_fairdom_link = True
                        models_with_non_fairdomhub_link += 1

                if blob_valid:
                    count_valid_blobs_found += 1

            # finish MIME check
            if check_mime_yes:
                models_with_valid_mime += 1
            elif check_mime_maybe:
                models_with_maybe_mime += 1
            elif check_mime_no:
                models_with_invalid_mime += 1

            # finish domain LINK check: count models without speified domain
            if check_domain_link is False:
                models_without_fairdomhub_link += 1

            # finish validity check
            if count_valid_blobs_found is 1:
                models_valid += 1
            if count_valid_blobs_found > 1:
                models_with_more_then_one_valid_content += 1


        except:
            models_without_content += 1
            continue

print("Number of public models: {0}".format(lines))
print("Number of models with fairdomhub.org-content in link-field: {0}".format(models_with_fairdomhub_link))
print("Number of models with non-fairdomhub.org-content in link-field: {0}".format(models_with_non_fairdomhub_link))
print("Number of models without fairdomhub.org-content in any link-field: {0}".format(models_without_fairdomhub_link))
print("Number of models without content_blobs: {0}".format(models_without_content))
# print("Number of models something in url-field: {0}".format(models_without_null_url))
print("Number of models with valid MIME¹: {0}".format(models_with_valid_mime))
print("Number of models with maybe MIME¹: {0}".format(models_with_maybe_mime))
print("Number of models with invalid MIME¹: {0}".format(models_with_invalid_mime))
print("Number of models with more then one valid model: {0}".format(models_with_more_then_one_valid_content))
print("Number of valid models (usable by MaSyMoS): {0}".format(models_valid))

print("\nunknown Files:")
for s in download_links_by_mime.items():
    print("- {0}, {1} times: {2}".format(s[0], len(s[1]), s[1]))

print("\n¹MIME-overview:\n- valid MIME: {0}\n- maybe MIME: {1}\n- invalid MIME: {2}".format(MIME_TYPES_YES,
                                                                                            MIME_TYPES_MAYBE,
                                                                                            MIME_TYPES_NO))
