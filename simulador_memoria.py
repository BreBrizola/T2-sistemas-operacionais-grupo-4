###
###     S I M U L A D O R    D E    M E M Ó R I A
###
### Prof. Filipo - github.com/ProfessorFilipo/MemSim/
### Grupo 04 - FIFO vs. Ótimo (OPT) - 4 Frames
###

import sys


class Frame:
    def __init__(self, id_frame):
        self.id_frame = id_frame
        self.pagina_alocada = None   # Número da página ou None se vazio
        self.timestamp = -1          # Usado pelo FIFO: momento de inserção


class TabelaPaginas:
    def __init__(self, num_frames, algoritmo):
        self.frames = [Frame(i) for i in range(num_frames)]
        self.total_page_faults = 0
        self.total_acessos = 0
        self.algoritmo = algoritmo.upper()   # 'FIFO' ou 'OPT'
        self.relogio = 0                     # Contador global de tempo (FIFO)
        self.fila_fifo = []                  # Ordem de inserção dos frames (FIFO)
        self.referencias_futuras = []        # Sequência completa de páginas (OPT)
        self.posicao_atual = 0               # Índice da referência atual (OPT)

    def definir_referencias(self, ref_list):
        """Fornece a sequência completa ao algoritmo OPT para look-ahead."""
        self.referencias_futuras = ref_list

    # ------------------------------------------------------------------
    # Ponto de entrada principal: processa um acesso a uma página
    # ------------------------------------------------------------------
    def acessar_pagina(self, numero_pagina, indice_atual=0):
        self.total_acessos += 1
        self.posicao_atual = indice_atual

        # 1. Verifica HIT — página já está na memória
        for frame in self.frames:
            if frame.pagina_alocada == numero_pagina:
                return True, frame.id_frame   # (Hit, frame_id)

        # 2. PAGE FAULT — página não está na memória
        self.total_page_faults += 1

        # 3. Existe frame vazio? Insere sem substituição
        for frame in self.frames:
            if frame.pagina_alocada is None:
                frame.pagina_alocada = numero_pagina
                self._inicializar_metadados(frame)
                return False, frame.id_frame  # (Fault, frame_id)

        # 4. Memória cheia — aplica o algoritmo de substituição
        frame_vitima = self._substituir_pagina(numero_pagina)
        frame_vitima.pagina_alocada = numero_pagina
        self._reinicializar_metadados(frame_vitima)
        return False, frame_vitima.id_frame   # (Fault, frame_id)

    # ------------------------------------------------------------------
    # Metadados: inicialização na primeira inserção
    # ------------------------------------------------------------------
    def _inicializar_metadados(self, frame):
        if self.algoritmo == 'FIFO':
            frame.timestamp = self.relogio
            self.relogio += 1
            self.fila_fifo.append(frame.id_frame)

    # ------------------------------------------------------------------
    # Metadados: reinicialização após substituição
    # ------------------------------------------------------------------
    def _reinicializar_metadados(self, frame):
        if self.algoritmo == 'FIFO':
            frame.timestamp = self.relogio
            self.relogio += 1
            # O frame já foi removido da fila em _substituir_pagina; reinsere no fim
            self.fila_fifo.append(frame.id_frame)

    # ------------------------------------------------------------------
    # FIFO: retira o frame mais antigo (cabeça da fila)
    # OPT : retira a página cujo próximo uso está mais distante no futuro
    # ------------------------------------------------------------------
    def _substituir_pagina(self, nova_pagina):
        if self.algoritmo == 'FIFO':
            vitima_id = self.fila_fifo.pop(0)   # Remove o mais antigo
            return self.frames[vitima_id]

        elif self.algoritmo == 'OPT':
            melhor_frame = None
            maior_distancia = -1

            for frame in self.frames:
                pagina = frame.pagina_alocada
                try:
                    # Próxima ocorrência desta página APÓS a posição atual
                    proxima_pos = self.referencias_futuras.index(
                        pagina, self.posicao_atual + 1
                    )
                    distancia = proxima_pos - self.posicao_atual
                except ValueError:
                    # Página nunca mais será referenciada → vítima ideal
                    return frame

                if distancia > maior_distancia:
                    maior_distancia = distancia
                    melhor_frame = frame

            return melhor_frame

        else:
            raise ValueError(f"Algoritmo '{self.algoritmo}' não suportado neste simulador.")

    # ------------------------------------------------------------------
    # Impressão do mapa de memória a cada passo
    # ------------------------------------------------------------------
    def imprimir_mapa_memoria(self, passo, pagina_acessada, foi_hit, frame_alterado=None):
        status = "Hit" if foi_hit else "Page Fault"
        print(f"\n--- Passo {passo}: Acesso à Página {pagina_acessada} ({status}) ---")

        for frame in self.frames:
            if frame.pagina_alocada is not None:
                conteudo = f"Página {frame.pagina_alocada}"
            else:
                conteudo = "[Vazio]"

            # Marca o frame alterado somente em caso de Page Fault
            marcador = ""
            if not foi_hit and frame.id_frame == frame_alterado:
                marcador = " <-- Alterado"

            print(f"[Frame {frame.id_frame}]: {conteudo}{marcador}")

        print("-" * 40)


