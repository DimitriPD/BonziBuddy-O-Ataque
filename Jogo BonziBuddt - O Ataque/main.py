import pygame
import os
import random

pygame.init()

level1 = [
    '                                                                                                                                ',
    '                                                      A                                                                         ',
    '                                                                                                                                ',
    '                          A                                                                                  XXX        M       ',
    '    M                                       XXXXXXXX                                     M                            XXX     A ',
    '   XX                 M             M                                  XX  XXXX A XXX   XXX            XXXX       X        XXXX ',
    '                  XXXXXXXXXX    XXXXXXXXX                                              A                                        ',
    '      A                                                           M                          M      A                           ',
    '                                                         A   XXXXXXXX                     XXXXX    XXX                          ',
    '            XXXX                                                                                                             M  ',
    '       XX                                   A        M                                                     A                XXXX',
    '  M                                      XXXXX    XXXXXXXX                                               XXXXX    M             ',
    '  XX              XXXX                                                                            A               X             ',
    '                           A    M                                    M            M  A           XXX                            ',
    '                         XXXXXXXXXXXXX               M             XXXXXX      XXXXXXXX                                         ',
    '                                                     X                                                                     A    ',
    '                                        XXX                                 A                                            XXXX   ',
    '                M                                            M              X                                                   ',
    '     M          X                             XXXX           X                                              M                   ',
    '    XX                                                                                                    XXXXXX                ',
    '                                                      XXXX             XXXX                                                     ',
    '                             M                                                                                                  ',
    '         XX                XXXXX                 A                             XXXX                A                       L    ',
    '            A                     A                       XXXXXX                            M                            XXXXX  ',
    ' C                   M                      M                           M   A           XXXXXXXXX    XXXX                       ',
    'XXXX  XXXX       XXXXXXXX          XXXX   XXXXXXX   XXX                 XXXXXXXXXX                           XXXXXXXX           '
]

level2 = [
    '                                      ',
    '                                      ',
    '                                      ',
    '                                      ',
    '                                      ',
    '                                      ',
    '                 B                    ',
    '                                      ',
    '                                      ',
    '                                      ',
    '                                      ',
    '                                      ',
    '                                      ',
    '                                      ',
    '                                      ',
    '                                      ',
    '                                      ',
    '                                      ',
    '                                      ',
    '                                      ',
    '                                      ',
    '                                      ',
    '                                      ',
    '                 C                    ',
    '                                      ',
    '                                      '
]
print(len(level2[0]))


tamanho_bloco = 32
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = len(level1) * tamanho_bloco
# 38 X 23 - BLOCO DE 32

tela = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Bonzi Buddy: O Ataque")
icone = pygame.image.load('imgs/inimigo/atirando/atirando_6.png')
pygame.display.set_icon(icone)

FUNDOXP = pygame.image.load("imgs/bg_image/fundoXP.png").convert()
FUNDOXP = pygame.transform.scale(FUNDOXP, (SCREEN_WIDTH, SCREEN_HEIGHT))

TELA_FINAL = pygame.image.load("imgs/bg_image/tela_final.png").convert_alpha()
TELA_FINAL = pygame.transform.scale(TELA_FINAL, (SCREEN_WIDTH, SCREEN_HEIGHT))

TAREFAS = pygame.image.load("imgs/bg_image/barra_tarefas.png").convert_alpha()
TAREFAS = pygame.transform.scale(TAREFAS, (SCREEN_WIDTH, 35))

start_game = False
comecar = False

tela_scroll = 0
bg_scroll = 0

fonte = pygame.font.SysFont('Futura', 30)
fonteTemp = pygame.font.SysFont('Futura', 15)
fonteFala = pygame.font.SysFont('Futura', 40)


def desenha_texto(texto, fonte, cor, x, y):
    img = fonte.render(texto, True, cor)
    tela.blit(img, (x,y))

def desenha_BG():
    tela.fill('black')
    tela.blit(FUNDOXP, (0,0))
    tela.blit(TAREFAS, (0, SCREEN_HEIGHT - 32))
    

def restart_level():
    for mac in macacos_grupo.sprites():
        mac.bala.empty()
    macacos_grupo.empty()
    balas_grupo_macaco.empty()
    bloco.empty()
    arquivos.empty()
    power_up_grupo.empty()
    cursor.balas.empty()    
    lixeira.empty()
    clip_group.empty()    

fps = pygame.time.Clock()
FPS = 60

lixeira = pygame.sprite.GroupSingle()

macacos_grupo = pygame.sprite.Group()
balas_grupo_macaco = pygame.sprite.Group()

bloco = pygame.sprite.Group()
arquivos = pygame.sprite.Group()

clip = pygame.sprite.GroupSingle()

pp_vida = pygame.image.load("imgs/power_ups/vida.png").convert_alpha()
pp_vida = pygame.transform.scale(pp_vida, (int(pp_vida.get_width() * 0.05), int(pp_vida.get_height() * 0.05)))

