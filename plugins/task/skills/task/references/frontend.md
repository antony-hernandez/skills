# Frontend — referencia para `task`

Correr esta referencia **después** de ubicar la spec, leer el árbol FRD → Propuesta → Spec, y confirmar que la subtarea es `[FRONTEND]` (o la mitad frontend de una tarea mixta acordada con el usuario).

La escritura de código la hace un worker despachado; esta referencia define qué verificar antes de despachar.

## Figma

1. **Confirmar acceso a Figma primero.** Si el MCP de Figma no está autenticado o no responde, decirlo explícitamente y continuar **degradado** — no ocultar la limitación.
2. Leer el Figma que enlaza la spec o el ticket: pantallas, estados, espaciado, copy, estados vacío/error/carga, comportamiento responsive.
3. **Mapear cada elemento visual** a un componente o token existente antes de proponer algo nuevo.

## Orden de lectura

1. Filas de la tabla `### Frontend` en Cambios Técnicos — orden = secuencia de construcción.
2. `🔎 Contexto de desarrollo` y `✅ Hallazgos verificados` de la spec.
3. `Tareas Técnicas` y `Criterios de Aceptación` del ticket — para detectar desvíos, no como fuente primaria.
4. Repo FE: instrucciones del agente, design system, componentes del módulo, convenciones de estado y routing.

## Qué verificar por fila

- Componente destino existe y su API admite el cambio de forma **aditiva** (nueva prop con default que preserva el comportamiento actual).
- Colores, tipografía y espaciado salen de tokens consumidos — nunca de hex hardcodeado ni de edits a `tailwind.config`, theme o CSS global.
- Estados loading / empty / error están definidos en Figma o en la fila; si faltan, levantar la mano con forma completa.
- Tests FE existentes del módulo: extenderlos, no inventar un runner nuevo.

**Alcance:** el FRD autoriza — archivos extra a la tabla son válidos si satisfacen criterios de producto. Componentes compartidos del design system, tokens publicados o contratos de API que otros consumen **siempre** levantan la mano, aunque la fila no los nombre.

## Mano levantada típica en frontend

- Token de color o spacing que no existe en el design system.
- Componente compartido del design system que requiere cambio de API o de default.
- Pantalla o estado en Figma sin equivalente en componentes existentes.
- Dependencia o patrón de estado que el repo FE no usa.
