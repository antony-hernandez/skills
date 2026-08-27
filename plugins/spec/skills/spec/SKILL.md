---
name: spec
description: Usalo cuando haya que refinar, definir o revisar los Cambios Técnicos de una Spec Técnica que ya existe en Confluence — también si el usuario solo pega el link de la spec o del FRD, habla de especificación técnica, de una HU con página de Confluence, o pregunta qué habría que tocar en el código para una HU documentada. No aplica a implementar código ni a crear tickets de Jira.
---

# Spec — refinar Cambios Técnicos

La Spec Técnica ya existe y ya tiene dueño: el **Líder Técnico** escribió problema, solución, arquitectura, objetivos, decisiones claves, riesgos y criterios de aceptación. Ese material no se reescribe.

El trabajo es refinar **dos secciones y ninguna más**:

| Sección | Quién la escribe |
|---|---|
| Problema · Solución · Arquitectura · Objetivos · Decisiones · Riesgos · ACs | LT — no tocar |
| **Cambios Técnicos** | **este skill** |
| **Refinamiento → Preguntas** | **este skill** |
| Jira | nadie acá |

Si algo fuera de esas dos secciones está mal, se señala y se le avisa al usuario; no se edita por cuenta propia.

## Por qué el proceso es así

La versión anterior saltaba de "leer los documentos" a "escribir la tabla". El resultado eran filas que sonaban bien y describían lugares equivocados: la spec decía "enganchar en `PublishFlowService`", se escribió la fila, y resultó que publicar un flujo ocurre por **dos caminos** — el publish directo y un job cada minuto que promueve lo que espera aprobación de Meta. El segundo no pasa por ese servicio; tiene su propia copia de los pasos. La fila apuntaba a un observador, no a un camino.

Nada de eso salía leyendo la spec ni buscando el nombre del servicio. Salía preguntando *"¿dónde se publica un flujo, de verdad?"* y siguiendo el hilo. Por eso hay una fase de investigación y una de acuerdo **antes** de redactar.

```
1. Contexto     leer el árbol de documentos
2. Proyecto     cómo es el repo y qué stack admite de verdad
3. Encuadre     qué parte del FRD cubre esta spec — parar y confirmar
4. Lugares      dónde se toca esto, de verdad
5. Flujo        trazar cada lugar de punta a punta
6. Debate       presentar lugares, gaps y riesgos — acordar
7. Escribir     recién acá se redacta la tabla
8. Preguntas    lo que el código no contesta
9. Publicar     Confluence
```

Las fases 5 y 6 son el corazón. No se escribe una sola fila hasta que el usuario y vos estén de acuerdo sobre qué lugares se tocan y qué riesgos hay. Escribir antes de ese acuerdo es lo que produce trabajo que hay que rehacer entero.

La fase 2 evita el otro fallo caro: filas que suenan bien en el FRD pero **no son viables en este ecosistema** (servicio que el repo no tiene, patrón que el equipo no usa, límite de plataforma ignorado).

## Dónde vive todo

```
PRD                          por qué el negocio lo quiere
└── FRD                      qué hace el producto — manda sobre PRD y Figma
    └── Propuesta Técnica    cómo se ataca, e índice de HUs
        ├── Spec Técnica HU-001
        └── Spec Técnica HU-00N
```

**Todo lo que produce el refinamiento vive dentro de la spec de su HU.** No se crean páginas hermanas para actas, diagramas ni notas. Una página hermana con decisiones se desincroniza en la primera semana, y quien implementa lee la spec y se pierde lo acordado. Si la iniciativa ya tiene páginas auxiliares, se leen como contexto (suelen estar más actualizadas) pero no se les agrega nada; se avisa que ese contenido debería bajar a las specs.

## Principio — la spec es hipótesis, no dictado

Una Spec Técnica se escribió en una fecha concreta. Desde entonces las HUs hermanas movieron el código, el Acta cerró decisiones que el body no alcanzó a incorporar, y partes del texto envejecieron. Además mucha documentación se redacta con IA: suena completa sin serlo.

Se lee como hipótesis a validar. Tres cosas la corrigen, en este orden:

