import pygame

class Arbol:
    def __init__(self, nodo_huffman):
        self.valor = (nodo_huffman.caracter, nodo_huffman.frecuencia)
        self.hijo_izquierda = None
        self.hijo_derecha = None

    def imprimir_nodo(self, ventana, fuente, valor, x, y, color=(0, 0, 255)):
        texto = f"{valor[0]}:{valor[1]}" if valor[0] else f"*:{valor[1]}"
        pygame.draw.circle(ventana, color, (x, y), 25)
        render = fuente.render(texto, True, (255, 255, 255))
        rect = render.get_rect(center=(x, y))
        ventana.blit(render, rect)

    def mostrar_nodos(self, ventana, fuente, xmin, xmax, incremento_vertical, nivel):
        x_centro = ((xmax - xmin) / 2) + xmin
        y = (incremento_vertical * nivel) + 30

        if self.hijo_izquierda:
            x_hijo = ((xmax - xmin) / 4) + xmin
            y_hijo = (incremento_vertical * (nivel + 1)) + 30
            pygame.draw.line(ventana, (0, 0, 0), (x_centro, y), (x_hijo, y_hijo), 2)
            self.hijo_izquierda.mostrar_nodos(ventana, fuente, xmin, x_centro, incremento_vertical, nivel + 1)

        if self.hijo_derecha:
            x_hijo = xmax - ((xmax - xmin) / 4)
            y_hijo = (incremento_vertical * (nivel + 1)) + 30
            pygame.draw.line(ventana, (0, 0, 0), (x_centro, y), (x_hijo, y_hijo), 2)
            self.hijo_derecha.mostrar_nodos(ventana, fuente, x_centro, xmax, incremento_vertical, nivel + 1)

        self.imprimir_nodo(ventana, fuente, self.valor, x_centro, y)

    def mostrar_arbol_grafico(self):
        ancho, alto = 1000, 700
        ventana_arbol = pygame.display.set_mode((ancho, alto))  # Nueva ventana
        pygame.display.set_caption("Árbol de Huffman")
        fuente = pygame.font.SysFont("Arial", 22)
        fuente_boton = pygame.font.SysFont("Arial", 24)
        reloj = pygame.time.Clock()
        corriendo = True

        boton_volver = pygame.Rect(ancho//2 - 100, alto - 60, 200, 40)
        color_boton = (70, 130, 180)

        while corriendo:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    corriendo = False
                elif evento.type == pygame.MOUSEBUTTONDOWN:
                    if boton_volver.collidepoint(evento.pos):
                        corriendo = False

            ventana_arbol.fill((255, 255, 255))  # Usar ventana_arbol en lugar de self.ventana
            
            incremento_vertical = (alto - 100) // self.altura
            self.mostrar_nodos(ventana_arbol, fuente, 0, ancho, incremento_vertical, 0)

            pygame.draw.rect(ventana_arbol, color_boton, boton_volver, border_radius=5)
            texto_boton = fuente_boton.render("Volver al Menú", True, (255, 255, 255))
            texto_rect = texto_boton.get_rect(center=boton_volver.center)
            ventana_arbol.blit(texto_boton, texto_rect)

            mouse_pos = pygame.mouse.get_pos()
            if boton_volver.collidepoint(mouse_pos):
                color_boton = (100, 150, 200)
            else:
                color_boton = (70, 130, 180)

            pygame.display.flip()
            reloj.tick(60)

    @property
    def hoja(self):
        return self.hijo_izquierda is None and self.hijo_derecha is None

    @property
    def altura(self):
        if self.hoja:
            return 1
        izq = self.hijo_izquierda.altura if self.hijo_izquierda else 0
        der = self.hijo_derecha.altura if self.hijo_derecha else 0
        return max(izq, der) + 1