# ----------------------------------------------------------------------
# Simulador: lê o arquivo, instancia a TabelaPaginas e conduz a simulação
# ----------------------------------------------------------------------
class Simulador:
    def __init__(self, caminho_arquivo, algoritmo):
        self.caminho_arquivo = caminho_arquivo
        self.algoritmo = algoritmo.upper()

    def _ler_entrada(self):
        try:
            with open(self.caminho_arquivo, 'r', encoding='utf-8') as arquivo:
                linhas = arquivo.readlines()
        except FileNotFoundError:
            print(f"Erro: O arquivo '{self.caminho_arquivo}' não foi encontrado.")
            return None, None

        linhas = [l.strip() for l in linhas if l.strip() and not l.strip().startswith('#')]

        if not linhas:
            print("Erro: Arquivo de entrada vazio.")
            return None, None

        # Primeira linha: quantidade de frames
        num_frames = int(linhas[0])
        # Demais linhas: sequência de acessos às páginas
        sequencia_paginas = [int(l) for l in linhas[1:]]
        return num_frames, sequencia_paginas

    def executar(self):
        num_frames, sequencia_paginas = self._ler_entrada()
        if num_frames is None:
            return None

        tabela_paginas = TabelaPaginas(num_frames, self.algoritmo)

        # OPT precisa da sequência completa antecipadamente (look-ahead)
        if self.algoritmo == 'OPT':
            tabela_paginas.definir_referencias(sequencia_paginas)

        print(f"Iniciando simulação com {num_frames} frames disponíveis. Algoritmo: {self.algoritmo}")
        print("=" * 40)

        for i, pagina in enumerate(sequencia_paginas):
            foi_hit, frame_id = tabela_paginas.acessar_pagina(pagina, indice_atual=i)
            tabela_paginas.imprimir_mapa_memoria(i + 1, pagina, foi_hit, frame_id)

        # Estatísticas finais
        print("\n================ STATS FINAIS ================")
        print(f"Total de Acessos: {tabela_paginas.total_acessos}")
        print(f"Total de Page Faults: {tabela_paginas.total_page_faults}")
        if tabela_paginas.total_acessos > 0:
            taxa = (tabela_paginas.total_page_faults / tabela_paginas.total_acessos) * 100
            print(f"Taxa de Page Faults: {taxa:.2f}%")
        print("==============================================")

        return tabela_paginas


# ----------------------------------------------------------------------
# Comparação final entre os dois algoritmos do grupo (FIFO vs OPT)
# ----------------------------------------------------------------------
def imprimir_comparacao(resultados):
    print("\n\n================ COMPARAÇÃO FINAL (FIFO vs OPT) ================")
    for nome, tabela in resultados.items():
        if tabela is None:
            continue
        taxa = 0.0
        if tabela.total_acessos > 0:
            taxa = (tabela.total_page_faults / tabela.total_acessos) * 100

        mapa_final = ", ".join(
            f"[F{frame.id_frame}]:{frame.pagina_alocada}"
            for frame in tabela.frames
        )

        print(f"\n{nome}:")
        print(f"  Acessos: {tabela.total_acessos}")
        print(f"  Page Faults: {tabela.total_page_faults}")
        print(f"  Taxa de Page Faults: {taxa:.2f}%")
        print(f"  Memória Final: {mapa_final}")
    print("==================================================================")


# ----------------------------------------------------------------------
# Ponto de entrada
# Uso: python simulador_memoria.py [arquivo] [algoritmo]
# Exemplos:
#   python simulador_memoria.py entrada.txt          -> executa FIFO e OPT e compara
#   python simulador_memoria.py entrada.txt FIFO     -> executa apenas FIFO
#   python simulador_memoria.py entrada.txt OPT      -> executa apenas OPT
# ----------------------------------------------------------------------
if __name__ == "__main__":
    arquivo_entrada = "entrada.txt"
    algoritmo = None  # None = executa ambos (FIFO e OPT) e compara

    if len(sys.argv) > 1:
        arquivo_entrada = sys.argv[1]
    if len(sys.argv) > 2:
        algoritmo = sys.argv[2].upper()
        if algoritmo not in ('FIFO', 'OPT'):
            print(f"Algoritmo '{algoritmo}' inválido para o Grupo 04. Use FIFO ou OPT.")
            sys.exit(1)

    if algoritmo is None:
        resultados = {}
        for nome in ('FIFO', 'OPT'):
            simulador = Simulador(arquivo_entrada, nome)
            resultados[nome] = simulador.executar()
            print()
        imprimir_comparacao(resultados)
    else:
        simulador = Simulador(arquivo_entrada, algoritmo)
        simulador.executar()
