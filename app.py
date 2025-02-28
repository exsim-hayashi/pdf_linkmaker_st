import streamlit as st
import fitz  # PyMuPDF
import io

# mm → pt 変換関数
def mm_to_pt(mm):
    return mm * 2.83465

# PDF にリンクを追加する関数
def add_link_to_pdf(pdf_bytes, x1_mm, y1_mm, x2_mm, y2_mm, url):
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    page = doc[0]  # 1ページ目にリンクを追加

    # mm → pt に変換
    x1, y1, x2, y2 = [mm_to_pt(v) for v in [x1_mm, y1_mm, x2_mm, y2_mm]]
    rect = fitz.Rect(x1, y1, x2, y2)

    # URLリンクを追加
    page.insert_link({"kind": fitz.LINK_URI, "from": rect, "uri": url})

    # 変更後のPDFをバイトデータとして取得
    output_bytes = io.BytesIO()
    doc.save(output_bytes)
    doc.close()
    output_bytes.seek(0)
    
    return output_bytes

def main():

    # Streamlit UI
    st.title("📄 PDF にリンクを埋め込むアプリ")

    st.markdown(
        """
        <meta name="robots" content="noindex, nofollow">
        """,
        unsafe_allow_html=True
    )

    # PDF アップロード
    uploaded_file = st.file_uploader("PDFをアップロード", type="pdf")

    # ユーザー入力
    url = st.text_input("🔗 リンク先のURLを入力", "https://example.com")
    x1_mm = st.number_input("X1 (mm)", min_value=0.0, value=242.70)
    y1_mm = st.number_input("Y1 (mm)", min_value=0.0, value=191.00)
    x2_mm = st.number_input("X2 (mm)", min_value=0.0, value=266.30)
    y2_mm = st.number_input("Y2 (mm)", min_value=0.0, value=207.30)

    # リンク追加ボタン
    if uploaded_file and st.button("🔧 PDF にリンクを埋め込む"):
        pdf_bytes = uploaded_file.read()
        output_pdf = add_link_to_pdf(pdf_bytes, x1_mm, y1_mm, x2_mm, y2_mm, url)

        # ダウンロードボタン
        st.download_button(
            label="📥 加工済みPDFをダウンロード",
            data=output_pdf,
            file_name="output.pdf",
            mime="application/pdf"
        )

if __name__ == "__main__":
    main()