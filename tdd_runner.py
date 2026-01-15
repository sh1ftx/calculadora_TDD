import sys
import subprocess
import time
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.rule import Rule
from rich.align import Align

console = Console()

# ======================================================
# PALETA SEMÂNTICA FINAL
# ======================================================
COLORS = {
    "red": "red",
    "green": "green",
    "yellow": "yellow",
    "blue": "cyan",     # divisórias gerais
    "text": "white",
    "dim": "dim",
}

BASE_DIR = Path(__file__).parent
CALC_FILE = BASE_DIR / "calculadora" / "calculadora.py"
VERSIONS_DIR = BASE_DIR / "versions"


# ======================================================
# UTILIDADES VISUAIS
# ======================================================
def pause(sec=1):
    time.sleep(sec)


def typewriter(text, delay=0.015):
    for char in text:
        console.print(char, end="", style=COLORS["text"])
        time.sleep(delay)
    console.print()


def title_panel(title, color):
    console.print()
    console.print(
        Panel(
            Align.center(Text(title, style=f"bold {color}")),
            border_style=color,
            padding=(1, 4),
        )
    )
    console.print()


def divider(title=None):
    console.print(
        Rule(title if title else "", style=COLORS["blue"])
    )


def ok(msg):
    console.print(f"✔ {msg}", style=f"bold {COLORS['green']}")


def fail(msg):
    console.print(f"✖ {msg}", style=f"bold {COLORS['red']}")


# ======================================================
# FUNÇÕES TÉCNICAS
# ======================================================
def clean_cache():
    for cache in BASE_DIR.rglob("__pycache__"):
        subprocess.run(["rm", "-rf", str(cache)], stdout=subprocess.DEVNULL)


def apply_version(stage: str):
    version = VERSIONS_DIR / f"calculadora_{stage}.py"
    if not version.exists():
        fail(f"Arquivo não encontrado: {version}")
        sys.exit(1)

    CALC_FILE.write_text(version.read_text())
    console.print(
        f"📄 Versão aplicada: calculadora_{stage}.py",
        style=COLORS["dim"],
    )


def run_pytest(expect_fail=False):
    clean_cache()
    console.print("▶ Executando testes...\n", style=COLORS["text"])

    result = subprocess.run(
        [sys.executable, "-m", "pytest"],
        stdout=sys.stdout,
        stderr=sys.stderr,
    )

    if expect_fail and result.returncode == 0:
        fail("Testes passaram quando deveriam falhar")
        sys.exit(1)

    if not expect_fail and result.returncode != 0:
        fail("Testes falharam inesperadamente")
        sys.exit(1)


# ======================================================
# EXECUÇÃO
# ======================================================
console.clear()

title_panel("🧪 CICLO TDD — TEST DRIVEN DEVELOPMENT", COLORS["blue"])

typewriter(
    "Este programa demonstra o ciclo completo do Test Driven Development.\n"
    "Cada fase é executada, validada e explicada em tempo real."
)

divider("CICLO TDD")

console.print(
    Panel(
        "🔴 RED      → testes falham\n"
        "🟢 GREEN    → código mínimo\n"
        "♻️ REFACTOR → melhoria segura",
        border_style=COLORS["blue"],
    )
)

pause(2)

# ---------------- RED ----------------
divider()
title_panel("🔴 FASE RED — TESTES DEVEM FALHAR", COLORS["red"])

typewriter(
    "Os testes já existem, mas o comportamento ainda não foi implementado.\n"
    "Falhar aqui confirma que os testes são válidos."
)

apply_version("red")
run_pytest(expect_fail=True)
ok("RED confirmado: testes falharam corretamente")

pause(2)

# ---------------- GREEN ----------------
divider()
title_panel("🟢 FASE GREEN — CÓDIGO MÍNIMO", COLORS["green"])

typewriter(
    "Implementamos apenas o necessário para satisfazer os testes.\n"
    "Nenhuma otimização extra é feita neste momento."
)

apply_version("green")
run_pytest()
ok("GREEN confirmado: todos os testes passaram")

pause(2)

# ---------------- REFACTOR ----------------
divider()
title_panel("♻️ FASE REFACTOR — MELHORIA SEGURA", COLORS["yellow"])

typewriter(
    "Com os testes verdes, o código pode ser melhorado com segurança.\n"
    "A funcionalidade externa permanece inalterada."
)

apply_version("refactor")
run_pytest()
ok("REFACTOR confirmado: testes continuam passando")

# ---------------- FINAL ----------------
divider()
title_panel("✅ CICLO TDD CONCLUÍDO COM SUCESSO", COLORS["blue"])

typewriter(
    "Resumo do ciclo executado:\n"
    "- 🔴 Testes falharam inicialmente\n"
    "- 🟢 Código mínimo foi implementado\n"
    "- ♻️ Código foi refatorado com segurança\n\n"
    "Isso é Test Driven Development na prática."
)
