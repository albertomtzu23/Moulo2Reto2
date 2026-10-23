# Reto de generación de código con IA — log y changelog

**Proyecto:** `m2-api-base`  
**Fecha de inicio:** 2026-10-22  
**Feature objetivo:** `GET /users/search?email=<email>`  
**Estado:** feature y documentación completadas; tests enfocados de `users` con 100% de cobertura. La validación manual detectó las tres mutaciones no equivalentes probadas. La suite completa reportó 99%, con un fallo preexistente de concurrencia de `reports`.

## Alcance y criterios de aceptación

La tarea del laboratorio descrita en `README.md` establece estos resultados:

- `200` y el usuario cuando el email válido existe.
- `422` cuando el formato del email es inválido.
- `404` cuando no existe un usuario con ese email.
- Pruebas en `tests/test_users.py`, siguiendo el estilo de la suite.

La implementación debe respetar las capas y convenciones de `CLAUDE.md`: la ruta delega en el servicio, el servicio usa el repositorio y los errores siguen el catálogo de `core/errors.py`.

## Registro de iteraciones

| Iteración | Actividad y evidencia | Resultado |
|---|---|---|
| 1 | Inspección de `README.md`, `CLAUDE.md`, `users/routes.py`, `users/service.py`, `users/repository.py`, `users/schemas.py` y `tests/test_users.py`. | Se confirmó que el README propone búsqueda de usuario por email y que el repositorio ya expone `find_by_email`. No se implementó la feature en esta iteración. |
| 2 | Ejecución inicial: `python -m pytest --cov=. --cov-report=term-missing`. | 11 tests pasaron y 1 falló. El fallo fue `tests/test_reports.py::test_ids_unicos_bajo_concurrencia`; cobertura total reportada: 99%. La prueba fallida corresponde a `reports`, no a la feature de búsqueda. |
| 3 | Revisión del estado del workspace. | Se detectaron cambios previos en `reports/service.py`, `tests/test_reports.py` y contenido sin seguimiento en `meterialDemos/`. Se dejaron intactos. |
| 4 | Preparación de esta evidencia y del documento de prompts. | Documentos creados; quedaban pendientes la implementación y su validación. |
| 5 | **Test-first, etapa roja:** se añadieron cuatro pruebas de búsqueda a `tests/test_users.py` antes de cambiar código de producción. | `pytest tests\test_users.py -q`: 7 pasaron y 3 fallaron. Fallaron los casos de usuario existente, usuario inexistente y mayúsculas/minúsculas; los tres recibieron 422 porque `/users/search` aún no existía. La prueba de email inválido pasó con 422. |
| 6 | **Test-first, etapa verde:** se añadió la ruta específica antes de `/{user_id}`, se conectó el servicio a `repository.find_by_email` y se documentó el endpoint en `README.md`. | `pytest tests\test_users.py -q`: 10 pasaron. `ruff check users\routes.py users\service.py`: todos los checks pasaron. No se ejecutó la suite completa en esta etapa. |
| 7 | Se proporcionó el prompt de contexto detallado que aparece abajo, con convenciones, archivos, interfaz del repositorio y criterios de aceptación. | El prompt deja evidencia explícita del contexto preparado para la feature. Se registra después de la implementación y no se atribuye como causa de los cambios ya realizados. |
| 8 | Se añadieron dos edge cases en `tests/test_users.py`: email vacío y parámetro `email` ausente. | `pytest tests\test_users.py --cov=users --cov-report=term-missing -q`: 12 tests pasaron; cobertura del paquete `users`: 100% (68 statements, 0 misses). `ruff check tests\test_users.py`: todos los checks pasaron. |
| 9 | Ejecución de suite completa y cobertura: `pytest --cov=. --cov-report=term-missing`. | 17 tests pasaron y 1 falló en `tests/test_reports.py::test_ids_unicos_bajo_concurrencia` (colisiones de IDs en prueba paralela). Cobertura total: 99% (243 statements, 2 misses: `main.py:18` y `reports/service.py:21`). El fallo está fuera de la feature de búsqueda y no se modificó como parte de esta tarea. |
| 10 | Se añadió una prueba directa del contrato `users_repository.find_by_email` para validar la búsqueda con mayúsculas, porque la validación HTTP normaliza el email antes de llamar al repositorio. | `pytest tests\test_users.py --cov=users --cov-report=term-missing -q`: 13 tests pasaron; cobertura de `users`: 100%. `ruff check tests\test_users.py`: todos los checks pasaron. |
| 11 | Mutation testing manual y aislado en copias temporales del proyecto (sin instalar herramientas ni modificar el código fuente del workspace). | Se probaron 4 mutaciones: eliminación de validación de email, inversión de la rama de no encontrado y eliminación de normalización del email consultado fueron detectadas; quitar `.lower()` a los emails almacenados sobrevivió y se clasificó como equivalente bajo el modelo actual, porque los valores `EmailStr` ya se normalizan al crear los usuarios. Resultado manual: 3/4 mutantes detectados; 3/3 mutantes no equivalentes detectados. No es un score producido por una herramienta de mutation testing. |
| 12 | Reejecución final de `pytest --cov=. --cov-report=term-missing`. | 18 tests pasaron y 1 falló en `tests/test_reports.py::test_ids_unicos_bajo_concurrencia`. Cobertura total: 99% (248 statements, 2 misses: `main.py:18` y `reports/service.py:21`). |
| 13 | Depuración y refactor de `users/service.py`: se revisaron casos de búsqueda, errores 404, validación y orden de rutas; no se reprodujeron fallos en `users`. Se extrajo `_require_user` para compartir el manejo 404 de `get_user` y `search_user`. | `pytest tests\test_users.py --cov=users --cov-report=term-missing -q`: 13 pasaron y cobertura `users`: 100% (66 statements, 0 misses). Ruff pasó en rutas, servicio, repositorio y tests. |
| 14 | Cierre de documentación: README actualizado con uso y respuestas HTTP; docstrings de la ruta y del servicio precisados; prompts ejecutados diferenciados de plantillas; reflexión completada. | Evidencia y resumen de cambios en este log. No se generaron capturas de pantalla; los resultados de comandos están transcritos arriba. |

