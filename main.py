import requests
from bs4 import BeautifulSoup

def main():
    # ニコ生ランキングから配信ページのURLを取得（0時、6時、12時、18時、21時？）
    stream_urls = get_streaming_url()

    # デバック用
    for i, stream_url in enumerate(stream_urls):
        print(f"{i+1}. {stream_url}")

    # 配信ページのURLからユーザーID・ユーザー名とコミュニティURLを取得
    get_user_data(stream_urls)

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

    for stream_url in stream_urls:

        # URLからHTMLを取得
        response = requests.get(stream_url)
        response.encoding = response.apparent_encoding  # エンコーディングを設定

        # BeautifulSoupオブジェクトを作成
        soup = BeautifulSoup(response.text, 'html.parser')

        # ユーザーデータ（ユーザーID・ユーザー名・コミュニティURL）を取得
        users = []
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


# --- 処理実行 ---
if __name__ == "__main__":
    main()
