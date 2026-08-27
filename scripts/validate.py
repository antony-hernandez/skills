#!/usr/bin/env python3
"""Valida los manifiestos del marketplace y exige bump de version cuando cambia un plugin.

Claude Code decide si baja una version nueva comparando el string de version resuelto:
si `version` en plugin.json no cambia, el usuario se queda con la copia cacheada aunque
hayas pusheado commits. Este script existe para que ese olvido rompa el CI y no llegue
silenciosamente a quien tiene la skill instalada.
"""
import json
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SEMVER = re.compile(r"^\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?$")
errors: list[str] = []


def fail(msg: str) -> None:
    errors.append(msg)


def load(path: pathlib.Path):
    try:
        return json.loads(path.read_text())
    except FileNotFoundError:
        fail(f"falta {path.relative_to(ROOT)}")
    except json.JSONDecodeError as exc:
        fail(f"{path.relative_to(ROOT)}: JSON inválido — {exc}")
    return None


def validate_manifests() -> list[str]:
    """Devuelve los nombres de plugin declarados en el marketplace."""
    market = load(ROOT / ".claude-plugin" / "marketplace.json")
    if market is None:
        return []

    for field in ("name", "owner", "plugins"):
        if field not in market:
            fail(f"marketplace.json: falta el campo requerido `{field}`")

    names = []
    for entry in market.get("plugins", []):
        name = entry.get("name")
        source = entry.get("source")
        if not name or not source:
            fail(f"marketplace.json: entrada sin `name` o `source`: {entry}")
            continue
        if "version" in entry:
            # Documentado: plugin.json siempre gana y la de marketplace.json se ignora
            # sin aviso, así que una version acá solo puede quedar desactualizada.
            fail(f"marketplace.json: `{name}` no debe declarar `version`; vive en su plugin.json")

        plugin_dir = (ROOT / source).resolve()
        manifest = plugin_dir / ".claude-plugin" / "plugin.json"
        plugin = load(manifest)
        if plugin is None:
            continue

        if plugin.get("name") != name:
            fail(f"{name}: plugin.json declara `{plugin.get('name')}`, distinto del marketplace")
        version = plugin.get("version")
        if not version:
            fail(f"{name}: plugin.json sin `version` — sin ella nadie recibe updates")
        elif not SEMVER.match(str(version)):
            fail(f"{name}: version `{version}` no es semver")

        skills = list(plugin_dir.glob("skills/*/SKILL.md"))
        if not skills:
            fail(f"{name}: no hay ninguna skills/<nombre>/SKILL.md")
        for skill in skills:
            head = skill.read_text()[:2000]
            if not head.startswith("---"):
                fail(f"{skill.relative_to(ROOT)}: falta el frontmatter YAML")
                continue
            front = head.split("---", 2)[1]
            for key in ("name:", "description:"):
                if key not in front:
                    fail(f"{skill.relative_to(ROOT)}: frontmatter sin `{key.rstrip(':')}`")

        names.append(name)
    return names


def validate_version_bump(names: list[str], base: str) -> None:
    def git(*args: str) -> str:
        return subprocess.run(
            ["git", *args], cwd=ROOT, capture_output=True, text=True, check=False
        ).stdout.strip()

    if not git("rev-parse", "--verify", "--quiet", base):
        print(f"aviso: no encuentro la ref base `{base}`; salteo el chequeo de bump")
        return

    for name in names:
        prefix = f"plugins/{name}/"
        changed = [p for p in git("diff", "--name-only", base, "HEAD").splitlines() if p.startswith(prefix)]
        if not changed:
            continue
        manifest = f"{prefix}.claude-plugin/plugin.json"
        before = git("show", f"{base}:{manifest}")
        after = (ROOT / manifest).read_text()
        old = json.loads(before).get("version") if before else None
        new = json.loads(after).get("version")
        if old is not None and old == new:
            fail(
                f"{name}: cambiaron archivos del plugin pero `version` sigue en {new}. "
                "Sin bump, Claude Code no baja la versión nueva a quien ya la tiene instalada."
            )


if __name__ == "__main__":
    plugin_names = validate_manifests()
    if len(sys.argv) > 1:
        validate_version_bump(plugin_names, sys.argv[1])

    if errors:
        print("\n".join(f"✗ {e}" for e in errors))
        sys.exit(1)
    print(f"✓ manifiestos válidos ({len(plugin_names)} plugin(s): {', '.join(plugin_names)})")
