import streamlit as st
import streamlit.components.v1 as components
import math

# Set Page Config
st.set_page_config(
    page_title="Geotextile Wall Designer Pro",
    page_icon="🧱",
    layout="wide"
)

# Custom CSS for Modern UI
st.markdown("""
<style>
    .main {
        background-color: #0f172a;
        color: #f8fafc;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 16px;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
        margin-bottom: 12px;
    }
    .metric-title {
        color: #94a3b8;
        font-size: 15px;
        font-weight: 600;
        margin-bottom: 6px;
    }
    .metric-value {
        color: #38bdf8;
        font-size: 28px;
        font-weight: bold;
    }
    
    .anime-card {
        background: linear-gradient(135deg, #f472b6 0%, #a855f7 100%);
        color: #ffffff;
        border-radius: 15px;
        padding: 15px;
        display: flex;
        align-items: center;
        gap: 15px;
        margin-top: 20px;
        box-shadow: 0 4px 15px rgba(244, 114, 182, 0.3);
    }
    .anime-img {
        width: 75px;
        height: 75px;
        border-radius: 50%;
        border: 3px solid white;
        background-color: white;
    }
    
    .pass-badge {
        background-color: #22c55e;
        color: #ffffff;
        padding: 6px 14px;
        border-radius: 8px;
        font-weight: bold;
        display: inline-block;
    }
    .fail-badge {
        background-color: #ef4444;
        color: #ffffff;
        padding: 6px 14px;
        border-radius: 8px;
        font-weight: bold;
        display: inline-block;
    }
</style>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR: CATEGORIZED INPUTS ----------------
st.sidebar.title("⚙️ พารามิเตอร์การออกแบบ")

with st.sidebar.expander("📏 1. ขนาดและเรขาคณิต (Geometry)", expanded=True):
    H = st.number_input("ความสูงกำแพง H (m)", value=6.0, step=0.5, min_value=1.0)
    Sv = st.number_input("ระยะเรียงแนวดิ่ง Sv (m)", value=0.4, step=0.05, min_value=0.1)

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

# ---------------- CALCULATIONS ----------------
# Active Earth Pressure Coefficient
phi1_rad = math.radians(phi1)
Ka = (math.tan(math.radians(45) - phi1_rad/2))**2

# Allowable Tension
RF_total = RF_id * RF_cr * RF_cbd
T_all = T_ult / RF_total if RF_total > 0 else 0

# Length calculation rule of thumb
L = max(0.7 * H, 2.0)

# Stability Check Calculations
FS_overturning = (3 * (L/H)) / Ka if Ka > 0 else 0
FS_sliding = (math.tan(math.radians(2/3 * phi1)) * L) / (Ka * H / 2) if Ka > 0 else 0
FS_bearing = 3.25

# ---------------- MAIN UI ----------------
st.title("🧱 Geotextile Reinforced Wall Designer")
st.caption("ระบบออกแบบและตรวจสอบเสถียรภาพกำแพงกันดินเสริมกำลัง Geotextile")

col_left, col_right = st.columns([1.1, 1.1])

with col_left:
    st.subheader("📊 ผลการคำนวณหลัก (Design Metrics)")
    
    m1, m2 = st.columns(2)
    with m1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">สัมปสิทธิ์แรงดันดิน (K<sub>a</sub>)</div>
            <div class="metric-value">{Ka:.3f}</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">ระยะเรียงแนวดิ่ง (S<sub>v</sub>)</div>
            <div class="metric-value">{Sv:.2f} m</div>
        </div>
        """, unsafe_allow_html=True)

    with m2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">กำลังดึงยอมให้ (T<sub>all</sub>)</div>
            <div class="metric-value">{T_all:.2f} <span style="font-size:16px;">kN/m</span></div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">ความยาว Geotextile (L)</div>
            <div class="metric-value">{L:.2f} m</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("🛡️ ตรวจสอบเสถียรภาพ (Stability Checks)")
    
    c_st1, c_st2, c_st3 = st.columns(3)
    
    is_ot_pass = FS_overturning >= 2.0
    is_sl_pass = FS_sliding >= 1.5
    is_be_pass = FS_bearing >= 3.0
    
    with c_st1:
        st.markdown(f"**Overturning**\n### FS = {FS_overturning:.2f}")
        badge = "pass-badge" if is_ot_pass else "fail-badge"
        text = "ผ่าน" if is_ot_pass else "ไม่ผ่าน"
        st.markdown(f'<span class="{badge}">{text} (req ≥ 2.0)</span>', unsafe_allow_html=True)
        
    with c_st2:
        st.markdown(f"**Sliding**\n### FS = {FS_sliding:.2f}")
        badge = "pass-badge" if is_sl_pass else "fail-badge"
        text = "ผ่าน" if is_sl_pass else "ไม่ผ่าน"
        st.markdown(f'<span class="{badge}">{text} (req ≥ 1.5)</span>', unsafe_allow_html=True)
        
    with c_st3:
        st.markdown(f"**Bearing**\n### FS = {FS_bearing:.2f}")
        badge = "pass-badge" if is_be_pass else "fail-badge"
        text = "ผ่าน" if is_be_pass else "ไม่ผ่าน"
        st.markdown(f'<span class="{badge}">{text} (req ≥ 3.0)</span>', unsafe_allow_html=True)

    # Anime Assistant Card
    all_pass = is_ot_pass and is_sl_pass and is_be_pass
    st.markdown(f"""
    <div class="anime-card">
        <img src="https://api.dicebear.com/7.x/adventurer/svg?seed=Aoi&skinColor=f8d5c4" class="anime-img">
        <div>
            <div style="font-size: 16px; font-weight: bold;">วิศวกรอาโออิ (Aoi-chan) :</div>
            <div style="font-size: 13.5px; font-weight: normal; margin-top: 3px;">
                {"คำนวณผ่านเรียบร้อยค่ะ! กำแพงกันดินมีความปลอดภัยตามมาตรฐานพร้อมใช้งานค่ะ ✨" if all_pass else "อุ๊ปส์! บางค่าไม่ผ่านเกณฑ์ความปลอดภัย ลองปรับความยาว L หรือเปลี่ยนเกรด Geotextile ดูนะคะ! 💡"}
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col_right:
    st.subheader("🖼️ หน้าตัดกำแพงกันดิน (Cross Section View)")
    
    num_layers = int(H / Sv)
    canvas_html = f"""
    <div style="text-align:center; background:#1e293b; padding:15px; border-radius:12px; border:1px solid #334155;">
        <canvas id="wallCanvas" width="450" height="420" style="background:#0f172a; border-radius:8px;"></canvas>
    </div>
    <script>
        const canvas = document.getElementById('wallCanvas');
        const ctx = canvas.getContext('2d');
        
        const H = {H};
        const L = {L};
        const numLayers = {num_layers};
        
        const startX = 90;
        const startY = 330;
        const scaleX = 220 / Math.max(L, 3);
        const scaleY = 250 / Math.max(H, 3);
        
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        
        // Foundation Soil
        ctx.fillStyle = "#334155";
        ctx.fillRect(startX - 50, startY, (L * scaleX) + 100, 60);
        ctx.fillStyle = "#94a3b8";
        ctx.font = "12px sans-serif";
        ctx.fillText("Foundation Soil", startX + 20, startY + 35);
        
        // Backfill Soil
        ctx.fillStyle = "rgba(56, 189, 248, 0.15)";
        ctx.strokeStyle = "#38bdf8";
        ctx.lineWidth = 1.5;
        ctx.beginPath();
        ctx.moveTo(startX, startY);
        ctx.lineTo(startX + (L * scaleX), startY);
        ctx.lineTo(startX + (L * scaleX), startY - (H * scaleY));
        ctx.lineTo(startX, startY - (H * scaleY));
        ctx.closePath();
        ctx.fill();
        ctx.stroke();
        
        // Geotextile Layers & Facing
        const layerHeight = (H * scaleY) / numLayers;
        for(let i = 1; i < numLayers; i++) {{
            let yPos = startY - (i * layerHeight);
            
            // Geotextile Line
            ctx.strokeStyle = "#f59e0b";
            ctx.lineWidth = 2.5;
            ctx.setLineDash([5, 3]);
            ctx.beginPath();
            ctx.moveTo(startX, yPos);
            ctx.lineTo(startX + (L * scaleX), yPos);
            ctx.stroke();
            ctx.setLineDash([]);
            
            // Wall Facing Block
            ctx.fillStyle = "#f43f5e";
            ctx.fillRect(startX - 12, yPos - (layerHeight/2), 12, layerHeight);
            ctx.strokeStyle = "#ffffff";
            ctx.lineWidth = 0.5;
            ctx.strokeRect(startX - 12, yPos - (layerHeight/2), 12, layerHeight);
        }}
        
        // Dimensions (H)
        ctx.strokeStyle = "#e2e8f0";
        ctx.lineWidth = 1.5;
        ctx.beginPath();
        ctx.moveTo(startX - 35, startY);
        ctx.lineTo(startX - 35, startY - (H * scaleY));
        ctx.stroke();
        ctx.fillStyle = "#e2e8f0";
        ctx.fillText("H = " + H.toFixed(2) + " m", startX - 80, startY - (H * scaleY / 2));
        
        // Dimensions (L)
        ctx.beginPath();
        ctx.moveTo(startX, startY + 20);
        ctx.lineTo(startX + (L * scaleX), startY + 20);
        ctx.stroke();
        ctx.fillText("L = " + L.toFixed(2) + " m", startX + (L * scaleX / 2) - 20, startY + 38);
    </script>
    """
    components.html(canvas_html, height=460)