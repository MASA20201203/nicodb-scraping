import requests
from bs4 import BeautifulSoup
import re
import mysql.connector
from dotenv import load_dotenv
import os


def main():
    # ニコ生ランキングから配信ページのURLを取得（0時、6時、12時、18時、21時？）
    stream_urls = get_streaming_urls()

    # デバック用
    # for i, stream_url in enumerate(stream_urls):
    #     print(f"{i+1}. {stream_url}")

    # 配信ページのURLからユーザーID・ユーザー名とコミュニティURLを取得
    users = get_users(stream_urls)

    # デバック用
    for i, user in enumerate(users):
        print(f"{i+1}. {user}")

    # ユーザーID・ユーザー名をDBに登録、すでにDBに登録されている場合は、登録しない。ユーザーIDが既に登録されているが、ユーザー名が異なる場合は、ユーザー名を更新する
    for user in users:
        register_users(user['user_id'], user['user_name'],
                       user['community_id'])

    # コミュニティIDから放送履歴URLを取得
    streaming_history_urls = get_streaming_history_urls()

    # デバック用
    for i, streaming_history_url in enumerate(streaming_history_urls):
        print(f"{i+1}. {streaming_history_url}")

    # 放送履歴URLから前日分の配信URLを取得
    prev_day_streaming_urls = get_prev_day_streaming_urls(
        streaming_history_urls)

    # 前日分の配信URLから配信データ（来場者数・コメント数・広告pt・ギフトpt）を取得・登録
    # get_streaming(

    # 1月分の配信データを集計して表示する（Next.js？）

# --- 処理定義 ---


def get_streaming_urls() -> list:
    """配信ページのURL取得

    ニコ生ランキングから配信ページのURLを取得（0時、6時、12時、18時、21時？）

    Returns:
        list: 公式ニコ生ランキングから取得した配信ページのURLのリスト
    """

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
        # title_div は既に a タグであるため、直接 get('href') が使える
        href = title_div.get('href')
        stream_url = href.split('?')[0]  # URLのクエリパラメータを除去
        if stream_url is not None:
            # print(f"URL: {stream_url}")
            stream_urls.append(stream_url)

    # デバック用
    # for i, stream_url in enumerate(stream_urls):
    #     print(f"{i+1}. {stream_url}")

    return stream_urls


def get_users(stream_urls: list) -> list:
    """配信情報取得

    配信ページのURLからユーザーID・ユーザー名とコミュニティURLを取得

    Args:
        stream_urls (list): 公式ニコ生ランキングから取得した配信ページのURLのリスト

    Returns:
        list[dict(str)]: ユーザーid、ユーザー名、コミュニティidを格納した辞書のリスト
    """

    users = []

    for i, stream_url in enumerate(stream_urls):

        # URLからHTMLを取得
        response = requests.get(stream_url)
        response.encoding = response.apparent_encoding  # エンコーディングを設定

        # BeautifulSoupオブジェクトを作成
        soup = BeautifulSoup(response.text, 'html.parser')

        user = {}

        # ユーザーID
        user_id_element = soup.select_one('.user-name').get('href')
        user_id = user_id_element.strip() if user_id_element else "Not Found"
        matched = re.search(r'\d+', user_id)  # user_idから数字のみを抽出
        user['user_id'] = matched.group(0) if matched else "Not Found"

        # ユーザー名
        user_name_element = soup.select_one('.name')
        user['user_name'] = user_name_element.text.strip(
        ) if user_name_element else "Not Found"

        # コミュニティID
        community_id_element = soup.select_one(
            '.___name-label___iW8g3').get('href')
        community_id = community_id_element.strip() if community_id_element else "Not Found"
        matched = re.search(r'\d+', community_id)  # community_idから数字のみを抽出
        user['community_id'] = matched.group(0) if matched else "Not Found"

        # user ディクショナリを users リストに追加
        # print(user)
        users.append(user)

    # デバック用
    # for i, user in enumerate(users):
    #     print(f"{i+1}. {user}")

    return users


