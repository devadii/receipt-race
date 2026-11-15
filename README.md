# receipt-race

Demonstration repo (built for a job application, not client work): a
check-then-act race where a stage ("done") and a watchdog ("timeout") can
both write a terminal receipt for the same execution.

History:
1. `receipts.py` with the bug (this commit)
2. `test:` failing regression test, CI red
3. `fix:` atomic write via PRIMARY KEY + INSERT OR IGNORE, CI green