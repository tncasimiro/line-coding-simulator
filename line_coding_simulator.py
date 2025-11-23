import os
import numpy as np
import matplotlib.pyplot as plt


def encode_nrz_l(bits, Rb, sps):
    """
    NRZ-L encoding
    0 -> nível baixo (-1)
    1 -> nível alto (+1)
    """
    bit_duration = 1 / Rb
    # Para garantir que t tenha o numero correto de pontos, calcular separado
    s = np.repeat(bits, sps)
    t = np.linspace(0, bit_duration * len(bits), len(s), endpoint=False)
    s = 2 * s - 1  # Map 0->-1 and 1->1
    return t, s


def encode_nrz_i(bits, Rb, sps):
    """
    NRZ-I encoding
    bit 1 -> inverte o nível
    bit 0 -> mantém o nível anterior
    """
    bit_duration = 1 / Rb
    s = np.zeros(len(bits) * sps)
    current_level = 1
    for i, bit in enumerate(bits):
        if bit == 1:
            current_level = -current_level
        s[i * sps:(i + 1) * sps] = current_level
    t = np.linspace(0, bit_duration * len(bits), len(s), endpoint=False)
    return t, s


def encode_rz(bits, Rb, sps):
    """
    RZ encoding
    1 -> nível alto na primeira metade do bit, zero na segunda
    0 -> zero durante todo o bit
    """
    bit_duration = 1 / Rb
    s = np.zeros(len(bits) * sps)
    half_sps = sps // 2
    for i, bit in enumerate(bits):
        if bit == 1:
            s[i * sps:i * sps + half_sps] = 1
            s[i * sps + half_sps:(i + 1) * sps] = 0
        else:
            s[i * sps:(i + 1) * sps] = 0
    t = np.linspace(0, bit_duration * len(bits), len(s), endpoint=False)
    return t, s


def encode_manchester(bits, Rb, sps):
    """
    Manchester encoding
    0 -> transição alto->baixo
    1 -> transição baixo->alto
    """
    bit_duration = 1 / Rb
    s = np.zeros(len(bits) * sps)
    half_sps = sps // 2
    for i, bit in enumerate(bits):
        if bit == 0:
            s[i * sps:i * sps + half_sps] = 1
            s[i * sps + half_sps:(i + 1) * sps] = -1
        else:
            s[i * sps:i * sps + half_sps] = -1
            s[i * sps + half_sps:(i + 1) * sps] = 1
    t = np.linspace(0, bit_duration * len(bits), len(s), endpoint=False)
    return t, s


def encode_diff_manchester(bits, Rb, sps):
    """
    Manchester diferencial
    0 -> transição no início do bit
    1 -> sem transição no início do bit
    (todos possuem transição no meio)
    """
    bit_duration = 1 / Rb
    s = np.zeros(len(bits) * sps)
    half_sps = sps // 2
    last_level = 1
    for i, bit in enumerate(bits):
        if bit == 0:
            # transição no início do bit (invert last_level)
            start_level = -last_level
        else:
            # sem transição no início do bit (mantém last_level)
            start_level = last_level
        # metade do bit: start_level
        s[i * sps:i * sps + half_sps] = start_level
        # metade do bit: invertido
        s[i * sps + half_sps:(i + 1) * sps] = -start_level
        last_level = -start_level
    t = np.linspace(0, bit_duration * len(bits), len(s), endpoint=False)
    return t, s


def encode_ami(bits, Rb, sps):
    """
    AMI (Alternate Mark Inversion)
    0 -> nível 0
    1 -> alterna entre +1 e -1
    """
    bit_duration = 1 / Rb
    s = np.zeros(len(bits) * sps)
    last_mark = -1
    for i, bit in enumerate(bits):
        if bit == 1:
            last_mark = -last_mark
            s[i * sps:(i + 1) * sps] = last_mark
        else:
            s[i * sps:(i + 1) * sps] = 0
    t = np.linspace(0, bit_duration * len(bits), len(s), endpoint=False)
    return t, s


def encode_pseudoternary(bits, Rb, sps):
    """
    Pseudoternário
    1 -> nível 0
    0 -> alterna entre +1 e -1
    """
    bit_duration = 1 / Rb
    s = np.zeros(len(bits) * sps)
    last_mark = -1
    for i, bit in enumerate(bits):
        if bit == 0:
            last_mark = -last_mark
            s[i * sps:(i + 1) * sps] = last_mark
        else:
            s[i * sps:(i + 1) * sps] = 0
    t = np.linspace(0, bit_duration * len(bits), len(s), endpoint=False)
    return t, s