> La medición inicial se hizo sobre el estado encontrado del workspace. No debe presentarse como una ejecución limpia ni atribuirse el fallo a la búsqueda por email.

## Patrón de generación aplicado: test-first

Se eligió **test-first** porque los criterios de aceptación del endpoint son verificables mediante peticiones HTTP y códigos de respuesta. La secuencia registrada fue:

1. Escribir pruebas para email existente, formato inválido, email inexistente y comparación sin distinguir mayúsculas/minúsculas. Después se añadieron los edge cases de parámetro ausente y email vacío.
2. Ejecutar las pruebas antes de implementar. Los tres casos que requerían encontrar un usuario fallaron con 422 porque `/users/search` se interpretaba como `/{user_id}` y `search` no era un ID entero; el caso de email inválido pasó con 422.
3. Implementar la ruta `GET /users/search` usando `EmailStr`, delegar al servicio y reutilizar `repository.find_by_email`.
4. Volver a ejecutar las pruebas: los diez tests de usuarios pasaron. Ejecutar Ruff sobre `users/routes.py` y `users/service.py`: todos los checks pasaron.

Esta evidencia corresponde a la secuencia realmente realizada. Las pruebas enfocadas cubren 100% del paquete `users`; la suite completa alcanzó 99% de cobertura, aunque una prueba ajena de concurrencia falló. En la validación manual de mutaciones, los tests detectaron las tres mutaciones no equivalentes probadas; una mutación equivalente sobrevivió.

## Evidencia recopilada y pendiente

Los pendientes siguen identificados para no atribuir resultados que no se ejecutaron.

| Evidencia | Enlace, ruta o resultado |
|---|---|
| Salida final de `pytest` | Suite completa anterior al refactor: 18 pasaron, 1 falló en test de concurrencia preexistente de `reports`; tras el refactor, los 13 tests de `users` pasaron |
| Cobertura final | Suite completa antes del refactor: 99%; tras el refactor, `users`: 100% (66 statements, 0 misses). El global completo no se volvió a ejecutar tras el refactor |
| Resultado de Ruff | `ruff check users\routes.py users\service.py users\repository.py tests\test_users.py`: todos los checks pasaron; `ruff check .` pendiente |
| Mutation testing | Manual en copias temporales: 3/4 detectados; el superviviente se clasificó como equivalente. Herramienta automatizada no instalada; no se reporta score oficial. |
| Logs de iteraciones | Resultados y comandos transcritos en el registro de iteraciones de este documento |
| Capturas de pantalla | No se capturaron durante el trabajo; si la plataforma las exige, deberán tomarse desde el editor/terminal y adjuntarse aparte |

## Prompt de contexto registrado

Prompt proporcionado para preparar el contexto de IA sobre la búsqueda por email:

