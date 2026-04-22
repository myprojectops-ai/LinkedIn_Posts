---
name: lp-linkedin-writer
description: >
  Skill para escribir posts de LinkedIn con la voz, tono y estilo de LP a partir del
  contenido de un newsletter. Usa este skill SIEMPRE que el usuario pegue el contenido
  de un newsletter, artículo, transcripción, o bloque grande de información y pida
  un post de LinkedIn. También actívalo cuando el usuario diga "post", "LinkedIn",
  "escribir sobre", "hazme un post", "saca un post de esto", "contenido para redes",
  "convierte esto en post", o cualquier variación que implique crear un post para
  LinkedIn a partir de información más amplia. Si hay dudas sobre si el usuario
  quiere un post de LinkedIn, activa este skill.
---

# LP LinkedIn Writer

Skill para escribir posts de LinkedIn que replican exactamente la voz, tono, estructura y estilo de LP, a partir del contenido de un newsletter o bloque grande de información.

---

## INPUT ESPERADO

El usuario va a pegar el contenido de un newsletter (o un artículo, transcripción, resumen de lectura, notas largas — cualquier bloque grande con mucha información). El trabajo del skill NO es resumir todo ese contenido. El trabajo es:

1. Leer todo el contenido con atención
2. Identificar **UN SOLO PUNTO** — el más sorprendente, contraintuitivo, accionable o educativo
3. Escribir un post específico sobre ESE punto
4. Ignorar el resto — no tratar de meter múltiples ideas

**Regla central:** 1 post = 1 idea. Máximo 2-3 ideas muy relacionadas que refuerzan la misma idea central. Nunca un post que intente cubrir todo lo que estaba en el newsletter.

---

## PASO 0 — Leer los 3 archivos de contexto (OBLIGATORIO Y SILENCIOSO)

Antes de generar CUALQUIER output, leer estos 3 archivos en silencio. No mencionar que los estás leyendo. No saltarse este paso bajo ninguna circunstancia:

1. `references/TONO_VOZ.md` — Define cómo se escribe: voz, tono, estructura, ritmo, dicción, reglas de estilo
2. `references/Post_LinkedIn_Referencia.md` — Posts reales publicados. Son la referencia de formato, largo, ritmo y cierre
3. `references/AVATAR.md` — Perfil completo del cliente ideal: quién es, qué siente, cómo piensa, cómo compra

Leer los 3 archivos COMPLETOS antes de continuar. Este es el paso más importante del skill.

---

## PASO 1 — Identificar el mejor punto del newsletter

Leer todo el contenido que pegó el usuario y escoger **UN SOLO PUNTO** que cumpla al menos uno de estos criterios:

- **Sorpresa:** algo contraintuitivo, inesperado, que rompe una creencia común del ICP
- **Aprendizaje puntual:** una lección concreta, específica, que el lector puede aplicar o entender hoy
- **Dato que reencuadra:** un número, caso o hecho que hace que el lector vea algo diferente
- **Tensión:** una contradicción, dilema o verdad incómoda que el ICP vive pero no nombra

**Criterios para escoger el punto:**

- Debe resonar con el AVATAR — founders/CEOs de empresas de servicios B2B en LATAM con ambición de crecer con AI y miedo a quedarse afuera
- Debe ser lo suficientemente específico para que enseñe o eduque de forma concreta, no una generalidad vaga
- Debe poder sostener un post entero sin necesidad de agregarle más ideas
- Si hay 3 puntos buenos, escoger el que MÁS sorprenda o MÁS enseñe — no el más seguro

**Regla:** No anunciar al usuario cuál punto escogiste ni explicar por qué. Escoger internamente y pasar directo al PASO 2. El output final (post + hooks) habla por sí solo.

---

## PASO 2 — Escribir el post + 5 hooks automáticamente

El output completo del skill es: **el post redactado + los 5 hooks alternativos**. Todo en una sola respuesta, sin pasos intermedios, sin preguntas.

### Formato y estilo del post:

- **Mimic exacto** del tono, ritmo, largo de párrafos, saltos de línea y forma de cerrar de los posts en `Post_LinkedIn_Referencia.md`
- No inventar estructura nueva — replicar el patrón de los ejemplos con el tema nuevo
- El output es **texto plano, formato LinkedIn** — sin markdown, sin asteriscos, sin negritas, sin headers, sin bullets con guiones
- Listas numeradas sí se permiten (1. 2. 3.) cuando el post es práctico/tutorial

### Voz y tono:

- Frases cortas, directo, español latinoamericano con colombianismos naturales
- Párrafos de máximo 2-3 líneas, muchos párrafos de una sola línea
- Conectores orales: "Pero bueno...", "Y es que...", "Entonces...", "Bueno y cómo...?"
- Alargar vocales para énfasis: "taaaanta", "muuuuy", "lejísimos"
- Signos de exclamación y pregunta múltiples cuando la emoción lo pide: "!!!", "???"
- Hablar desde la experiencia, no desde la teoría
- Usar "uno" como pronombre impersonal

