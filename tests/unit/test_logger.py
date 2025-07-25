from engine.utils.logger import log


def test_logger_emits() -> None:
    try:
        log.info("unit‑test‑ping", subsystem="logger")
    except Exception as exc:
        assert False, f"Logger raised {exc}"
