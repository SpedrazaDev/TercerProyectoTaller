import pygame
from ArbolBinario import Arbol
from codificador import codificar, cargar_arbol_desde_bin
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
        self.botones = [
            {"texto": "Codificar", "rect": pygame.Rect(250, 200, 300, 50)},
            {"texto": "Decodificar", "rect": pygame.Rect(250, 280, 300, 50)},
            {"texto": "Mostrar Árbol", "rect": pygame.Rect(250, 360, 300, 50)},
            {"texto": "Salir", "rect": pygame.Rect(250, 440, 300, 50)},
        ]
        self.arbol = None  # Guarda el árbol tras codificar

    def draw_text(self, text, x, y, color=(0, 0, 0)):
        img = self.fuente.render(text, True, color)
        self.ventana.blit(img, (x, y))

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
                                mensaje = self.input_text("Escribe el mensaje a codificar:")
                                nombre = self.input_text("Escribe el nombre del archivo con el que quieres guardar:")
                                if mensaje:
                                    
                                    self.arbol, self.codigos, self.mensaje_codificado = codificar(mensaje, nombre)

                                    print("Codificación finalizada")
                            elif i == 1:
                                print("Aquí va lógica de decodificar (no implementada aún)")
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
