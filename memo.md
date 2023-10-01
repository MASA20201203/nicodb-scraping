# プロジェクト作成

## ニコ生ランキングから配信ページの URL を取得

### 配信ページ箇所のソースコード

```
<a class="___rk-program-card-detail-title___gJhRF" href="https://live.nicovideo.jp/watch/lv342949002?ref=RankingPage-UserProgramListSection-ProgramCard&amp;provider_type=community" title="家賃2万円の古民家！？内見しにきた！！"><span>家賃2万円の古民家！？内見しにきた！！</span></a>

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
