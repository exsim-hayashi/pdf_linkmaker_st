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

    # 変更後のPDFをバイトデータとして取得
    output_bytes = io.BytesIO()
    doc.save(output_bytes)
    doc.close()
    output_bytes.seek(0)
    
    return output_bytes

def main():
    st.title("📎 PDF にリンクを埋め込むアプリ")

    # noindex 設定
    st.markdown(
        "<meta name='robots' content='noindex, nofollow'>",
        unsafe_allow_html=True
    )

    # プリセット座標
    presets = {
        "本店用": (242.70, 191.00, 266.30, 207.30, "https://ikken-s.com/idhomehontenone"),
        "小山店用": (242.77, 188.95, 266.07, 205.53, "https://ikken-s.com/idhomeoyama")
    }

    preset_choice = st.selectbox("📌 プリセットを選択", list(presets.keys()))
    x1_mm, y1_mm, x2_mm, y2_mm, preset_url = presets[preset_choice]

    # 入力フィールド
    url = st.text_input("🔗 リンク先URL", preset_url)
    st.write("📐 リンクエリア調整（単位：mm）")
    x1_mm = st.number_input("X1", min_value=0.0, value=x1_mm)
    y1_mm = st.number_input("Y1", min_value=0.0, value=y1_mm)
    x2_mm = st.number_input("X2", min_value=0.0, value=x2_mm)
    y2_mm = st.number_input("Y2", min_value=0.0, value=y2_mm)

    # アップロードフォーム
    with st.form("upload_form"):
        uploaded_file = st.file_uploader("📤 PDF をアップロード", type=["pdf"])
        submitted = st.form_submit_button("✅ PDFを読み込む")

    if submitted and uploaded_file:
        st.session_state["pdf_name"] = uploaded_file.name
        st.session_state["pdf_bytes"] = uploaded_file.read()
        st.success("PDF を読み込みました。リンク埋め込みの準備ができました。")

    # セッションにPDFがあればボタンを表示
    if "pdf_bytes" in st.session_state:
        if st.button("🔧 PDF にリンクを埋め込む"):
            output_pdf = add_link_to_pdf(
                st.session_state["pdf_bytes"],
                x1_mm, y1_mm, x2_mm, y2_mm, url
            )

            base_name, ext = os.path.splitext(st.session_state["pdf_name"])
            output_filename = f"{base_name}_リンク追加済{ext}"

            st.download_button(
                label="📥 加工済みPDFをダウンロード",
                data=output_pdf,
                file_name=output_filename,
                mime="application/pdf"
            )

if __name__ == "__main__":
    main()
