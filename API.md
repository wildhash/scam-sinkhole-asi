# ScamSinkhole ASI - API Documentation

## Base URL
```
http://localhost:8000
```

## Interactive Documentation
FastAPI provides interactive API documentation:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Authentication
Currently, the API does not require authentication. In production, implement OAuth2 or API key authentication.

## Endpoints

### System

#### GET /api
Get API information
```bash
curl http://localhost:8000/api
```

#### GET /health
Health check endpoint
```bash
curl http://localhost:8000/health
```

#### GET /api/stats
Get overall system statistics
```bash
curl http://localhost:8000/api/stats
```

Response:
```json
{
  "personas_count": 100,
  "total_calls": 50,
  "active_calls": 5,
  "completed_calls": 45,
  "total_call_duration_seconds": 12500,
  "intelligence_extracted": 30,
  "reports_submitted": 25,
  "confirmed_reports": 20
}
```

---

### Swarm Module

#### POST /api/swarm/generate-persona
Generate a single AI persona

Request:
```bash
curl -X POST http://localhost:8000/api/swarm/generate-persona \
  -H "Content-Type: application/json" \
  -d '{"archetype": "confused_grandpa"}'
```

Response:
```json
{
  "id": "uuid-here",
  "name": "Herbert Thompson",
  "archetype": "confused_grandpa",
  "backstory": "A 78-year-old retired accountant...",
  "personality_traits": ["forgetful", "talkative", "trusting"],
  "speech_patterns": ["repeats questions", "goes off topic"],
  "created_at": "2024-01-01T12:00:00Z"
}
```

#### POST /api/swarm/spawn
Spawn multiple personas

Request:
```bash
curl -X POST http://localhost:8000/api/swarm/spawn \
  -H "Content-Type: application/json" \
  -d '{"count": 100}'
```

Response:
```json
{
  "personas": [...],
  "count": 100
}
```

#### GET /api/swarm/personas
List all personas

```bash
curl http://localhost:8000/api/swarm/personas
```

#### GET /api/swarm/personas/{persona_id}
Get a specific persona

```bash
curl http://localhost:8000/api/swarm/personas/{persona_id}
```

---

### Attack Module

#### POST /api/attack/initiate-call
Initiate a call to a scammer

Request:
```bash
curl -X POST http://localhost:8000/api/attack/initiate-call \
  -H "Content-Type: application/json" \
  -d '{
    "target_number": "+15551234567",
    "persona_id": "persona-uuid"
  }'
```

Response:
```json
{
  "id": "session-uuid",
  "persona_id": "persona-uuid",
  "target_number": "+15551234567",
  "start_time": "2024-01-01T12:00:00Z",
  "status": "active",
  "transcript": []
}
```

#### POST /api/attack/dial-list
Dial multiple scam numbers

Request:
```bash
curl -X POST http://localhost:8000/api/attack/dial-list \
  -H "Content-Type: application/json" \
  -d '{
    "phone_numbers": ["+15551234567", "+15559876543"]
  }'
```

#### GET /api/attack/sessions
Get all call sessions

```bash
curl http://localhost:8000/api/attack/sessions
```

#### GET /api/attack/sessions/active
Get only active call sessions

```bash
curl http://localhost:8000/api/attack/sessions/active
```

#### GET /api/attack/sessions/{session_id}
Get a specific call session

```bash
curl http://localhost:8000/api/attack/sessions/{session_id}
```

#### POST /api/attack/sessions/{session_id}/end
Manually end a call session

```bash
curl -X POST http://localhost:8000/api/attack/sessions/{session_id}/end
```

---

### Intel Module

#### POST /api/intel/analyze
Analyze a call transcript for intelligence

Request:
```bash
curl -X POST http://localhost:8000/api/intel/analyze \
  -H "Content-Type: application/json" \
  -d '{"call_session_id": "session-uuid"}'
```