1. **El codebase** — gana siempre sobre lo que la spec afirma del sistema actual.
2. **El Acta de refinamiento** — gana sobre el body de la spec cuando se contradicen (suele ser posterior).
3. **El FRD** — fuente de verdad de producto sobre PRD y Figma.

Cuando algo queda desmentido, la fila lo dice explícitamente. Un lector tiene que ver qué cambió respecto de lo escrito y por qué, sin abrir el repo.

## Invocación

```
/spec <URL_SPEC> [<URL_FRD>]
```

`URL_SPEC` es el input principal. `URL_FRD` es opcional; normalmente la spec ya lo enlaza. Si el usuario solo pasa el FRD, preguntar cuál de sus specs hijas refinar: un FRD sin spec destino no es trabajo para este skill.

## Pre-flight

`atlassianUserInfo()`. Si falla, parar: sin el MCP de Atlassian no hay nada que leer ni dónde escribir.

Para el codebase: revisar en **la rama base de la iniciativa**, no en `develop` por defecto. En iniciativas multi-HU, cuando las hermanas están mergeadas en una rama de feature y todavía no en `develop`, leer `develop` hace que media tabla diga "no existe" sobre código ya escrito. Si no está claro cuál es la rama base, preguntarla antes de leer nada.

Si el repo tiene `.codegraph/`, usar CodeGraph **antes que grep**. `codegraph explore "<pregunta o símbolos>"` devuelve el código verbatim más los caminos de llamada entre símbolos — justo lo que la fase 5 necesita — en una sola llamada. `codegraph node <símbolo|archivo>` da un símbolo con sus llamadores. Arrancar a grep teniendo CodeGraph indexado cuesta más y encuentra menos, porque grep no sigue llamadas. Si no hay `.codegraph/`, grep y lectura directa. Lo que nunca vale es proponer una ruta sin haberla abierto.

## Fase 1 — Contexto

### Navegar por el árbol, no por los links

Partiendo de la spec, subir hasta la Propuesta Técnica y enumerar a sus hijas con `getConfluencePageDescendants`. Los links del body envejecen, se copian mal entre specs y a veces apuntan a una versión vieja; el árbol refleja lo que existe hoy. De ahí sale la lista real de HUs, incluidas las que ninguna spec enlaza — suelen ser las que ya movieron el código.

### Orden de lectura

Sin el FRD primero, la spec se lee como tareas sueltas y se pierde para qué existen.

1. **FRD** — problema de producto, HUs, criterios de aceptación.
2. **Propuesta Técnica** — ataque, reparto por capa, orden entre HUs.
3. **Spec a refinar** — estructura exacta, headings, y sobre todo la forma de la tabla de Cambios Técnicos (varía entre specs de la misma iniciativa). Esa forma se respeta.
4. **Specs hermanas** — no es opcional en multi-HU: sin eso se propone como nuevo algo que otra HU ya entregó. De cada una: qué dejó construido para reusar, qué queda fuera porque lo cubre otra, decisiones con el número de esta HU.
5. **Páginas auxiliares** (acta, diagramas) — contexto, no destino de escritura.

El **PRD** se lee cuando el FRD deja algo sin explicar, y nunca gana sobre el FRD. Trae el *por qué* y nombra componentes y documentos que originaron la iniciativa. Si cita un FRD o una spec **aguas arriba**, hay que leerla: ahí suele estar la restricción que explica el caso raro.

### Los comentarios son parte del documento

En **cada** página que se abra — FRD, Propuesta, spec destino y hermanas — pedir `getConfluencePageFooterComments` y `getConfluencePageInlineComments`. Buena parte de las decisiones se cierra en un comentario y nunca baja al body. Si body y comentario discrepan, gana el comentario si es posterior, y se deja dicho en la fila que corresponda.

Anotar el resultado como lista corta: "esto ya existe / esto lo cubre HU-XX / esto se decidió en un comentario".

## Fase 2 — Proyecto y ecosistema

El FRD dice *qué* quiere el producto. Esta fase dice *en qué mundo* se implementa. Sin ella, el skill propone Redis donde solo hay Firestore, un worker largo donde solo hay Cloud Functions con timeout, o un patrón que el equipo ya rechazó en `AGENTS.md`.