pp_municao = pygame.image.load("imgs/power_ups/municao.png").convert_alpha()
pp_municao = pygame.transform.scale(pp_municao, (int(pp_municao.get_width() * 0.05), int(pp_municao.get_height() * 0.05)))

pp_ivencibilidade = pygame.image.load("imgs/power_ups/ivencibilidade.png").convert_alpha()
pp_ivencibilidade = pygame.transform.scale(pp_ivencibilidade, (int(pp_ivencibilidade.get_width() * 0.05), int(pp_ivencibilidade.get_height() * 0.05)))

# Globais
toma_dano = True

power_up = {
    'vida' : pp_vida,
    'municao' : pp_municao,
    'invencibilidade' : pp_ivencibilidade
}
power_up_grupo = pygame.sprite.Group()

class Mundo():
    def __init__(self, level):
        self.largura = len(level[0])
        self.level = level

    def gera_nivel(self):
        for indice_y, linha in enumerate(self.level):
            for indice_x, obj in enumerate(linha):
                x = indice_x * tamanho_bloco
                y = indice_y * tamanho_bloco
                if obj == 'X': # Chao
                    if x >= 35 and y == 22:
                        chao = Bloco(x=x, y=y + (tamanho_bloco / 2) * 2, larg=tamanho_bloco, alt= tamanho_bloco)
                    else:
                        chao = Bloco(x=x, y=y, larg=tamanho_bloco, alt= tamanho_bloco / 2)
                    bloco.add(chao)

                elif obj == 'C': # Cursor / Player
                    cursor = Cursor(x=x, y=y, scale=1, speed=6, municao=20)
                    barra_vida = Barra_Vida(200, SCREEN_HEIGHT - 28, cursor.vida, cursor.vidaMaxima, 220)
                
                elif obj == 'M': # Macaco / Inimigo
                    pos = (x,y)
                    macaco = Macaco(pos=pos, scale=1)
                    macacos_grupo.add(macaco)
                
                elif obj == 'A': # Arquivos
                    arquivo = Arquivo(x, y, 20, 20)
                    arquivos.add(arquivo)

                elif obj == 'L': #Lixeira
                    lix = Lixeira(x, y, 1)
                    lixeira.add(lix)

                elif obj == 'B': #Clip_Scene Boss
                    c = Clip_boss(x=x, y=y, scale=.4)
                    clip.add(c)
                
        barra_clip = Barra_Vida(200, 10, 300, 300, 800)    
        return cursor, barra_vida, barra_clip
    

