# Backend — referencia para `task`

Correr esta referencia **después** de ubicar la spec, leer el árbol FRD → Propuesta → Spec, y confirmar que la subtarea es `[BACKEND]` (o la mitad backend de una tarea mixta acordada con el usuario).

La escritura de código la hace un worker despachado; esta referencia define qué verificar antes de despachar y qué criterios de aceptación incluir en el brief.

## Orden de lectura

1. Filas de la tabla `### Backend` en Cambios Técnicos — orden = secuencia de construcción.
2. `🔎 Contexto de desarrollo` y `✅ Hallazgos verificados` de la spec.
3. `Tareas Técnicas` y `Criterios de Aceptación` del ticket — para detectar desvíos, no como fuente primaria.
4. Contexto del proyecto — en este orden, lo que exista:
   - `AGENTS.md` / `CLAUDE.md` / reglas del proyecto
   - Mapa de módulos: puntos de entrada (`index`, routers, triggers, crons, colas)
   - Manifiestos y lockfiles (`package.json`, `firebase.json`, etc.)
   - Infra ya cableada (Cloud Functions, Firestore, colas, webhooks)

## Qué verificar por fila

- **Punto de entrada real** — endpoint, trigger, cron o cola; no asumir el primero que aparece en grep.
- **Forma de documentos/colecciones** — campos nuevos son aditivos; nunca repurposear uno existente.
- **Quién más escribe esos campos** — semántica distinta → riesgo de corrupción, no solo de omisión.
- **Idempotencia** — si el camino reintenta, ¿el cambio se dispara en cada intento?
- **Índices y queries** — la query necesaria existe y está indexada por lo que filtra.
- **Ramas de fallo** — qué pasa en error y en reintento; si corrompe datos buenos, parar y reportar.
- **Tests existentes** — qué cubren hoy y qué casos pide la fila de tests de la spec.

## Criterios de aceptación obligatorios

**Cada fila backend** lleva en el brief:

```
tsc -p tsconfig.build.json --noEmit
```

`ts-jest` no aplica `noUnusedLocals` ni el `strict` del tsconfig de producción — una spec puede pasar mientras el build de producción falla (TS6138, TS2322, TS6133/TS6192). Medido: ~25s, ~2.3GB pico.

**Tests:** correr el comando del proyecto, no uno que el implementador elija. En `atom-cloudfunctions`, `npm test` ejecuta **mocha** con ts-node; jest está instalado pero ningún script del proyecto lo corre — un jest verde no es lo que ejecuta CI.

**Realidad mocha hoy:** mocha es el comando del proyecto, pero gran parte de los specs existentes **no corren bajo mocha** — muchos son jest-only, otros fallan por mocks de config ausentes (`FIRE_PROJECT_ID_KEY` en `jest.setup.ts`, sin equivalente mocha). Si el spec de una fila no puede ejecutarse bajo mocha, **levantar la mano** nombrando el criterio alternativo — no reportar un jest verde como hecho.

- **Prohibido** `jest <directorio>` — spawnea un worker por core y agota memoria. Un solo archivo spec está bien.
- Preferir `npm test` con el path del spec concreto cuando aplique bajo mocha.

### Lint y build

- **La lista de archivos la da el diff, no una lista escrita a mano:** `git diff --name-only <base>...HEAD -- '*.ts'`. Si sale vacía, no hay nada que lintear — no se lintea el árbol "por si acaso".
- **Lint de esos archivos, nunca del árbol.** `npx eslint <lista del diff>` — **sin `--fix`**. Los `npm run lint` de ambos repos llevan `--fix` y reescriben todo `src`, que es el comportamiento de formateo que el brief ya prohíbe.
- **Build del proyecto después.** En `atom-cloudfunctions`: `npm run build:prod` (`tsc -p tsconfig.build.json && tsc-alias`) — emite artefactos, a diferencia del typecheck `--noEmit` ya documentado arriba; mantener ambos y decir qué atrapa cada uno. El `--noEmit` atrapa TS6138/TS6133/TS6192 bajo el tsconfig de producción sin compilar; `build:prod` confirma que el emit completo (incluyendo `tsc-alias`) termina limpio. Un build no puede acotarse a archivos cambiados — corre entero y corre al final.
- **`atom`:** la configuración de build no es obvia — existen ocho (`build:dev`, `build:core`, `build:qa`, `build:prod`, …). No elegir una: confirmar cuál con el usuario; una configuración equivocada es mano levantada, no adivinanza.

**"Sobre el diff" significa dos cosas distintas, y confundirlas produce una regla incumplible:** para lint es **alcance** — se lintea exactamente lo que el diff lista. Para build es **atribución** — `tsc` compila el proyecto entero, así que el build corre completo y lo que se acota es a quién se le imputa el error: solo cuenta si no reproduce en el commit base.

Incluir estos comandos en los criterios de aceptación del brief; el coordinador los re-ejecuta al verificar.

## Convenciones de archivos

Interfaces, types, helpers y constants viven en archivos propios con nombre `name.kind.ts` (ej. `user.interface.ts`, `status.constant.ts`). Preferir clases sobre funciones libres.

Scripts de verificación desechables van **sin trackear** en `functions/scripts/`, fuera del `include` del tsconfig — nunca compilan a `lib/` ni viajan en un deploy.

## Regla de ecosistema

**Nunca introducir** dependencia, servicio o modelo de ejecución que el repo no tenga ya cableado. Redis, Kafka, cola nueva, framework distinto → mano levantada, no código.

## Mano levantada típica en backend

- Schema Firestore o DTO publicado que requiere cambio incompatible.
- Campo compartido con otro escritor y semántica distinta.
- Índice compuesto que no existe y la HU lo necesita.
- Timeout, cuota o límite de plataforma que la fila ignora.
- Patrón de persistencia o auth que el módulo vecino usa distinto al propuesto en la spec.
- Spec de fila que no corre bajo mocha — nombrar criterio alternativo verificable.
