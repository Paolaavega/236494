import time

def agrupar_por_grupo(sesiones):
    """
    Agrupa las sesiones sueltas por (Clave, Grupo).
    Ejemplo: Las sesiones de Lunes y Miércoles del grupo A de Cálculo se unen en un solo objeto.
    """
    grupos = {}
    for s in sesiones:
        # Creamos una llave única combinando la clave de la materia y el grupo
        key = (s["clave"], s["grupo"])
        
        if key not in grupos:
            grupos[key] = {
                "clave": s["clave"],
                "materia": s["materia"],
                "grupo": s["grupo"],
                "docente": s["docente"],
                "cupo": s["cupo"],
                "sesiones": []
            }
            
        # Agregamos la sesion a la lista de sesiones de este grupo
        grupos[key]["sesiones"].append({
            "dia": s["dia"],
            "hora_inicio": s["hora_inicio"],
            "hora_fin": s["hora_fin"]
        })
        
    return list(grupos.values())

def grupo_cumple(grupo, filtros):
    """
    Evalúa si un grupo completo pasa los filtros.
    El criterio es estricto: TODAS las sesiones del grupo deben cumplir las reglas de horario y día.
    """
    for sesion in grupo["sesiones"]:
        # Si el día de la sesion está en la lista de días a excluir, el grupo entero se descarta
        if filtros.get("excluir_dias") and sesion["dia"] in filtros["excluir_dias"]:
            return False
            
        # Si la sesion empieza antes de la hora mínima deseada, se descarta el grupo
        if filtros.get("hora_min") and sesion["hora_inicio"] < filtros["hora_min"]:
            return False
            
        # Si la sesión termina después de la hora máxima deseada, se descarta el grupo
        if filtros.get("hora_max") and sesion["hora_fin"] > filtros["hora_max"]:
            return False
            
    # Filtros de texto (busqueda parcial)
    if filtros.get("materia") and filtros["materia"].lower() not in grupo["materia"].lower():
        return False
    if filtros.get("docente") and filtros["docente"].lower() not in grupo["docente"].lower():
        return False
        
    # Filtro de cupo
    if filtros.get("solo_con_cupo") and grupo["cupo"] <= 0:
        return False
        
    return True

def filtrar_dfs(grupos, filtros):
    """
    Búsqueda en Profundidad (DFS) ITERATIVA.
    Usa una pila (stack) para recorrer los grupos uno por uno sin riesgo de desbordar la memoria de Python.
    """
    # Inicializamos la pila con todos los grupos. 
    # Usamos reversed() para que el orden de salida sea el mismo que el orden original de la lista.
    pila = list(reversed(grupos)) 
    resultado = []
    
    while pila:
        # Sacamos el último elemento que entro (LIFO - Last In, First Out)
        grupo_actual = pila.pop()
        
        # Evaluamos si el grupo cumple con los filtros
        if grupo_cumple(grupo_actual, filtros):
            resultado.append(grupo_actual)
            
    return resultado

def buscar(grupos, filtros):
    """
    Función principal que ejecuta la búsqueda y mide el tiempo de ejecución.
    """
    inicio = time.perf_counter()
    
    # Aquí se ejecuta el DFS
    resultado = filtrar_dfs(grupos, filtros)
    
    fin = time.perf_counter()
    tiempo = fin - inicio
    
    return resultado, len(grupos), tiempo