class Cursor(pygame.sprite.Sprite):
    def __init__(self, x, y, scale=1, speed=0, municao=0):
        pygame.sprite.Sprite.__init__(self) 
        self.scale = scale
        img = pygame.image.load('imgs/player/sprite/spr_0.png').convert_alpha()
    
        self.image = img
        self.image = pygame.transform.scale(img, (int(img.get_width() * self.scale), int(img.get_height() * self.scale)))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        self.speed = speed
        self.direcao = pygame.math.Vector2(0,0)
        self.width = self.image.get_width()
        self.height = self.image.get_height()

        self.grav = 0.5
        self.jump = False
        self.jspd = -16
        self.qnt_pulo = 1
        self.noChao = False

        self.atirar = False
        self.balas = pygame.sprite.Group()
        self.municao = municao
        self.timer = 0

        self.ivenc = 0
        self.coletados = 0

        self.boss = False

        self.vivo = True
        self.vida = 100
        self.vidaMaxima = 100

        self.flip = True

    def gravidade(self):
        if self.rect.y - 2 <= 0:
            self.direcao.y = 0

        if self.direcao.y >= 8:
            self.grav = 0
        else:
            self.grav = 1.2
        
        if self.direcao.y <= -16:
            self.jspd = 0
        else:
            self.jspd = -16
        
        self.direcao.y += self.grav

        self.rect.y += self.direcao.y

    def move(self):
        tela_scroll = 0
        dx = 0
        tecla = pygame.key.get_pressed()

        self.moving_left = tecla[pygame.K_a]  
        self.moving_right = tecla[pygame.K_d]

        if self.moving_left:
            dx = -self.speed
            self.flip = False
            self.direcao.x = - 1 
        if self.moving_right:
            dx = self.speed
            self.flip = True
            self.direcao.x = 1

        if self.rect.left + dx <= 0 or self.rect.right + dx >= SCREEN_WIDTH:
            dx = 0


        # Colisao Horizontal
        for tile in bloco.sprites():
            if tile.rect.colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                dx = 0

        level_complete = False
        if pygame.sprite.spritecollide(self, lixeira, False):
            if self.coletados >= arq_menu_quant:
                level_complete = True
                dx = 0

        self.rect.x += dx

        if self.rect.bottom > SCREEN_HEIGHT:
            self.vida = 0

        # Tela se move
        if (self.rect.right > SCREEN_WIDTH - SCREEN_WIDTH / 5 and bg_scroll < (mundo.largura * tamanho_bloco) - SCREEN_WIDTH) or (self.rect.left < SCREEN_WIDTH / 5 and bg_scroll > (dx)):
            self.rect.x -= dx
            tela_scroll = -dx

        if self.boss == True:
            v_move = -tecla[pygame.K_w] + tecla[pygame.K_s]
            self.rect.y += v_move * self.speed
        else:
            if tecla[pygame.K_w] and cursor.qnt_pulo > 0:                
                cursor.pulo()  
                     
        if self.noChao:
            self.qnt_pulo = 1 

        return tela_scroll, level_complete


    def pulo(self):
        self.qnt_pulo -= 1

        if self.qnt_pulo < 0:
            self.qnt_pulo = 0
        self.direcao.y += self.jspd
        self.rect.y += self.direcao.y

    def colisao_vertical(self):
        self.gravidade()

        for tile in bloco.sprites():
            if tile.rect.colliderect(self.rect):
                if self.direcao.y > 0:
                    self.rect.bottom = tile.rect.top
                    self.direcao.y = 0
                    self.noChao = True
                elif self.direcao.y < 0:
                    self.rect.top = tile.rect.bottom
                    self.direcao.y = 0

        if self.noChao and self.direcao.y < 0 or self.direcao.y > 1:
            self.noChao = False

    
    def atirando(self):
        if self.atirar and self.timer == 0 and self.municao > 0:
            tiro = Tiro_tintas(self.rect.centerx, self.rect.centery - (0.6 * self.rect.size[1]), self.direcao.x)
            self.balas.add(tiro)
            self.timer = 20
            self.municao -= 1
        else:
            if self.timer > 0:
                self.timer -= 1
        
    def invencivel(self):
        global toma_dano
        if toma_dano == False:
            self.ivenc -= 0.03
            desenha_texto(f"{self.ivenc:.0f}", fonteTemp, (255,255,0), self.rect.x + 20, self.rect.y + 20)

        if self.ivenc <= 1:
            self.ivenc = 0
            toma_dano = True

    def esta_vivo(self):
        if self.vida <= 0:
            self.vida = 0
            self.speed = 0
            self.vivo = False
            print('morri')


    def desenhar(self):
        tela.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)
        # pygame.draw.rect(tela, (255,0,0), self.rect, 1)
        cursor.image = pygame.image.load('imgs/player/sprite/spr_0.png')
        
    def update(self):
        self.esta_vivo()
        self.desenhar()

        self.atirando()
        self.balas.draw(tela)
        self.balas.update()

        if self.boss == False: 
            self.colisao_vertical()
            self.invencivel()
 

class Barra_Vida():
    def __init__(self, x, y, vida, vidaMax, larg):
        self.x = x
        self.y = y
        self.vida = vida
        self.vidaMax = vidaMax
        self.larg = larg

    def draw(self, vida):
        self.vida = vida
        razao = self.vida / self.vidaMax

        pygame.draw.rect(tela, (0,0,0), (self.x - 1, self.y - 1, self.larg + 2, 27))
        pygame.draw.rect(tela, (255,0,0), (self.x, self.y, self.larg, 25))
        pygame.draw.rect(tela, (0,255,0), (self.x, self.y, self.larg * razao, 25))


class Poderes(pygame.sprite.Sprite):
    def __init__(self, tipo_item, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.tipo_item = tipo_item
        self.image = power_up[self.tipo_item]
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)

    def colide_cursor(self):
        if pygame.sprite.collide_rect(self, cursor):
            if self.tipo_item == 'vida':
                desenha_texto("+40", fonte, (0,255,0), self.rect.x +10, self.rect.y-10)
                cursor.vida += 40
                if cursor.vida > cursor.vidaMaxima:
                    cursor.vida = cursor.vidaMaxima
            elif self.tipo_item == 'municao':
                desenha_texto("+10", fonte, (0,0,255), self.rect.x +10, self.rect.y-10)
                cursor.municao += 10
            elif self.tipo_item == 'invencibilidade':
                global toma_dano 
                cursor.ivenc += 15
                toma_dano = False
            self.kill()

    def update(self):
        self.rect.x += tela_scroll
        # pygame.draw.rect(tela, (0,0,0), self.rect, 1)
        self.colide_cursor()