> Lee @CLAUDE.md y @README.md. Para implementar la búsqueda por email, consulta @users/routes.py, @users/service.py, @users/repository.py, @users/schemas.py, @core/errors.py y @tests/test_users.py.
>
> La interfaz del repositorio es find_by_email(email: str) -> User | None. El endpoint GET /users/search?email=<email> debe responder 200 si encuentra el usuario, 422 si el email es inválido y 404 si no existe. La ruta específica /search debe ir antes de /{user_id}. Respeta el flujo ruta → servicio → repositorio y las convenciones de CLAUDE.md.

## Reflexión

- **Qué funcionó:** test-first dio una señal verificable antes de implementar: las tres pruebas de búsqueda fallaron porque la ruta aún no existía. Reutilizar `find_by_email` mantuvo la arquitectura y las 13 pruebas enfocadas alcanzaron 100% de cobertura en `users`.
- **Qué se depuró:** al principio, `GET /users/search` sin una ruta específica producía 422 al coincidir con `/{user_id}`. Se confirmó mediante la respuesta de las pruebas antes de añadir la ruta estática en el orden requerido. Además, la mutación de comparación por email mostró que probar mayúsculas solo por HTTP no aislaba el comportamiento del repositorio; se añadió una prueba directa para `find_by_email`.
- **Refactorización:** `_require_user` centraliza la conversión de `None` al error 404 estándar y se comparte entre la consulta por ID y la búsqueda por email. Las pruebas de usuario existente e inexistente protegieron ambos caminos; después del refactor, las 13 pruebas continuaron pasando.
- **Qué mejoraríamos:** ejecutar la suite completa en un estado estable y resolver por separado la carrera de IDs en `reports`; automatizar mutation testing con una herramienta configurada en el proyecto; guardar capturas de terminal/editor en el momento de cada iteración, además del registro textual.

## Changelog de la entrega

### [0.1.0] — 2026-10-22 — documentación de evidencia

- Se añadió este registro para anotar el proceso, resultados comprobables, reflexión y cambios de la entrega.
- Se añadió `clase5-prompts.md` con prompts propuestos para trabajar la feature por etapas.
- `README.md` ya contiene instrucciones de instalación, ejecución, tests y calidad; se actualizará si cambia el comportamiento documentado.
- Se documentó el prompt de contexto usado para orientar la feature.
- La implementación de `GET /users/search` quedó registrada en la iteración 6. La suite completa y mutation testing siguen pendientes.

### [0.2.0] — 2026-10-22 — búsqueda de usuarios por email

- Se añadió `GET /users/search?email=<email>` con validación de email y búsqueda mediante el servicio y el repositorio existentes.
- Pasaron los 10 tests de `tests/test_users.py` y Ruff en los módulos de usuarios modificados.
- Se registró el patrón test-first con sus resultados observados antes y después de la implementación.

### [0.3.0] — 2026-10-22 — edge cases y cobertura

- Se añadieron pruebas para email vacío y parámetro de búsqueda ausente.
- Las 12 pruebas de usuarios pasaron y cubrieron 100% del paquete `users`.
- La suite completa alcanzó 99% de cobertura (17 pasaron, 1 falló en una prueba de concurrencia de `reports`).

### [0.4.0] — 2026-10-22 — mutation testing

- Se añadió una prueba unitaria directa para proteger la comparación insensible a mayúsculas del repositorio.
- En una comprobación manual sobre copias temporales, las pruebas detectaron 3 de 3 mutaciones no equivalentes; sobrevivió una mutación considerada equivalente por la normalización del tipo `EmailStr`.
- La suite completa final quedó en 18 pasaron y 1 fallo ajeno a la feature, con 99% de cobertura.

### [0.5.0] — 2026-10-22 — depuración y refactor del servicio

- Se verificó que las pruebas del endpoint y sus errores pasan; no se reprodujo un defecto funcional en `users`.
- Se centralizó en `_require_user` el manejo 404 compartido por búsqueda y consulta por ID.
- Los 13 tests de `users` pasaron con 100% de cobertura; Ruff pasó en los archivos de usuarios y pruebas.

### [0.6.0] — 2026-10-22 — documentación y cierre de evidencia

- Se actualizó el README para describir la feature ya implementada e incluir un ejemplo de solicitud y respuestas HTTP.
- Se aclararon los docstrings de la ruta y las funciones de búsqueda/lookup del servicio.
- Se añadieron al documento de prompts ejemplos de prompts ejecutados, separados de las plantillas propuestas.
- Se completó la reflexión y se aclaró que hay logs transcritos, pero no capturas de pantalla.
