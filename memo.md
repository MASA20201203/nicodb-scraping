# ニコ生クリ奨ランキングのデータ取得

## 放送履歴 URL から前日分の配信 URL を取得

### 放送履歴 URL

```
https://com.nicovideo.jp/community/co1992508
https://com.nicovideo.jp/live/co1992508
https://com.nicovideo.jp/live/co1992508?com_header=1&page=1
https://com.nicovideo.jp/live/co[community_id]?com_header=1
https://com.nicovideo.jp/live/co[community_id]
```

### communities テーブル・user_community テーブル作成

```
下記テーブル項目を使用する予定なのですが、mysqlでテーブルを作成する場合、どのように作成したらよいでしょうか。

* user_communityテーブル
id: user_communityID
user.id: ユーザーID
community_id: コミュニティID
created_at: 登録日時
updated_at: 更新日時

* communitiesテーブル
id: コミュニティID
created_at: 登録日時
updated_at: 更新日時

* usersテーブル
id: ユーザーID
name: ユーザー名
created_at: 登録日時
updated_at: 更新日時

また、下記を外部キーとして設定したいです。

user_communityテーブルのuser.idとusersテーブルのid
user_communityテーブルのcommunity.idとcommunitiesテーブルのid


```

```
-- communitiesテーブルの作成
CREATE TABLE communities (
    id INT PRIMARY KEY,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- user_communityテーブルの作成
CREATE TABLE user_community (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    community_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (community_id) REFERENCES communities(id)
);
```

user_community テーブル
111, 333
222, 333

### 既存 users データのバックアップ・削除

```
mysqldump -u test_user -p nicodb_db users > users_20231021.sql

SELECT @@foreign_key_checks;
set foreign_key_checks = 0;
TRUNCATE TABLE users;
TRUNCATE TABLE communities;
TRUNCATE TABLE user_community;
set foreign_key_checks = 1;
SELECT @@foreign_key_checks;

DESCRIBE user_community;
SHOW INDEX FROM user_community;
ALTER TABLE user_community ADD UNIQUE INDEX uc_unique (user_id, community_id);
```

## ユーザー ID・ユーザー名を DB に登録、すでに DB に登録されている場合は、登録しない

### ChatGPT への質問

```

取得したユーザーID・ユーザー名をDBに登録、すでにDBに登録されている場合は、登録しないとしたいのですが、どのようにしたらよいでしょうか。
また、ユーザーIDが既に登録されているが、ユーザー名が異なる場合は、ユーザー名を更新したいです。

DBはMySQLを使用しています。

↓

```

### DB 情報の確認

### MySQL サーバーの起動

```
sudo service mysql status
sudo service mysql start
```

### MySQL コマンド

```
sudo mysql -u root -p
show databases;
use nicodb_db;
show tables;
SHOW COLUMNS FROM テーブル名;
SHOW TABLE STATUS;

SELECT User, Host FROM mysql.user;

test_user
test
```

### テーブル作成

#### アドバイス

```
決めること
データ型
プライマリーキー
ユーザーテーブルはBIGINT（ビッグイント）で
キャラ型イント型日時型だけでいいよ

めっちゃ悩ましいのですが、テーブルの中のユーザーIDってニコニコのIDじゃないですか、それとは別に内部IDを作っておいたほうがいいのかなって
```

#### ChatGPT へのプロンプト

- users テーブル

```
usersテーブルを作成しようとしています。
下記テーブル項目を使用する予定なのですが、mysqlでテーブルを作成する場合、どのように作成したらよいでしょうか。

* テーブル項目
id: ユーザーID（例:128551563）
name: ユーザー名
created_at: 登録日時
updated_at: 更新日時
```

```
CREATE TABLE users (
  id INT PRIMARY KEY,  -- ユーザーID（自動インクリメント）
  name VARCHAR(255) NOT NULL,         -- ユーザー名（NULL不可）
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  -- 登録日時（デフォルトは現在のタイムスタンプ）
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP  -- 更新日時（デフォルトは現在のタイムスタンプ、更新時に自動で更新）
);
```

```
mysql> show columns from users;
+------------+--------------+------+-----+-------------------+-----------------------------------------------+
| Field      | Type         | Null | Key | Default           | Extra                                         |
+------------+--------------+------+-----+-------------------+-----------------------------------------------+
| id         | int          | NO   | PRI | NULL              |                                               |
| name       | varchar(255) | NO   |     | NULL              |                                               |
| created_at | timestamp    | YES  |     | CURRENT_TIMESTAMP | DEFAULT_GENERATED                             |
| updated_at | timestamp    | YES  |     | CURRENT_TIMESTAMP | DEFAULT_GENERATED on update CURRENT_TIMESTAMP |
+------------+--------------+------+-----+-------------------+-----------------------------------------------+
4 rows in set (0.01 sec)
```

### 登録データ確認

```
select count(*) from users;
select * from users;
```

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

```

````

### URL からユーザー ID を抽出

````

下記コードで下記 user_id の値が取得できました。
user_id の値の中から数字のみを抽出したいです。
どうしたらよいでしょうか。

```コード
# ユーザーID
user_id_element = soup.select_one('.user-name').get('href')
user_id = user_id_element.strip() if user_id_element else "Not Found"
````

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
