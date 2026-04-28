═══════════════════════════════════════
🟢 HAPPY PATH
═══════════════════════════════════════

TC-L01 - Login exitoso como customer
email: customer@practicesoftwaretesting.com / pass: welcome01
Resultado esperado: Redirige al home, sesión activa

TC-L02 - Login exitoso como admin
email: admin@practicesoftwaretesting.com / pass: welcome01
Resultado esperado: Redirige al home, acceso a rutas de admin

═══════════════════════════════════════
🔴 CASOS NEGATIVOS
═══════════════════════════════════════

TC-L03 - Login con email inexistente
email: noexiste@test.com / pass: welcome01
Resultado esperado: Mensaje: Invalid email or password

TC-L04 - Login con password incorrecta
email: customer@practicesoftwaretesting.com / pass: wrongpass
Resultado esperado: Mensaje: Invalid email or password

TC-L05 - Login con email vacío
email: (vacío) / pass: welcome01
Resultado esperado: Validación requerida en campo email

TC-L06 - Login con password vacía
email: customer@practicesoftwaretesting.com / pass: (vacío)
Resultado esperado: Validación requerida en campo password

TC-L07 - Login con ambos campos vacíos
email: (vacío) / pass: (vacío)
Resultado esperado: Validación requerida en ambos campos

═══════════════════════════════════════
🔵 NAVEGACIÓN
═══════════════════════════════════════

TC-L08 - Navegar a registro
Acción: Click en "Register your account"
Resultado esperado: Redirige a /auth/register

TC-L09 - Navegar a recuperación de contraseña
Acción: Click en "Forgot password?"
Resultado esperado: Redirige a /auth/forgot-password

═══════════════════════════════════════
🟡 UI / UX
═══════════════════════════════════════

TC-L10 - Password enmascarada
Resultado esperado: El campo password no muestra el texto en claro

TC-L11 - Mensaje de error desaparece
Resultado esperado: Al ingresar nuevas credenciales el mensaje desaparece

═══════════════════════════════════════
🔴 SEGURIDAD
═══════════════════════════════════════

TC-L12 - Inyección SQL en email
Resultado esperado: No genera error de servidor ni acceso

TC-L13 - Sin límite de intentos
Resultado esperado: Documentado como riesgo conocido (xfail)