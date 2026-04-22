# Daily LinkedIn Drafts Agent

Genera 2 drafts de LinkedIn por día (uno "news", uno "educativo") a partir de las noticias que el agente de Notion deposita en la base Posts.

## Contexto

- **DB FUENTE (Ideas — lectura)**: `collection://87b3bf22-3c67-4dd9-bd44-429d01d6922f` (base "Posts" en Notion). El agente de Notion deposita ahí las noticias diarias como entries con `Estado="Idea"`.
- **DB DESTINO (Drafts — escritura)**: `collection://a6bd73d4-7351-4f48-a1ca-5f278fd3fc72` (base "LinkedIn posts" en Notion). Los drafts que genera este agente quedan ahí.
- **Skill obligatorio**: `lp-linkedin-writer` (en `.claude/skills/`). Escribe con la voz de LP. Input = newsletter / bloque grande. Output = post plain-text para LinkedIn + 5 hooks alternativos.
- **Audiencia del post**: founders/CEOs de empresas de servicios B2B en LATAM (5-80 personas) que quieren crecer con AI.

## Propiedades de la DB FUENTE ("Posts")

| Propiedad | Tipo | Uso |
|---|---|---|
| `Post` | title | Título de la noticia |
| `Estado` | status | `Idea` (noticia sin procesar), y otros estados editoriales legacy |
| `Formato` | select | `Post`, `Reel`, etc. |
| `Link (URL)` | url | URL del newsletter fuente |
| `Notas` | text | Cuerpo completo del newsletter |
| `Fecha de publicación` | date | Fecha de la noticia |
| `Usada` | checkbox | `__YES__` si ya se generó un draft de esa Idea |

## Propiedades de la DB DESTINO ("LinkedIn posts")

| Propiedad | Tipo | Uso |
|---|---|---|
| `Post` | title | Hook / primera línea del draft |
| `Estado` | select | `En draft` (default), `En edición`, `Publicado` |
| `Tipo` | select | `News` o `Educativo` |
| `Fuente URL` | url | URL del newsletter fuente |
| `Fuente` | text | Título de la Idea fuente (para trazabilidad) |
| `Fecha` | date | Fecha de generación (hoy) |

## Flujo

### 1. Query Ideas frescas

Usa `mcp__claude_ai_Notion__notion-search` con `data_source_url: "collection://87b3bf22-3c67-4dd9-bd44-429d01d6922f"` y query vacío o amplio, o `notion-query-database-view` sobre la vista "Todos". Filtra localmente por:
- `Estado == "Idea"`
- `Usada != "__YES__"` (o null)
- Ordena por `date:Fecha de publicación:start` desc

Toma las 10 más recientes. Lee el contenido de `Notas` (cuerpo del newsletter) de cada una.

**Si no hay Ideas frescas**: termina con mensaje "sin Ideas frescas hoy — no se generaron drafts" y salte los pasos siguientes.

### 2. Escoger fuentes (hasta 2)

Elige internamente, sin anunciar:

- **Fuente para ángulo NEWS** → la Idea con la noticia/anuncio de mercado más sorprendente o contraintuitiva. Mira movimientos de labs (Anthropic, OpenAI, Google), nuevos productos, cifras impactantes, decisiones estratégicas que reencuadren el mercado.
- **Fuente para ángulo EDUCATIVO** → la Idea con el how-to o insight más accionable para un founder que opera hoy. Tutoriales de prompts, workflows concretos, casos de uso aplicables esta semana, formas de ahorrar tiempo/dinero con AI.

Puede ser la MISMA Idea si un solo newsletter cubre ambos fuertes (p.ej. uno que anuncia un lanzamiento y además trae un how-to).

### 3. Ejecutar el skill `lp-linkedin-writer` — POST #1 (news)

Activa el skill pasándole el contenido completo de `Notas` de la Idea elegida como input. Al final del input añade:

```
---
Ángulo requerido para este post: NEWS / movimiento de mercado. Escoge el punto del newsletter con mayor sorpresa o reencuadre estratégico — algo que un founder de servicios B2B en LATAM necesita ver hoy.
```

El skill devolverá: **post completo** + **5 hooks alternativos**. Captúralo tal cual.

### 4. Ejecutar el skill `lp-linkedin-writer` — POST #2 (educativo)

Repite con la otra Idea (o la misma si es el caso). Input = `Notas` de esa Idea + al final:

```
---
Ángulo requerido para este post: EDUCATIVO / accionable. Escoge el punto más práctico que un founder pueda aplicar esta semana en su negocio. Tutorial, workflow, prompt, decisión concreta — no hype abstracto.
```

### 5. Crear los 2 drafts en la DB "LinkedIn posts"

Usa `mcp__claude_ai_Notion__notion-create-pages` apuntando a la DB DESTINO:

```json
{
  "parent": { "type": "data_source_id", "data_source_id": "a6bd73d4-7351-4f48-a1ca-5f278fd3fc72" },
  "pages": [
    {
      "properties": {
        "Post": "<primera línea del post news — máx 80 chars>",
        "Estado": "En draft",
        "Tipo": "News",
        "Fuente URL": "<URL de la Idea fuente news>",
        "Fuente": "<título Idea news>",
        "date:Fecha:start": "YYYY-MM-DD"
      },
      "content": "<POST COMPLETO news>\n\n---\n\n5 hooks alternativos:\n\n1. <hook1>\n2. <hook2>\n3. <hook3>\n4. <hook4>\n5. <hook5>"
    },
    {
      "properties": {
        "Post": "<primera línea del post educativo — máx 80 chars>",
        "Estado": "En draft",
        "Tipo": "Educativo",
        "Fuente URL": "<URL de la Idea fuente educativo>",
        "Fuente": "<título Idea educativo>",
        "date:Fecha:start": "YYYY-MM-DD"
      },
      "content": "<POST COMPLETO educativo>\n\n---\n\n5 hooks alternativos:\n\n1. <hook1>\n2. <hook2>\n3. <hook3>\n4. <hook4>\n5. <hook5>"
    }
  ]
}
```

### 6. Marcar las Ideas fuente como usadas (en la DB FUENTE)

Para cada Idea que usaste (1 o 2), `mcp__claude_ai_Notion__notion-update-page` sobre la entry en la DB "Posts":

```json
{
  "page_id": "<id de la Idea en la DB Posts>",
  "command": "update_properties",
  "properties": { "Usada": "__YES__" },
  "content_updates": []
}
```

Nota: el flag `Usada` vive en la DB FUENTE (Posts), no en la DB DESTINO (LinkedIn posts).

### 7. Reporte final

Devuelve 4-6 líneas:

```
OK — 2 drafts creados
• News:      <hook primera línea> → <url draft Notion>
• Educativo: <hook primera línea> → <url draft Notion>
Fuentes marcadas como Usada: <título(s) Idea>
```

## Reglas fijas

1. El skill `lp-linkedin-writer` es obligatorio. No escribir posts sin pasarlos por el skill (cargará los 3 archivos de referencia: TONO_VOZ, AVATAR, Post_LinkedIn_Referencia).
2. Estado de los drafts nuevos siempre `En draft` — nunca publicar directo.
3. Usa solo datos que estén en `Notas`. No inventes cifras, casos ni ejemplos.
4. Si una fuente no tiene suficiente material para uno de los ángulos, úsala igual para el otro y deja un solo draft (reporta en el resumen final).
5. Nunca dupliques una Idea ya usada — el filtro `Usada != __YES__` es lo que previene repeticiones.
6. No uses WebFetch ni scrapers — todo el contenido viene del campo `Notas` en Notion.
