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
        <dd>現在取得・表示中のデータをPOSTメソッドで保存</dd>
        <dd>データの状態を更新(PUT)・削除(DELETE)できる。</dd>
        <dd>前回表示したデータを呼び出すことが出来る。(create_atより最新の日付のデータを呼び出せる。)</dd>
    </dl>
</dl>
<dl>
    <dt>API:</dt>
    <dd> URL | METHOD | description </dd>
    <dd> /api/register | post | </dd>
    <dd> /api/login | post | </dd>
    <dd> /api/update/<int: id> | put | </dd>
    <dd> /api/delete/<int: id> | delete | </dd>
    <dd> /api/scraping | get | </dd>
    <dd> /api/scraping/all | get | </dd>
    <dd> /api/scraping/<int: id> | get | </dd>
    <dd> /api/scraping/<int: id> | post | </dd>
    <dd> /api/scraping/<int: id> | put | </dd>
    <dd> /api/scraping/<int: id> | delete | </dd>  
</dl>

uvicornワーカークラスでgunicornを使用しています。
$ gunicorn --log-level debug main:app --reload  
% --reload はdebug時は便利だが本番では推奨されない。
% gunicorn main:app -w 4 --bind "0.0.0.0:8000" -k uvicorn.workers.UvicornWorker --log-level debug    
    % gunicorn.conf.pyに記述することも出来るのでそちらの方が楽。