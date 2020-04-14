import pygame, random,  pygame.mixer, time
from pygame.locals import *
from scripts.player import Player, Shot
from scripts.enemy import Enemy


class Game():
    def __init__(self):

        pygame.init() #inicializa o pygame

        self.game_start = True # variavel que comanda se o jogo comeca ou nao

        self.window_width = 1200 # largura da janela
        self.window_height = 600 # altura da janela

        self.window = pygame.display.set_mode((self.window_width, self.window_height)) # cria a janela passando a largura e a altura como parametros

        self.background = pygame.image.load("img/background.jpg") # pega a imagem de background
        self.background = pygame.transform.scale(self.background, (self.window_width, self.window_height)) # defini um width e um height para imagem do background

        # Player
        self.player_group = pygame.sprite.Group() # cria um grupo para o player
        self.player = Player() # cria o player
        self.player_group.add(self.player) # adiciona o player no grupo
        self.player_right = False # inicializa do a variavel de movimento FALSE
        self.player_left = False # inicializa do a variavel de movimento FALSE

        #Tiro
        self.shoot_group = pygame.sprite.Group() # cria o grupo dos tiros

        # Enemy
        self.create_enemy = True
        self.enemy_group = pygame.sprite.Group()


        # INFORMAÇÕES DOS PONTOS E LEVEL
        self.player_points = self.player.points
        self.font = pygame.font.Font("font/8bit.ttf", 30)
        self.points_text = self.font.render("SCORE: " + str(self.player_points), 1, (255,255,255))
        self.level = 0
        self.enemy_in_window = 5
        self.level_text = self.font.render("LEVEL: "+ str(self.level),1,(255,255,255))


        # MUSICA AMBIENTE
        pygame.mixer.init()
        pygame.mixer.set_reserved(0)
        self.game_music = pygame.mixer.Sound("sounds/game_music.wav")
        pygame.mixer.Channel(0).play(self.game_music,-1)


        # FPS
        self.fps = pygame.time.Clock() # joga olock dentro de uma variavel para controle de fps

        # LOOP PRINCIPAL
        self.game_init = True
        while self.game_init:
            self.fps.tick(30) # defini o fps do jogo
            for event in pygame.event.get(): # evento para os comandos do jogo
                if event.type == QUIT:
                    pygame.quit()

                if event.type == KEYDOWN: # quando a tecla estiver apertada
                    if event.key == K_RIGHT:
                        self.player_right = True
                    if event.key == K_LEFT:
                        self.player_left = True
                    if event.key == K_SPACE: # botao para atirar
                        self.player_shot = Shot() # pega a classe do tiro
                        self.player_shot.rect[0] = self.player.rect[0]+23 # passa a posicao inicial em x
                        self.player_shot.rect[1] = self.player.rect[1] # passa a posicao inicial em y
                        self.shoot_group.add(self.player_shot) # adiciona o tiro no grupo dos tiros
                        pygame.mixer.Channel(1).play(pygame.mixer.Sound("sounds/shot.wav")) # musica dos tiros


                if event.type == KEYUP: # quando soltar a tecla
                    if event.key == K_RIGHT:
                        self.player_right = False
                    if event.key == K_LEFT:
                        self.player_left = False

            if self.player_right: # se a condicao for verdadeira o player mexe para direita
                self.player.rect[0] += self.player.speed
            if self.player_left: # se a condicao for verdadeira o player mexe para esquerda
                self.player.rect[0] -= self.player.speed

            self.window.blit(self.background,(0,0)) # desenha o background
            self.window.blit(self.points_text,(850,10)) # texto do score
            self.window.blit(self.level_text,(650,10))
            self.shoot_group.update() # chama a funcao de update de todos que tiverem no grupo de tiros
            self.player_group.update() # chama a funcao update de todos que tiverem no grupo do  player
            self.player_group.draw(self.window) # desenha todo grupo do  player na tela
            self.enemy_group.update() # chama o update do grupo de inimigos
            self.enemy_group.draw(self.window) # desenha os inimigos na tela


            if len(self.enemy_group) <5: # se tiver menos que 5 inimigos , adiciona mais inimigo
                for i in range(5):
                    self.enemy = Enemy()
                    self.enemy_group.add(self.enemy)
                    print("adicionou mais um")

            if self.enemy.rect[1] > 600: # quando os inimigos chegarem a 700px da tela, eles são destruidos
                self.enemy_group.remove(self.enemy)
                print("saiu da tela")

            # VERIFICAÇÃO DE SCORE E LEVEL
            if self.player_points > 500:
                self.enemy.speed  = 2
                self.level = 1
                self.level_text = self.font.render("LEVEL: "+ str(self.level),1,(255,255,255))
            if self.player_points > 2000:
                self.enemy.speed  = 3
                self.level = 2
                self.level_text = self.font.render("LEVEL: "+ str(self.level),1,(255,255,255))
            if self.player_points > 4000:
                self.enemy.speed  = 4
                self.level = 3
                self.level_text = self.font.render("LEVEL: "+ str(self.level),1,(255,255,255))
            if self.player_points > 8000:
                self.enemy.speed  = 6
                self.level = 4
                self.level_text = self.font.render("LEVEL: "+ str(self.level),1,(255,255,255))
            if self.player_points > 10000:
                self.enemy.speed  = 8
                self.level = 5
                self.level_text = self.font.render("LEVEL: "+ str(self.level),1,(255,255,255))
            if self.player_points > 20000:
                self.enemy.speed  = 9
                self.level = 6
                self.level_text = self.font.render("LEVEL: "+ str(self.level),1,(255,255,255))
            if self.player_points > 50000:
                self.enemy.speed  = 12
                self.level = "FINAL LEVEL"
                self.level_text = self.font.render("LEVEL: "+ str(self.level),1,(255,255,255))


            for bullet in self.shoot_group: # para cada tiro que estiver no grupo de tiros
                self.shoot_group.draw(self.window) # desenha o tiro na tela
                if self.player_shot.rect[1]< -20: # verifica se a posicao y do tiro é menor que -20 , no caso se ja saiu da tela
                    self.shoot_group.remove(self.player_shot) # se a verificacao for verdadeira, entao ela elimina aquele tiro do grupo de tiros


            #VERIFICANDO AS COLISÕES
            if (pygame.sprite.groupcollide(self.shoot_group, self.enemy_group, True, True)):
                self.player_points += random.randint(1,10)
                self.points_text = self.font.render("SCORE: " + str(self.player_points), 1, (255,255,255))
                pygame.mixer.Channel(2).play(pygame.mixer.Sound("sounds/enemy_death.wav")) # musica da morte do inimigo


            if (pygame.sprite.groupcollide(self.player_group, self.enemy_group, True, False)):
                    Game()
                    self.game_init = False




            pygame.display.update()
Game()
