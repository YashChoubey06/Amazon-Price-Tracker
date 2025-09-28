from bs4 import BeautifulSoup
import requests
import smtplib
import os
from dotenv import load_dotenv

load_dotenv()

target_price = 2500

header = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "en-US,en;q=0.9,en-IN;q=0.8",
    "Priority": "u=0, i",
    "Sec-Ch-Ua": "\"Chromium\";v=\"140\", \"Not=A?Brand\";v=\"24\", \"Microsoft Edge\";v=\"140\"",
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": "\"Windows\"",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "cross-site",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36 Edg/140.0.0.0",
}

response = requests.get("https://www.amazon.in/Puma-Unisex-Adult-Black-Shadow-Gray-Sneaker/dp/B0CZPSXNTF/ref=sr_1_8?crid=1YYNU3Q8UBRQ5&dib=eyJ2IjoiMSJ9.GtAxOtXR95mJBits-CU0wU4sNqBBMD0rPJgvT6x0cxuoa_gx7ef0Wvgao4clXwoRJkN0ndZdGSmjCcxEa51zgt8G6EuclQv6_wYFIYRRkCwOuUrp4pZhpaRg0t5KIz87SHG-E9bErv4HQEvfftfDz4z2x3_bUmh8pyHyTj1tQOxf8jcxiygVVkPcb9KqvAW-TBZ49_NvpCHt_qvjNL9Blb4JuyljJ9QYNLs1DzV3lmWSLctTRPzIQ5BKFM497GgG18_kURMRnVM0X2pnpzHHLYJd-9tgEu9puPFbO0EmKG4.Zrp3zjBTVuDg3BLl2jRheOjtwd9cjbynsZgrrSQVIS4&dib_tag=se&keywords=bmw%2Bshoes%2Bfor%2Bmen&nsdOptOutParam=true&qid=1759045830&s=shoes&sprefix=bm%2Bshoes%2Bfor%2Bmen%2Cshoes%2C292&sr=1-8&th=1&psc=1")
website_html = response.text

soup = BeautifulSoup(website_html,"html.parser")

price_decimal = soup.find(name="span",class_="a-price-whole").text
str_price = price_decimal.split(",")
price = int(str_price[0])*1000 + int(str_price[1])

product_title = (soup.find(name="span",id="productTitle").text).rstrip().lstrip()

if price < target_price:

    my_email = os.getenv("MYMAIL")
    my_pass = os.getenv("MYPASS")
    with smtplib.SMTP(os.getenv("SMTP_ADDRESS"), 587) as connection:
        connection.starttls()
        connection.login(
            user=my_email,
            password=my_pass
        )
        msg = f"Subject:Amazon Price Alert!\n\n{product_title} is now {target_price}"
        connection.sendmail(
            from_addr=my_email,
            to_addrs=my_email,
            msg=msg.encode("utf-8")
        )
