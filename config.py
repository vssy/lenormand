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
    3: {"name": "船", "file": "3_ship.jpg", "keywords": "旅行、距離、貿易、移動",
        "meaning": "代表遠行、貿易往來，或是人生的新航向"},
    4: {"name": "房子", "file": "4_house.jpg", "keywords": "家庭、安全、不動產、穩定",
        "meaning": "象徵家庭、住所，也代表安全感和穩定性"},
    5: {"name": "樹", "file": "5_tree.jpg", "keywords": "健康、成長、家族、生命力",
        "meaning": "代表健康狀況、家族關係，也象徵生命力和個人成長"},
    6: {"name": "雲", "file": "6_clouds.jpg", "keywords": "困惑、不確定、混亂、轉變",
        "meaning": "暗示情況不明朗，可能有變數或需要做出抉擇"},
    7: {"name": "蛇", "file": "7_snake.jpg", "keywords": "智慧、誘惑、欺騙、成熟女性",
        "meaning": "代表智慧或警告，也可能暗示人際關係中的複雜情況"},
    8: {"name": "棺材", "file": "8_coffin.jpg", "keywords": "結束、轉變、失去、疾病",
        "meaning": "象徵某事物的結束或重大轉變，提醒需要放下"},
    9: {"name": "花束", "file": "9_bouquet.jpg", "keywords": "快樂、禮物、讚美、愛情",
        "meaning": "代表喜悅、讚美或禮物，在感情方面是好兆頭"},
    10: {"name": "鐮刀", "file": "10_scythe.jpg", "keywords": "突變、決定、危險、切斷",
         "meaning": "表示突如其來的改變或決定性的時刻"},
    11: {"name": "鞭子", "file": "11_whip.jpg", "keywords": "衝突、爭吵、重複、壓力",
         "meaning": "代表衝突、爭執或重複發生的問題"},
    12: {"name": "鳥", "file": "12_birds.jpg", "keywords": "交談、焦慮、八卦、消息",
         "meaning": "象徵溝通、談話，也可能暗示焦慮或謠言"},
    13: {"name": "孩子", "file": "13_child.jpg", "keywords": "新開始、純真、學習、小事",
         "meaning": "代表新的開始、純真或學習階段"},
    14: {"name": "狐狸", "file": "14_fox.jpg", "keywords": "狡猾、工作、謹慎、欺騙",
         "meaning": "提醒要謹慎行事，也可能與工作或商業相關"},
    15: {"name": "熊", "file": "15_bear.jpg", "keywords": "力量、權威、保護、財富",
         "meaning": "象徵權力、地位或財富，也代表保護者角色"},
    16: {"name": "星星", "file": "16_stars.jpg", "keywords": "希望、靈感、目標、方向",
         "meaning": "代表希望、理想和目標，指引方向"},
    17: {"name": "鸛鳥", "file": "17_stork.jpg", "keywords": "改變、懷孕、搬遷、進步",
         "meaning": "預示即將到來的改變或進步"},
    18: {"name": "狗", "file": "18_dog.jpg", "keywords": "忠誠、友情、保護、服務",
         "meaning": "象徵忠實的朋友或可靠的夥伴"},
    19: {"name": "塔", "file": "19_tower.jpg", "keywords": "權威、機構、孤立、高處",
         "meaning": "代表官方機構或權威，也可能暗示孤立感"},
    20: {"name": "花園", "file": "20_garden.jpg", "keywords": "社交、公眾、群體、展示",
         "meaning": "與社交活動、公眾場合或群體活動有關"},
    21: {"name": "山", "file": "21_mountain.jpg", "keywords": "障礙、挑戰、延遲、阻礙",
         "meaning": "表示需要克服的困難或障礙"},
    22: {"name": "十字路口", "file": "22_crossroads.jpg", "keywords": "選擇、決定、方向、機會",
         "meaning": "代表人生的重要抉擇或多個選項"},
    23: {"name": "老鼠", "file": "23_mice.jpg", "keywords": "損失、焦慮、偷竊、消耗",
         "meaning": "警告可能的損失或資源的消耗"},
    24: {"name": "心", "file": "24_heart.jpg", "keywords": "愛情、感情、喜愛、熱情",
         "meaning": "象徵愛情或深厚的情感連結"},
    25: {"name": "戒指", "file": "25_ring.jpg", "keywords": "承諾、循環、契約、關係",
         "meaning": "代表承諾、合約或重要的關係"},
    26: {"name": "書", "file": "26_book.jpg", "keywords": "知識、秘密、學習、研究",
         "meaning": "與學習、知識或秘密有關"},
    27: {"name": "信", "file": "27_letter.jpg", "keywords": "文件、通訊、消息、契約",
         "meaning": "代表重要的文件或通訊"},
    28: {"name": "男人", "file": "28_man.jpg", "keywords": "男性、丈夫、情人、求問者",
         "meaning": "代表重要的男性角色或求問者本人"},
    29: {"name": "女人", "file": "29_woman.jpg", "keywords": "女性、妻子、情人、求問者",
         "meaning": "代表重要的女性角色或求問者本人"},
    30: {"name": "百合", "file": "30_lily.jpg", "keywords": "純潔、和平、家庭、性",
         "meaning": "象徵純潔、和諧或家庭生活"},
    31: {"name": "太陽", "file": "31_sun.jpg", "keywords": "成功、快樂、活力、光明",
         "meaning": "代表成功、幸福和光明的前景"},
    32: {"name": "月亮", "file": "32_moon.jpg", "keywords": "情緒、直覺、名譽、認可",
         "meaning": "與情緒、直覺或社會認可有關"},
    33: {"name": "鑰匙", "file": "33_key.jpg", "keywords": "解答、發現、重要、成功",
         "meaning": "象徵重要的發現或解決方案"},
    34: {"name": "魚", "file": "34_fish.jpg", "keywords": "財富、豐盛、生意、流動",
         "meaning": "與財務、生意或資源流動有關"},
    35: {"name": "錨", "file": "35_anchor.jpg", "keywords": "穩定、安全、希望、目標",
         "meaning": "代表穩定性和長期目標"},
    36: {"name": "十字架", "file": "36_cross.jpg", "keywords": "命運、苦難、責任、信仰",
         "meaning": "象徵必經的考驗或重要的人生課題"}
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
