import os
import shutil
import subprocess

def sincronizar_archivo(nombre_archivo):
    """
    Busca el archivo generado, lo fuerza dentro de la carpeta Git y lo sube.
    ¡A prueba de balas!
    """
    # 1. Definir la base militar de Git (tu repositorio)
    repo_git = "/root/zeroclaw"
    
    # 2. El radar: todos los lugares donde Alfa suele soltar archivos
    posibles_rutas = [
        os.path.join("/root/.zeroclaw/workspace", nombre_archivo),  # Zona de trabajo principal
        os.path.join(os.getcwd(), nombre_archivo),                  # Donde sea que esté ejecutándose
        os.path.join("/root/zeroclaw", nombre_archivo)              # Por si ya lo puso en Git
    ]
    
    archivo_encontrado = None
    
    # 3. Búsqueda implacable
    for ruta in posibles_rutas:
        if os.path.exists(ruta):
            archivo_encontrado = ruta
            break # ¡Lo encontramos! Detenemos la búsqueda.
            
    if not archivo_encontrado:
        return f"❌ Error crítico: El radar no detectó '{nombre_archivo}' en el VPS."
        
    # 4. Extracción a la zona segura de Git
    ruta_final_git = os.path.join(repo_git, nombre_archivo)
    
    # Si el archivo no está en la raíz de Git, lo clonamos allí
    if archivo_encontrado != ruta_final_git:
        try:
            shutil.copy(archivo_encontrado, ruta_final_git)
        except Exception as e:
            return f"❌ Error al mover el archivo a la base Git: {str(e)}"

    # 5. Ejecución táctica (Add, Commit, Push)
    try:
        # Nos paramos obligatoriamente en la carpeta de Git
        os.chdir(repo_git)
        
        # Obligamos a Git a mirar el archivo nuevo
        subprocess.run(["git", "add", nombre_archivo], check=True, capture_output=True)
        
        # Hacemos el commit (sin check=True por si el archivo ya estaba y no hay cambios)
        mensaje_commit = f"🤖 Alfa Automático: Creación/Actualización de {nombre_archivo}"
        subprocess.run(["git", "commit", "-m", mensaje_commit], capture_output=True)
        
        # Disparamos tu script blindado para subir a GitHub
        resultado_push = subprocess.run(["./push_to_git.sh"], check=True, capture_output=True, text=True)
        
        return f"✅ ¡Éxito total! '{nombre_archivo}' fue detectado y subido a la rama main."
        
    except subprocess.CalledProcessError as e:
        # Si algo falla en la terminal, capturamos el texto exacto del error
        error_msg = e.stderr if e.stderr else e.stdout
        return f"❌ Fallo en la matriz de Git:\n{error_msg}"
    except Exception as e:
        return f"❌ Error general del sistema:\n{str(e)}"
