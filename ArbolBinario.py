import pygame
import time

class Arbol:
    def __init__(self, nodo_huffman):
        self.valor = (nodo_huffman.caracter, nodo_huffman.frecuencia)
        self.hijo_izquierda = None
        self.hijo_derecha = None
        
        # Atributos para el dibujo incremental
        self.dibujado = False
        self.linea_izquierda_dibujada = False
        self.linea_derecha_dibujada = False

    def imprimir_nodo(self, ventana, fuente, valor, x, y, color=(0, 0, 255)):
        texto = f"{valor[0]}:{valor[1]}" if valor[0] else f"*:{valor[1]}"
        pygame.draw.circle(ventana, color, (x, y), 25)
        render = fuente.render(texto, True, (255, 255, 255))
        rect = render.get_rect(center=(x, y))
        ventana.blit(render, rect)

    def _mostrar_nodos_recursivo(self, ventana, fuente, xmin, xmax, incremento_vertical, nivel):
        x_centro = ((xmax - xmin) / 2) + xmin
        y = (incremento_vertical * nivel) + 30

        # Dibujar primero la línea izquierda y el nodo hijo izquierdo
        if self.hijo_izquierda and not self.linea_izquierda_dibujada:
            x_hijo = ((xmax - xmin) / 4) + xmin
            y_hijo = (incremento_vertical * (nivel + 1)) + 30
            pygame.draw.line(ventana, (0, 0, 0), (x_centro, y), (x_hijo, y_hijo), 2)
            pygame.display.flip()
            time.sleep(1)
            self.linea_izquierda_dibujada = True
            self.hijo_izquierda._mostrar_nodos_recursivo(ventana, fuente, xmin, x_centro, incremento_vertical, nivel + 1)
        elif self.hijo_izquierda and self.linea_izquierda_dibujada: # Si ya se dibujó la línea, solo asegurar que el hijo se dibuje
             self.hijo_izquierda._mostrar_nodos_recursivo(ventana, fuente, xmin, x_centro, incremento_vertical, nivel + 1)


        # Dibujar el nodo actual si no ha sido dibujado
        if not self.dibujado:
            self.imprimir_nodo(ventana, fuente, self.valor, x_centro, y)
            pygame.display.flip()
            time.sleep(1)
            self.dibujado = True

        # Dibujar luego la línea derecha y el nodo hijo derecho
        if self.hijo_derecha and not self.linea_derecha_dibujada:
            x_hijo = xmax - ((xmax - xmin) / 4)
            y_hijo = (incremento_vertical * (nivel + 1)) + 30
            pygame.draw.line(ventana, (0, 0, 0), (x_centro, y), (x_hijo, y_hijo), 2)
            pygame.display.flip()
            time.sleep(1)
            self.linea_derecha_dibujada = True
            self.hijo_derecha._mostrar_nodos_recursivo(ventana, fuente, x_centro, xmax, incremento_vertical, nivel + 1)
        elif self.hijo_derecha and self.linea_derecha_dibujada: # Si ya se dibujó la línea, solo asegurar que el hijo se dibuje
            self.hijo_derecha._mostrar_nodos_recursivo(ventana, fuente, x_centro, xmax, incremento_vertical, nivel + 1)


    def mostrar_arbol_grafico(self):
        ancho, alto = 1000, 700
        ventana_arbol = pygame.display.set_mode((ancho, alto))
        pygame.display.set_caption("Árbol de Huffman")
        fuente = pygame.font.SysFont("Arial", 22)
        fuente_boton = pygame.font.SysFont("Arial", 24)
        reloj = pygame.time.Clock()
        corriendo = True

        boton_volver = pygame.Rect(ancho//2 - 100, alto - 60, 200, 40)
        color_boton = (70, 130, 180)

        # Inicializar Pygame si no ha sido inicializado (aunque la clase Arbol original ya lo hacía en su __init__)
        if not pygame.get_init():
            pygame.init()

        # Reiniciar el estado de dibujado de todos los nodos antes de empezar
        self._reset_dibujado()

        # Flag para controlar si la animación ha terminado
        animacion_terminada = False

        while corriendo:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    corriendo = False
                elif evento.type == pygame.MOUSEBUTTONDOWN:
                    if boton_volver.collidepoint(evento.pos):
                        corriendo = False

            # Limpiar la ventana solo si la animación no ha terminado para evitar redibujar todo
            if not animacion_terminada:
                ventana_arbol.fill((255, 255, 255))
            
            incremento_vertical = (alto - 100) // self.altura

            # Ejecutar la animación una sola vez
            if not animacion_terminada:
                self._mostrar_nodos_recursivo(ventana_arbol, fuente, 0, ancho, incremento_vertical, 0)
                # Verificar si todos los nodos han sido dibujados
                if self._todos_los_nodos_dibujados():
                    animacion_terminada = True
            else:
                # Si la animación terminó, solo redibujar el árbol estático
                self._dibujar_arbol_completo(ventana_arbol, fuente, 0, ancho, incremento_vertical, 0)


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

        pygame.quit()

    # Métodos auxiliares para el control de la animación

    def _reset_dibujado(self):
        """Reinicia el estado de dibujado de todos los nodos del árbol."""
        self.dibujado = False
        self.linea_izquierda_dibujada = False
        self.linea_derecha_dibujada = False
        if self.hijo_izquierda:
            self.hijo_izquierda._reset_dibujado()
        if self.hijo_derecha:
            self.hijo_derecha._reset_dibujado()

    def _todos_los_nodos_dibujados(self):
        """Verifica si todos los nodos y sus líneas han sido dibujados."""
        if not self.dibujado:
            return False
        if self.hijo_izquierda and (not self.linea_izquierda_dibujada or not self.hijo_izquierda._todos_los_nodos_dibujados()):
            return False
        if self.hijo_derecha and (not self.linea_derecha_dibujada or not self.hijo_derecha._todos_los_nodos_dibujados()):
            return False
        return True

    def _dibujar_arbol_completo(self, ventana, fuente, xmin, xmax, incremento_vertical, nivel):
        """Dibuja el árbol completo de una vez (sin retardo) para cuando la animación ha terminado."""
        x_centro = ((xmax - xmin) / 2) + xmin
        y = (incremento_vertical * nivel) + 30

        if self.hijo_izquierda:
            x_hijo = ((xmax - xmin) / 4) + xmin
            y_hijo = (incremento_vertical * (nivel + 1)) + 30
            pygame.draw.line(ventana, (0, 0, 0), (x_centro, y), (x_hijo, y_hijo), 2)
            self.hijo_izquierda._dibujar_arbol_completo(ventana, fuente, xmin, x_centro, incremento_vertical, nivel + 1)

        if self.hijo_derecha:
            x_hijo = xmax - ((xmax - xmin) / 4)
            y_hijo = (incremento_vertical * (nivel + 1)) + 30
            pygame.draw.line(ventana, (0, 0, 0), (x_centro, y), (x_hijo, y_hijo), 2)
            self.hijo_derecha._dibujar_arbol_completo(ventana, fuente, x_centro, xmax, incremento_vertical, nivel + 1)
        
        self.imprimir_nodo(ventana, fuente, self.valor, x_centro, y)

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

# Clase para simular un NodoHuffman (necesaria para el constructor de Arbol)
class NodoHuffman:
    def __init__(self, caracter, frecuencia):
        self.caracter = caracter
        self.frecuencia = frecuencia
