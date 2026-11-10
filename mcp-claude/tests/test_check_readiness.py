"""Read-only readiness contract tests; run with unittest discovery."""
import contextlib
import importlib.util
import io
import json
import tempfile
from pathlib import Path
import subprocess
import unittest
from unittest.mock import patch


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "check_readiness.py"
SPEC = importlib.util.spec_from_file_location("check_readiness", SCRIPT)
assert SPEC is not None and SPEC.loader is not None
probe = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(probe)
BASE = "https://example.test"


def tool(name="get_data_quality"):
    """Build one valid public read-only tool fixture."""
    return {"name": name, "title": "Data quality", "inputSchema": {"type": "object"},
            "annotations": {"readOnlyHint": True, "destructiveHint": False, "openWorldHint": False}}


def response(value, status=200, challenge=None):
    """Build the narrow transport response used by the probe."""
    return {"status": status, "body": json.dumps(value), "www_authenticate": challenge}


def rpc(tools, cursor=None):
    """Build a JSON-RPC catalog page."""
    result = {"tools": tools}
    if cursor is not None:
        result["nextCursor"] = cursor
    return response({"jsonrpc": "2.0", "id": 1, "result": result})


def metadata():
    """Build valid OAuth discovery documents."""
    return ({"issuer": BASE, "authorization_endpoint": BASE + "/authorize",
             "token_endpoint": BASE + "/token", "registration_endpoint": BASE + "/register",
             "token_endpoint_auth_methods_supported": ["none"],
             "grant_types_supported": ["authorization_code", "refresh_token"],
             "response_types_supported": ["code"], "code_challenge_methods_supported": ["S256"]},
            {"resource": BASE + "/mcp", "authorization_servers": [BASE]})


