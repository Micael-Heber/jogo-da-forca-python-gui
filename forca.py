# arquivo: forca.py
import random
import os
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from palavras import PALAVRAS
import pygame
import ttkbootstrap as tb

pygame.init()

class JogoForca:
    def __init__(self, master):
        self.master = master
        self.master.title("Jogo da Forca Moderno")
        self.master.geometry("800x600")
        self.master.resizable(True, True)

        self.som_clique = pygame.mixer.Sound("sons/clique.wav")
        self.som_vitoria = pygame.mixer.Sound("sons/vitoria.wav")
        self.som_derrota = pygame.mixer.Sound("sons/derrota.wav")

        self.setup_tela_inicial()

    def setup_tela_inicial(self):
        self.frame_inicio = tb.Frame(self.master, padding=20)
        self.frame_inicio.pack(expand=True)

        tb.Label(self.frame_inicio, text="Escolha uma categoria:", font=("Segoe UI", 14)).pack(pady=10)
        self.combo_categoria = tb.Combobox(self.frame_inicio, values=list(PALAVRAS.keys()), state="readonly", bootstyle="dark")
        self.combo_categoria.pack()

        tb.Label(self.frame_inicio, text="Escolha a dificuldade:", font=("Segoe UI", 14)).pack(pady=10)
        self.combo_dificuldade = tb.Combobox(self.frame_inicio, values=["Fácil", "Médio", "Difícil"], state="readonly", bootstyle="dark")
        self.combo_dificuldade.pack()

        tb.Button(self.frame_inicio, text="Começar Jogo", command=self.iniciar_jogo, bootstyle="success-outline", width=20).pack(pady=30)

    def iniciar_jogo(self):
        categoria = self.combo_categoria.get()
        dificuldade = self.combo_dificuldade.get()

        if not categoria or not dificuldade:
            messagebox.showwarning("Aviso", "Escolha uma categoria e dificuldade")
            return

        palavras_cat = [p for p in PALAVRAS[categoria] if self.filtra_dificuldade(p[0], dificuldade)]
        self.palavra, self.dica = random.choice(palavras_cat)
        self.palavra = self.palavra.upper()

        self.letras_descobertas = ["_" for _ in self.palavra]
        self.letras_erradas = []
        self.tentativas_restantes = 6

        self.frame_inicio.destroy()
        self.setup_tela_jogo()

    def filtra_dificuldade(self, palavra, nivel):
        l = len(palavra)
        return (nivel == "Fácil" and l <= 5) or (nivel == "Médio" and 6 <= l <= 8) or (nivel == "Difícil" and l > 8)

    def setup_tela_jogo(self):
        self.frame_jogo = tb.Frame(self.master, padding=10)
        self.frame_jogo.pack(fill="both", expand=True)

        self.lbl_imagem = tb.Label(self.frame_jogo)
        self.lbl_imagem.pack(pady=10)

        self.lbl_palavra = tb.Label(self.frame_jogo, text=" ".join(self.letras_descobertas), font=("Courier New", 28, "bold"), bootstyle="default")
        self.lbl_palavra.pack(pady=15)

        self.lbl_erros = tb.Label(self.frame_jogo, text="", bootstyle="danger")
        self.lbl_erros.pack()

        self.lbl_dica = tb.Label(self.frame_jogo, text="", font=("Segoe UI", 10, "italic"))
        self.lbl_dica.pack()

        self.btn_dica = tb.Button(self.frame_jogo, text="Ver Dica", command=self.mostrar_dica, bootstyle="info-outline")
        self.btn_dica.pack(pady=5)

        self.frame_botoes = tb.Frame(self.frame_jogo)
        self.frame_botoes.pack(pady=15)

        self.botoes = {}
        letras = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        for i, letra in enumerate(letras):
            btn = tb.Button(self.frame_botoes, text=letra, width=3, command=lambda l=letra: self.tentar_letra(l), bootstyle="secondary")
            btn.grid(row=i//10, column=i%10, padx=5, pady=5)
            self.botoes[letra] = btn

        self.atualizar_interface()

    def tentar_letra(self, letra):
        self.som_clique.play()

        if letra in self.palavra:
            for i, l in enumerate(self.palavra):
                if l == letra:
                    self.letras_descobertas[i] = letra
        else:
            if letra not in self.letras_erradas:
                self.letras_erradas.append(letra)
                self.tentativas_restantes -= 1

        self.atualizar_interface()

        if "_" not in self.letras_descobertas:
            self.som_vitoria.play()
            self.frame_jogo.destroy()
            self.mostrar_tela_final(True)
        elif self.tentativas_restantes == 0:
            self.som_derrota.play()
            self.frame_jogo.destroy()
            self.mostrar_tela_final(False)

    def mostrar_dica(self):
        self.lbl_dica.config(text="Dica: " + self.dica)

    def atualizar_interface(self):
        self.lbl_palavra.config(text=" ".join(self.letras_descobertas))
        self.lbl_erros.config(text="Erros: " + ", ".join(self.letras_erradas))
        self.mostrar_imagem()

    def mostrar_imagem(self):
        caminho = os.path.join("imagens", f"forca{6 - self.tentativas_restantes}.png")
        imagem = Image.open(caminho).resize((180, 180))
        self.imgtk = ImageTk.PhotoImage(imagem)
        self.lbl_imagem.config(image=self.imgtk)

    def mostrar_tela_final(self, venceu):
        self.frame_final = tb.Frame(self.master, padding=20)
        self.frame_final.pack(expand=True)

        msg = "Parabéns! Você venceu!" if venceu else "Que pena! Você perdeu."
        cor = "success" if venceu else "danger"

        tb.Label(self.frame_final, text=msg, font=("Segoe UI", 20, "bold"), bootstyle=cor).pack(pady=15)
        tb.Label(self.frame_final, text=f"A palavra era: {self.palavra}", font=("Courier New", 16)).pack(pady=5)

        tb.Button(self.frame_final, text="Jogar Novamente", command=self.reiniciar_jogo, bootstyle="primary-outline").pack(pady=30)

    def reiniciar_jogo(self):
        self.frame_final.destroy()
        self.setup_tela_inicial()

if __name__ == "__main__":
    app = tb.Window(themename="darkly")
    JogoForca(app)
    app.mainloop()