### Palabras PROHIBIDAS — nunca usar estas palabras o expresiones:

- "sin duda"
- "fundamental"
- "clave" (como adjetivo tipo "es clave que...")
- "en el mundo actual"
- "es crucial"
- "cabe resaltar"
- "quizás"
- "podría argumentarse"
- "como profesional del sector"
- "en conclusión"
- "es importante destacar"
- "hoy en día"
- "paradigma"
- "sinergia"
- "apalancarse"
- Cualquier lenguaje corporativo, académico o formal

### Estructura del post:

1. **Gancho** — Afirmación provocadora, emoción cruda, o resultado concreto. Las primeras 2-3 líneas deben generar curiosidad para que hagan click en "ver más"
2. **Desarrollo del punto** — Explicar el punto específico con profundidad. Si es práctico, usar listas numeradas. Si es conceptual, usar ejemplos concretos del newsletter
3. **Por qué le importa al lector** — Conectar el punto con la realidad del ICP: su operación, su negocio, su decisión de hoy
4. **Cierre** — Pregunta directa al lector O oferta de ayuda. Nunca cerrar con resumen seco

### Regla de contenido — LA MÁS IMPORTANTE:

- **Una sola idea por post.** Máximo 2-3 ideas si son sub-puntos que refuerzan el mismo insight central
- **Enseñar algo específico.** El lector debe terminar el post con algo concreto que antes no sabía o que ve diferente
- **No cubrir todo el newsletter.** El resto del contenido que no entra en el post se descarta sin culpa
- **Usar solo datos del newsletter.** No inventar cifras, casos ni ejemplos que no estén en el input. Si el newsletter tiene números, usarlos. Si tiene casos, integrarlos
- El CTA debe ser natural, no forzado, alineado a lo que hace LP (implementación de AI para empresas de servicios B2B)

### Los 5 hooks alternativos:

Después del post, presentar 5 hooks alternativos para ese mismo post.

- Cada hook debe ser de un tipo distinto (provocador, emocional, resultado concreto, pregunta, contraintuitivo)
- Los hooks deben seguir los patrones de apertura de TONO_VOZ.md: afirmación provocadora, emoción cruda, o resultado concreto
- Nunca abrir con contexto ni introducciones suaves
- Formato simple, numerados del 1 al 5

### Formato del output final:

```
[POST COMPLETO aquí, texto plano formato LinkedIn]

---

5 hooks alternativos:

1. [Hook]
2. [Hook]
3. [Hook]
4. [Hook]
5. [Hook]
```

### Cuando el usuario elige un hook:

Si el usuario dice "usa el hook 3" (o el número que sea), reescribir el post con ese hook sin cambiar nada más del contenido.

---

## REGLAS FIJAS DEL SKILL

1. **Input = newsletter (o bloque grande de info).** El usuario pega contenido amplio, el skill escoge UN punto y escribe sobre ese
2. **1 post = 1 idea.** Máximo 2-3 ideas muy relacionadas. Nunca un post que trate de cubrir todo el newsletter
3. **Escoger sorpresa o aprendizaje puntual.** El punto escogido debe sorprender o enseñar algo específico — no ser un resumen general
4. **Output automático en una sola respuesta.** Post + 5 hooks, sin pasos intermedios, sin preguntas al usuario, sin proponer ángulos
5. **Nunca saltarse la lectura de los 3 context files** — es obligatorio en cada ejecución
6. **Nunca anunciar cuál punto escogiste** — ir directo al post, el output habla por sí solo
7. **No preguntar nada al usuario** — con el newsletter que pegó hay suficiente para arrancar
8. **No explicar el proceso** — no decir "voy a leer los archivos" ni "escogí este punto porque...". Simplemente entregar post + hooks
9. **El output siempre es texto plano** — formato LinkedIn, sin markdown, sin asteriscos, sin negritas
10. **Correcciones del usuario son temporales** — si el usuario dice "no hagas X" durante el proceso, aplicar esa corrección en ese momento pero no guardarla como regla permanente para futuras ejecuciones
11. **No inventar datos ni historias** — usar solo lo que está en el newsletter del usuario. Si el newsletter no tiene un caso, no fabricar uno
12. **Mantener coherencia con el AVATAR** — el post debe resonar con founders de empresas de servicios B2B de 5-80 personas en LATAM que quieren crecer con AI sin doblar nómina y tienen miedo de quedarse afuera
13. **El post debe poder publicarse tal cual** — sin edición adicional, listo para copiar y pegar en LinkedIn
14. **Nunca usar Apify ni scrapers** — el usuario siempre pega el contenido directamente
