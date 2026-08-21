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

# ------------------------------------------------------------------
# Idioma — el bot le añade ?lang=es|en al enlace del dashboard según
# lo que la persona eligió en Telegram con /idioma. Si llega sin ese
# parámetro (enlaces viejos, gente que entra directo a la URL), se
# asume español.
# ------------------------------------------------------------------
_lang_param = st.query_params.get("lang", "es")
IDIOMA = _lang_param if _lang_param in ("es", "en") else "es"

TEXTOS = {
    "es": {
        "titulo_pagina": "Tu progreso",
        "titulo_vacio_sin_token": "Tu dashboard",
        "msg_vacio_sin_token": "Este enlace es privado y personal. Pídeselo al bot de Telegram escribiendo <b>/dashboard</b>.",
        "titulo_enlace_invalido": "Enlace no válido",
        "msg_enlace_invalido": "Pide uno nuevo escribiéndole al bot <b>/dashboard</b>.",
        "hola_nombre": "Hola, {nombre}",
        "msg_sin_habitos": "Todavía no tienes hábitos activos. Créalos con <b>/nuevohabito</b> desde el bot.",
        "badge_pro": "✨ PLAN PRO",
        "tus_frases": "💬 Tus frases",
        "racha_mas_larga": "Racha más larga",
        "cumplimiento_30": "Cumplimiento 30 días",
        "habitos_activos": "Hábitos activos",
        "seccion_cumplimiento": "📊 Cumplimiento por hábito — últimos 30 días",
        "tooltip_habito": "Hábito",
        "tooltip_pct_cumplido": "% cumplido",
        "tooltip_racha_dias": "Racha (días)",
        "seccion_constancia": "📅 Constancia desde que empezaste",
        "sin_registros": "Todavía no hay registros.",
        "tooltip_dia": "Día",
        "tooltip_estado": "Estado",
        "estado_cumplido": "Cumplido",
        "estado_sin_marcar": "Sin marcar",
        "seccion_metas": "🏆 Metas del año",
        "progreso_automatico": "🔗 progreso automático",
        "seccion_entreno": "🏋️ Entreno — últimos 30 días",
        "kg_movidos": "Kg movidos",
        "entrenos": "Entrenos",
        "series_totales": "Series totales",
        "tooltip_grupo": "Grupo",
        "tooltip_volumen_kg": "Volumen (kg)",
        "tooltip_pct_total": "% del total",
        "top_ejercicios": "💪 Top ejercicios por volumen",
        "tooltip_ejercicio": "Ejercicio",
        "pie_tiempo_real": "Datos actualizados en tiempo real desde el bot de Telegram ✨",
    },
    "en": {
        "titulo_pagina": "Your progress",
        "titulo_vacio_sin_token": "Your dashboard",
        "msg_vacio_sin_token": "This link is private and personal. Ask the Telegram bot for it by typing <b>/dashboard</b>.",
        "titulo_enlace_invalido": "Invalid link",
        "msg_enlace_invalido": "Ask the bot for a new one by typing <b>/dashboard</b>.",
        "hola_nombre": "Hi, {nombre}",
        "msg_sin_habitos": "You don't have any active habits yet. Create them with <b>/newhabit</b> from the bot.",
        "badge_pro": "✨ PRO PLAN",
        "tus_frases": "💬 Your quotes",
        "racha_mas_larga": "Longest streak",
        "cumplimiento_30": "30-day completion",
        "habitos_activos": "Active habits",
        "seccion_cumplimiento": "📊 Completion by habit — last 30 days",
        "tooltip_habito": "Habit",
        "tooltip_pct_cumplido": "% completed",
        "tooltip_racha_dias": "Streak (days)",
        "seccion_constancia": "📅 Consistency since you started",
        "sin_registros": "No records yet.",
        "tooltip_dia": "Day",
        "tooltip_estado": "Status",
        "estado_cumplido": "Done",
        "estado_sin_marcar": "Not marked",
        "seccion_metas": "🏆 Yearly goals",
        "progreso_automatico": "🔗 automatic progress",
        "seccion_entreno": "🏋️ Workouts — last 30 days",
        "kg_movidos": "Kg moved",
        "entrenos": "Workouts",
        "series_totales": "Total sets",
        "tooltip_grupo": "Group",
        "tooltip_volumen_kg": "Volume (kg)",
        "tooltip_pct_total": "% of total",
        "top_ejercicios": "💪 Top exercises by volume",
        "tooltip_ejercicio": "Exercise",
        "pie_tiempo_real": "Data updated in real time from the Telegram bot ✨",
    },
}


