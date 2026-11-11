# Bitácora de uso de IA

Herramientas usadas: **Claude Code** (asistente en VS Code) y GitHub Copilot.

> Completar/ajustar con tus propias palabras antes de entregar: qué entendiste, qué revisaste y qué decidiste tú.

---

## 1. Revisión del proyecto y corrección de la configuración (Punto 1)

**Prompt:** "vamos por parte, ya hice el primer commit" (junto con el PDF de la evaluación).

**Respuesta de la IA:** detectó que `settings.py` tenía cambios sin commit que dejaban la base de datos en SQLite, que `load_dotenv()` ya no se llamaba (por lo que `SECRET_KEY` quedaba en `None`) y que `.env.example` tenía una `SECRET_KEY` real. También detectó que `prestamos/urls.py` tenía un error de sintaxis y que `base.html` estaba vacío.

**Qué acepté / corregí:** acepté volver a MySQL leyendo los datos desde `.env`, dejar un valor de ejemplo en `.env.example` y completar la vista de inicio con `base.html`. Decidí juntar estos arreglos en el commit del Punto 1.

---

## 2. Estructura del código: modelos, admin y fixture (Punto 2)

**Prompt:** "si deja listo para llegar y para yo llegar y hacer el segundo commit".

**Respuesta de la IA:** generó los modelos `Categoria`, `Herramienta` y `Prestamo` con `choices` para los estados, el admin con `list_display`, `list_filter` y `search_fields`, y un fixture JSON con 3 categorías y 15 herramientas (`HER-001` a `HER-015`, dos de ellas "En reparación" para probar el catálogo).

**Qué acepté / corregí:** tenía una versión de los modelos generada con Copilot que no cumplía la pauta (modelo `socio` propio en vez de `User`, sin `codigo` ni `estado`, `CASCADE` en vez de `PROTECT`). La IA lo comparó con la pauta y descarté esa versión. También se reordenaron los commits para que quedara uno por punto.

---

## 3. Diseño de interfaz (Puntos 3 a 5)

**Prompt:** "si sigue, aplicale" / "si" (continuar con los puntos 3, 4 y 5).

**Respuesta de la IA:** usó Bootstrap 5 desde CDN para `base.html`: barra de navegación con enlaces según el rol (socio o encargado), nombre del usuario conectado, botón de cerrar sesión, contador de la solicitud y zona de mensajes. Tablas para los listados, tarjetas para el catálogo y una sola página de confirmación de eliminación reutilizada para herramientas y categorías.

**Qué acepté / corregí:** acepté el diseño. Aprendí que en Django 5 el cierre de sesión debe ser un formulario POST y no un enlace.

---

## 4. Revisión de seguridad (Puntos 5 y 6)

**Prompt:** "sigue con el punto 6".

**Respuesta de la IA:** aplicó y probó estas medidas:
- `get_object_or_404(Prestamo, pk=pk, socio=request.user)`: un socio que cambia el id en la URL recibe 404 y no puede ver ni cancelar préstamos ajenos.
- Las acciones que modifican datos (agregar, quitar, confirmar, cancelar, activar, devolver, eliminar) solo aceptan POST (`@require_POST`) y llevan `{% csrf_token %}`.
- Las vistas de gestión usan `@encargado_required` (`login_required` + `user_passes_test(is_staff)`).
- `confirmar_solicitud` usa `transaction.atomic()` y `select_for_update()` y vuelve a verificar la disponibilidad, para que dos socios no pidan la misma herramienta a la vez.
- `.env` está en `.gitignore`; solo se sube `.env.example`.

**Qué acepté / corregí:** acepté las medidas. Revisé las pruebas: un socio no puede entrar a las vistas del encargado y otro socio recibe 404 al intentar cancelar un préstamo ajeno.

---

## 5. Consultas sobre Linux

**Prompt:** _(completar con tus preguntas reales, por ejemplo cómo activar el entorno virtual o instalar MySQL)_

**Respuesta de la IA:** _(completar)_

**Qué acepté / corregí:** _(completar)_
