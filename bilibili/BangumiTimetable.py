import aiohttp
import asyncio
import datetime

async def get_new_bangumi_json() -> dict:
    url = "https://bangumi.bilibili.com/web_api/timeline_global"
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9",
        "origin": "https://www.bilibili.com",
        "referer": "https://www.bilibili.com/",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36"
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url=url, headers=headers) as resp:
            result = await resp.json()
    return result


async def get_formatted_new_bangumi_json() -> list:
    all_bangumi_data = await get_new_bangumi_json()
    all_bangumi_data = all_bangumi_data["result"][-7:]
    formatted_bangumi_data = list()

    for bangumi_data in all_bangumi_data:
        temp_bangumi_data_list = list()
        for data in bangumi_data["seasons"]:
            temp_bangumi_data_dict = dict()
            temp_bangumi_data_dict["title"] = data["title"]
            temp_bangumi_data_dict["cover"] = data["cover"]
            temp_bangumi_data_dict["pub_index"] = data["pub_index"]
            temp_bangumi_data_dict["pub_time"] = data["pub_time"]
            temp_bangumi_data_dict["url"] = data["url"]
            temp_bangumi_data_list.append(temp_bangumi_data_dict)
        formatted_bangumi_data.append(temp_bangumi_data_list)

    return formatted_bangumi_data


async def formatted_output_bangumi(days: int) -> str:
    formatted_bangumi_data = await get_formatted_new_bangumi_json()
    temp_output_substring = ["------BANGUMI------\n"]
    now = datetime.datetime.now()
    for index in range(days):
        temp_output_substring.append(now.strftime("\n%m-%d 即将播出："))
        for data in formatted_bangumi_data[index]:
            temp_output_substring.append("\n%s %s %s\n" % (data["pub_time"], data["title"], data["pub_index"]))
            temp_output_substring.append("url:%s\n" % (data["url"]))
        temp_output_substring.append("\n\n----------------\n")
        now += datetime.timedelta(days=1)
    return "".join(temp_output_substring)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(formatted_output_bangumi(2))
    print(result)
