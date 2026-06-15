###
###     T E S T E S   U N I T Á R I O S
###     Grupo 04 - FIFO vs. Ótimo (OPT) - 4 Frames
###

import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from simulador_memoria import TabelaPaginas, Simulador


class TestHitsEFaults(unittest.TestCase):

    def test_fault_em_frame_vazio(self):
        tabela = TabelaPaginas(2, 'FIFO')

        foi_hit, frame_id = tabela.acessar_pagina(1, indice_atual=0)

        self.assertFalse(foi_hit)
        self.assertEqual(frame_id, 0)
        self.assertEqual(tabela.total_acessos, 1)
        self.assertEqual(tabela.total_page_faults, 1)
        self.assertEqual(tabela.frames[0].pagina_alocada, 1)

    def test_hit_nao_incrementa_faults(self):
        tabela = TabelaPaginas(2, 'FIFO')

        tabela.acessar_pagina(1, indice_atual=0)  # fault
        foi_hit, frame_id = tabela.acessar_pagina(1, indice_atual=1)  # hit

        self.assertTrue(foi_hit)
        self.assertEqual(frame_id, 0)
        self.assertEqual(tabela.total_acessos, 2)
        self.assertEqual(tabela.total_page_faults, 1)


class TestSubstituicaoFIFO(unittest.TestCase):

    def test_substitui_pagina_mais_antiga(self):
        tabela = TabelaPaginas(2, 'FIFO')

        tabela.acessar_pagina(1, indice_atual=0)  # frame0 = 1
        tabela.acessar_pagina(2, indice_atual=1)  # frame1 = 2

        # memória cheia: 3 deve substituir a página 1 (mais antiga)
        foi_hit, frame_id = tabela.acessar_pagina(3, indice_atual=2)

        self.assertFalse(foi_hit)
        self.assertEqual(frame_id, 0)
        self.assertEqual(tabela.frames[0].pagina_alocada, 3)
        self.assertEqual(tabela.frames[1].pagina_alocada, 2)
        self.assertEqual(tabela.total_page_faults, 3)


class TestSubstituicaoOPT(unittest.TestCase):

    def test_vitima_nunca_mais_referenciada(self):
        # Sequência: 1, 2, 3, 1, 4
        referencias = [1, 2, 3, 1, 4]
        tabela = TabelaPaginas(2, 'OPT')
        tabela.definir_referencias(referencias)

        tabela.acessar_pagina(1, indice_atual=0)  # frame0 = 1
        tabela.acessar_pagina(2, indice_atual=1)  # frame1 = 2

        # memória cheia: page 2 (frame1) nunca mais será usada -> vítima
        foi_hit, frame_id = tabela.acessar_pagina(3, indice_atual=2)

        self.assertFalse(foi_hit)
        self.assertEqual(frame_id, 1)
        self.assertEqual(tabela.frames[1].pagina_alocada, 3)
        self.assertEqual(tabela.frames[0].pagina_alocada, 1)

    def test_vitima_com_proximo_uso_mais_distante(self):
        # Sequência: 1, 2, 3, 2, 1, 4
        referencias = [1, 2, 3, 2, 1, 4]
        tabela = TabelaPaginas(2, 'OPT')
        tabela.definir_referencias(referencias)

        tabela.acessar_pagina(1, indice_atual=0)  # frame0 = 1
        tabela.acessar_pagina(2, indice_atual=1)  # frame1 = 2

        # memória cheia: página 1 (frame0) só volta a ser usada na posição 4,
        # enquanto a página 2 (frame1) volta na posição 3 -> 1 é a vítima
        foi_hit, frame_id = tabela.acessar_pagina(3, indice_atual=2)

        self.assertFalse(foi_hit)
        self.assertEqual(frame_id, 0)
        self.assertEqual(tabela.frames[0].pagina_alocada, 3)
        self.assertEqual(tabela.frames[1].pagina_alocada, 2)


class TestSimuladorArquivoEntrada(unittest.TestCase):

    CAMINHO_ENTRADA = os.path.join(os.path.dirname(__file__), '..', 'entrada.txt')

    def test_estatisticas_fifo(self):
        simulador = Simulador(self.CAMINHO_ENTRADA, 'FIFO')
        tabela = simulador.executar()

        self.assertEqual(tabela.total_acessos, 12)
        self.assertEqual(tabela.total_page_faults, 7)
        taxa = (tabela.total_page_faults / tabela.total_acessos) * 100
        self.assertAlmostEqual(taxa, 58.33, places=2)

    def test_estatisticas_opt(self):
        simulador = Simulador(self.CAMINHO_ENTRADA, 'OPT')
        tabela = simulador.executar()

        self.assertEqual(tabela.total_acessos, 12)
        self.assertEqual(tabela.total_page_faults, 6)
        taxa = (tabela.total_page_faults / tabela.total_acessos) * 100
        self.assertAlmostEqual(taxa, 50.00, places=2)

    def test_arquivo_inexistente_nao_lanca_excecao(self):
        simulador = Simulador('arquivo_que_nao_existe.txt', 'FIFO')
        resultado = simulador.executar()

        self.assertIsNone(resultado)


if __name__ == '__main__':
    unittest.main()
