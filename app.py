import os
import streamlit as st
from bokeh.models.widgets import Button
from bokeh.models import CustomJS
from streamlit_bokeh_events import streamlit_bokeh_events
from PIL import Image
import time
import paho.mqtt.client as paho
import json
from gtts import gTTS
from googletrans import Translator

def on_publish(client,userdata,result):
    print("el dato ha sido publicado \n")
    pass

def on_message(client, userdata, message):
    global message_received
    time.sleep(2)
    message_received = str(message.payload.decode("utf-8"))
    st.write(message_received)

broker="broker.mqttdashboard.com"
port=1883
client1= paho.Client("LucesCSC")
client1.on_message = on_message

# ===================== ESTILO =====================
st.set_page_config(page_title="Interfaces Multimodales", page_icon="🪐", layout="centered")
st.markdown("""
<style>
/* Fondo galaxia con estrellas animadas */
body {
    background: radial-gradient(1200px 700px at 15% 10%, #1b2440 0%, transparent 60%),
                radial-gradient(900px 500px at 85% 20%, #211b43 0%, transparent 60%),
                linear-gradient(180deg, #0b1120 0%, #020617 100%);
}
#stars, #stars2, #stars3 {
  position: fixed; top: 0; left: 0; right: 0; bottom: 0;
  display: block; z-index: -1; background: transparent;
  background-repeat: repeat;
}
#stars { background-image: radial-gradient(2px 2px at 20px 30px, #ffffffa6, transparent 40%);
         animation: animStar 120s linear infinite; opacity: 0.4; }
#stars2 { background-image: radial-gradient(1px 1px at 40px 60px, #a5b4fccc, transparent 40%);
          animation: animStar 180s linear infinite; opacity: 0.3; }
#stars3 { background-image: radial-gradient(1.5px 1.5px at 80px 120px, #93c5fdcc, transparent 40%);
          animation: animStar 240s linear infinite; opacity: 0.25; }
@keyframes animStar { from {background-position: 0 0;} to {background-position: -10000px 10000px;} }

.main > div { padding-top: 0rem; }
.container { max-width: 760px; margin: 0 auto; }

/* Hero “cabina estelar” */
.hero {
    position: relative;
    margin-top: 1rem;
    padding: 1.5rem 1.2rem;
    border-radius: 22px;
    background: linear-gradient(180deg, rgba(255,255,255,0.06), rgba(255,255,255,0.03));
    border: 1px solid rgba(255,255,255,0.12);
    box-shadow: 0 10px 40px rgba(0,0,0,0.35);
    backdrop-filter: blur(10px);
    text-align: center;
}
.hero:before, .hero:after {
    content: ""; position: absolute; inset: -1px; border-radius: 24px;
    pointer-events: none;
}
.hero:before {
    background: conic-gradient(from 180deg at 50% 50%, #7c3aed66, #2563eb66, #22d3ee44, #7c3aed66);
    filter: blur(30px); opacity: 0.25;
}

/* Logo constelación */
.logo-wrap { display: flex; justify-content: center; margin-bottom: .4rem; }
.logo-constellation { width: 86px; height: 86px; }
.spark {
  filter: drop-shadow(0 0 6px #93c5fd) drop-shadow(0 0 12px #7c3aed);
  animation: twinkle 2.4s ease-in-out infinite;
}
@keyframes twinkle { 0%,100%{opacity:.8; transform:scale(1)} 50%{opacity:1; transform:scale(1.06)} }

/* Tarjeta vidrio */
.glass-card {
    background: rgba(255, 255, 255, 0.06);
    border: 1px solid rgba(255, 255, 255, 0.12);
    border-radius: 20px;
    padding: 1.6rem;
    box-shadow: 0 0 25px rgba(0,0,0,0.35);
    backdrop-filter: blur(12px);
    text-align: center;
}

/* Tipos, colores */
h1 { color: #f8fafc !important; text-align: center; font-weight: 800; letter-spacing: 0.5px; margin-bottom: 0.2rem; }
h2, h3, h4 { color: #cbd5e1 !important; text-align: center; }
p, .stMarkdown { color: #94a3b8 !important; font-size: 0.98rem; }
small, .muted { color: #7e8aa6 !important; }

img { display: block; margin: 0.6rem auto 0.8rem auto; border-radius: 16px; box-shadow: 0 8px 28px rgba(0,0,0,0.45); }

/* Botón micrófono */
.voice-btn .bk.bk-btn {
    background: radial-gradient(120% 120% at 30% 20%, #2563eb 0%, #7c3aed 60%, #a855f7 100%) !important;
    border: none !important; color: white !important; font-weight: 700 !important;
    border-radius: 16px !important; padding: 0.7rem 2rem !important; font-size: 1rem !important;
    box-shadow: 0 12px 30px rgba(124, 58, 237, 0.35);
    transition: transform .15s ease, box-shadow .15s ease;
}
.voice-btn .bk.bk-btn:hover { transform: translateY(-2px) scale(1.02); box-shadow: 0 16px 36px rgba(124,58,237,0.5); }

/* Insignias y chips */
.badge {
  display: inline-flex; align-items: center; gap: 8px;
  padding: 6px 12px; border-radius: 999px; border: 1px solid rgba(255,255,255,0.16);
  background: rgba(255,255,255,0.06); color: #c7d2fe; font-weight: 600; font-size: 0.85rem;
}
.badge small { color: #9aa7dd; font-weight: 500; }

/* Órbita decorativa */
.orbit-wrap { position: relative; height: 180px; margin: 0.6rem auto 1rem; width: 180px; }
.planet { position: absolute; top: 50%; left: 50%; width: 18px; height: 18px; background: #93c5fd;
          border-radius: 50%; transform: translate(-50%, -50%); box-shadow: 0 0 18px #93c5fd; }
.orbit {
  position: absolute; top: 50%; left: 50%; border: 1px dashed rgba(255,255,255,0.2);
  border-radius: 50%; transform: translate(-50%, -50%);
}
.o1 { width: 160px; height: 160px; animation: spin 22s linear infinite; }
.o2 { width: 120px; height: 120px; animation: spin 16s linear infinite reverse; }
.o3 { width: 80px;  height: 80px;  animation: spin 10s linear infinite; }
@keyframes spin { to { transform: translate(-50%, -50%) rotate(360deg);} }

.footer { margin-top: 1.5rem; color: #64748b; font-size: 0.85rem; text-align: center; }
code { background: rgba(15,23,42,0.35); padding: 3px 7px; border-radius: 6px; font-size: 0.82rem; color: #a5b4fc; }
.hr { height: 1px; background: linear-gradient(90deg, transparent, #ffffff24, transparent); margin: 1rem 0; }
.tip { background: rgba(37, 99, 235, 0.1); border: 1px solid rgba(37, 99, 235, 0.25); padding: .6rem .8rem; border-radius: 12px; color: #c7d2fe; }
</style>
<div id="stars"></div><div id="stars2"></div><div id="stars3"></div>
""", unsafe_allow_html=True)
# ========================================================

