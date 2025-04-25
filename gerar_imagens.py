from PIL import Image, ImageDraw
import os

def gerar_imagens_forca(pasta="imagens"):
    os.makedirs(pasta, exist_ok=True)
    largura, altura = 300, 300

    for i in range(7):
        img = Image.new("RGB", (largura, altura), "white")
        draw = ImageDraw.Draw(img)

        # Estrutura da forca
        draw.line((50, 250, 250, 250), fill="black", width=5)
        draw.line((100, 250, 100, 50), fill="black", width=5)
        draw.line((100, 50, 200, 50), fill="black", width=5)
        draw.line((200, 50, 200, 80), fill="black", width=5)

        if i >= 1:
            draw.ellipse((180, 80, 220, 120), outline="black", width=4)  # cabeça
        if i >= 2:
            draw.line((200, 120, 200, 180), fill="black", width=4)  # corpo
        if i >= 3:
            draw.line((200, 130, 170, 160), fill="black", width=4)  # braço esq
        if i >= 4:
            draw.line((200, 130, 230, 160), fill="black", width=4)  # braço dir
        if i >= 5:
            draw.line((200, 180, 170, 220), fill="black", width=4)  # perna esq
        if i >= 6:
            draw.line((200, 180, 230, 220), fill="black", width=4)  # perna dir

        img.save(os.path.join(pasta, f"forca{i}.png"))

gerar_imagens_forca()