class Tiro_tintas(pygame.sprite.Sprite):
    def __init__(self, x, y, direcao=1):
        pygame.sprite.Sprite.__init__(self)

        self.speed = 6
        self.direcao = direcao

        self.cores = ['blue', 'red', 'purple', 'orange', 'green']
        self.image = pygame.Surface((8,8))
        self.image.fill(random.choice(self.cores))

        self.rect = self.image.get_rect()
        self.rect.center = (x,y)

        self.alcance = 10

        self.update_time = pygame.time.get_ticks()

    def colisoes(self):
        for macaco in macacos_grupo.sprites():
            if pygame.sprite.spritecollide(macaco, cursor.balas, True):
                if macaco.vivo:
                    desenha_texto('-35', fonte, (255,0,0), macaco.rect.x + 20, macaco.rect.y - 10)
                    macaco.vida -= 35
                    self.kill()
                else:
                    self.kill()

        for bala in balas_grupo_macaco.sprites():
            if pygame.sprite.spritecollide(bala, cursor.balas, True):
                self.kill()
                bala.kill()

        for tile in bloco.sprites():
            if pygame.sprite.spritecollide(tile, cursor.balas, True):
                self.kill()

        if  mundo.level == level2:
            if pygame.sprite.collide_rect(self, clip.sprite):
                self.kill()
                clip.sprite.vida -= 10

    def update(self):
        pygame.draw.rect(tela, (0,0,0), self.rect, 1)

        if cursor.boss == False:
            self.rect.x += (self.direcao * self.speed)
        else:
            self.rect.y += (-1 * self.speed)
        self.colisoes()
        
        if self.rect.x > SCREEN_WIDTH or self.rect.x < 0:
            self.kill()
            print("morri")

        if cursor.boss == False:
            if self.alcance < 0:
                self.kill()
            
            self.alcance -= 0.2
        

class Macaco(pygame.sprite.Sprite):
    def __init__(self, pos, scale=1, speed=0):
        pygame.sprite.Sprite.__init__(self)
        
        self.scale = scale  
        self.sprite_index = 0
        self.acao = 0
        self.delay = 90
        self.update_time = pygame.time.get_ticks()
        
        self.animation_list = []
        self.carregarImgs()
        self.image = self.animation_list[self.acao][self.sprite_index]
        self.rect = self.image.get_rect()
        self.rect.center = (pos[0], pos[1] - (self.rect.size[1] / 5.5))

        self.atirar = False
        self.bala = pygame.sprite.Group()

        self.speed = speed
        self.flip = False

        self.vivo = True
        self.vida = 100
        

    def carregarImgs(self):
        tipos_animacao = ['parado', 'pulando', 'atirando']
        for animacao in tipos_animacao:
            lista_temp = []

            #Contando numeros de arquivos em uma pasta
            num_frames = len(os.listdir(f'imgs/inimigo/{animacao}'))
            for i in range(num_frames):
                img = pygame.image.load(f'imgs/inimigo/{animacao}/{animacao}_{i}.png').convert_alpha()
                img = pygame.transform.scale(img, (int(img.get_width() * self.scale), int(img.get_height() * self.scale)))
                lista_temp.append(img)
            self.animation_list.append(lista_temp)

    def atualiza_animacao(self):
        DELAY_ANIMACAO = self.delay
        escolha = random.choice(['sim', 'nao'])


        if self.acao > 2:
            self.acao = 0

        self.image = self.animation_list[self.acao][self.sprite_index]

        if pygame.time.get_ticks() - self.update_time > DELAY_ANIMACAO:
            self.update_time = pygame.time.get_ticks()
            self.sprite_index += 1

        if self.acao == 2 and self.sprite_index > len(self.animation_list[self.acao]) - 1 :#and escolha == 'sim':
            self.atirar = True
        else:
            self.atirar = False

        if self.sprite_index >= len(self.animation_list[self.acao]):
            self.sprite_index = 0
            self.acao += 1
        
    def atualiza_acao(self, nova_acao, delay):
        if nova_acao != self.acao:
            self.acao = nova_acao
            self.delay = delay
            self.sprite_index = 0
            self.sprite_index = 0
            self.update_time = pygame.time.get_ticks()

    def direcao(self):
        if cursor.rect.x > self.rect.x:
            self.flip = False
        elif cursor.rect.x < self.rect.x:
            self.flip = True 

    def atirando(self):
        tiro = Tiro_Banana(x=self.rect.centerx, y=self.rect.centery - (0.8 * self.rect.size[1]))
        self.bala.add(tiro)
        balas_grupo_macaco.add(tiro)

    def esta_vivo(self):
        dropa = random.choice(['sim', 'nao', 'sim'])
        if self.vida <= 0:
            aleatorio = random.choice(['vida', 'municao', 'invencibilidade', 'vida', 'municao', 'municao','vida', 'municao', 'invencibilidade','municao'])
            if dropa == 'sim':
                print(aleatorio)
                power = Poderes(aleatorio, self.rect.x, self.rect.y + (self.rect.size[1] / 2))
                power_up_grupo.add(power)
            self.kill()

    def desenhar(self):
        tela.blit(pygame.transform.flip(self.image, self.flip, False), self.rect) 
        # pygame.draw.rect(tela, (255,0,0), self.rect, 1)

    def colide_cursor(self):
        if pygame.sprite.collide_rect(self, cursor):
            if toma_dano:
                cursor.vida = 0
            
        
    def update(self):
        self.rect.x += tela_scroll

        self.esta_vivo()
        self.atualiza_animacao()
        self.desenhar()
        self.direcao()
        self.colide_cursor()

        if self.atirar:
            self.atirando()
        
        self.bala.update()
        self.bala.draw(tela)

