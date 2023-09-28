from inewave.nwlistop.vmort import Vmort

from datetime import datetime
from tests.mocks.mock_open import mock_open
from unittest.mock import MagicMock, patch

from tests.mocks.arquivos.vmort import MockVmort

ARQ_TESTE = "./tests/mocks/arquivos/__init__.py"


def test_atributos_encontrados_vmort():
    m: MagicMock = mock_open(read_data="".join(MockVmort))
    with patch("builtins.open", m):
        n = Vmort.read(ARQ_TESTE)
        assert n.valores is not None
        assert n.valores.iloc[0, 0] == datetime(2020, 1, 1)
        assert n.valores.iloc[-1, -1] == 0.0
        assert n.ree is not None
        assert n.ree == "SUDESTE"


def test_atributos_nao_encontrados_vmort():
    m: MagicMock = mock_open(read_data="")
    with patch("builtins.open", m):
        n = Vmort.read(ARQ_TESTE)
        assert n.valores is None
        assert n.ree is None


def test_eq_vmort():
    m: MagicMock = mock_open(read_data="".join(MockVmort))
    with patch("builtins.open", m):
        n1 = Vmort.read(ARQ_TESTE)
        n2 = Vmort.read(ARQ_TESTE)
        assert n1 == n2


# Não deve ter teste de diferença, visto que o atributo é
# implementado como Lazy Property.
