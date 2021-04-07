# Rotinas de testes associadas ao arquivo parp.dat do NEWAVE
from typing import Callable, List, Dict

import numpy as np  # type: ignore
from inewave.config import MESES, REES
from inewave.newave.parp import LeituraPARp
from inewave.newave.modelos.parp import PARp
from tests.newave import DIR_TESTES

ARQ_PARP = "parp_parp.dat"
ARQ_PARPA = "parp_parpa.dat"
ARQ_PARPA_SEM_REDORDEM = "parp_parpa_sem_redordem.dat"


# Classe para realizar testes com o parp.dat
class TestesPARp:
    __test__ = False

    def __init__(self,
                 parp: PARp,
                 usa_parpa: bool,
                 ano_pmo: int,
                 num_cfgs: int,
                 num_anos_estudo: int) -> None:
        self.parp = parp
        self.usa_parpa = usa_parpa
        self.ano_pmo = ano_pmo
        self.num_cfgs = num_cfgs
        self.num_anos_estudo = num_anos_estudo

    @staticmethod
    def _dimensoes_dict(func: Callable[[int],
                                       Dict[int, np.ndarray]],
                        num_chaves: int,
                        dim_desejada: tuple) -> bool:
        dims: List[bool] = []
        for i_ree, ree in enumerate(REES):
            # Variáveis auxiliares
            elems = func(i_ree + 1)
            chaves = list(elems.keys())
            # Condição do teste
            b = len(chaves) == num_chaves
            for _, serie in elems.items():
                b = b and serie.shape == dim_desejada
            dims.append(b)
        return all(dims)

    @staticmethod
    def _dimensoes_list(func: Callable[[int],
                                       List[np.ndarray]],
                        num_elementos_desejados: int) -> bool:
        dims: List[bool] = []
        for i_ree, ree in enumerate(REES):
            # Variáveis auxiliares
            elems = func(i_ree + 1)
            # Condição do teste
            b = len(elems) == num_elementos_desejados
            dims.append(b)
        return all(dims)

    def dimensoes_series_energia(self) -> bool:
        return self._dimensoes_dict(self.parp.series_energia_ree,
                                    self.num_cfgs,
                                    (self.ano_pmo - 2 - 1931 + 1,
                                     len(MESES))
                                    )

    def dimensoes_correl_energia(self) -> bool:
        return TestesPARp._dimensoes_dict(self.parp.correlograma_energia_ree,
                                          self.num_anos_estudo * len(MESES),
                                          (len(MESES) - 1,)
                                          )

    def dimensoes_ordens_finais(self) -> bool:
        return TestesPARp._dimensoes_dict(self.parp.ordens_finais_ree,
                                          self.num_anos_estudo,
                                          (len(MESES),)
                                          )

    def dimensoes_ordens_originais(self) -> bool:
        return TestesPARp._dimensoes_dict(self.parp.ordens_originais_ree,
                                          self.num_anos_estudo,
                                          (len(MESES),)
                                          )

    def dimensoes_coeficientes(self) -> bool:
        return TestesPARp._dimensoes_list(self.parp.coeficientes_ree,
                                          self.num_anos_estudo * len(MESES))

    def dimensoes_contribuicoes(self) -> bool:
        return TestesPARp._dimensoes_list(self.parp.contribuicoes_ree,
                                          self.num_anos_estudo * len(MESES))

    def dimensoes_correl_esp_anual(self) -> bool:
        dims: List[bool] = []
        elems = self.parp.correlacoes_espaciais_anuais
        cfgs = list(elems.keys())
        b = len(cfgs) == self.num_cfgs
        for cfg in cfgs:
            chaves_rees = list(elems[cfg].keys())
            b = b and len(chaves_rees) == len(REES)
            for ree in chaves_rees:
                chaves_internas_rees = list(elems[cfg][ree].keys())
                b = b and len(chaves_internas_rees) == len(REES)
            dims.append(b)
        return all(dims)

    def dimensoes_correl_esp_mensal(self) -> bool:
        dims: List[bool] = []
        elems = self.parp.correlacoes_espaciais_mensais
        cfgs = list(elems.keys())
        b = len(cfgs) == self.num_cfgs
        for cfg in cfgs:
            chaves_rees = list(elems[cfg].keys())
            b = b and len(chaves_rees) == len(REES)
            for ree in chaves_rees:
                chaves_internas_rees = list(elems[cfg][ree].keys())
                b = b and len(chaves_internas_rees) == len(REES)
                for ree_interna in chaves_internas_rees:
                    correls = elems[cfg][ree][ree_interna]
                    b = b and correls.shape == (len(MESES), )
            dims.append(b)
        return all(dims)

    def dimensoes_series_medias(self) -> bool:
        return TestesPARp._dimensoes_dict(self.parp.series_medias_ree,
                                          self.num_anos_estudo,
                                          (self.ano_pmo - 2 - 1931 + 1,
                                           len(MESES))
                                          )

    def dimensoes_correl_medias(self) -> bool:
        return TestesPARp._dimensoes_dict(self.parp.correlograma_media_ree,
                                          self.num_anos_estudo * len(MESES),
                                          (len(MESES),)
                                          )


