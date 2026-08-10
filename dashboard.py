"""
dashboard.py — Dashboard web multiusuario (Streamlit) para ver el
progreso de hábitos y metas, leyendo de la misma base de Supabase que
usa el bot de Telegram.

Cómo funciona el acceso: cada usuario Pro tiene un enlace privado con
un token (se lo manda el bot con /dashboard). No hay login con
contraseña ni cuentas: el token en la URL identifica al usuario, igual
que ya hace el enlace de Hevy (?token=...) que usa el bot. Es
intencionalmente simple: no hace falta gestionar contraseñas para algo
que es un complemento del bot, no un producto aparte.

Requiere las mismas variables de entorno que el bot (mismo proyecto de
Supabase, así que son las mismas credenciales):
    SUPABASE_URL
    SUPABASE_SERVICE_KEY

Para probarlo en local:
    pip install -r requirements_dashboard.txt
    streamlit run dashboard.py
    (y le pasas la URL con ?token=... de un usuario de prueba)

Para desplegarlo (Streamlit Community Cloud, Railway, Render...) sube
este archivo junto con db.py y requirements_dashboard.txt al mismo
repositorio, y configura esas dos variables de entorno como "secrets"
en la plataforma elegida. La URL pública que te den es la que pones en
DASHBOARD_URL en flask_app.py.
"""

import os
from datetime import date, timedelta

import altair as alt
import pandas as pd
import streamlit as st

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

st.set_page_config(page_title="Tu progreso", page_icon="📊", layout="centered")


def cargar_usuario():
    token = st.query_params.get("token")
    if not token:
        st.title("📊 Tu dashboard")
        st.info(
            "Este enlace es privado y personal. Pídeselo al bot de "
            "Telegram escribiendo **/dashboard**."
        )
        st.stop()
    usuario = db.get_usuario_por_dashboard_token(token)
    if not usuario:
        st.title("📊 Tu dashboard")
        st.error(
            "Este enlace no es válido. Pide uno nuevo escribiéndole al "
            "bot **/dashboard**."
        )
        st.stop()
    return usuario


usuario = cargar_usuario()

nombre = usuario.get("nombre") or usuario.get("telegram_username") or "ahí"
st.title(f"📊 Hola, {nombre}")

# ---------- Datos base ----------
habitos = db.listar_habitos(usuario["id"])
if not habitos:
    st.info("Todavía no tienes hábitos activos. Créalos con /nuevohabito desde el bot.")
    st.stop()

hoy = date.today()
desde_30 = hoy - timedelta(days=29)
registros_30 = db.obtener_registros_entre(usuario["id"], desde_30, hoy)
registros_anio = db.obtener_registros_entre(usuario["id"], date(hoy.year, 1, 1), hoy)

df_30 = pd.DataFrame(registros_30)
df_anio = pd.DataFrame(registros_anio)

# ---------- Métricas rápidas ----------
rachas = {h["nombre"]: db.calcular_racha(usuario["id"], h["id"]) for h in habitos}
racha_maxima = max(rachas.values()) if rachas else 0

if not df_30.empty:
    cumplidos_30 = df_30[df_30["completado"] == True].shape[0]
    posibles_30 = len(habitos) * 30
    pct_30 = round(100 * cumplidos_30 / posibles_30) if posibles_30 else 0
else:
    pct_30 = 0

col1, col2, col3 = st.columns(3)
col1.metric("Racha más larga", f"{racha_maxima} días")
col2.metric("Cumplimiento (30 días)", f"{pct_30}%")
col3.metric("Hábitos activos", len(habitos))

st.divider()

# ---------- Cumplimiento por hábito (30 días) ----------
st.subheader("Cumplimiento por hábito — últimos 30 días")
filas = []
for h in habitos:
    if df_30.empty:
        cumplidos = 0
    else:
        cumplidos = df_30[
            (df_30["habito_id"] == h["id"]) & (df_30["completado"] == True)
        ].shape[0]
    filas.append({
        "Hábito": h["nombre"],
        "% cumplido": round(100 * cumplidos / 30),
        "Racha actual": rachas.get(h["nombre"], 0),
    })

df_resumen = pd.DataFrame(filas).sort_values("% cumplido", ascending=False)

chart_barras = (
    alt.Chart(df_resumen)
    .mark_bar(color="#4CAF50")
    .encode(
        x=alt.X("% cumplido:Q", scale=alt.Scale(domain=[0, 100])),
        y=alt.Y("Hábito:N", sort="-x"),
        tooltip=["Hábito", "% cumplido", "Racha actual"],
    )
    .properties(height=max(120, 40 * len(habitos)))
)
st.altair_chart(chart_barras, use_container_width=True)

st.divider()

# ---------- Calendario del año (mapa de calor tipo GitHub) ----------
st.subheader(f"Constancia en {hoy.year}")
if df_anio.empty:
    st.caption("Todavía no hay registros este año.")
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
        .mark_rect()
        .encode(
            x=alt.X("semana:O", title=None, axis=alt.Axis(labels=False, ticks=False)),
            y=alt.Y(
                "dia_semana:O",
                title=None,
                axis=alt.Axis(
                    labels=True,
                    ticks=False,
                    labelExpr="['Lun','Mar','Mié','Jue','Vie','Sáb','Dom'][datum.value]",
                ),
            ),
            color=alt.Color("cumplidos:Q", scale=alt.Scale(scheme="greens"), legend=None),
            tooltip=[
                alt.Tooltip("fecha:T", title="Día"),
                alt.Tooltip("cumplidos:Q", title="Hábitos cumplidos"),
            ],
        )
        .properties(height=160)
    )
    st.altair_chart(heatmap, use_container_width=True)

st.divider()

# ---------- Metas del año ----------
st.subheader("Metas del año")
metas = db.listar_metas(usuario["id"])
if not metas:
    st.caption("No tienes metas activas. Créalas con /nuevameta desde el bot.")
else:
    for m in metas:
        if m.get("habito_id"):
            progreso = db.contar_cumplidos_habito_anio(m["habito_id"], usuario["id"], hoy.year)
        else:
            progreso = m["progreso"]
        objetivo = m["objetivo"] or 1
        pct = min(1.0, progreso / objetivo)
        unidad = f" {m['unidad']}" if m.get("unidad") else ""
        st.write(f"**{m['nombre']}** — {progreso:g}/{objetivo:g}{unidad}")
        st.progress(pct)

st.caption("Datos actualizados en tiempo real desde el bot de Telegram.")
