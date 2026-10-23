# Reto de generación de código con IA — prompts

Estos prompts son una guía reutilizable para el laboratorio. Los que todavía no se hayan enviado a una IA son **propuestos**, no evidencia de ejecución. Registra los prompts realmente usados y sus resultados en `clase5-log-proceso.md`.

## Prompts ejecutados y evidencia

Los siguientes prompts sí se utilizaron en la conversación del reto. Las pruebas
y la implementación ocurrieron antes del prompt de contexto final; no se debe
presentar ese prompt posterior como causa de cambios anteriores.

### Pruebas test-first

```text
Lee @CLAUDE.md, @README.md, @users/routes.py, @users/service.py,
@users/repository.py, @users/schemas.py, @core/errors.py y @tests/test_users.py.

Vamos a implementar GET /users/search?email=<email> usando test-first.
Por ahora, modifica únicamente @tests/test_users.py; no cambies código de
producción ni archivos de reports/.

Criterios: 200 para un email existente, 422 para un email inválido y 404
para un email válido sin coincidencia. Incluye también un caso que compruebe
si la búsqueda conserva la comparación sin distinguir mayúsculas/minúsculas.

Después ejecuta las pruebas de users y reporta el resultado exacto, sin
afirmar que pasan si no se ejecutaron.
```

**Resultado registrado:** se añadieron los casos de búsqueda; la primera
ejecución tuvo 7 tests pasados y 3 fallidos porque la ruta aún no existía.
Ver iteraciones 5 y 6 en `clase5-log-proceso.md`.

### Contexto e interfaces

```text
Lee @CLAUDE.md y @README.md. Para implementar la búsqueda por email,
consulta @users/routes.py, @users/service.py, @users/repository.py,
@users/schemas.py, @core/errors.py y @tests/test_users.py.

La interfaz del repositorio es find_by_email(email: str) -> User | None.
El endpoint GET /users/search?email=<email> debe responder 200 si encuentra
el usuario, 422 si el email es inválido y 404 si no existe. La ruta específica
/search debe ir antes de /{user_id}. Respeta el flujo ruta → servicio →
repositorio y las convenciones de CLAUDE.md.
```

**Resultado registrado:** se guardó como evidencia de contexto después de
implementar el endpoint. Ver iteración 7 de `clase5-log-proceso.md`.

### Implementación incremental

```text
Genera el nuevo endpoint REST, añade la ruta específica antes de
`/users/{user_id}` y conecta el servicio con `find_by_email`.
```

**Resultado registrado:** se implementó `GET /users/search`, el servicio
delegó la consulta en el repositorio y las pruebas enfocadas pasaron. Ver
iteración 6 de `clase5-log-proceso.md`.

### Depuración y refactorización

```text
Debuggea y refactoriza el código generado.
```

**Resultado registrado:** no se reprodujo un fallo funcional en `users`; se
extrajo `_require_user` para compartir el manejo del error 404 y se volvieron
a ejecutar las pruebas de usuarios y Ruff. Ver iteración 13 de
`clase5-log-proceso.md`.

## Contexto del proyecto

Antes de cada etapa, proporciona a la IA las convenciones y archivos pertinentes. En Claude Code, por ejemplo:

```text
Lee @CLAUDE.md y @README.md. Para comprender el patrón del recurso,
consulta @users/routes.py, @users/service.py, @users/repository.py,
@users/schemas.py, @core/errors.py y @tests/test_users.py.
No cambies archivos fuera del alcance indicado.
```

## Prompt 1 — test-first: definir y escribir pruebas

```text
Vamos a implementar la feature GET /users/search?email=<email> en esta API
FastAPI. Trabaja primero en modo test-first: todavía no cambies código de
producción.

Lee @CLAUDE.md, @README.md, @users/routes.py, @users/service.py,
@users/repository.py, @users/schemas.py, @core/errors.py y
@tests/test_users.py.

Criterios de aceptación:
- 200 con el usuario correspondiente si el email válido existe.
- 422 si el formato del email es inválido.
- 404 si el email válido no corresponde a ningún usuario.
- Las pruebas van en @tests/test_users.py y siguen el estilo existente.

Propón casos para éxito, email inválido, usuario inexistente y diferencias de
mayúsculas/minúsculas según el comportamiento del repositorio. Implementa
únicamente las pruebas. No cambies tests ni lógica de reports.
Al terminar, enumera los archivos modificados y ejecuta las pruebas nuevas;
explica cualquier fallo esperado antes de implementar la feature.
```

## Prompt 2 — implementación incremental

```text
Implementa la feature de búsqueda por email según los criterios de
@README.md y las pruebas de @tests/test_users.py. Respeta las convenciones de
@CLAUDE.md y el flujo routes -> service -> repository.

Usa el método existente del repositorio si cubre el caso; no dupliques la
búsqueda. La ruta específica /users/search debe declararse antes de
/users/{user_id}. Mantén la validación del email coherente con los schemas y
usa @core/errors.py para los errores de dominio.

Limita los cambios a users/ y tests/test_users.py. No cambies reports/ ni
archivos con cambios preexistentes. Ejecuta las pruebas enfocadas y reporta
los resultados exactos; no afirmes que pasan si no se ejecutaron.
```

## Prompt 3 — depuración y refactorización segura

```text
Analiza el fallo siguiente usando el test y la salida real, sin asumir una
causa: [pegar aquí el fallo completo].

Contrasta el resultado esperado con el observado, localiza la capa que produce
la diferencia y plantea la corrección mínima. No modifiques código hasta
explicar la evidencia que confirma la causa. Después de corregir, ejecuta el
test que reproducía el fallo y los tests de users relacionados. No alteres
reports/ ni cambios ajenos a esta tarea.
```

## Prompt 4 — documentación y cierre

```text
Revisa la implementación final en @users/ y las pruebas en @tests/test_users.py.
Actualiza la documentación directamente relacionada: docstrings de las
funciones nuevas o modificadas y las instrucciones/endpoints de @README.md.
Registra el cambio con fecha, versión y resumen en el changelog acordado.

Valida con pytest, cobertura y ruff usando los comandos del proyecto. Informa
por separado comandos, resultados y cualquier fallo preexistente o ajeno a
esta feature. No inventes resultados de mutation testing: si no se ejecutó,
déjalo como pendiente.
```

## Prompt 5 — mutation testing (si la herramienta está disponible)

```text
Ayúdame a validar la calidad de las pruebas de la feature de búsqueda por
email mediante mutation testing. Primero inspecciona la configuración y las
herramientas disponibles, sin instalar paquetes ni modificar dependencias.
Propón un comando limitado al código y tests de users, ejecútalo solo si la
herramienta ya está disponible y registra mutantes detectados y supervivientes.
Si no hay herramienta configurada, informa esa limitación y deja el resultado
pendiente; no afirmes un porcentaje de mutación.
```

## Registro de uso

Para cada prompt realmente utilizado, anota en `clase5-log-proceso.md` la etapa,
el prompt o una referencia a esta sección, los archivos tocados y la salida
observada. Adjunta capturas o logs conservando suficiente contexto para
verificar cada afirmación.
