import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import streamlit.components.v1 as components

# ---------------------------------------------------------
# 1. 페이지 설정
# ---------------------------------------------------------
st.set_page_config(
    page_title="인천 3-Active 통합 성과 대시보드",
    page_icon="🗺️",
    layout="wide"
)

st.title("🗺️ 인천 3-Active 통합 성과 대시보드")
st.markdown("""
**Hub & Spoke 네트워크 활동성**과 그로 인한 **사회경제적 파급효과**를 종합적으로 분석합니다.
* **좌표 보정 완료**: 실제 시설 위치 기반 시각화
* **마우스 오버**: 지도 아이콘 위에 마우스를 올리면 상세 정보 확인 가능
""")

# ---------------------------------------------------------
# 2. 데이터 준비 (실제 좌표 반영)
# ---------------------------------------------------------
# (1) 거점 도서관 (Hub)
hubs_data = {
    '북구도서관': {'lat': 37.5066218, 'lon': 126.7230735, 'status': 'Hub', 'region': '부평권'},
    '부평도서관': {'lat': 37.4849744, 'lon': 126.7045964, 'status': 'Hub', 'region': '부평권'},
    '계양도서관': {'lat': 37.5459641, 'lon': 126.7301965, 'status': 'Hub', 'region': '계양권'},
    '서구도서관': {'lat': 37.4943306, 'lon': 126.6796541, 'status': 'Hub', 'region': '서구권'},
    '주안도서관': {'lat': 37.4554851, 'lon': 126.6927471, 'status': 'Hub', 'region': '미추홀권'},
    '중앙도서관': {'lat': 37.4556557, 'lon': 126.7025455, 'status': 'Hub', 'region': '남동권'},
    '연수도서관': {'lat': 37.4178463, 'lon': 126.6852658, 'status': 'Hub', 'region': '연수권'},
    '화도진도서관': {'lat': 37.4817612, 'lon': 126.6282561, 'status': 'Hub', 'region': '동구권'},
    '강화도서관': {'lat': 37.7488175, 'lon': 126.4831844, 'status': 'Cold Spot', 'region': '강화권'}
}
df_hubs = pd.DataFrame(hubs_data).T.reset_index().rename(columns={'index': 'name'})

# (2) 협력 서점 (Store)
bookstores_data = [
    {'name': '더북스', 'lat': 37.4897746, 'lon': 126.7233082, 'hub': '부평도서관'},
    {'name': '낮잠과바람', 'lat': 37.5086005, 'lon': 126.7278369, 'hub': '북구도서관'},
    {'name': '책방산책', 'lat': 37.5404568, 'lon': 126.7190295, 'hub': '계양도서관'},
    {'name': '세종문고', 'lat': 37.4115479, 'lon': 126.6786156, 'hub': '연수도서관'},
    {'name': '열다책방', 'lat': 37.4066529, 'lon': 126.6714896, 'hub': '연수도서관'},
    {'name': '위즈덤스퀘어', 'lat': 37.4250000, 'lon': 126.6550000, 'hub': '중앙도서관'},
    {'name': '미래문고', 'lat': 37.4869218, 'lon': 126.7391518, 'hub': '서구도서관'},
    {'name': '서점안착', 'lat': 37.5349240, 'lon': 126.6515736, 'hub': '서구도서관'},
    {'name': '나비날다', 'lat': 37.4728064, 'lon': 126.6361411, 'hub': '화도진도서관'},
    {'name': '한미서점', 'lat': 37.4725453, 'lon': 126.6366690, 'hub': '주안도서관'},
    {'name': '나즌문턱', 'lat': 37.4723723, 'lon': 126.6373493, 'hub': '화도진도서관'}
]
np.random.seed(42)
for item in bookstores_data: item['traffic'] = np.random.randint(50, 300)
df_bookstores = pd.DataFrame(bookstores_data)

