from receipts import ReceiptStore


def test_stage_and_watchdog_cannot_both_write_a_terminal_receipt():
    """Force the bad interleaving deterministically: no sleep(), no retries.

    The stage has checked "no receipt yet" and is about to write 'done'.
    At exactly that point the watchdog runs to completion and writes 'timeout'.
    """
    store = ReceiptStore()
    watchdog_results = []

    def watchdog_fires_now() -> None:
        store.before_write = None  # fire once
        watchdog_results.append(store.finish("run-1", "timeout"))

    store.before_write = watchdog_fires_now
    stage_result = store.finish("run-1", "done")

    assert watchdog_results == [True]
    assert stage_result is False  # the loser is told it lost
    assert store.receipts("run-1") == [("run-1", "timeout")]  # exactly one