# arbol.py
import pygame
import time

class Arbol:
    def __init__(self, valor):
        self.valor = valor
        self.hijo_izquierda = None
        self.hijo_derecha = None

    def imprimir_nodo(self, ventana, fuente, valor, x, y, color=(0, 0, 255)):
        pygame.draw.circle(ventana, color, (x, y), 20)
        texto_render = fuente.render(str(valor), True, (255, 255, 255))
        texto_rect = texto_render.get_rect(center=(x, y))
        ventana.blit(texto_render, texto_rect)

    def mostrar_nodos(self, ventana, fuente, xmin, xmax, incremento_vertical, nivel):
        x_centro = ((xmax - xmin) / 2) + xmin
        y = (incremento_vertical * nivel) + 30

        if self.hijo_izquierda:
            x_hijo = ((xmax - xmin) / 4) + xmin
            y_hijo = (incremento_vertical * (nivel + 1)) + 30
            pygame.draw.line(ventana, (0, 0, 0), (x_centro, y), (x_hijo, y_hijo), 4)
            self.hijo_izquierda.mostrar_nodos(ventana, fuente, xmin, x_centro, incremento_vertical, nivel + 1)

        if self.hijo_derecha:
            x_hijo = xmax - ((xmax - xmin) / 4)
            y_hijo = (incremento_vertical * (nivel + 1)) + 30
            pygame.draw.line(ventana, (0, 0, 0), (x_centro, y), (x_hijo, y_hijo), 4)
            self.hijo_derecha.mostrar_nodos(ventana, fuente, x_centro, xmax, incremento_vertical, nivel + 1)

        self.imprimir_nodo(ventana, fuente, self.valor, x_centro, y)

    def mostrar_arbol_grafico(self):
        pygame.init()
        ancho, alto = 1000, 600
        ventana = pygame.display.set_mode((ancho, alto))
        pygame.display.set_caption("Visualización del Árbol")
        fuente = pygame.font.SysFont("Arial", 22)
        reloj = pygame.time.Clock()
        corriendo = True

        while corriendo:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    corriendo = False

            ventana.fill((255, 255, 255))
            incremento_vertical = (alto - 30) // self.altura
            self.mostrar_nodos(ventana, fuente, 0, ancho, incremento_vertical, 0)

            pygame.display.flip()
            reloj.tick(60)

        pygame.quit()

    # Métodos de utilidad
    def insertar(self, valor):
        if valor <= self.valor:
            if self.hijo_izquierda is None:
                self.hijo_izquierda = Arbol(valor)
            else:
                self.hijo_izquierda.insertar(valor)
        else:
            if self.hijo_derecha is None:
                self.hijo_derecha = Arbol(valor)
            else:
                self.hijo_derecha.insertar(valor)

    @property
    def hoja(self):
        return self.hijo_izquierda is None and self.hijo_derecha is None

    @property
    def altura(self):
        if self.hoja:
            return 1
        izquierda = self.hijo_izquierda.altura if self.hijo_izquierda else 0
        derecha = self.hijo_derecha.altura if self.hijo_derecha else 0
        return max(izquierda, derecha) + 1
