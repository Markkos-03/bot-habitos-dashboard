"""
db.py — capa de acceso a datos sobre Supabase (Postgres). v2, ajustado
al flask_app.py real de Marcos.

Requiere:
    pip install supabase

Variables de entorno esperadas:
    SUPABASE_URL
    SUPABASE_SERVICE_KEY   (la service_role key, no la anon key)
"""

import os
import secrets
from datetime import date, timedelta
from functools import lru_cache

from supabase import create_client, Client


# ------------------------------------------------------------------
# Cliente
# ------------------------------------------------------------------

@lru_cache(maxsize=1)
def get_client() -> Client:
    url = os.environ["SUPABASE_URL"]
    key = os.environ["SUPABASE_SERVICE_KEY"]
    return create_client(url, key)


# ------------------------------------------------------------------
# Usuarios
# ------------------------------------------------------------------

def get_usuario_por_chat_id(chat_id: int) -> dict | None:
    sb = get_client()
    res = sb.table("usuarios").select("*").eq("telegram_chat_id", chat_id).limit(1).execute()
    return res.data[0] if res.data else None


def get_usuario_por_hevy_token(token: str) -> dict | None:
    sb = get_client()
    res = sb.table("usuarios").select("*").eq("hevy_token", token).limit(1).execute()
    return res.data[0] if res.data else None


def get_usuario_por_stripe_customer(stripe_customer_id: str) -> dict | None:
    sb = get_client()
    res = sb.table("usuarios").select("*").eq("stripe_customer_id", stripe_customer_id).limit(1).execute()
    return res.data[0] if res.data else None


def get_usuario_por_dashboard_token(token: str) -> dict | None:
    sb = get_client()
    res = sb.table("usuarios").select("*").eq("dashboard_token", token).limit(1).execute()
    return res.data[0] if res.data else None


def obtener_o_crear_dashboard_token(usuario_id: str) -> str:
    """Devuelve el token del enlace privado al dashboard de este
    usuario. La primera vez que lo pide (comando /dashboard) genera uno
    nuevo, aleatorio e imposible de adivinar, lo guarda y lo devuelve;
    las siguientes veces devuelve siempre el mismo, así el enlace no
    cambia cada vez que lo piden."""
    sb = get_client()
    res = sb.table("usuarios").select("dashboard_token").eq("id", usuario_id).limit(1).execute()
    token_actual = res.data[0]["dashboard_token"] if res.data else None
    if token_actual:
        return token_actual
    nuevo_token = secrets.token_urlsafe(24)
    sb.table("usuarios").update({"dashboard_token": nuevo_token}).eq("id", usuario_id).execute()
    return nuevo_token


def crear_usuario(chat_id: int, username: str | None = None, nombre: str | None = None,
                   plan: str = "free") -> dict:
    sb = get_client()
    res = sb.table("usuarios").insert({
        "telegram_chat_id": chat_id,
        "telegram_username": username,
        "nombre": nombre,
        "plan": plan,
        "hevy_token": secrets.token_urlsafe(16),
    }).execute()
    return res.data[0]


def get_or_create_usuario(chat_id: int, username: str | None = None, nombre: str | None = None) -> dict:
    usuario = get_usuario_por_chat_id(chat_id)
    if usuario:
        return usuario
    return crear_usuario(chat_id, username, nombre)


def listar_usuarios_activos() -> list[dict]:
    """Todos los usuarios registrados — para los cron jobs que le
    mandan un mensaje a cada uno."""
    sb = get_client()
    return sb.table("usuarios").select("*").execute().data


def set_plan(usuario_id: str, plan: str, stripe_customer_id: str | None = None,
             stripe_subscription_id: str | None = None) -> None:
    sb = get_client()
    payload = {"plan": plan}
    if stripe_customer_id is not None:
        payload["stripe_customer_id"] = stripe_customer_id
    if stripe_subscription_id is not None:
        payload["stripe_subscription_id"] = stripe_subscription_id
    sb.table("usuarios").update(payload).eq("id", usuario_id).execute()


def set_modo_examenes(usuario_id: str, activo: bool) -> None:
    sb = get_client()
    sb.table("usuarios").update({"modo_examenes": activo}).eq("id", usuario_id).execute()


# ------------------------------------------------------------------
# Hábitos
# ------------------------------------------------------------------

def listar_habitos(usuario_id: str, solo_activos: bool = True) -> list[dict]:
    sb = get_client()
    query = sb.table("habitos").select("*").eq("usuario_id", usuario_id)
    if solo_activos:
        query = query.eq("activo", True)
    return query.order("creado_en").execute().data


def contar_habitos_activos(usuario_id: str) -> int:
    sb = get_client()
    res = (
        sb.table("habitos")
        .select("id", count="exact")
        .eq("usuario_id", usuario_id)
        .eq("activo", True)
        .execute()
    )
    return res.count or 0


