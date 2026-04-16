# 🌿 TuAlergiahoy — Prueba Técnica Full Stack

Aplicación web full-stack que automatiza el flujo de registro de usuarios alérgicos: captura sus datos, consulta niveles de polen en tiempo real, genera un informe personalizado con IA y lo envía por correo electrónico junto con un PDF médico.

---

## Stack tecnológico

| Capa             | Tecnología                                                   |
| ---------------- | ------------------------------------------------------------ |
| Frontend         | Nuxt 4 + Vue 3 (Composition API) + TypeScript                |
| Backend          | Django 5 + Django REST Framework                             |
| Base de datos    | SQLite (via Django ORM)                                      |
| IA generativa    | Google Gemini Flash (via `google-genai`)                     |
| Calidad del aire | Open-Meteo Air Quality API                                   |
| Google Workspace | Sheets API (Service Account) + Docs API + Drive API (OAuth2) |
| Email            | SMTP (Gmail) con adjunto PDF                                 |

---

## Arquitectura del proyecto

```
tualergiahoy/
├── backend/
│   └── registro/
│       ├── services/
│       │   ├── orchestrator.py       # Coordinador del flujo completo
│       │   ├── ai_service.py         # Integración con Gemini
│       │   ├── docs_service.py       # Generación de PDF desde Google Docs
│       │   ├── sheets_service.py     # Escritura en Google Sheets
│       │   ├── pollen_service.py     # Consulta Open-Meteo
│       │   ├── geocoding_service.py  # Geocodificación de ciudad
│       │   ├── email_service.py      # Envío de email HTML con adjunto
│       │   └── google_auth_service.py
│       ├── interfaces/               # Contratos de cada servicio (ABC)
│       ├── dtos/                     # Objetos de transferencia de datos
│       ├── exceptions.py             # Excepciones básicas
│       ├── models.py
│       ├── serializers.py
│       └── views.py
└── frontend/
    ├── pages/
    │   ├── index.vue                 # Landing page
    │   └── registro.vue             # Formulario multi-paso
    ├── composables/
    │   └── useRegistroForm.ts        # Lógica de formulario centralizada
    ├── services/
    │   └── authApiService.ts         # Cliente SSE
    ├── components/                   # Atomic design (atoms → organisms → templates)
    ├── utils/                        # Funciones auxiliares
    ├── constants/                    # Alérgenos, ciudades, configuración de pasos
    └── types/                        # Tipado estricto con TypeScript
```

---

## Flujo de registro

Cuando un usuario completa el formulario, el backend ejecuta el siguiente flujo de forma automatizada y transmite el progreso al frontend en tiempo real mediante **Server-Sent Events (SSE)**:

```
POST /api/registro/
        │
        ▼
1. Persistir usuario y registro en base de datos
        │
        ▼
2. Geocodificar la ciudad → Open-Meteo Geocoding API
        │
        ▼
3. Obtener niveles de polen actuales → Open-Meteo Air Quality API
        │
        ├──▶ 4. Insertar fila en Google Sheets (non-blocking: si falla, continúa)
        │
        ▼
5. Generar previsión personalizada con Gemini Flash (IA)
        │
        ▼
6. Copiar plantilla Google Docs → rellenar placeholders → exportar a PDF → eliminar copia
        │
        ▼
7. Enviar email HTML de bienvenida con datos de polen + PDF adjunto
```

Si la IA no está disponible, el sistema aplica **graceful degradation**: envía el email de bienvenida igualmente, sin PDF, sin interrumpir el registro.

---

## Decisiones técnicas destacadas

### Backend

**Orquestador con inyección de dependencias**
El flujo completo vive en `RegistroOrchestrator`, que recibe todos los servicios como parámetros con valores por defecto. Cada servicio implementa una interfaz (`IGeocodingService`, `IPollenService`, etc.), lo que permite sustituirlos por mocks en tests sin tocar nada del código de producción.

**SSE con generador Python**
El endpoint de registro devuelve un `StreamingHttpResponse` alimentado por un generador. Cada paso del flujo emite un evento SSE con mensaje y porcentaje de progreso. El frontend lo consume con la Fetch API leyendo el stream directamente, sin librerías adicionales.

**Graceful degradation**
Si Gemini no responde, se captura `AIServiceUnavailableError` y el flujo continúa enviando el email sin PDF. Si Google Sheets falla, se loggea el error con contexto (`registro_id`, `email`) y el resto del flujo no se ve afectado.

**Generación de PDF desde Google Docs**
Se crea una copia de la plantilla en Drive, se reemplazan los `{{PLACEHOLDER}}` con `batchUpdate`, se exporta como PDF via Drive API y se elimina la copia en un bloque `finally` para garantizar limpieza aunque falle la exportación.

**Autenticación Google dual**
`SheetsService` usa Service Account (sin interacción humana, adecuado para escritura en servidor). `DocsService` y `DriveService` usan OAuth2 con token cacheado en `token.pickle`, necesario porque las Service Accounts no tienen acceso a Google Drive personal sin plan de pago. El token se refresca automáticamente.

