import requests


def parse_NTESSTUDYSI(userId='1024616784'):
    cookies = {
        'STUDY_SESS': '"CkRzH3oHpH+78iv53u8gsPRgUR1QLGfbhj4z2VY0HGKdbTTx1G/+rs1VHEyXQz/xsBabzYmOmtAuEknsT2/DDfv5GVWv326h9xRqsOevsE80Hr8H84pz4ONGcRQ1A4GWT+jXH/TvpTxR5Q29s2lgqeXhgkhk7QVvXUQFfYfwMVInppr6KrivyjY6FmKs/Qou"',
        'STUDY_INFO': '"ocean_yyl@163.com|-1|1024616784|1766502987943"',
        'STUDY_PERSIST': '"dKmEJ3j368/l9gVjCtzSf5rJVeYxUIjP8gdXnmc72Yulh2VTociZwW4Q4yRPs4FzA1U3WiGPUTN6+JrTEC+ndvwAFkRO/aWsGqk4N9LO+2G/BuxJsrFzXU07b5n5a8YC8hua5BsTJNmc8+OrniZ7nkFDfyFa9bTw9+QG8lnw6qMCSWBDpEHqZPtE1vcFMrT37nq/A9TGSd6gcPOHPThw4bMvgn/cbHDYooW/UU0xt/dOSdFA6J5jrZLCRv8JU8qN8WQLi3xTJ45sq/acjsEWiA=="'
    }

    headers = {
    }

    params = {
        'userId': userId,
    }

    response = requests.get('https://www.icourse163.org/home.htm', params=params, cookies=cookies, headers=headers)
    cookie_str = response.headers.get('Set-Cookie')
    return cookie_str.split("NTESSTUDYSI=")[1].split(";")[0]


if __name__ == '__main__':
    EDUWEBDEVICE = parse_NTESSTUDYSI()
    print(EDUWEBDEVICE)
