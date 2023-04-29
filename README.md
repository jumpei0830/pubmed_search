# Systematic reviewを自動化しようプロジェクト

＜はじめに＞   
非プログラマーでpython初学者が「systematic reviewを自動化してみよう」というコンセプトのもと、chatGPTの力を借りながら開発しています。
目標としては「非プログラマーでも簡単に使える」、「python初学者でも理解しやすい」ものを目指しているのでwebアプリを作成しています。
本格的なsystematic reviewやmeta-analysisはプロトコルが厳格なので論文化は無理ですが、ふと思いついた研究疑問の検索ツールとして活用していただけたらと思います。

＜開発環境＞  
・言語：python3.11(3.10でも可).  
・統合環境： microsoft visual studio code.  
・webアプリ: streamlit.    
・OS: macOS Ventura 13.0 (macbookpro 2021, 14inchi).    

＜プロセス＞　※論文にするには現状圧倒的に信頼性の低い方法です. 
1. 任意に設定した検索式でpubmedからヒットした論文のアブストラクトテーブルを作る　(search_app.py).   
URL: https://jumpei0830-pubmed-search-search-app-3db7f3.streamlit.app/        
2. タイトルやアブストラクトの内容から一次スクリーニングをして組み入れ論文を選択する　(検討中)
3. 組み入れ論文を熟読し、内容を要約する　（pdf_summary_app.py）.   
URL: https://jumpei0830-pubmed-search-pdf-summary-app-orqhm0.streamlit.app/     

１、３について自動化ができました。2は精度が低いのと、著作権上全文入手が自動では出来ません。



＜メモ＞.   
・local vscode上で作成し、streamlit runで動作確認したのち、githubにアップロード、streamlitにデプロイ.   
・streamlitがpython3.10までのため今後の作成はpython3.10にて作成予定(pipが3.10、pip3が3.11に注意).   
・requirements.txtで必要なパッケージとバージョンの記述、pip freezeからコピペ？pip -Vで確認    
・