# (3) 참여 학교 (School)
schools_data = [
    {'name': '부평여고', 'lat': 37.5005587, 'lon': 126.7196623, 'hub': '북구도서관'},
    {'name': '부광중',   'lat': 37.5012607, 'lon': 126.7368838, 'hub': '북구도서관'},
    {'name': '부평동초', 'lat': 37.4996601, 'lon': 126.7237400, 'hub': '부평도서관'},
    {'name': '부평고',   'lat': 37.5022465, 'lon': 126.7275792, 'hub': '부평도서관'},
    {'name': '계산고',   'lat': 37.5469338, 'lon': 126.7296607, 'hub': '계양도서관'},
    {'name': '작전중',   'lat': 37.5333644, 'lon': 126.7295462, 'hub': '계양도서관'},
    {'name': '가좌고',   'lat': 37.4894556, 'lon': 126.6808340, 'hub': '서구도서관'},
    {'name': '가림고',   'lat': 37.4928274, 'lon': 126.6812112, 'hub': '서구도서관'},
    {'name': '청라고',   'lat': 37.5369893, 'lon': 126.6607886, 'hub': '서구도서관'},
    {'name': '구월중',   'lat': 37.4553432, 'lon': 126.7092909, 'hub': '중앙도서관'},
    {'name': '석정여고', 'lat': 37.4686806, 'lon': 126.6946944, 'hub': '중앙도서관'},
    {'name': '인천여고', 'lat': 37.4222410, 'lon': 126.6896458, 'hub': '연수도서관'},
    {'name': '연수고',   'lat': 37.4114651, 'lon': 126.6798641, 'hub': '연수도서관'},
    {'name': '박문여고', 'lat': 37.3827092, 'lon': 126.6660388, 'hub': '연수도서관'},
    {'name': '학익고',   'lat': 37.4390469, 'lon': 126.6633655, 'hub': '주안도서관'},
    {'name': '주안남초', 'lat': 37.4502383, 'lon': 126.6854180, 'hub': '주안도서관'},
    {'name': '제물포고', 'lat': 37.4766308, 'lon': 126.6239769, 'hub': '화도진도서관'},
    {'name': '인일여고', 'lat': 37.4779465, 'lon': 126.6261618, 'hub': '화도진도서관'},
    {'name': '강화여고', 'lat': 37.7546656, 'lon': 126.4789540, 'hub': '강화도서관'},
    {'name': '갑룡초',   'lat': 37.7436611, 'lon': 126.5029419, 'hub': '강화도서관'}
]
for item in schools_data: item['traffic'] = np.random.randint(100, 500)
df_schools = pd.DataFrame(schools_data)

# 좌표 병합 (선 그리기용)
df_bookstores = pd.merge(df_bookstores, df_hubs[['name', 'lat', 'lon']], left_on='hub', right_on='name', suffixes=('', '_hub'))
df_schools = pd.merge(df_schools, df_hubs[['name', 'lat', 'lon']], left_on='hub', right_on='name', suffixes=('', '_hub'))

# ---------------------------------------------------------
# 3. 사이드바 컨트롤
# ---------------------------------------------------------
st.sidebar.header("🛠️ 필터 및 설정")

# 권역 필터
all_regions = sorted(df_hubs['region'].unique().tolist())
selected_regions = st.sidebar.multiselect(
    "📍 표시할 권역 선택",
    all_regions,
    default=all_regions
)

st.sidebar.markdown("---")
st.sidebar.subheader("표시 요소 (Toggle)")

# 도서관/학교/서점 모두 제어 가능하도록 설정
show_hubs = st.sidebar.checkbox("🏛️ 거점 도서관 (Hub)", value=True)
show_schools = st.sidebar.checkbox("🏫 참여 학교 (School)", value=True)
show_bookstores = st.sidebar.checkbox("📚 협력 서점 (Store)", value=True)

# 데이터 필터링
filtered_hubs = df_hubs[df_hubs['region'].isin(selected_regions)]
filtered_hubs_names = filtered_hubs['name'].tolist()

# 선택 여부에 따라 데이터프레임 조정
if not show_hubs:
    display_hubs = pd.DataFrame(columns=filtered_hubs.columns)
else:
    display_hubs = filtered_hubs

if show_schools:
    filtered_schools = df_schools[df_schools['hub'].isin(filtered_hubs_names)]
else:
    filtered_schools = pd.DataFrame(columns=df_schools.columns)

if show_bookstores:
    filtered_bookstores = df_bookstores[df_bookstores['hub'].isin(filtered_hubs_names)]
else:
    filtered_bookstores = pd.DataFrame(columns=df_bookstores.columns)

