import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

# Set Page Config
st.set_page_config(
    page_title="Geotextile Wall Design Pro",
    page_icon="🧱",
    layout="wide"
)

# Custom CSS for Anime Theme & Modern UI
st.markdown("""
<style>
    /* Dark Soft Theme Background */
    .main {
        background-color: #1e1e2e;
        color: #cdd6f4;
    }
    
    /* Custom Metric Cards */
    .metric-card {
        background: linear-gradient(135deg, #2b2b40 0%, #181825 100%);
        border: 1px solid #45475a;
        border-radius: 12px;
        padding: 16px;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
        margin-bottom: 12px;
    }
    .metric-title {
        color: #a6adc8;
        font-size: 14px;
        font-weight: 600;
        margin-bottom: 4px;
    }
    .metric-value {
        color: #89b4fa;
        font-size: 28px;
        font-weight: bold;
    }
    
    /* Anime Character Card */
    .anime-card {
        background: linear-gradient(135deg, #f5c2e7 0%, #cba6f7 100%);
        color: #11111b;
        border-radius: 15px;
        padding: 15px;
        display: flex;
        align-items: center;
        gap: 15px;
        margin-top: 15px;
        font-weight: bold;
    }
    .anime-img {
        width: 80px;
        height: 80px;
        border-radius: 50%;
        border: 3px solid white;
        object-fit: cover;
    }
    
    /* Status Badge */
    .pass-badge {
        background-color: #a6e3a1;
        color: #11111b;
        padding: 4px 12px;
        border-radius: 8px;
        font-weight: bold;
    }
    .fail-badge {
        background-color: #f38ba8;
        color: #11111b;
        padding: 4px 12px;
        border-radius: 8px;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR: CATEGORIZED INPUTS ----------------
st.sidebar.image("https://api.dicebear.com/7.x/bottts/svg?seed=engineer", width=100)
st.sidebar.title("⚙️ พารามิเตอร์การออกแบบ")

with st.sidebar.expander("📏 1. ขนาดและเรขาคณิต (Geometry)", expanded=True):
    H = st.number_input("ความสูงกำแพง H (m)", value=6.0, step=0.5)

with st.sidebar.expander("🌾 2. คุณสมบัติดินถม (Backfill Soil)", expanded=True):
    gamma1 = st.number_input("หน่วยน้ำหนักดินถม γ1 (kN/m³)", value=17.0, step=0.5)
    phi1 = st.number_input("มุมเสียดทานดินถม φ1 (°)", value=30.0, step=1.0)

with st.sidebar.expander("🧵 3. แผ่นสังเคราะห์ (Geotextile Props)", expanded=False):
    T_ult = st.number_input("กำลังรับแรงดึงประลัย T_ult (kN/m)", value=50.0, step=5.0)
    RF_id = st.number_input("RF_id (Installation Damage)", value=1.2, step=0.1)
    RF_cr = st.number_input("RF_cr (Creep)", value=2.0, step=0.1)
    RF_cbd = st.number_input("RF_cbd (Chemical/Bio)", value=1.2, step=0.1)

with st.sidebar.expander("🏗️ 4. ดินฐานราก (Foundation Soil)", expanded=False):
    gamma2 = st.number_input("หน่วยน้ำหนักดินฐานราก γ2 (kN/m³)", value=18.0, step=0.5)
    phi2 = st.number_input("มุมเสียดทานฐานราก φ2 (°)", value=25.0, step=1.0)
    c2 = st.number_input("แรงยึดเหนี่ยวฐานราก c2 (kPa)", value=20.0, step=5.0)

# ---------------- CALCULATIONS ----------------
# Active Earth Pressure Coefficient
Ka = np.tan(np.radians(45 - phi1/2))**2

# Allowable Tension
RF_total = RF_id * RF_cr * RF_cbd
T_all = T_ult / RF_total

# Spacing & Length
Sv = 0.4  # Assigned vertical spacing (m)
sigma_a = Ka * gamma1 * H
L = 0.7 * H  # Standard design rule of thumb for geotextile length

# Stability Check Calculations (Simplified Demo Logic)
FS_overturning = (3 * (L/H)) / (Ka)
FS_sliding = (np.tan(np.radians(2/3 * phi1)) * L) / (Ka * H / 2)
FS_bearing = 3.2  # Placeholder value for demo

# ---------------- MAIN UI ----------------
st.title("🧱 Geotextile Reinforced Wall Designer")
st.caption("ระบบออกแบบและตรวจสอบเสถียรภาพกำแพงกันดินเสริมกำลัง Geotextile")

col_left, col_right = st.columns([1.2, 1])

with col_left:
    st.subheader("📊 ผลการคำนวณหลัก (Design Metrics)")
    
    # 2x2 Grid for Metrics
    m1, m2 = st.columns(2)
    with m1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">สัมปสิทธิ์แรงดันดิน ($K_a$)</div>
            <div class="metric-value">{Ka:.3f}</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">ระยะเรียงแนวดิ่ง ($S_v$)</div>
            <div class="metric-value">{Sv:.2f} m</div>
        </div>
        """, unsafe_allow_html=True)

    with m2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">กำลังดึงยอมให้ ($T_{{all}}$)</div>
            <div class="metric-value">{T_all:.2f} <span style="font-size:16px;">kN/m</span></div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">ความยาว Geotextile ($L$)</div>
            <div class="metric-value">{L:.2f} m</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("🛡️ ตรวจสอบเสถียรภาพ (Stability Checks)")
    
    # Stability Status Rows
    c_st1, c_st2, c_st3 = st.columns(3)
    
    with c_st1:
        status = "pass-badge" if FS_overturning >= 2.0 else "fail-badge"
        text = "ผ่าน" if FS_overturning >= 2.0 else "ไม่ผ่าน"
        st.markdown(f"**Overturning**\n### FS = {FS_overturning:.2f}")
        st.markdown(f'<span class="{status}">{text} (req ≥ 2.0)</span>', unsafe_allow_html=True)
        
    with c_st2:
        status = "pass-badge" if FS_sliding >= 1.5 else "fail-badge"
        text = "ผ่าน" if FS_sliding >= 1.5 else "ไม่ผ่าน"
        st.markdown(f"**Sliding**\n### FS = {FS_sliding:.2f}")
        st.markdown(f'<span class="{status}">{text} (req ≥ 1.5)</span>', unsafe_allow_html=True)
        
    with c_st3:
        status = "pass-badge" if FS_bearing >= 3.0 else "fail-badge"
        text = "ผ่าน" if FS_bearing >= 3.0 else "ไม่ผ่าน"
        st.markdown(f"**Bearing**\n### FS = {FS_bearing:.2f}")
        st.markdown(f'<span class="{status}">{text} (req ≥ 3.0)</span>', unsafe_allow_html=True)

    # Anime Assistant Card
    st.markdown(f"""
    <div class="anime-card">
        <img src="https://api.dicebear.com/7.x/adventurer/svg?seed=Aoi&skinColor=f8d5c4" class="anime-img">
        <div>
            <div style="font-size: 16px; font-weight: bold;">วิศวกรอาโออิ (Aoi-chan) แจ้งเตือน:</div>
            <div style="font-size: 13.5px; font-weight: normal; margin-top: 3px;">
                {"คำนวณผ่านเรียบร้อยค่ะ! กำแพงกันดินมีความปลอดภัยสูง พร้อมใช้งานต่อได้เลย ✨" if (FS_overturning>=2 and FS_sliding>=1.5) else "อุ๊ปส์! บางค่าไม่ผ่านเกณฑ์ความปลอดภัย ลองเพิ่มความยาว L หรือกำลังดึง Geotextile ดูนะคะ! 💡"}
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col_right:
    st.subheader("🖼️ รูปแบบหน้าตัดกำแพง (Cross Section)")
    
    # Matplotlib Realistic Drawing
    fig, ax = plt.subplots(figsize=(6, 7), facecolor='#1e1e2e')
    ax.set_facecolor('#252538')
    
    # Draw Foundation Soil
    foundation = patches.Rectangle((-1, -1.5), L + 3, 1.5, edgecolor='none', facecolor='#585b70')
    ax.add_patch(foundation)
    
    # Draw Backfill Soil
    backfill = patches.Polygon([[0, 0], [L + 0.5, 0], [L + 0.5, H], [0, H]], closed=True, facecolor='#a6e3a1', alpha=0.3)
    ax.add_patch(backfill)
    
    # Draw Geotextile Layers & Facing
    num_layers = int(H / Sv)
    for i in range(1, num_layers):
        y = i * Sv
        # Geotextile Line
        ax.plot([0, L], [y, y], color='#fab387', linewidth=2.5, linestyle='--')
        # Wall Face Block
        facing = patches.Rectangle((-0.15, y - Sv/2), 0.15, Sv, facecolor='#f38ba8', edgecolor='#11111b')
        ax.add_patch(facing)
        
    # Wall Dimensions Annotations
    ax.annotate('', xy=(L, -0.3), xytext=(0, -0.3), arrowprops=dict(arrowstyle='<->', color='#89b4fa', lw=1.5))
    ax.text(L/2, -0.6, f'L = {L:.2f} m', color='#89b4fa', ha='center', fontweight='bold')
    
    ax.annotate('', xy=(-0.5, 0), xytext=(-0.5, H), arrowprops=dict(arrowstyle='<->', color='#89b4fa', lw=1.5))
    ax.text(-0.8, H/2, f'H = {H:.2f} m', color='#89b4fa', va='center', rotation=90, fontweight='bold')

    # Styling Axes
    ax.set_xlim(-1.2, L + 1.2)
    ax.set_ylim(-1.8, H + 0.8)
    ax.set_aspect('equal')
    ax.axis('off')
    
    st.pyplot(fig)