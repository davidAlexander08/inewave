from inewave.nwlistcf.modelos.arquivos import BlocoNomesArquivos

from cfinterface.files.sectionfile import SectionFile

from typing import List, TypeVar, Type, Optional
import pandas as pd  # type: ignore

# Para compatibilidade - até versão 1.0.0
from os.path import join
import warnings


class Arquivos(SectionFile):
    """
    Armazena os dados de entrada do NWLISTCF referentes ao arquivo
    `arquivos.dat`.

    Esta classe lida com informações de entrada do NWLISTCF e
    que deve se referir aos nomes dos demais arquivos de entrada
    utilizados para o caso em questão.

    """

    T = TypeVar("T")

    SECTIONS = [BlocoNomesArquivos]

    @classmethod
    def le_arquivo(
        cls, diretorio: str, nome_arquivo="arquivos.dat"
    ) -> "Arquivos":
        msg = (
            "O método le_arquivo(diretorio, nome_arquivo) será descontinuado"
            + " na versão 1.0.0 - use o método read(caminho_arquivo)"
        )
        warnings.warn(msg, category=FutureWarning)
        return cls.read(join(diretorio, nome_arquivo))

    def escreve_arquivo(self, diretorio: str, nome_arquivo="arquivos.dat"):
        msg = (
            "O método escreve_arquivo(diretorio, nome_arquivo) será"
            + " descontinuado na versão 1.0.0 -"
            + " use o método write(caminho_arquivo)"
        )
        warnings.warn(msg, category=FutureWarning)
        self.write(join(diretorio, nome_arquivo))

    def __bloco_por_tipo(self, bloco: Type[T], indice: int) -> Optional[T]:
        """
        Obtém um gerador de blocos de um tipo, se houver algum no arquivo.

        :param bloco: Um tipo de bloco para ser lido
        :type bloco: T
        :param indice: O índice do bloco a ser acessado, dentre os do tipo
        :type indice: int
        :return: O gerador de blocos, se houver
        :rtype: Optional[Generator[T], None, None]
        """
        try:
            return next(
                b
                for i, b in enumerate(self.data.of_type(bloco))
                if i == indice
            )
        except StopIteration:
            return None

    def __le_nome_por_indice(self, indice: int) -> Optional[str]:
        b = self.__bloco_por_tipo(BlocoNomesArquivos, 0)
        if b is not None:
            if indice in b.data.index:
                dado = b.data.iloc[indice, 1]
                if isinstance(dado, str):
                    return dado
        return None

    def __atualiza_nome_por_indice(self, indice: int, nome: str):
        b = self.__bloco_por_tipo(BlocoNomesArquivos, 0)
        if b is not None:
            dif = indice - b.data.shape[0] + 1
            if dif > 0:
                col_vazia = [None] * dif
                b.data = pd.concat(
                    [
                        b.data,
                        pd.DataFrame(
                            data={
                                "Legenda": col_vazia,
                                "Nome": col_vazia,
                            }
                        ),
                    ],
                    ignore_index=True,
                )
            b.data.iloc[indice, 1] = nome

    @property
    def arquivos(self) -> List[str]:
        """
        Os nomes dos arquivos utilizados.

        :return: Os arquivos na mesma ordem em que são declarados
        :rtype: List[str]
        """
        b = self.__bloco_por_tipo(BlocoNomesArquivos, 0)
        return [] if b is None else b.data.iloc[:, 1]

    @property
    def nwlistcf(self) -> Optional[str]:
        """
        Nome do arquivo de dados gerais utilizado pelo NWLISTCF.
        """
        return self.__le_nome_por_indice(0)

    @nwlistcf.setter
    def nwlistcf(self, arq: str):
        self.__atualiza_nome_por_indice(0, arq)

    @property
    def cortes(self) -> Optional[str]:
        """
        Nome do arquivo de cortes gerado pelo NEWAVE.
        """
        return self.__le_nome_por_indice(1)

    @cortes.setter
    def cortes(self, arq: str):
        self.__atualiza_nome_por_indice(1, arq)

    @property
    def cortesh(self) -> Optional[str]:
        """
        Nome do arquivo de cabeçalho de cortes produzido pelo NEWAVE.
        """
        return self.__le_nome_por_indice(2)

    @cortesh.setter
    def cortesh(self, arq: str):
        self.__atualiza_nome_por_indice(2, arq)

    @property
    def newdesp(self) -> Optional[str]:
        """
        Nome do arquivo para despacho hidrotérmico produzido pelo NEWAVE.
        """
        return self.__le_nome_por_indice(3)

    @newdesp.setter
    def newdesp(self, arq: str):
        self.__atualiza_nome_por_indice(3, arq)

    @property
    def cortese(self) -> Optional[str]:
        """
        Nome do arquivo dos estados dos cortes produzido pelo NEWAVE.
        """
        return self.__le_nome_por_indice(4)

    @cortese.setter
    def cortese(self, arq: str):
        self.__atualiza_nome_por_indice(4, arq)

    @property
    def energiaf(self) -> Optional[str]:
        """
        Nome do arquivo com as energias para simulação
        forward produzido pelo NEWAVE.
        """
        return self.__le_nome_por_indice(5)

    @energiaf.setter
    def energiaf(self, arq: str):
        self.__atualiza_nome_por_indice(5, arq)

    @property
    def rsar(self) -> Optional[str]:
        """
        Nome do arquivo com restrições SAR produzido pelo NEWAVE.
        """
        return self.__le_nome_por_indice(6)

    @rsar.setter
    def rsar(self, arq: str):
        self.__atualiza_nome_por_indice(6, arq)

    @property
    def rsarh(self) -> Optional[str]:
        """
        Nome do arquivo com cabeçalho da SAR produzido pelo NEWAVE.
        """
        return self.__le_nome_por_indice(7)

    @rsarh.setter
    def rsarh(self, arq: str):
        self.__atualiza_nome_por_indice(7, arq)

    @property
    def rsari(self) -> Optional[str]:
        """
        Nome do arquivo de índice da SAR produzido pelo NEWAVE.
        """
        return self.__le_nome_por_indice(8)

    @rsari.setter
    def rsari(self, arq: str):
        self.__atualiza_nome_por_indice(8, arq)

    @property
    def relatorio_cortes(self) -> Optional[str]:
        """
        Nome do arquivo com a saída do NWLISTCF contendo os
        cortes produzidos pelo NEWAVE.
        """
        return self.__le_nome_por_indice(9)

    @relatorio_cortes.setter
    def relatorio_cortes(self, arq: str):
        self.__atualiza_nome_por_indice(9, arq)

    @property
    def relatorio_estados(self) -> Optional[str]:
        """
        Nome do arquivo com a saída do NWLISTCF contendo os
        estados visitados pelo NEWAVE.
        """
        return self.__le_nome_por_indice(10)

    @relatorio_estados.setter
    def relatorio_estados(self, arq: str):
        self.__atualiza_nome_por_indice(10, arq)

    @property
    def relatorio_rsar(self) -> Optional[str]:
        """
        Nome do arquivo com a saída do NWLISTCF contendo os
        a SAR utilizada pelo NEWAVE.
        """
        return self.__le_nome_por_indice(11)

    @relatorio_rsar.setter
    def relatorio_rsar(self, arq: str):
        self.__atualiza_nome_por_indice(11, arq)

    @property
    def energiaxf(self) -> Optional[str]:
        """
        Nome do arquivo com as médias móveis das energias
        para simulação forward produzido pelo NEWAVE.
        """
        return self.__le_nome_por_indice(12)

    @energiaxf.setter
    def energiaxf(self, arq: str):
        self.__atualiza_nome_por_indice(12, arq)

    @property
    def vazaof(self) -> Optional[str]:
        """
        Nome do arquivo com as vazões para simulação
        forward produzido pelo NEWAVE.
        """
        return self.__le_nome_por_indice(13)

    @vazaof.setter
    def vazaof(self, arq: str):
        self.__atualiza_nome_por_indice(13, arq)

    @property
    def vazaoxf(self) -> Optional[str]:
        """
        Nome do arquivo com as médias móveis de vazões
        para simulação forward produzido pelo NEWAVE.
        """
        return self.__le_nome_por_indice(14)

    @vazaoxf.setter
    def vazaoxf(self, arq: str):
        self.__atualiza_nome_por_indice(14, arq)