def t(clave, **kwargs):
    plantilla = TEXTOS.get(IDIOMA, TEXTOS["es"]).get(clave)
    if plantilla is None:
        plantilla = TEXTOS["es"].get(clave, clave)
    return plantilla.format(**kwargs) if kwargs else plantilla


st.set_page_config(page_title=t("titulo_pagina"), page_icon="✨", layout="centered")

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

#MainMenu, footer, [data-testid="stToolbar"] { visibility: hidden; }
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

/* ---------- Menú lateral (páginas: dashboard / Privacidad / Terminos) ---------- */
[data-testid="stSidebar"] {
    background: #12122a;
    border-right: 1px solid rgba(255,255,255,0.08);
}
[data-testid="stSidebarNav"] {
    padding-top: 1.2rem;
}
[data-testid="stSidebarNav"] a {
    color: #cfcfe6 !important;
    border-radius: 10px;
    padding: 0.55rem 0.9rem !important;
    margin: 0.15rem 0.7rem;
    font-weight: 500;
    transition: background 0.15s ease, color 0.15s ease;
}
[data-testid="stSidebarNav"] a:hover {
    background: rgba(167,139,250,0.18);
    color: #ffffff !important;
}
[data-testid="stSidebarNav"] a[aria-current="page"] {
    background: linear-gradient(135deg, rgba(124,58,237,0.35), rgba(52,211,153,0.20));
    color: #ffffff !important;
}
/* El botón de abrir/cerrar el menú por defecto solo aparece bien
   visible al pasar el cursor por encima — lo forzamos a estar
   siempre visible y con buen contraste sobre el fondo oscuro. */
[data-testid="stSidebarCollapsedControl"],
[data-testid="collapsedControl"],
[data-testid="stSidebarCollapseButton"],
[data-testid="baseButton-headerNoPadding"] {
    opacity: 1 !important;
    visibility: visible !important;
}
[data-testid="stSidebarCollapsedControl"] svg,
[data-testid="collapsedControl"] svg,
[data-testid="stSidebarCollapseButton"] svg {
    color: #e5e5f0 !important;
    fill: #e5e5f0 !important;
    opacity: 1 !important;
}
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


def pantalla_vacia(titulo, mensaje):
    # Todo en una sola línea a propósito: si el HTML va indentado en
    # varias líneas, el parser de Markdown de Streamlit a veces se
    # confunde con las etiquetas anidadas y deja texto suelto tipo
    # "</div>" visible en pantalla. En una sola línea no pasa.
    html = (
        '<div class="hero" style="text-align:center;">'
        f'<h1>✨ {titulo}</h1>'
        f'<p style="color:rgba(244,244,248,0.65); margin-top:0.6rem;">{mensaje}</p>'
        '</div>'
    )
    st.markdown(html, unsafe_allow_html=True)
    st.stop()


def cargar_usuario():
    token = st.query_params.get("token")
    if not token:
        pantalla_vacia(t("titulo_vacio_sin_token"), t("msg_vacio_sin_token"))
    usuario = db.get_usuario_por_dashboard_token(token)
    if not usuario:
        pantalla_vacia(t("titulo_enlace_invalido"), t("msg_enlace_invalido"))
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

nombre = usuario.get("nombre") or usuario.get("telegram_username") or ("there" if IDIOMA == "en" else "ahí")
hoy = date.today()
fecha_fmt = hoy.strftime("%m/%d/%Y") if IDIOMA == "en" else hoy.strftime("%d/%m/%Y")

# ---------- Datos base ----------
habitos = db.listar_habitos(usuario["id"])
if not habitos:
    pantalla_vacia(t("hola_nombre", nombre=nombre), t("msg_sin_habitos"))

desde_30 = hoy - timedelta(days=29)
registros_30 = db.obtener_registros_entre(usuario["id"], desde_30, hoy)
citas = db.listar_citas(usuario["id"])

df_30 = pd.DataFrame(registros_30)

