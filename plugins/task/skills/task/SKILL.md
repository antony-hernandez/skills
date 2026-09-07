---
name: task
description: Usalo cuando una subtarea Jira tipo Development tenga Spec refinada y falte coordinar su implementación — no cuando haya que refinar specs (`spec`), escribir código en esta sesión, ni para subtareas de certificación o revisión.
---

# Task — coordinar una subtarea de desarrollo

La Spec ya está refinada. El trabajo acá es **coordinar una subtarea** — leer, verificar, convertir criterios en comandos y **despachar un worker** vía Orca orchestration.

La unidad es **una subtarea**, no la Historia. Varias `[BACKEND]` / `[FRONTEND]` se coordinan por separado.

## Invocación

```
/task <KEY_SUBTAREA>
```

Si el usuario pasa solo la Historia, pedir cuál subtarea implementar.

## Pre-flight

`atlassianUserInfo()`. Si falla, parar.

**Tipo:** debe ser `Development`. Rechazar `[CERTIFICACION]` y `[REVISION]` — no son implementación.

**Assignee:** si está asignada a otra persona, avisar y **seguir**.

Verificar contra la rama base de la spec, no `develop` por defecto. Con `.codegraph/`, **CodeGraph antes que grep**: `codegraph explore` devuelve fuente y call paths en una llamada. Filtrar por `projectPath` cuando el workspace mezcla repos (`atom-cloudfunctions` indexado; `atom` no).

- **Correr `codegraph status <repo>` y leer ambas líneas.** `✓ Index is up to date` = contenido; `⚠ built by an earlier version` = eje aparte. No juzgar por fecha de archivo — un índice de 9 días midió actual con 27.000 aristas ocultas por la advertencia de versión.
- **`sync` no reemplaza `index`.** ~1s, solo deriva de contenido; la advertencia de versión solo se limpia con rebuild completo.
- **Worktree: índice propio al crearse.** `codegraph init` — 17.8s, 2.26GB pico, 201MB — antes de despachar, nunca durante un worker. **Nunca consultar el índice del checkout principal:** otro árbol, respuesta limpia y equivocada.

El brief debe decir lo mismo al worker.

**Antes de cada pasada de auditoría:** confirmar rama y último commit (`git branch --show-current`, `git log -1 --oneline`). Un worktree Orca puede revertirse a otra rama entre pasadas — greps contra el árbol equivocado reportan archivos inexistentes.

## Fase 1 — Ubicar

1. Leer la subtarea en Jira.
2. **Spec** — en orden: link `Spec:` en la subtarea → Historia padre → **preguntar** si falta.
3. Leer `Repo:`, `Tareas Técnicas` y `Criterios de Aceptación`.

Anotar: key, repo, spec URL, disciplina, rama base.

## Fase 2 — Leer el árbol

**Abrir y leer cada nivel** — nombrarlo no alcanza:

```
PRD → FRD → Propuesta Técnica → Spec Técnica → Subtarea Jira
```

1. **FRD** — producto, HUs, ACs de producto. **El FRD autoriza el alcance** — la tabla de Cambios Técnicos es referencia, no techo.
2. **Propuesta Técnica** — ataque, reparto por capa, orden entre HUs.
3. **Spec** — Cambios Técnicos, contexto y hallazgos verificados.
4. **Subtarea** — `Tareas Técnicas` condensa; la fila con `Actualidad` y pseudocódigo manda sobre el checkbox.

Página "SoT" o "Acta" **no entra** salvo que la Propuesta Técnica la enlace.

**Precedencia:** FRD > Propuesta Técnica > Spec > Jira. Propuesta gana sobre Spec; FRD gana sobre todos — reportar conflictos.

## Fase 3 — Rutear

1. Prefijo `[BACKEND]` / `[FRONTEND]` en el título.
2. Si no hay: `Repo:` y tablas `### Frontend` / `### Backend` de la spec.

Cargar `references/frontend.md` o `references/backend.md`. Si toca ambas capas, **preguntar** por cuál arrancar.

## Fase 4 — Verificar antes de despachar

Por cada fila de `Tareas Técnicas`, en orden de construcción:

```
NEW real        → construir según la fila
YA EXISTE       → REUSE/WIRE o reportar fila obsoleta
EXISTE PARCIAL  → solo el delta
```

Si `Actualidad` está desmentida: **parar y reportar — no despachar**. No adaptar ni improvisar.

**Alcance:** FRD satisfecho permite archivos extra. Levantar la mano en paths compartidos — componentes, design tokens, contratos publicados (DTOs de API, schemas Firestore, eventos publicados) — aunque la fila no los nombre.

## Fase 5 — Criterios ejecutables

Cada `Criterio de Aceptación` del ticket → **comando con output crudo pegado**. Máximo 9. Contable, nunca adjetivos.

**Buscar en el FRD** criterios de aceptación **sin fila correspondiente** en Cambios Técnicos — también se convierten en comandos aquí.

El tope de 9 es por dispatch: si ticket + FRD pasan de 9, **partir dispatch** por grupo de filas — un criterio que se cae del brief es un criterio que nadie verifica.

Sin comando → **levantar la mano**, no despachar. Si choca con *Do not touch*, gana la prohibición.

