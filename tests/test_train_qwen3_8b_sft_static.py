from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "train_qwen3_8b_sft.sh"


def test_sft_launcher_exports_wrapper_environment_contract() -> None:
    text = SCRIPT.read_text(encoding="utf-8")

    assert 'DEP_TARGET="${DEP_TARGET:-${PYTHON_DEPS_DIR:-${RUN_DIR}/python_deps}}"' in text
    assert 'LF="${LF:-${LLAMAFACTORY_DIR}}"' in text
    assert "export DEP_TARGET LF LLAMAFACTORY_CLI" in text
    assert 'export DEP_TARGET="${DEP_TARGET}"' in text
    assert 'export LF="${LF}"' in text


def test_sft_launcher_uses_configurable_llamafactory_cli() -> None:
    text = SCRIPT.read_text(encoding="utf-8")

    assert 'LLAMAFACTORY_CLI="${LLAMAFACTORY_CLI:-llamafactory-cli}"' in text
    assert '${LLAMAFACTORY_CLI} train ${RUNTIME_CONFIG}' in text
    assert '"${LLAMAFACTORY_CLI}" train "${RUNTIME_CONFIG}"' in text
