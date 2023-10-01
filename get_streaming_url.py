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
for index, title_div in enumerate(soup.select('.___rk-program-card-detail-title___gJhRF')):
    if index >= 50:  # 50回繰り返したらループを抜ける（ユーザー放送のデータのみ取得）
        break
    titles.append(title_div.text.strip())

    # print("--- title_div ---")
    # print(title_div)

    # hrefの取得
    href = title_div.get('href')  # title_div は既に a タグであるため、直接 get('href') が使える
    stream_url = href.split('?')[0] # URLのクエリパラメータを除去
    if stream_url is not None:
        print(f"URL: {stream_url}")

# 取得した配信タイトルを出力
print("ニコニコ生放送のランキングページのタイトル一覧")
for i, title in enumerate(titles):
    print(f"{i+1}. {title}")