def register_users(user_id: str, user_name: str, community_id: str) -> None:
    """ユーザー・コミュニティ情報登録

    ユーザーID・ユーザー名・コミュニティIDをDBに登録、すでにDBに登録されている場合は、登録しない。
    ユーザーIDが既に登録されているが、ユーザー名が異なる場合は、ユーザー名を更新する

    Args:
        user_id（str）: ユーザーID
        user_name（str）: ユーザー名
        community_id（str）: コミュニティID
    """

    # デバック用
    # print("--- user_info ---")
    # print(user_id, user_name)

    # .envファイルから環境変数を読み込む
    load_dotenv()
    DB_HOST = os.environ.get('DB_HOST')
    DB_USER = os.environ.get('DB_USER')
    DB_PASSWORD = os.environ.get('DB_PASSWORD')
    DB_NAME = os.environ.get('DB_NAME')

    # MySQLへの接続を確立
    cnx = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )

    # カーソルオブジェクトを作成
    cursor = cnx.cursor()

    # usersテーブルを更新
    sql = """
    INSERT INTO users (id, name)
    VALUES (%s, %s)
    ON DUPLICATE KEY UPDATE name = VALUES(name);
    """

    # # デバック用
    # print('--- users ---')
    # print(user_id, user_name)

    cursor.execute(sql, (user_id, user_name))

    # communitiesテーブルを更新
    sql = """
    INSERT INTO communities (id)
    VALUES (%s)
    ON DUPLICATE KEY UPDATE id=id;
    """

    # デバック用
    # print('--- communities ---')
    # print(type(community_id))
    # print(community_id)

    cursor.execute(sql, (community_id, ))

    # user_communityテーブルを更新

    # user_communityテーブルに既に同じ組み合わせが存在するか確認
    check_sql = """
    SELECT COUNT(*) FROM user_community WHERE user_id = %s AND community_id = %s
    """

    cursor.execute(check_sql, (user_id, community_id))
    if cursor.fetchone()[0] == 0:

        sql = """
        INSERT INTO user_community (user_id, community_id)
        VALUES (%s, %s)
        """

        # デバック用
        # print('--- user_community ---')
        # print(user_id, community_id)

        cursor.execute(sql, (user_id, community_id))

    # 変更をコミット
    cnx.commit()

    # 接続を閉じる
    cursor.close()
    cnx.close()


def get_streaming_history_urls() -> list:
    """コミュニティIDから放送履歴URLを取得

    communitiesテーブル.id（コミュニティID）を用いて、放送履歴URLを作成する

    Returns:
        list: 放送データ取得対象の放送履歴URLのリスト
    """

    # .envファイルから環境変数を読み込む
    load_dotenv()
    DB_HOST = os.environ.get('DB_HOST')
    DB_USER = os.environ.get('DB_USER')
    DB_PASSWORD = os.environ.get('DB_PASSWORD')
    DB_NAME = os.environ.get('DB_NAME')

    # MySQLへの接続を確立
    cnx = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )

    # カーソルオブジェクトを作成
    cursor = cnx.cursor()

    # communitiesテーブルからidを取得
    sql = "SELECT id FROM communities"
    cursor.execute(sql)

    # 取得したIDを保存するためのリスト
    community_ids = [row[0] for row in cursor.fetchall()]

    # 接続を閉じる
    cursor.close()
    cnx.close()

    # デバッグ用
    # for i, community_id in enumerate(community_ids):
    #     print(f"{i+1}. {community_id}")

    # 放送履歴URLを格納するリストを作成
    streaming_history_urls = []
    streaming_history_url_template = "https://com.nicovideo.jp/live/co"
    for community_id in community_ids:
        streaming_history_url = f"{streaming_history_url_template}{community_id}"
        streaming_history_urls.append(streaming_history_url)

    return streaming_history_urls


# 放送履歴URLから前日分の配信URLを取得する
def get_prev_day_streaming_urls(streaming_history_urls) -> list:
    """前日分の配信URL取得

    放送履歴URLから前日分の配信URLを取得

    Args:
        streaming_history_urls (list): 放送履歴URLのリスト

    Returns:
        list: 前日分の配信URLのリスト
    """

    prev_day_urls = []

    for streaming_history_url in streaming_history_urls:
        response = requests.get(streaming_history_url)
        response.encoding = response.apparent_encoding  # エンコーディングを設定
        soup = BeautifulSoup(response.text, 'html.parser')

        # 以下のセレクタは仮のものです。実際のHTML構造に合わせて調整する必要があります。
        prev_day_elements = soup.select('.liveDate')

        print("--- streaming_history_url ---")
        print(streaming_history_url)

        for element in prev_day_elements:
            print("--- element ---")
            print(element)
            print(element.text.strip())
            # href = element.get('href')
            # if href:
            #     prev_day_urls.append(href)

        break

    return prev_day_urls

# 前日分の配信URLから配信データ（来場者数・コメント数・広告pt・ギフトpt）を取得・登録
# def get_streaming(


# --- 処理実行 ---
if __name__ == "__main__":
    main()
