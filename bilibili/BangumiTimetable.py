import aiohttp
import asyncio
import datetime

async def getNewBangumiJson() -> dict:
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


async def getNewBangumi() -> list:
    allBangumiData = await getNewBangumiJson()
    allBangumiData = allBangumiData["result"][-7:]
    formatedBangumiData = list()

    for bangumiData in allBangumiData:
        tempBangumiDataList = list()
        for data in bangumiData["seasons"]:
            tempBangumiDataDict = dict()
            tempBangumiDataDict["title"] = data["title"]
            tempBangumiDataDict["cover"] = data["cover"]
            tempBangumiDataDict["pub_index"] = data["pub_index"]
            tempBangumiDataDict["pub_time"] = data["pub_time"]
            tempBangumiDataDict["url"] = data["url"]
            tempBangumiDataList.append(tempBangumiDataDict)
        formatedBangumiData.append(tempBangumiDataList)

    return formatedBangumiData


async def formattedOutputBangumi(days: int) -> str:
    formatedBangumiData = await getNewBangumi()
    outputStr = "------BANGUMI------\n"
    now = datetime.datetime.now()
    for index in range(days):
        outputStr += now.strftime("\n%m-%d 即将播出：")
        for data in formatedBangumiData[index]:
            outputStr += "\n%s %s %s\nurl:%s\n" % (data["pub_time"], data["title"], data["pub_index"], data["url"])
        outputStr += "\n\n----------------\n"
        now += datetime.timedelta(days=1)
    return outputStr


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(formattedOutputBangumi(2))
    print(result)
