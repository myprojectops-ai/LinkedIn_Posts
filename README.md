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
| `CLAUDE.md` | Contexto y principios no-negociables del proyecto. Lo lee el agente primero. |
| `agent-prompt.md` | Flujo diario del agente (pasos operativos) |
| `.claude/skills/lp-linkedin-writer/` | Skill con la voz de LP: `SKILL.md` + 3 referencias (TONO_VOZ, AVATAR, Post_LinkedIn_Referencia) |
| `posts-pasados/` | Inspo `.txt`/`.md` de LP para afinar la voz. **Prioridad alta** sobre las otras referencias. |
| `trigger-prompt.md` | Prompt consolidado desplegado en el trigger remoto (generado — NO editar a mano) |
| `regenerate-trigger.py` | Regenera `trigger-prompt.md` a partir de CLAUDE.md + agent-prompt.md + skill + posts-pasados |

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

## Cómo alimentar el agente (añadir posts pasados o cambiar algo)

1. Haz el cambio que quieras:
   - Tirar un `.md` o `.txt` en `posts-pasados/` para afinar la voz
   - Editar `CLAUDE.md` para cambiar principios / contexto
   - Editar `agent-prompt.md` para cambiar el flujo
   - Editar los archivos del skill (`.claude/skills/lp-linkedin-writer/`)

2. Regenera `trigger-prompt.md`:

```bash
python regenerate-trigger.py
```

3. Actualiza el trigger remoto con el nuevo prompt. Opción 1 (UI): https://claude.ai/code/scheduled/trig_01MWV3k2PP4MZxr6Pebf4LPg — editar el prompt manualmente copiando el contenido de `trigger-prompt.md`. Opción 2 (API): `POST /v1/code/triggers/{id}` con el contenido de `trigger-prompt.md` en `events[0].data.message.content`.

4. Commit y push los cambios al repo para mantener el historial.

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
