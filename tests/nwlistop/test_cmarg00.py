from inewave.nwlistop.cmarg00 import Cmarg00

from tests.mocks.mock_open import mock_open
from unittest.mock import MagicMock, patch

from tests.mocks.arquivos.cmarg00 import MockCmarg00


def test_atributos_encontrados_cmarg00():
    m: MagicMock = mock_open(read_data="".join(MockCmarg00))
    with patch("builtins.open", m):
        n = Cmarg00.le_arquivo("")
        assert n.custos is not None
        assert n.submercado is not None


def test_atributos_nao_encontrados_cmarg00():
    m: MagicMock = mock_open(read_data="")
    with patch("builtins.open", m):
        n = Cmarg00.le_arquivo("")
        assert n.custos is None
        assert n.submercado is None


def test_eq_cmarg00():
    m: MagicMock = mock_open(read_data="".join(MockCmarg00))
    with patch("builtins.open", m):
        n1 = Cmarg00.le_arquivo("")
        n2 = Cmarg00.le_arquivo("")
        assert n1 == n2


# Não deve ter teste de diferença, visto que o atributo é
# implementado como Lazy Property.
