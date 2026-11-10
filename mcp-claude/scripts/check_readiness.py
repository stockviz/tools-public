#!/usr/bin/env python3
"""Probe public Claude connector readiness without credentials or external writes.

Only GET discovery/health and POST tools/list plus the read-only
get_data_quality authentication challenge are sent. OAuth registration/login
and authorized tool execution are deliberately NOT tested. Requires curl.
"""
import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile
from urllib.parse import urlsplit, urlunsplit


DEFAULT_BASE = "https://mutual-fund-mcp.stockviz.workers.dev"
MAX_PAGES = 20
URL_FIELDS = {"issuer", "resource", "authorization_endpoint", "token_endpoint", "registration_endpoint"}
LIST_FIELDS = {"authorization_servers", "token_endpoint_auth_methods_supported", "grant_types_supported",
               "response_types_supported", "code_challenge_methods_supported", "scopes_supported"}


def validate_base_url(value, allow_localhost_http=False):
    """Require a credential-free HTTPS origin, with opt-in loopback HTTP."""
    try:
        parts = urlsplit(value)
        port = parts.port
        local = parts.hostname in {"localhost", "127.0.0.1", "::1"}
        valid_scheme = parts.scheme == "https" or (allow_localhost_http and local and parts.scheme == "http")
        if (not valid_scheme or not parts.hostname or parts.username is not None or parts.password is not None
                or parts.query or parts.fragment or parts.path not in {"", "/"}
                or any(char.isspace() for char in value) or "\\" in value
                or (port is not None and port < 1) or "?" in value or "#" in value):
            raise ValueError
    except (ValueError, TypeError):
        raise ValueError("base URL must be an HTTPS origin without credentials, path, query or fragment; "
                         "loopback HTTP requires --allow-localhost-http") from None
    return urlunsplit((parts.scheme, parts.netloc, "", "", ""))


def safe_url(value):
    """Return sanitized public endpoint URLs, never userinfo/query/fragment."""
    if not isinstance(value, str):
        return None
    try:
        parts = urlsplit(value)
        if (parts.scheme not in {"https", "http"} or not parts.hostname or parts.username is not None
                or parts.password is not None or parts.query or parts.fragment
                or any(char.isspace() for char in value) or "\\" in value):
            return None
        _ = parts.port
        return urlunsplit((parts.scheme, parts.netloc, parts.path, "", ""))
    except ValueError:
        return None


def sanitize_metadata(document):
    """Allowlist OAuth metadata rather than preserving arbitrary response fields."""
    result = {}
    for key in URL_FIELDS:
        if key in document:
            result[key] = safe_url(document[key])
    for key in LIST_FIELDS:
        values = document.get(key)
        if isinstance(values, list):
            result[key] = ([safe_url(value) for value in values] if key == "authorization_servers"
                           else [value for value in values if isinstance(value, str)])
    return result


def parse_payload(body):
    """Decode a JSON object or exactly one SSE data event, including multiline data."""
    try:
        value = json.loads(body)
    except (ValueError, TypeError):
        events = []
        data = []
        for line in body.replace("\r\n", "\n").split("\n") + [""]:
            if not line:
                if data:
                    events.append("\n".join(data))
                    data = []
            elif line.startswith("data:"):
                data.append(line[5:].removeprefix(" "))
        if len(events) != 1:
            raise ValueError("expected one JSON or SSE response") from None
        try:
            value = json.loads(events[0])
        except ValueError:
            raise ValueError("invalid SSE JSON") from None
    if not isinstance(value, dict):
        raise ValueError("expected a JSON object")
    return value


