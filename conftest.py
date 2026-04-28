import base64
import html as html_lib
import re
import time
from datetime import datetime
from pathlib import Path

import pytest
from playwright.sync_api import Page

from pages.login_page import LoginPage

_test_results = []


# ---------------------------------------------------------------------------
# Hook para capturar el resultado del test en el fixture de teardown
# ---------------------------------------------------------------------------
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)


# ---------------------------------------------------------------------------
# Fixture: page (scope=function) — crea contexto propio y captura resultado
# ---------------------------------------------------------------------------
@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args):
    return {**browser_type_launch_args, "args": ["--disable-dev-shm-usage"]}


@pytest.fixture(scope="function")
def page(request, browser):
    context = browser.new_context()
    pg = context.new_page()
    pg.set_default_timeout(90_000)
    pg.set_default_navigation_timeout(90_000)
    start_time = time.time()

    yield pg

    duration = round(time.time() - start_time, 2)

    rep = getattr(request.node, "rep_call", None)
    if rep is None or rep.failed:
        result = "Fallido"
        error_log = str(rep.longrepr) if (rep and rep.longrepr) else "Error desconocido"
    else:
        result = "Pasado"
        error_log = ""

    try:
        screenshot_bytes = pg.screenshot(full_page=True)
        screenshot_b64 = base64.b64encode(screenshot_bytes).decode()
    except Exception:
        screenshot_b64 = ""

    url = pg.url
    docstring = request.node.function.__doc__ or ""
    po_info = _parse_po_info(docstring)

    _test_results.append({
        "name": request.node.name,
        "nodeid": request.node.nodeid,
        "result": result,
        "duration": duration,
        "error_log": error_log,
        "screenshot_b64": screenshot_b64,
        "url": url,
        "po_info": po_info,
    })

    pg.close()
    context.close()


# ---------------------------------------------------------------------------
# Fixture: login_page — igual al original, depende de page
# ---------------------------------------------------------------------------
@pytest.fixture
def login_page(page: Page) -> LoginPage:
    return LoginPage(page)


# ---------------------------------------------------------------------------
# Hook de sesión — genera el reporte al finalizar todos los tests
# ---------------------------------------------------------------------------
def pytest_sessionfinish(session, exitstatus):
    _generate_po_report()


# ---------------------------------------------------------------------------
# Parseo del docstring del test
# ---------------------------------------------------------------------------
def _parse_po_info(docstring: str) -> dict:
    keys = ["escenario", "esperado", "impacto", "accion"]
    result = {k: "" for k in keys}
    if not docstring:
        return result
    for i, key in enumerate(keys):
        next_keys = keys[i + 1:]
        if next_keys:
            stop = "|".join(next_keys)
            pattern = rf"{key}\s*:\s*(.*?)(?=\n\s*(?:{stop})\s*:|$)"
        else:
            pattern = rf"{key}\s*:\s*(.*?)(?:\s*)$"
        match = re.search(pattern, docstring, re.IGNORECASE | re.DOTALL)
        if match:
            result[key] = match.group(1).strip()
    return result


