# 🛍️ E-commerce Chat AI API

## Autor
**Viviana Arango Tabares**

---

## Descripción

Este proyecto consiste en el desarrollo de una API REST para un e-commerce de zapatos que integra un asistente virtual inteligente utilizando **Google Gemini AI**.

El sistema permite a los usuarios:
- Consultar productos
- Recibir recomendaciones personalizadas
- Mantener contexto conversacional
- Gestionar historial de chat

---

## Arquitectura

El proyecto está construido siguiendo los principios de **Clean Architecture**, separando responsabilidades en tres capas principales:

- **Domain** → Entidades y reglas de negocio  
- **Application** → Casos de uso y servicios  
- **Infrastructure** → Base de datos, API, IA y frameworks

```bash
  src/
  - domain/
  - application/
  - infrastructure/
  - tests/
```

  
---

## Tecnologías utilizadas

- Python 3.11  
- FastAPI  
- SQLAlchemy  
- SQLite  
- Pydantic  
- Google Gemini AI  
- Docker & Docker Compose  
- Pytest  

---

## Instalación y ejecución

### 1. Clonar repositorio

```bash
git clone https://github.com/ViVi09030/ecommerce-chat-ai.git
cd ecommerce-chat-ai
```

### 2. Activar entorno virtual

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno

```bash
GEMINI_API_KEY=tu_api_key
DATABASE_URL=sqlite:///./data/ecommerce_chat.db
```

---

## Ejecutar aplicación

### Modo local

```bash
python -m uvicorn src.infrastructure.api.main:app --reload
```

### Modo Docker

```bash
docker-compose up --build
```

---

## Documentación de la API

Accede a Swagger:
```bash
http://localhost:8000/docs
```

---

## Endpoints Principales

- **Productos**
  - `GET /products`
  - `GET /products/{id}`
- **Chat**
  - `POST /chat`
  - `GET /chat/history/{session_id}`
  - `DELETE /chat/history/{session_id}`
- **Sistema**
  - `GET /health`

---

## Testing

Ejecutar pruebas:
```bash
pytest
```

El proyecto incluye pruebas para:
- Entidades (Domain)
- Servicios (Application)

---

## Funcionalidades principales

- Gestión de productos
- Validaciones de negocio
- Chat con contexto
- Recomendaciones con IA
- Persistencia de conversaciones
- Arquitectura desacoplada

---

## Troubleshooting (Solución de problemas)

A continuación se listan los errores más comunes al ejecutar el proyecto y cómo solucionarlos.

---

### Error: uvicorn bloqueado (Device Guard)

`uvicorn.exe ha sido bloqueado por la directiva de Device Guard`

**Solución:**

Ejecutar uvicorn como módulo de Python:

```bash
python -m uvicorn src.infrastructure.api.main:app --reload
```

### Error: Docker Desktop no abre

Docker puede fallar al iniciar debido a problemas con WSL o procesos en segundo plano.

**Solución:**

- Reiniciar WSL:

```bash
wsl --shutdown
```

2. Finalizar procesos de Docker:

```bash
taskkill /F /IM "Docker Desktop.exe"
```

### Error: puerto 8000 ocupado

`Address already in use`

**Solución:**
- Cerrar procesos que estén usando el puerto
- O ejecutar en otro puerto:
  
```bash
python -m uvicorn src.infrastructure.api.main:app --reload --port 8001
```

### Error: pytest async

`RuntimeError: asyncio loop error`

**Solución:**
- Instalar soporte async:

```bash
pip install pytest-asyncio
```
---
