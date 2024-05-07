import pygame
import random
import sys

pygame.init()

# Configurações da tela
LARGURA_JANELA = 400
ALTURA_JANELA = 600
tela = pygame.display.set_mode((LARGURA_JANELA, ALTURA_JANELA))
pygame.display.set_caption("Floppy Birb")

# Cores
BRANCO = (255, 255, 255)
VERDE = (45, 180, 105)
PRETO = (0, 0, 0)
VERDE_CLARO = (100, 200, 120)  # Verde mais claro para sombreamento
VERDE_ESCURO = (30, 120, 70)
AMARELO = (255, 255, 51)

# Variáveis globais do jogo
birb_x = 50
birb_y = ALTURA_JANELA // 2
birb_velocidade = 0
gravidade = 0.5
pulo = 9

cano_largura = 50
cano_espaço = 150
cano_x = LARGURA_JANELA
cano_altura = random.randint(50, 400)
cano_velocidade = 3

pontos = 0

clock = pygame.time.Clock()

# Carrega a imagem de fundo
background_img = pygame.image.load('Floppy-Birb/images/floppybckgnd.png')
background_img = pygame.transform.scale(background_img, (LARGURA_JANELA, ALTURA_JANELA))

# Carrega a imagem do pássaro e ajusta o tamanho
birb_img = pygame.image.load('Floppy-Birb/images/floppybirb.png').convert_alpha()
birb_img = pygame.transform.scale(birb_img, (birb_img.get_width() * 2, birb_img.get_height() * 2))

# Fonte para texto
fonte = pygame.font.SysFont("comicsansms", 24)

# Variável global para controlar o movimento do background
background_x = 0

