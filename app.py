import pygame
import random
import sys
import os
import pygame.mixer

pygame.init()
pygame.mixer.init()

# Configurações da tela
LARGURA_JANELA = 400
ALTURA_JANELA = 600
tela = pygame.display.set_mode((LARGURA_JANELA, ALTURA_JANELA))
pygame.display.set_caption("Floppy Birb")

# Cores
BRANCO = (255, 255, 255)
VERDE = (45, 180, 105)
PRETO = (0, 0, 0)
VERDE_CLARO = (100, 200, 120)
VERDE_ESCURO = (30, 120, 70)
AMARELO = (255, 255, 51)
AMARELO_ESCURO = (204, 204, 0, 200)
VERMELHO = (255, 0, 0)

# Variáveis globais do jogo
pontos = 0
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
clock = pygame.time.Clock()

# Carrega a imagem de fundo
background_img = pygame.image.load('Floppy-Birb/bckgrnd/floppybckgnd.png')
background_img = pygame.transform.scale(background_img, (LARGURA_JANELA, ALTURA_JANELA))

personagem_selecionado = None

# Carrega a imagem do pássaro e ajusta o tamanho
birb_img = pygame.image.load('Floppy-Birb/images/1-floppybirb.png').convert_alpha()
birb_img = pygame.transform.scale(birb_img, (birb_img.get_width() * 2, birb_img.get_height() * 2))

# Carrega os arquivos de som
som_pulo = pygame.mixer.Sound('Floppy-Birb/sound/jump.wav')
som_colisao = pygame.mixer.Sound('Floppy-Birb/sound/collision.wav')

# Carrega música de fundo
pygame.mixer.music.load('Floppy-Birb/sound/DoomEternalOST.ogg')
F = 'Floppy-Birb/sound/F.ogg'

# Função para carregar automaticamente as imagens dos personagens da pasta 'images'
def carregar_imagens_personagens(pasta="Floppy-Birb/images"):
    imagens_personagens = []
    for arquivo in os.listdir(pasta):
        if arquivo.endswith(".png"):
            caminho_completo = os.path.join(pasta, arquivo)
            imagem = pygame.image.load(caminho_completo).convert_alpha()
            imagem = pygame.transform.scale(imagem, (imagem.get_width() * 3, imagem.get_height() * 3))
            imagens_personagens.append(imagem)
    return imagens_personagens

# Função para atualizar o personagem atual
def atualizar_birb_img(personagem_img):
    global birb_img  
    birb_img = personagem_img
# Fonte para texto
fonte = pygame.font.SysFont("comicsansms", 24)

# Variável global para controlar o movimento do background
background_x = 0