def curl_request(url, payload=None):
    """Use bounded credential-free curl, retaining only WWW-Authenticate headers."""
    with tempfile.TemporaryDirectory(prefix="claude-readiness-") as directory:
        headers_path = Path(directory) / "headers"
        command = ["curl", "--disable", "--silent", "--show-error", "--globoff",
                   "--proto", "=https,http", "--connect-timeout", "10", "--max-time", "30",
                   "--max-filesize", "4194304", "--max-redirs", "0", "--noproxy", "*",
                   "--dump-header", str(headers_path), "--write-out", "\n%{http_code}",
                   "--header", "Accept: application/json, text/event-stream"]
        if payload is not None:
            command += ["--header", "Content-Type: application/json", "--data-binary", json.dumps(payload)]
        command += ["--url", url]
        try:
            completed = subprocess.run(command, capture_output=True, text=True, timeout=35, check=False)
        except (OSError, subprocess.TimeoutExpired):
            raise ValueError("curl unavailable or timed out") from None
        if completed.returncode != 0:
            raise ValueError("curl transport failed (exit %s)" % completed.returncode)
        try:
            body, status = completed.stdout.rsplit("\n", 1)
            status = int(status)
            if not 100 <= status <= 599:
                raise ValueError
            headers = headers_path.read_text(encoding="utf-8", errors="replace") if headers_path.exists() else ""
        except (ValueError, OSError):
            raise ValueError("invalid curl response") from None
        challenges = [line.split(":", 1)[1].strip() for line in headers.splitlines()
                      if line.lower().startswith("www-authenticate:")]
        return {"status": status, "body": body, "www_authenticate": ", ".join(challenges) or None}


def collect_tools(request, endpoint):
    """Collect at most twenty pages and reject failed, duplicate or looping catalogs."""
    tools, names, cursors = [], set(), set()
    params = {}
    for _ in range(MAX_PAGES):
        response = request(endpoint, {"jsonrpc": "2.0", "id": 1, "method": "tools/list", "params": params})
        if response["status"] != 200:
            raise ValueError("tools/list HTTP failure")
        message = parse_payload(response["body"])
        result = message.get("result")
        if (message.get("jsonrpc") != "2.0" or message.get("id") != 1 or "error" in message
                or not isinstance(result, dict) or not isinstance(result.get("tools"), list)):
            raise ValueError("invalid tools/list JSON-RPC response")
        for tool in result["tools"]:
            if not isinstance(tool, dict) or not isinstance(tool.get("name"), str) or not tool["name"].strip():
                raise ValueError("invalid tool name")
            if tool["name"] in names:
                raise ValueError("duplicate tool name")
            names.add(tool["name"])
            tools.append(tool)
        cursor = result.get("nextCursor")
        if cursor is None:
            return tools
        if not isinstance(cursor, str) or not cursor or cursor in cursors:
            raise ValueError("invalid or repeated catalog cursor")
        cursors.add(cursor)
        params = {"cursor": cursor}
    raise ValueError("catalog exceeds twenty-page limit")


def check(name, passed, detail=None):
    """Build one stable JSON check record without raw response contents."""
    result = {"name": name, "passed": bool(passed)}
    if detail is not None:
        result["detail"] = detail
    return result


def catalog_checks(tools):
    """Check titles/names/schemas and applicable read-only annotation semantics."""
    checks = [check("catalog.nonempty", bool(tools))]
    for tool in tools:
        name = tool["name"]
        title = tool.get("title")
        annotations = tool.get("annotations", {})
        schema = tool.get("inputSchema", {})
        checks.extend([
            check("tool.title", isinstance(title, str) and bool(title.strip()), {"tool": name}),
            check("tool.name", bool(re.fullmatch(r"[A-Za-z0-9_.-]{1,64}", name)), {"tool": name}),
            check("tool.input_schema", isinstance(schema, dict) and schema.get("type") == "object", {"tool": name}),
            check("tool.annotations", isinstance(annotations, dict)
                  and annotations.get("readOnlyHint") is True
                  and annotations.get("destructiveHint") is False
                  and isinstance(annotations.get("openWorldHint"), bool)
                  and ("idempotentHint" not in annotations or isinstance(annotations["idempotentHint"], bool)),
                  {"tool": name}),
        ])
    return checks


def oauth_checks(auth, resource, base):
    """Validate HTTPS issuer/endpoints, public DCR, PKCE, refresh and resource binding."""
    issuer = auth.get("issuer")
    checks = []
    for field in ("issuer", "authorization_endpoint", "token_endpoint", "registration_endpoint"):
        value = safe_url(auth.get(field))
        checks.append(check("oauth." + field + ".https", bool(value and value.startswith("https://"))))
    checks += [check("oauth.issuer_binding", issuer == base),
               check("oauth.resource_binding", resource.get("resource") == base + "/mcp"),
               check("oauth.authorization_server_binding", isinstance(resource.get("authorization_servers"), list)
                     and issuer in resource["authorization_servers"]
                     and all(isinstance(url, str) and safe_url(url) == url and url.startswith("https://")
                             for url in resource["authorization_servers"]))]
    for field, required in [("token_endpoint_auth_methods_supported", {"none"}),
                            ("grant_types_supported", {"authorization_code", "refresh_token"}),
                            ("response_types_supported", {"code"}),
                            ("code_challenge_methods_supported", {"S256"})]:
        values = auth.get(field)
        checks.append(check("oauth." + field, isinstance(values, list)
                            and all(isinstance(value, str) for value in values)
                            and required.issubset(values)))
    return checks


