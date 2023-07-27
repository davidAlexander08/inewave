from inewave.nwlistop.varmuh import Varmuh

from tests.mocks.mock_open import mock_open
from unittest.mock import MagicMock, patch

from tests.mocks.arquivos.varmuh import MockVarmUH

ARQ_TESTE = "./tests/mocks/arquivos/__init__.py"


def test_atributos_encontrados_varmuh():
    m: MagicMock = mock_open(read_data="".join(MockVarmUH))
    with patch("builtins.open", m):
        n = Varmuh.read(ARQ_TESTE)
        assert n.usina is not None
        assert n.usina == "CAMARGOS"
        assert n.valores is not None
        assert n.valores.iloc[0, 0] == 2022
        assert n.valores.iloc[-1, -1] == 662.80


def test_atributos_nao_encontrados_varmuh():
    m: MagicMock = mock_open(read_data="")
    with patch("builtins.open", m):
        n = Varmuh.read(ARQ_TESTE)
        assert n.usina is None
        assert n.valores is None


def test_eq_varmuh():
    m: MagicMock = mock_open(read_data="".join(MockVarmUH))
    with patch("builtins.open", m):
        n1 = Varmuh.read(ARQ_TESTE)
        n2 = Varmuh.read(ARQ_TESTE)
        assert n1 == n2


# Não deve ter teste de diferença, visto que o atributo é
# implementado como Lazy Property.
