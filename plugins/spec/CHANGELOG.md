# Changelog — spec

Format: [Keep a Changelog](https://keepachangelog.com/en/1.1.0/). Versioning: [SemVer](https://semver.org/).

## [0.9.0] — 2026-08-27

### Added
- **Phase 2 — Project and ecosystem.** Before framing the HU, load agent instructions (`AGENTS.md`, `CLAUDE.md`, project rules), the real module map, and living conventions — not only FRD/PRD.
- **Stack viability gate.** Proposals must fit technologies and platform limits already in the repo. New infra/deps without explicit OK become blocking questions, not CT rows.
- Common-errors rows for skipping ecosystem discovery and inventing stack pieces.

### Changed
- Process renumbered to 9 phases (project/ecosystem sits between document context and framing).

## [0.8.1] — 2026-08-26

### Fixed
- Igual que 0.7.0, la **0.8.0 se publicó sin los cambios en `SKILL.md`**: el script abortó
  en un ancla inexistente antes de escribir el archivo, y el bump corría aparte. Esta trae
  los cambios que 0.8.0 describía. La secuencia ahora encadena la verificación del archivo
  antes del commit, en vez de dejarla para después del push.

## [0.8.0] — 2026-08-26

Dos devoluciones del equipo sobre la misma sección: primero que el bloque salía recortado
en la tabla, después que era demasiado código.

### Added
- **Pseudocódigo, no código.** El bloque describe el algoritmo, no la implementación.
  Escribirlo con sintaxis del lenguaje —llaves, funciones flecha, literales de objeto,
  marcadores de diff— hace que el revisor corrija sintaxis en vez de discutir la lógica, y
  que quien implementa lo copie en lugar de resolverlo en su stack. La forma que funciona
  es la de un algoritmo de manual: `Entrada:`, pasos numerados, viñetas por caso, con los
  nombres reales de campos y funciones dentro de la frase.
- **Antes de inventar un estilo, mirar si el documento ya tiene uno.** Las specs suelen
  traer un bloque de algoritmo escrito por el LT en la sección de solución; copiar esa
  forma hace que la sección se lea como parte del mismo documento.
- Para el cambio que cablea una llamada, el bloque debe incluir **las ramas donde la
  llamada no entra**, que suelen ser la mitad del cambio.

### Changed
- La regla de "el bloque va en la celda" se completa con las dos condiciones que la hacen
  viable: **tabla a ancho completo** con reparto de columnas a favor de `Detalle`, y bloque
  escrito a **64 columnas**. Sueltas no alcanzan — un bloque en una celda angosta no tiene
  wrap ni scroll, y se leen los primeros veinte caracteres de cada línea. Los comentarios
  alineados a la derecha son los que estiran; van arriba, en su propio renglón.

## [0.7.1] — 2026-08-26

### Fixed
- La 0.7.0 se publicó con su entrada de changelog pero **sin los cambios en `SKILL.md`**:
  el script que los aplicaba abortó en un reemplazo cuyo texto ancla ya no existía, y el
  archivo nunca se escribió. Esta versión trae los cambios que 0.7.0 describía.

## [0.7.0] — 2026-08-26

Corrige una regla que 0.6.0 tomó prestada y que en la práctica empeoró las specs.

### Changed
- **El código vuelve adentro de la celda.** Sacarlo abajo dejaba la celda más limpia y le
  daba ancho y resaltado al bloque, pero el precio era que la fila dejaba de ser el cambio
  y pasaba a ser un puntero al cambio: quien lee la fila ya no podía implementarla sin
  irse a otro lado. Solo se saca cuando el bloque es material de referencia largo —un
  archivo entero, un esquema grande— y no el cambio en sí.
- **Prohibido citar identificadores de decisión** (`ADR-6`, `B11`, ids de acta). Obligan a
  abrir otra página para entender la fila, y esa página envejece por su cuenta. Se escribe
  lo que el identificador dice.

### Added
- La regla que ordena las dos anteriores: **la fila tiene que bastarse sola**. Quien va a
  implementar lee una fila y tiene que poder escribir el código sin salir de ahí; eso manda
  sobre cualquier consideración de prolijidad.

## [0.6.1] — 2026-08-26

### Changed
- La tabla vuelve a **cuatro columnas**: se saca el `#` que había entrado en 0.6.0.
  Confluence numera las filas solo con `data-number-column`, así que una columna a mano
  duplica lo que la tabla ya hace y obliga a renumerar entera cada vez que se inserta una
  fila en el medio.
- Sin `#`, los bloques de código dejan de necesitar id: se titulan con el mismo nombre que
  su fila y la fila cierra apuntándolo.

## [0.6.0] — 2026-08-26

Fusión con una plantilla de otro equipo. Su fuerte era el formato del documento; el
nuestro, el proceso de investigación. Se toma cada mitad de donde estaba mejor resuelta.

### Added
- **Tabla de cinco columnas:** `#` · `Qué` · `Archivo` · `Detalle` · `Estado`. El `#`
  permite referenciar filas —hizo falta apenas la tabla pasó de seis filas—, `Archivo` es
  columna navegable, y `Estado` con íconos (🆕 🔧 🗑️ ✅) deja ver de un vistazo cuánto se
  crea y cuánto se toca. El orden de las filas es la secuencia de construcción.
- **Los bloques de código van después de la tabla**, referenciados desde la fila con un
  id. Dentro de la celda el código es ilegible y pierde el resaltado de sintaxis; en
  Confluence encima queda en una columna angosta.
- **Sección `🔎 Contexto de desarrollo`**, antes de Cambios Técnicos: la casa de todo lo
  que no es un cambio. Sin ese lugar, el contexto transversal termina colándose como fila
  o perdiéndose en la conversación.
- **Sección `✅ Hallazgos verificados`**, al final de Cambios Técnicos, para lo que costó
  encontrar y no debería reinvestigarse.
- **Trade-off obligatorio** en Decisiones Claves, con topes numéricos (5–8 decisiones,
  3–6 riesgos), y la distinción riesgo ≠ pendiente.
- **Aclaración de notación del ✅**, la lista de suposiciones caras a verificar, y la
  relectura final en busca de contradicciones internas entre el código y la prosa.

### Changed
- Se lee **la rama base de la iniciativa**, no `develop`. En una iniciativa multi-HU con
  las hermanas mergeadas en una rama de feature, leer `develop` hace que media tabla diga
  "no existe" sobre código ya escrito.
- La columna `Qué` pierde la etiqueta entre paréntesis: la daban por duplicado el ícono de
  `Estado` y la palabra que abre `Cambios propuestos`.
- Un `✅ Reusar` sigue siendo fila solo con acción propia; documentar un patrón existente
  va a `🔎 Contexto de desarrollo`.

## [0.5.0] — 2026-08-26

Aprendizajes de terminar el refinamiento de HU-003, ya con el proceso de 0.4.0 andando.

### Added
- **El algoritmo en la celda.** Una fila solo en prosa se entiende y no se puede
  implementar. Después de la prosa va pseudocódigo cuando hay recorrido u orden, firma y
  forma de los datos cuando el cambio es un contrato, o el punto exacto de inserción en
  estilo diff cuando es cablear algo en una secuencia existente. Escribirlo obliga a
  resolver lo que la prosa deja ambiguo: en el caso real, redactar el recorrido dejó a la
  vista que una bandera que la prosa proponía rastrear sobraba.
- **Segunda pasada de revisión: ¿está partida de más?** Si al borrar una fila otra deja de
  funcionar, no eran dos cambios sino uno contado dos veces. La unidad es el cambio, no el
  motivo — partir un mismo archivo en cuatro filas porque cada parte tiene su porqué
  produce filas indistinguibles y una estimación inflada.
- **Tabla de acuerdos al cerrar el debate**, una línea por decisión y en lenguaje de
  negocio: un malentendido se detecta en una línea, no en tres párrafos.
- **Dos preguntas al catálogo de rastreo:** si la consulta que resuelve el destino devuelve
  uno o varios y está indexada por lo que creés — un `getByX` que filtra por empresa y
  canal pero no por el agente puede devolver el documento de otro —, y si el documento
  sobre el que se va a escribir ya existe cuando el paso corre.
- **Dónde queda la salvaguarda cuando se decide autoritativo:** en los tests y en la
  observabilidad, y eso se escribe en la fila — qué test es la red y qué log tiene que ser
  visible para enterarse antes que el usuario.

### Changed
- Publicar exige haber **mostrado las filas redactadas**, no solo haber acordado el plan.

## [0.4.0] — 2026-08-25

Reescritura completa. Las tres versiones anteriores fueron parches sucesivos, cada una
tapando el agujero de la anterior; la estructura ya no sostenía lo aprendido.

El defecto de fondo era el salto de "leer los documentos" a "escribir la tabla". Produce
filas que suenan bien y describen lugares equivocados: la spec decía enganchar en el
servicio de publish, se escribió la fila, y resultó que publicar un flujo ocurre por dos
caminos — el publish directo y un job programado que promueve lo que espera aprobación de
Meta. El segundo no pasa por ese servicio. La fila apuntaba a un observador, no a un camino.

### Added
- Proceso de 8 fases con dos nuevas antes de redactar: **Flujo**, que traza cada lugar de
  punta a punta, y **Debate**, donde se acuerda con el usuario qué se toca y qué riesgos hay.
  No se escribe una fila hasta ese acuerdo.
- Catálogo de preguntas de rastreo: cuántos caminos llegan, si hay uno programado además del
  sincrónico, si lo que parece camino es en realidad un trigger observando, qué pasa en la
  rama de error y en la de reintento, cuántas versiones del modelo conviven, qué pasa cuando
  el recurso se borra, y si el cambio escala.
- La pregunta que decide el diseño: **si el cambio se equivoca, ¿omite datos o corrompe datos
  que estaban bien?** Omitir se arregla con un reintento; corromper exige salvaguarda.
- CodeGraph antes que grep cuando el repo está indexado: devuelve los caminos de llamada, que
  es justo lo que la fase de trazado necesita, y grep no sigue llamadas.
- El PRD como fuente del *por qué* cuando el FRD calla, y la regla de seguir los documentos
  **aguas arriba** que cite: ahí suele estar la restricción que explica el caso raro.

### Changed
- Los errores comunes pasan a tabla con la columna "por qué duele", cada uno con el caso real
  que lo originó.

## [0.3.0] — 2026-08-25

El formato de la tabla que traía la skill no era el que usan las specs de la casa, y su
ejemplo enseñaba justo lo que no hay que hacer: una fila cuyo cambio era "ninguno de
lógica". Refinando HU-003 eso produjo cuatro filas que no eran cambios y una tabla que
leía como informe con citas.

### Changed
- La celda pasa de tres bloques (`Existente` / `Cambio` / `Por qué`) a dos:
  **`Actualidad:`** y **`Cambios propuestos:`**, con el motivo integrado en la prosa.
- Se elimina el `archivo:línea` obligatorio en la tabla. Se verifica igual durante el
  análisis, pero no se cita: las líneas se desactualizan al primer merge y convierten una
  lista de cambios en un informe.
- El ejemplo pasa a ser un cambio real (un enganche) en vez de un `REUSE` sin acción.

### Added
- Filtro previo al formato: **toda fila es un cambio**. Lo que no implica escribir código
  —correcciones al documento, observaciones, restricciones ya implícitas en otra fila— va
  a `Refinamiento` o se le plantea al usuario. En la tabla infla la estimación.
- Un `REUSE` es fila solo si lleva acción propia.
- Cierre de revisión: de cada fila, *si la borro, ¿queda algo sin hacer?* Si no, sobra.
- Tres errores comunes nuevos, incluido mirar cómo escriben la tabla las specs hermanas
  antes de inventar un formato.

## [0.2.0] — 2026-08-25

Aprendizajes de refinar HU-003: la skill navegaba por los links del cuerpo de los
documentos y solo miraba los comentarios del FRD.

### Added
- Jerarquía canónica de la iniciativa documentada (`PRD → FRD → Propuesta Técnica → Spec
  Técnica por HU`), y navegación por el árbol de Confluence con
  `getConfluencePageDescendants` en vez de por los links del body, que envejecen y a veces
  apuntan a versiones viejas.
- Regla: **todo lo que produce el refinamiento vive dentro de la spec de su HU**. No se
  crean páginas hermanas para actas, diagramas ni notas; una decisión que afecta a varias
  HUs se escribe en cada spec. Las páginas auxiliares que ya existan se leen como
  contexto, pero no se les agrega nada.
- Los comentarios (footer e inline) se leen en **todas** las páginas —FRD, Propuesta, la
  spec destino y las hermanas—, no solo en el FRD. Si un comentario posterior contradice
  el body, gana el comentario y se deja dicho en la fila.
- La Propuesta Técnica pasa a ser lectura obligatoria y ordenada, no un "si está,
  léela". El PRD se lee solo ante ambigüedad del FRD y nunca gana sobre él.

## [0.1.0] — 2026-08-25

Primera versión publicada. La skill se reescribió por completo respecto de su borrador
interno, que estaba planteada como "FRD → crear Spec Técnica + backlog de Jira" cuando
el trabajo real es refinar una spec que ya existe.

### Added
- Reparto de responsabilidades explícito: la arquitectura, los objetivos y las decisiones
  claves son del Líder Técnico; la skill solo escribe **Cambios Técnicos** y
  **Refinamiento → Preguntas**.
- Orden de autoridad para resolver contradicciones: codebase > Acta de refinamiento > FRD.
- Lectura obligatoria del contexto de la iniciativa (Propuesta Técnica, Acta y specs
  hermanas) antes de analizar, para no proponer como nuevo lo que otra HU ya entregó.
- Verificación de cada símbolo que la spec declara `NEW`, resuelto a
  `NEW real` / `YA EXISTE` / `EXISTE PARCIAL` con `archivo:línea`.
- Formato fijo de celda en tres bloques — `Existente:` / `Cambio:` / `Por qué:` — con el
  lector que tiene en mente cada uno.
- Etiquetas de acción `NEW` / `MODIFY` / `WIRE` / `REUSE` / `FIX`.
- Escritura en Confluence con round-trip en HTML, para no destruir paneles y macros.
- Checklist de qué mirar en backend.

### Removed
- Creación de Epic y tickets en Jira: fuera de este flujo.
- Generación de contratos TypeScript, criterios de aceptación y riesgos: son del LT.
- Regla del 50% de ambigüedades bloqueantes y la auditoría genérica de "fugas" del FRD.

### Known gaps
- El checklist de frontend está sin definir. Se completa cuando toque una HU de FE.
