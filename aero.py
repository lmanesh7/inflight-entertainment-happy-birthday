import streamlit as st
import pandas as pd
import random
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
import io

# --- 1. HELPER FUNCTION: Create Custom Card ---
@st.cache_data
def create_birthday_card(name):
    st.balloons()
    st.markdown("""
    <style>
    body {
        background: linear-gradient(135deg, #ff8fab, #ffc2d1);
        color: white;
        text-align: center;
    }
    .card-container {
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(12px);
        border-radius: 30px;
        padding: 50px;
        margin-top: 50px;
        width: 70%;
        margin-left: auto;
        margin-right: auto;
        box-shadow: 0 8px 25px rgba(0,0,0,0.2);
    }
    .title {
        font-family: 'Pacifico', cursive;
        font-size: 60px;
        margin-bottom: 10px;
    }
    .subtitle {
        font-size: 30px;
        font-weight: 300;
    }
    .message {
        margin-top: 30px;
        font-size: 22px;
        line-height: 1.7;
        font-weight: 400;
    }
    .footer {
        margin-top: 40px;
        font-size: 24px;
        font-weight: bold;
    }
    </style>

    <link href="https://fonts.googleapis.com/css2?family=Pacifico&display=swap" rel="stylesheet">
    """, unsafe_allow_html=True)

    # ---- Greeting Card UI ----
    st.markdown('<div class="card-container">', unsafe_allow_html=True)

    st.markdown('<div class="title">🎉 Happy Birthday, Sister! 🎉</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Wishing you a year filled with love, joy, and endless celebrations 💖</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="message">
    On this special day, I just want to remind you how truly wonderful you are.

    May your journey ahead be filled with magical moments, new adventures,  
    and everything beautiful that life has to offer.  
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="footer">With all my love, <br> Manesh ❤️</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
# --- 2. Page Config & State ---
st.set_page_config(page_title="Birthday Air", page_icon="🎂", layout="wide", initial_sidebar_state="collapsed")

if 'show_card' not in st.session_state: st.session_state.show_card = False
if 'passenger_name' not in st.session_state: st.session_state.passenger_name = "Keerthi"
if 'lat' not in st.session_state: st.session_state.lat = 39.0119
if 'lon' not in st.session_state: st.session_state.lon = -98.4842
if 'altitude' not in st.session_state: st.session_state.altitude = 36000
if 'speed' not in st.session_state: st.session_state.speed = 540

# --- 3. CSS Styling (Now supports Link Buttons) ---
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    div[data-testid="stMetricValue"] { color: #FFD700; font-family: monospace; }
    h1 { background: -webkit-linear-gradient(45deg, #FFD700, #FF69B4); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
    
    /* UNIFIED BUTTON STYLING (Standard & Link Buttons) */
    div.stButton > button, div.stLinkButton > a {
        width: 100%;
        border-radius: 8px;
        height: 3em;
        background-color: #1f2937;
        color: white;
        border: 1px solid #374151;
        display: flex;
        align-items: center;
        justify-content: center;
        text-decoration: none;
        font-weight: 500;
    }
    div.stButton > button:hover, div.stLinkButton > a:hover {
        background-color: #FFD700; /* Gold on hover */
        color: black;
        border-color: #FFD700;
    }
    </style>
    """, unsafe_allow_html=True)

# --- HEADER ---
c1, c2, c3, c4 = st.columns([2,1,1,1])
with c1: st.title("🎉 AIR BIRTHDAY")
with c2: st.caption("FLIGHT"); st.write("**BDAY-2025**")
with c3: st.caption("DESTINATION"); st.write("**PARTY**")
with c4: st.caption("LOCAL TIME"); st.write(datetime.now().strftime("%H:%M"))

st.markdown("---")
# --- INITIALIZE AUDIO STATE ---
# We define a playlist of real MP3s (Wikimedia/Royalty Free)
if 'playlist' not in st.session_state:
    st.session_state.playlist = [
        {"title": "Happy Birthday (Tune)", "artist": "The Party Crew", "url": "happy-birthday-357371.mp3"},
        {"title": "Happy Birthday (Classic)", "artist": "Saavane", "url": "happy-birthday-to-you.mp3"},
        {"title": "Happy Birthday (Guitar)", "artist": "Smoother", "url": "happy-birthday-guitar.mp3"},
        {"title": "Happy Birthday (Jazz)", "artist": "Funky Town", "url": "happy-birthday-jazz.mp3"},
    ]

if 'current_track_idx' not in st.session_state:
    st.session_state.current_track_idx = 0

# Helper function to change tracks
def change_track(direction):
    if direction == "next":
        st.session_state.current_track_idx = (st.session_state.current_track_idx + 1) % len(st.session_state.playlist)
    elif direction == "prev":
        st.session_state.current_track_idx = (st.session_state.current_track_idx - 1) % len(st.session_state.playlist)

# --- CSS FOR THE VISUALIZER ---
# This creates 5 bars that bounce up and down smoothly
visualizer_css = """
<style>
.visualizer-container {
    display: flex;
    align-items: flex-end;
    height: 60px;
    gap: 5px;
    margin-top: 20px;
    margin-bottom: 20px;
}
.bar {
    width: 100%;
    background-color: #FFD700;
    animation: bounce 1s infinite ease-in-out;
}
.bar:nth-child(1) { animation-duration: 0.8s; height: 30%; }
.bar:nth-child(2) { animation-duration: 1.2s; height: 80%; }
.bar:nth-child(3) { animation-duration: 0.5s; height: 50%; }
.bar:nth-child(4) { animation-duration: 1.0s; height: 90%; }
.bar:nth-child(5) { animation-duration: 0.7s; height: 40%; }

@keyframes bounce {
    0%, 100% { transform: scaleY(0.5); opacity: 0.7; }
    50% { transform: scaleY(1.2); opacity: 1; }
}
</style>
<div class="visualizer-container">
    <div class="bar"></div>
    <div class="bar"></div>
    <div class="bar"></div>
    <div class="bar"></div>
    <div class="bar"></div>
</div>
"""

# ================= MAIN LOGIC =================

# 1. CARD MODE
if st.session_state.show_card:
    #img_buffer = create_birthday_card(st.session_state.passenger_name)
    create_birthday_card(st.session_state.passenger_name)
    co1, co2, co3 = st.columns([1, 2, 1])
    with co2:
        # Close button to return to flight
        if st.button("❤️ Return to Flight Entertainment", use_container_width=True):
            st.session_state.show_card = False
            st.rerun()

# 2. FLIGHT MODE (Standard)
else:
    col_media, col_data = st.columns([2, 1])

    # LEFT: Media
    with col_media:
        st.toast(f"👨‍✈️ **Captain's Announcement:** Welcome aboard, {st.session_state.passenger_name}. We are currently cruising at {st.session_state.altitude:,} ft.")
        st.success("👨‍✈️ **Captain's Announcement:** Ladies and gentlemen, we have a VIP birthday passenger on board. Please prepare for celebration.")
        st.markdown("# Happy Birthday!")
        st.caption("Seat 1A • First Class • VIP Service")
        
        # Surprise Trigger
        if st.button("🎁 CLICK FOR SURPRISE MODE", use_container_width=True):
            st.session_state.show_card = True
            st.balloons()
            st.rerun()

        t1, t2 = st.tabs(["🎵 Party Song", "📸 Memories"])
        with t1:
            # Get current song data
            current_song = st.session_state.playlist[st.session_state.current_track_idx]
            
            # LAYOUT: Album Art (Left) | Controls (Right)
            r1_c1, r1_c2 = st.columns([1, 2], gap="medium")
            
            with r1_c1:
                # Dynamic Album Art based on track index (just changing colors/text for demo)
                art_url = f"https://placehold.co/300x300/1f2937/FFD700?text=Track+{st.session_state.current_track_idx + 1}"
                st.image(art_url, use_container_width=True)
                
            with r1_c2:
                st.subheader("Now Playing")
                st.markdown(f"### 🎵 {current_song['title']}")
                st.caption(f"Artist: {current_song['artist']}")
                
                # THE AUDIO PLAYER
                # Note: We use the URL as the 'key' so the player reloads when the song changes
                st.audio(current_song['url'], format="audio/ogg", autoplay=True)
                
                # CONTROL BUTTONS
                b1, b2, b3 = st.columns(3)
                with b1:
                    if st.button("⏮ Prev"):
                        change_track("prev")
                        st.rerun()
                with b2:
                    st.button("⏸ Pause")
                with b3:
                    if st.button("Next ⏭"):
                        change_track("next")
                        st.rerun()

            # VISUALIZER SECTION
            st.markdown("---")
            st.caption("Audio Spectrum (Live)")
            # Inject the CSS/HTML visualizer
            st.markdown(visualizer_css, unsafe_allow_html=True)
            
            # PLAYLIST / QUEUE SECTION
            with st.expander("View Queue / Add Songs", expanded=True):
                # 1. Show List
                for idx, song in enumerate(st.session_state.playlist):
                    if idx == st.session_state.current_track_idx:
                        st.markdown(f"**▶ {idx+1}. {song['title']}** (Playing)")
                    else:
                        st.markdown(f"{idx+1}. {song['title']}")
                
                st.divider()
                
                # 2. Add to Queue Logic
                new_song_name = ""#st.text_input("Request a Song", placeholder="Enter song title...")
                if False:
                    if False:
                        # We add a placeholder entry (reuse a URL for demo purposes)
                        new_entry = {
                            "title": new_song_name,
                            "artist": "Guest Request",
                            "url": "https://upload.wikimedia.org/wikipedia/commons/c/c8/Kevin_MacLeod_-_Pixelland.ogg"
                        }
                        st.session_state.playlist.append(new_entry)
                        st.toast(f"Added '{new_song_name}' to queue!", icon="✅")
                        st.rerun()
                    # --- SECTION 1: Player & Art ---
                    row1_col1, row1_col2 = st.columns([1, 2], gap="medium")
                    
                    with row1_col1:
                        # Album Art with Gold Text
                        st.image("https://placehold.co/300x300/1f2937/FFD700?text=BDAY+MIX+VOL.1", use_container_width=True)
                    
                    with row1_col2:
                        st.subheader("Now Playing")
                        st.markdown("### 🎵 Happy Birthday (Jazz Remix)")
                        st.caption("Artist: The Party Crew • Album: Celebration Vibes 2025")
                        
                        # The actual Audio Player
                        st.audio("happy-birthday-357371.mp3", format="audio/mp3")
                        
                        # Fake Playback Controls
                        ctrl1, ctrl2, ctrl3, ctrl4 = st.columns(4)
                        with ctrl1: st.button("⏮ Prev", key="prev")
                        with ctrl2: st.button("⏸ Pause", key="pause")
                        with ctrl3: st.button("Next ⏭", key="next")
                        with ctrl4: st.button("🔀 Shuffle", key="shuff")

                    st.markdown("---")

                    # --- SECTION 2: The "Visualizer" ---
                    # We use a bar chart with random data to look like an equalizer
                    st.caption("Audio Spectrum Analyzer")
                    chart_data = pd.DataFrame(
                        [random.randint(20, 100) for _ in range(40)], 
                        columns=["frequency"]
                    )
                    # Set the color to Gold (#FFD700) to match the theme
                    st.bar_chart(chart_data, height=80, color="#FFD700")

                    # --- SECTION 3: Playlist ---
                    with st.expander("View Up Next (Playlist)", expanded=True):
                        # Using markdown table for a clean look
                        st.markdown("""
                        | Track | Artist | Duration |
                        | :--- | :--- | :--- |
                        | **1. Celebration** | Kool & The Gang | 3:40 |
                        | **2. Dancing Queen** | ABBA | 3:51 |
                        | **3. September** | Earth, Wind & Fire | 3:35 |
                        | **4. Uptown Funk** | Mark Ronson | 4:30 |
                        """)
        with t2:
            st.subheader("#Some Throwback Memories")
            try:

                img1 = Image.open("PXL_20240512_174827288.jpg")
                img2 = Image.open("col2.jpg")
                img3 = Image.open("col3.jpg")
                
                # Create three columns
                col1, col2, col3 = st.columns([1,2,1])
                with col2:
                    st.image(img1, width=350)
                with col1:
                    st.image(img2, width=350)
                with col3:
                    st.image(img3, width=350)
            except:
                col1, col2, col3 = st.columns([1,2,1])
                with col2:
                    st.markdown("🎂 🎈 🎁")

    # RIGHT: Flight Physics Fragment
    with col_data:
        @st.fragment(run_every=1)
        def update_flight_status():
            st.session_state.lon -= 0.05 
            st.session_state.lat += random.uniform(-0.01, 0.01)
            st.session_state.altitude += random.randint(-15, 15)
            st.session_state.speed += random.randint(-1, 1)

            with st.container(border=True):
                st.subheader("Flight Telemetry")
                m1, m2 = st.columns(2)
                m1.metric("Altitude", f"{st.session_state.altitude:,} ft")
                m2.metric("Ground Speed", f"{st.session_state.speed} mph")
                st.write("---")
                map_data = pd.DataFrame({'lat': [st.session_state.lat], 'lon': [st.session_state.lon], 'size': [1500], 'color': ['#FFD700']})
                st.map(map_data, latitude='lat', longitude='lon', size='size', color='color', zoom=3)
                st.caption(f"Status: Cruising to Party City")

        update_flight_status()

    # --- FOOTER (WITH WHATSAPP) ---
    st.markdown("---")
    f1, f2, f3 = st.columns(3)

    with f1: 
        if st.button("💡 Dim Cabin Lights"):
            st.toast("Lights dimmed.", icon="🌑")

    with f2: 
        # WHATSAPP INTEGRATION
        # REPLACE THIS NUMBER with yours
        phone_number = "15551234567" 
        msg = "Excuse me, I am in Seat 1A and I would like to order the Birthday Cake please! 🎂"
        whatsapp_url = f"https://wa.me/{phone_number}?text={msg.replace(' ', '%20')}"
        
        # Link Button using the new CSS
        st.link_button("👋 Call Attendant ", whatsapp_url)

    with f3: 
        st.slider("Party Volume", 0, 100, 100)