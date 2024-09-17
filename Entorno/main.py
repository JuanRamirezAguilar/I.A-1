# Librerias
import pygame
import random

# Clase aspiradora
class Aspiradora:
    # Constructor de la aspiradora
    def __init__(self, coord_x, coord_y, entorno) -> None:
        self.coord_x = coord_x
        self.coord_y = coord_y
        self.entorno = entorno

    # Direcciones posibles en que la aspiradora puede moverse en el entorno
    def mover(self, direccion) -> None:
        if direccion == "UP" and self.coord_y > 0:
            self.coord_y -= 1
        elif direccion == "DOWN" and self.coord_y < 4:
            self.coord_y += 1
        elif direccion == "LEFT" and self.coord_x > 0:
            self.coord_x -= 1
        elif direccion == "RIGHT" and self.coord_x < 4:
            self.coord_x += 1

    # Accion de la aspiradora para limpiar una casilla
    def limpiar(self) -> bool:
        if self.entorno[self.coord_y][self.coord_x] == "sucia":
            self.entorno[self.coord_y][self.coord_x] = "limpia"
            return True
        return False
    

# Clase entorno
class Entorno:
    # Constructor del entorno
    def __init__(self) -> None:
        self.celdas = [["limpia" for _ in range(5)] for _ in range(5)]
        self.generar_suciedad()

    # Funcion que genera el estado suciedad dentro del entorno
    def generar_suciedad(self) -> None:
        for i in range(random.randint(5, 10)): # Se van a generar la suciedad de 5 a 10
            x = random.randint(0, 4)
            y = random.randint(0, 4)
            self.celdas[x][y] = "sucia"


def main() -> None:
    pygame.init()

    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    ANCHO_VENTANA = 500
    ALTO_VENTANA = 500
    RESOLUCION = (ALTO_VENTANA, ANCHO_VENTANA)
    TAMANO_CELDA = 100

    pantalla = pygame.display.set_mode(RESOLUCION)
    pygame.display.set_caption("Entorno de aspiradora")

    # Generamos el entorno y la aspiradora
    entorno = Entorno()
    aspiradora = Aspiradora(0, 0, entorno.celdas)

    # Contadores del entorno
    contador_basura = 0
    contador_movimientos = 0

    # Cargamos la imagen de la basura y de la aspiradora
    basura_img = pygame.image.load("src/compost.png")
    asp_img = pygame.image.load("src/aspiradora.png")
    # Escalamos las imagenes
    basura_img = pygame.transform.scale(basura_img, (TAMANO_CELDA - 50, TAMANO_CELDA - 50))
    asp_img = pygame.transform.scale(asp_img, (TAMANO_CELDA - 50, TAMANO_CELDA - 50))

    run = True
    while run:
        """Eventos del programa, tales como entradas de inputs
           En este caso son las teclas de movimiento y la barra espaciadora"""
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                run = False
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_UP:
                    aspiradora.mover("UP")
                elif evento.key == pygame.K_DOWN:
                    aspiradora.mover("DOWN")
                elif evento.key == pygame.K_LEFT:
                    aspiradora.mover("LEFT")
                elif evento.key == pygame.K_RIGHT:
                    aspiradora.mover("RIGHT")
                elif evento.key == pygame.K_SPACE:
                    # En caso de que limpie una suciedad, se incrementa en 1 el contador
                    if aspiradora.limpiar():
                        contador_basura += 1
                        print(f"Numero de Basuras recogidas: {contador_basura}")
                        
            if evento.type == pygame.KEYDOWN and evento.key != pygame.K_SPACE:
                # Si detecta un movimiento:
                contador_movimientos += 1
                print(f"Numero de movimientos de la aspiradora: {contador_movimientos}")

        pantalla.fill(WHITE)

        

        # Dibujamos el entorno
        for fila in range(5):
            for columna in range(5):
                x = columna * TAMANO_CELDA
                y = fila * TAMANO_CELDA
                color = WHITE 
                if entorno.celdas[fila][columna] == "sucia":
                    # Coordenadas de la basura
                    x_celda = columna * TAMANO_CELDA
                    y_celda = fila * TAMANO_CELDA
                    
                    
                    # Centramos la imagen
                    img_ancho, img_alto = basura_img.get_size()  # Obtener tamaño de la imagen

                    # Calcular el desplazamiento para centrar la imagen dentro de la celda
                    x_centrada = x_celda + (TAMANO_CELDA - img_ancho) // 2
                    y_centrada = y_celda + (TAMANO_CELDA - img_alto) // 2

                    # Dibujamos la imagen
                    pantalla.blit(basura_img, (x_centrada, y_centrada))
                    pygame.draw.rect(pantalla, BLACK, (x, y, TAMANO_CELDA, TAMANO_CELDA), 1)
                else:
                    pygame.draw.rect(pantalla, color, (x, y, TAMANO_CELDA, TAMANO_CELDA))
                    pygame.draw.rect(pantalla, BLACK, (x, y, TAMANO_CELDA, TAMANO_CELDA), 1)

        # Dibujar las aspiradora
        x_celda = aspiradora.coord_x * TAMANO_CELDA
        y_celda = aspiradora.coord_y * TAMANO_CELDA

        # Centrar la imagen en la primera celda (0,0)
        img_ancho, img_alto = asp_img.get_size()  # Obtener tamaño de la imagen

        # Calcular el desplazamiento para centrar la imagen dentro de la celda
        x_centrada = x_celda + (TAMANO_CELDA - img_ancho) // 2
        y_centrada = y_celda + (TAMANO_CELDA - img_alto) // 2

        # Dibujar la imagen centrada
        pantalla.blit(asp_img, (x_centrada, y_centrada))

        pygame.display.flip()

    pygame.quit()



if __name__ == "__main__":
    main()