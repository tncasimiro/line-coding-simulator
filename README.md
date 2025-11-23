# Simulador de Codificação de Linha em Python

## Visão Geral

Este projeto implementa um simulador completo dos principais esquemas de codificação de linha digital em Python, conforme especificado para a disciplina de Comunicação de Dados. Ele gera sinais codificados, exibe gráficos temporais e apresenta análises sobre número de transições, componente DC e estimativa de largura de banda relativa.

7 Esquemas de Codificação Implementados:

1. NRZ-L (Non Return to Zero Level)
2. NRZ-I (Non Return to Zero Invert on Ones)
3. RZ (Return to Zero)
4. Manchester
5. Manchester Diferencial
6. AMI (Alternate Mark Inversion)
7. Pseudoternário

## Arquivos Principais

- `line_coding_simulator.py`: Script principal contendo as funções de codificação, análise, geração de gráficos e interface para entrada de dados.
- `test_line_coding_simulator.py`: Conjunto de testes unitários para validar as funções principais.

## Pré-requisitos

- Python 3.6 ou superior
- Bibliotecas Python:
  - numpy
  - matplotlib

## Instalação de Dependências

Execute o comando abaixo para instalar as bibliotecas necessárias:

```bash
pip install numpy matplotlib
```

## Como Executar o Simulador

1. Abra um terminal ou prompt de comando.

2. Navegue até o diretório onde está salvo o arquivo `line_coding_simulator.py`.

3. Execute o comando:

```bash
python line_coding_simulator.py
```

4. O programa solicitará escolher a forma de entrada da sequência de bits:
   - Digitar `1` para inserir manualmente uma sequência (exemplo: `1011001110`).
   - Digitar `2` para ler a sequência de um arquivo `.txt` com a linha de bits.

5. Após fornecer a sequência válida, o simulador calculará as codificações, exibirá nos gráficos e imprimirá as análises no terminal.

6. Os gráficos gerados serão salvos automaticamente na pasta do projeto como arquivos PNG com nomes indicativos (ex: `NRZ-L_Codificacao.png`).

## Onde Encontrar os Gráficos

Verifique a pasta do projeto para os arquivos de gráficos em formato PNG. Você pode abrir estes arquivos com qualquer visualizador de imagens.

## Sobre os Testes

- Os testes unitários estão no arquivo `test_line_coding_simulator.py`.
- Para rodar os testes, execute no terminal:

```bash
python -m unittest test_line_coding_simulator.py
```

## Sugestões para Melhorias Futuras

- Interface gráfica para manipulação interativa das sequências.
- Exportação dos resultados analíticos em CSV.
- Mais validação e tratamento de erros nas entradas.
- Parâmetros de linha de comando para facilitar a execução.
- Documentação mais detalhada e exemplos adicionais.
