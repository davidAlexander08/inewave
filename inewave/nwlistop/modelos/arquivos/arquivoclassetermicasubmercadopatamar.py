from inewave.nwlistop.modelos.blocos.submercado import Submercado
from inewave.nwlistop.modelos.blocos.valoresclassetermicaseriepatamar import (
    ValoresClasseTermicaSeriePatamar,
)

from cfinterface.files.blockfile import BlockFile
import pandas as pd  # type: ignore
from typing import TypeVar, Optional


class ArquivoClasseTermicaSubmercadoPatamar(BlockFile):
    """
    Armazena os dados das saídas por patamar, por submercado e por
    classe térmica.
    """

    T = TypeVar("T")

    BLOCKS = [Submercado, ValoresClasseTermicaSeriePatamar]

    def __init__(self, data=...) -> None:
        super().__init__(data)
        self.__valores = None

    @classmethod
    def le_arquivo(
        cls, diretorio: str, nome_arquivo="arq.out"
    ) -> "ArquivoClasseTermicaSubmercadoPatamar":
        return cls.read(diretorio, nome_arquivo)

    def escreve_arquivo(self, diretorio: str, nome_arquivo="arq.out"):
        self.write(diretorio, nome_arquivo)

    def __monta_tabela(self) -> pd.DataFrame:
        df = None
        for b in self.data.of_type(ValoresClasseTermicaSeriePatamar):
            dados = b.data
            if dados is None:
                continue
            elif df is None:
                df = b.data
            else:
                df = pd.concat([df, b.data], ignore_index=True)
        return df

    @property
    def valores(self) -> Optional[pd.DataFrame]:
        """
        Tabela com os valores por classe térmica, por patamar, por série e
        por mês/ano de estudo.

        - classe (`str`)
        - data (`datetime`)
        - patamar (`str`)
        - serie (`str`)
        - valor (`float`)

        :return: A tabela dos valores por patamar.
        :rtype: pd.DataFrame | None
        """
        if self.__valores is None:
            self.__valores = self.__monta_tabela()
        return self.__valores

    @property
    def submercado(self) -> Optional[str]:
        """
        O submercado associado ao arquivo lido.

        :return: Os nome do submercado
        :rtype: str
        """
        b = self.data.get_blocks_of_type(Submercado)
        if isinstance(b, Submercado):
            return b.data
        return None
