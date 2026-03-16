import pytest
from pathlib import Path

FIXTURES_DIR = Path(__file__).parent / "fixtures"


@pytest.fixture
def fixtures_dir():
    return FIXTURES_DIR


@pytest.fixture
def simple_tool_dir():
    return FIXTURES_DIR / "simple_tool"


@pytest.fixture
def simple_vehicle_dir():
    return FIXTURES_DIR / "simple_vehicle"


@pytest.fixture
def complex_mod_dir():
    return FIXTURES_DIR / "complex_mod"


@pytest.fixture
def already_v2_dir():
    return FIXTURES_DIR / "already_v2"


@pytest.fixture
def tmp_output(tmp_path):
    """Temporary output directory for test results."""
    out = tmp_path / "output"
    out.mkdir()
    return out
