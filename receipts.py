import sqlite3
from typing import Callable, Optional


class ReceiptStore:
    """Records exactly one terminal receipt ('done' or 'timeout') per execution."""

    def __init__(self) -> None:
        self.conn = sqlite3.connect(":memory:", check_same_thread=False)
        self.conn.execute(
            "CREATE TABLE receipts (execution_id TEXT NOT NULL, status TEXT NOT NULL)"
        )
        # Test seam: runs between the "is it terminal?" check and the write.
        self.before_write: Optional[Callable[[], None]] = None

    def terminal_status(self, execution_id: str) -> Optional[str]:
        row = self.conn.execute(
            "SELECT status FROM receipts WHERE execution_id = ?", (execution_id,)
        ).fetchone()
        return row[0] if row else None

    def finish(self, execution_id: str, status: str) -> bool:
        """Called by the stage ('done') and the watchdog ('timeout')."""
        if self.terminal_status(execution_id) is not None:
            return False
        if self.before_write:
            self.before_write()
        self.conn.execute(
            "INSERT INTO receipts (execution_id, status) VALUES (?, ?)",
            (execution_id, status),
        )
        self.conn.commit()
        return True

    def receipts(self, execution_id: str) -> list:
        return self.conn.execute(
            "SELECT execution_id, status FROM receipts WHERE execution_id = ?",
            (execution_id,),
        ).fetchall()