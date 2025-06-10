import pygame
import heapq
import os
import struct
import sys
from ArbolBinario import Arbol


# ---------- CLASE NODO HUFFMAN ----------
class NodoHuffman:
    def __init__(self, caracter=None, frecuencia=0):
        self.caracter = caracter
        self.frecuencia = frecuencia
        self.izquierda = None
        self.derecha = None

    def __lt__(self, otro):
        return self.frecuencia < otro.frecuencia


# ---------- FUNCIONES DE CODIFICACIÓN ----------
def contar_frecuencias(mensaje):
    frecuencias = {}
    for c in mensaje:
        frecuencias[c] = frecuencias.get(c, 0) + 1
    return frecuencias

def construir_arbol(frecuencias):
    heap = []
    for caracter, freq in frecuencias.items():
        heapq.heappush(heap, NodoHuffman(caracter, freq))

    while len(heap) > 1:
        nodo1 = heapq.heappop(heap)
        nodo2 = heapq.heappop(heap)

        # Siempre asignar el de menor frecuencia a la izquierda
        if nodo1.frecuencia <= nodo2.frecuencia:
            izquierda, derecha = nodo1, nodo2
        else:
            izquierda, derecha = nodo2, nodo1

        padre = NodoHuffman(None, izquierda.frecuencia + derecha.frecuencia)
        padre.izquierda = izquierda
        padre.derecha = derecha

        heapq.heappush(heap, padre)

    return heap[0] if heap else None


def generar_codigos(nodo, codigo="", codigos=None):
    if codigos is None:
        codigos = {}

    if nodo is None:
        return codigos

    if nodo.caracter is not None:
        codigos[nodo.caracter] = codigo if codigo else "0"

    generar_codigos(nodo.izquierda, codigo + "0", codigos)
    generar_codigos(nodo.derecha, codigo + "1", codigos)

    return codigos

def codificar_mensaje(mensaje, codigos):
    return "".join(codigos[c] for c in mensaje)


def escribir_archivo_bin(nombre, mensaje_codificado, frecuencias):
    carpeta = "archivos"
    os.makedirs(carpeta, exist_ok=True)
    ruta_bin = os.path.join(carpeta, f"{nombre}.bin")

    try:
        with open(ruta_bin, "wb") as f:
            f.write(struct.pack(">I", len(frecuencias)))

            for char, freq in sorted(frecuencias.items()):
                if len(char.encode("utf-8")) != 1:
                    raise ValueError(f"El carácter «{char}» no cabe en 1 byte ASCII.")
                if freq > 0xFFFF:
                    raise ValueError("Frecuencia supera 65535; no cabe en 2 bytes.")
                f.write(char.encode("utf-8"))
                f.write(struct.pack(">H", freq))

            bits_totales = len(mensaje_codificado)
            padding_bits = (8 - bits_totales % 8) % 8
            f.write(bytes([padding_bits]))

            b, cuenta = 0, 0
            for bit in mensaje_codificado:
                b = (b << 1) | int(bit)
                cuenta += 1
                if cuenta == 8:
                    f.write(bytes([b]))
                    b, cuenta = 0, 0
            if cuenta:
                f.write(bytes([b << (8 - cuenta)]))

        print("✅ Archivo binario guardado en:", ruta_bin)

    except (FileNotFoundError, PermissionError) as e:
        print("⚠️ Error al escribir el archivo binario:", e)
    except Exception as e:
        print("⚠️ Error inesperado:", e)


def cargar_arbol_desde_bin(nombre_archivo):
    try:
        with open(nombre_archivo, "rb") as f:
            cantidad = struct.unpack(">I", f.read(4))[0]
            frecuencias = {}
            for _ in range(cantidad):
                char = f.read(1).decode("utf-8")
                freq = struct.unpack(">H", f.read(2))[0]
                frecuencias[char] = freq
            # Saltamos el byte de padding y bits codificados (no los necesitamos ahora)
            return convertir_a_arbol_visual(construir_arbol(frecuencias))
    except Exception as e:
        print("⚠️ Error al cargar el árbol desde el archivo:", e)
        return None


def convertir_a_arbol_visual(nodo_huffman):
    if nodo_huffman is None:
        return None
    nodo_visual = Arbol(nodo_huffman)  # ✅ Pasamos el nodo, no una tupla
    nodo_visual.hijo_izquierda = convertir_a_arbol_visual(nodo_huffman.izquierda)
    nodo_visual.hijo_derecha = convertir_a_arbol_visual(nodo_huffman.derecha)
    return nodo_visual



def codificar(mensaje, nombre):
    frecuencias = contar_frecuencias(mensaje)
    arbol_huffman = construir_arbol(frecuencias)
    codigos = generar_codigos(arbol_huffman)
    mensaje_codificado = codificar_mensaje(mensaje, codigos)
    escribir_archivo_bin(nombre, mensaje_codificado, frecuencias)
    arbol_visual = convertir_a_arbol_visual(arbol_huffman)
    return arbol_visual, codigos, mensaje_codificado