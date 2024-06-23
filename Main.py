import pygame as pg
import sys
import math 
from Recursos import Constantes as con
from Recursos import Colores
from Recursos import Clases
from Recursos import Funciones as func

def Main():
    pg.init()

    #display
    pantalla=pg.display.set_mode(con.TAMAÑO_PANTALLA)
    reloj=pg.time.Clock()
    pg.display.set_caption("El último en pie")
    imagenBackground = pg.image.load(".\\Sprites\\BG redimencionado.png").convert()
    #display

    #utilidades
    timer = pg.time.Clock()
    ultimoSpawn = pg.time.get_ticks()
    enemigosSpawneados = 0
    listaTipoEnemigosParaSpawn = []
    listaEnemigos = []
    #utilidades



    #objects
    bullets = pg.sprite.Group()
    character = Clases.Character(100,con.SUELO_Y,100)
    weapon = Clases.Weapon(character)
    suelo = Clases.Map(".\\Sprites\\BG Suelo.png", [800,22])
    suelo.rect.y = con.SUELO_Y 
    barrera = Clases.Map(None,[147,93], 100)
    # zombie1 = Clases.Zombie("debil",700,con.SUELO_Y,100) instancia manual de enemigo

    barrierHealthBar = Clases.HealthBar(barrera)
    characterHealthbar = Clases.HealthBar(character)
    # enemies.append(zombie1)append manual de enemigo
    #objects
    
    #listaSprites
    objetos = pg.sprite.pygame.sprite.Group()
    objetos.add(character)
    objetos.add(suelo)
    objetos.add(barrera)
    # objetos.add(enemies) añadir manual al enemigo

    #####################
    #  Spawn automatico #
    #####################
    func.ProcessEnemigos(1, listaTipoEnemigosParaSpawn)
    objetos.add(weapon)
    #listaSprites


    #ejecución

    ejecutar = True
    while ejecutar:
        eventos = pg.event.get()
        for evento in eventos:
            if evento.type == pg.QUIT:
                ejecutar = False
        for evento in eventos:
            if evento.type == pg.MOUSEBUTTONDOWN:
                if evento.button == 1:  
                    character.isShooting = True
                    bullet = func.CheckShooting(character, weapon)
                    if bullet:
                        bullets.add(bullet)
            elif evento.type == pg.MOUSEBUTTONUP:  
                if evento.button == 1: 
                    character.isShooting = False
            

        pantalla.fill(Colores.CELESTE)
        pantalla.blit(imagenBackground,(0,0))
        reloj.tick(30)
        timer = pg.time.get_ticks()

        #####################
        #       UPDATES     #
        #      Funciones    #
        #####################

        character.update()
        weapon.update()
        func.CheckCollider(character, barrera)
        
        func.CheckBulletCollider(listaEnemigos, bullets)  
        func.CheckBarrierHP(barrera, objetos)
        bullets.update()
        objetos.update()
        barrera.update()  

        ######################
        #       DRAWS        #
        ######################

        #spawn de enemigos
        if pg.time.get_ticks() - ultimoSpawn > con.cooldownEnemigos:
            if enemigosSpawneados < len(listaTipoEnemigosParaSpawn): #OJO CON ESTO. Largo del diccionario ok?
                tipoEnemigo = listaTipoEnemigosParaSpawn[enemigosSpawneados] 
                nuevoEnemigo = Clases.Zombie(tipoEnemigo)
                listaEnemigos.append(nuevoEnemigo)
                enemigosSpawneados += 1
                ultimoSpawn = pg.time.get_ticks()
            objetos.add(listaEnemigos)


        #esta func la muevo acá por el tipo de la lista "enemies", si no, la toma como tipo int, porque no agregué nada antes
        func.CheckColliderEnemy(listaEnemigos, barrera, character, timer)
        for i in range(enemigosSpawneados):
             if i < len(listaEnemigos):
                enemyHealthBar = Clases.HealthBar(listaEnemigos[i])
                enemyHealthBar.draw(pantalla)
        
        bullets.draw(pantalla)  
        #barrierHealthBar.draw(pantalla) menjor sin hb
        characterHealthbar.draw(pantalla)  
        objetos.draw(pantalla) 
        

        
            
        pg.display.flip()




    #ejecución

    pg.quit()
    sys.exit()


if __name__ == "__main__":
    Main()