# Testes com o parp.dat de um PMO sem PAR(p)-A
parp_parp = LeituraPARp(DIR_TESTES).le_arquivo(ARQ_PARP)
teste_parp_parp = TestesPARp(parp_parp,
                             False,
                             2020,
                             60,
                             10)


def test_dimensao_series_energia_parp_parp():
    assert teste_parp_parp.dimensoes_series_energia()


def test_dimensao_series_medias_parp_parp():
    assert not teste_parp_parp.dimensoes_series_medias()


def test_dimensao_correl_energia_parp_parp():
    assert teste_parp_parp.dimensoes_correl_energia()


def test_dimensao_correl_medias_parp_parp():
    assert not teste_parp_parp.dimensoes_correl_medias()


def test_dimensao_ordens_finais_parp_parp():
    assert teste_parp_parp.dimensoes_ordens_finais()


def test_dimensao_ordens_originais_parp_parp():
    assert teste_parp_parp.dimensoes_ordens_originais()


def test_dimensao_coeficientes_parp_parp():
    assert teste_parp_parp.dimensoes_coeficientes()


def test_dimensao_contribuicoes_parp_parp():
    assert teste_parp_parp.dimensoes_contribuicoes()


def test_dimensao_correl_esp_anual_parp_parp():
    assert teste_parp_parp.dimensoes_correl_esp_anual()


def test_dimensao_correl_esp_mensal_parp_parp():
    assert teste_parp_parp.dimensoes_correl_esp_mensal()


# Testes com o parp.dat de um PMO com PAR(p)-A
parp_parpa = LeituraPARp(DIR_TESTES).le_arquivo(ARQ_PARPA)
teste_parp_parpa = TestesPARp(parp_parpa,
                              True,
                              2020,
                              50,
                              10)


def test_dimensao_series_energia_parp_parpa():
    assert teste_parp_parpa.dimensoes_series_energia()


def test_dimensao_series_medias_parp_parpa():
    assert teste_parp_parpa.dimensoes_series_medias()


def test_dimensao_correl_energia_parp_parpa():
    assert teste_parp_parpa.dimensoes_correl_energia()


def test_dimensao_correl_medias_parp_parpa():
    assert teste_parp_parpa.dimensoes_correl_medias()


def test_dimensao_ordens_finais_parp_parpa():
    assert teste_parp_parpa.dimensoes_ordens_finais()


def test_dimensao_ordens_originais_parp_parpa():
    assert teste_parp_parpa.dimensoes_ordens_originais()


def test_dimensao_coeficientes_parp_parpa():
    assert teste_parp_parpa.dimensoes_coeficientes()


def test_dimensao_contribuicoes_parp_parpa():
    assert teste_parp_parpa.dimensoes_contribuicoes()


def test_dimensao_correl_esp_anual_parp_parpa():
    assert teste_parp_parpa.dimensoes_correl_esp_anual()


def test_dimensao_correl_esp_mensal_parp_parpa():
    assert teste_parp_parpa.dimensoes_correl_esp_mensal()


# Testes com o parp.dat de um PMO com PAR(p)-A sem Red. Ordem
parp_parpa_sem_red = LeituraPARp(DIR_TESTES).le_arquivo(ARQ_PARPA_SEM_REDORDEM)
teste_parp_parpa_sem_red = TestesPARp(parp_parpa_sem_red,
                                      True,
                                      2020,
                                      50,
                                      10)


def test_dimensao_series_energia_parp_parpa_sem_red():
    assert teste_parp_parpa_sem_red.dimensoes_series_energia()


def test_dimensao_series_medias_parp_parpa_sem_red():
    assert teste_parp_parpa_sem_red.dimensoes_series_medias()


def test_dimensao_correl_energia_parp_parpa_sem_red():
    assert teste_parp_parpa_sem_red.dimensoes_correl_energia()


def test_dimensao_correl_medias_parp_parpa_sem_red():
    assert teste_parp_parpa_sem_red.dimensoes_correl_medias()


