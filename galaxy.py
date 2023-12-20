import pygame, random

width = 800
height = 600
black = (0,0,0)
white = (255,255,255)
green = (0,255,0)
score = 0

pygame.init()
pygame.mixer.init() #se usa para que pygame pueda producir sonidos
screen = pygame.display.set_mode((width, height)) #seteamos el display de la pantalla con las dimensiones
pygame.display.set_caption("GalaxyAttack") #seteamos el titulo de la ventana
clock = pygame.time.Clock() #se usa para controlar la velocidad de los frames con la funcion tick()

def draw_text(surf, text, size, x, y): #surf es la superficie donde se dibuja el texto
    font = pygame.font.Font(pygame.font.match_font('arial'), size) #seleccionamos la fuente
    text_surface = font.render(text, True, white) #renderizamos el texto el true es para que se vea suave el texto
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y) #posicionamos el rectangulo en el centro superior
    surf.blit(text_surface, text_rect) #dibujamos el texto

def draw_shield_bar(surf, x, y, pct): #pct es el porcentaje de la barra
    if pct < 0: #si el escudo es menor a 0 lo seteamos a 0
        pct = 0
    bar_length = 100 #longitud de la barra
    bar_height = 10 #altura de la barra
    fill = (pct / 100) * bar_length #llenado de la barra
    outline_rect = pygame.Rect(x, y, bar_length, bar_height) #rectangulo de la barra
    fill_rect = pygame.Rect(x, y, fill, bar_height) #rectangulo del llenado de la barra
    pygame.draw.rect(surf, green, fill_rect) #dibujamos el llenado de la barra
    pygame.draw.rect(surf, white, outline_rect, 2) #dibujamos el rectangulo de la barra

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.image = pygame.image.load("./assets/player.png").convert()  #cargamos la imagen del jugador
        self.image.set_colorkey(black) #removemos la parte negra de la imagen (el borde)
        self.rect = self.image.get_rect() #obtenemos el rectangulo de la imagen
        self.rect.centerx = width / 2 #centramos el rectangulo en el eje x
        self.rect.bottom = height - 10 #posicionamos el rectangulo en el borde inferior de la pantalla
        self.speed_x = 0 #velocidad en el eje x
        self.shield = 100 #escudo del jugador
    
    def update(self):
        self.speed_x=0
        keystate = pygame.key.get_pressed() #obtenemos el estado del teclado
        if keystate[pygame.K_LEFT]:
            self.speed_x = -5
        if keystate[pygame.K_RIGHT]:
            self.speed_x = 5
        self.rect.x += self.speed_x
        if self.rect.right > width:
            self.rect.right = width
        if self.rect.left < 0:
            self.rect.left = 0
    
    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)
        laser_sound.play() #reproducimos el sonido de la bala 


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = random.choice(enemy_images) #seleccionamos una imagen de la lista de imagenes de enemigos
        self.image.set_colorkey(black) 
        self.rect = self.image.get_rect() #obtenemos el rectangulo de la imagen
        self.rect.x = random.randrange(width - self.rect.width) #posicionamos el enemigo en el eje x
        self.rect.y = random.randrange(-140, -100) #posicionamos el enemigo arriba de la pantalla 
        self.speed_y = random.randrange(1, 10) #velocidad en el eje y
        self.speed_x = random.randrange(-5, 5) #velocidad en el eje x

    def update(self):
        self.rect.y += self.speed_y #movemos el enemigo en el eje y
        self.rect.x += self.speed_x #movemos el enemigo en el eje x
        if self.rect.top > height + 10 or self.rect.left < -40 or self.rect.right > width + 40: #si el enemigo sale de la pantalla lo reposicionamos arriba
            self.rect.x = random.randrange(width - self.rect.width) 
            self.rect.y = random.randrange(-100, -40) 
            self.speed_y = random.randrange(1, 10) 


class Bullet(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.image = pygame.image.load("./assets/laser1.png").convert()
        self.image.set_colorkey(black) 
        self.rect = self.image.get_rect() #obtenemos el rectangulo de la imagen
        self.rect.centerx = x
        self.rect.y = y
        self.speed_y = -10 #velocidad en el eje y

    def update(self):
        self.rect.y += self.speed_y #movemos el enemigo en el eje y
        if self.rect.bottom < 0: #si la bala sale de la pantalla la eliminamos
            self.kill() #eliminamos todas las instancias de la bala de todas las listas

class Explosion(pygame.sprite.Sprite):
    def __init__(self, center):
        super().__init__()
        self.image = explosion_anim[0]
        self.rect = self.image.get_rect()
        self.rect.center = center #centramos el rectangulo
        self.frame = 0 #frame de la animacion
        self.last_update = pygame.time.get_ticks() #tiempo transcurrido desde que se inicio el juego
        self.frame_rate = 50 #velocidad de la animacion
    
    def update(self):
        now = pygame.time.get_ticks() #tiempo transcurrido desde que se inicio el juego
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion_anim): #si el frame es igual a la longitud de la lista de imagenes de la explosion lo eliminamos de todas las listas 
                self.kill()
            else:
                center = self.rect.center #centro del rectangulo
                self.image = explosion_anim[self.frame] #cambiamos la imagen de la explosion
                self.rect = self.image.get_rect() #obtenemos el rectangulo de la imagen
                self.rect.center = center #centramos el rectangulo en el eje x

