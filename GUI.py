import pygame
from ArbolBinario import Arbol
from codificador import codificar, cargar_arbol_desde_bin
from decodificador import decodificar # Añade esta línea
import os
import sys



class GUI:
    def __init__(self):
        pygame.init()
        self.ancho = 800
        self.alto = 600
        self.ventana = pygame.display.set_mode((self.ancho, self.alto))
        pygame.display.set_caption("Codificación Binaria - Menú")
        self.fuente = pygame.font.SysFont("Arial", 24)
        # Definir dimensiones de los botones
        boton_ancho = 300
        boton_alto = 50
        espacio_entre_botones = 30
        
        # Calcular posición inicial centrada verticalmente
        total_botones_alto = (4 * boton_alto) + (3 * espacio_entre_botones)
        y_inicial = (self.alto - total_botones_alto) // 2
        
        # Crear botones centrados
        self.botones = [
            {"texto": "Codificar", "rect": pygame.Rect((self.ancho - boton_ancho)//2, y_inicial, boton_ancho, boton_alto)},
            {"texto": "Decodificar", "rect": pygame.Rect((self.ancho - boton_ancho)//2, y_inicial + boton_alto + espacio_entre_botones, boton_ancho, boton_alto)},
            {"texto": "Mostrar Árbol", "rect": pygame.Rect((self.ancho - boton_ancho)//2, y_inicial + 2*(boton_alto + espacio_entre_botones), boton_ancho, boton_alto)},
            {"texto": "Salir", "rect": pygame.Rect((self.ancho - boton_ancho)//2, y_inicial + 3*(boton_alto + espacio_entre_botones), boton_ancho, boton_alto)},
        ]
        self.arbol = None  # Guarda el árbol tras codificar

    def draw_text(self, text, x, y, color=(0, 0, 0)):
        img = self.fuente.render(text, True, color)
        self.ventana.blit(img, (x, y))

        
    def mostrar_mensaje_decodificado_y_volver(self, mensaje):
        corriendo_sub_pantalla = True
        reloj = pygame.time.Clock()
        boton_rect = pygame.Rect(250, 400, 300, 50) # Rect para el botón "Volver al Menú"

        while corriendo_sub_pantalla:
            self.ventana.fill((255, 255, 255)) # Fondo blanco

            self.draw_text("Mensaje Decodificado:", self.ancho // 2 - 150, 100, (0, 0, 0))
            # Ajusta la posición para centrar el mensaje o mostrarlo de forma legible
            # Usaremos un color verde para el mensaje decodificado, como antes
            self.draw_text(mensaje, self.ancho // 2 - (len(mensaje) * 6), 200, (0, 128, 0)) # Ajuste aproximado para centrar

            # Dibujar botón "Volver al Menú"
            pygame.draw.rect(self.ventana, (0, 100, 200), boton_rect)
            texto_boton = pygame.font.SysFont("Arial", 30).render("Volver al Menú", True, (255, 255, 255))
            texto_boton_rect = texto_boton.get_rect(center=boton_rect.center)
            self.ventana.blit(texto_boton, texto_boton_rect)

            pygame.display.flip()

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    corriendo_sub_pantalla = False
                    return "salir" # Indica que el usuario quiere salir del programa
                elif evento.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if boton_rect.collidepoint(pos):
                        corriendo_sub_pantalla = False # El usuario hizo click en volver, salir de esta sub-pantalla
                        return "menu_principal" # Indica que debe volver al menú principal

            reloj.tick(60)
        return "salir" # Si el bucle se cierra por QUIT (cerrar ventana)
    
    def mostrar_mensaje_codificado_y_volver(self, mensaje_original, mensaje_codificado, codigos):
        corriendo_sub_pantalla = True
        reloj = pygame.time.Clock()
        boton_rect = pygame.Rect(250, 500, 300, 50)  # Bajé el botón para dar más espacio

        while corriendo_sub_pantalla:
            self.ventana.fill((255, 255, 255))  # Fondo blanco

            # Título
            self.draw_text("Resultado de la Codificación", self.ancho // 2 - 150, 50, (0, 0, 0))
            
            # Mensaje original
            self.draw_text("Mensaje Original:", 50, 120, (0, 0, 0))
            self.draw_text(mensaje_original, 50, 150, (0, 100, 0))
            
            # Mensaje codificado (los bits)
            self.draw_text("Mensaje Codificado (bits):", 50, 200, (0, 0, 0))
            # Si el mensaje codificado es muy largo, lo cortamos para que quepa
            if len(mensaje_codificado) > 80:
                linea1 = mensaje_codificado[:80]
                linea2 = mensaje_codificado[80:160] + ("..." if len(mensaje_codificado) > 160 else "")
                self.draw_text(linea1, 50, 230, (0, 0, 200))
                self.draw_text(linea2, 50, 260, (0, 0, 200))
            else:
                self.draw_text(mensaje_codificado, 50, 230, (0, 0, 200))
            
            # Tabla de códigos
            self.draw_text("Tabla de Códigos:", 50, 320, (0, 0, 0))
            y_pos = 350
            caracteres_por_linea = 0
            x_pos = 50
            
            for caracter, codigo in codigos.items():
                # Mostrar el carácter y su código
                if caracter == ' ':
                    texto_codigo = f"[ESPACIO]: {codigo}"
                else:
                    texto_codigo = f"'{caracter}': {codigo}"
                
                self.draw_text(texto_codigo, x_pos, y_pos, (100, 0, 100))
                
                # Control de layout - máximo 4 códigos por línea
                caracteres_por_linea += 1
                if caracteres_por_linea >= 4:
                    y_pos += 25
                    x_pos = 50
                    caracteres_por_linea = 0
                else:
                    x_pos += 180  # Espaciado horizontal
            
            # Información adicional
            info_y = y_pos + 50 if caracteres_por_linea == 0 else y_pos + 75
            self.draw_text(f"Caracteres únicos: {len(codigos)}", 50, info_y, (128, 128, 128))
            self.draw_text(f"Bits totales: {len(mensaje_codificado)}", 300, info_y, (128, 128, 128))
            self.draw_text(f"Bytes originales: {len(mensaje_original)}", 500, info_y, (128, 128, 128))

            # Botón "Volver al Menú"
            pygame.draw.rect(self.ventana, (0, 100, 200), boton_rect)
            texto_boton = pygame.font.SysFont("Arial", 30).render("Volver al Menú", True, (255, 255, 255))
            texto_boton_rect = texto_boton.get_rect(center=boton_rect.center)
            self.ventana.blit(texto_boton, texto_boton_rect)

            pygame.display.flip()

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    corriendo_sub_pantalla = False
                    return "salir"
                elif evento.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if boton_rect.collidepoint(pos):
                        corriendo_sub_pantalla = False
                        return "menu_principal"

            reloj.tick(60)
        return "salir"


    def mostrar_menu(self):
        corriendo = True
        reloj = pygame.time.Clock()

        while corriendo:
            self.ventana.fill((255, 255, 255))
            for boton in self.botones:
                pygame.draw.rect(self.ventana, (0, 100, 200), boton["rect"])
                texto = pygame.font.SysFont("Arial", 30).render(boton["texto"], True, (255, 255, 255))
                texto_rect = texto.get_rect(center=boton["rect"].center)
                self.ventana.blit(texto, texto_rect)
            pygame.display.flip()

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    corriendo = False
                elif evento.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    for i, boton in enumerate(self.botones):
                        if boton["rect"].collidepoint(pos):
                            if i == 0:  # Codificar
                                mensaje_codificar = self.input_text("Escribe el mensaje a codificar:")
                                nombre = self.input_text("Escribe el nombre del archivo con el que quieres guardar:")
                                
                                if mensaje_codificar:
                                    self.arbol, self.codigos, self.mensaje_codificado = codificar(mensaje_codificar, nombre)
                                    accion = self.mostrar_mensaje_codificado_y_volver(
                                        mensaje_codificar,      # Mensaje original
                                        self.mensaje_codificado, # Cadena de bits codificada
                                        self.codigos            # Diccionario de códigos
                                    )
                                    if accion == "salir":
                                        corriendo = False
                                        break
                                    print("Codificación finalizada")
                            elif i == 1:  # Decodificar
                                nombre_base_archivo = self.input_text("Ingrese el nombre del archivo .bin (sin extensión):")
                                
                                if nombre_base_archivo:  # Si el usuario no canceló
                                    nombre_base_archivo = nombre_base_archivo.strip()
                                    ruta_completa = os.path.join("archivos", f"{nombre_base_archivo}.bin")
                                    
                                    # Verificar existencia del archivo
                                    if not os.path.exists(ruta_completa):
                                        self.mostrar_mensaje_temporal(f"Archivo no encontrado: {nombre_base_archivo}.bin", 2000, (255, 0, 0))
                                        continue
                                        
                                    # Mostrar progreso
                                    self.mostrar_mensaje_temporal("Decodificando...", 500, (0, 100, 0))
                                    
                                    try:
                                        mensaje_decodificado = decodificar(ruta_completa)
                                        
                                        if mensaje_decodificado:
                                            accion = self.mostrar_mensaje_decodificado_y_volver(mensaje_decodificado)
                                            if accion == "salir":
                                                corriendo = False
                                                break
                                        else:
                                            self.mostrar_mensaje_temporal("El archivo está vacío o es inválido", 2000, (255, 0, 0))
                                            
                                    except Exception as e:
                                        self.mostrar_mensaje_temporal(f"Error: {str(e)}", 3000, (255, 0, 0))
                            elif i == 2:  # Mostrar árbol
                                archivo = self.input_text("Escribe el nombre del archivo .bin (sin .bin):")
                                if archivo:
                                    ruta = os.path.join("archivos", archivo + ".bin")
                                    arbol_cargado = cargar_arbol_desde_bin(ruta)
                                    if arbol_cargado:
                                        arbol_cargado.mostrar_arbol_grafico()
                                    else:
                                        print("No se pudo cargar el árbol.")

                                else:
                                    print("No hay árbol para mostrar. Primero codifica un mensaje.")
                            elif i == 3:
                                pygame.quit()
                                sys.exit()
            reloj.tick(60)

        pygame.quit()

    def mostrar_mensaje_temporal(self, mensaje, duracion_ms, color=(0, 0, 0)):
        """Muestra un mensaje temporal en la pantalla"""
        self.ventana.fill((255, 255, 255))
        self.draw_text(mensaje, 
                    self.ancho//2 - len(mensaje)*6,  # Aproximación para centrar
                    self.alto//2,
                    color)
        pygame.display.flip()
        pygame.time.wait(duracion_ms)

    def input_text(self, prompt):
        # Muestra prompt y permite que el usuario escriba texto hasta ENTER
        texto = ""
        input_activo = True
        reloj = pygame.time.Clock()

        while input_activo:
            self.ventana.fill((255, 255, 255))
            self.draw_text(prompt, 20, 50)
            self.draw_text(texto + "|", 20, 100)  # Barra de cursor

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_RETURN:
                        input_activo = False
                    elif evento.key == pygame.K_BACKSPACE:
                        texto = texto[:-1]
                    else:
                        # Solo letras, números y algunos caracteres básicos
                        if len(evento.unicode) == 1 and evento.unicode.isprintable():
                            texto += evento.unicode

            pygame.display.flip()
            reloj.tick(30)

        return texto.strip() if texto.strip() != "" else None


if __name__ == "__main__":
    interfaz = GUI()
    interfaz.mostrar_menu()
