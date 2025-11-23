# ScamSinkhole ASI 🛡️

An autonomous swarm of AGI "victims" that floods scam lines to waste criminal resources, extract intelligence, and automate carrier takedowns.

## Overview

ScamSinkhole is an offensive ASI defense system designed to combat phone scammers by:

1. **Swarm**: Spawning hundreds of unique AI personas with dynamic backstories
2. **Attack**: Dialing known scam numbers to keep scammers engaged for maximum duration
3. **Intel**: Analyzing conversations to extract crypto wallets, bank accounts, and other intelligence
4. **Kill**: Auto-reporting extracted intelligence to carriers and authorities

## Architecture

### Technology Stack
- **Backend**: Python 3.8+ with FastAPI
- **AI/AGI**: OpenAI API (GPT-4) for persona generation and conversation
- **Voice**: Telnyx Voice API for outbound calling
- **Frontend**: HTML/CSS/JavaScript with WebSocket for real-time updates

### Components

#### 1. Swarm Module (`app/modules/swarm/`)
Generates and manages AI personas using AGI API:
- Creates diverse persona archetypes (confused grandpa, slow banker, etc.)
- Generates unique backstories and personality traits
- Manages real-time conversation responses

#### 2. Attack Module (`app/modules/attack/`)
Manages outbound calls using Telnyx:
- Initiates calls to scammer phone numbers
- Handles call sessions and state management
- Tracks call duration and transcripts

#### 3. Intel Module (`app/modules/intel/`)
Extracts intelligence from conversations:
- Regex-based extraction of crypto wallets, bank accounts, phone numbers
- AGI-powered analysis for advanced pattern recognition
- Confidence scoring for extracted data

#### 4. Kill Module (`app/modules/kill/`)
Auto-reports intelligence to authorities:
- Submits reports to telecom carriers
- Files complaints with law enforcement (IC3, FTC)
- Tracks report submission status

#### 5. API Layer (`app/api/`)
FastAPI REST endpoints and WebSocket for:
- Persona management
- Call orchestration
- Intelligence retrieval
- Real-time status updates

#### 6. UI Layer (`app/ui/`)
Live War Room dashboard:
- Real-time statistics
- Live activity feed
- Interactive map visualization
- Call monitoring

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Setup

1. Clone the repository:
```bash
git clone https://github.com/wildhash/scam-sinkhole-asi.git
cd scam-sinkhole-asi
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment variables:
```bash
cp .env.example .env
```

Edit `.env` and add your API keys:
```
AGI_API_KEY=your_openai_api_key
TELNYX_API_KEY=your_telnyx_api_key
TELNYX_PHONE_NUMBER=+1234567890
```

## Usage

### Starting the Server

Run the application:
```bash
python main.py
```

The server will start at `http://localhost:8000`

### Web Interface

Open your browser and navigate to:
```
http://localhost:8000
```

You'll see the Live War Room dashboard with:
- Real-time statistics
- Agent status
- Active calls
- Intelligence extracted
- Reports filed

### API Endpoints

#### Swarm Management
- `POST /api/swarm/generate-persona` - Generate a single persona
- `POST /api/swarm/spawn` - Spawn multiple personas (default: 100)
- `GET /api/swarm/personas` - List all personas
- `GET /api/swarm/personas/{id}` - Get specific persona

#### Attack Operations
- `POST /api/attack/initiate-call` - Start a call to a scammer
- `POST /api/attack/dial-list` - Dial multiple numbers
- `GET /api/attack/sessions` - List all call sessions
- `GET /api/attack/sessions/active` - List active calls
- `POST /api/attack/sessions/{id}/end` - End a call

#### Intelligence
- `POST /api/intel/analyze` - Analyze a call transcript
- `GET /api/intel/intelligence` - List all intelligence
- `GET /api/intel/intelligence/high-value` - High-confidence intel only

#### Reporting
- `POST /api/kill/report` - Submit report to authorities
- `GET /api/kill/reports` - List all reports

