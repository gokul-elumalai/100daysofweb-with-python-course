import aiohttp
import requests
import bs4
from colorama import Fore
import asyncio


# async def get_html(episode_number: int) -> str:
#     print(f"{Fore.YELLOW}Getting HTML for episode {episode_number}", flush=True)
#
#     url = f'https://talkpython.fm/{episode_number}'
#     resp = requests.get(url)
#     resp.raise_for_status()
#
#     return resp.text

async def get_html(episode_number: int) -> str:
    print(f"{Fore.YELLOW}Getting HTML for episode {episode_number}", flush=True)

    url = f'https://talkpython.fm/{episode_number}'

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            resp.raise_for_status()

            return await resp.text()


async def get_title(html: str, episode_number: int) -> str:
    print(f"{Fore.CYAN}Getting TITLE for episode {episode_number}", flush=True)
    soup = bs4.BeautifulSoup(html, 'html.parser')
    header = soup.select_one('h1')
    return header.text.strip() if header else "MISSING"


def main():
    loop = asyncio.new_event_loop()
    loop.run_until_complete(get_title_range())
    print("Done.")


async def get_title_range():
    # Please keep this range pretty small to not DDoS my site. ;)
    tasks = []
    for n in range(150, 170):
        tasks.append((n, asyncio.create_task(get_html(n))))

    for n, t in tasks:
        html = await t
        title = await get_title(html, n)
        print(f"{Fore.WHITE}Title found: {title}", flush=True)


if __name__ == '__main__':
    main()
