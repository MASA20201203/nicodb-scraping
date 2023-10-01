import get_streaming_url

# ニコ生ランキングから配信ページのURLを取得（0時、6時、12時、18時、21時？）
stream_urls = get_streaming_url.get_streaming_url()

# デバック用
for i, stream_url in enumerate(stream_urls):
    print(f"{i+1}. {stream_url}")

# 配信ページのURLからユーザーID・ユーザー名とコミュニティURLを取得
# get_user_data.py

# ユーザーID・ユーザーをDBに登録、すでにDBに登録されている場合は、登録しない


# コミュニティURLから放送履歴URLを取得
# 放送履歴URLから前日分の配信URLを取得
# 前日分の配信URLから配信データ（来場者数・コメント数・広告pt・ギフトpt）を取得・登録
# 1月分の配信データを集計して表示する（Next.js？）


# --- 以下、処理定義 ---