Correrla **antes** del encuadre. Si el workspace no es el repo correcto, preguntar cuál es — no inventar stack.

### Entender el proyecto (no solo el FRD)

Leer, en este orden, lo que exista en el/los repos de la HU:

1. **Instrucciones del agente** — `AGENTS.md`, `CLAUDE.md`, `.cursor/rules`, constitución / `specs/*/plan.md`, skills de proyecto. Ahí viven reglas no negociables (reuso, tipado, errores tipados, qué no tocar).
2. **Mapa del código** — módulos que la HU toca, puntos de entrada (`index`, routers, triggers), cómo se parte FE vs BE si aplica.
3. **Convenciones vivas** — helpers/servicios/utils del dominio; si ya hay un patrón para X, la fila lo reusa. No reinventar.
4. **Memoria de iniciativa** — `memory/`, actas locales, runbooks del ticket: a menudo explican por qué un atajo “obvio” ya falló.

El objetivo no es resumir el repo entero. Es poder responder en una frase: *cómo se construye trabajo de este tipo acá*, y detectar cuando la spec pide algo que choca con esas reglas.

### Tecnologías y límites del ecosistema

Antes de proponer cualquier dependencia, servicio o forma de ejecución, verificar que **ya pertenece** al ecosistema del proyecto o que el usuario la pide explícitamente.

Mirar evidencias concretas:

- manifiestos y lockfiles (`package.json`, `firebase.json`, `pubspec`, etc.)
- infra ya cableada (Cloud Functions, Firestore, Typesense, colas, crons, webhooks)
- patrones de persistencia, auth, logging y tests que el módulo ya usa
- límites de plataforma que el código o la doc del repo ya asumen (timeouts, batch size, complejidad de filtros, cuotas, gen 1 vs 2, etc.)

Reglas:

- **No inventar piezas nuevas** (Redis, Kafka, DB distinta, framework nuevo, cola nueva) solo porque “encajarían”. Si la solución las necesita, va como **pregunta bloqueante**, no como fila.
- **Preferir lo que el repo ya hace** para el mismo problema en otro módulo, aunque sea menos elegante que un diseño de libro.
- **Respetar límites duros** descubiertos en código o docs del proyecto. Una fila que ignora un timeout, un índice faltante o un tope de filtro no es refinamiento: es deuda.
- Si FE y BE usan stacks distintos, anotar ambos; no aplicar reglas de uno al otro.

Cerrar esta fase con un bloque corto (para el debate, no para Confluence todavía):

```
## Proyecto y ecosistema

**Repos:** <nombre(s) y rama base>
**Cómo se trabaja acá:** <2–4 reglas no negociables relevantes a esta HU>
**Stack en juego:** <runtime, DB, búsqueda, jobs, FE si aplica>
**Fuera de ecosistema (no proponer sin OK):** <lista corta>
**Límites que condicionan el diseño:** <timeouts, cuotas, índices, etc.>
```

## Fase 3 — Encuadre

Una spec cubre un pedazo del FRD, casi nunca todo. Muchas lo declaran (`Producto: FRD HU-1 / HU-2`). Si no, deducirlo y decirlo en voz alta. Presentar el encuadre y **esperar confirmación** antes de gastar análisis:

```
## Encuadre

**FRD:** <qué problema de producto resuelve, una oración>
**Esta spec cubre:** <qué HUs/criterios habilita — y qué queda para otras>
**Stack:** Backend / Frontend — acotado a lo verificado en fase 2
**Decisiones del Acta que aplican:** <ids, una línea cada una>
**Ya construido por HUs hermanas:** <lista corta>

¿Encaja con lo que esperás de esta spec?
```

Confirmar el encuadre es barato; descubrir a mitad de la tabla que se estaba resolviendo otra HU, no.

## Fase 4 — Lugares

Antes de trazar flujos, ubicar dónde vive el cambio:

**Verificar cada símbolo que la spec llama nuevo.** Helper, endpoint, campo, constante, colección. Resolver a un estado, anotando `archivo:línea` **para vos** (a la tabla no van):