# Função para desenhar o botão de selecionar personagens
def desenha_botao_personagens():
    # Define as coordenadas e dimensões do botão
    botao_rect = pygame.Rect(LARGURA_JANELA // 2 - 80, ALTURA_JANELA // 2 + 100, 160, 40)
    
    # Desenha o retângulo amarelo do botão
    pygame.draw.rect(tela, AMARELO, botao_rect, border_radius=8)  # Botão preto com bordas arredondadas
    pygame.draw.rect(tela, PRETO, botao_rect, border_radius=8, width=3)
    
    # Renderiza o texto "Personagens" em preto no botão
    fonte_botao = pygame.font.SysFont("comicsansms", 24)
    texto_botao = fonte_botao.render("Personagens", True, PRETO)
    
    # Centraliza o texto dentro do botão
    texto_rect_botao = texto_botao.get_rect(center=botao_rect.center)
    
    # Desenha o texto na tela
    tela.blit(texto_botao, texto_rect_botao)

# Função para desenhar o pássaro
def desenha_passaro():
    # Calcula o ângulo de inclinação do pássaro com base na velocidade do pulo
    angulo = birb_velocidade * -5  # Ajuste este valor conforme necessário para controlar a inclinação

    # Rotaciona a imagem do pássaro
    birb_rotacionado = pygame.transform.rotate(birb_img, angulo)
    # Obtém um novo retângulo que contém o pássaro rotacionado
    retangulo_rotacionado = birb_rotacionado.get_rect(center=(birb_x, birb_y))

    # Desenha o pássaro rotacionado na tela
    tela.blit(birb_rotacionado, retangulo_rotacionado)

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

# Função para mostrar a tela de início
def mostra_tela_inicio(background_x = 0):

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

        # Desenha o botão "Personagens"
        desenha_botao_personagens()

        # Atualiza a tela
        pygame.display.flip()

        # Espera pelo evento de tecla para iniciar o jogo ou mostrar a tela de seleção de personagem
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return  # Sai da função e inicia o jogo
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                botao_rect = pygame.Rect(LARGURA_JANELA // 2 - 80, ALTURA_JANELA // 2 + 100, 160, 40)
                if botao_rect.collidepoint(mouse_x, mouse_y):
                    mostra_tela_selecao_personagem()
        # Limita a taxa de atualização da tela
        clock.tick(60)

# Função da tela de seleção de personagens
def mostra_tela_selecao_personagem(background_x=0):

    # Carrega imagens dos personagens automaticamente da pasta 'images'
    imagens_personagens = carregar_imagens_personagens()
    if not imagens_personagens:
        raise ValueError("Nenhuma imagem encontrada na pasta 'images'.")

    indice_personagem_selecionado = 0  # Índice do personagem atualmente selecionado
    personagem_selecionado = imagens_personagens[indice_personagem_selecionado]  # Personagem inicialmente selecionado

    # Tamanho e posição do quadrado amarelo com borda preta
    quadro_x = LARGURA_JANELA // 4
    quadro_y = ALTURA_JANELA // 4
    quadro_largura = LARGURA_JANELA // 2
    quadro_altura = ALTURA_JANELA // 2

    # Definição do botão de retorno no canto superior direito do quadrado amarelo
    botao_voltar_tamanho = 30  # Tamanho do botão
    botao_voltar_x = quadro_x + quadro_largura - botao_voltar_tamanho + 13.5
    botao_voltar_y = quadro_y - 13.5
    botao_voltar_rect = pygame.Rect(botao_voltar_x, botao_voltar_y, botao_voltar_tamanho, botao_voltar_tamanho)

    # Define os botões das setas
    seta_esquerda_rect = pygame.Rect(quadro_x - 80, ALTURA_JANELA // 2 - 25, 50, 50)
    seta_direita_rect = pygame.Rect(quadro_x + quadro_largura + 30, ALTURA_JANELA // 2 - 25, 50, 50)

    selecionado = False  # Inicializa o estado de seleção como False

    # Loop da tela de seleção de personagem
    rodando = True
    while rodando:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    rodando = False  # Sair da tela de seleção de personagem
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                # Verifica se o botão "X" foi clicado para voltar à tela principal
                if botao_voltar_rect.collidepoint(mouse_x, mouse_y):
                    return  # Voltar para a tela principal
                # Verifica se clicou na seta esquerda
                elif seta_esquerda_rect.collidepoint(mouse_x, mouse_y):
                    indice_personagem_selecionado = (indice_personagem_selecionado - 1) % len(imagens_personagens)
                    personagem_selecionado = imagens_personagens[indice_personagem_selecionado]
                # Verifica se clicou na seta direita
                elif seta_direita_rect.collidepoint(mouse_x, mouse_y):
                    indice_personagem_selecionado = (indice_personagem_selecionado + 1) % len(imagens_personagens)
                    personagem_selecionado = imagens_personagens[indice_personagem_selecionado]
                # Verifica se clicou no botão "Selecionar"
                elif botao_selecionar_rect.collidepoint(mouse_x, mouse_y):
                    selecionado = not selecionado  # Alterna o estado de seleção
                    personagem_selecionado = imagens_personagens[indice_personagem_selecionado]
                    atualizar_birb_img(personagem_selecionado)

        # Movimento do plano de fundo
        background_x -= int(cano_velocidade * 0.5)
        if background_x <= -background_img.get_width():
            background_x = 0

        # Desenha o fundo com movimento parallax
        tela.fill(BRANCO)
        tela.blit(background_img, (background_x, 0))
        tela.blit(background_img, (background_x + background_img.get_width(), 0))

        # Desenha o quadro amarelo com bordas pretas
        pygame.draw.rect(tela, AMARELO, (quadro_x, quadro_y, quadro_largura, quadro_altura), border_radius=10)  # Preenche o retângulo com amarelo claro
        pygame.draw.rect(tela, PRETO, (quadro_x, quadro_y, quadro_largura, quadro_altura), border_radius=10, width=3)  # Desenha as bordas pretas

        # Desenha o retângulo amarelo escuro ao redor da área da imagem do personagem
        margem = 20
        area_personagem_rect = pygame.Rect(quadro_x + margem, quadro_y + margem, quadro_largura - 2 * margem, quadro_altura - 2 * margem)
        pygame.draw.rect(tela, AMARELO_ESCURO if selecionado else AMARELO, area_personagem_rect, border_radius=10)
        pygame.draw.rect(tela, PRETO, area_personagem_rect, border_radius=10, width=3)

        # Desenha a imagem do personagem atualmente selecionado dentro da área delimitada
        personagem_rect = personagem_selecionado.get_rect(center=(LARGURA_JANELA // 2, ALTURA_JANELA // 2))
        tela.blit(personagem_selecionado, personagem_rect)

        # Definição do botão "Selecionar" dentro do retângulo amarelo principal
        botao_selecionar_rect = pygame.Rect(quadro_x + quadro_largura // 2 - 80, quadro_y + quadro_altura - 70, 160, 50)
        pygame.draw.rect(tela, AMARELO_ESCURO if selecionado else AMARELO, botao_selecionar_rect, border_radius=10)
        pygame.draw.rect(tela, PRETO, botao_selecionar_rect, border_radius=10, width=3)

        # Desenha o texto no botão "Selecionar" com base no estado de seleção
        fonte_botao = pygame.font.SysFont("comicsansms", 24)
        texto_selecionar = fonte_botao.render("Selecionado" if selecionado else "Selecionar", True, PRETO)
        texto_rect_selecionar = texto_selecionar.get_rect(center=botao_selecionar_rect.center)
        tela.blit(texto_selecionar, texto_rect_selecionar)

        # Desenha as setas dentro dos quadrados amarelos com borda preta
        tamanho_seta = 50
        seta_esquerda_rect = pygame.Rect(quadro_x - 80, ALTURA_JANELA // 2 - 25, tamanho_seta, tamanho_seta)
        seta_direita_rect = pygame.Rect(quadro_x + quadro_largura + 30, ALTURA_JANELA // 2 - 25, tamanho_seta, tamanho_seta)

        # Desenha os quadrados amarelos com borda preta ao redor das setas
        pygame.draw.rect(tela, AMARELO, seta_esquerda_rect, border_radius=10)  # Seta esquerda
        pygame.draw.rect(tela, PRETO, seta_esquerda_rect, border_radius=10, width=3)  # Borda preta
        pygame.draw.rect(tela, AMARELO, seta_direita_rect, border_radius=10)  # Seta direita
        pygame.draw.rect(tela, PRETO, seta_direita_rect, border_radius=10, width=3)  # Borda preta

        # Desenha o texto das setas
        fonte_seta = pygame.font.SysFont("arial", 36)
        texto_seta_esquerda = fonte_seta.render("<", True, PRETO)
        texto_seta_direita = fonte_seta.render(">", True, PRETO)

        # Posiciona texto das setas nos retângulos
        tela.blit(texto_seta_esquerda, seta_esquerda_rect.move(10, 5))
        tela.blit(texto_seta_direita, seta_direita_rect.move(10, 5))

        # Desenha o botão "X" para voltar à tela principal (formato circular com borda)
        pygame.draw.ellipse(tela, VERMELHO, botao_voltar_rect)  # Botão vermelho (elipse)
        pygame.draw.ellipse(tela, PRETO, botao_voltar_rect, width=2)  # Borda preta para o botão

        # Desenha as linhas diagonais dentro do botão "X" (tamanho menor)
        line_thickness = 2
        linha1_inicio = (botao_voltar_rect.left + 10, botao_voltar_rect.top + 10)
        linha1_fim = (botao_voltar_rect.right - 10, botao_voltar_rect.bottom - 10)
        linha2_inicio = (botao_voltar_rect.left + 10, botao_voltar_rect.bottom - 10)
        linha2_fim = (botao_voltar_rect.right - 10, botao_voltar_rect.top + 10)
        pygame.draw.line(tela, PRETO, linha1_inicio, linha1_fim, line_thickness)  # Linha diagonal (X)
        pygame.draw.line(tela, PRETO, linha2_inicio, linha2_fim, line_thickness)  # Linha diagonal (X)

        # Atualiza a tela
        pygame.display.flip()

# Função para mostrar a tela de fim de jogo
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
    overlay.blit(texto_fim2,  texto_rect2)

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
    global cano_velocidade, background_x
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
    
    birb_raio_y = 20 // 2  # Raio vertical do pássaro (metade da altura)

    velocidade_aumento_por_ponto = 0.1  # Taxa de aumento da velocidade dos canos por ponto

    while rodando:
        while esperando_inicio:
            if primeiro_jogo:
                mostra_tela_inicio()
                primeiro_jogo = False
                pygame.mixer.music.play(-1) # Toca música do jogo principal em loop
                
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
                    som_pulo.play()
                    
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
            som_colisao.play()
            # Carrega e toca a música de fim de jogo
            pygame.mixer.music.stop()
            pygame.mixer.music.load(F)
            pygame.mixer.music.play()
            mostra_tela_fim()
            
            # Para a música de fim de jogo e toca a do jogo principal
            pygame.mixer.music.stop()
            pygame.mixer.music.load('Floppy-Birb/sound/DoomEternalOST.ogg')
            pygame.mixer.music.play()

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