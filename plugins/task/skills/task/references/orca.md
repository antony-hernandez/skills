# Orca — referencia para `task`

Correr esta referencia **después** de armar el brief de cinco partes y **antes** de `run-create`.

## Secuencia Orca

1. Resolver CLI: **`orca-ide` en Linux fuera de un terminal Orca** — nunca `orca` a secas (es el lector de pantalla GNOME). Cargar primero: `orca-ide skills get orchestration`.
2. Registrar el repo: `orca-ide repo add --path <repo>` — sin esto el selector de worktree falla con `selector_not_found`.
3. `run-create` → `task-create` → `worker-start --task <id> --worktree <selector> --agent cursor --model <id> --from <coordinator_handle>`.
   El coordinador debería correr **dentro de un terminal Orca**, donde Orca resuelve el emisor solo y `--from` se omite. Desde fuera —una sesión de Claude Code, por ejemplo— no hay identidad de emisor y `worker-start` falla con `no_active_sender_terminal`: pasar el `coordinator_handle` que devolvió `run-create`. El binding del Run no sobrevive la sesión — crear Run nuevo, no rebindear desde fuera.
4. Esperar: `orca-ide orchestration check --wait --types worker_done,escalation,question --timeout-ms <n> --terminal <coordinator_handle>`. `check` toma `--terminal`, no `--from`.
5. **Pipear solo stdout.** `check --json` imprime un JSON en stdout y keepalives en stderr; `2>&1 | parser` falla con `Extra data: line 2`.
6. Responder `question` con `orca-ide orchestration reply --id <msg_id> --body <answer>`, luego `check --ack <delivery_id>` y seguir esperando.
7. Liberar worker terminado: `worker-release --dispatch <id>`.

## Supervisión honesta

- Un timeout de `check --wait` es **checkpoint, no fallo**. Tareas de código corren 15–60 minutos — nunca matar ni reiniciar un worker por silencio.
- Orca pega el brief en el input del agente pero **no siempre lo envía**. Un worker con brief pendiente parece pensando — mismo `terminal: running`, mismo silencio. Leer el tail con `worker-read --dispatch <id>`; si el brief está pendiente, enviarlo con `orca-ide terminal send --terminal <handle> --enter`.
- `worker: failed` con `terminal: running` y `liveness: live` **no prueba fallo**. Orca marca failed por timeout de readiness y vuelve a `succeeded` cuando corre el trabajo. Supervisar bus de mensajes **más** tail del terminal, nunca el bus solo.
