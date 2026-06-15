# Simulador de Gerência de Memória (Paginação) - SISOP 2026/1

Este repositório contém a implementação do Trabalho Prático 02 da disciplina de Sistemas Operacionais (Turma 2026/1), ministrada pelo Prof. Filipo Mór. 

O objetivo deste projeto é simular o gerenciamento de memória virtual de um Sistema Operacional, focando na paginação e no tratamento de faltas de página (*Page Faults*) através de algoritmos de substituição.

## 👥 Grupo 04
* **Integrantes:** Felipe, Brenda e Toninho
* **Algoritmos Designados:** FIFO vs. Ótimo (OPT)
* **Configuração Base:** 4 Frames 

## ⚙️ Funcionalidades e Algoritmos

O simulador processa um fluxo de referências a endereços de memória a partir de um arquivo de texto, gerencia a tabela de páginas e os quadros (*frames*) da memória física. A cada instrução, um mapa visual da memória é impresso no terminal, e estatísticas de *hits* e *page faults* são calculadas ao final.

Os algoritmos implementados para substituição de páginas são:
1. **FIFO (First-In, First-Out):** A página que está há mais tempo na memória (a primeira que entrou) é a escolhida para ser substituída.
2. **OPT (Ótimo / Optimal Page Replacement):** Algoritmo teórico que substitui a página que demorará mais tempo para ser referenciada novamente no futuro.

## 🚀 Requisitos

* Python 3.10 ou superior.
* Nenhuma biblioteca externa (*built-in* apenas).

## 💻 Como Executar

O programa é executado via linha de comando (terminal), permitindo a passagem do arquivo de entrada e a escolha do algoritmo como argumentos.

**Sintaxe:**
```bash
python simulador_memoria.py [arquivo_de_entrada] [ALGORITMO]
```

**Exemplos de uso:**

Para rodar com o algoritmo **FIFO**:
```bash
python simulador_memoria.py entrada.txt FIFO
```

Para rodar com o algoritmo **Ótimo (OPT)**:
```bash
python simulador_memoria.py entrada.txt OPT
```

### Formato do Arquivo de Entrada (`entrada.txt`)
O arquivo de entrada deve ser um arquivo de texto simples (sem caminhos absolutos no código), contendo:
* **1ª Linha:** Quantidade de frames disponíveis na memória física (ex: `4`).
* **Linhas Seguintes:** A sequência de números de páginas sendo referenciadas pelo processo, um número por linha.

## 📊 Critérios de Avaliação Atendidos
* Corretude Teórica dos algoritmos FIFO e OPT.
* Impressão fiel do mapa de memória passo a passo.
* Qualidade do código fonte (sem dependências externas ou caminhos absolutos).
* Versionamento distribuído no GitHub.