class Tiro_Banana(pygame.sprite.Sprite):
    def __init__(self, x, y, speed = 1.4):
        pygame.sprite.Sprite.__init__(self)

        self.speed = speed
        self.image = pygame.image.load('imgs/inimigo/tiro/banana.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (int(self.image.get_width() * 1.5), int(self.image.get_height() * 1.5)))

        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        
        self.dano = 7
        self.timer = 10

        self.update_time = pygame.time.get_ticks()

    def bala_segue(self):   
        cursor_center = cursor.rect.center
        bala_center = self.rect.center

        self.vel = [cursor_center[0] - bala_center[0], cursor_center[1] - bala_center[1]]

        teste = (self.vel[0] ** 2 + self.vel[1] ** 2) ** 0.5
        if teste <= 1 :
            teste = 1
                
        self.vel = [(self.vel[0]) / teste * self.speed, self.vel[1] / teste * self.speed]  

    def colide_cursor(self):
        if pygame.sprite.collide_rect(cursor, self):
            if cursor.vivo:

                if toma_dano:
                    cursor.vida -= self.dano
                    desenha_texto('-7', fonte, (255,0,0), cursor.rect.x + 30, cursor.rect.y - 15)
                    dano_img = pygame.image.load('imgs/player/sprite/cursor_dano.png')
                    cursor.image = pygame.transform.scale(dano_img, (int(dano_img.get_width() * 1.2), int(dano_img.get_height() * 1.2)))
                else:
                    desenha_texto('0', fonte, (255,0,0), cursor.rect.x + 30, cursor.rect.y - 15)

                self.kill()
            else:
                self.kill()
  
    def colide_chao(self):
        for tile in bloco.sprites():
            if tile.rect.colliderect(self.rect):
                self.kill()
        
    def update(self):
        self.bala_segue()   
        self.image = pygame.transform.rotate(self.image, 90)  
        self.rect.x += self.vel[0] * self.speed
        self.rect.y += self.vel[1] * self.speed
        if self.timer <= 1:
            self.kill()
        self.colide_cursor()
        self.colide_chao()
        # pygame.draw.rect(tela, (255,0,0), self.rect, 1)
        self.timer -= 0.1
        desenha_texto(f'{self.timer:.0f}', fonteTemp, (255,255,255), self.rect.x + 10, self.rect.y - 10)
        

class Bloco(pygame.sprite.Sprite):
    def __init__(self, x, y, larg, alt):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((larg, alt))
        self.image.fill('black')
        self.rect = self.image.get_rect()
        self.rect.center = (x, y - (self.rect.size[1] / 2))

    def desenha(self):
        self.rect.x += tela_scroll
        tela.blit(self.image, self.rect)

    def update(self):
        self.desenha()

class Arquivo(pygame.sprite.Sprite):
    def __init__(self, x, y, larg, alt):
        pygame.sprite.Sprite.__init__(self)
        self.existe = True
        self.image = pygame.image.load("imgs/elementos/spr_arquivo.png")
        self.image = pygame.transform.scale(self.image, (int(self.image.get_width() * 0.1), int(self.image.get_height() * 0.1)))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        self.mudar = False

    def desenha(self):
        self.rect.x += tela_scroll
        tela.blit(self.image, self.rect)
        # pygame.draw.rect(tela, (0,0,0), self.rect, 1)

    def troca_pos(self):
        X_random = random.randint(100, SCREEN_WIDTH - 100)
        Y_random = random.randint(50, SCREEN_HEIGHT - 100)

    def colide_cursor(self):
        if pygame.sprite.collide_rect(cursor, self):
            self.kill()
            self.existe = False
            cursor.coletados += 1

    def update(self):
        self.desenha()
        self.colide_cursor()
        self.troca_pos()


class Lixeira(pygame.sprite.Sprite):
    def __init__(self, x, y, scale=1):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("imgs/elementos/lixeira_vazia.png")
        self.image = pygame.transform.scale(self.image, (int(self.image.get_width() * 0.08), int(self.image.get_height() * 0.08)))
        self.rect = self.image.get_rect(center=(x,y))

        self.luta_boss = False
    def desenhar(self):
        if cursor.coletados == arq_menu_quant:
            self.image = pygame.image.load("imgs/elementos/lixeira_cheia.png")
            self.image = pygame.transform.scale(self.image, (int(self.image.get_width() * 0.1), int(self.image.get_height() * 0.1)))
            desenha_texto(f"{arq_menu_quant}", fonte, (0,255,0), self.rect.x + 40, self.rect.y - 20)
        else:
            desenha_texto(f"{cursor.coletados} / {arq_menu_quant}", fonte, (255,255,255), self.rect.x + 40, self.rect.y - 20)

        self.rect.x += tela_scroll
        tela.blit(self.image, self.rect)

    def update(self):
        self.desenhar()



class InicioXp(pygame.sprite.Sprite):
    def __init__(self):
        self.lista_animacao = []
        self.indice = 0
        self.update_time = pygame.time.get_ticks()
        self.carregarImgs()
        self.image = self.lista_animacao[self.indice]
        self.rect = self.image.get_rect(center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))

    def carregarImgs(self):
        num_frames = len(os.listdir(f'imgs/inicio_xp'))
        for i in range(num_frames):
            img = pygame.image.load(f'imgs/inicio_xp/spr_{i}.png').convert_alpha() 
            self.lista_animacao.append(img)

    def atualiza_animacao(self):
        DELAY_ANIMACAO = 100

        self.image = self.lista_animacao[self.indice]

        if pygame.time.get_ticks() - self.update_time > DELAY_ANIMACAO:
            self.update_time = pygame.time.get_ticks()
            self.indice += 1

        if self.indice >= len(self.lista_animacao):
            self.indice = 0
        
    def desenha(self):
        tela.blit(self.image, self.rect)

    def update(self):
        self.desenha()
        self.atualiza_animacao()
        