# ---------------------------------------------------------
# 4. 카카오맵 HTML 생성
# ---------------------------------------------------------
def generate_kakao_map_html(hubs, schools, bookstores):
    hubs_json = hubs.to_json(orient='records', force_ascii=False)
    schools_json = schools.to_json(orient='records', force_ascii=False)
    bookstores_json = bookstores.to_json(orient='records', force_ascii=False)
    
    KAKAO_KEY = "a355516d451bb52744d83c5763eb1560"

    html_code = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <style>
            html, body, #map {{ width: 100%; height: 100%; margin: 0; padding: 0; }}
            
            /* 아이콘 스타일 */
            .map-icon {{
                display: flex; justify-content: center; align-items: center;
                border-radius: 50%; background: white; cursor: pointer;
                transition: transform 0.2s;
            }}
            .map-icon:hover {{ transform: scale(1.3); z-index: 1000 !important; }}

            .hub-icon {{
                width: 40px; height: 40px; border: 2px solid #2ecc71; 
                box-shadow: 0 2px 5px rgba(0,0,0,0.3); font-size: 20px;
            }}
            .hub-cold {{ border-color: #e74c3c; }}

            .spoke-icon {{
                width: 26px; height: 26px; box-shadow: 0 1px 3px rgba(0,0,0,0.3); font-size: 15px;
            }}
            .school {{ border: 2px solid #3498db; }}
            .bookstore {{ border: 2px solid #f39c12; }}
            
            /* 라벨 스타일 */
            .label-static {{
                position: absolute; bottom: 45px; left: -50%; transform: translateX(25%);
                background: rgba(255,255,255,0.9); padding: 3px 6px; border-radius: 4px;
                border: 1px solid #999; font-size: 11px; font-weight: bold; white-space: nowrap;
                box-shadow: 0 1px 2px rgba(0,0,0,0.2);
            }}
        </style>
    </head>
    <body>
        <div id="map"></div>
        <script type="text/javascript" src="//dapi.kakao.com/v2/maps/sdk.js?appkey={KAKAO_KEY}"></script>
        <script>
            var hubs = {hubs_json};
            var schools = {schools_json};
            var bookstores = {bookstores_json};

            var container = document.getElementById('map');
            var options = {{ center: new kakao.maps.LatLng(37.50, 126.70), level: 9 }};
            var map = new kakao.maps.Map(container, options);
            map.addControl(new kakao.maps.ZoomControl(), kakao.maps.ControlPosition.RIGHT);

            // 1. Hub 표시
            hubs.forEach(function(hub) {{
                var pos = new kakao.maps.LatLng(hub.lat, hub.lon);
                var isCold = hub.status === 'Cold Spot';
                var iconClass = isCold ? 'map-icon hub-icon hub-cold' : 'map-icon hub-icon';
                var color = isCold ? '#e74c3c' : '#2ecc71';
                
                // 마우스 오버 툴팁 (title 속성)
                var tooltip = hub.name + " (" + hub.status + ")\\n권역: " + hub.region;

                // 권역 원
                new kakao.maps.Circle({{
                    map: map, center: pos, radius: 1500, strokeWeight: 0,
                    fillColor: color, fillOpacity: 0.1
                }});

                // 아이콘 및 라벨
                var content = '<div class="' + iconClass + '" title="' + tooltip + '">🏛️</div>' + 
                              '<div class="label-static">' + hub.name + '</div>';

                new kakao.maps.CustomOverlay({{
                    map: map, position: pos, content: content, yAnchor: 0.5
                }});
            }});

            // 2. School 표시
            schools.forEach(function(item) {{
                var path = [new kakao.maps.LatLng(item.lat, item.lon), new kakao.maps.LatLng(item.lat_hub, item.lon_hub)];
                var weight = Math.max(1, item.traffic / 50);
                var tooltip = item.name + "\\n[학교]\\n연계 트래픽: " + item.traffic + "건\\nHub: " + item.hub;

                new kakao.maps.Polyline({{
                    map: map, path: path, strokeWeight: weight, strokeColor: '#3498db', strokeOpacity: 0.6
                }});

                var content = '<div class="map-icon spoke-icon school" title="' + tooltip + '">🏫</div>';
                new kakao.maps.CustomOverlay({{
                    map: map, position: new kakao.maps.LatLng(item.lat, item.lon),
                    content: content, yAnchor: 0.5
                }});
            }});

            // 3. Bookstore 표시
            bookstores.forEach(function(item) {{
                var path = [new kakao.maps.LatLng(item.lat, item.lon), new kakao.maps.LatLng(item.lat_hub, item.lon_hub)];
                var weight = Math.max(1, item.traffic / 40);
                var tooltip = item.name + "\\n[서점]\\n연계 트래픽: " + item.traffic + "건\\nHub: " + item.hub;

                new kakao.maps.Polyline({{
                    map: map, path: path, strokeWeight: weight, strokeColor: '#f39c12',
                    strokeOpacity: 0.8, strokeStyle: 'shortdash'
                }});

                var content = '<div class="map-icon spoke-icon bookstore" title="' + tooltip + '">📚</div>';
                new kakao.maps.CustomOverlay({{
                    map: map, position: new kakao.maps.LatLng(item.lat, item.lon),
                    content: content, yAnchor: 0.5
                }});
            }});
        </script>
    </body>
    </html>
    """
    return html_code

# ---------------------------------------------------------
# 5. 메인 레이아웃 (지도 & 분석)
# ---------------------------------------------------------
col_map, col_stat = st.columns([3, 2])

with col_map:
    st.subheader("① Hub & Spoke 네트워크 맵")
    map_html = generate_kakao_map_html(display_hubs, filtered_schools, filtered_bookstores)
    components.html(map_html, height=700)

with col_stat:
    st.subheader("② 통합 성과 지표 (KPI)")
    
    # [1] 활동성 지표 (Old)
    st.markdown("#### 🏃‍♂️ 네트워크 활동성")
    total_school = filtered_schools['traffic'].sum() if not filtered_schools.empty else 0
    total_store = filtered_bookstores['traffic'].sum() if not filtered_bookstores.empty else 0
    
    c1, c2 = st.columns(2)
    c1.metric("학교 연계 트래픽", f"{total_school:,}건")
    c2.metric("서점 연계 트래픽", f"{total_store:,}건")
    
    st.markdown("---")

    # [2] 사회경제적 파급효과 (New - 이미지 데이터 반영)
    st.markdown("#### 💰 사회경제적 파급효과 & 행복지수")
    
    m1, m2 = st.columns(2)
    m1.metric("😊 학생 긍정 정서", "78.4점", "▲ 12.0%")
    m2.metric("💳 서점 매출 기여", "12.5 억원", "지역경제 활성화")
    
    m3, m4 = st.columns(2)
    m3.metric("🏥 의료비 절감 추정", "4.8 억원", "건강증진 효과")
    m4.metric("🌲 탄소 배출 감축", "240 톤/년", "ESG 실천")

    st.markdown("---")

    # [3] 상세 분석 차트 (탭으로 구성)
    tab1, tab2, tab3 = st.tabs(["월별 지속성", "소비 패턴 변화", "걷기-독서 상관관계"])
    
    with tab1:
        # (Old) 월별 활동 지속성
        df_line = pd.DataFrame({
            '월': [f'{i}월' for i in range(1, 13)],
            '이벤트 참여': [100, 150, 300, 1200, 800, 200, 200, 300, 1500, 900, 200, 150],
            '자발적 습관': np.linspace(100, 900, 12) + np.random.randint(-50, 50, 12)
        }).melt(id_vars='월', var_name='유형', value_name='참여자수')
        
        fig_line = px.line(df_line, x='월', y='참여자수', color='유형', markers=True,
                           color_discrete_map={'이벤트 참여': 'gray', '자발적 습관': 'green'})
        fig_line.update_layout(height=250, margin=dict(l=10, r=10, t=30, b=10))
        st.plotly_chart(fig_line, use_container_width=True)

    with tab2:
        # (New) 문화 소비 패턴 변화
        st.caption("디지털 게임/오락 위주 소비에서 도서/공연/전시 등 건전한 여가 비용으로의 전환")
        df_spending = pd.DataFrame({
            'Category': ['디지털 게임/오락', '도서/공연/전시'],
            'Before': [70, 30],
            'After': [45, 55]
        }).melt(id_vars='Category', var_name='Period', value_name='Ratio')

        fig_bar = px.bar(df_spending, x='Ratio', y='Category', color='Period', orientation='h',
                         color_discrete_map={'Before': '#bdc3c7', 'After': '#2ecc71'},
                         barmode='group')
        fig_bar.update_layout(height=250, margin=dict(l=10, r=10, t=30, b=10))
        st.plotly_chart(fig_bar, use_container_width=True)

    with tab3:
        # (Old) 걷기-독서 상관관계
        df_scatter = pd.DataFrame({
            '주간 평균 걸음 수': np.random.randint(2000, 12000, 100),
            '독서 완독 점수': (np.random.randint(2000, 12000, 100) * 0.005) + np.random.randint(10, 30, 100)
        })
        fig_scatter = px.scatter(df_scatter, x='주간 평균 걸음 수', y='독서 완독 점수',
                                 opacity=0.6, title="신체 활동과 독서 성과의 연관성")
        fig_scatter.update_layout(height=250, margin=dict(l=10, r=10, t=30, b=10))
        st.plotly_chart(fig_scatter, use_container_width=True)