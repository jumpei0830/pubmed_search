import streamlit as st
import PyPDF4
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer
import io
import csv

##アップロードのフェーズ
st.header("１：論文をアップロードする")
# PDFファイルのアップロード
uploaded_files = st.file_uploader("PDFファイルをアップロードしてください", type="pdf", accept_multiple_files=True)

#個別要約のフェーズ
st.header("２：個々の論文を要約する")

num_sentences = st.selectbox(
        "要約する文の数を選択してください（参考:15で3000words程度）",
        list(range(1, 31)), # 1から30までの範囲を指定
        key = "num_sentences"
    )
all_texts = []  # 各PDFのテキストデータを保存するリスト
csv_data = []

for index, uploaded_file in enumerate(uploaded_files):
    # アップロードされたPDFファイルをテキスト化
    pdf_reader = PyPDF4.PdfFileReader(uploaded_file)
    num_pages = pdf_reader.numPages
    
    text = ""
    for page_number in range(num_pages):
        page = pdf_reader.pages[page_number]
        text += page.extractText()
        
    all_texts.append(text)  # テキストデータをリストに追加

    # テキスト化された結果を表示
    st.text_area(f"テキスト化結果 {index+1}", text)

    # 要約器を作成
    summarizer = LexRankSummarizer()

    # テキストを要約
    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    summary = summarizer(parser.document, num_sentences)

    # 要約結果を表示
    st.subheader(f"要約結果 {index+1}")
    for sentence in summary:
        st.write(sentence)

    # ファイル名を表示
    st.write(f"ファイル名: {uploaded_file.name}")

    # 要約結果をtxtファイルとしてダウンロード
    if st.button(f"要約結果のテキストをダウンロードする {index+1}"):
        summary_text = "\n".join(str(sentence) for sentence in summary)
        file = io.BytesIO(summary_text.encode("utf-8"))
        st.download_button(
            label=f"DOWNLOAD {uploaded_file.name}",
            data=file,
            file_name=f"summary_{index+1}_{uploaded_file.name}.txt",
            mime="text/plain",
        )
   #csv作成
    csv_header = ["filename", "summary"]
    csv_data.append([uploaded_file.name, "\n".join(str(sentence) for sentence in summary)])
    
# CSVファイルを作成してダウンロード
st.write("個別結果をまとめてcsvファイルとしてダウンロードする")
if st.button("DOWNLOAD CSV"):
    csv_file = io.StringIO()
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(csv_header)
    csv_writer.writerows(csv_data)
    st.download_button(
        label="DOWNLOAD",
        data=csv_file.getvalue(),
        file_name="summary_results.csv",
        mime="text/csv"
    )




##全体を要約するフェーズ
st.header("２：全体の要約をする")

total_num_sentences = st.selectbox(
        "要約する文の数を選択してください（参考:15で3000words程度）",
        list(range(1, 31)),  # 1から30までの範囲を指定
        key = "total_num_sentences"
    )
        
if st.button("全体の要約結果を表示する"):
    # 全てのテキストを結合
    all_text = "\n".join(all_texts)

    # 全体の要約を作成
    st.subheader("処理中・・・")
    total_parser = PlaintextParser.from_string(all_text, Tokenizer("english"))
    total_summarizer = LexRankSummarizer()
    total_summary = total_summarizer(total_parser.document, total_num_sentences)

    # 全体の要約結果を表示
    st.subheader("全体の要約結果")
    total_summary_text = "\n".join(str(sentence) for sentence in total_summary)
    st.write(total_summary_text)


    