st.markdown("<div class='container'>", unsafe_allow_html=True)

# --- HERO / NARRATIVA + LOGO ---
st.markdown("""
<div class="hero">
  <div class="badge">🛰️ <span>Cabina de mando • <small>Streamlit → MQTT → Wokwi</small></span></div>

  <div class="logo-wrap">
    <!-- LOGO CONSTELACIÓN (SVG inline, minimal) -->
    <svg class="logo-constellation" viewBox="0 0 120 120" fill="none" xmlns="http://www.w3.org/2000/svg" aria-label="Constelación">
      <!-- Líneas -->
      <path d="M20 92 L48 70 L78 78 L100 26" stroke="url(#g1)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" opacity="0.9"/>
      <path d="M48 70 L62 40" stroke="url(#g2)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" opacity="0.8"/>

      <!-- Nodos (estrellas) -->
      <circle class="spark" cx="20" cy="92" r="3.6" fill="#a5b4fc"/>
      <circle class="spark" cx="48" cy="70" r="4.2" fill="#93c5fd"/>
      <circle class="spark" cx="62" cy="40" r="3.4" fill="#c7d2fe"/>
      <circle class="spark" cx="78" cy="78" r="4.6" fill="#a5b4fc"/>
      <circle class="spark" cx="100" cy="26" r="5.0" fill="#93c5fd"/>

      <!-- Gradientes -->
      <defs>
        <linearGradient id="g1" x1="20" y1="92" x2="100" y2="26">
          <stop offset="0" stop-color="#7c3aed"/>
          <stop offset="1" stop-color="#2563eb"/>
        </linearGradient>
        <linearGradient id="g2" x1="48" y1="70" x2="62" y2="40">
          <stop offset="0" stop-color="#22d3ee"/>
          <stop offset="1" stop-color="#7c3aed"/>
        </linearGradient>
      </defs>
    </svg>
  </div>

  <h1>INTERFACES MULTIMODALES</h1>
  <h3>Control por voz — <em>Constelación Domótica</em></h3>
  <p>
    Bienvenid@ a la <b>cabina estelar</b>. Aquí tu voz enciende constelaciones:<br/>
    prueba con <i>“enciende luz azul”</i>, <i>“apaga todas”</i>, o <i>“verde on”</i> y observa cómo responde tu galaxia.
  </p>
  <div class="orbit-wrap">
    <div class="orbit o1"></div>
    <div class="orbit o2"></div>
    <div class="orbit o3"></div>
    <div class="planet"></div>
  </div>
</div>
""", unsafe_allow_html=True)