**Prompt de IA con jerarquía de prioridades y reglas de seguridad**
El prompt enviado a Gemini prioriza alergias severas > moderadas > leves, incluye datos reales de la API meteorológica, la estación actual y la medicación del usuario. Contiene reglas explícitas de seguridad médica: prohibido recomendar fármacos específicos o modificar dosis.

### Frontend

**Composable `useRegistroForm`**
Toda la lógica del formulario multi-paso (estado, validación con Zod, navegación entre pasos, consumo del stream SSE, manejo de errores de servidor) vive en un único composable reutilizable. Las páginas solo consumen lo que necesitan.

**Validación en dos capas**
Zod valida el formulario paso a paso en el cliente antes de enviar. Si el servidor devuelve errores de validación (DRF), se mapean al estado de errores por campo y se muestran inline.

**Middleware de reset**
Un middleware de Nuxt limpia el estado del formulario al salir de la ruta `/registro`, evitando que datos de un registro anterior persistan si el usuario navega hacia atrás.

**Atomic design**
Los componentes siguen una jerarquía atoms → molecules → organisms → templates. Los campos de formulario son configurables mediante `FieldConfig`, lo que permite reutilizar `RegistrationStep` para múltiples pasos simplemente cambiando la configuración.

---

## Cobertura de tests

Tests escritos con `pytest` + `unittest.mock`:

**`test_orchestrator.py`** — prueba el flujo completo del orquestador:

- Flujo completo OK: verifica que el email se envía con PDF
- IA no disponible: verifica degradación correcta (email sin PDF)
- Sheets falla: verifica que el flujo continúa y el email llega igualmente
- Geocoding falla: verifica que el flujo se corta y no se ejecuta ningún paso posterior

**`test_serializer.py`** — prueba validaciones de entrada:

- Ciudad vacía → error
- Ciudad inválida (no en choices) → error
- Alergias mal formadas → error
- Campos obligatorios ausentes → error

**`test_ai_service.py`** — prueba el servicio de IA de forma aislada:

- Respuesta correcta → devuelve texto
- API no disponible → lanza `AIServiceUnavailableError`
- Respuesta vacía (`text=None`) → devuelve `"Sin respuesta"`

---

## Variables de entorno

Crea un `.env` en `backend/` copiando `.env.example`:

```bash
cp .env.example .env
```

| Variable                        | Descripción                                             |
| ------------------------------- | ------------------------------------------------------- |
| `SECRET_KEY`                    | Django secret key                                       |
| `GOOGLE_CREDENTIALS_PATH`       | Ruta al JSON de Service Account (para Sheets)           |
| `GOOGLE_SHEETS_ID`              | ID de la hoja de Google Sheets                          |
| `GOOGLE_DOCS_TEMPLATE_ID`       | ID de la plantilla de Google Docs                       |
| `GOOGLE_DRIVE_FOLDER_ID`        | ID de la carpeta donde se guardan las copias temporales |
| `GOOGLE_OAUTH_CREDENTIALS_PATH` | Ruta al JSON de credenciales OAuth2 (para Docs/Drive)   |
| `GEMINI_API_KEY`                | API key de Google AI Studio                             |
| `EMAIL_HOST`                    | Servidor SMTP (ej. `smtp.gmail.com`)                    |
| `EMAIL_PORT`                    | Puerto SMTP (ej. `587`)                                 |
| `EMAIL_HOST_USER`               | Cuenta de correo                                        |
| `EMAIL_HOST_PASSWORD`           | Contraseña de aplicación de Gmail                       |
| `DEFAULT_FROM_EMAIL`            | Nombre y dirección del remitente                        |

Para el frontend, crea un `.env` en `frontend/`:

```env
NUXT_PUBLIC_API_BASE=http://localhost:8000/api
```

---

## Instalación y arranque

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate       # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env           # Configura las variables
python manage.py migrate
python manage.py runserver
```

> La primera vez que el servidor llame a Google Docs/Drive, abrirá el navegador para el flujo OAuth2. El token resultante se guarda en `token.pickle` para usos posteriores.

### Frontend

```bash
cd frontend
npm install
cp .env.example .env           # Configura NUXT_PUBLIC_API_BASE
npm run dev
```

### Tests

```bash
cd backend
pytest registro/tests/ -v
```

---

## Notas adicionales

- El campo `alergias` se almacena como `JSONField` en la base de datos, lo que permite estructuras flexibles (`nombre` + `severidad`) sin esquema rígido.
- El modelo `Usuario` extiende `AbstractUser` eliminando `username` y usando `email` como identificador único.
- Los registros usan `UUIDField` como primary key para facilitar la integración con sistemas externos (Sheets, Docs) sin exponer IDs secuenciales.
- La arquitectura sigue principios SOLID:
  - Cada servicio tiene una única responsabilidad (SRP)
  - Se depende de interfaces (`IService`) en lugar de implementaciones concretas (DIP)
  - Los servicios son intercambiables y fácilmente testeables mediante inyección de dependencias (IoC)
