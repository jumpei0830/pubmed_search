# ターミナルにて      streamlit run /Users/jumpeikudo/Desktop/python/pubmed_search/app/search_app.py  

import streamlit as st
import requests
import xml.etree.ElementTree as et
import csv
import io


# タイトルとヘッダーの表示
st.title("PubMed検索アプリ")
st.header("ヒットした論文のアブストラクトテーブルを作成してくれます！")

markdown = """

**使い方：**    
systematic reviewなどをする際にpubmedなど複数のデータベースからヒットした論文でテーブルを作ることがあります。
いちいちwebサイトからコピペをするのはめんどくさいので、pythonでまとめて実行してもらいます。
  
**注意：**  
・　検索ボタンを押すと自動で保存までするので、ヒット数が多いと止まることがあります。  
・　検索語は AND や OR などで区切って作成してください。
"""
st.markdown(markdown)

# ユーザー入力の取得
query = st.text_input("検索したい単語を入力してください")

# 検索ボタンが押されたときの処理
if st.button("検索"):
    # 検索処理
    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    payload = {
        "db": "pubmed",
        "term": query,
        "usehistory": "y"
    }

    ret = requests.get(url, params=payload)
    xml = ret.text.encode("utf-8")
    root = et.fromstring(xml)

    # ヒット数を表示
    count = int(root.findtext(".//Count"))
    st.write("PubMed上で", query, "に一致する論文は ", count, "件ありました。")

    # 論文の情報を取得し、CSVファイルに書き込む
    st.write("処理中・・・")
    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
    payload = {
        "db": "pubmed",
        "query_key": root.findtext("QueryKey"),
        "WebEnv": root.findtext("WebEnv"),
        "retmode": "text",
        "rettype": "xml"
    }

    ret = requests.get(url, params=payload)
    root = et.fromstring(ret.content)

    # CSVファイルに書き込むデータを準備
    result_csv = io.StringIO()
    writer = csv.writer(result_csv)
    writer.writerow(["Title", "Year", "FirstAuthor", "Abstract"])

    for article in root.findall(".//PubmedArticle"):
        try:
            title = article.findtext(".//ArticleTitle") or ""
            year = article.findtext(".//PubDate/Year") or ""
            last_name = article.findtext(".//AuthorList/Author[1]/LastName") or ""
            fore_name = article.findtext(".//AuthorList/Author[1]/ForeName") or ""
            first_author = last_name + " " + fore_name
            abstract = ""
            for abstract_text in article.findall(".//AbstractText"):
                abstract += abstract_text.text.strip() + "\n"
            if not abstract:
                abstract = "No abstract available"
            writer.writerow([title, year, first_author, abstract])
        except:
            pass

    # ダウンロードボタンを表示
    st.download_button("DOWNLOAD", result_csv.getvalue().encode("utf-8"), "result_table.csv", "Click here to download")

    st.write("タイトルとアブストラクトをresult_table.csvファイルに書き込みました。上部のボタンからダウンロードすることができます。")

    
    
markdown2="""
備考：  
・DeepL翻訳やAI要約は有料のため未実装  
・ワードクラウドの作成はエラーのため未実装  
・full text articleの取得は著作権上実装不可（pdfからテキスト化と自然言語要約は実装可能）  

"""
st.markdown(markdown2)