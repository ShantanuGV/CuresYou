# API

---

# Introduction

CurseYou exposes its rendering engine through a lightweight backend API.

The API acts as the communication layer between the frontend and the procedural rendering engine.

Its responsibilities include:

* receiving user requests
* validating input
* invoking the rendering pipeline
* returning the generated river typography

The API itself contains very little rendering logic. All computational work is delegated to the backend engine.

---

# System Overview

```text
                Frontend
                    │
         HTTP Request (JSON)
                    │
                    ▼
              Flask Server
                    │
                    ▼
             Pipeline Engine
                    │
                    ▼
         Procedural Rendering
                    │
                    ▼
            Generated PNG
                    │
                    ▼
             HTTP Response
```

---

# Request Flow

Every request follows the same execution sequence.

```text
Client Request

↓

Input Validation

↓

Pipeline Initialization

↓

Metadata Loading

↓

Optimization

↓

Layout

↓

Rendering

↓

PNG Generation

↓

Response
```

---

# Primary Endpoint

The backend exposes a rendering endpoint responsible for generating river typography.

### Request Method

```http
POST
```

---

### Expected Content Type

```text
application/json
```

---

### Request Body

Example

```json
{
    "text": "CURSEYOU"
}
```

The request contains the text that should be converted into a river composition.

---

# Successful Response

When rendering completes successfully, the server returns the generated image.

Depending on the frontend implementation, the image may be returned as:

* PNG
* Binary response
* Base64 encoded image
* File response

The frontend then displays the generated result.

---

# Processing Stages

After receiving a request, the backend performs the following operations.

```text
Receive Request

↓

Validate Input

↓

Load Metadata

↓

Retrieve Candidates

↓

Optimize Sequence

↓

Compute Layout

↓

Generate Bridges

↓

Render Composition

↓

Return Image
```

---

# Input Validation

Before rendering begins, the backend validates the incoming request.

Typical validation includes:

* empty input
* invalid characters
* malformed JSON
* unsupported request format

Only valid requests proceed to the rendering pipeline.

---

# Error Handling

If an error occurs during processing, the server returns an appropriate error response instead of terminating unexpectedly.

Possible situations include:

* invalid request
* missing metadata
* rendering failure
* internal processing error

The backend is designed to fail gracefully whenever possible.

---

# Backend Responsibilities

The API layer performs only orchestration.

Responsibilities include:

* request parsing
* response generation
* pipeline invocation
* exception handling

The following operations are **not** handled by the API itself:

* optimization
* layout computation
* bridge generation
* image blending
* rendering

These are delegated to the engine modules.

---

# Pipeline Invocation

Internally, the request is forwarded to the procedural pipeline.

```text
HTTP Request

↓

server.py

↓

pipeline.py

↓

river_engine

↓

Rendered PNG

↓

HTTP Response
```

The API therefore acts as a thin interface between the client and the rendering engine.

---

# Response Lifecycle

```text
Client

↓

POST Request

↓

Flask Server

↓

River Engine

↓

Generated Image

↓

HTTP Response

↓

Frontend Display
```

---

# Performance Considerations

API latency depends primarily on:

* input length
* number of glyph candidates
* optimization time
* rendering resolution

The API introduces very little overhead compared with the rendering engine.

---

# Security Considerations

The backend performs only rendering operations.

It does not execute arbitrary user code.

The API is intended solely for generating procedural river typography from text input.

---

# Extending the API

Future versions of the backend could expose additional functionality, such as:

* rendering configuration
* output resolution selection
* background selection
* multiple export formats
* batch rendering
* optimization settings

The current architecture allows these features to be added without redesigning the rendering engine.

---

# API Summary

The CurseYou API provides a lightweight interface between the frontend and the procedural rendering engine.

Its primary responsibilities are to:

* receive rendering requests
* validate input
* invoke the backend pipeline
* return generated river typography

All computational work is performed inside the engine modules, keeping the API layer simple, maintainable, and easy to extend.
