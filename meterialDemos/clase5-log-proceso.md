# Reto de generación de código con IA — log y changelog

**Proyecto:** `m2-api-base`  
**Fecha de inicio:** 2026-10-22  
**Feature objetivo:** `GET /users/search?email=<email>`  
**Estado:** endpoint implementado; las pruebas enfocadas de usuarios y Ruff pasaron. La validación completa de cobertura y mutation testing sigue pendiente.

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

> La medición inicial se hizo sobre el estado encontrado del workspace. No debe presentarse como una ejecución limpia ni atribuirse el fallo a la búsqueda por email.

## Patrón de generación aplicado: test-first

Se eligió **test-first** porque los criterios de aceptación del endpoint son verificables mediante peticiones HTTP y códigos de respuesta. La secuencia registrada fue:

1. Escribir pruebas para email existente, formato inválido, email inexistente y comparación sin distinguir mayúsculas/minúsculas.
2. Ejecutar las pruebas antes de implementar. Los tres casos que requerían encontrar un usuario fallaron con 422 al no existir la ruta; el caso de email inválido pasó.
3. Implementar la ruta `GET /users/search` usando `EmailStr`, delegar al servicio y reutilizar `repository.find_by_email`.
4. Volver a ejecutar las pruebas: los diez tests de usuarios pasaron. Ejecutar Ruff sobre `users/routes.py` y `users/service.py`: todos los checks pasaron.

Esta evidencia corresponde a la secuencia realmente realizada. La cobertura total de la feature, la suite completa y mutation testing todavía deben ejecutarse antes de informar sus resultados.

## Evidencia por completar

Añade evidencia real durante el reto. No marques una actividad como terminada hasta haberla ejecutado.

| Evidencia | Enlace, ruta o resultado |
|---|---|
| Salida final de `pytest` | Pendiente |
| Cobertura final (`pytest --cov=. --cov-report=term-missing`) | Pendiente; registrar porcentaje y módulos |
| Resultado de `ruff check .` | Pendiente |
| Mutation testing: herramienta, comando, mutantes detectados/supervivientes | Pendiente |
| Capturas o logs de iteraciones | Pendiente; guardar rutas aquí |

## Prompt de contexto registrado

Prompt proporcionado para preparar el contexto de IA sobre la búsqueda por email:

> Lee @CLAUDE.md y @README.md. Para implementar la búsqueda por email, consulta @users/routes.py, @users/service.py, @users/repository.py, @users/schemas.py, @core/errors.py y @tests/test_users.py.
>
> La interfaz del repositorio es find_by_email(email: str) -> User | None. El endpoint GET /users/search?email=<email> debe responder 200 si encuentra el usuario, 422 si el email es inválido y 404 si no existe. La ruta específica /search debe ir antes de /{user_id}. Respeta el flujo ruta → servicio → repositorio y las convenciones de CLAUDE.md.

## Reflexión

Completar después de implementar y validar:

- **Qué funcionó:** pendiente.
- **Qué problema de depuración se encontró y cómo se verificó la causa:** pendiente.
- **Qué refactor se hizo y qué pruebas protegieron el comportamiento:** pendiente.
- **Qué mejoraríamos al usar IA en otro reto:** pendiente.

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