Response:
```json
{
  "id": "intel-uuid",
  "call_session_id": "session-uuid",
  "extracted_at": "2024-01-01T12:00:00Z",
  "crypto_wallets": ["1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa"],
  "bank_accounts": ["123456789"],
  "phone_numbers": ["+15559998888"],
  "urls": ["http://scamsite.com"],
  "organization_names": ["Fake Corp"],
  "confidence_score": 0.85
}
```

#### GET /api/intel/intelligence
Get all intelligence data

```bash
curl http://localhost:8000/api/intel/intelligence
```

#### GET /api/intel/intelligence/high-value
Get high-confidence intelligence only

```bash
curl "http://localhost:8000/api/intel/intelligence/high-value?min_confidence=0.7"
```

#### GET /api/intel/intelligence/{intelligence_id}
Get specific intelligence data

```bash
curl http://localhost:8000/api/intel/intelligence/{intelligence_id}
```

---

### Kill Module

#### POST /api/kill/report
Submit intelligence report to carriers/authorities

Request:
```bash
curl -X POST http://localhost:8000/api/kill/report \
  -H "Content-Type: application/json" \
  -d '{
    "intelligence_id": "intel-uuid",
    "report_type": "both"
  }'
```

Report types:
- `"carrier"` - Submit to telecom carriers only
- `"authority"` - Submit to law enforcement only
- `"both"` - Submit to both (default)

Response:
```json
{
  "id": "report-uuid",
  "intelligence_id": "intel-uuid",
  "report_type": "both",
  "submitted_at": "2024-01-01T12:00:00Z",
  "status": "confirmed",
  "response": {
    "carrier": {
      "status": "submitted",
      "status_code": 200
    },
    "authority": {
      "status": "submitted",
      "status_code": 200
    }
  }
}
```

#### GET /api/kill/reports
Get all reports

```bash
curl http://localhost:8000/api/kill/reports
```

#### GET /api/kill/reports/{report_id}
Get a specific report

```bash
curl http://localhost:8000/api/kill/reports/{report_id}
```

---

### WebSocket

#### WS /ws
Connect to WebSocket for real-time updates

```javascript
const ws = new WebSocket('ws://localhost:8000/ws');

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log('Event:', data.type, data);
};
```

Event types:
- `persona_created` - New persona generated
- `swarm_spawned` - Multiple personas created
- `call_initiated` - Call started
- `batch_calls_initiated` - Multiple calls started
- `call_ended` - Call completed
- `intelligence_extracted` - Intelligence analyzed
- `report_submitted` - Report filed

---

## Error Responses

All endpoints return standard HTTP status codes:

- `200 OK` - Success
- `201 Created` - Resource created
- `400 Bad Request` - Invalid request
- `404 Not Found` - Resource not found
- `500 Internal Server Error` - Server error

Error response format:
```json
{
  "detail": "Error message here"
}
```

---

## Rate Limiting

Currently, there are no rate limits. In production, implement rate limiting to prevent abuse.

---

## Examples

### Complete Workflow

1. **Spawn personas**:
```bash
curl -X POST http://localhost:8000/api/swarm/spawn \
  -H "Content-Type: application/json" \
  -d '{"count": 100}'
```

2. **Dial scam numbers**:
```bash
curl -X POST http://localhost:8000/api/attack/dial-list \
  -H "Content-Type: application/json" \
  -d '{"phone_numbers": ["+15551234567", "+15559876543"]}'
```

3. **Monitor active calls**:
```bash
curl http://localhost:8000/api/attack/sessions/active
```

4. **Extract intelligence**:
```bash
curl -X POST http://localhost:8000/api/intel/analyze \
  -H "Content-Type: application/json" \
  -d '{"call_session_id": "session-uuid"}'
```

5. **Submit report**:
```bash
curl -X POST http://localhost:8000/api/kill/report \
  -H "Content-Type: application/json" \
  -d '{"intelligence_id": "intel-uuid", "report_type": "both"}'
```

6. **Check statistics**:
```bash
curl http://localhost:8000/api/stats
```
