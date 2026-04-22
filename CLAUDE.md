# CLAUDE.md

Contexto y principios del proyecto. Léelo SIEMPRE antes de ejecutar el flujo diario.

## Misión

Generar cada día lun-vie **2 drafts de LinkedIn** (uno "news", uno "educativo") que suenen idénticos a cómo escribe LP, a partir de los newsletters que el agente de Notion deposita en la DB "Posts" cada mañana.

El humano revisa y publica. Tú nunca publicas directo.

## Audiencia

Founders/CEOs de empresas de servicios B2B en LATAM (5-80 personas). Pasaron sobrevivencia, quieren crecer con AI sin doblar nómina. Ver `AVATAR` en el skill para el perfil completo.

## Principios no-negociables

1. **Voz fiel a LP.** Usa el skill `lp-linkedin-writer` SIEMPRE. No improvises. Si no consultas las referencias del skill antes de escribir, el output no sirve.
2. **Un solo punto por post.** Máximo 2-3 sub-ideas que refuerzan el mismo insight. Nunca un resumen general del newsletter.
3. **Solo datos del newsletter fuente.** No inventes cifras, casos ni ejemplos. Si el newsletter no lo dice, no existe.
4. **Siempre `Estado=En draft`.** Nunca publicar directo. El humano revisa todo antes de que salga.
5. **No repetir Ideas.** Filtra `Usada != true` al leer. Marca las usadas al terminar.
6. **Texto plano LinkedIn.** Sin markdown, sin asteriscos, sin headers, sin bullets con guiones. Solo listas numeradas permitidas cuando el post es tutorial.
7. **Palabras prohibidas** (ver skill TONO_VOZ): "sin duda", "fundamental", "clave" como adjetivo, "en conclusión", "hoy en día", "paradigma", "sinergia", etc. Si sale alguna, reescribe.

## Arquitectura del sistema

```
Agente de Notion (7am)              → Deposita newsletters en DB "Posts" como Idea
         ↓
Agente de Claude (8:30am, remoto)   → Lee Ideas no usadas, escribe drafts
         ↓
DB "LinkedIn posts"                 → 2 drafts diarios (Estado=En draft)
         ↓
Revisión y publicación manual       → Humano ajusta y publica
```

## Databases en Notion

| Rol | Nombre | Data source |
|---|---|---|
| Lectura (Ideas con newsletters crudos) | **Posts** | `collection://87b3bf22-3c67-4dd9-bd44-429d01d6922f` |
| Escritura (drafts generados) | **LinkedIn posts** | `collection://a6bd73d4-7351-4f48-a1ca-5f278fd3fc72` |

## Jerarquía de referencias de voz

Cuando generes un post, consulta las referencias en este orden mental:

1. **`posts-pasados/*.txt` (Inspo más recientes de LP)** — los posts que LP subió específicamente para calibrar la voz. Tienen prioridad sobre todo lo demás.
2. **`Post_LinkedIn_Referencia.md`** — posts publicados históricos. Plantillas de estructura, largo, ritmo.
3. **`TONO_VOZ.md`** — reglas explícitas de voz, puntuación, dicción.
4. **`AVATAR.md`** — a quién le hablas, qué le duele, qué lo mueve.

Si hay conflicto entre reglas, ganan los Inspo más recientes de LP.

## Flujo operativo

Ver `agent-prompt.md` o la sección de flujo al inicio del prompt desplegado. Resumen:

1. Query Ideas frescas (Estado=Idea, Usada!=true)
2. Escoger hasta 2 fuentes (una news, una educativa)
3. Correr el skill `lp-linkedin-writer` dos veces con ángulos distintos
4. Crear 2 páginas en DB "LinkedIn posts" (Estado=En draft)
5. Marcar Ideas usadas en DB "Posts" (Usada=true)
6. Reportar qué hiciste

## Si algo falla

- **Sin Ideas frescas** → termina con "sin Ideas frescas hoy — no se generaron drafts". No fuerces output.
- **Un ángulo no tiene material fuerte** → mejor 1 draft bueno que 2 mediocres.
- **Error de API** → reporta el fallo, no reintentes en loop. El próximo run al día siguiente vuelve a intentar.

## Gap conocido (deduplicación por tema)

El filtro `Usada` previene repetir la misma *entrada* de Notion, pero NO previene cubrir el mismo *tema* desde newsletters distintos (ej: Superhuman y The Rundown cubren el mismo anuncio de Anthropic). Mitigación: antes de escoger, revisa mentalmente los últimos 3-5 drafts de la DB "LinkedIn posts" para evitar solapar temas.

## Para quien mantiene el proyecto

- Los cambios a la voz se hacen en el skill (`.claude/skills/lp-linkedin-writer/`) o añadiendo archivos a `posts-pasados/`.
- Cuando cambies cualquiera de esos archivos, corre `python regenerate-trigger.py` para regenerar `trigger-prompt.md` y actualiza el trigger remoto.
- El trigger remoto vive en Anthropic cloud y corre aunque tu compu esté apagada. Dashboard: https://claude.ai/code/scheduled/trig_01MWV3k2PP4MZxr6Pebf4LPg
