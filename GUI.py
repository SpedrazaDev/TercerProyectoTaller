# gui.py
import pygame
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
                            if i == 0:
                                print("Lógica de codificar")
                            elif i == 1:
                                print("Lógica de decodificar")
                            elif i == 2:
                                print("Mostrar árbol")
                            elif i == 3:
                                pygame.quit()
                                sys.exit()
            reloj.tick(60)

        pygame.quit()


if __name__ == "__main__":
    interfaz = GUI()
    interfaz.mostrar_menu()