def test_dimensao_ordens_finais_parp_parpa_sem_red():
    assert teste_parp_parpa_sem_red.dimensoes_ordens_finais()


def test_dimensao_ordens_originais_parp_parpa_sem_red():
    assert teste_parp_parpa_sem_red.dimensoes_ordens_originais()


def test_dimensao_coeficientes_parp_parpa_sem_red():
    assert teste_parp_parpa_sem_red.dimensoes_coeficientes()


def test_dimensao_contribuicoes_parp_parpa_sem_red():
    assert teste_parp_parpa_sem_red.dimensoes_contribuicoes()


def test_dimensao_correl_esp_anual_parp_parpa_sem_red():
    assert teste_parp_parpa_sem_red.dimensoes_correl_esp_anual()


def test_dimensao_correl_esp_mensal_parp_parpa_sem_red():
    assert teste_parp_parpa_sem_red.dimensoes_correl_esp_mensal()

# def test_eq_parp():
#     leitor2 = LeituraPARp("tests/_arquivos")
#     leitor2.le_arquivo()
#     assert leitor.parp == leitor2.parp


# def test_neq_parp():
#     leitor2 = LeituraPARp("tests/_arquivos")
#     leitor2.le_arquivo()
#     leitor2.parp.ordens_orig[1] = np.array([])
#     assert leitor2.parp != leitor.parp
#     assert leitor2.parp is not None


# def test_series_energia_ree():
#     series = leitor.parp.series_energia_ree(1)
#     assert len(series.keys()) == 50
#     # Confere valores aleatórios para validar
#     assert series[38][0, 0] == 8428.04
#     assert series[44][6, 4] == 4855.95
#     assert series[44][10, 11] == 7472.84


# def test_series_medias_ree():
#     series = leitor.parp.series_medias_ree(1)
#     assert len(series.keys()) == 10
#     assert not any(series[2024][0, :])
#     # Confere valores aleatórios para validar
#     assert series[2020][9, 0] == 5266.78


# def test_correlograma_energia_ree():
#     correl = leitor.parp.correlograma_energia_ree(1)
#     assert len(correl.keys()) == 5 * n_meses
#     # Confere valores aleatórios para validar
#     assert correl[1][0] == 0.18930
#     assert correl[25][5] == -0.02014


# def test_correlograma_media_ree():
#     correl = leitor.parp.correlograma_media_ree(1)
#     assert len(correl.keys()) == 5 * n_meses
#     # Confere valores aleatórios para validar
#     assert correl[1][0] == 0.29324
#     assert correl[60][5] == 0.88305


# def test_ordens_originais_ree():
#     ordens = leitor.parp.ordens_originais_ree(1)
#     assert len(ordens.keys()) == 10
#     # Confere valores aleatórios para validar
#     assert ordens[2020][1] == 2
#     assert ordens[2024][5] == 6


# def test_ordens_finais_ree():
#     ordens = leitor.parp.ordens_finais_ree(1)
#     assert len(ordens.keys()) == 10
#     # Confere valores aleatórios para validar
#     assert ordens[2020][1] == 1
#     assert ordens[2024][5] == 1


# def test_coeficientes_ree():
#     coefs = leitor.parp.coeficientes_ree(1)
#     assert len(coefs) == 10 * n_meses
#     # Confere valores aleatórios para validar
#     assert len(coefs[0]) == 2
#     assert coefs[0][0] == 0.203
#     assert len(coefs[23]) == 5
#     assert coefs[23][-1] == -0.218


# def test_contribuicoes_ree():
#     contribs = leitor.parp.contribuicoes_ree(1)
#     assert len(contribs) == 10 * n_meses
#     # Confere valores aleatórios para validar
#     assert len(contribs[0]) == 2
#     assert contribs[0][0] == 0.261
#     assert len(contribs[23]) == 5
#     assert contribs[23][-1] == -0.475


# def test_correlacoes_espaciais_ano_configuracao():
#     corrs = leitor.parp.correlacoes_espaciais_anuais
#     n_rees = len(REES)
#     assert len(corrs.keys()) == 3
#     assert all([corrs[1][i][i] == 1
#                 for i in range(1, n_rees + 1)])
#     # Confere valores aleatórios para validar
#     corrs[1][1][2] == -0.1809


# def test_correlacoes_espaciais_mes_configuracao():
#     corrs = leitor.parp.correlacoes_espaciais_mensais
#     assert len(corrs.keys()) == 3
#     # Confere valores aleatórios para validar
#     assert corrs[1][1][2][0] == -0.3822
#     assert corrs[1][1][2][11] == -0.4190