# Função para desenhar o pássaro
def desenha_passaro():
    tela.blit(birb_img, (birb_x - birb_img.get_width() // 2, birb_y - birb_img.get_height() // 2))

# Função para desenhar os canos
def desenha_canos():
    # Desenha o cano superior
    pygame.draw.rect(tela, VERDE, (cano_x, 0, cano_largura, cano_altura))
    pygame.draw.rect(tela, VERDE, (cano_x - 3, cano_altura - 20, cano_largura + 6, 20))  # Borda superior
    pygame.draw.rect(tela, VERDE_ESCURO, (cano_x, cano_altura - 23, cano_largura, 3))  # Faixa de sombreado da borda superior

    # Linha de sombreamento do cano superior (esquerda)
    pygame.draw.rect(tela, VERDE_CLARO, (cano_x, 0, 4, cano_altura))  # Linha vertical esquerda (verde claro)
    pygame.draw.rect(tela, VERDE_ESCURO, (cano_x + 47, 0, 4, cano_altura - 20))  # Linha vertical direita (verde escuro)
    pygame.draw.rect(tela, VERDE_ESCURO, (cano_x + 50, cano_altura - 20, 4, 20))  # Linha vertical direita da borda (verde escuro)

    # Desenha o cano inferior
    pygame.draw.rect(tela, VERDE, (cano_x, cano_altura + cano_espaço, cano_largura, ALTURA_JANELA - cano_altura - cano_espaço))
    pygame.draw.rect(tela, VERDE, (cano_x - 3, cano_altura + cano_espaço, cano_largura + 6, 20))  # Borda inferior
    pygame.draw.rect(tela, VERDE_ESCURO, (cano_x, cano_altura + cano_espaço + 20, cano_largura, 3))  # Faixa de sombreado da borda inferior

    # Linha de sombreamento do cano inferior (esquerda)
    pygame.draw.rect(tela, VERDE_CLARO, (cano_x, cano_altura + cano_espaço, 4, ALTURA_JANELA - cano_altura - cano_espaço))  # Linha vertical esquerda (verde claro)
    pygame.draw.rect(tela, VERDE_ESCURO, (cano_x + 47, cano_altura + cano_espaço + 20, 4, ALTURA_JANELA - cano_altura - cano_espaço))  # Linha vertical direita (verde escuro)
    pygame.draw.rect(tela, VERDE_ESCURO, (cano_x + 50, cano_altura + cano_espaço, 4, 20))  # Linha vertical direita da borda (verde escuro)

# Função para mostrar a tela de início com movimento de fundo
def mostra_tela_inicio():
    global background_x

    titulo_fonte = pygame.font.SysFont("comicsansms", 36, bold=True)  # Define uma fonte em negrito para o título
    clock = pygame.time.Clock()
    start_time = pygame.time.get_ticks()  # Tempo de início da animação
    font_size = 36  # Tamanho inicial da fonte

    # Lista com as letras do título e suas novas posições x
    letras = [
        ("F", LARGURA_JANELA // 2 - 160),
        ("L", LARGURA_JANELA // 2 - 130),
        ("O", LARGURA_JANELA // 2 - 100),
        ("P", LARGURA_JANELA // 2 - 70),
        ("P", LARGURA_JANELA // 2 - 40),
        ("Y", LARGURA_JANELA // 2 - 10),
        (" ", LARGURA_JANELA // 2 + 30),
        ("B", LARGURA_JANELA // 2 + 60),
        ("I", LARGURA_JANELA // 2 + 90),
        ("R", LARGURA_JANELA // 2 + 120),
        ("B", LARGURA_JANELA // 2 + 150)
    ]

    while True:
        tela.fill(BRANCO)

        # Calcula o tempo decorrido desde o início da animação
        elapsed_time = pygame.time.get_ticks() - start_time

        # Movimento do plano de fundo
        background_x -= int(cano_velocidade * 0.5)  # Ajuste o fator de movimento do background

        # Verifica se o plano de fundo passou da tela, e reinicia se necessário
        if background_x <= -background_img.get_width():
            background_x = 0

        # Desenha o plano de fundo
        tela.blit(background_img, (background_x, 0))
        tela.blit(background_img, (background_x + background_img.get_width(), 0))

        # Renderiza cada letra do título com efeito de animação
        for letra, pos_x in letras:
            # Renderiza a letra em amarelo (um pouco maior)
            letra_texto_amarelo = titulo_fonte.render(letra, True, AMARELO)
            letra_texto_amarelo = pygame.transform.scale(letra_texto_amarelo, (font_size, font_size))

            # Renderiza a letra em preto (um pouco menor)
            letra_texto_preto = titulo_fonte.render(letra, True, PRETO)
            letra_texto_preto = pygame.transform.scale(letra_texto_preto, (font_size, font_size))

            # Obtém os retângulos de cada versão da letra
            letra_rect_amarelo = letra_texto_amarelo.get_rect(midtop=(pos_x, ALTURA_JANELA // 3))
            letra_rect_preto = letra_texto_preto.get_rect(midtop=(pos_x, ALTURA_JANELA // 3))

            # Ajusta o retângulo da letra preta para ficar ligeiramente menor
            letra_rect_preto.inflate_ip(-4, -4)

            # Desenha a letra preta (menor) primeiro para simular o contorno
            tela.blit(letra_texto_preto, letra_rect_preto)

            # Desenha a letra amarela (maior) por cima
            tela.blit(letra_texto_amarelo, letra_rect_amarelo)

        # Renderiza o texto "Aperte ESPAÇO para começar" na parte inferior da tela
        texto_inicio = fonte.render("Aperte ESPAÇO para começar", True, PRETO)
        texto_rect_inicio = texto_inicio.get_rect(center=(LARGURA_JANELA // 2, ALTURA_JANELA - 50))
        tela.blit(texto_inicio, texto_rect_inicio)

        # Atualiza a tela
        pygame.display.flip()

        # Espera pelo evento de tecla para iniciar o jogo
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return  # Sai da função e inicia o jogo

        # Limita a taxa de atualização da tela
        clock.tick(60)

# Função para mostrar tela de fim de jogo
def mostra_tela_fim():
    global pontos

    # Cria uma superfície semi-transparente para cobrir o jogo pausado
    overlay = pygame.Surface((LARGURA_JANELA, ALTURA_JANELA), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 128))  # Cor preta semi-transparente (RGBA), ajuste a opacidade conforme necessário

    # Desenha a caixa de diálogo para os textos de fim de jogo
    caixa_rect = pygame.Rect(LARGURA_JANELA // 4, ALTURA_JANELA // 4, LARGURA_JANELA // 2, ALTURA_JANELA // 2)
    pygame.draw.rect(overlay, AMARELO, caixa_rect, border_radius=10)  # Cor cinza claro para a caixa com bordas arredondadas

    # Desenha a borda em volta da caixa
    pygame.draw.rect(overlay, PRETO, caixa_rect, border_radius=10, width=3)  # Borda preta ao redor da caixa

    # Desenha os textos de fim de jogo na caixa
    fonte_fim = pygame.font.SysFont("comicsansms", 32)
    texto_fim1 = fonte_fim.render("Fim de jogo", True, PRETO)
    texto_rect1 = texto_fim1.get_rect(center=(LARGURA_JANELA // 2, ALTURA_JANELA // 3))
    overlay.blit(texto_fim1, texto_rect1)

    texto_fim2 = fonte_fim.render(f"Pontuação: {pontos}", True, PRETO)
    texto_rect2 = texto_fim2.get_rect(center=(LARGURA_JANELA // 2, ALTURA_JANELA // 2))
    overlay.blit(texto_fim2, texto_rect2)

    # Desenha o botão de reiniciar dentro da caixa
    botao_rect = pygame.Rect(LARGURA_JANELA // 2 - 80, ALTURA_JANELA // 2 + 50, 160, 40)
    pygame.draw.rect(overlay, PRETO, botao_rect, border_radius=8)  # Botão preto com bordas arredondadas
    fonte_botao = pygame.font.SysFont("comicsansms", 24)
    texto_botao = fonte_botao.render("Reiniciar", True, BRANCO)
    texto_rect_botao = texto_botao.get_rect(center=botao_rect.center)
    overlay.blit(texto_botao, texto_rect_botao)

    # Aplica a superfície semi-transparente à tela
    tela.blit(overlay, (0, 0))

    pygame.display.flip()

    # Aguarda o clique do mouse no botão de reiniciar
    esperando_clique = True
    while esperando_clique:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if botao_rect.collidepoint(mouse_x, mouse_y):
                    reiniciar_jogo()
                    esperando_clique = False

# Função para reiniciar o jogo
def reiniciar_jogo():
    global birb_y, birb_velocidade, cano_x, cano_altura, pontos, cano_velocidade
    birb_y = ALTURA_JANELA // 2
    birb_velocidade = 0
    cano_x = LARGURA_JANELA
    cano_altura = random.randint(50, 400)
    pontos = 0
    cano_velocidade = 3  # Reinicia a velocidade inicial dos canos
    mostra_tela_inicio()

# Função para mover o background
def move_background():
    global background_x, cano_velocidade
    background_x -= int(cano_velocidade * 0.5)  # Ajuste o fator de movimento do background

    if background_x <= -background_img.get_width():
        background_x = 0  # Reinicia a posição do background quando sair completamente da tela

# Função para mostrar a pontuação durante o jogo
def mostra_pontuacao():
    texto_pontuacao = fonte.render(str(pontos), True, PRETO)
    pontuacao_rect = texto_pontuacao.get_rect(topright=(LARGURA_JANELA - 20, 20))  # Posição no canto superior direito

    # Desenha a forma interna
    pontuacao_rect_in = pontuacao_rect.inflate(20, 20)  # Aumenta o tamanho do retângulo para a borda preta
    pygame.draw.rect(tela, AMARELO, pontuacao_rect_in, border_radius=8)  # Retângulo amarelo

    # Desenha a forma preto externa
    pygame.draw.rect(tela, PRETO, pontuacao_rect_in, 3, border_radius=8)  # Borda preta com 3 pixels de largura

    # Centraliza o texto dentro do retângulo
    texto_rect_pontuacao = texto_pontuacao.get_rect(center=pontuacao_rect_in.center)
    tela.blit(texto_pontuacao, texto_rect_pontuacao)

# Função para verificar colisão entre o pássaro e os canos
def verifica_colisao():
    global birb_x, birb_y, birb_img, cano_x, cano_altura, cano_largura, cano_espaço

    # Dimensões reais do pássaro após redimensionamento x2
    birb_largura = 56
    birb_altura = 40

    birb_raio_x = birb_largura // 2
    birb_raio_y = birb_altura // 2

    birb_centro_x = birb_x
    birb_centro_y = birb_y

    cano_topo = cano_altura
    cano_base = cano_altura + cano_espaço

    # Verifica se o pássaro está dentro dos limites horizontais dos canos
    if (birb_centro_x + birb_raio_x > cano_x and birb_centro_x - birb_raio_x < cano_x + cano_largura):
        # Verifica se o centro vertical do pássaro está fora da zona segura entre os canos
        if not (birb_centro_y > cano_topo and birb_centro_y < cano_base):
            return True

    # Verifica colisão com a parte superior ou inferior da tela
    if birb_y - birb_raio_y < 0 or birb_y + birb_raio_y > ALTURA_JANELA:
        return True

    # Verifica colisão na parte superior do pássaro
    if birb_y - birb_raio_y < cano_topo:
        if birb_x + birb_raio_x > cano_x and birb_x - birb_raio_x < cano_x + cano_largura:
            return True

    return False

# Loop principal do jogo
def jogo():
    global birb_y, birb_velocidade, cano_x, cano_altura, pontos, background_x, cano_velocidade

    rodando = True
    esperando_inicio = True
    primeiro_jogo = True

    birb_raio_x = 28 // 2  # Raio horizontal do pássaro (metade da largura)
    birb_raio_y = 20 // 2  # Raio vertical do pássaro (metade da altura)

    velocidade_aumento_por_ponto = 0.1  # Taxa de aumento da velocidade dos canos por ponto

    while rodando:
        while esperando_inicio:
            if primeiro_jogo:
                mostra_tela_inicio()
                primeiro_jogo = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        esperando_inicio = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    birb_velocidade = -pulo

        # Atualiza a posição do pássaro com base na gravidade
        birb_velocidade += gravidade
        birb_y += birb_velocidade

        # Atualiza posição dos canos
        cano_x -= cano_velocidade
        if cano_x + cano_largura < 0:
            cano_x = LARGURA_JANELA
            cano_altura = random.randint(50, 400)
            pontos += 1
            # Aumenta a velocidade do cano de acordo com os pontos
            cano_velocidade += velocidade_aumento_por_ponto

        # Verifica colisões
        if verifica_colisao():
            mostra_tela_fim()

        # Verifica se o pássaro atingiu os limites da tela
        if birb_y + birb_raio_y > ALTURA_JANELA or birb_y - birb_raio_y < 0:
            mostra_tela_fim()

        # Desenha o fundo com movimento parallax
        tela.fill(BRANCO)
        tela.blit(background_img, (background_x, 0))
        tela.blit(background_img, (background_x + background_img.get_width(), 0))

        move_background()  # Chama a função para mover o background

        # Desenha elementos
        desenha_passaro()
        desenha_canos()
        mostra_pontuacao()  # Mostra a pontuação na tela
        pygame.display.flip()
        clock.tick(60)

# Inicia o jogo
jogo()

pygame.quit()
