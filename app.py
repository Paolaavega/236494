import streamlit as st
import pandas as pd
from extraer import procesar_pdf
from buscador import agrupar_por_grupo, buscar

st.set_page_config(page_title="Planificador de Horarios UACJ", layout="wide", page_icon="📚")

# --- MEMORIA DE LA APP ---
if "mi_horario" not in st.session_state:
    st.session_state["mi_horario"] = []
if "resultados_busqueda" not in st.session_state:
    st.session_state["resultados_busqueda"] = []
if "version_busqueda" not in st.session_state:
    st.session_state["version_busqueda"] = 0

def hay_choque(grupo_nuevo, lista_grupos):
    for g in lista_grupos:
        if g["clave"] == grupo_nuevo["clave"]:
            return "duplicado"
        for s_nueva in grupo_nuevo["sesiones"]:
            for s_guardada in g["sesiones"]:
                if s_nueva["dia"] == s_guardada["dia"]:
                    if (s_nueva["hora_inicio"] < s_guardada["hora_fin"] and 
                        s_nueva["hora_fin"] > s_guardada["hora_inicio"]):
                        return f"choque con {g['materia']}"
    return False

st.title("📚 Planificador de Horarios - UACJ")
st.markdown("Sube el PDF oficial, busca tus materias y arma tu horario antes de inscribirte.")

col_izq, col_der = st.columns([2, 1])

with col_izq:
    st.header("1. Buscar materias")
    archivo_subido = st.file_uploader("Sube el PDF de horarios", type=["pdf"])

    if archivo_subido is not None:
        if "datos_cargados" not in st.session_state:
            with st.spinner("Extrayendo datos del PDF..."):
                df = procesar_pdf(archivo_subido)
                sesiones = df.fillna("").to_dict("records")
                st.session_state["grupos"] = agrupar_por_grupo(sesiones)
                st.session_state["datos_cargados"] = True
            st.success("¡PDF procesado!")
        
        # Usamos la versión para que los campos se reinicien
        v = st.session_state["version_busqueda"]

        with st.form(f"filtros_busqueda_{v}"):
            st.write("**Filtros de búsqueda**")
            c1, c2 = st.columns(2)
            # Agregamos la versión al key para forzar el borrado
            materia = c1.text_input("Materia (ej. CALCULO)", key=f"mat_{v}")
            docente = c2.text_input("Docente", key=f"doc_{v}")
            
            dias_excluir = st.multiselect("Días que NO quieres clase", ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado"], key=f"dias_{v}")
            
            c3, c4 = st.columns(2)
            hora_min = c3.text_input("No antes de (HH:MM)", key=f"hmin_{v}")
            hora_max = c4.text_input("No después de (HH:MM)", key=f"hmax_{v}")
            
            solo_con_cupo = st.checkbox("Solo mostrar con cupo disponible", value=True, key=f"cupo_{v}")
            
            buscar_btn = st.form_submit_button("🔍 Buscar", type="primary")
        
        if buscar_btn:
            filtros = {}
            if materia: filtros["materia"] = materia
            if docente: filtros["docente"] = docente
            if dias_excluir: filtros["excluir_dias"] = dias_excluir
            if hora_min: filtros["hora_min"] = hora_min
            if hora_max: filtros["hora_max"] = hora_max
            if solo_con_cupo: filtros["solo_con_cupo"] = True
            
            grupos = st.session_state["grupos"]
            st.session_state["resultados_busqueda"], total, tiempo = buscar(grupos, filtros)
            st.session_state["tiempo_busqueda"] = tiempo
            st.session_state["total_revisados"] = total

        if st.session_state["resultados_busqueda"]:
            st.info(f"El DFS revisó {st.session_state['total_revisados']} grupos y encontró {len(st.session_state['resultados_busqueda'])} opciones en {st.session_state['tiempo_busqueda']:.4f} segundos.")
            
            for g in st.session_state["resultados_busqueda"]:
                horario_texto = " | ".join([f"{s['dia']} {s['hora_inicio']}-{s['hora_fin']}" for s in g["sesiones"]])
                
                with st.container():
                    col_info, col_btn = st.columns([4, 1])
                    with col_info:
                        st.markdown(f"**{g['materia']}** - Grupo **{g['grupo']}**")
                        st.caption(f"👨‍🏫 {g['docente']} | 🕒 {horario_texto} | 👥 Cupo: {g['cupo']}")
                    
                    with col_btn:
                        if st.button("➕ Agregar", key=f"add_{g['clave']}_{g['grupo']}"):
                            choque = hay_choque(g, st.session_state["mi_horario"])
                            
                            if choque == "duplicado":
                                st.warning("Ya tienes esta materia agregada.")
                            elif choque:
                                st.error(f"¡Choque de horario! ({choque})")
                            else:
                                st.session_state["mi_horario"].append(g)
                                
                                # EL TRUCO MÁGICO:
                                # Borramos los resultados de la izquierda
                                st.session_state["resultados_busqueda"] = []
                                # Aumentamos la versión para que las cajas de texto se dibujen vacías de nuevo
                                st.session_state["version_busqueda"] += 1
                                
                                st.rerun()
                    st.divider()

with col_der:
    st.header("2. Mi Horario")
    
    if not st.session_state["mi_horario"]:
        st.info("Aún no has agregado materias.")
    else:
        st.write(f"Has seleccionado **{len(st.session_state['mi_horario'])}** materias.")
        
        if st.button("🗑️ Limpiar todo"):
            st.session_state["mi_horario"] = []
            st.rerun()
            
        st.divider()
        
        for i, g in enumerate(st.session_state["mi_horario"]):
            with st.expander(f"✅ {g['materia']} (Gpo {g['grupo']})", expanded=True):
                for s in g["sesiones"]:
                    st.write(f"- {s['dia']}: {s['hora_inicio']} - {s['hora_fin']}")
                
                if st.button("Quitar", key=f"del_{i}"):
                    st.session_state["mi_horario"].pop(i)
                    st.rerun()