def get_habito(habito_id: str) -> dict | None:
    sb = get_client()
    res = sb.table("habitos").select("*").eq("id", habito_id).limit(1).execute()
    return res.data[0] if res.data else None


def crear_habito(usuario_id: str, nombre: str, es_recordatorio: bool = False,
                  es_critico: bool = False, vinculado_hevy: bool = False) -> dict:
    sb = get_client()
    res = sb.table("habitos").insert({
        "usuario_id": usuario_id,
        "nombre": nombre,
        "es_recordatorio": es_recordatorio,
        "es_critico": es_critico,
        "vinculado_hevy": vinculado_hevy,
    }).execute()
    return res.data[0]


def vincular_habito_hevy(usuario_id: str, nombre: str) -> bool:
    """Marca este hábito como el que se completa automáticamente cuando
    llega una señal de entreno (texto pegado o foto). Solo puede haber
    uno por usuario, así que primero desmarca cualquier otro."""
    sb = get_client()
    habito = (
        sb.table("habitos")
        .select("id")
        .eq("usuario_id", usuario_id)
        .ilike("nombre", nombre)
        .eq("activo", True)
        .limit(1)
        .execute()
    )
    if not habito.data:
        return False
    sb.table("habitos").update({"vinculado_hevy": False}).eq("usuario_id", usuario_id).execute()
    sb.table("habitos").update({"vinculado_hevy": True}).eq("id", habito.data[0]["id"]).execute()
    return True


def desactivar_habito_por_nombre(usuario_id: str, nombre: str) -> bool:
    sb = get_client()
    res = (
        sb.table("habitos")
        .update({"activo": False})
        .eq("usuario_id", usuario_id)
        .ilike("nombre", nombre)
        .execute()
    )
    return bool(res.data)


# ------------------------------------------------------------------
# Registros diarios (check-ins)
# ------------------------------------------------------------------

def registrar_check(usuario_id: str, habito_id: str, fecha: date | None = None,
                     completado: bool = True) -> dict:
    sb = get_client()
    fecha = fecha or date.today()
    res = (
        sb.table("registros_habitos")
        .upsert(
            {
                "usuario_id": usuario_id,
                "habito_id": habito_id,
                "fecha": fecha.isoformat(),
                "completado": completado,
            },
            on_conflict="habito_id,fecha",
        )
        .execute()
    )
    return res.data[0]


def obtener_registros_entre(usuario_id: str, desde: date, hasta: date) -> list[dict]:
    sb = get_client()
    return (
        sb.table("registros_habitos")
        .select("*")
        .eq("usuario_id", usuario_id)
        .gte("fecha", desde.isoformat())
        .lte("fecha", hasta.isoformat())
        .execute()
        .data
    )


def obtener_registros(usuario_id: str, dias: int | None = None) -> list[dict]:
    """dias=None trae todo el historial (Pro). dias=14 trae últimas 2
    semanas (Free)."""
    hasta = date.today()
    desde = date(2000, 1, 1) if dias is None else hasta - timedelta(days=dias)
    return obtener_registros_entre(usuario_id, desde, hasta)


def calcular_racha(usuario_id: str, habito_id: str) -> int:
    sb = get_client()
    registros = (
        sb.table("registros_habitos")
        .select("fecha")
        .eq("usuario_id", usuario_id)
        .eq("habito_id", habito_id)
        .eq("completado", True)
        .order("fecha", desc=True)
        .execute()
        .data
    )
    fechas_completadas = {date.fromisoformat(r["fecha"]) for r in registros}

    racha = 0
    cursor = date.today()
    if cursor not in fechas_completadas:
        cursor -= timedelta(days=1)
    while cursor in fechas_completadas:
        racha += 1
        cursor -= timedelta(days=1)
    return racha


def marcar_habito_vinculado_hevy(usuario_id: str) -> dict | None:
    """Busca el hábito que el usuario marcó como 'vinculado_hevy'
    (equivalente a tu 'Gym' hardcodeado) y lo registra como cumplido
    hoy. Devuelve el hábito marcado, o None si el usuario no tiene
    ninguno configurado así."""
    sb = get_client()
    res = (
        sb.table("habitos")
        .select("*")
        .eq("usuario_id", usuario_id)
        .eq("vinculado_hevy", True)
        .eq("activo", True)
        .limit(1)
        .execute()
    )
    if not res.data:
        return None
    habito = res.data[0]
    registrar_check(usuario_id, habito["id"])
    return habito


# ------------------------------------------------------------------
# Entrenos (Hevy)
# ------------------------------------------------------------------

def entreno_existe(usuario_id: str, hevy_id: str) -> bool:
    sb = get_client()
    res = (
        sb.table("entrenos")
        .select("id", count="exact")
        .eq("usuario_id", usuario_id)
        .eq("hevy_id", hevy_id)
        .execute()
    )
    return (res.count or 0) > 0


