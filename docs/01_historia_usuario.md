# HU-001 — Módulo Login

## Historia de Usuario

**Como** usuario registrado de Practice Software Testing,  
**quiero** poder iniciar sesión con mi email y contraseña,  
**para** acceder a las funcionalidades de la plataforma según mi rol (admin o customer).

---

## Criterios de Aceptación

- **CA-01** — Login exitoso como customer: el usuario ingresa credenciales válidas y es redirigido al home con sesión activa.
- **CA-02** — Login exitoso como admin: el admin ingresa credenciales válidas y accede a las rutas exclusivas de administración.
- **CA-03** — Credenciales inválidas: el sistema muestra `Invalid email or password` sin revelar cuál campo es incorrecto.
- **CA-04** — Campos vacíos: el sistema activa validaciones del lado cliente sin hacer petición al servidor.
- **CA-05** — Navegación desde login: el usuario puede navegar a Registro y Recuperación de contraseña desde la página de login.
- **CA-06** — Seguridad básica: la contraseña viaja cifrada, el campo está enmascarado y no se expone en texto plano.

---

## Notas Técnicas

- SPA Angular — requiere esperas explícitas en los tests
- Selectores estables: `#email`, `#password`
- Separar tests por rol: admin vs customer

---

*Fecha: Abril 2026 | Proyecto: PST_Project*