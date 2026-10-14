import streamlit as st

# 1. 페이지 기본 설정 (가장 먼저 호출되어야 함)
st.set_page_config(
    page_title="MBTI 단짝 포켓몬 찾기",
    page_icon="🔍",
    layout="centered"
)

# 2. 커스텀 CSS 적용 (크림/노란색 톤, 큰 글씨)
st.markdown("""
<style>
    /* 전체 배경색 (따뜻한 크림색) */
    .stApp {
        background-color: #FFF9E6;
    }
    
    /* 텍스트 기본 색상 및 크기 */
    html, body, [class*="css"]  {
        color: #4A3A31;
        font-family: 'Malgun Gothic', 'Apple SD Gothic Neo', sans-serif;
    }
    
    /* 메인 제목 스타일 */
    h1 {
        color: #F57F17 !important;
        text-align: center;
        font-size: 2.5rem !important;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
        padding-bottom: 20px;
    }
    
    /* 서브 제목 및 본문 글씨 크기 키우기 */
    h2, h3 {
        color: #E65100 !important;
    }
    p, li, .stSelectbox label {
        font-size: 1.2rem !important;
    }
    
    /* 버튼 스타일 변경 (따뜻한 노란색) */
    div.stButton > button {
        background-color: #FFB300;
        color: white;
        font-weight: bold;
        font-size: 1.5rem !important;
        padding: 15px 30px;
        border: none;
        border-radius: 30px;
        width: 100%;
        transition: all 0.3s;
    }
    div.stButton > button:hover {
        background-color: #FFA000;
        box-shadow: 0 4px 10px rgba(255, 179, 0, 0.4);
        color: white;
    }
    
    /* 결과 박스 디자인 */
    .result-box {
        background-color: #FFFFFF;
        padding: 30px;
        border-radius: 20px;
        border: 3px solid #FFE082;
        box-shadow: 0 8px 16px rgba(0,0,0,0.05);
        text-align: center;
        margin-top: 20px;
    }
    
    .poke-name {
        font-size: 2rem;
        font-weight: bold;
        color: #E65100;
        margin-bottom: 5px;
    }
    
    .poke-type {
        font-size: 1.1rem;
        color: #795548;
        background-color: #FFF3E0;
        padding: 5px 15px;
        border-radius: 20px;
        display: inline-block;
        margin-bottom: 20px;
    }
    
    .poke-desc {
        font-size: 1.3rem;
        line-height: 1.6;
        color: #5D4037;
        margin-top: 15px;
        text-align: left;
        background: #FFF8E1;
        padding: 20px;
        border-radius: 15px;
        word-break: keep-all;
    }
</style>
""", unsafe_allow_html=True)