def show_go_screen(): #muestra el MENU DE INICIO
    screen.blit(background, [0, 0]) #dibujamos el fondo
    draw_text(screen, "GalaxyAttack", 64, width / 2, height / 4) #dibujamos el titulo
    #quiero mostrar el score que logro el jugador
    draw_text(screen, "Score: " + str(score), 22, width / 2, height / 2.5) #dibujamos el puntaje
    draw_text(screen, "Arrow keys to move, Space to fire", 22, width / 2, height / 2) #dibujamos las instrucciones
    draw_text(screen, "Press a key to play", 18, width / 2, height * 3 / 4) #dibujamos las instrucciones
    pygame.display.flip() #actualizamos la pantalla
    waiting = True
    while waiting:
        clock.tick(60) # 60 FPS
        for event in pygame.event.get():
            if event.type == pygame.QUIT: #si se presiona la X de la ventana se cierra el juego
                pygame.quit()
            if event.type == pygame.KEYUP:
                waiting = False

enemy_images = [] #lista de imagenes de enemigos
enemy_list = ["assets/meteorGrey_big1.png", "assets/meteorGrey_big2.png", "assets/meteorGrey_big3.png", "assets/meteorGrey_big4.png",
				"assets/meteorGrey_med1.png", "assets/meteorGrey_med2.png", "assets/meteorGrey_small1.png", "assets/meteorGrey_small2.png",
				"assets/meteorGrey_tiny1.png", "assets/meteorGrey_tiny2.png"] #lista de enemigos

for img in enemy_list:
    enemy_images.append(pygame.image.load(img).convert()) #cargamos las imagenes de los enemigos

#explosion de los meteoros
explosion_anim = [] #lista de imagenes de la explosion
for i in range(9):
    filename = 'assets/regularExplosion0{}.png'.format(i) #nombre de las imagenes de la explosion 
    img = pygame.image.load(filename).convert()
    img.set_colorkey(black)
    img_scale = pygame.transform.scale(img, (70, 70)) #escalamos la imagen
    explosion_anim.append(img_scale) #agregamos la imagen a la lista

#Cargar imagen de fondo
background = pygame.image.load("./assets/background.png").convert() #cargamos la imagen de fondo
#Cargar sonidos
laser_sound = pygame.mixer.Sound("./assets/laser5.ogg") #cargamos el sonido de la bala
explosion_sound = pygame.mixer.Sound("./assets/explosion.wav") #cargamos el sonido de la explosion
music = pygame.mixer.music.load("./assets/music.ogg") #cargamos la musica de fondo


pygame.mixer.music.play(loops=-1) #reproducimos la musica de fondo
game_over = True
running = True
while running:
    if game_over:

        show_go_screen() #mostramos la pantalla de inicio

        game_over = False
        all_sprites = pygame.sprite.Group() #grupo de sprites
        enemy_list = pygame.sprite.Group() #grupo de enemigos
        bullets = pygame.sprite.Group() #grupo de balas

        player = Player() 
        all_sprites.add(player) #se agrega el jugador al grupo de sprites
        for i in range(8):
            enemy = Enemy()
            all_sprites.add(enemy) #se agrega el enemigo al grupo de sprites
            enemy_list.add(enemy) #se agrega el enemigo al grupo de enemigos

        score = 0

    clock.tick(60) # 60 FPS
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: #si se presiona la X de la ventana se cierra el juego
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()

    #colisiones meteoro laser
    hits = pygame.sprite.groupcollide(enemy_list, bullets, True, True) #si un enemigo colisiona con una bala
    for hit in hits: #por cada enemigo que colisiona con una bala
        score+=10 #sumamos 10 puntos al puntaje
        enemy = Enemy()  
        all_sprites.add(enemy) #se agrega el enemigo al grupo de sprites
        enemy_list.add(enemy) #se agrega el enemigo al grupo de enemigos
        explosion_sound.play()
        explosion_sound.set_volume(0.2)
        explosion = Explosion(hit.rect.center) #creamos una explosion y pasamos por parametro el centro del rectangulo del enemigo 
        all_sprites.add(explosion) #se agrega la explosion al grupo de sprites


    #colisiones meteoro jugador
    hits = pygame.sprite.spritecollide(player, enemy_list, True) #si el jugador colisiona con un enemigo
    if hits:
        player.shield -= 25
        if player.shield <= 0:
            game_over = True

    all_sprites.update() #actualizamos todos los sprites
    screen.blit(background, [0, 0]) #dibujamos el fondo
    all_sprites.draw(screen) #dibujamos todos los sprites
    draw_text(screen, str(score), 25, width // 2, 10) #dibujamos el puntaje
    draw_shield_bar(screen, 5, 5, player.shield) #dibujamos la barra de escudo
    pygame.display.flip() #actualizamos la pantalla

pygame.quit() #cerramos pygame