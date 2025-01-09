import streamlit as st
import random
from PIL import Image
import os
from anthropic import Anthropic
from config import CLAUDE_API_KEY, CARDS, ARRAYS

def get_array_description(array_type):
    array_layouts = {
        "單張牌": {
            "positions": ["單張牌"],
            "description": "最基本的牌陣，用於快速回答是/否問題或獲得簡單指引。"
        },
        "三張牌": {
            "positions": ["過去", "現在", "未來"],
            "description": "經典的三張牌陣，展示情況的發展脈絡。"
        },
        "五張牌": {
            "positions": ["過去", "現在", "問題關鍵", "建議", "可能結果"],
            "description": "深入分析問題的五張牌陣，提供更全面的視角和建議。"
        },
        "十字牌陣": {
            "positions": ["當前處境", "阻礙", "建議", "外在影響", "可能結果"],
            "description": "以十字形排列的五張牌陣，從多個角度分析問題。"
        }
    }
    return array_layouts.get(array_type, {
        "positions": ["位置"],
        "description": "未知牌陣"
    })


def initialize_session():
    if 'selected_cards' not in st.session_state:
        st.session_state.selected_cards = []
    if 'interpretation' not in st.session_state:
        st.session_state.interpretation = None

def load_card_image(card_number):
    try:
        image_path = f"images/{CARDS[card_number]['file']}"
        return Image.open(image_path)
    except:
        st.error(f"無法載入卡牌圖片：{card_number}")
        return None

def get_interpretation(question, cards, array_type):
    client = Anthropic(api_key=CLAUDE_API_KEY)
    
    array_info = get_array_description(array_type)
    positions = array_info["positions"]
    
    prompt = f"""
    請以專業塔羅占卜師的角度，解讀以下雷諾曼牌陣：
    
    問題：{question}
    牌陣：{array_type}
    
    抽到的牌：
    """
    
    for card, position in zip(cards, positions):
        prompt += f"\n{position}位置：{CARDS[card]['name']}"
    
    response = client.messages.create(
        model="claude-3-sonnet-20240229",
        messages=[{"role": "user", "content": prompt}]
    )
    
    return response.content

def main():
    st.set_page_config(page_title="雷諾曼占卜", page_icon="🔮", layout="wide")
    initialize_session()
    
    st.title("🔮 雷諾曼占卜系統")
    
    # 選擇牌陣
    array_type = st.selectbox(
        "請選擇牌陣",
        list(ARRAYS.keys())
    )
    
    # 顯示牌陣說明
    array_info = get_array_description(array_type)
    st.write(array_info["description"])
    
    # 輸入問題
    question = st.text_input("請輸入您的問題：")
    
    if st.button("抽牌"):
        if question:
            # 抽牌
            num_cards = ARRAYS[array_type]
            st.session_state.selected_cards = random.sample(
                list(CARDS.keys()), num_cards
            )
            
            # 顯示牌陣
            cols = st.columns(num_cards)
            for idx, (card, col) in enumerate(
                zip(st.session_state.selected_cards, cols)
            ):
                with col:
                    st.image(
                        load_card_image(card),
                        caption=f"{array_info['positions'][idx]}: {CARDS[card]['name']}"
                    )
            
            # 取得解讀
            with st.spinner("正在解讀牌意..."):
                st.session_state.interpretation = get_interpretation(
                    question,
                    st.session_state.selected_cards,
                    array_type
                )
            
            # 顯示解讀結果
            st.write("### 解讀結果")
            st.write(st.session_state.interpretation)
        else:
            st.warning("請先輸入問題")

if __name__ == "__main__":
    main()
