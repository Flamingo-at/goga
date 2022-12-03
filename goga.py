import asyncio
import aiohttp

from re import findall
from imbox import Imbox
from loguru import logger
from aiohttp import ClientSession
from random import choice, randint
from aiohttp_proxy import ProxyConnector
from string import digits, ascii_lowercase, ascii_uppercase


def random_tor_proxy():
    proxy_auth = str(randint(1, 0x7fffffff)) + ':' + \
        str(randint(1, 0x7fffffff))
    proxies = f'socks5://{proxy_auth}@localhost:' + str(choice(tor_ports))
    return(proxies)


async def get_connector():
    if use_tor_proxy:
        connector = ProxyConnector.from_url(random_tor_proxy())
    else:
        connector = None
    return(connector)


def get_imap(provider: str, login: str, password: str):
    return Imbox(
        provider,
        username=login,
        password=password,
        ssl=True,
        ssl_context=None,
        starttls=None)


async def get_code_email(email: str, password: str):
    imbox = get_imap('imap.rambler.ru', email, password)
    return await recv_message(imbox)


async def recv_message(imbox: Imbox):
    folder = "Inbox"
    for _, message in imbox.messages(folder=folder)[::-1]:
        if message.sent_from[0]["email"] == "support@x3english.com":
            return findall(r'<strong>(\d{6})<.strong>', message.body["plain"][0])[0]
    return await recv_message(imbox)


async def info_generate():
    str = '1234567890abcdef'
    device_id = ''.join([choice(str) for _ in range(16)])
    info = ''.join([choice(str) for _ in range(9)])
    info1 = ''.join([choice(str) for _ in range(6)])
    info2 = ''.join([choice(str) for _ in range(6)])
    return([device_id, info + info1, info + info2])


async def register(client: ClientSession, email: str, password: str):
    try:
        device_id, info1, info2 = await info_generate()
        registration_id = ''.join([choice(digits + ascii_lowercase + ascii_uppercase) for _ in range(22)]) + ':' + \
            'APA91b' + ''.join([choice(digits + ascii_lowercase +
                                       ascii_uppercase + '_' + '-') for _ in range(134)])

        response = await client.post('https://app.goga.ai/api/v1/auth/register-anonymous',
                                     json={
                                         "platform": "app",
                                         "language": "UA",
                                         "setting": {
                                             "daily_learn_time": '0',
                                             "notification_enable": 'false',
                                             "level": '1',
                                             "target": '1'
                                         },
                                         "registration_id": registration_id,
                                         "platform_type": "android",
                                         "device_id": device_id,
                                         "info": f"{info1}, {info2}, android 30",
                                         "country": "UA"
                                     })
        data = await response.json()
        token = 'Bearer ' + data['data']['token']

        await client.post('https://app.goga.ai/api/v1/users/bind-email',
                          json={
                              "password": password,
                              "code": "",
                              "email": email
                          }, headers={'authorization': token})

        await client.post('https://app.goga.ai/api/v1/users/verify-email',
                          json={
                              "email": email,
                              "language": "en"
                          }, headers={'authorization': token})
        return(token)
    except:
        logger.error(await response.text())
        raise Exception()


async def confirm_email(client: ClientSession, code: str, token: str):
    await client.post('https://app.goga.ai/api/v1/users/verify-code',
                      json={
                          "code": code
                      }, headers={'authorization': token})


async def add_referral_code(client: ClientSession, token: str):
    await client.post('https://app.goga.ai/api/v1/user-referrals/claim',
                      json={
                          "referral_code": ref
                      }, headers={'authorization': token})


async def worker(q: asyncio.Queue):
    while True:
        try:
            async with aiohttp.ClientSession(connector=await get_connector()) as client:

                emails = await q.get()
                email, password = emails.split(":")

                logger.info('Registering')
                token = await register(client, email, password)

                logger.info('Get code email')
                code = await get_code_email(email, password)

                logger.info('Email confirmation')
                await confirm_email(client, code, token)

                logger.info('Add referral code')
                await add_referral_code(client, token)

        except:
            logger.error('Error\n')
            with open('error.txt', 'a', encoding='utf-8') as f:
                f.write(f'{email}:{password}\n')
        else:
            logger.info('Saving data')
            with open('registered.txt', 'a', encoding='utf-8') as f:
                f.write(f'{email}:{password}\n')
            logger.success('Successfully\n')

        await asyncio.sleep(delay)


async def main():
    emails = open("rambler_emails.txt", "r+").read().strip().split("\n")

    q = asyncio.Queue()

    for account in list(emails):
        q.put_nowait(account)

    tasks = [asyncio.create_task(worker(q)) for _ in range(threads)]
    await asyncio.gather(*tasks)


if __name__ == '__main__':
    print("Bot GOGA @flamingoat\n")

    ref = str(input('Refferal code: '))
    threads = int(input('Threads: '))
    delay = int(input('Delay(sec): '))
    use_tor_proxy = input('Use tor proxies?(y/n): ').lower()

    if use_tor_proxy == 'y':
        tor_ports = [9150]
        use_tor_proxy = True
    else:
        use_tor_proxy = False

    asyncio.run(main())