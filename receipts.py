import sqlite3
from typing import Callable, Optional


class ReceiptStore:
    """Records exactly one terminal receipt ('done' or 'timeout') per execution."""

    def __init__(self) -> None:
        self.conn = sqlite3.connect(":memory:", check_same_thread=False)
        self.conn.execute(
            "CREATE TABLE receipts (execution_id TEXT PRIMARY KEY, status TEXT NOT NULL)"
        )
        # Test seam: runs right before the write attempt.
        self.before_write: Optional[Callable[[], None]] = None

    def terminal_status(self, execution_id: str) -> Optional[str]:
        row = self.conn.execute(
            "SELECT status FROM receipts WHERE execution_id = ?", (execution_id,)
        ).fetchone()
        return row[0] if row else None

    def finish(self, execution_id: str, status: str) -> bool:
        """Called by the stage ('done') and the watchdog ('timeout').

        The check and the write are ONE atomic statement: the PRIMARY KEY
        lets exactly one caller insert; the other gets rowcount 0.
        """
        if self.before_write:
            self.before_write()
        cur = self.conn.execute(
            "INSERT OR IGNORE INTO receipts (execution_id, status) VALUES (?, ?)",
            (execution_id, status),
        )
        self.conn.commit()
        return cur.rowcount == 1

    def receipts(self, execution_id: str) -> list:
        return self.conn.execute(
            "SELECT execution_id, status FROM receipts WHERE execution_id = ?",
            (execution_id,),
        ).fetchall()