```
NEW real        → no existe nada equivalente; la fila propone construirlo
YA EXISTE       → existe y cumple; baja a REUSE o WIRE, y se corrige la spec
EXISTE PARCIAL  → existe pero le falta algo; la fila describe solo el delta
```

Este paso suele mover la estimación de la HU. Cuando la mueve, decirlo.

**Buscar lo que la spec no menciona.** Quién más escribe o lee el mismo dato. Dos escritores del mismo campo con semánticas distintas — uno incremental, otro absoluto — merece fila propia, no una nota al pie.

**Localizar el punto de enganche real.** La spec suele decir "en el create/update de X". El código puede reaccionar con un trigger, o tener dos caminos donde la spec asume uno.

**Entender el modelo antes de proponer un algoritmo.** Si el cambio recorre un grafo, una máquina de estados o un pipeline, abrir cómo se representa de verdad. Un algoritmo sobre un modelo supuesto se ve razonable y falla en el caso que la HU quería cubrir.

### Qué mirar según el stack

Completa —no reemplaza— la fase 2. Acá se baja al detalle del cambio; allá se cerró qué tecnologías existen.

- **Backend** — punto de entrada real (endpoint, trigger, cola, cron) · forma de documentos y colecciones tocadas · quién más escribe esos campos · transacciones e idempotencia · qué query hace falta y si necesita índice · tolerancia a fallo · qué cubren los tests existentes · límites ya listados en fase 2 (timeout, batch, cuotas).
- **Frontend** — pendiente de definir con el usuario. No inventar el checklist: preguntarle qué mirar. Mientras tanto, no proponer librerías ni patrones de estado que el repo FE no use ya.

## Fase 5 — Flujo

Para cada lugar de la fase 3, trazar de punta a punta. El catálogo de abajo encuentra cosas que una sola búsqueda no encuentra:

- **¿Cuántos caminos llegan hasta acá?** Buscar **todos** los llamadores, no el primero. El caso del publish tenía dos; quedarse con el primero dejó fuera el job.
- **¿Hay un camino programado —cron, pubsub, cola— además del sincrónico?** Si algo puede quedar "pendiente", casi siempre hay un job que lo retoma después.
- **¿Hay un trigger de base de datos observando el mismo cambio?** Un trigger no es un camino: reacciona a que alguien ya escribió. Enganchar ahí suele costar una relectura que el camino real no necesita, y confunde el observador con el lugar donde ocurre la acción.
- **¿Qué pasa en la rama de error? ¿Y en la de reintento?**
- **Si esto reintenta, ¿cada cuánto, y mi cambio se dispararía en cada intento?**
- **¿Quién más escribe este campo, con qué semántica?**
- **¿Cuántas versiones del modelo conviven?** Un recorrido que asume el modelo nuevo devuelve basura sobre datos viejos.
- **¿Cuántas veces se ejecuta esto por evento?** ¿Escala si el recurso está muy reutilizado?
- **¿Qué pasa cuando el recurso se borra, se desactiva o vuelve a borrador?**
- **La consulta que resuelve el destino, ¿devuelve uno o varios, y está indexada por lo que creés?** Un `getByX` que filtra por empresa y canal pero no por el agente que estás publicando puede devolverte el documento de otro.
- **El documento sobre el que voy a escribir, ¿ya existe cuando mi paso corre?** Depende del orden dentro del mismo proceso, no solo de que exista en algún momento.
- **Si mi cambio se equivoca, ¿omite datos o corrompe datos que estaban bien?**

Esa última pregunta merece pausa propia. Un cambio que ante la duda degrada información existente y correcta es distinto de uno que simplemente no hace nada. Omitir se arregla con un reintento o un backfill; corromper exige salvaguarda —validación previa, escritura condicional, feature flag, rollback— no solo un test. Si la respuesta es "corrompe", el riesgo tiene que aparecer en el debate y la salvaguarda en la fila.

## Fase 6 — Debate

Antes de escribir, presentar al usuario:

