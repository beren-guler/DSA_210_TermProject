#I got this from gemini , 
#this is for webtoon kaggle dataset,
#converting the cover image URL to a valid one by adding necessary headers to bypass the server restrictions.

import requests

# Kaggle'daki hata veren o URL
url = "https://webtoon-phinf.pstatic.net/20170519_186/1495168005850vV99u_JPEG/462ff0c6-28a7-4738-88c4-45ecf2321836.jpg?"

# Sunucuyu kandırmak için gereken Header'lar
headers = {
    'Referer': 'https://www.webtoons.com/', # En kritik satır bu!
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

response = requests.get(url, headers=headers)

if response.status_code == 200:

    with open('webtoon_cover.jpg', 'wb') as f:
        f.write(response.content)
    print("Görsel başarıyla indirildi!")
else:
    print(f"Hata Kodu: {response.status_code}")