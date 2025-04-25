from scipy.io.wavfile import write
import numpy as np
import os

def gerar_som(nome_arquivo, frequencia, duracao_ms):
    taxa = 44100
    duracao = duracao_ms / 1000
    t = np.linspace(0, duracao, int(taxa * duracao), False)
    onda = 0.5 * np.sin(2 * np.pi * frequencia * t)
    onda = np.int16(onda * 32767)
    write(nome_arquivo, taxa, onda)

os.makedirs("sons", exist_ok=True)
gerar_som("sons/clique.wav", 700, 120)
gerar_som("sons/vitoria.wav", 1000, 400)
gerar_som("sons/derrota.wav", 200, 500)