- los lugares encontrados y el flujo de cada uno
- los gaps: lo que la spec asume y el código desmiente
- los edge cases
- lo que se le puede romper a otro
- las preguntas que el código no puede contestar

Y esperar acuerdo. Sin ese acuerdo, la tabla es una apuesta disfrazada de especificación.

Cerrar el debate con una **tabla de acuerdos**: una línea por decisión, en el lenguaje del negocio, no del código. Sirve para que quien responde vea de un vistazo si algo quedó mal entendido — es más fácil detectar un malentendido en una línea que en tres párrafos.

```
| Plantilla inicial | primera enviable en cada camino; corta ahí |
| Inactiva          | dejó de ser la primera, aunque siga en el flujo |
| Sync              | autoritativo; salvaguarda en tests y logs |
```

Si en el debate se decide que un cambio es **autoritativo** —que su resultado pisa lo que había sin red de contención—, la salvaguarda se muda a los tests y a la observabilidad. Eso deja de ser conversación y tiene que quedar escrito en la fila: qué test es la red, y qué log tiene que ser visible para enterarse antes que el usuario.

## Fase 7 — Escribir las filas

### Formato de la tabla

La tabla tiene **cuatro columnas:** `Qué` · `Archivo` · `Detalle` · `Estado`.

Sin columna de numeración: Confluence numera las filas solo con `data-number-column`, así que una columna `#` a mano duplica lo que la tabla ya hace y hay que renumerarla entera cada vez que se inserta una fila en el medio.
- `Archivo` — ruta relativa al módulo, `**(nuevo)**` al final si el archivo no existe, varios archivos separados con `<br>`. El número de línea va **solo cuando la línea es el punto del cambio**; los rangos envejecen al primer merge y no se ponen por costumbre.
- `Estado` — 🆕 Crear (no existe hoy) · 🔧 Modificar (existe y cambia) · 🗑️ Deprecar (se borra tras portar su lógica) · ✅ Reusar (se consume sin cambios). Cablear una llamada nueva dentro de un método existente es 🔧. No inventar íconos nuevos.
- El orden de las filas es la **secuencia de construcción**: dependencias primero.

Si la HU toca una sola capa, una tabla; si toca frontend y backend, dos tablas (`### Frontend` / `### Backend`) dentro de la misma spec.

**Encabezado obligatorio** de la sección Cambios Técnicos:

```
Sección exclusiva de desarrollo. Verificado en `[rama base de la iniciativa]`.
Rutas relativas a `[ruta base del módulo]`.
Orden = secuencia de construcción (dependencias primero).
Estado: 🆕 Crear · 🔧 Modificar · 🗑️ Deprecar · ✅ Reusar
```

Si la spec usa IDs de refinamiento con ✅, **aclarar qué significan**:

```
Notación: `DEV-Xxx ✅` remite a una decisión cerrada en Refinamiento —
no significa que el cambio ya esté implementado en el código.
```

Sin esa línea, un ✅ dentro de una fila se lee como «ya hecho».

### 🔎 Contexto de desarrollo

Va **antes** de Cambios Técnicos. Es la casa de **todo lo que no es un cambio**: contexto transversal que complementa al LT sin corregirlo ni meterse en sus secciones.

Qué entra:

- Datos confirmados leyendo el código que matizan supuestos del FRD
- Precedentes del repo (patrón + ruta) que el implementador debe conocer
- Restricciones técnicas descubiertas que condicionan los cambios

Distinción: los **✅ Hallazgos verificados** puntuales que cuelgan de una fila van al final de Cambios Técnicos. Esta sección es para el contexto transversal.

### Toda fila es un cambio

La tabla lista **lo que se va a hacer**. Si el renglón no implica escribir código, no es fila: va a `Refinamiento`, a `🔎 Contexto de desarrollo`, o se le plantea al usuario. Lo que suele colarse: "esto ya existe, reusarlo" sin acción; una corrección al documento; una restricción de orden implícita en otra fila; una observación sobre cómo funciona algo hoy.

Un ✅ Reusar solo es fila si lleva **acción propia**: "reusar el pipeline de export, filtrando por owner y `templateId`" es un cambio. "REUSE el helper, no cambia nada" o "esto existe, tenelo en cuenta" no lo es — va a Contexto de desarrollo.