# ---------------------------------------------------------------------------
# Generación del reporte HTML
# ---------------------------------------------------------------------------
def _generate_po_report():
    output_path = Path("reports/reporte_login.html")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    total = len(_test_results)
    failed = sum(1 for r in _test_results if r["result"] == "Fallido")
    passed = total - failed

    css = """\
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: Helvetica, Arial, sans-serif; font-size: 14px; background: #f4f6f9; color: #333; padding: 30px; }
h1 { font-size: 26px; color: #222; margin-bottom: 4px; }
.subtitle { color: #888; font-size: 13px; margin-bottom: 30px; }
.summary-bar { display: flex; gap: 16px; margin-bottom: 30px; }
.summary-card { flex: 1; background: white; border-radius: 8px; padding: 18px 24px; border-left: 5px solid #ccc; box-shadow: 0 1px 4px rgba(0,0,0,0.08); }
.summary-card.total { border-color: #555; }
.summary-card.failed { border-color: #e53935; }
.summary-card.passed { border-color: #43a047; }
.summary-card .number { font-size: 36px; font-weight: bold; }
.summary-card.failed .number { color: #e53935; }
.summary-card.passed .number { color: #43a047; }
.summary-card .label { font-size: 13px; color: #888; margin-top: 2px; }
.test-card { background: white; border-radius: 8px; box-shadow: 0 1px 4px rgba(0,0,0,0.08); margin-bottom: 24px; overflow: hidden; }
.test-header { display: flex; align-items: center; justify-content: space-between; padding: 16px 20px; border-bottom: 1px solid #eee; }
.test-header .test-name { font-weight: bold; font-size: 15px; }
.test-header .test-file { font-size: 12px; color: #999; margin-top: 3px; }
.badge { display: inline-block; padding: 4px 12px; border-radius: 20px; font-size: 12px; font-weight: bold; color: white; }
.badge.failed { background: #e53935; }
.badge.passed { background: #43a047; }
.test-body { display: grid; grid-template-columns: 1fr 1fr; gap: 0; }
.technical { padding: 20px; border-right: 1px solid #eee; }
.technical h3 { font-size: 12px; text-transform: uppercase; letter-spacing: 0.05em; color: #888; margin-bottom: 12px; }
.meta-row { display: flex; gap: 8px; margin-bottom: 10px; font-size: 13px; }
.meta-label { color: #999; min-width: 80px; }
.log-box { background: #1e1e1e; color: #d4d4d4; border-radius: 6px; padding: 14px; font-family: "Courier New", Courier, monospace; font-size: 11.5px; line-height: 1.6; white-space: pre-wrap; overflow-x: auto; margin-top: 12px; }
.error-line { color: #f48771; }
.pointer-line { color: #569cd6; font-weight: bold; }
.screenshot-section { margin-top: 16px; }
.screenshot-label { font-size: 11px; text-transform: uppercase; letter-spacing: 0.05em; color: #888; margin-bottom: 8px; }
.po-view { padding: 20px; background: #fafbfc; }
.po-view h3 { font-size: 12px; text-transform: uppercase; letter-spacing: 0.05em; color: #888; margin-bottom: 12px; }
.po-section { margin-bottom: 16px; }
.po-label { font-size: 11px; font-weight: bold; text-transform: uppercase; letter-spacing: 0.06em; color: #aaa; margin-bottom: 4px; }
.po-section p { font-size: 13.5px; line-height: 1.6; color: #333; }
.alert-box { background: #fff3e0; border-left: 4px solid #fb8c00; border-radius: 4px; padding: 12px 14px; font-size: 13px; line-height: 1.6; margin-top: 14px; color: #444; }
.alert-box strong { color: #e65100; }
.info-box { background: #e8f5e9; border-left: 4px solid #43a047; border-radius: 4px; padding: 12px 14px; font-size: 13px; line-height: 1.6; color: #444; }
.duration-badge { font-size: 12px; color: #888; background: #f0f0f0; padding: 2px 8px; border-radius: 10px; }
footer { text-align: center; color: #bbb; font-size: 12px; margin-top: 40px; }"""

    cards_html = ""
    for r in _test_results:
        result_class = "failed" if r["result"] == "Fallido" else "passed"
        badge_text = r["result"]
        po = r["po_info"]

        # Log de error formateado
        error_html = ""
        if r["error_log"]:
            lines = r["error_log"].splitlines()
            formatted_lines = []
            for line in lines:
                escaped = html_lib.escape(line)
                if any(kw in line for kw in ("AssertionError", "Error", "FAILED", "Exception")):
                    formatted_lines.append(f'<span class="error-line">{escaped}</span>')
                elif line.strip().startswith(">") or line.startswith("E "):
                    formatted_lines.append(f'<span class="pointer-line">{escaped}</span>')
                else:
                    formatted_lines.append(escaped)
            error_html = (
                '<div class="log-box">'
                + "\n".join(formatted_lines)
                + "</div>"
            )

        # Captura de pantalla
        screenshot_html = ""
        if r["screenshot_b64"]:
            screenshot_html = (
                '<div class="screenshot-section">'
                '<div class="screenshot-label">Captura de pantalla</div>'
                f'<img src="data:image/png;base64,{r["screenshot_b64"]}" '
                'style="width:100%;border-radius:4px;border:1px solid #eee;" />'
                "</div>"
            )

        # Caja de impacto: naranja si falló, verde si pasó
        if r["result"] == "Fallido":
            impact_html = (
                '<div class="alert-box" style="margin-top:14px;">'
                f'<strong>&#9888; Impacto en el negocio:</strong> {html_lib.escape(po.get("impacto", ""))}'
                "</div>"
            )
        else:
            impact_html = (
                '<div class="info-box" style="margin-top:14px;">'
                f'<strong>Impacto en el negocio:</strong> {html_lib.escape(po.get("impacto", ""))}'
                "</div>"
            )

        accion_html = (
            '<div class="info-box" style="margin-top:10px;">'
            f'<strong>Acci&#243;n recomendada:</strong> {html_lib.escape(po.get("accion", ""))}'
            "</div>"
        )

        cards_html += f"""
        <div class="test-card">
            <div class="test-header">
                <div>
                    <div class="test-name">{html_lib.escape(r['name'])}</div>
                    <div class="test-file">{html_lib.escape(r['nodeid'])}</div>
                </div>
                <div style="display:flex;align-items:center;gap:8px;">
                    <span class="duration-badge">{r['duration']}s</span>
                    <span class="badge {result_class}">{badge_text}</span>
                </div>
            </div>
            <div class="test-body">
                <div class="technical">
                    <h3>Detalle t&#233;cnico</h3>
                    <div class="meta-row">
                        <span class="meta-label">Archivo</span>
                        <span>{html_lib.escape(r['nodeid'])}</span>
                    </div>
                    <div class="meta-row">
                        <span class="meta-label">URL</span>
                        <span>{html_lib.escape(r['url'])}</span>
                    </div>
                    <div class="meta-row">
                        <span class="meta-label">Duraci&#243;n</span>
                        <span>{r['duration']}s</span>
                    </div>
                    {error_html}
                    {screenshot_html}
                </div>
                <div class="po-view">
                    <h3>Explicaci&#243;n para el negocio</h3>
                    <div class="po-section">
                        <div class="po-label">&#191;Qu&#233; se estaba probando?</div>
                        <p>{html_lib.escape(po.get('escenario', ''))}</p>
                    </div>
                    <div class="po-section">
                        <div class="po-label">&#191;Qu&#233; se esperaba?</div>
                        <p>{html_lib.escape(po.get('esperado', ''))}</p>
                    </div>
                    {impact_html}
                    {accion_html}
                </div>
            </div>
        </div>"""

    html_content = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Reporte de Pruebas &mdash; Login</title>
    <style>
{css}
    </style>
</head>
<body>
    <h1>Reporte de Pruebas Automatizadas</h1>
    <div class="subtitle">Login &mdash; practicesoftwaretesting.com &nbsp;&middot;&nbsp; {now}</div>

    <div class="summary-bar">
        <div class="summary-card total">
            <div class="number">{total}</div>
            <div class="label">Total de pruebas</div>
        </div>
        <div class="summary-card failed">
            <div class="number">{failed}</div>
            <div class="label">Fallidas</div>
        </div>
        <div class="summary-card passed">
            <div class="number">{passed}</div>
            <div class="label">Pasadas</div>
        </div>
    </div>

    {cards_html}

    <footer>
        Generado autom&#225;ticamente por el framework de pruebas PST &nbsp;&middot;&nbsp; {now}
    </footer>
</body>
</html>"""

    output_path.write_text(html_content, encoding="utf-8")
    print(f"\n[reporte_po] HTML generado en: {output_path.resolve()}")