class ReadinessTests(unittest.TestCase):
    """Exercise real pure helpers and injected transport boundaries."""

    def setUp(self):
        """Fail explicitly until the implementation exists (TDD red)."""
        self.assertIsNotNone(probe, "readiness implementation does not exist yet")

    def test_base_url_rejects_credentials_queries_fragments_and_remote_http(self):
        """Prevent credentials and insecure remote transports."""
        for url in ["http://example.test", "https://u:p@example.test", "https://example.test?q=x",
                    "https://example.test/#x", "https://example.test/mcp", "https://example.test:bad",
                    "https://example.test\n", "file:///etc/passwd"]:
            with self.subTest(url=url), self.assertRaises(ValueError):
                probe.validate_base_url(url)
        self.assertEqual(probe.validate_base_url(BASE + "/"), BASE)

    def test_local_http_requires_explicit_opt_in(self):
        """Allow only loopback HTTP with an explicit switch."""
        for host in ["localhost", "127.0.0.1", "[::1]"]:
            url = "http://" + host + ":8080"
            with self.assertRaises(ValueError):
                probe.validate_base_url(url)
            self.assertEqual(probe.validate_base_url(url, True), url)
        with self.assertRaises(ValueError):
            probe.validate_base_url("http://example.test", True)

    def test_json_and_multiline_sse(self):
        """Accept JSON and one RPC response amidst SSE keepalives."""
        value = {"jsonrpc": "2.0", "id": 1, "result": {"tools": []}}
        self.assertEqual(probe.parse_payload(json.dumps(value)), value)
        stream = ': ping\r\n\r\nevent: message\r\ndata: {"jsonrpc":"2.0",\r\ndata: "id":1,"result":{"tools":[]}}\r\n\r\n'
        self.assertEqual(probe.parse_payload(stream), value)
        for bad in ["not json", "[]", "data: nope\n\n", "data: {}\n\ndata: {}\n\n"]:
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                probe.parse_payload(bad)

    def test_pagination_aggregates_and_forwards_cursor(self):
        """Aggregate every page without following arbitrary URLs."""
        calls = []
        pages = iter([rpc([tool("one")], "opaque"), rpc([tool("two")])])
        def request(url, payload=None):
            """Record only the requested RPC envelope."""
            calls.append((url, payload))
            return next(pages)
        tools = probe.collect_tools(request, BASE + "/mcp")
        self.assertEqual([item["name"] for item in tools], ["one", "two"])
        self.assertEqual(calls[1][1]["params"], {"cursor": "opaque"})
        self.assertTrue(all(call[1]["method"] == "tools/list" for call in calls))

    def test_catalog_rejects_duplicate_failed_malformed_and_looping_pages(self):
        """Never report partial or ambiguous catalogs as complete."""
        cases = [[rpc([tool(), tool()])], [response({}, 503)],
                 [response({"jsonrpc": "2.0", "id": 1, "error": {"code": -1}})],
                 [response({"result": {"tools": "wrong"}})],
                 [rpc([tool("one")], "x"), rpc([tool("two")], "x")],
                 [rpc([tool()], 5)], [rpc([None])]]
        for pages in cases:
            iterator = iter(pages)
            with self.subTest(pages=pages), self.assertRaises(ValueError):
                probe.collect_tools(lambda *args: next(iterator), BASE + "/mcp")

    def test_catalog_page_limit_is_twenty(self):
        """Bound endless pagination even when cursors are distinct."""
        calls = []
        def request(*args):
            """Return a fresh tool and cursor forever."""
            calls.append(1)
            return rpc([tool(str(len(calls)))], str(len(calls)))
        with self.assertRaises(ValueError):
            probe.collect_tools(request, BASE + "/mcp")
        self.assertEqual(len(calls), 20)

    def test_catalog_validation(self):
        """Require nonempty titles, bounded names, schemas and read-only hints."""
        self.assertTrue(all(c["passed"] for c in probe.catalog_checks([tool()])))
        for items in [[], [dict(tool(), title=" ")], [dict(tool(), name="a" * 65)],
                      [dict(tool(), inputSchema={})], [dict(tool(), annotations={})],
                      [dict(tool(), annotations={"readOnlyHint": True, "destructiveHint": True,
                                                  "openWorldHint": False})]]:
            with self.subTest(items=items):
                self.assertTrue(any(not c["passed"] for c in probe.catalog_checks(items)))

    def test_oauth_validation_and_sanitization(self):
        """Validate DCR/PKCE/public refresh and omit unknown secret metadata."""
        auth, resource = metadata()
        self.assertTrue(all(c["passed"] for c in probe.oauth_checks(auth, resource, BASE)))
        for key, value in [("issuer", "http://example.test"), ("registration_endpoint", None),
                           ("token_endpoint_auth_methods_supported", ["client_secret_basic"]),
                           ("grant_types_supported", ["authorization_code"]),
                           ("code_challenge_methods_supported", ["plain"])]:
            with self.subTest(key=key):
                self.assertTrue(any(not c["passed"] for c in probe.oauth_checks(dict(auth, **{key: value}), resource, BASE)))
        self.assertTrue(any(not c["passed"] for c in probe.oauth_checks(auth, dict(resource, resource=BASE), BASE)))
        self.assertTrue(any(not c["passed"] for c in probe.oauth_checks(auth, dict(resource, authorization_servers=["https://other.test"]), BASE)))
        sanitized = probe.sanitize_metadata(dict(auth, access_token="SECRET", token_endpoint=BASE + "/token?secret=SECRET"))
        self.assertNotIn("SECRET", json.dumps(sanitized))

    def test_full_probe_is_read_only_and_omits_raw_failures(self):
        """Use only discovery, list and the specifically allowed read-only call."""
        auth, resource = metadata()
        calls = []
        def request(url, payload=None):
            """Serve discovery without credentials or mutation."""
            calls.append((url, payload))
            if url.endswith("healthz"):
                return response({"status": "ok", "secret": "SECRET"})
            if url.endswith("oauth-authorization-server"):
                return response(dict(auth, secret="SECRET"))
            if url.endswith("oauth-protected-resource"):
                return response(resource)
            if payload["method"] == "tools/list":
                return rpc([tool()])
            return response({"secret": "SECRET"}, 401, 'Bearer resource_metadata="' + BASE + '/.well-known/oauth-protected-resource"')
        report = probe.run_probe(BASE, request)
        self.assertTrue(report["passed"])
        self.assertEqual(report["tool_count"], 1)
        self.assertIn("timestamp", report)
        self.assertNotIn("SECRET", json.dumps(report))
        self.assertEqual(calls[-1][1]["params"], {"name": "get_data_quality", "arguments": {}})
        self.assertEqual(len(calls), 5)

    def test_network_errors_and_bad_auth_are_reported_without_leaks(self):
        """Continue after transport failures without copying exception secrets."""
        def broken(*args):
            """Simulate a secret-bearing transport error."""
            raise OSError("SECRET")
        report = probe.run_probe(BASE, broken)
        self.assertFalse(report["passed"])
        self.assertNotIn("SECRET", json.dumps(report))
        self.assertGreaterEqual(len(report["checks"]), 4)

    def test_curl_transport_and_failures(self):
        """Curl ignores local curlrc, never sends auth, and handles process errors."""
        with patch.object(probe.subprocess, "run", return_value=subprocess.CompletedProcess([], 0, '{"status":"ok"}\n200', "")) as run:
            result = probe.curl_request(BASE + "/healthz")
            self.assertEqual(result["status"], 200)
            command = run.call_args.args[0]
            self.assertEqual(command[:2], ["curl", "--disable"])
            self.assertNotIn("--location", command)
            self.assertNotIn("--user", command)
        for failure in [OSError("SECRET"), subprocess.TimeoutExpired("curl", 1)]:
            with patch.object(probe.subprocess, "run", side_effect=failure), self.assertRaises(ValueError) as caught:
                probe.curl_request(BASE)
            self.assertNotIn("SECRET", str(caught.exception))

    def test_protected_call_requires_401_and_bearer_challenge(self):
        """Reject public execution, missing challenges and non-Bearer authentication."""
        auth, resource = metadata()
        for status, challenge in [(200, "Bearer"), (401, None), (401, "Basic realm=example")]:
            def request(url, payload=None):
                """Serve valid discovery but an invalid authentication gate."""
                if url.endswith("healthz"):
                    return response({"status": "ok"})
                if url.endswith("oauth-authorization-server"):
                    return response(auth)
                if url.endswith("oauth-protected-resource"):
                    return response(resource)
                assert payload is not None
                return rpc([tool()]) if payload["method"] == "tools/list" else response({}, status, challenge)
            with self.subTest(status=status, challenge=challenge):
                self.assertFalse(probe.run_probe(BASE, request)["passed"])

    def test_curl_keeps_only_challenge_and_rejects_bad_status(self):
        """Read only the allowed header, not cookies or arbitrary response headers."""
        def completed(command, **kwargs):
            """Simulate curl's header file and body trailer."""
            header_path = Path(command[command.index("--dump-header") + 1])
            header_path.write_text("HTTP/2 401\nSet-Cookie: SECRET\nWWW-Authenticate: Bearer\nX-Secret: SECRET\n")
            return subprocess.CompletedProcess(command, 0, '{}\n401', "")
        with patch.object(probe.subprocess, "run", side_effect=completed):
            result = probe.curl_request(BASE, {"method": "tools/list"})
        self.assertEqual(result, {"status": 401, "body": "{}", "www_authenticate": "Bearer"})
        for status, text in [(0, "malformed"), (7, "SECRET"), (0, "{}\n999")]:
            with patch.object(probe.subprocess, "run", return_value=subprocess.CompletedProcess([], status, text, "SECRET")):
                with self.assertRaises(ValueError) as caught:
                    probe.curl_request(BASE)
                self.assertNotIn("SECRET", str(caught.exception))

    def test_cli_output_and_failure_exit_codes(self):
        """Persist machine-readable evidence and propagate readiness failures."""
        with tempfile.TemporaryDirectory(prefix="readiness-tests-") as directory:
            path = Path(directory) / "nested" / "report.json"
            for passed, exit_code in [(True, 0), (False, 1)]:
                expected = {"passed": passed}
                with patch.object(probe, "run_probe", return_value=expected), contextlib.redirect_stdout(io.StringIO()):
                    self.assertEqual(probe.main(["--output", str(path)]), exit_code)
                self.assertEqual(json.loads(path.read_text()), expected)
            with patch.object(probe, "run_probe", return_value={"passed": True}), contextlib.redirect_stderr(io.StringIO()):
                self.assertEqual(probe.main(["--output", directory]), 2)

    def test_cli_rejects_insecure_url(self):
        """Reject insecure configuration before any network request."""
        completed = subprocess.run(["python3", str(SCRIPT), "--base-url", "http://example.test"], capture_output=True, text=True)
        self.assertNotEqual(completed.returncode, 0)
        self.assertIn("HTTPS", completed.stderr)


if __name__ == "__main__":
    unittest.main()
