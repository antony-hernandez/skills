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

Verificar contra la rama base de la spec, no `develop` por defecto. Con `.codegraph/`, **CodeGraph antes que grep**: `codegraph explore "<pregunta o símbolos>"` devuelve fuente y call paths en una llamada — lo que Fase 4 necesita; grep no sigue llamadas. No todo repo está indexado: `atom-cloudfunctions` tiene índice propio; `atom` no — filtrar por `projectPath` en el índice del workspace root. Confirmar índice y antigüedad antes de confiar. El brief debe decir lo mismo al worker.

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

**Precedencia:** FRD > Propuesta Técnica > Spec > Jira. Si Propuesta Técnica y Spec discrepan, **gana la Propuesta Técnica** — reportar en ambas direcciones. Si FRD y cualquier nivel inferior discrepan, **gana el FRD**.

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

**Alcance:** si el FRD queda satisfecho, archivos extra a los de la tabla son válidos. Lo que sí exige levantar la mano son **paths que rompen a otros** — componentes compartidos, design tokens, contratos publicados (DTOs de API, schemas Firestore, eventos publicados) — aunque la fila no los nombre.

## Fase 5 — Criterios ejecutables

Cada `Criterio de Aceptación` del ticket → **comando con output crudo pegado**. Máximo 9. Contable, nunca adjetivos.

**Buscar en el FRD** criterios de aceptación **sin fila correspondiente** en Cambios Técnicos — también se convierten en comandos aquí.

El tope de 9 es por dispatch, no por subtarea. Si los criterios del ticket más los del FRD pasan de 9, **partir el dispatch** por grupo de filas en vez de recortar criterios: un criterio que se cae del brief es un criterio que nadie verifica.

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

### Secuencia Orca

1. Resolver CLI: **`orca-ide` en Linux fuera de un terminal Orca** — nunca `orca` a secas (es el lector de pantalla GNOME). Cargar primero: `orca-ide skills get orchestration`.
2. Registrar el repo: `orca-ide repo add --path <repo>` — sin esto el selector de worktree falla con `selector_not_found`.
3. `run-create` → `task-create` → `worker-start --task <id> --worktree <selector> --agent cursor --model <id> --from <coordinator_handle>`.
   El coordinador debería correr **dentro de un terminal Orca**, donde Orca resuelve el emisor solo y `--from` se omite. Desde fuera —una sesión de Claude Code, por ejemplo— no hay identidad de emisor y `worker-start` falla con `no_active_sender_terminal`: pasar el `coordinator_handle` que devolvió `run-create`. El binding del Run no sobrevive la sesión — crear Run nuevo, no rebindear desde fuera.
4. Esperar: `orca-ide orchestration check --wait --types worker_done,escalation,question --timeout-ms <n> --terminal <coordinator_handle>`. `check` toma `--terminal`, no `--from`.
5. **Pipear solo stdout.** `check --json` imprime un JSON en stdout y keepalives en stderr; `2>&1 | parser` falla con `Extra data: line 2`.
6. Responder `question` con `orca-ide orchestration reply --id <msg_id> --body <answer>`, luego `check --ack <delivery_id>` y seguir esperando.
7. Liberar worker terminado: `worker-release --dispatch <id>`.

### Supervisión honesta

- Un timeout de `check --wait` es **checkpoint, no fallo**. Tareas de código corren 15–60 minutos — nunca matar ni reiniciar un worker por silencio.
- Orca pega el brief en el input del agente pero **no siempre lo envía**. Un worker con brief pendiente parece pensando — mismo `terminal: running`, mismo silencio. Leer el tail con `worker-read --dispatch <id>`; si el brief está pendiente, enviarlo con `orca-ide terminal send --terminal <handle> --enter`.
- `worker: failed` con `terminal: running` y `liveness: live` **no prueba fallo**. Orca marca failed por timeout de readiness y vuelve a `succeeded` cuando corre el trabajo. Supervisar bus de mensajes **más** tail del terminal, nunca el bus solo.

Re-ejecutar ACs tras `worker_done`. Commits: **uno por feature**, no uno por task, si el usuario pide commits.

### Code review despachado

Gate antes de commit — sesión nueva, no el worktree donde se escribió el código.

1. **Brief sin conclusiones del coordinador.** Lleva commit y base, criterios del ticket con alcance/fuera de alcance verbatim, criterios FRD y spec verbatim, y reparto de subtareas hermanas como datos crudos. No lleva filas obsoletas ni hallazgos previos. Brief con conclusiones del coordinador devuelve conclusiones del coordinador.
2. **Worktree propio, detached en el commit pusheado** — `git worktree add --detach <path> <ref>`.
3. **Filtro de deuda preexistente.** Todo hallazgo rojo se corre también contra el **commit base**; se reporta solo si **no** reproduce ahí. Un hallazgo cuenta solo cuando no aparece en la base — separa lo introducido por el cambio de deuda heredada.

Devuelve hallazgos con comando y output crudo, más tabla criterio-vs-evidencia. Formato: `path:line [BLOQUEANTE|ALTO|MEDIO|BAJO]` o "revisado sin hallazgos". El coordinador re-verifica cada hallazgo y cada fila — incluidas donde el veredicto contradice su propio criterio.

## Fase 7 — Cierre

La HU **no está hecha** con tests de fila verdes. Cerrar con tabla de criterios vs evidencia — **los criterios FRD que cuentan son los que cubre esta subtarea**, no el FRD entero.

| Criterio | Veredicto | Dueño si no cumple |
|---|---|---|

Veredictos: `CUMPLE` / `NO CUMPLE` / `fuera de alcance` / `no verificable en el repo`. Criterio no cumplido lleva dueño — subtarea hermana o `Confluence, no código`. Dueño hermano = **hand-off, no fallo**. Cierre cuando lo que cubre esta subtarea está satisfecho y lo fuera de alcance tiene dueño.

Reportar: filas despachadas, saltadas, desvíos FRD/spec/ticket, manos levantadas.

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

## Cuándo no usar

- Refinar specs → `spec`
- Sin Spec refinada → primero `spec`
- Certificación o review → otro flujo
- Escribir código en esta sesión → otro flujo
