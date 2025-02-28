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
    # Streamlit UI
    st.title("ID PDF にリンクを埋め込むアプリ")

    # noindex 設定
    st.markdown(
        """
        <meta name="robots" content="noindex, nofollow">
        """,
        unsafe_allow_html=True
    )

    # PDF アップロード
    uploaded_file = st.file_uploader("📤 **PDFをアップロード**", type="pdf")

    # プリセット座標の選択
    presets = {
        "本店用": (242.70, 191.00, 266.30, 207.30, "https://ikken-s.com/idhomehontenone"),
        "小山店用": (242.77, 188.95, 266.07, 205.53, "https://ikken-s.com/idhomeoyama")
    }
    
    preset_choice = st.selectbox("📌 **プリセットを選択**", list(presets.keys()))

    # ユーザー入力（プリセットを選択したら値を更新）
    x1_mm, y1_mm, x2_mm, y2_mm, preset_url = presets[preset_choice]

    url = st.text_input("🔗 **リンク先のURLを入力**", preset_url)
    
    st.write("**調整用オプション**")
    
    x1_mm = st.number_input("X1 (mm)", min_value=0.0, value=x1_mm)
    y1_mm = st.number_input("Y1 (mm)", min_value=0.0, value=y1_mm)
    x2_mm = st.number_input("X2 (mm)", min_value=0.0, value=x2_mm)
    y2_mm = st.number_input("Y2 (mm)", min_value=0.0, value=y2_mm)

    # リンク追加ボタン
    if uploaded_file and st.button("🔧 PDF にリンクを埋め込む"):
        pdf_bytes = uploaded_file.read()
        output_pdf = add_link_to_pdf(pdf_bytes, x1_mm, y1_mm, x2_mm, y2_mm, url)

        # 元のファイル名を取得し、「_リンク追加済」を追加
        original_filename = uploaded_file.name  # 元のファイル名
        base_name, ext = os.path.splitext(original_filename)  # 拡張子分離
        output_filename = f"{base_name}_リンク追加済{ext}"  # 新しいファイル名

        # ダウンロードボタン
        st.download_button(
            label="📥 加工済みPDFをダウンロード",
            data=output_pdf,
            file_name=output_filename,
            mime="application/pdf"
        )

if __name__ == "__main__":
    main()
