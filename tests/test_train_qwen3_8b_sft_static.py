from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "train_qwen3_8b_sft.sh"


def test_sft_launcher_exports_wrapper_environment_contract() -> None:
    text = SCRIPT.read_text(encoding="utf-8")

    assert 'DEP_TARGET="${DEP_TARGET:-${PYTHON_DEPS_DIR:-${RUN_DIR}/python_deps}}"' in text
    assert 'LF="${LF:-${LLAMAFACTORY_DIR}}"' in text
    assert 'MCORE_ADAPTER_DIR="${MCORE_ADAPTER_DIR:-${REPO_ROOT}/code/mcore_adapter}"' in text
    assert "export DEP_TARGET LF LLAMAFACTORY_CLI MCORE_ADAPTER_DIR" in text
    assert 'export DEP_TARGET="${DEP_TARGET}"' in text
    assert 'export LF="${LF}"' in text


def test_sft_launcher_uses_configurable_llamafactory_cli() -> None:
    text = SCRIPT.read_text(encoding="utf-8")

    assert 'LLAMAFACTORY_CLI="${LLAMAFACTORY_CLI:-llamafactory-cli}"' in text
    assert '${LLAMAFACTORY_CLI} train ${RUNTIME_CONFIG}' in text
    assert '"${LLAMAFACTORY_CLI}" train "${RUNTIME_CONFIG}"' in text


def test_sft_launcher_gates_mcore_adapter_when_mca_enabled() -> None:
    text = SCRIPT.read_text(encoding="utf-8")

    assert 'if [[ "${USE_MCA}" == "1" ]]; then' in text
    assert 'importlib.util.find_spec("mcore_adapter")' in text
    assert "mcore_adapter import failed while USE_MCA=1" in text
    assert "Remote GPU/LTP nodes must not git clone/fetch or download dependencies" in text
    assert 'PYTHONPATH_PREFIX="${MCORE_ADAPTER_DIR}:${PYTHONPATH_PREFIX}"' in text