# 3. 포켓몬 데이터베이스 (인터넷 공식 아트워크 이미지 URL 사용)
# 이미지 출처: PokeAPI Github (안정적인 링크)
pokemon_data = {
    "ISTJ": {
        "name": "거북왕", "eng": "Blastoise", "type": "💧 물",
        "img": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/9.png",
        "trait": "성실함, 듬직함, 책임감",
        "reason": "항상 묵묵하게 자신의 역할을 다하는 거북왕처럼, 당신은 규칙을 잘 지키고 책임감이 강해 모두가 믿고 의지할 수 있는 든든한 방패 같은 사람입니다."
    },
    "ISFJ": {
        "name": "해피너스", "eng": "Blissey", "type": "🥚 노말",
        "img": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/242.png",
        "trait": "다정함, 헌신적, 따뜻함",
        "reason": "따뜻한 마음으로 상처입은 포켓몬을 치유하는 해피너스처럼, 당신은 타인을 배려하고 챙겨주는 것을 좋아하는 다정다감한 성격의 소유자입니다."
    },
    "INFJ": {
        "name": "루카리오", "eng": "Lucario", "type": "🥊 격투 / ⚙️ 강철",
        "img": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/448.png",
        "trait": "통찰력, 신념, 차분함",
        "reason": "상대의 파동을 읽어내는 루카리오처럼, 당신은 사람들의 속마음을 잘 이해하는 깊은 통찰력과 이상을 향해 나아가는 굳은 신념을 가졌습니다."
    },
    "INTJ": {
        "name": "뮤츠", "eng": "Mewtwo", "type": "🔮 에스퍼",
        "img": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/150.png",
        "trait": "완벽주의, 지능적, 독립적",
        "reason": "뛰어난 지능으로 상황을 주도하는 뮤츠처럼, 당신은 독립적이고 분석력이 뛰어나며 목표를 향해 전략적으로 움직이는 완벽주의자입니다."
    },
    "ISTP": {
        "name": "핫삼", "eng": "Scizor", "type": "🐞 벌레 / ⚙️ 강철",
        "img": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/212.png",
        "trait": "냉철함, 순발력, 실용주의",
        "reason": "필요할 때 날렵하게 움직이는 핫삼처럼, 당신은 평소엔 조용하지만 위기 상황에서 뛰어난 순발력과 냉철한 판단력으로 문제를 해결합니다."
    },
    "ISFP": {
        "name": "잠만보", "eng": "Snorlax", "type": "💤 노말",
        "img": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/143.png",
        "trait": "여유로움, 평화주의, 느긋함",
        "reason": "먹고 자는 것을 가장 좋아하는 잠만보처럼, 당신은 다투는 것을 싫어하고 현재의 평화롭고 여유로운 삶을 가장 중요하게 생각하는 긍정주의자입니다."
    },
    "INFP": {
        "name": "메타몽", "eng": "Ditto", "type": "🟣 노말",
        "img": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/132.png",
        "trait": "감수성, 유연함, 공감능력",
        "reason": "어떤 포켓몬으로도 변할 수 있는 메타몽처럼, 당신은 말랑말랑한 감수성으로 누구와도 잘 맞춰주며 타인의 감정에 깊이 공감할 줄 압니다."
    },
    "INTP": {
        "name": "야도란", "eng": "Slowbro", "type": "💧 물 / 🔮 에스퍼",
        "img": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/80.png",
        "trait": "호기심, 철학적, 마이웨이",
        "reason": "멍해 보이지만 속으로는 딴생각을 하고 있는 야도란처럼, 당신은 지적 호기심이 많고 자신만의 확고하고 깊은 내면 세계를 가진 철학자입니다."
    },
    "ESTP": {
        "name": "피카츄", "eng": "Pikachu", "type": "⚡ 전기",
        "img": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/25.png",
        "trait": "에너지, 활동적, 스타성",
        "img_offset": True,
        "reason": "어디서든 톡톡 튀고 주목받는 피카츄처럼, 당신은 넘치는 에너지와 타고난 스타성으로 주변을 즐겁게 만들며 현재를 만끽하는 행동파입니다."
    },
    "ESFP": {
        "name": "푸린", "eng": "Jigglypuff", "type": "🎤 노말 / 🧚 페어리",
        "img": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/39.png",
        "trait": "사교적, 긍정적, 분위기메이커",
        "reason": "노래 부르기를 좋아해 사람들의 이목을 끄는 푸린처럼, 당신은 긍정적이고 사교적이라 어디서든 사람들을 웃게 만드는 최고의 분위기 메이커입니다."
    },
    "ENFP": {
        "name": "토게피", "eng": "Togepi", "type": "🐣 페어리",
        "img": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/175.png",
        "trait": "순수함, 호기심, 해피바이러스",
        "reason": "순수하고 호기심 가득한 눈으로 세상을 보는 토게피처럼, 당신은 풍부한 상상력과 열정으로 매일매일을 즐거운 모험으로 만드는 해피 바이러스입니다."
    },
    "ENTP": {
        "name": "팬텀", "eng": "Gengar", "type": "👻 고스트 / ☠️ 독",
        "img": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/94.png",
        "trait": "장난기, 번뜩이는 아이디어, 유쾌함",
        "reason": "장난치기를 좋아하는 예측불허의 팬텀처럼, 당신은 두뇌 회전이 빠르고 기발한 아이디어가 넘치며 틀에 갇히지 않는 유쾌한 매력의 소유자입니다."
    },
    "ESTJ": {
        "name": "리자몽", "eng": "Charizard", "type": "🔥 불꽃 / 🦅 비행",
        "img": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/6.png",
        "trait": "리더십, 열정, 체계적",
        "reason": "강력한 불꽃으로 무리를 이끄는 리자몽처럼, 당신은 뜨거운 열정과 뛰어난 추진력으로 목표를 향해 흔들림 없이 돌진하는 타고난 지휘관입니다."
    },
    "ESFJ": {
        "name": "이상해씨", "eng": "Bulbasaur", "type": "🌿 풀 / ☠️ 독",
        "img": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/1.png",
        "trait": "친절함, 싹싹함, 협동심",
        "reason": "무리를 챙기고 자연과 조화롭게 살아가는 이상해씨처럼, 당신은 친절하고 주변 사람들을 꼼꼼하게 챙길 줄 아는 다정한 마당발입니다."
    },
    "ENFJ": {
        "name": "망나뇽", "eng": "Dragonite", "type": "🐲 드래곤 / 🦅 비행",
        "img": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/149.png",
        "trait": "온화함, 수호자, 이타적",
        "reason": "바다에서 조난당한 사람을 구해주는 다정한 망나뇽처럼, 당신은 타인의 성장을 돕고 곤경에 처한 사람을 지나치지 못하는 따뜻한 리더입니다."
    },
    "ENTJ": {
        "name": "갸라도스", "eng": "Gyarados", "type": "🌊 물 / 🦅 비행",
        "img": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/130.png",
        "trait": "카리스마, 불굴의 의지, 결단력",
        "reason": "잉어킹에서 거대한 용으로 진화하는 갸라도스처럼, 당신은 압도적인 카리스마와 불굴의 의지로 역경을 이겨내고 큰 성과를 쟁취해냅니다."
    }
}

