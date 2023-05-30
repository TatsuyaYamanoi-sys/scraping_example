# 【fastapi_blog】
<dl>
    <dt>目的: </dt> 
    <dd>fastAPIの学習</dd>
</dl>
<dl>
    <dt>課題: </dt> 
    <dd>-</dd>
</dl>
<dl>
    <dt>機能: </dt>
    <dd>ユーザーをCRUDできる。</dd>
    <dl>
        <dt>アクティブユーザーはスクレイピング機能を利用できる。</dt>
        <dd>検索キーワードをしてスクレイピングできる。</dd>
        <dd>1pageのデータを取得・表示</dd>
        <dd>全てのデータを取得・表示</dd>
    </dl>
    <dl>
        <dt>アクティブユーザーはデータベースでCRUDできる。</dt>
        <dd>現在取得・表示中のデータをPOSTメソッドで保存できる。</dd>
        <dd>データの状態を更新(PUT)・削除(DELETE)できる。</dd>
        <dd>前回保存したデータに絞り込んで呼び出すことが出来る。(create_atより最新の日付のデータを呼び出せる。)</dd>
    </dl>
</dl>
<dl>
    <dt>API:</dt>
    <dd> URL | METHOD | description </dd>
    <dd> /api/auth/register | post | ユーザー新規登録</dd>
    <dd> /api/auth/login | post | ユーザー認証</dd>
    <dd> /api/auth/update/<int: user_id> | put | ユーザー情報を変更</dd>
    <dd> /api/auth/delete/<int: user_id> | delete | ユーザー削除</dd>
    <dd> /api/scraping | get | スクレイピングを開始し、案件情報を最新の１ページから情報を取得・返す</dd>
    <dd> /api/scraping/all | get | スクレイピングを開始し、案件情報を全てのページから情報を取得・返す</dd>
    <dd> /api/scraping/<int: user_id> | get | ログインユーザーに紐づくDBに保存されている案件を取得する。</dd>
    <dd> /api/scraping/latest/<int: user_id> | get | ログインユーザーに紐づくDBに保存されている案件から、前回保存した案件のみ取得する。</dd>
    <dd> /api/scraping | post | スクレイピングした現在表示中の案件を、DBに保存する。</dd>
    <dd> /api/scraping/<int: product_id> | put | DBに保存されている案件情報を変更する。</dd>
    <dd> /api/scraping/<int: product_id> | delete | DBに保存されている案件情報を削除する。</dd>  
</dl>

uvicornワーカークラスでgunicornを使用しています。
$ gunicorn --log-level debug main:app --reload  
% --reload はdebug時は便利だが本番では推奨されない。
% gunicorn main:app -w 4 --bind "0.0.0.0:8000" -k uvicorn.workers.UvicornWorker --log-level debug    
    % gunicorn.conf.pyに記述することも出来るのでそちらの方が楽。