def count_transitions(signal):
    """
    Conta transições no sinal codificado
    """
    transitions = np.sum(signal[:-1] != signal[1:])
    return transitions


def calculate_dc_component(signal):
    """
    Calcula o componente DC (valor médio do sinal)
    """
    return np.mean(signal)


def estimate_bandwidth(transitions, signal_duration):
    """
    Estimativa de largura de banda relativa baseada no número de transições por segundo
    """
    if signal_duration == 0:
        return "indefinida"
    trans_per_second = transitions / signal_duration
    # Critério aproximado para banda baixa, média e alta
    # Ajustado para escala da duração do sinal
    if trans_per_second < 0.5:
        return "baixa"
    elif trans_per_second < 1.5:
        return "média"
    else:
        return "alta"


def plot_signal(t, s, bits, title, save=False):
    plt.figure(figsize=(10, 3))
    plt.step(t, s, where='post')
    plt.title(title)
    plt.xlabel("Tempo (s)")
    plt.ylabel("Amplitude")
    plt.grid(True)

    # Desenhar linhas verticais para limites de cada bit
    if len(t) < 2:
        bit_duration = 0.01  # valor pequeno padrão para evitar erro
    else:
        bit_duration = t[1] - t[0]
    # Infer sps como número de amostras por bit
    sps = int(len(s) / len(bits))
    for i in range(len(bits) + 1):
        plt.axvline(x=i * bit_duration * sps, color='gray',
                    linestyle='--', linewidth=0.5)

    plt.ylim(-2, 2)
    plt.tight_layout()
    if save:
        filename = title.replace(" ", "_").replace(
            "ç", "c").replace("ã", "a") + ".png"
        folder = os.path.dirname(os.path.abspath(__file__))
        filepath = os.path.join(folder, filename)
        plt.savefig(filepath)
    plt.show()
    if save:
        plt.close()


def analyze_and_print(name, t, s, bits, save=False):
    transitions = count_transitions(s)
    dc = calculate_dc_component(s)
    duration = t[-1] - t[0]
    bandwidth = estimate_bandwidth(transitions, duration)
    print(f"{name}: DC = {dc:.2f}, Transições = {transitions}, Banda = {bandwidth}")
    plot_signal(t, s, bits, f"{name} - Codificacao", save=save)


def read_bits_from_input():
    while True:
        choice = input(
            "Digite 1 para inserir sequência manualmente ou 2 para ler de arquivo .txt: ")
        if choice == "1":
            bitstring = input("Digite a sequência de bits (ex.: 1011001110): ")
            if set(bitstring).issubset({"0", "1"}):
                bits = [int(b) for b in bitstring]
                return bits
            else:
                print("Sequência inválida! Apenas 0 e 1 são permitidos.")
        elif choice == "2":
            filename = input("Digite o nome do arquivo .txt: ")
            try:
                with open(filename, "r") as f:
                    bitstring = f.read().strip()
                if set(bitstring).issubset({"0", "1"}):
                    bits = [int(b) for b in bitstring]
                    return bits
                else:
                    print(
                        "Arquivo contém caracteres inválidos! Apenas 0 e 1 são permitidos.")
            except FileNotFoundError:
                print("Arquivo não encontrado.")
        else:
            print("Opção inválida. Digite 1 ou 2.")


def main():
    print("Simulador de Codificação de Linha\n")
    bits = read_bits_from_input()
    Rb = 1e3  # taxa de bits: 1000 bits/segundo (pode ser alterada)
    sps = 100  # amostras por bit

    encoders = [
        ("NRZ-L", encode_nrz_l),
        ("NRZ-I", encode_nrz_i),
        ("RZ", encode_rz),
        ("Manchester", encode_manchester),
        ("Manchester Diferencial", encode_diff_manchester),
        ("AMI", encode_ami),
        ("Pseudoternário", encode_pseudoternary)
    ]

    for name, func in encoders:
        t, s = func(bits, Rb, sps)
        analyze_and_print(name, t, s, bits, save=True)


if __name__ == "__main__":
    main()
