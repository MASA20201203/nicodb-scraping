import requests
from bs4 import BeautifulSoup

# ニコニコ生放送のランキングページURL
url = "https://live.nicovideo.jp/ranking"

# URLからHTMLを取得
response = requests.get(url)
response.encoding = response.apparent_encoding  # エンコーディングを設定


# print("--- response ---")
# print(response)
# print("--- response.encoding ---")
# print(response.encoding)
# print("--- response.text ---")
# print(response.text)

# BeautifulSoupオブジェクトを作成
soup = BeautifulSoup(response.text, 'html.parser')

# print("--- soup ---")
# print(soup)

# 配信タイトルが格納されている要素を探してリストに追加
titles = []
# for title_div in soup.select('.Mg-btm0px.Pd-right10px.Pd-left10px.H-fix2col .Fz-m.Fw-b'):
for title_div in soup.select('.___rk-program-card-detail-title___gJhRF'):
    titles.append(title_div.text.strip())

# 取得した配信タイトルを出力
print("ニコニコ生放送のランキングページのタイトル一覧")
for i, title in enumerate(titles):
    print(f"{i+1}. {title}")