st.subheader("CONTROL POR VOZ")

image = Image.open('voice_ctrl.jpg')
st.image(image, width=220)

st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
st.markdown("### 🎙 Pulsa el botón y habla")
st.markdown(
    "Convierte tu voz en texto y publícalo en MQTT → "
    "<code>voice_ctrlCSC</code><br/>"
    "<span class='muted'>Tu mensaje viajará por el broker hasta tu universo Wokwi.</span>",
    unsafe_allow_html=True
)

# ============== Botón Bokeh (SIN CAMBIOS DE LÓGICA) ==============
st.markdown("<div class='voice-btn'>", unsafe_allow_html=True)
stt_button = Button(label="🎧 Iniciar reconocimiento", width=240)

stt_button.js_on_event("button_click", CustomJS(code="""
    var recognition = new webkitSpeechRecognition();
    recognition.continuous = true;
    recognition.interimResults = true;

    recognition.onresult = function (e) {
        var value = "";
        for (var i = e.resultIndex; i < e.results.length; ++i) {
            if (e.results[i].isFinal) {
                value += e.results[i][0].transcript;
            }
        }
        if (value != "") {
            document.dispatchEvent(new CustomEvent("GET_TEXT", {detail: value}));
        }
    }
    recognition.start();
"""))

result = streamlit_bokeh_events(
    stt_button,
    events="GET_TEXT",
    key="listen",
    refresh_on_update=False,
    override_height=75,
    debounce_time=0)
st.markdown("</div>", unsafe_allow_html=True)

# --- Tips de voz y narrativa de apoyo (solo UI, sin tocar lógica) ---
st.markdown("<div class='hr'></div>", unsafe_allow_html=True)
st.markdown("""
<div class="tip">
<b>✨ Sugerencias de comando:</b> “enciende luz <code>azul</code> / <code>roja</code> / <code>verde</code>”, “apaga todas”, “amarilla off”.
<br/>Cada orden se publica en el topic <code>voice_ctrlCSC</code> para que Wokwi la reciba.
</div>
""", unsafe_allow_html=True)

# ============== Lógica MQTT (sin tocar) ==============
if result:
    if "GET_TEXT" in result:
        st.write(result.get("GET_TEXT"))
        client1.on_publish = on_publish
        client1.connect(broker, port)
        message = json.dumps({"Act1": result.get("GET_TEXT").strip()})
        ret = client1.publish("voice_ctrlCSC", message)

    try:
        os.mkdir("temp")
    except:
        pass

st.markdown("</div>", unsafe_allow_html=True)  # glass-card

# --- Créditos / Pie ---
st.markdown("<p class='footer'>Camilo Seguro-Eafit-2025 • Demo estelar por voz • MQTT broker: <code>broker.mqttdashboard.com</code></p>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)  # container