El coordinador re-ejecuta estos comandos al verificar — no confiar en el reporte del worker.

## Fase 6 — Despachar

**No escribir código en el working tree.** Cada dispatch lleva un brief con cinco partes obligatorias:

| Parte | Contenido |
|---|---|
| **Why** | Por qué existe el trabajo |
| **Qué producir** | Archivos, comportamiento, evidencia esperada |
| **No tocar** | Prohibiciones explícitas — incluir `git reset`, `git checkout`, `git stash`, `git restore` y `git clean`; para leer o comparar otro commit usar `git show`; para trabajar contra otro commit usar `git worktree add --detach <ref>` |
| **Criterios de aceptación** | Comandos con output crudo pegado |
| **Levantar la mano** | Forma de `orca orchestration ask` cuando algo bloquee |

**El writer es `cursor`.** `--agent claude` es el fallo — el modelo caro coordina, lee diffs, corre checks y decide; nunca genera código. Ese es todo el argumento de costo, y un dispatch que nombra `claude` gasta el dinero que el split existe para ahorrar.

Cargar `references/orca.md` — secuencia de dispatch y supervisión.

Esperar: `orca-ide orchestration check --wait --types worker_done,escalation,question --timeout-ms <n> --terminal <coordinator_handle>`.

Re-ejecutar ACs tras `worker_done`. Commits: **uno por feature**, no uno por task, si el usuario pide commits. Nunca stagear el índice `.codegraph/` dentro de un worktree — no está en `.gitignore` y son ~201MB.

### Code review despachado

Gate antes de commit — sesión nueva, no el worktree del código.

1. **Brief sin conclusiones del coordinador** — commit, base, criterios verbatim, subtareas hermanas como datos crudos. Brief con conclusiones del coordinador devuelve conclusiones del coordinador.
2. **Worktree detached** en el commit pusheado — `git worktree add --detach <path> <ref>`.
3. **Filtro de deuda preexistente** — hallazgo rojo solo si no reproduce en commit base. Aplica también a lint y build: cualquier resultado rojo se corre contra el commit base antes de atribuirlo a este cambio — estos repos arrastran fallos preexistentes, y un rojo no es evidencia por sí solo. Usar `git show` y `git worktree add --detach`, nunca `git stash`.

Formato: `path:line [BLOQUEANTE|ALTO|MEDIO|BAJO]` o "revisado sin hallazgos". Coordinador re-verifica cada hallazgo y cada fila — incluidas aquellas donde el veredicto contradice su propio criterio.

## Fase 7 — Cierre

La HU **no está hecha** con tests de fila verdes. Tabla criterios vs evidencia — **solo criterios FRD que cubre esta subtarea**.

| Criterio | Veredicto | Dueño si no cumple |
|---|---|---|

Veredictos: `CUMPLE` / `NO CUMPLE` / `fuera de alcance` / `no verificable en el repo`. Dueño hermano = hand-off, no fallo. Cierre cuando lo que cubre esta subtarea está satisfecho y lo de afuera tiene dueño.

Reportar: filas despachadas, saltadas, desvíos, manos levantadas.

**Worktrees:** al cerrar — nunca durante el trabajo — listar y podar worktrees viejos acumulados de tickets anteriores.

**Jira** solo si el usuario lo pide.

## Checklist de reanudación

Si el coordinador se interrumpió, retomar con:

1. Rama actual y último commit (`git log -1`).
2. Dispatches abiertos (`worker-list` o equivalente).
3. Último `worker_done` recibido.
4. Qué filas ya se despacharon.

## Errores comunes

| Error | Por qué duele |
|---|---|
| `[CERTIFICACION]` / `[REVISION]` | No son desarrollo |
| FRD nombrado pero no abierto | Se pierden ACs de producto |
| Saltar Propuesta Técnica | Se pierde orden entre HUs |
| "SoT" no enlazada por la Propuesta | Autoridad autodeclarada |
| Despachar a `claude` en vez de `cursor` | Gasta el modelo caro en código que el split existe para evitar |
| Código en el working tree del coordinador | Rompe aislamiento Orca |
| `Tareas Técnicas` sobre la tabla | Pierde pseudocódigo y Actualidad |
| Tabla como techo de alcance | El FRD autoriza; la tabla orienta |
| AC del FRD sin fila ignorado | Queda sin verificar al cerrar |
| Adaptar fila obsoleta | Despacha sobre supuestos falsos |
| Criterio sin comando | Nadie puede verificar |
| Confiar en `worker_done` sin re-correr ACs | Evidencia incompleta |
| Auditar sin confirmar rama | Greps contra árbol equivocado |
| Omitir prohibición git en No tocar | Worker puede destruir trabajo |
| Matar worker por timeout de check | Trabajo largo es normal |
| Consultar índice del checkout principal desde un worktree | Otro árbol — respuesta limpia y equivocada |
| Juzgar índice por fecha del archivo | `status` y versión del motor son ejes independientes |

## Cuándo no usar

- Refinar specs → `spec`
- Sin Spec refinada → primero `spec`
- Certificación o review → otro flujo
- Escribir código en esta sesión → otro flujo