### La celda Detalle: dos bloques

```
**Actualidad:** qué hay hoy en el codebase, en una o dos frases. Si no hay nada, decirlo.

**Cambios propuestos:** la etiqueta de acción y lo que se va a escribir — nombres,
firmas, campos, queries, condiciones — con el motivo integrado en la prosa.
```

**Actualidad** hace revisable la propuesta: sin saber de qué se parte, nadie juzga si el cambio es el correcto. Nombrar módulo, servicio o helper alcanza; **sin `archivo:línea` en la celda**.

**Cambios propuestos** es lo que alguien implementa sin volver a preguntar. Si dice "actualizar la lógica de X", la fila no sirve. El porqué va integrado: "se descartan las campañas terminales porque una campaña cerrada no va a enviar más y la fila queda muerta en el panel".

### Columna Qué

Nombre del cambio y dónde vive. Sin etiqueta: el ícono de `Estado` ya la da de un vistazo y `Cambios propuestos` abre con la palabra exacta.

```
**Detector de plantillas iniciales** — helper nuevo en `flow-builder`
```

La palabra va al principio de `Cambios propuestos`: `NEW` · `EXTEND` · `MODIFY` · `WIRE` · `REUSE`. Son cinco contra cuatro íconos a propósito — `EXTEND`, `MODIFY` y `WIRE` caen todas en 🔧, y la diferencia entre agregar a algo, cambiarle el comportamiento y solo cablear una llamada importa al implementar.

Una fila = un cambio verificable. Si necesita dos `**Cambios propuestos:**`, son dos filas.

### La fila tiene que bastarse sola

Quien va a implementar lee **una fila** y tiene que poder escribir el código sin salir de ahí. Eso manda sobre cualquier consideración de prolijidad, y de ahí salen dos reglas.

**El bloque va dentro de la celda.** Es tentador mandarlo abajo de la tabla: la celda queda limpia y el bloque gana ancho. El precio es que la fila deja de ser el cambio y pasa a ser un puntero al cambio. Solo se saca cuando es material de referencia largo —un archivo entero, un esquema grande— y no el cambio en sí.

Para que entre, van tres cosas juntas: la tabla a **ancho completo**, el reparto explícito de columnas a favor de `Detalle`, y el bloque escrito a **64 columnas**. Sueltas no alcanzan — un bloque en una celda angosta no tiene wrap ni scroll, y el lector ve los primeros veinte caracteres de cada línea. Los comentarios alineados a la derecha son los que estiran; van arriba, en su propio renglón.

**Nada de identificadores que hay que ir a buscar.** Escribir «según ADR-6» o «por B11» obliga a abrir otra página para entender la fila, y esa página envejece por su cuenta. Se escribe **lo que ese identificador dice**: en vez de "la anomalía de B5", *"llegar a un nodo de sub-agente sin plantilla previa es un error de armado: se registra como anomalía y el recorrido sigue"*. Vale nombrar una HU hermana cuando identifica trabajo concreto; no cuando reemplaza una definición.

### Pseudocódigo, no código

El bloque describe **el algoritmo**, no la implementación. Escribirlo con sintaxis del lenguaje —llaves, funciones flecha, literales de objeto, marcadores de diff— hace que se lea como código a medio escribir: el revisor se pone a corregir sintaxis en vez de discutir la lógica, y quien implementa lo copia en lugar de resolverlo en su stack.

La forma que funciona es la de un algoritmo de manual: `Entrada:`, pasos numerados, viñetas para los casos, y los nombres reales de campos y funciones incrustados en la frase.

```
Entrada: actions[] del publish, agentType

1) Indexar las acciones por id, por bloque y por padre
2) Arrancar en la acción inicial
3) Recorrer con cola y set de visitados:
     · plantilla     → registrarla y CORTAR el camino
     · sub-agente    → anomalía, seguir por sus salidas
     · fin de flujo  → cortar
4) Devolver las plantillas dedupadas más las anomalías
```