# 4. 화면 UI 구성
st.title("MBTI 단짝 포켓몬 찾기 🔍")
st.markdown("<p style='text-align: center; color: #795548;'>나의 MBTI 유형을 선택하고 나와 찰떡인 포켓몬을 만나보세요!</p>", unsafe_allow_html=True)

st.write("") # 여백

# MBTI 16가지 선택지
mbti_list = list(pokemon_data.keys())
selected_mbti = st.selectbox("당신의 MBTI는 무엇인가요?", mbti_list, index=0)

st.write("") # 여백

# 찾기 버튼
if st.button("내 단짝 포켓몬 찾기! 🚀"):
    # 버튼 누르면 풍선 축하 효과
    st.balloons()
    
    # 선택된 포켓몬 데이터 가져오기
    data = pokemon_data[selected_mbti]
    
    # 결과 화면 출력 (HTML/CSS 활용)
    st.markdown(f"""
    <div class="result-box">
        <h3 style="color: #795548 !important; margin-bottom: 20px;">🎉 {selected_mbti}인 당신과 어울리는 포켓몬은...</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # 이미지는 Streamlit 컬럼을 이용해 중앙 정렬
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image(data["img"], use_column_width=True)
        
    st.markdown(f"""
    <div class="result-box" style="margin-top: 0px; border-top: none; border-radius: 0 0 20px 20px;">
        <div class="poke-name">{data["name"]} <span style="font-size:1.2rem; color:#999;">({data["eng"]})</span></div>
        <div class="poke-type">{data["type"]}</div>
        
        <div class="poke-desc">
            <strong>✨ 특징:</strong> {data["trait"]}<br><br>
            <strong>💖 어울리는 이유:</strong><br>
            {data["reason"]}
        </div>
    </div>
    """, unsafe_allow_html=True)
