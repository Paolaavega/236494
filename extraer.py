import pdfplumber
import pandas as pd
import re

def procesar_pdf(pdf_file):
    filas = []
    with pdfplumber.open(pdf_file) as pdf:
        for pagina in pdf.pages:
            tablas = pagina.extract_tables()
            for tabla in tablas:
                for fila in tabla:
                    if not fila or not fila[0] or "Clave" in str(fila[0]):
                        continue
                    filas.append(fila)
    
    datos = []
    for fila in filas:
        try:
            if len(fila) < 7: continue
                
            clave = str(fila[0]).strip() if fila[0] else ""
            materia = str(fila[1]).strip() if fila[1] else ""
            grupo = str(fila[2]).strip() if fila[2] else ""
            tipo = str(fila[3]).strip() if fila[3] else ""
            docente = str(fila[4]).strip() if fila[4] else ""
            salon = str(fila[5]).strip() if fila[5] else ""
            horario = str(fila[6]).strip() if fila[6] else ""
            cupo_str = str(fila[7]).strip() if len(fila) > 7 and fila[7] else "0"
            
            if not clave or "..." in docente:
                continue
                
            cupo_match = re.search(r'\d+', cupo_str)
            cupo = int(cupo_match.group()) if cupo_match else 0

            # Extraer día y horas
            sesiones = re.findall(r'([A-Za-záéíóúÁÉÍÓÚ]+)\s+(\d{1,2}:\d{2})-(\d{1,2}:\d{2})', horario)
            
            for dia, inicio, fin in sesiones:
                datos.append({
                    "clave": clave, "materia": materia, "grupo": grupo,
                    "tipo": tipo, "docente": docente, "salon": salon,
                    "dia": dia, "hora_inicio": inicio, "hora_fin": fin, "cupo": cupo
                })
        except Exception:
            pass
    
    return pd.DataFrame(datos)