**Antes de inventar un estilo, mirá si el documento ya tiene uno.** Las specs suelen traer algún bloque de algoritmo escrito por el LT en la sección de solución; copiar esa forma cuesta nada y hace que la sección se lea como parte del mismo documento.

Qué va en el bloque:

- un **algoritmo en pasos** cuando hay recorrido, orden o condiciones de corte
- la **forma de los datos** cuando el cambio es un contrato: qué campos entran y salen
- **dónde y bajo qué condición** entra la llamada, cuando el cambio es cablear algo en una secuencia existente — incluyendo las ramas donde *no* entra, que suelen ser la mitad del cambio

**Los comentarios del código son parte de la spec.** Explicá el porqué de lo no obvio ahí mismo:

```typescript
// getDocRef y NO repository.get(): ese método traga la excepción y
// convertiría una caída de infraestructura en un 403 engañoso.
```

Escribir el pseudocódigo no es adorno: obliga a resolver lo que la prosa deja ambiguo, y es lo que separa una fila que se puede implementar de una que solo se entiende.

### Ejemplo de fila

| Qué | Archivo | Detalle | Estado |
|---|---|---|---|
| **Enganche en publish directo** — `PublishFlowService` | `publish-flow.service.ts` | **Actualidad:** `publish()` corre sus pasos en secuencia y termina en el log de actividad. Nada toca el registry.<br><br>**Cambios propuestos:** **WIRE** un paso nuevo al final, en background y con su propio `try/catch`: detector, resolución de owners y sync por cada uno. Corre sobre las actions ya en memoria, finalizadas por el paso que asigna a las plantillas nuevas su id real de Meta. Un fallo del registry no puede romper el publish. Ver bloque *Enganche en publish directo*. | 🔧 |

### ✅ Hallazgos verificados

Al final de Cambios Técnicos: datos puntuales que costaron encontrar, para que quien tome la HU no repita la exploración. Acá van los hallazgos que cuelgan de una fila; en `🔎 Contexto de desarrollo` va el transversal.

### Cierre de revisión

Dos pasadas sobre la tabla terminada.

**¿Sobra?** De cada fila: *si la borro, ¿queda algo sin hacer?* Si no, sobra.

**¿Está partida de más?** Si al borrar una fila **otra deja de funcionar**, no eran dos cambios: era uno contado dos veces. La unidad es el cambio —lo que alguien va a escribir de una sentada—, no el motivo.

### Tests

Cerrar siempre con una fila de tests que diga qué casos cubrir **y cuáles no**, porque ya los cubre otra HU. Ahí va el riesgo silencioso: qué error de este cambio no rompe nada visible y por eso solo lo atrapa un test.

### Verificar antes de escribir

No escribas una fila sin haber abierto el archivo. Los errores más caros vienen de suponer:

- Que un middleware hace lo que su nombre sugiere
- Que un campo del documento se llama como en la UI
- Que un tipo tiene más valores de los que tiene
- Que algo «ya existe» sin confirmar dónde

### Al terminar

Releé buscando **contradicciones internas**. Cuando una spec se edita por partes, un bloque de código puede quedar describiendo el diseño viejo mientras la prosa ya describe el nuevo — y quien implementa copia el código, no la prosa.

## Fase 8 — Preguntas de refinamiento

Van a `Refinamiento → Preguntas`. Cuando se responden, pasan a `Acordado` con la respuesta.

Antes de escribir una pregunta, intentar contestarla leyendo el código. Se pregunta lo que el código **no puede** contestar: reglas de negocio, decisiones de producto, qué se espera cuando dos fuentes discrepan.

```
**P1 (bloqueante) — <el punto en una frase>.** <Evidencia: qué dice la spec,
qué hace el código.> *Por qué importa:* <qué decisión técnica cambia según la respuesta.>
```

Marcar `bloqueante` solo si sin la respuesta no se puede decidir qué código escribir; el resto va como asunción explícita dentro de la fila.

Presentar las preguntas junto con la tabla (o en el debate de la fase 6 si bloquean el acuerdo).

### Decisiones Claves y Riesgos (señalar al LT si hay que tocarlos)

No se reescriben solos, pero si el refinamiento cerró decisiones o riesgos nuevos, proponerlos aparte:

**Decisiones Claves** — tres columnas obligatorias: `Decisión` · `Razón` · `Trade-off`. Una decisión sin trade-off escrito es una decisión que no se evaluó. Entre 5 y 8; registrar también **lo que se descartó y por qué**.

**Riesgos y Dependencias** — `Tipo` · `Impacto` · `Mitigación`. **Riesgo ≠ pendiente:** un riesgo es algo que puede salir mal en ejecución; una decisión sin tomar va a Refinamiento → Pendientes. Entre 3 y 6.

## Fase 9 — Publicar en Confluence

Solo después de que el usuario apruebe el draft — y aprobar el draft significa **haber visto las filas redactadas**, no haber estado de acuerdo con el plan. Mostrarlas en la conversación antes de escribir la página.

1. Releer la página con `contentFormat: "html"`. Leer y escribir markdown destruye paneles, macros, badges y checkboxes.
2. Reemplazar **Cambios Técnicos**, **🔎 Contexto de desarrollo** (si aplica) y **Refinamiento → Preguntas**. El resto queda intacto.
3. `updateConfluencePage` con el cuerpo **completo** de la página y `contentFormat: "html"`.
4. Si la sección de Cambios Técnicos no existe, preguntar antes de crearla.
5. Reportar el link.

Si un cambio obliga a tocar algo del LT — un AC nuevo, un riesgo, el resumen desalineado — proponerlo aparte y dejar que el usuario decida.

## Errores comunes

| Error | Por qué duele |
|---|---|
| Saltar la fase de proyecto/ecosistema | Filas “correctas” en el FRD e inviables en el repo (servicio inexistente, límite de plataforma) |
| Proponer dependencia o infra nueva sin OK | El equipo no la opera; la HU se hincha o se bloquea en implementación |
| Ignorar `AGENTS.md` / reglas del repo | Se contradice lo que el proyecto ya decidió no hacer |
| Escribir la tabla antes de trazar flujos y acordar | Filas que apuntan al lugar equivocado; hay que rehacer entero |
| Quedarse con el primer lugar que aparece | El publish tenía dos caminos; el segundo se perdió |
| Leer `develop` en vez de la rama base de la iniciativa | Media tabla dice "no existe" sobre código ya escrito en la feature |
| Confundir un observador (trigger) con un camino real | Se engancha donde se reacciona, no donde ocurre la acción |
| Ignorar el camino programado | Si algo puede quedar pendiente, casi siempre hay un job que lo retoma |
| Grep teniendo CodeGraph indexado | Cuesta más y no sigue llamadas |
| Fila ✅ Reusar solo para documentar un patrón | No es trabajo; va a Contexto de desarrollo |
| Mandar el bloque abajo y dejar la fila apuntándolo | La fila deja de ser el cambio y pasa a ser un puntero al cambio |
| Bloque con sintaxis del lenguaje en vez de pasos | Se revisa la sintaxis en vez de la lógica, y se copia en vez de resolverse |
| Bloque en una celda de tabla angosta | Sin wrap ni scroll: se leen los primeros veinte caracteres de cada línea |
| Citar `ADR-6`, `B11` o cualquier id de decisión | Obliga a abrir otra página, que además envejece aparte. Escribí lo que el id dice |
| Partir un mismo cambio en varias filas por sus motivos | El motivo no es la unidad; la estimación se infla |
| Publicar sin mostrar las filas redactadas | Aprobar el plan no es aprobar el texto |
| Citar `archivo:línea` en la tabla por costumbre | Las líneas se desactualizan al primer merge |
| Reescribir arquitectura, objetivos o decisiones | Son del LT |
| Crear página nueva para decisiones o diagramas | Se desincroniza; quien implementa no la lee |
| Escribir Confluence en markdown | Se pierden paneles y macros |
| Crear o mover tickets de Jira | Fuera de este flujo |

## Cuándo no usar

- Ya hay Cambios Técnicos refinados y aprobados, y toca implementar → otro flujo de implementación
- No existe Spec Técnica, solo un FRD → primero hay que crearla; este skill refina, no crea el documento
