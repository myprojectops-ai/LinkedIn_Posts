"""Regenera trigger-prompt.md consolidando todas las fuentes.

Uso:
    python regenerate-trigger.py

Lee:
- CLAUDE.md (contexto y principios, primero)
- agent-prompt.md (flujo diario)
- .claude/skills/lp-linkedin-writer/SKILL.md + references/*
- posts-pasados/*.md y *.txt (Inspo extras de LP, prioridad alta)

Escribe:
- trigger-prompt.md (el prompt consolidado que usa el trigger remoto)

Después de ejecutar, actualiza el trigger remoto con el nuevo contenido.
Dashboard: https://claude.ai/code/scheduled/trig_01MWV3k2PP4MZxr6Pebf4LPg
"""

from pathlib import Path

BASE = Path(__file__).parent
SKILL = BASE / ".claude/skills/lp-linkedin-writer"
PASADOS = BASE / "posts-pasados"

claude_md = (BASE / "CLAUDE.md").read_text(encoding="utf-8")
agent_prompt = (BASE / "agent-prompt.md").read_text(encoding="utf-8")
skill_md = (SKILL / "SKILL.md").read_text(encoding="utf-8")
avatar = (SKILL / "references/AVATAR.md").read_text(encoding="utf-8")
tono = (SKILL / "references/TONO_VOZ.md").read_text(encoding="utf-8")
posts_ref = (SKILL / "references/Post_LinkedIn_Referencia.md").read_text(encoding="utf-8")

extras = []
for f in sorted(PASADOS.iterdir()):
    if f.is_file() and f.suffix.lower() in (".md", ".txt") and f.name != ".gitkeep":
        content = f.read_text(encoding="utf-8").strip()
        if content:
            extras.append(f"### {f.stem}\n\n{content}")

extras_block = ""
if extras:
    extras_block = (
        "\n\n---\n\n## REFERENCIA EXTRA — Inspo propios de LP (prioridad alta)\n\n"
        "Estos posts son los más representativos de cómo escribe LP hoy. "
        "Cuando haya conflicto entre reglas, estos Inspo ganan.\n\n"
        + "\n\n".join(extras)
    )

consolidated = f"""# ======================================================================
# CLAUDE.md — LEE ESTO PRIMERO
# ======================================================================

{claude_md}

---

# ======================================================================
# FLUJO DIARIO (agent-prompt.md)
# ======================================================================

{agent_prompt}

---

# ======================================================================
# APÉNDICE: Skill lp-linkedin-writer (embebido)
# ======================================================================

El entorno remoto NO tiene filesystem local. Cuando el flujo diga "activa el skill lp-linkedin-writer", sigue las instrucciones de SKILL.md y consulta internamente las referencias embebidas abajo (sin anunciarlo).

---

## SKILL.md

{skill_md}

---

## Referencia 1/3 — TONO_VOZ.md

{tono}

---

## Referencia 2/3 — AVATAR.md

{avatar}

---

## Referencia 3/3 — Post_LinkedIn_Referencia.md

{posts_ref}
{extras_block}
"""

out = BASE / "trigger-prompt.md"
out.write_text(consolidated, encoding="utf-8")

print(f"[OK] Wrote {out.name}")
print(f"  Size:            {len(consolidated):,} chars (~{len(consolidated)//4:,} tokens)")
print(f"  Inspo embebidos: {len(extras)}")
print()
print("Próximo paso: actualiza el trigger remoto con este contenido.")
print("Dashboard: https://claude.ai/code/scheduled/trig_01MWV3k2PP4MZxr6Pebf4LPg")
