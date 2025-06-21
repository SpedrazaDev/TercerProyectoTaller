# Leer encabezado y reconstruir árbol

# Leer bits y decodificar

# Mostrar proceso animado en pantalla



import heapq
import struct
from codificador import NodoHuffman 
from ArbolBinario import Arbol 

def construir_arbol_desde_frecuencias(frecuencias):
    # Crear un heap (cola de prioridad) de nodos Huffman
    heap = []
    for caracter, freq in frecuencias.items():
        # Añadir frecuencia como nodo hoja al heap
        heapq.heappush(heap, NodoHuffman(caracter, freq))

    # Construir el árbol combinando los nodos de menor frecuencia
    while len(heap) > 1:
        nodo1 = heapq.heappop(heap)
        nodo2 = heapq.heappop(heap)

        # (el de menor frecuencia va a la izquierda)
        if nodo1.frecuencia <= nodo2.frecuencia:
            izquierda, derecha = nodo1, nodo2
        else:
            izquierda, derecha = nodo2, nodo1

        # Crear un nuevo nodo padre que combine los dos nodos extraídos
        padre = NodoHuffman(None, izquierda.frecuencia + derecha.frecuencia)
        padre.izquierda = izquierda
        padre.derecha = derecha
        # Añadir el nodo padre al heap
        heapq.heappush(heap, padre)
    
    # El último nodo restante en el heap es la raíz del árbol de Huffman
    return heapq.heappop(heap) if heap else None


def decodificar(nombre_archivo_codificado):
    """
    Lee un archivo binario codificado con Huffman y devuelve el mensaje original.

    Args:
        nombre_archivo_codificado (str): La ruta del archivo .bin a decodificar.

    Returns:
        str: El mensaje decodificado, o None si ocurre un error.
    """
    try:
        with open(nombre_archivo_codificado, "rb") as f:
            cantidad = struct.unpack(">I", f.read(4))[0]
            print(f"DEBUG DECOD: Cantidad de caracteres únicos: {cantidad}") #

            frecuencias = {}
            for _ in range(cantidad):
                char_byte = f.read(1)
                char = char_byte.decode("utf-8")
                freq = struct.unpack(">H", f.read(2))[0]
                frecuencias[char] = freq
            print(f"DEBUG DECOD: Frecuencias leídas: {frecuencias}") #

            arbol_huffman_raiz = construir_arbol_desde_frecuencias(frecuencias)
            if arbol_huffman_raiz is None:
                print("⚠️ Error: No se pudo reconstruir el árbol de Huffman para la decodificación.")
                return None
            
            # --- DEBUG---  aqui es donde le digo que se ve que el orden(codigos) es distinto
            def generar_codigos_debug(nodo, codigo="", codigos=None):
                if codigos is None:
                    codigos = {}
                if nodo is None:
                    return codigos
                if nodo.caracter is not None:
                    codigos[nodo.caracter] = codigo if codigo else "0"
                generar_codigos_debug(nodo.izquierda, codigo + "0", codigos)
                generar_codigos_debug(nodo.derecha, codigo + "1", codigos)
                return codigos

            codigos_reconstruidos = generar_codigos_debug(arbol_huffman_raiz)
            print(f"DEBUG DECOD: Códigos reconstruidos: {codigos_reconstruidos}")

            padding_bits = struct.unpack("B", f.read(1))[0]
            print(f"DEBUG DECOD: Bits de padding: {padding_bits}") #

            bits_codificados_bytes = f.read()
            print(f"DEBUG DECOD: Longitud de bytes codificados (antes de convertir): {len(bits_codificados_bytes)}")

            bits_binarios = ""
            for byte in bits_codificados_bytes:
                bits_binarios += bin(byte)[2:].zfill(8)
            print(f"DEBUG DECOD: Cadena de bits BINARIA (antes de padding, primeros 100): {bits_binarios[:100]}...")
            print(f"DEBUG DECOD: Longitud de cadena de bits (antes de padding): {len(bits_binarios)}")

            if padding_bits > 0:
                bits_binarios = bits_binarios[:-padding_bits]
            print(f"DEBUG DECOD: Cadena de bits BINARIA (después de padding, primeros 100): {bits_binarios[:100]}...")
            print(f"DEBUG DECOD: Longitud de cadena de bits (después de padding): {len(bits_binarios)}")

            mensaje_decodificado = ""
            nodo_actual = arbol_huffman_raiz

            # --- DEBUG: Depuración paso a paso de la decodificación ---
            bits_procesados = 0
            for bit in bits_binarios:
                # print(f"DEBUG DECOD: Procesando bit {bits_procesados}: {bit}") # Para depuración MUY detallada
                if bit == '0':
                    nodo_actual = nodo_actual.izquierda
                else:
                    nodo_actual = nodo_actual.derecha

                if nodo_actual.caracter is not None:
                    mensaje_decodificado += nodo_actual.caracter
                    # print(f"DEBUG DECOD: Carácter decodificado: '{nodo_actual.caracter}'. Mensaje actual: '{mensaje_decodificado}'") # Para depuración detallada
                    nodo_actual = arbol_huffman_raiz
                bits_procesados += 1
            # --- FIN DEBUG DECODIFICACIÓN PASO A PASO ---

            print(f"✅ Archivo '{nombre_archivo_codificado}' decodificado exitosamente.")
            return mensaje_decodificado

    except FileNotFoundError:
        print(f"⚠️ Error: El archivo '{nombre_archivo_codificado}' no se encontró.")
        return None
    except Exception as e:
        print(f"⚠️ Error al decodificar el archivo '{nombre_archivo_codificado}': {e}")
        return None


# Puedes añadir esta función si quieres visualizar el árbol decodificado, similar a codificador.py
def cargar_arbol_desde_bin_para_visualizacion(nombre_archivo):
    """
    Carga la información del encabezado de un archivo binario
    y reconstruye el árbol de Huffman visual.
    """
    try:
        with open(nombre_archivo, "rb") as f:
            cantidad = struct.unpack(">I", f.read(4))[0]
            frecuencias = {}
            for _ in range(cantidad):
                char = f.read(1).decode("utf-8")
                freq = struct.unpack(">H", f.read(2))[0]
                frecuencias[char] = freq
            
            # Construir el árbol de Huffman a partir de las frecuencias
            arbol_huffman_raiz = construir_arbol_desde_frecuencias(frecuencias)
            
            # Convertir el nodo raíz de Huffman a la estructura Arbol de ArbolBinario.py
            if arbol_huffman_raiz:
                return convertir_a_arbol_visual(arbol_huffman_raiz)
            else:
                return None
    except Exception as e:
        print(f"⚠️ Error al cargar el árbol desde el archivo para visualización: {e}")
        return None

def convertir_a_arbol_visual(nodo_huffman):
    if nodo_huffman is None:
        return None
   
    nodo_visual = Arbol(nodo_huffman)
    nodo_visual.hijo_izquierda = convertir_a_arbol_visual(nodo_huffman.izquierda)
    nodo_visual.hijo_derecha = convertir_a_arbol_visual(nodo_huffman.derecha)
    return nodo_visual