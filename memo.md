# ニコ生クリ奨ランキングのデータ取得

## 配信ページの URL からユーザー ID・ユーザー名とコミュニティ URL を取得

### 返り値の設定

````
下記コードで、user_id_number、user_name、community_id_number を戻り値として返却したいです。
どのようにすればよいでしょうか。

```コード
def get_user_data(stream_urls):

    for stream_url in stream_urls:

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

        # ユーザー名
        user_name_element = soup.select_one('.name')
        user_name = user_name_element.text.strip() if user_name_element else "Not Found"

        # コミュニティID
        community_id_element = soup.select_one('.___name-label___iW8g3').get('href')
        community_id = community_id_element.strip() if community_id_element else "Not Found"

        # community_idから数字のみを抽出
        matched = re.search(r'\d+', community_id)
        if matched:
            community_id_number = matched.group(0)  # 最初にマッチした数字列を取得
        else:
            community_id_number = "Not Found"

        # 結果を表示
        print(f"User ID: {user_id_number}")
        print(f"User Name: {user_name}")
        print(f"Community ID: {community_id_number}")
````

```


### URL からユーザー ID を抽出

```

下記コードで下記 user_id の値が取得できました。
user_id の値の中から数字のみを抽出したいです。
どうしたらよいでしょうか。

```コード
# ユーザーID
user_id_element = soup.select_one('.user-name').get('href')
user_id = user_id_element.strip() if user_id_element else "Not Found"
```

```user_id
https://www.nicovideo.jp/user/121419314/live_programs?ref=watch_user_information
```

```

### たたき台作成

```

下記 URL で Python を用いた web スクレイピングで、ユーザー ID、ユーザー名、コミュニティ ID を取得する方法を教えてください。

https://live.nicovideo.jp/watch/lv342940931

ユーザー ID、ユーザー名、コミュニティ ID の例は下記のとおりです。

ユーザー ID：52053485
ユーザー名：3 時サブ垢
コミュニティ ID：co1992508

```

## ニコ生ランキングから配信ページの URL を取得

### 配信ページ箇所のソースコード

```

<a class="___rk-program-card-detail-title___gJhRF" href="https://live.nicovideo.jp/watch/lv342949002?ref=RankingPage-UserProgramListSection-ProgramCard&amp;provider_type=community" title="家賃2万円の古民家！？内見しにきた！！"><span>家賃 2 万円の古民家！？内見しにきた！！</span></a>

<a class="___rk-program-card-detail-title___gJhRF" href="https://live.nicovideo.jp/watch/lv342947517?ref=RankingPage-UserProgramListSection-ProgramCard&amp;provider_type=community" title="皆様ーこんにちはー何もする事がない！"><span>皆様ーこんにちはー何もする事がない！</span></a>

```

### GPT への注文

下記ニコニコ生放送のランキングサイトからユーザー放送の配信タイトルを、python を用いて web スクレイピングで取得する方法を教えてください。
配信タイトル例：無言、ドライブ配信

https://live.nicovideo.jp/ranking

## git

```

echo "# nicodb-scraping" >> README.md
git init
git add README.md
git commit -m "first commit"
git branch -M main
git remote add origin https://github.com/MASA20201203/nicodb-scraping.git
git push -u origin main

```

```