class Botao():
	def __init__(self,x, y, image, scale):
		width = image.get_width()
		height = image.get_height()
		self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
		self.rect = self.image.get_rect()
		self.rect.center = (x, y)
		self.clicked = False

	def draw(self, surface):
		action = False

		pos = pygame.mouse.get_pos()

		if self.rect.collidepoint(pos):
			if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
				action = True
				self.clicked = True

		if pygame.mouse.get_pressed()[0] == 0:
			self.clicked = False

		surface.blit(self.image, (self.rect.x, self.rect.y))

		return action

class Clip_Scene(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.lista_animacao = []
        self.indice = 0
        self.update_time = pygame.time.get_ticks()
        self.carregarImgs()
        self.image = pygame.image.load('imgs/clip/clip_fala_0.png').convert_alpha()
        self.rect = self.image.get_rect(center = (SCREEN_WIDTH / 2 + 100, SCREEN_HEIGHT / 2))
        self.animar = False

    def carregarImgs(self):
        num_frames = len(os.listdir(f'imgs/clip_mal'))
        for i in range(num_frames):
            img = pygame.image.load(f'imgs/clip_mal/clip_fala_{i}.png').convert_alpha() 
            self.lista_animacao.append(img)

    def atualiza_animacao(self):
        DELAY_ANIMACAO = 2500
        cont = 1

        self.image = self.lista_animacao[self.indice]
        self.image = pygame.transform.scale(self.image, (int(self.image.get_width() * 2), int(self.image.get_height() * 2)))

        if pygame.time.get_ticks() - self.update_time > DELAY_ANIMACAO:
            self.update_time = pygame.time.get_ticks()
            self.indice += cont

        if self.indice >= len(self.lista_animacao):
            self.indice = 0
            self.animar = False
            self.image = pygame.image.load('imgs/clip/clip_fala_0.png').convert_alpha()
            self.rect = self.image.get_rect(center = (SCREEN_WIDTH / 2 + 100, SCREEN_HEIGHT / 2))

    def desenha(self):
        tela.blit(self.image, self.rect)

    def update(self):
        if self.animar:
            self.atualiza_animacao()

class Clip_boss(pygame.sprite.Sprite):
    def __init__(self, x, y, scale):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('imgs/clip/clip_bolado.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (int(self.image.get_width() * scale), int(self.image.get_height() * scale)))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)      
        
        self.vivo = True
        self.atirar = False
        self.bala = pygame.sprite.Group()
        self.spd = 3
        self.vida = 300
        self.delay = 0

    def move(self):
        if self.rect.x > SCREEN_WIDTH - 300 or self.rect.x < 200:
            self.spd *= -1

        self.rect.x += self.spd

    def atirando(self):
        aleatorio = random.choice([+self.rect.size[0]/2, -self.rect.size[0]/ 2])
        tiro = Tiro_Clip(x=self.rect.centerx + aleatorio, y=self.rect.centery)
        self.bala.add(tiro)
        balas_grupo_macaco.add(tiro)
        self.atirar = False

    def esta_vivo(self):
        if self.vida <= 0:
            self.vivo = False

    def colide_cursor(self):
        if pygame.sprite.collide_rect(self, cursor):
            cursor.vida = 0

    def desenha(self):
        tela.blit(self.image, self.rect)
        # pygame.draw.rect(tela, (255,0,0), self.rect, 1)
    
    def update(self):
        self.desenha()
        self.move()
        self.esta_vivo()
        self.colide_cursor()

        if self.atirar == True:
            self.atirando()

        if self.delay == 0:
            self.atirar = True
            self.delay = 60 
        else:
            self.delay -= 1
        
        self.bala.draw(tela)
        self.bala.update()
        
class Tiro_Clip(pygame.sprite.Sprite):
    def __init__(self, x, y, speed = 2, scale=0.08):
        pygame.sprite.Sprite.__init__(self)
        aleatorio = random.choice(['excel', 'powerpoint', 'word'])
        self.speed = speed
        self.image = pygame.image.load(f'imgs/clip/tiros/{aleatorio}.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (int(self.image.get_width() * scale), int(self.image.get_height() * scale)))

        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        
        self.dano = 15
        self.timer = 80

        self.update_time = pygame.time.get_ticks()

    def bala_segue(self):   
        cursor_center = cursor.rect.center
        bala_center = self.rect.center

        self.vel = [cursor_center[0] - bala_center[0], cursor_center[1] - bala_center[1]]

        teste = (self.vel[0] ** 2 + self.vel[1] ** 2) ** 0.5
        if teste <= 1 :
            teste = 1
                
        self.vel = [(self.vel[0]) / teste * self.speed, self.vel[1] / teste * self.speed]  

    def colide_cursor(self):
        if pygame.sprite.collide_rect(cursor, self):
            if cursor.vivo:
                self.kill()
                cursor.vida -= self.dano
                desenha_texto('-15', fonte, (255,0,0), cursor.rect.x + 30, cursor.rect.y - 15)
                dano_img = pygame.image.load('imgs/player/sprite/cursor_dano.png')
                cursor.image = pygame.transform.scale(dano_img, (int(dano_img.get_width() * 1.2), int(dano_img.get_height() * 1.2)))
            else:
                self.kill()
        
    def update(self):
        self.bala_segue()   
        self.rect.x += self.vel[0] * self.speed
        self.rect.y += self.vel[1] * self.speed
        if self.timer <= 1:
            self.kill()
        self.colide_cursor()
        # pygame.draw.rect(tela, (255,0,0), self.rect, 1)
        self.timer -= .3
        desenha_texto(f'{self.timer:.0f}', fonteTemp, (255,0,0), self.rect.x + 10, self.rect.y - 10)
        

mundo = Mundo(level1)
cursor, barra_de_vida, barra_clip = mundo.gera_nivel()

inicioXP = InicioXp()

botaoStart = Botao(SCREEN_WIDTH / 2, SCREEN_HEIGHT - 150, pygame.image.load('imgs/botao/botaoStart.png'), 1.5)
botaoSair = Botao(SCREEN_WIDTH / 2, SCREEN_HEIGHT - 90, pygame.image.load('imgs/botao/botaoSair.png'), 1)
botaoRestart = Botao(SCREEN_WIDTH / 2 + 80, SCREEN_HEIGHT / 2 + 50, pygame.image.load('imgs/botao/botaoRestart.png'), 1)
botaoSair2 = Botao(SCREEN_WIDTH / 2 - 100, SCREEN_HEIGHT / 2 + 50, pygame.image.load('imgs/botao/botaoSair2.png'), 1.2)
botaoNovamente = Botao(SCREEN_WIDTH / 2, SCREEN_HEIGHT - 150, pygame.image.load('imgs/botao/botaoJogarNovamente.png'), 1.5)

clip_group = pygame.sprite.GroupSingle()
cena = Clip_Scene()
clip_group.add(cena)

clip_Scene = clip_group.sprite

msg_erro = pygame.image.load("imgs/botao/msg_erro.png").convert_alpha()
msg_erro_rect = msg_erro.get_rect(center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))

arq_menu = pygame.image.load("imgs/elementos/spr_arquivo.png").convert_alpha()
arq_menu = pygame.transform.scale(arq_menu, (int(arq_menu.get_width() * 0.1), int(arq_menu.get_height() * 0.1)))
arq_menu_quant = len(arquivos.sprites())

venceu = False
run = True
while run:
    fps.tick(FPS)
    if start_game == False:
        tela.fill('black')
        inicioXP.update()
        if botaoStart.draw(tela):
            start_game = True
        if botaoSair.draw(tela):
            run = False
    elif comecar == False:
        desenha_BG()
        clip_Scene.desenha()
        # tela.fill('black')
        desenha_texto('RÁPIDO PRECISO DE SUA AJUDA. O SISTEMA FOI INFECTADO!!!', fonteFala, (0,0,0), (SCREEN_WIDTH / 2) - 500, SCREEN_HEIGHT - 660)
        desenha_texto('LEVE TODOS OS ARQUIVOS ATÉ A LIXEIRA!', fonteFala, (0,0,0), (SCREEN_WIDTH / 2) - 500, SCREEN_HEIGHT - 610)

        desenha_texto('A / D - PARA SE MOVER', fonteFala, (255,0,0), (SCREEN_WIDTH / 2) - 500, SCREEN_HEIGHT - 550)
        desenha_texto('W - PARA PULAR', fonteFala, (0,60,0), (SCREEN_WIDTH / 2) - 500, SCREEN_HEIGHT - 500)
        desenha_texto('ESPAÇO - PARA ATIRAR', fonteFala, (0,0,255), (SCREEN_WIDTH / 2) - 500, SCREEN_HEIGHT - 450)
        desenha_texto('ESC - PARA PAUSAR', fonteFala, 'yellow', (SCREEN_WIDTH / 2) - 500, SCREEN_HEIGHT - 400)

        tela.blit(pp_vida, ((SCREEN_WIDTH / 2) - 500, SCREEN_HEIGHT - 330))
        desenha_texto(f'- GANHA 40 DE VIDA', fonte, (255,255,255), (SCREEN_WIDTH / 2) - 470, SCREEN_HEIGHT - 325)

        tela.blit(pp_municao, ((SCREEN_WIDTH / 2) - 500, SCREEN_HEIGHT - 290))
        desenha_texto(f'- GANHA 10 DE MUNIÇÃO', fonte, (255,255,255), (SCREEN_WIDTH / 2) - 470, SCREEN_HEIGHT - 285)

        tela.blit(pp_ivencibilidade, ((SCREEN_WIDTH / 2) - 500, SCREEN_HEIGHT - 250))
        desenha_texto(f'- INVENCÍVEL POR 15s', fonte, (255,255,255), (SCREEN_WIDTH / 2) - 470, SCREEN_HEIGHT - 245)

        quadro = pygame.Surface((SCREEN_WIDTH / 2 - 300, 200))
        quadro = quadro.get_rect(topleft = (SCREEN_WIDTH / 2 - 510, SCREEN_HEIGHT - 560))
        pygame.draw.rect(tela, (0,0,0), quadro, 1)
        if botaoStart.draw(tela):
            comecar = True

    else:
        desenha_BG()
        bloco.update()
        lixeira.update()
        arquivos.update()

        power_up_grupo.draw(tela)
        power_up_grupo.update()

        if mundo.level == level2:
            if clip.sprite.vivo:
                clip.update()    
                barra_clip.draw(clip.sprite.vida)
                barra_de_vida.draw(cursor.vida)
                desenha_texto(texto=f'MUNIÇÃO: {cursor.municao}', fonte=fonte, cor=(255,255,255,1), x=430 ,y = SCREEN_HEIGHT - 25)
            else:
                venceu = True
                tela.fill('black')
                tela.blit(TELA_FINAL, (0,0))
                desenha_texto("VOCE FORMATOU SEU WINDOWS!!", fonteFala, (255,255,255), (SCREEN_WIDTH / 2) -200, 100)
                desenha_texto("PARABENS POR DERROTAR O CLIPPY.", fonteFala, (255,255,255), (SCREEN_WIDTH / 2) -200, 150)
                if botaoNovamente.draw(tela):
                    start_game = False
                    comecar = False
                    bg_scroll = 0    
                    restart_level()   
                    mundo = Mundo(level1)
                    cursor, barra_de_vida, barra_clip= mundo.gera_nivel()
                    venceu = False
                if botaoSair.draw(tela):
                    run = False

        if mundo.level == level1:
            barra_de_vida.draw(cursor.vida)
            desenha_texto(texto=f'MUNIÇÃO: {cursor.municao}', fonte=fonte, cor=(255,255,255,1), x=430 ,y = SCREEN_HEIGHT - 25)
        if cursor.boss == False:
            tela.blit(arq_menu, (580, SCREEN_HEIGHT - 27))
            desenha_texto(texto=f': {cursor.coletados} / {arq_menu_quant}', fonte=fonte, cor=(255,255,255,1), x=605 ,y = SCREEN_HEIGHT - 22)

        for mac in macacos_grupo.sprites():
            if mac.vivo:
                mac.update()  

        if cursor.vivo:
            if venceu == False:
                cursor.update()
            tela_scroll, level_complete = cursor.move()
            bg_scroll -= tela_scroll 

            if level_complete: 
                tela_scroll = 0
                macacos_grupo.empty()
                clip_Scene.rect.x = SCREEN_WIDTH / 2 - 800
                clip_Scene.animar = True
                clip_Scene.desenha()
                clip_Scene.update()
                if clip_Scene.animar == False:
                    bg_scroll = 0
                    restart_level()   
                    mundo = Mundo(level2)
                    cursor, barra_de_vida, barra_clip = mundo.gera_nivel()
                    cursor.boss = True
                    cursor.municao = 200
                    
        else:
            tela_scroll = 0
            tela.blit(msg_erro, msg_erro_rect)
            if botaoRestart.draw(tela):
                bg_scroll = 0    
                restart_level()   
                mundo = Mundo(level1)
                cursor, barra_de_vida, barra_clip = mundo.gera_nivel()
            
            if botaoSair2.draw(tela):
                run = False
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                start_game = False
            # TIRO do Player
            if event.key == pygame.K_SPACE:
                cursor.atirar = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                cursor.atirar = False    
    
    pygame.display.update()

pygame.quit()