# ---------- Hero ----------
hero_html = (
    '<div class="hero">'
    f'<div class="fecha">{fecha_fmt}</div>'
    f'<h1>{t("hola_nombre", nombre=nombre)} 👋</h1>'
    f'<span class="badge">{t("badge_pro")}</span>'
    '</div>'
)
st.markdown(hero_html, unsafe_allow_html=True)

# ---------- Carrusel de frases guardadas con /cita ----------
if citas:
    frases_js = json.dumps([c["texto"] for c in citas])
    st.markdown(f'<div class="quote-title">{t("tus_frases")}</div>', unsafe_allow_html=True)
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

stats_html = (
    '<div class="stat-grid">'
    '<div class="stat-card"><div class="emoji">🔥</div>'
    f'<div class="value">{racha_maxima}</div>'
    f'<div class="label">{t("racha_mas_larga")}</div></div>'
    '<div class="stat-card"><div class="emoji">⚡</div>'
    f'<div class="value">{pct_30}%</div>'
    f'<div class="label">{t("cumplimiento_30")}</div></div>'
    '<div class="stat-card"><div class="emoji">🎯</div>'
    f'<div class="value">{len(habitos)}</div>'
    f'<div class="label">{t("habitos_activos")}</div></div>'
    '</div>'
)
st.markdown(stats_html, unsafe_allow_html=True)

# ---------- Cumplimiento por hábito (30 días) ----------
st.markdown(f'<div class="section-title">{t("seccion_cumplimiento")}</div>', unsafe_allow_html=True)

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
            alt.Tooltip("Hábito:N", title=t("tooltip_habito")),
            alt.Tooltip("% cumplido:Q", title=t("tooltip_pct_cumplido")),
            alt.Tooltip("Racha actual:Q", title=t("tooltip_racha_dias")),
        ],
    )
    .properties(height=max(160, 46 * len(habitos)), background="transparent")
    .configure_view(strokeWidth=0)
    .configure_axis(domain=False)
)
st.altair_chart(chart_barras, use_container_width=True)

# ---------- Constancia: una fila por hábito, una columna por día
# desde tu primer registro (no un año fijo) ----------
st.markdown(f'<div class="section-title">{t("seccion_constancia")}</div>', unsafe_allow_html=True)

registros_todos = db.obtener_registros(usuario["id"], dias=None)
df_todos = pd.DataFrame(registros_todos)

if df_todos.empty:
    st.markdown(
        f'<p style="color:rgba(244,244,248,0.5);">{t("sin_registros")}</p>',
        unsafe_allow_html=True,
    )
else:
    df_todos["fecha"] = pd.to_datetime(df_todos["fecha"])
    fecha_inicio = df_todos["fecha"].min()
    rango_fechas = pd.date_range(fecha_inicio, pd.Timestamp(hoy), freq="D")

    mapa_nombre = {h["id"]: h["nombre"] for h in habitos}
    df_todos["Hábito"] = df_todos["habito_id"].map(mapa_nombre)
    df_todos = df_todos[df_todos["Hábito"].notna()]  # solo hábitos que siguen activos

    nombres_habitos = [h["nombre"] for h in habitos]
    malla = pd.MultiIndex.from_product(
        [nombres_habitos, rango_fechas], names=["Hábito", "fecha"]
    ).to_frame(index=False)

    cumplidos = df_todos[df_todos["completado"] == True][["Hábito", "fecha"]].copy()
    cumplidos["hecho"] = t("estado_cumplido")

    malla = malla.merge(cumplidos, on=["Hábito", "fecha"], how="left")
    malla["hecho"] = malla["hecho"].fillna(t("estado_sin_marcar"))
    # Campo con la fecha en ISO (único y ordena bien aunque pasen años)
    # para posicionar las columnas; la etiqueta que se ve sí es dd/mm.
    malla["fecha_iso"] = malla["fecha"].dt.strftime("%Y-%m-%d")

    grid_chart = (
        alt.Chart(malla)
        .mark_rect(cornerRadius=3, stroke="#0a0a17", strokeWidth=2)
        .encode(
            x=alt.X(
                "fecha_iso:O",
                title=None,
                axis=alt.Axis(
                    labelAngle=-45, labelOverlap=True, grid=False, domain=False,
                    labelColor="#9ca3af", labelFontSize=10,
                    labelExpr="substring(datum.value,8,10) + '/' + substring(datum.value,5,7)",
                ),
            ),
            y=alt.Y(
                "Hábito:N", title=None, sort=nombres_habitos,
                axis=alt.Axis(grid=False, domain=False, labelColor="#f4f4f8",
                               labelFontSize=12, labelFontWeight=600),
            ),
            color=alt.Color(
                "hecho:N",
                scale=alt.Scale(domain=[t("estado_cumplido"), t("estado_sin_marcar")], range=["#34d399", "#f87171"]),
                legend=None,
            ),
            tooltip=[
                alt.Tooltip("Hábito:N", title=t("tooltip_habito")),
                alt.Tooltip("fecha:T", title=t("tooltip_dia"), format=("%m/%d/%Y" if IDIOMA == "en" else "%d/%m/%Y")),
                alt.Tooltip("hecho:N", title=t("tooltip_estado")),
            ],
        )
        .properties(height=max(140, 42 * len(habitos)), background="transparent")
        .configure_view(strokeWidth=0)
    )
    st.altair_chart(grid_chart, use_container_width=True)