def run_probe(base, request=curl_request):
    """Run independent checks, preserve public schemas, and return failure evidence."""
    report = {"timestamp": datetime.now(timezone.utc).isoformat(), "base_url": base,
              "read_only": True, "checks": [], "endpoints": {}, "tools": [], "tool_count": 0}
    checks = report["checks"]
    documents = {}
    for label, path in [("health", "/healthz"), ("authorization_server", "/.well-known/oauth-authorization-server"),
                        ("protected_resource", "/.well-known/oauth-protected-resource")]:
        url = base + path
        record = {"url": url}
        report["endpoints"][label] = record
        try:
            response = request(url)
            record["status"] = response["status"]
            if response["status"] != 200:
                raise ValueError("unexpected HTTP status")
            document = parse_payload(response["body"])
            if label == "health":
                checks.append(check("health.status", document.get("status") == "ok"))
            else:
                documents[label] = document
                record["metadata"] = sanitize_metadata(document)
            checks.append(check(label + ".response", True))
        except (ValueError, OSError, KeyError, TypeError):
            checks.append(check(label + ".response", False, "request or response validation failed"))
    checks.extend(oauth_checks(documents.get("authorization_server", {}), documents.get("protected_resource", {}), base))
    report["endpoints"]["tools_list"] = {"url": base + "/mcp"}
    try:
        tools = collect_tools(request, base + "/mcp")
        # Tool definitions are public catalog data; omit unrelated response/envelope fields.
        report["tools"] = [{key: tool[key] for key in ("name", "title", "description", "inputSchema", "outputSchema", "annotations")
                            if key in tool} for tool in tools]
        report["tool_count"] = len(tools)
        checks.append(check("catalog.complete", True))
        checks.extend(catalog_checks(tools))
    except (ValueError, OSError, KeyError, TypeError):
        checks.append(check("catalog.complete", False, "catalog request, pagination or response validation failed"))
    record = {"url": base + "/mcp", "tool": "get_data_quality"}
    report["endpoints"]["protected_call"] = record
    try:
        response = request(base + "/mcp", {"jsonrpc": "2.0", "id": 2, "method": "tools/call",
                                           "params": {"name": "get_data_quality", "arguments": {}}})
        record["status"] = response["status"]
        challenge = response.get("www_authenticate")
        # Only this explicitly permitted response header is retained; never bodies or other headers.
        record["www_authenticate"] = challenge
        checks.append(check("protected_call.http_401", response["status"] == 401))
        checks.append(check("protected_call.www_authenticate", isinstance(challenge, str)
                            and bool(re.match(r"(?i)^Bearer(?:\s|$)", challenge))))
    except (ValueError, OSError, KeyError, TypeError):
        checks.append(check("protected_call.response", False, "request or response validation failed"))
    report["passed"] = all(item["passed"] for item in checks)
    report["failed_check_count"] = sum(not item["passed"] for item in checks)
    return report


def main(argv=None):
    """Write JSON evidence and exit nonzero on failed readiness or local errors."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-url", default=DEFAULT_BASE)
    parser.add_argument("--allow-localhost-http", action="store_true", help="permit HTTP only for explicit loopback checks")
    parser.add_argument("--output", type=Path, help="write JSON report here (also prints JSON to stdout)")
    args = parser.parse_args(argv)
    try:
        base = validate_base_url(args.base_url, args.allow_localhost_http)
    except ValueError as exc:
        parser.error(str(exc))
    report = run_probe(base)
    text = json.dumps(report, indent=2, ensure_ascii=False) + "\n"
    if args.output:
        try:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(text, encoding="utf-8")
        except OSError:
            print("could not write output report", file=sys.stderr)
            return 2
    print(text, end="")
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    sys.exit(main())
