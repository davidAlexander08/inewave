from inewave.config import MESES_DF, MAX_PATAMARES, MAX_SERIES_SINTETICAS

from cfinterface.components.block import Block
from cfinterface.components.line import Line
from cfinterface.components.field import Field
from cfinterface.components.integerfield import IntegerField
from cfinterface.components.literalfield import LiteralField
from cfinterface.components.floatfield import FloatField
from typing import List, IO
import numpy as np  # type: ignore
import pandas as pd  # type: ignore


class Submercado(Block):
    """
    Bloco com a informaçao do submercado associado aos valores de Custo
    Marginal de Operação.
    """

    BEGIN_PATTERN = r"CUSTO MARGINAL DE DEMANDA \(\$/MWh\)"
    END_PATTERN = ""

    def __init__(self, previous=None, next=None, data=None) -> None:
        super().__init__(previous, next, data)
        self.__linha = Line([LiteralField(12, 70)])

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, Submercado):
            return False
        bloco: Submercado = o
        if not all(
            [
                isinstance(self.data, str),
                isinstance(o.data, str),
            ]
        ):
            return False
        else:
            return self.data == bloco.data

    # Override
    def read(self, file: IO):
        self.data = self.__linha.read(file.readline())[0]


class CmargsAnos(Block):
    """
    Bloco com a informaçao do submercado associado aos valores de Custo
    Marginal de Operação.
    """

    BEGIN_PATTERN = "     ANO: "
    END_PATTERN = "  MEDIA"

    def __init__(self, previous=None, next=None, data=None) -> None:
        super().__init__(previous, next, data)
        self.__linha_ano = Line([IntegerField(4, 10)])
        campos_serie_patamar: List[Field] = [
            IntegerField(4, 2),
            IntegerField(2, 9),
        ]
        campos_custos: List[Field] = [
            FloatField(8, 15 + 9 * i, 2) for i in range(len(MESES_DF) + 1)
        ]
        self.__linha = Line(campos_serie_patamar + campos_custos)

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, CmargsAnos):
            return False
        bloco: CmargsAnos = o
        if not all(
            [
                isinstance(self.data, pd.DataFrame),
                isinstance(o.data, pd.DataFrame),
            ]
        ):
            return False
        else:
            return self.data.equals(bloco.data)

    # Override
    def read(self, file: IO):
        def converte_tabela_em_df():
            cols = ["Série", "Patamar"] + MESES_DF + ["Média"]
            df = pd.DataFrame(tabela, columns=cols)
            df["Ano"] = self.__ano
            df = df[["Ano"] + cols]
            df = df.astype(
                {"Série": "int64", "Patamar": "int64", "Ano": "int64"}
            )
            return df

        self.__ano = self.__linha_ano.read(file.readline())[0]
        file.readline()

        # Variáveis auxiliares
        self.__serie_atual = 0
        tabela = np.zeros(
            (MAX_PATAMARES * MAX_SERIES_SINTETICAS, len(MESES_DF) + 3)
        )
        i = 0
        while True:
            linha = file.readline()
            if self.ends(linha):
                tabela = tabela[:i, :]
                self.data = converte_tabela_em_df()
                break
            dados = self.__linha.read(linha)
            if dados[0] is not None:
                self.__serie_atual = dados[0]
            tabela[i, 0] = self.__serie_atual
            tabela[i, 1:] = dados[1:]
            i += 1
