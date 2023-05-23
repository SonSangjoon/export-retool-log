import json
import math
import requests
import time

from datetime import date, datetime, timedelta
from tqdm import tqdm

PROJECT_NAME = ""
ACCESS_TOKEN = ""
XSRF_TOKEN = ""


def get_day_timestamp(date):
    date_format = "%Y.%m.%d"
    timestamp = datetime.strptime(date, date_format)
    return timestamp


def get_retool_log_by_timestamp(start_timestamp="", end_timestamp="", page_num=1):
    url = f"https://{PROJECT_NAME}.retool.com/api/auditTrails?createdAt__gte={start_timestamp}&createdAt__lt={end_timestamp}&pageNum={page_num}"

    headers = {
        "Content-Type": "application/json; charset=utf-8",
        "X-XSRF-TOKEN": XSRF_TOKEN,
    }

    cookies = {"accessToken": ACCESS_TOKEN}

    res = requests.get(url, headers=headers, cookies=cookies).json()

    return res


def create_json_file(title="output", data=[]):
    with open(title, "w") as f:
        json.dump(data, f, indent=4)


if __name__ == "__main__":
    # check valid info
    with tqdm(total=1, desc="checking info", unit="request") as pbar:
        initial_res = get_retool_log_by_timestamp()
        pbar.update(1)

    if "success" in initial_res:
        if not initial_res["success"]:
            raise RuntimeError(initial_res["message"])

    # get log date range
    start_date = input("enter start date by yyyy.mm.dd:")
    end_date = input("enter end date by yyyy.mm.dd:")
    timestamp_start = get_day_timestamp(start_date)
    timestamp_end = get_day_timestamp(end_date)

    # set time interval
    d = timedelta(days=1)
    cur_date = timestamp_start

    log = []

    while cur_date <= timestamp_end:
        start, end = int(cur_date.timestamp()), int((cur_date + d).timestamp()) - 1
        res = get_retool_log_by_timestamp(start, end)

        formatted_date = cur_date.strftime("%y.%m.%d")
        totalPage = math.ceil(res["totalCount"] / 10)
        desc = f"extacting {formatted_date}"

        if res["isTotalCountTruncated"]:
            create_json_file(f"[{start_date}-{formatted_date}]_log.json", log)

            raise RuntimeError(f"{formatted_date} exceeds limits, make timedelta smaller")

        if totalPage != 0:
            for i in tqdm(range(totalPage), initial=1, leave=True, desc=desc):
                res = get_retool_log_by_timestamp(start, end)
                log.extend(res["events"])

        cur_date += d

    create_json_file(f"[{start_date}-{end_date}]_log.json", log)

    print(f"retool log data exported to {output_file}")
