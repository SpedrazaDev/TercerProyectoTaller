import pygame

class Arbol:
    def __init__(self, valor):
        pygame.init()
        self.valor = valor
        self.hijo_izquierda:Arbol = None
        self.hijo_derecha:Arbol = None

    def imprimir_nodo(self,raiz,valor,x,y):
        pygame.draw.circle(raiz.VENTANA, (0,0,255), (x, y), 20)
        texto_render = raiz.fuente.render(str(valor), True, (255,255,255))
        texto_rect = texto_render.get_rect(center=(x, y))
        raiz.VENTANA.blit(texto_render, texto_rect)
    
    def mostrar_nodos(self,raiz,xmin,xmax,incremento_vertical,nivel):
        import time
        if self.hijo_izquierda!=None:
            time.sleep(1)
            pygame.display.flip()
            pygame.draw.line(raiz.VENTANA, 
                            (0,0,0), 
                            (((xmax-xmin)/2)+xmin,
                            (incremento_vertical*nivel)+30),
                            (((xmax-xmin)/4)+xmin,
                            (incremento_vertical*(nivel+1))+30), 
                            4)
            self.hijo_izquierda.mostrar_nodos(raiz,
                                              xmin,((xmax-xmin)/2)+xmin,
                                              incremento_vertical,
                                              nivel+1)
        if self.hijo_derecha!=None:
            time.sleep(1)
            pygame.display.flip()
            pygame.draw.line(raiz.VENTANA, 
                            (0,0,0), 
                            (((xmax-xmin)/2)+xmin,
                            (incremento_vertical*nivel)+30),
                            (xmax-((xmax-xmin)/4),
                            (incremento_vertical*(nivel+1))+30), 
                            4)
            self.hijo_derecha.mostrar_nodos(raiz,
                                              ((xmax-xmin)/2)+xmin,xmax,
                                              incremento_vertical,
                                              nivel+1)
        self.imprimir_nodo(raiz,self.valor,
                           ((xmax-xmin)/2)+xmin,
                           (incremento_vertical*nivel)+30)
        time.sleep(1)
        pygame.display.flip()

    def mostrar_arbol_grafico(self):
        ancho=1000
        alto=600
        self.VENTANA = pygame.display.set_mode((ancho, alto))
        pygame.display.set_caption("Despliegue de árbol")
        self.fuente = pygame.font.SysFont("Arial", 22)
        reloj = pygame.time.Clock()
        corriendo = True
        while corriendo:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    corriendo = False
            self.VENTANA.fill((255, 255, 255))
            incremento_vertical=((alto-30)/(self.altura))
            self.mostrar_nodos(self,0,ancho,incremento_vertical,0)
            pygame.display.flip()
            reloj.tick(60)
        pygame.quit()

    def insertar(self, elemento:any):
        valor=elemento
        if valor <= self.valor:
            if self.hijo_izquierda is None:
                self.hijo_izquierda = Arbol(valor)
            else:
                self.hijo_izquierda.insertar(valor)
        elif valor > self.valor:
            if self.hijo_derecha is None:
                self.hijo_derecha = Arbol(valor)
            else:
                self.hijo_derecha.insertar(valor)
        else:
            raise ValueError("El valor ya existe en el árbol")

    def insertar_nodo(self, nodo):
        nodo:Arbol=nodo
        if nodo.valor <= self.valor:
            if self.hijo_izquierda is None:
                self.hijo_izquierda = nodo
            else:
                self.hijo_izquierda.insertar_nodo(nodo)
        elif nodo.valor > self.valor:
            if self.hijo_derecha is None:
                self.hijo_derecha = nodo
            else:
                self.hijo_derecha.insertar_nodo(nodo)
        else:
            raise ValueError("El valor ya existe en el árbol")
    
    @property
    def hoja(self)->bool:
        return (self.hijo_derecha==None and self.hijo_izquierda==None) 

    def eliminar(self,valor:int):
        if self.valor==valor:
            if self.hijo_izquierda!=None:
                self.valor=self.hijo_izquierda.valor
                hizhiz=self.hijo_izquierda.hijo_izquierda
                hizhder=self.hijo_izquierda.hijo_derecha
                hder=self.hijo_derecha
                self.hijo_izquierda=hizhiz
                self.hijo_derecha=hizhder
                self.insertar_nodo(hder)
        elif valor<=self.valor and self.hijo_izquierda!=None:
            self.hijo_izquierda.eliminar(valor)
        elif valor>self.valor and self.hijo_derecha!=None:
            self.hijo_derecha.eliminar(valor)
    

    def imprimir(self, espaciado:str=""):
        print(espaciado,self.valor)
        if self.hijo_izquierda is not None:
            self.hijo_izquierda.imprimir(espaciado+"...")
        else:
            print(espaciado+"...(None)")
        if self.hijo_derecha is not None:
            self.hijo_derecha.imprimir(espaciado+"...")
        else:
            print(espaciado+"...(None)")
    
    def buscar(self, valor):
        if valor==self.valor:
            return (self)
        elif valor<=self.valor and self.hijo_izquierda!=None:
            return(self.hijo_izquierda.buscar(valor))
        elif self.hijo_derecha!=None:
            return(self.hijo_derecha.buscar(valor))
        else:
            return None

    @property
    def altura (self)->int:
        if self.hoja:
            return (1)
        else: 
            altura_hijo_iz=0
            altura_hijo_der=0
            if self.hijo_izquierda!=None:
                altura_hijo_iz=self.hijo_izquierda.altura
            if self.hijo_derecha!=None:
                altura_hijo_der=self.hijo_derecha.altura
            if altura_hijo_iz>=altura_hijo_der:
                return (altura_hijo_iz+1)
            else:
                return (altura_hijo_der+1)

    @property
    def ancho (self)->int:
        if self.hoja:
            return (1)
        else: 
            ancho_hijo_iz=0
            ancho_hijo_der=0
            if self.hijo_izquierda!=None:
                ancho_hijo_iz=self.hijo_izquierda.ancho
            if self.hijo_derecha!=None:
                ancho_hijo_der=self.hijo_derecha.ancho
            return (ancho_hijo_iz+ancho_hijo_der+1)
"""
    def mostrar_nodos(self, nodo, x, y, ancho):
        if nodo is not None:
            self.imprimir_nodo(nodo.valor, x, y)
            if nodo.hijo_izquierda is not None:
                pygame.draw.line(self.VENTANA, (0, 0, 0), (x, y), (x - ancho // 2, y + 70), 2)
                self.imprimir_nodo(nodo.valor, x, y)
                self.mostrar_nodos(nodo.hijo_izquierda, x - ancho // 2, y + 70, ancho // 2)
            if nodo.hijo_derecha is not None:
                pygame.draw.line(self.VENTANA, (0, 0, 0), (x, y), (x + ancho // 2, y + 70), 2)
                self.imprimir_nodo(nodo.valor, x, y)
                self.mostrar_nodos(nodo.hijo_derecha, x + ancho // 2, y + 70, ancho // 2)
"""
if __name__ == "__main__":
    import random as rd
    # Crear un árbol binario de búsqueda
    elementos=[10,5,15,-13,8,28,12,12,14,-2,4,-7,5,3]
    raiz = Arbol(elementos[0])
    for e in elementos[1:]:
        raiz.insertar(e)
    print("Altura = ",raiz.altura)
    print("Ancho = ",raiz.ancho)
    raiz.mostrar_arbol_grafico()