# ---------- Metas del año ----------
metas = db.listar_metas(usuario["id"])
if metas:
    st.markdown(f'<div class="section-title">{t("seccion_metas")}</div>', unsafe_allow_html=True)
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
            f'<span class="linked">{t("progreso_automatico")}</span>' if m.get("habito_id") else ""
        )
        goal_html = (
            '<div class="goal-card">'
            f'<div class="goal-ring" style="background: conic-gradient({color} {pct * 3.6}deg, rgba(255,255,255,0.08) 0deg);">'
            f'<span>{pct}%</span></div>'
            '<div class="goal-info">'
            f'<div class="name">{m["nombre"]}</div>'
            f'<div class="sub">{progreso:g} / {objetivo:g}{unidad}</div>'
            f'{vinculo_html}'
            '</div>'
            '</div>'
        )
        st.markdown(goal_html, unsafe_allow_html=True)

# ---------- Entreno (Hevy) — volumen y reparto por grupo muscular,
# últimos 30 días ----------
entrenos_raw = db.listar_entrenos(usuario["id"], limite=200)
df_entrenos = pd.DataFrame(entrenos_raw)
if not df_entrenos.empty:
    df_entrenos["fecha"] = pd.to_datetime(df_entrenos["fecha"])
    df_entrenos_30 = df_entrenos[df_entrenos["fecha"] >= pd.Timestamp(desde_30)]
else:
    df_entrenos_30 = df_entrenos

