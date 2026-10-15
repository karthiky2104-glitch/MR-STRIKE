import asyncio
import io
import subprocess
import sys
import threading
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

import server


class WorkerTests(unittest.TestCase):
    def test_worker_prints_server_thread_message(self):
        output = io.StringIO()

        with redirect_stdout(output):
            server.worker()

        self.assertEqual(output.getvalue(), "Server thread running...\n")


class MainTests(unittest.IsolatedAsyncioTestCase):
    def test_script_entrypoint_runs_main(self):
        result = subprocess.run(
            [sys.executable, str(Path(server.__file__))],
            capture_output=True,
            check=True,
            text=True,
        )

        self.assertEqual(result.stdout, "Server thread running...\nNone\n")
        self.assertEqual(result.stderr, "")

    async def test_main_runs_worker_in_background_thread(self):
        caller_thread_id = threading.get_ident()
        worker_thread_ids = []
        output = io.StringIO()

        def record_worker_thread():
            worker_thread_ids.append(threading.get_ident())

        with patch.object(server, "worker", side_effect=record_worker_thread) as worker:
            with redirect_stdout(output):
                await server.main()

        worker.assert_called_once_with()
        self.assertEqual(len(worker_thread_ids), 1)
        self.assertNotEqual(worker_thread_ids[0], caller_thread_id)
        self.assertEqual(output.getvalue(), "None\n")

    async def test_main_propagates_worker_exception(self):
        output = io.StringIO()

        def fail_worker():
            raise RuntimeError("worker failed")

        with patch.object(server, "worker", side_effect=fail_worker):
            with redirect_stdout(output):
                with self.assertRaisesRegex(RuntimeError, "worker failed"):
                    await server.main()

        self.assertEqual(output.getvalue(), "")


if __name__ == "__main__":
    unittest.main()
