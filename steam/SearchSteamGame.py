import aiohttp
import asyncio
import datetime

async def getSteamGameSearch(keyword: str) -> dict:
    url = "https://steamstats.cn/api/steam/search?q=%s&page=1&format=json&lang=zh-hans" % keyword
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9,zh-TW;q=0.8,en-US;q=0.7,en;q=0.6",
        "pragma": "no-cache",
        "referer": "https://steamstats.cn/",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36"
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(url=url, headers=headers) as resp:
            result = await resp.json()
    return result


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(getSteamGameSearch("monster"))
    print(result["data"]["results"])
