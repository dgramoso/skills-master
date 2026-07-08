# skills-master
Repositorio maestro de IA-Skills

## Skills

| Skill | Descripción |
|---|---|
| `advanced-analytics` | Workflow analítico de negocio: EDA, modelado (regresión/clasificación/clustering/scoring), traducción de métricas técnicas a decisiones ejecutivas |
| `analytics-workflow` | Metodología SDD genérica para proyectos analíticos (churn, fraude, segmentación, dashboards) |
| `ask-matt` | Router que sugiere qué skill de este repo usar según la situación |
| `caveman` | Modo de comunicación ultra-comprimido, reduce tokens ~75% eliminando relleno |
| `codebase-design` | Vocabulario compartido para diseñar módulos profundos (deep modules) |
| `diagnose` | Disciplina de diagnóstico para bugs difíciles: construir un loop de feedback antes de tocar código |
| `diagnosing-bugs` | Loop de diagnóstico para bugs difíciles y regresiones de performance |
| `diseno-proyecto` | Spec-Driven Development (SDD) para diseñar proyectos de software desde cero |
| `domain-modeling` | Construye y afina el modelo de dominio de un proyecto (terminología, ADRs) |
| `git-guardrails-claude-code` | Instala un hook PreToolUse que bloquea comandos git peligrosos (push, reset --hard, clean, etc.) |
| `graphify` | Cualquier input (código, docs, papers) → grafo de conocimiento con comunidades y reporte HTML/JSON |
| `grill-me` | Interroga al usuario hasta alinear entendimiento sobre un plan o diseño |
| `grill-with-docs` | Interrogatorio que además genera ADRs y glosario contra la documentación del proyecto |
| `handoff` | Compacta la conversación actual en un documento de traspaso agente-a-agente |
| `implement` | Implementa trabajo a partir de un PRD o set de issues |
| `improve-codebase-architecture` | Escanea el codebase en busca de oportunidades de "deepening" y las presenta en un reporte HTML |
| `lecciones-aprendidas` | Captura lecciones aprendidas al cierre de un proyecto/sprint (qué funcionó, qué no, decisiones clave) |
| `metodologia-credit-scoring` | Metodología SDD + Ponytail para proyectos de credit scoring: WOE/IV, scorecard, PSI, governance |
| `migrate-to-shoehorn` | Migra assertions `as` de TypeScript a `@total-typescript/shoehorn` en tests |
| `pensamiento-critico` | Interrogatorio crítico por primeros principios, inversión, 5 porqués, para problemas difusos o decisiones atascadas |
| `ponytail-gain` | Muestra el impacto medido de ponytail (menos código, menos costo, más velocidad) como scoreboard |
| `premortem` | Premortem sobre cualquier plan/decisión: asume que falló y trabaja hacia atrás para encontrar puntos ciegos |
| `prototype` | Construye un prototipo descartable para explorar un diseño (terminal app o variantes de UI) |
| `resolving-merge-conflicts` | Resuelve conflictos de un merge/rebase de git en curso |
| `scaffold-exercises` | Crea estructuras de directorios de ejercicios para secciones de curso |
| `setup-matt-pocock-skills` | Configura el repo para usar el ecosistema de skills de ingeniería (issue tracker, triage, docs) |
| `setup-pre-commit` | Configura hooks de pre-commit con Husky, lint-staged y Prettier |
| `skill-cleaner` | Audita las skills locales de Claude Code: presupuesto de prompt, duplicados, descripciones largas, candidatas a no usadas |
| `strategic-planning` | Router de triage que deriva a pensamiento-critico / strategic-problem-solving / premortem según el tipo de decisión |
| `strategic-problem-solving` | Resolución estratégica de problemas de negocio y decisiones de alto impacto, con escenarios, scoring AHP y red-team |
| `tdd` | Test-driven development, red-green-refactor |
| `teach` | Enseña al usuario un concepto o skill nuevo dentro del workspace |
| `technical-exploded-view-infographic` | Genera un prompt de imagen para infografías técnicas exploded-view |
| `to-issues` | Convierte un plan/spec/PRD en issues independientes (tracer-bullet slices) |
| `to-prd` | Convierte la conversación actual en un PRD y lo publica en el tracker |
| `triage` | Mueve issues y PRs externos por una máquina de estados de triage |
| `write-a-skill` | Crea una nueva skill de Claude Code con estructura y documentación correctas |
| `zoom-out` | Da contexto más amplio o una perspectiva de más alto nivel sobre una sección de código |

## Skills genéricas de ingeniería (`ecc/`)

