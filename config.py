import streamlit as st
import os
from dotenv import load_dotenv

# 設定頁面配置
st.set_page_config(
    page_title="雷諾曼占卜",
    page_icon="🔮",
    layout="wide"
)

# 載入環境變數
load_dotenv()

# 優先使用 Streamlit secrets，如果不存在則使用環境變數
try:
    CLAUDE_API_KEY = st.secrets["CLAUDE_API_KEY"]
except:
    CLAUDE_API_KEY = os.getenv("CLAUDE_API_KEY")

if not CLAUDE_API_KEY:
    st.error("未設定 CLAUDE_API_KEY")
    st.stop()

# 雷諾曼牌的設定
CARDS = {
    1: {"name": "騎士", "file": "1_rider.jpg", "keywords": "消息、拜訪、速度、年輕男子", 
        "meaning": "代表快速到來的消息或訪客，也可能暗示交通工具或年輕男性"},
    2: {"name": "三葉草", "file": "2_clover.jpg", "keywords": "幸運、機會、希望、小確幸",
        "meaning": "象徵短暫的好運和機會，提醒要把握當下的幸福"},
    # ... 其他卡牌設定 ...
}

# AI Prompt 模板
PROMPT_TEMPLATE = """You are an experienced Lenormand card reader. Your task is to interpret the Lenormand cards chosen by the user and explain their meanings. Here's how to proceed:

First, here's a dictionary of Lenormand card meanings:

<lenormand_meanings>
{lenormand_meanings}
</lenormand_meanings>

When interpreting the cards, follow these guidelines:
1. Each card has its own individual meaning, but they should also be interpreted in relation to each other.
2. The first card typically represents the subject or focus of the reading.
3. The second card modifies or adds context to the first card.
4. If there's a third card, it usually represents the outcome or additional information.

Present your interpretation in this order:
1. Brief introduction
2. Individual meaning of each card
3. Combined interpretation of the cards
4. Conclusion or summary

Your tone should be respectful, insightful, and encouraging. Avoid being overly negative or making absolute predictions. Instead, focus on providing guidance and potential interpretations.

Here are the cards chosen by the user:

<chosen_cards>
{chosen_cards}
</chosen_cards>

Provide your interpretation of these cards based on the meanings provided and the guidelines above. Write your complete response inside <interpretation> tags."""

def format_card_meanings():
    """格式化雷諾曼牌意義為字典格式"""
    meanings = {}
    for card_id, card_info in CARDS.items():
        meanings[card_info['name']] = card_info['meaning']
    return str(meanings)

def format_chosen_cards(selected_cards):
    """格式化選擇的卡牌資訊"""
    return ", ".join([CARDS[card_id]['name'] for card_id in selected_cards])

def get_ai_interpretation(selected_cards):
    """獲取 AI 解讀結果"""
    from anthropic import Anthropic

    # 準備 prompt
    lenormand_meanings = format_card_meanings()
    chosen_cards = format_chosen_cards(selected_cards)
    
    prompt = PROMPT_TEMPLATE.format(
        lenormand_meanings=lenormand_meanings,
        chosen_cards=chosen_cards
    )

    # 呼叫 Claude API
    anthropic = Anthropic(api_key=CLAUDE_API_KEY)
    response = anthropic.messages.create(
        model="claude-3-sonnet-20240229",
        max_tokens=1000,
        messages=[{
            "role": "user",
            "content": prompt
        }]
    )

    return response.content

def main():
    st.title("🔮 雷諾曼占卜系統")
    
    # 使用者選擇卡片
    selected_cards = st.multiselect(
        "請選擇 1-3 張卡牌",
        options=list(CARDS.keys()),
        format_func=lambda x: f"{x}. {CARDS[x]['name']}"
    )

    if len(selected_cards) > 0:
        # 顯示選擇的卡片
        cols = st.columns(len(selected_cards))
        for idx, card_id in enumerate(selected_cards):
            with cols[idx]:
                st.image(f"cards/{CARDS[card_id]['file']}")
                st.write(f"**{CARDS[card_id]['name']}**")
                st.write(CARDS[card_id]['keywords'])

        # 當選擇 1-3 張卡片時，顯示解讀按鈕
        if 1 <= len(selected_cards) <= 3:
            if st.button("解讀卡牌"):
                with st.spinner("正在解讀卡牌..."):
                    interpretation = get_ai_interpretation(selected_cards)
                    st.write("## 卡牌解讀")
                    st.write(interpretation)
        elif len(selected_cards) > 3:
            st.warning("請最多只選擇 3 張卡片")

if __name__ == "__main__":
    main()
