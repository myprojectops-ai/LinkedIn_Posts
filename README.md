# LinkedIn Daily Drafts Agent

Agente que cada día lun-vie a las 8:30am Bogotá lee las AI news que deposita otro agente en Notion y genera 2 drafts de LinkedIn (uno "news", uno "educativo") en la voz de LP.

## Cómo funciona

```
Agente de Notion (7am)             → Deposita newsletters en DB "Posts" como Idea
          ↓
Agente de Claude (8:30am, remoto)  → Lee Ideas no usadas, escoge 2, escribe drafts
          ↓
DB "LinkedIn posts" en Notion      → Drafts listos para revisar (Estado = En draft)
          ↓
Ideas fuente en DB "Posts"         → Quedan con Usada = true (no se repiten)
```

## Estructura del proyecto

| Archivo / carpeta | Qué es |
|---|---|
| `.claude/skills/lp-linkedin-writer/` | Skill con la voz de LP: `SKILL.md` + 3 referencias (TONO_VOZ, AVATAR, Post_LinkedIn_Referencia) |
| `agent-prompt.md` | Instrucciones del flujo diario (fuente humana-legible) |
| `trigger-prompt.md` | Prompt consolidado que corre el agente remoto (se regenera desde los 4 archivos del skill + `agent-prompt.md`) |
| `posts-pasados/` | Tira aquí `.md` o `.txt` con posts pasados para afinar la voz. Cuando añadas archivos, regenera `trigger-prompt.md` (ver abajo) |

## Trigger remoto

- **ID**: `trig_01MWV3k2PP4MZxr6Pebf4LPg`
- **Dashboard**: https://claude.ai/code/scheduled/trig_01MWV3k2PP4MZxr6Pebf4LPg
- **Schedule**: `30 13 * * 1-5` (UTC) = 8:30am Bogotá, lun-vie
- **Modelo**: `claude-sonnet-4-6`
- **MCP conectado**: Notion

## Notion — recursos

| Recurso | URL |
|---|---|
| DB "Posts" (fuente, Ideas con newsletters) | https://www.notion.so/7967dcc8dcfd4db1b527e59ade4aaa0c |
| DB "LinkedIn posts" (destino, drafts generados) | https://www.notion.so/5e2ea9281266400194177e6f6a5e0b81 |

## Cómo alimentar el agente (añadir posts pasados)

1. Tira archivos `.md` o `.txt` en `posts-pasados/`. Uno por post, o varios posts en un mismo archivo separados por `---`.
2. Regenera `trigger-prompt.md`:

```bash
python -c "
from pathlib import Path
base = Path('.')
skill = base / '.claude/skills/lp-linkedin-writer'
pasados = base / 'posts-pasados'

agent_prompt = (base / 'agent-prompt.md').read_text(encoding='utf-8')
skill_md = (skill / 'SKILL.md').read_text(encoding='utf-8')
avatar = (skill / 'references/AVATAR.md').read_text(encoding='utf-8')
tono = (skill / 'references/TONO_VOZ.md').read_text(encoding='utf-8')
posts_ref = (skill / 'references/Post_LinkedIn_Referencia.md').read_text(encoding='utf-8')

extras = []
for f in sorted(pasados.iterdir()):
    if f.is_file() and f.suffix.lower() in ('.md', '.txt'):
        extras.append(f'### {f.stem}\n\n{f.read_text(encoding=\"utf-8\").strip()}')

extras_block = ''
if extras:
    extras_block = '\n\n---\n\n## REFERENCIA EXTRA — Posts pasados propios (subidos por el usuario)\n\n' + '\n\n'.join(extras)

consolidated = f'''{agent_prompt}

---

# APÉNDICE: Skill lp-linkedin-writer (embebido)

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
'''

(base / 'trigger-prompt.md').write_text(consolidated, encoding='utf-8')
print(f'Wrote trigger-prompt.md ({len(consolidated):,} chars)')
"
```

3. Actualiza el trigger remoto con el nuevo prompt. Opción 1 (UI): https://claude.ai/code/scheduled/trig_01MWV3k2PP4MZxr6Pebf4LPg — editar el prompt manualmente. Opción 2 (API): pasarle el contenido de `trigger-prompt.md` al `events[0].data.message.content` del trigger via `POST /v1/code/triggers/{id}`.

## DB "LinkedIn posts" — schema

| Propiedad | Tipo | Uso |
|---|---|---|
| `Post` | title | Primera línea del draft (hook elegido) |
| `Estado` | select | `En draft` / `En edición` / `Publicado` |
| `Tipo` | select | `News` / `Educativo` |
| `Fuente URL` | url | Link al newsletter fuente |
| `Fuente` | text | Título de la Idea fuente en la DB "Posts" |
| `Fecha` | date | Día en que se generó el draft |

El body de cada página tiene: post completo + separador `---` + `5 hooks alternativos:` + los 5 hooks numerados.

## Anti-repetición

La DB "Posts" tiene una propiedad `Usada` (checkbox). Cuando el agente usa una Idea, la marca como `Usada=true`. El query del día siguiente filtra `Estado=Idea AND Usada != true`, así nunca repite una entrada.

**Gap conocido**: si dos newsletters distintos (Superhuman y The Rundown) cubren el mismo anuncio el mismo día, son 2 Ideas distintas. Se podría pillar una hoy y otra mañana sobre el mismo tema. Mitigación: revisar los drafts antes de publicar.

## Costo estimado

~$4-8 USD/mes con Claude Sonnet 4.6 (21 runs mensuales).