if not df_entrenos_30.empty:
    st.markdown(f'<div class="section-title">{t("seccion_entreno")}</div>', unsafe_allow_html=True)

    series_30 = db.obtener_series_entre(usuario["id"], desde_30, hoy)
    df_series = pd.DataFrame(series_30)
    if not df_series.empty:
        df_series_validas = df_series[df_series["es_calentamiento"] != True]
    else:
        df_series_validas = df_series

    volumen_30 = df_series_validas["volumen_serie"].sum() if not df_series_validas.empty else 0
    # Separador de miles: punto en español (1.234), coma en inglés (1,234).
    volumen_fmt = f"{volumen_30:,.0f}" if IDIOMA == "en" else f"{volumen_30:,.0f}".replace(",", ".")

    entreno_stats_html = (
        '<div class="stat-grid">'
        '<div class="stat-card"><div class="emoji">📦</div>'
        f'<div class="value">{volumen_fmt}</div>'
        f'<div class="label">{t("kg_movidos")}</div></div>'
        '<div class="stat-card"><div class="emoji">🏋️</div>'
        f'<div class="value">{len(df_entrenos_30)}</div>'
        f'<div class="label">{t("entrenos")}</div></div>'
        '<div class="stat-card"><div class="emoji">🔢</div>'
        f'<div class="value">{len(df_series_validas)}</div>'
        f'<div class="label">{t("series_totales")}</div></div>'
        '</div>'
    )
    st.markdown(entreno_stats_html, unsafe_allow_html=True)

    if not df_series_validas.empty:
        # Colores validados para fondo oscuro (paleta categórica de 8
        # tonos, orden fijo — nunca se reasignan aunque cambien los
        # grupos presentes, para que un grupo siempre tenga el mismo
        # color de un vistazo a otro).
        GRUPO_COLORES = {
            "Pecho": "#3987e5",
            "Espalda": "#d95926",
            "Piernas": "#199e70",
            "Hombros": "#c98500",
            "Biceps": "#d55181",
            "Triceps": "#008300",
            "Core": "#9085e9",
            "Otros": "#e66767",
        }
        orden_grupos = list(GRUPO_COLORES.keys())

        por_grupo = (
            df_series_validas.assign(grupo_muscular=df_series_validas["grupo_muscular"].fillna("Otros"))
            .groupby("grupo_muscular")["volumen_serie"]
            .sum()
            .reset_index()
            .rename(columns={"grupo_muscular": "Grupo", "volumen_serie": "Volumen"})
        )
        por_grupo["pct"] = round(100 * por_grupo["Volumen"] / por_grupo["Volumen"].sum())
        por_grupo["orden"] = por_grupo["Grupo"].apply(
            lambda g: orden_grupos.index(g) if g in orden_grupos else len(orden_grupos)
        )
        # Solo entran en la leyenda los grupos que de verdad aparecen en
        # este periodo (si no, saldrían los 8 siempre, con 7 sin hueco
        # en el donut). El color de cada grupo es siempre el mismo,
        # aparezca o no, para que de un vistazo a otro no cambie.
        grupos_presentes = [g for g in orden_grupos if g in set(por_grupo["Grupo"])]

        donut = (
            alt.Chart(por_grupo)
            .mark_arc(innerRadius=64, outerRadius=108, cornerRadius=4, stroke="#0a0a17", strokeWidth=2)
            .encode(
                theta=alt.Theta("Volumen:Q", stack=True),
                order=alt.Order("orden:Q"),
                color=alt.Color(
                    "Grupo:N",
                    scale=alt.Scale(domain=grupos_presentes, range=[GRUPO_COLORES[g] for g in grupos_presentes]),
                    legend=alt.Legend(
                        title=None, labelColor="#f4f4f8", labelFontSize=12,
                        symbolType="circle", orient="right",
                    ),
                ),
                tooltip=[
                    alt.Tooltip("Grupo:N", title=t("tooltip_grupo")),
                    alt.Tooltip("Volumen:Q", format=",.0f", title=t("tooltip_volumen_kg")),
                    alt.Tooltip("pct:Q", title=t("tooltip_pct_total")),
                ],
            )
            .properties(height=270, background="transparent")
            .configure_view(strokeWidth=0)
        )
        st.altair_chart(donut, use_container_width=True)

        top_ejercicios = (
            df_series_validas.groupby("ejercicio")["volumen_serie"]
            .sum()
            .reset_index()
            .rename(columns={"ejercicio": "Ejercicio", "volumen_serie": "Volumen"})
            .sort_values("Volumen", ascending=False)
            .head(5)
        )
        if not top_ejercicios.empty:
            st.markdown(
                '<div style="margin: 1.3rem 0 0.7rem 0; font-family:\'Poppins\',sans-serif; '
                f'font-weight:700; font-size:0.95rem;">{t("top_ejercicios")}</div>',
                unsafe_allow_html=True,
            )
            chart_top = (
                alt.Chart(top_ejercicios)
                .mark_bar(cornerRadiusEnd=8, size=16, color="#22d3ee")
                .encode(
                    x=alt.X("Volumen:Q", axis=alt.Axis(grid=False, title=None, labelColor="#9ca3af")),
                    y=alt.Y("Ejercicio:N", sort="-x",
                            axis=alt.Axis(grid=False, title=None, labelColor="#f4f4f8",
                                           labelFontSize=12, labelFontWeight=600)),
                    tooltip=[
                        alt.Tooltip("Ejercicio:N", title=t("tooltip_ejercicio")),
                        alt.Tooltip("Volumen:Q", format=",.0f", title=t("tooltip_volumen_kg")),
                    ],
                )
                .properties(height=max(120, 34 * len(top_ejercicios)), background="transparent")
                .configure_view(strokeWidth=0)
                .configure_axis(domain=False)
            )
            st.altair_chart(chart_top, use_container_width=True)

st.markdown(
    f'<div class="caption-suave">{t("pie_tiempo_real")}</div>',
    unsafe_allow_html=True,
)
