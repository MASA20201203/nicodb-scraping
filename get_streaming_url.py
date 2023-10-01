import requests
from bs4 import BeautifulSoup

# ニコニコ生放送のランキングページURL
url = "https://live.nicovideo.jp/ranking"

# URLからHTMLを取得
response = requests.get(url)
response.encoding = response.apparent_encoding  # エンコーディングを設定

# BeautifulSoupオブジェクトを作成
soup = BeautifulSoup(response.text, 'html.parser')

# 配信タイトルが格納されている要素を探してリストに追加
titles = []
for title_div in soup.select('.Mg-btm0px.Pd-right10px.Pd-left10px.H-fix2col .Fz-m.Fw-b'):
    titles.append(title_div.text.strip())

# 取得した配信タイトルを出力
print("ニコニコ生放送のランキングページのタイトル一覧")
for i, title in enumerate(titles):
    print(f"{i+1}. {title}")





