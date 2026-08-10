"""
dashboard.py — Dashboard web multiusuario (Streamlit) para ver el
progreso de hábitos y metas, leyendo de la misma base de Supabase que
usa el bot de Telegram.

Cómo funciona el acceso: cada usuario Pro tiene un enlace privado con
un token (se lo manda el bot con /dashboard). No hay login con
contraseña ni cuentas: el token en la URL identifica al usuario, igual
que ya hace el enlace de Hevy (?token=...) que usa el bot.

Requiere las mismas variables de entorno que el bot (mismo proyecto de
Supabase, así que son las mismas credenciales):
    SUPABASE_URL
    SUPABASE_SERVICE_KEY

Para desplegarlo (Streamlit Community Cloud, Railway, Render...) sube
este archivo junto con db.py y requirements_dashboard.txt (como
requirements.txt) al mismo repositorio, y configura esas dos variables
como "secrets" en la plataforma elegida. La URL pública que te den es
la que pones en DASHBOARD_URL en flask_app.py.
"""

import json
import os
from datetime import date, timedelta

import altair as alt
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

# En Streamlit Community Cloud las credenciales se configuran como
# "Secrets" (st.secrets), no como variables de entorno normales, así
# que las volcamos a os.environ aquí para que db.py (compartido con el
# bot) las encuentre igual que en PythonAnywhere. En Railway/Render, que
# sí inyectan variables de entorno de verdad, st.secrets simplemente
# viene vacío y este bloque no hace nada.
try:
    for _clave in ("SUPABASE_URL", "SUPABASE_SERVICE_KEY"):
        if _clave not in os.environ and _clave in st.secrets:
            os.environ[_clave] = st.secrets[_clave]
except Exception:
    pass

import db

st.set_page_config(page_title="Tu progreso", page_icon="✨", layout="centered")

# ------------------------------------------------------------------
# Estilo — paleta pensada para transmitir logro y calma a la vez:
# violeta/índigo de fondo (premium, aspiracional), verde-turquesa como
# color de "vas bien" (crecimiento, salud) y ámbar/rojo como semáforo
# de aviso en lo que flojea. Todo con bordes redondeados: nada de cajas
# cuadradas.
# ------------------------------------------------------------------
CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Poppins:wght@600;700;800&display=swap');

html, body, [class*="css"], .stMarkdown, p, span, div {
    font-family: 'Inter', -apple-system, sans-serif;
}

.stApp {
    background:
        radial-gradient(circle at 15% -10%, rgba(124,58,237,0.35) 0%, transparent 45%),
        radial-gradient(circle at 100% 10%, rgba(16,185,129,0.20) 0%, transparent 40%),
        #0a0a17;
    color: #f4f4f8;
}

#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 2.2rem; padding-bottom: 4rem; max-width: 880px; }