#### Statistics
- `GET /api/stats` - Overall system statistics

### Example Workflow

1. **Spawn the Swarm**:
```bash
curl -X POST http://localhost:8000/api/swarm/spawn \
  -H "Content-Type: application/json" \
  -d '{"count": 100}'
```

2. **Dial Scam Numbers**:
```bash
curl -X POST http://localhost:8000/api/attack/dial-list \
  -H "Content-Type: application/json" \
  -d '{"phone_numbers": ["+15551234567", "+15559876543"]}'
```

3. **Extract Intelligence**:
```bash
curl -X POST http://localhost:8000/api/intel/analyze \
  -H "Content-Type: application/json" \
  -d '{"call_session_id": "session-id-here"}'
```

4. **Submit Report**:
```bash
curl -X POST http://localhost:8000/api/kill/report \
  -H "Content-Type: application/json" \
  -d '{"intelligence_id": "intel-id-here", "report_type": "both"}'
```

## Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `AGI_API_KEY` | OpenAI API key for persona generation | Yes |
| `AGI_API_BASE_URL` | OpenAI API base URL | No (default: https://api.openai.com/v1) |
| `TELNYX_API_KEY` | Telnyx API key for voice calls | Yes |
| `TELNYX_PHONE_NUMBER` | Your Telnyx phone number | Yes |
| `APP_HOST` | Server host | No (default: 0.0.0.0) |
| `APP_PORT` | Server port | No (default: 8000) |
| `DEBUG` | Enable debug mode | No (default: false) |
| `REPORT_WEBHOOK_URL` | Webhook URL for reports | No |

## Features

### Persona Archetypes

The system includes 10 diverse persona types:
1. Confused Grandpa
2. Slow Banker
3. Tech-Illiterate Retiree
4. Paranoid Conspiracy Theorist
5. Chatty Lonely Widow
6. Hard-of-Hearing Senior
7. Overly Trusting Immigrant
8. Penny-Pinching Accountant
9. Forgetful Alzheimer's Patient
10. Religious Church Lady

Each persona has:
- Unique name and backstory
- Personality traits
- Speech patterns and mannerisms
- Dynamic conversation abilities

### Intelligence Extraction

The system extracts:
- Cryptocurrency wallet addresses (Bitcoin, Ethereum)
- Bank account numbers
- Phone numbers
- URLs and websites
- Organization names
- Confidence scores

### Real-time Monitoring

The War Room UI provides:
- Live statistics dashboard
- Active call monitoring
- Activity feed with timestamps
- Interactive attack map
- WebSocket-based updates

## Security Considerations

⚠️ **Important**: This system is for educational and defensive purposes only.

- Keep your API keys secure
- Use `.env` files and never commit them
- Respect local laws regarding call recording
- Only target confirmed scam numbers
- Implement proper rate limiting in production

## Development

### Project Structure
```
scam-sinkhole-asi/
├── app/
│   ├── core/
│   │   ├── config.py      # Configuration management
│   │   └── models.py      # Data models
│   ├── modules/
│   │   ├── swarm/         # Persona generation
│   │   ├── attack/        # Call management
│   │   ├── intel/         # Intelligence extraction
│   │   └── kill/          # Reporting system
│   ├── api/
│   │   └── main.py        # FastAPI application
│   └── ui/
│       └── index.html     # War Room interface
├── main.py                # Application entry point
├── requirements.txt       # Python dependencies
├── .env.example          # Environment template
└── README.md             # Documentation
```

### Testing

Run the development server with auto-reload:
```bash
python main.py
```

The server will restart automatically when you make code changes.

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is for educational and defensive purposes only. Use responsibly and in accordance with local laws.

## Disclaimer

This software is provided as-is for educational purposes. The authors are not responsible for any misuse of this software. Always ensure you comply with local laws and regulations regarding automated calling and recording.

## Support

For issues, questions, or contributions, please open an issue on GitHub.
