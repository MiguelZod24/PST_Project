Feature: Login - Practice Software Testing
  Como usuario registrado
  Quiero iniciar sesión con mi email y contraseña
  Para acceder a la plataforma según mi rol

  # ─────────────────────────────────────
  # HAPPY PATH
  # ─────────────────────────────────────

  Scenario: Login exitoso como customer
    Given el usuario está en la página de login
    When ingresa el email "customer@practicesoftwaretesting.com"
    And ingresa la password "welcome01"
    And hace click en el botón Login
    Then es redirigido al home
    And la sesión queda activa

  Scenario: Login exitoso como admin
    Given el usuario está en la página de login
    When ingresa el email "admin@practicesoftwaretesting.com"
    And ingresa la password "welcome01"
    And hace click en el botón Login
    Then es redirigido al home
    And tiene acceso a las rutas exclusivas de admin

  # ─────────────────────────────────────
  # CASOS NEGATIVOS
  # ─────────────────────────────────────

  Scenario: Login con email inexistente
    Given el usuario está en la página de login
    When ingresa el email "noexiste@test.com"
    And ingresa la password "welcome01"
    And hace click en el botón Login
    Then ve el mensaje "Invalid email or password"
    And permanece en la página de login

  Scenario: Login con password incorrecta
    Given el usuario está en la página de login
    When ingresa el email "customer@practicesoftwaretesting.com"
    And ingresa la password "wrongpassword"
    And hace click en el botón Login
    Then ve el mensaje "Invalid email or password"
    And permanece en la página de login

  # ─────────────────────────────────────
  # CAMPOS VACÍOS
  # ─────────────────────────────────────

  Scenario: Login con email vacío
    Given el usuario está en la página de login
    When deja el campo email vacío
    And ingresa la password "welcome01"
    And hace click en el botón Login
    Then ve una validación requerida en el campo email
    And no se realiza ninguna petición al servidor

  Scenario: Login con password vacía
    Given el usuario está en la página de login
    When ingresa el email "customer@practicesoftwaretesting.com"
    And deja el campo password vacío
    And hace click en el botón Login
    Then ve una validación requerida en el campo password
    And no se realiza ninguna petición al servidor

  Scenario: Login con ambos campos vacíos
    Given el usuario está en la página de login
    When deja ambos campos vacíos
    And hace click en el botón Login
    Then ve validaciones requeridas en ambos campos
    And no se realiza ninguna petición al servidor

  # ─────────────────────────────────────
  # NAVEGACIÓN
  # ─────────────────────────────────────

  Scenario: Navegar a registro desde login
    Given el usuario está en la página de login
    When hace click en "Register your account"
    Then es redirigido a "/auth/register"

  Scenario: Navegar a recuperación de contraseña
    Given el usuario está en la página de login
    When hace click en "Forgot password?"
    Then es redirigido a "/auth/forgot-password"