.hero {
    background: linear-gradient(135deg, rgba(124,58,237,0.30), rgba(34,211,238,0.10));
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 28px;
    padding: 2rem 2.2rem;
    margin-bottom: 1.6rem;
}
.hero .fecha {
    color: rgba(244,244,248,0.55);
    font-size: 0.85rem;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-bottom: 0.4rem;
}
.hero h1 {
    font-family: 'Poppins', sans-serif;
    font-size: 2.1rem;
    font-weight: 800;
    margin: 0 0 0.35rem 0;
    line-height: 1.15;
}
.hero .badge {
    display: inline-block;
    background: linear-gradient(135deg, #a78bfa, #34d399);
    color: #0a0a17;
    font-weight: 700;
    font-size: 0.72rem;
    padding: 0.2rem 0.65rem;
    border-radius: 999px;
    letter-spacing: 0.03em;
}

.quote-title, .section-title {
    font-family: 'Poppins', sans-serif;
    font-size: 1.15rem;
    font-weight: 700;
    margin: 2.1rem 0 0.9rem 0;
}

.stat-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 0.9rem;
    margin-bottom: 0.6rem;
}
.stat-card {
    background: rgba(255,255,255,0.045);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 22px;
    padding: 1.2rem 0.8rem;
    text-align: center;
}
.stat-card .emoji { font-size: 1.5rem; margin-bottom: 0.15rem; }
.stat-card .value {
    font-family: 'Poppins', sans-serif;
    font-size: 1.9rem;
    font-weight: 800;
    background: linear-gradient(135deg, #34d399, #22d3ee);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    line-height: 1.1;
}
.stat-card .label {
    color: rgba(244,244,248,0.5);
    font-size: 0.72rem;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    margin-top: 0.25rem;
}

.goal-card {
    display: flex;
    align-items: center;
    gap: 1.1rem;
    background: rgba(255,255,255,0.045);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 20px;
    padding: 0.9rem 1.2rem;
    margin-bottom: 0.75rem;
}
.goal-ring {
    width: 58px; height: 58px;
    border-radius: 50%;
    flex-shrink: 0;
    display: flex; align-items: center; justify-content: center;
    position: relative;
}
.goal-ring::before {
    content: "";
    position: absolute;
    width: 44px; height: 44px;
    border-radius: 50%;
    background: #0f0f22;
}
.goal-ring span {
    position: relative;
    font-family: 'Poppins', sans-serif;
    font-weight: 700;
    font-size: 0.78rem;
    z-index: 1;
}
.goal-info { flex: 1; min-width: 0; }
.goal-info .name { font-weight: 700; font-size: 1rem; }
.goal-info .sub { color: rgba(244,244,248,0.5); font-size: 0.82rem; margin-top: 0.1rem; }
.goal-info .linked {
    display: inline-block;
    margin-top: 0.3rem;
    font-size: 0.68rem;
    color: #22d3ee;
    background: rgba(34,211,238,0.12);
    padding: 0.1rem 0.5rem;
    border-radius: 999px;
}

.caption-suave {
    color: rgba(244,244,248,0.4);
    font-size: 0.8rem;
    text-align: center;
    margin-top: 2.5rem;
}

/* La mayoría va a abrir esto desde el navegador interno de Telegram
   en el móvil, así que las tarjetas se apilan en pantallas estrechas. */
@media (max-width: 520px) {
    .stat-grid { grid-template-columns: 1fr 1fr; }
    .hero h1 { font-size: 1.7rem; }
    .hero { padding: 1.6rem 1.4rem; }
}
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


def pantalla_vacia(titulo, mensaje):
    st.markdown(
        f"""
        <div class="hero" style="text-align:center;">
            <h1>✨ {titulo}</h1>
            <p style="color:rgba(244,244,248,0.65); margin-top:0.6rem;">{mensaje}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.stop()


def cargar_usuario():
    token = st.query_params.get("token")
    if not token:
        pantalla_vacia(
            "Tu dashboard",
            "Este enlace es privado y personal. Pídeselo al bot de Telegram escribiendo <b>/dashboard</b>.",
        )
    usuario = db.get_usuario_por_dashboard_token(token)
    if not usuario:
        pantalla_vacia(
            "Enlace no válido",
            "Pide uno nuevo escribiéndole al bot <b>/dashboard</b>.",
        )
    return usuario


def color_semaforo(pct):
    """Rojo si va flojo, ámbar si va regular, verde si va bien — el
    código de colores más universalmente entendible que existe."""
    if pct >= 66:
        return "#34d399"
    if pct >= 33:
        return "#fbbf24"
    return "#f87171"


usuario = cargar_usuario()

nombre = usuario.get("nombre") or usuario.get("telegram_username") or "ahí"
hoy = date.today()
fecha_es = hoy.strftime("%d/%m/%Y")

# ---------- Datos base ----------
habitos = db.listar_habitos(usuario["id"])
if not habitos:
    pantalla_vacia(
        f"Hola, {nombre}",
        "Todavía no tienes hábitos activos. Créalos con <b>/nuevohabito</b> desde el bot.",
    )

desde_30 = hoy - timedelta(days=29)
registros_30 = db.obtener_registros_entre(usuario["id"], desde_30, hoy)
registros_anio = db.obtener_registros_entre(usuario["id"], date(hoy.year, 1, 1), hoy)
citas = db.listar_citas(usuario["id"])

df_30 = pd.DataFrame(registros_30)
df_anio = pd.DataFrame(registros_anio)

# ---------- Hero ----------
st.markdown(
    f"""
    <div class="hero">
        <div class="fecha">{fecha_es}</div>
        <h1>Hola, {nombre} 👋</h1>
        <span class="badge">✨ PLAN PRO</span>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------- Carrusel de frases guardadas con /cita ----------
if citas:
    frases_js = json.dumps([c["texto"] for c in citas])
    st.markdown('<div class="quote-title">💬 Tus frases</div>', unsafe_allow_html=True)
    carousel_html = f"""
    <div style="font-family:'Inter',-apple-system,sans-serif; background:linear-gradient(135deg, rgba(124,58,237,0.30), rgba(34,211,238,0.12));
                border:1px solid rgba(255,255,255,0.08); border-radius:22px; padding:1.5rem 1.8rem;
                text-align:center; color:#f4f4f8; box-sizing:border-box;">
        <div id="quote-text" style="font-size:1.1rem; font-style:italic; line-height:1.55; min-height:3rem;
                                     opacity:1; transition:opacity .5s ease;"></div>
    </div>
    <script>
        const frases = {frases_js};
        let i = 0;
        const el = document.getElementById("quote-text");
        function mostrar() {{
            el.style.opacity = 0;
            setTimeout(() => {{
                el.textContent = "\\u201C" + frases[i] + "\\u201D";
                el.style.opacity = 1;
                i = (i + 1) % frases.length;
            }}, 400);
        }}
        mostrar();
        setInterval(mostrar, 20000);
    </script>
    """
    components.html(carousel_html, height=130)

# ---------- Métricas rápidas ----------
rachas = {h["nombre"]: db.calcular_racha(usuario["id"], h["id"]) for h in habitos}
racha_maxima = max(rachas.values()) if rachas else 0

if not df_30.empty:
    cumplidos_30 = df_30[df_30["completado"] == True].shape[0]
    posibles_30 = len(habitos) * 30
    pct_30 = round(100 * cumplidos_30 / posibles_30) if posibles_30 else 0
else:
    pct_30 = 0

st.markdown(
    f"""
    <div class="stat-grid">
        <div class="stat-card">
            <div class="emoji">🔥</div>
            <div class="value">{racha_maxima}</div>
            <div class="label">Racha más larga</div>
        </div>
        <div class="stat-card">
            <div class="emoji">⚡</div>
            <div class="value">{pct_30}%</div>
            <div class="label">Cumplimiento 30 días</div>
        </div>
        <div class="stat-card">
            <div class="emoji">🎯</div>
            <div class="value">{len(habitos)}</div>
            <div class="label">Hábitos activos</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------- Cumplimiento por hábito (30 días) ----------
st.markdown('<div class="section-title">📊 Cumplimiento por hábito — últimos 30 días</div>', unsafe_allow_html=True)

filas = []
for h in habitos:
    if df_30.empty:
        cumplidos = 0
    else:
        cumplidos = df_30[
            (df_30["habito_id"] == h["id"]) & (df_30["completado"] == True)
        ].shape[0]
    pct = round(100 * cumplidos / 30)
    filas.append({
        "Hábito": h["nombre"],
        "% cumplido": pct,
        "Racha actual": rachas.get(h["nombre"], 0),
        "color": color_semaforo(pct),
    })

df_resumen = pd.DataFrame(filas).sort_values("% cumplido", ascending=False)

chart_barras = (
    alt.Chart(df_resumen)
    .mark_bar(cornerRadiusEnd=8, size=20)
    .encode(
        x=alt.X("% cumplido:Q", scale=alt.Scale(domain=[0, 100]),
                axis=alt.Axis(grid=False, title=None, labelColor="#9ca3af", tickColor="#2a2a3f")),
        y=alt.Y("Hábito:N", sort="-x",
                axis=alt.Axis(grid=False, title=None, labelColor="#f4f4f8", labelFontSize=13, labelFontWeight=600)),
        color=alt.Color("color:N", scale=None, legend=None),
        tooltip=[
            alt.Tooltip("Hábito:N"),
            alt.Tooltip("% cumplido:Q"),
            alt.Tooltip("Racha actual:Q", title="Racha (días)"),
        ],
    )
    .properties(height=max(160, 46 * len(habitos)), background="transparent")
    .configure_view(strokeWidth=0)
    .configure_axis(domain=False)
)
st.altair_chart(chart_barras, use_container_width=True)

# ---------- Calendario del año (mapa de calor tipo GitHub) ----------
st.markdown(f'<div class="section-title">📅 Constancia en {hoy.year}</div>', unsafe_allow_html=True)
if df_anio.empty:
    st.markdown(
        '<p style="color:rgba(244,244,248,0.5);">Todavía no hay registros este año.</p>',
        unsafe_allow_html=True,
    )
else:
    cumplidos_por_dia = (
        df_anio[df_anio["completado"] == True]
        .groupby("fecha")
        .size()
        .reset_index(name="cumplidos")
    )
    cumplidos_por_dia["fecha"] = pd.to_datetime(cumplidos_por_dia["fecha"])
    cumplidos_por_dia["semana"] = cumplidos_por_dia["fecha"].dt.isocalendar().week
    cumplidos_por_dia["dia_semana"] = cumplidos_por_dia["fecha"].dt.dayofweek

    heatmap = (
        alt.Chart(cumplidos_por_dia)
        .mark_rect(cornerRadius=4, stroke="#0a0a17", strokeWidth=3)
        .encode(
            x=alt.X("semana:O", title=None, axis=alt.Axis(labels=False, ticks=False, domain=False)),
            y=alt.Y(
                "dia_semana:O",
                title=None,
                axis=alt.Axis(
                    labels=True, ticks=False, domain=False, labelColor="#9ca3af", labelFontSize=11,
                    labelExpr="['Lun','Mar','Mié','Jue','Vie','Sáb','Dom'][datum.value]",
                ),
            ),
            color=alt.Color(
                "cumplidos:Q",
                scale=alt.Scale(range=["#151530", "#34d399"]),
                legend=None,
            ),
            tooltip=[
                alt.Tooltip("fecha:T", title="Día"),
                alt.Tooltip("cumplidos:Q", title="Hábitos cumplidos"),
            ],
        )
        .properties(height=170, background="transparent")
        .configure_view(strokeWidth=0)
    )
    st.altair_chart(heatmap, use_container_width=True)

# ---------- Metas del año ----------
metas = db.listar_metas(usuario["id"])
if metas:
    st.markdown('<div class="section-title">🏆 Metas del año</div>', unsafe_allow_html=True)
    for m in metas:
        if m.get("habito_id"):
            progreso = db.contar_cumplidos_habito_anio(m["habito_id"], usuario["id"], hoy.year)
        else:
            progreso = m["progreso"]
        objetivo = m["objetivo"] or 1
        pct = min(100, round(100 * progreso / objetivo))
        color = color_semaforo(pct)
        unidad = f" {m['unidad']}" if m.get("unidad") else ""
        vinculo_html = (
            '<span class="linked">🔗 progreso automático</span>' if m.get("habito_id") else ""
        )
        st.markdown(
            f"""
            <div class="goal-card">
                <div class="goal-ring" style="background: conic-gradient({color} {pct * 3.6}deg, rgba(255,255,255,0.08) 0deg);">
                    <span>{pct}%</span>
                </div>
                <div class="goal-info">
                    <div class="name">{m['nombre']}</div>
                    <div class="sub">{progreso:g} / {objetivo:g}{unidad}</div>
                    {vinculo_html}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

st.markdown(
    '<div class="caption-suave">Datos actualizados en tiempo real desde el bot de Telegram ✨</div>',
    unsafe_allow_html=True,
)