def guardar_entreno(usuario_id: str, hevy_id: str, fecha: date, hora: str, titulo: str,
                     volumen_total: float, num_series: int, series: list[dict]) -> dict:
    sb = get_client()
    entreno = (
        sb.table("entrenos")
        .insert({
            "usuario_id": usuario_id,
            "hevy_id": hevy_id,
            "fecha": fecha.isoformat(),
            "hora": hora,
            "titulo": titulo,
            "volumen_total": volumen_total,
            "num_series": num_series,
        })
        .execute()
        .data[0]
    )
    if series:
        filas = [{**s, "entreno_id": entreno["id"], "usuario_id": usuario_id} for s in series]
        sb.table("entrenos_series").insert(filas).execute()
    return entreno


def registrar_fallback_hevy(usuario_id: str | None, texto_crudo: str, motivo: str) -> None:
    sb = get_client()
    sb.table("entrenos_fallback").insert({
        "usuario_id": usuario_id,
        "texto_crudo": texto_crudo[:2000],
        "motivo": motivo,
    }).execute()


# ------------------------------------------------------------------
# Citas
# ------------------------------------------------------------------

def agregar_cita(usuario_id: str, texto: str) -> dict:
    sb = get_client()
    return sb.table("citas").insert({"usuario_id": usuario_id, "texto": texto}).execute().data[0]


def listar_citas(usuario_id: str) -> list[dict]:
    """Todas las frases guardadas con /cita, la más reciente primero.
    La usa el dashboard para el carrusel de frases."""
    sb = get_client()
    return (
        sb.table("citas")
        .select("*")
        .eq("usuario_id", usuario_id)
        .order("creado_en", desc=True)
        .execute()
        .data
    )


# ------------------------------------------------------------------
# Metas del año
# ------------------------------------------------------------------

def crear_meta(usuario_id: str, nombre: str, objetivo: float, unidad: str | None = None) -> dict:
    sb = get_client()
    anio = date.today().year
    res = sb.table("metas").insert({
        "usuario_id": usuario_id,
        "nombre": nombre,
        "objetivo": objetivo,
        "unidad": unidad,
        "anio": anio,
    }).execute()
    return res.data[0]


def listar_metas(usuario_id: str, solo_activas: bool = True) -> list[dict]:
    sb = get_client()
    query = sb.table("metas").select("*").eq("usuario_id", usuario_id)
    if solo_activas:
        query = query.eq("activa", True)
    return query.order("creado_en").execute().data


def get_meta_por_nombre(usuario_id: str, nombre: str) -> dict | None:
    sb = get_client()
    res = (
        sb.table("metas")
        .select("*")
        .eq("usuario_id", usuario_id)
        .ilike("nombre", nombre)
        .eq("activa", True)
        .limit(1)
        .execute()
    )
    return res.data[0] if res.data else None


def actualizar_progreso_meta(meta_id: str, nuevo_progreso: float) -> dict:
    sb = get_client()
    res = sb.table("metas").update({"progreso": nuevo_progreso}).eq("id", meta_id).execute()
    return res.data[0]


def desactivar_meta(usuario_id: str, nombre: str) -> bool:
    sb = get_client()
    res = (
        sb.table("metas")
        .update({"activa": False})
        .eq("usuario_id", usuario_id)
        .ilike("nombre", nombre)
        .execute()
    )
    return bool(res.data)


def vincular_meta_habito(usuario_id: str, nombre_meta: str, nombre_habito: str) -> str | None:
    """Vincula una meta a un hábito ya existente para que su progreso
    se cuente solo: cada día que ese hábito se marca como cumplido
    suma 1 a la meta, sin necesidad de usar /meta a mano. Devuelve el
    nombre real del hábito vinculado, o None si no encontró la meta o
    el hábito."""
    sb = get_client()
    meta = get_meta_por_nombre(usuario_id, nombre_meta)
    if not meta:
        return None
    habito = (
        sb.table("habitos")
        .select("id, nombre")
        .eq("usuario_id", usuario_id)
        .ilike("nombre", nombre_habito)
        .eq("activo", True)
        .limit(1)
        .execute()
    )
    if not habito.data:
        return None
    sb.table("metas").update({"habito_id": habito.data[0]["id"]}).eq("id", meta["id"]).execute()
    return habito.data[0]["nombre"]


def contar_cumplidos_habito_anio(habito_id: str, usuario_id: str, anio: int) -> int:
    """Cuenta cuántos días de ese año el hábito se marcó como cumplido.
    Es lo que usan las metas vinculadas a un hábito para calcular su
    progreso automáticamente, sin guardar nada aparte."""
    sb = get_client()
    desde = date(anio, 1, 1)
    hasta = date(anio, 12, 31)
    res = (
        sb.table("registros_habitos")
        .select("id", count="exact")
        .eq("usuario_id", usuario_id)
        .eq("habito_id", habito_id)
        .eq("completado", True)
        .gte("fecha", desde.isoformat())
        .lte("fecha", hasta.isoformat())
        .execute()
    )
    return res.count or 0