Subconjunto curado de [Everything Claude Code](https://github.com/affaan-m/everything-claude-code) — patrones de ingeniería, datos y operaciones que no son específicos de un proyecto.

| Skill | Descripción |
|---|---|
| `agentic-engineering` | Operar como agentic engineer: ejecución eval-first, descomposición, ruteo de modelos por costo |
| `ai-regression-testing` | Testing de regresión para desarrollo asistido por IA — sandbox sin DB, detección de puntos ciegos del modelo |
| `api-connector-builder` | Construye un conector de API nuevo siguiendo el patrón de integración existente en el repo |
| `api-design` | Patrones de diseño REST: naming, status codes, paginación, filtros, versionado, rate limiting |
| `article-writing` | Artículos, guías, posts y newsletters en una voz consistente derivada de ejemplos o guía de marca |
| `backend-patterns` | Patrones de arquitectura backend, diseño de API y optimización de base de datos (Node/Express/Next.js) |
| `clickhouse-io` | Patrones de ClickHouse: queries, optimización, analítica de alto rendimiento |
| `code-tour` | Genera archivos `.tour` de CodeTour — recorridos guiados con anclas a archivo/línea real |
| `coding-standards` | Convenciones de código transversales: naming, legibilidad, inmutabilidad, revisión de calidad |
| `configure-ecc` | Instalador interactivo de Everything Claude Code — selecciona e instala skills/reglas |
| `content-engine` | Sistemas de contenido nativo por plataforma (X, LinkedIn, TikTok, YouTube, newsletters) |
| `cost-aware-llm-pipeline` | Optimización de costo de APIs de LLM: ruteo de modelo por complejidad, budget, caching |
| `cost-tracking` | Rastrea y reporta uso de tokens/costo de Claude Code por proyecto, tool, sesión o fecha |
| `customer-billing-ops` | Operación de billing de clientes: suscripciones, refunds, churn, recuperación de billing portal |
| `dashboard-builder` | Construye dashboards de monitoreo que responden preguntas reales de operación (Grafana, SigNoz) |
| `data-scraper-agent` | Agente de scraping automatizado para cualquier fuente pública, con enriquecimiento LLM y storage |
| `database-migrations` | Buenas prácticas de migraciones de schema, rollback y zero-downtime (Postgres, MySQL, ORMs) |
| `deployment-patterns` | Patrones de deployment, CI/CD, Docker, health checks, rollback y production readiness |
| `docker-patterns` | Patrones de Docker/Compose: desarrollo local, seguridad de contenedores, networking, volúmenes |
| `e2e-testing` | Patrones de testing E2E con Playwright: Page Object Model, CI/CD, manejo de tests flaky |
| `email-ops` | Triage, redacción y verificación de envío de correo con evidencia (ECC) |
| `error-handling` | Patrones de manejo de errores en TypeScript/Python/Go: errores tipados, retries, circuit breakers |
| `eval-harness` | Framework formal de evaluación de sesiones de Claude Code (eval-driven development) |
| `exa-search` | Búsqueda neuronal vía Exa MCP para investigación web, de código y de empresas |
| `finance-billing-ops` | Workflow de revenue, pricing, refunds y billing con evidencia de código (ECC) |
| `frontend-slides` | Presentaciones HTML animadas desde cero o convertidas desde PowerPoint |
| `github-ops` | Operaciones de GitHub vía `gh` CLI: triage de issues, PRs, CI/CD, releases |
| `google-workspace-ops` | Operación unificada sobre Drive, Docs, Sheets y Slides |
| `investor-materials` | Pitch decks, memos de inversores, aplicaciones a aceleradoras, modelos financieros |
| `iterative-retrieval` | Patrón de refinamiento progresivo de recuperación de contexto para subagentes |
| `market-research` | Investigación de mercado, análisis competitivo y due diligence con atribución de fuentes |
| `mcp-server-patterns` | Construcción de servidores MCP con Node/TypeScript SDK: tools, resources, prompts |
| `mle-workflow` | Workflow de ML engineering en producción: contratos de datos, entrenamiento reproducible, monitoreo |
| `mysql-patterns` | Patrones de MySQL/MariaDB: schema, queries, indexing, replicación, connection pooling |
| `postgres-patterns` | Patrones de PostgreSQL: optimización de queries, diseño de schema, indexing, seguridad |
| `prompt-optimizer` | Analiza prompts crudos, identifica gaps y devuelve un prompt optimizado listo para usar |
| `python-patterns` | Idioms pythonicos, PEP 8, type hints y buenas prácticas para apps mantenibles |
| `python-testing` | Estrategias de testing en Python con pytest: TDD, fixtures, mocking, cobertura |
| `regex-vs-llm-structured-text` | Framework de decisión: regex vs LLM para parsear texto estructurado |
| `search-first` | Investigar antes de codear: busca herramientas/librerías/patrones existentes antes de escribir código nuevo |
| `security-review` | Checklist de seguridad al agregar auth, manejar input de usuario, secrets o endpoints de pago |
| `security-scan` | Escanea la configuración de Claude Code (`.claude/`) en busca de vulnerabilidades e inyección |
| `tdd-workflow` | TDD con cobertura 80%+ incluyendo tests unitarios, de integración y E2E |
| `terminal-ops` | Workflow de ejecución de repo con evidencia: comandos corridos, CI debuggeado, fix verificado (ECC) |

## Herramientas

| Directorio | Uso |
|---|---|
| `skill-cleaner/scripts/skill-cleaner.js` | `node skill-cleaner/scripts/skill-cleaner.js --no-logs` — audita presupuesto de prompt y duplicados de skills locales |
