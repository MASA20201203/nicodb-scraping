import requests
from bs4 import BeautifulSoup
import re

def main():
    # ニコ生ランキングから配信ページのURLを取得（0時、6時、12時、18時、21時？）
    stream_urls = get_streaming_url()

    # デバック用
    # for i, stream_url in enumerate(stream_urls):
    #     print(f"{i+1}. {stream_url}")

    # 配信ページのURLからユーザーID・ユーザー名とコミュニティURLを取得
    users = get_user_data(stream_urls)

    # ユーザーID・ユーザーをDBに登録、すでにDBに登録されている場合は、登録しない


    # コミュニティURLから放送履歴URLを取得
    # 放送履歴URLから前日分の配信URLを取得
    # 前日分の配信URLから配信データ（来場者数・コメント数・広告pt・ギフトpt）を取得・登録
    # 1月分の配信データを集計して表示する（Next.js？）

# --- 処理定義 ---

# ニコ生ランキングから配信ページのURLを取得（0時、6時、12時、18時、21時？）
def get_streaming_url():

    # ニコニコ生放送のランキングページURL
    url = "https://live.nicovideo.jp/ranking"

    # URLからHTMLを取得
    response = requests.get(url)
    response.encoding = response.apparent_encoding  # エンコーディングを設定

    # BeautifulSoupオブジェクトを作成
    soup = BeautifulSoup(response.text, 'html.parser')

    # 配信タイトルが格納されている要素を探してリストに追加
    stream_urls = []
    for index, title_div in enumerate(soup.select('.___rk-program-card-detail-title___gJhRF')):
        if index >= 50:  # 50回繰り返したらループを抜ける（ユーザー放送のデータのみ取得）
            break

        # hrefの取得
        href = title_div.get('href')  # title_div は既に a タグであるため、直接 get('href') が使える
        stream_url = href.split('?')[0] # URLのクエリパラメータを除去
        if stream_url is not None:
            # print(f"URL: {stream_url}")
            stream_urls.append(stream_url)

    # デバック用
    # for i, stream_url in enumerate(stream_urls):
    #     print(f"{i+1}. {stream_url}")

    return stream_urls

# 配信ページのURLからユーザーID・ユーザー名とコミュニティURLを取得
def get_user_data(stream_urls):

    users = []

    for i, stream_url in enumerate(stream_urls):

        # URLからHTMLを取得
        response = requests.get(stream_url)
        response.encoding = response.apparent_encoding  # エンコーディングを設定

        # BeautifulSoupオブジェクトを作成
        soup = BeautifulSoup(response.text, 'html.parser')

        # ユーザーID
        user_id_element = soup.select_one('.user-name').get('href')
        user_id = user_id_element.strip() if user_id_element else "Not Found"

        # user_idから数字のみを抽出
        matched = re.search(r'\d+', user_id)
        if matched:
            user_id_number = matched.group(0)  # 最初にマッチした数字列を取得
        else:
            user_id_number = "Not Found"

        users[i]['user_id'] = user_id_number

        # ユーザー名
        user_name_element = soup.select_one('.name')
        user_name = user_name_element.text.strip() if user_name_element else "Not Found"
        users[i]['user_name'] = user_name

        # コミュニティID
        community_id_element = soup.select_one('.___name-label___iW8g3').get('href')
        community_id = community_id_element.strip() if community_id_element else "Not Found"

        # community_idから数字のみを抽出
        matched = re.search(r'\d+', community_id)
        if matched:
            community_id_number = matched.group(0)  # 最初にマッチした数字列を取得
        else:
            community_id_number = "Not Found"

        users[i]['community_id'] = community_id_number

        # 結果を表示
        # print(f"User ID: {user_id_number}")
        # print(f"User Name: {user_name}")
        # print(f"Community ID: {community_id_number}")

        # return stream_urls

    # デバック用
    for i, user in enumerate(users):
        print(f"{i+1}. {user}")

# --- 処理実行 ---
if __name__ == "__main__":
    main()
