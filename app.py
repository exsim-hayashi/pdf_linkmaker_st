import streamlit as st
import fitz  # PyMuPDF
import io
import os

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

    output_bytes = io.BytesIO()
    doc.save(output_bytes)
    doc.close()
    output_bytes.seek(0)
    
    return output_bytes

def main():
    st.set_page_config(page_title="PDFにリンクを埋め込む", layout="centered")

    st.title("📎 PDF にリンクを埋め込むツール")

    # noindex 設定（SEO対策）
    st.markdown(
        """<meta name="robots" content="noindex, nofollow">""",
        unsafe_allow_html=True
    )

    # プリセットの設定
    presets = {
        "本店用": (242.70, 191.00, 266.30, 207.30, "https://ikken-s.com/idhomehontenone"),
        "小山店用": (242.77, 188.95, 266.07, 205.53, "https://ikken-s.com/idhomeoyama")
    }

    uploaded_file = st.file_uploader("📤 PDFをアップロード", type="pdf")

    if uploaded_file:
        # アップロード直後にファイルを読んでセッション保存
        pdf_bytes = uploaded_file.read()
        st.session_state["pdf_bytes"] = pdf_bytes
        st.session_state["filename"] = uploaded_file.name

    if "pdf_bytes" in st.session_state:
        preset_choice = st.selectbox("📌 プリセットを選択", list(presets.keys()))
        x1_mm, y1_mm, x2_mm, y2_mm, default_url = presets[preset_choice]

        url = st.text_input("🔗 リンク先のURL", default_url)

        st.write("**🔧 座標を調整（単位: mm）**")
        x1_mm = st.number_input("X1", value=x1_mm, key="x1")
        y1_mm = st.number_input("Y1", value=y1_mm, key="y1")
        x2_mm = st.number_input("X2", value=x2_mm, key="x2")
        y2_mm = st.number_input("Y2", value=y2_mm, key="y2")

        # リンク処理はすぐ実行、セッションが切れる前に済ませる
        output_pdf = add_link_to_pdf(st.session_state["pdf_bytes"], x1_mm, y1_mm, x2_mm, y2_mm, url)

        # ファイル名を変更
        base_name, ext = os.path.splitext(st.session_state["filename"])
        output_filename = f"{base_name}_リンク追加済{ext}"

        st.download_button(
            label="📥 加工済みPDFをダウンロード",
            data=output_pdf,
            file_name=output_filename,
            mime="application/pdf"
        )
    else:
        st.info("まず PDF をアップロードしてください。")

if __name__ == "__main__":
    main()
