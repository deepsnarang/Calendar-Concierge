# Calendar-Concierge
Problem: 
  Most calendar apps just log events for you and save them on the date and time you selected but sometimes with a busy week its hard to keep track of everything you have to do and what you need for all your scheduled tasks and it gets confusing, hard and overwhelming:(
Solution:
 Thats why I built an agent called Calendar Concierge to help with that! Calendar Concierge is an agent that reads the events on your google calendar and generates a daily schedule based on your events and how your feeling at that time. It also has many features like helping you prepare for your event, giving you a debrief of the event and what you need and if your travelling even helps plan activities and a packing list!

 Functions of Calendar Concierge:
  
  Conflict Check — flags overlapping events, tight events and getting to places in 30 minutes, and overloaded days
  
  Full Day Timeline — a schedule of your events in order 
  
  Risk Alerts — potential issues that are adapted to your mood and weather in that place
  
  Prep Briefs for event types like :
        
        Meetings: key points to take about, key questions to ask and more
        
        Workouts: weather at that time for your location, gear reminders, tips and more
        
        Travel: day-by-day itinerary, packing list, destination weather, timezone info and more
        
        Dinners: conversation starters or what to order and more
        
        Medical: questions for the doctor and more
        
        Studying: focus areas and more
        
        Birthdays: gift ideas, messages to send and more


Agent generated with `agents-cli` version `0.6.0`
Built with Google ADK 2.0, Gemini 2.5 Flash, and OAuth-secured Google Calendar access.


## Project Structure

Calendar-Concierge/
├── app/
│   ├── agent.py               # Main agent logic, tools, and instruction prompt
│   ├── fast_api_app.py        # FastAPI Backend server
│   └── app_utils/             # App utilities and helpers
├── tests/                     # Unit, integration, and load tests
├── Dockerfile                 # For deployment
└── pyproject.toml             # Project dependencies
```

> 💡 **Tip:** Use [Gemini CLI](https://github.com/google-gemini/gemini-cli) for AI-assisted development - project context is pre-configured in `GEMINI.md`.

Requirements
Before you begin, ensure you have:

uv: Python package manager - Install
agents-cli: Install with uv tool install google-agents-cli
Google Cloud SDK: For GCP services - Install
Gemini API key: Get one free at aistudio.google.com
Google Cloud project with Calendar API enabled and OAuth 2.0 credentials


## Quick Start

Install `agents-cli` and its skills if not already installed:

```bash
uvx google-agents-cli setup
```

Install required packages:

```bash
agents-cli install
```
Set up your environment variables by creating a .env file:
```
GOOGLE_API_KEY=your_gemini_api_key_here

```

Test the agent with a local web server:

```bash
agents-cli playground
```
##Security 

Make sure you have Google Caldenar OAuth set up (this is for security purposes)

For this:
Google Calendar OAuth Setup

First Go to console.cloud.google.com
Then enable the Google Calendar API
After that create OAuth 2.0 credentials (as the Desktop app type)
Then download it as credentials.json and place in your folder
Finally add your Google email as a test user under OAuth consent screen so that it can work


## Commands

| Command              | Description                                                                                 |
| -------------------- | ------------------------------------------------------------------------------------------- |
| `agents-cli install` | Install dependencies using uv                                                         |
| `agents-cli playground` | Launch local development environment                                                  |
| `agents-cli lint`    | Run code quality checks                                                               |
| `agents-cli eval`    | Evaluate agent behavior (generate, grade, analyze, and more — see `agents-cli eval --help`) |
| `uv run pytest tests/unit tests/integration` | Run unit and integration tests                                                        || [A2A Inspector](https://github.com/a2aproject/a2a-inspector) | Launch A2A Protocol Inspector                                                        |

## 🛠️ Project Management

| Command | What It Does |
|---------|--------------|
| `agents-cli scaffold enhance` | Add CI/CD pipelines and Terraform infrastructure |
| `agents-cli infra cicd` | One-command setup of entire CI/CD pipeline + infrastructure |
| `agents-cli scaffold upgrade` | Auto-upgrade to latest version while preserving customizations |

---

## Development

Edit your agent logic in `app/agent.py` and test with `agents-cli playground` - it auto-reloads on save.

## Deployment

```bash
gcloud config set project <your-project-id>
agents-cli deploy
```

To add CI/CD and Terraform, run `agents-cli scaffold enhance`.
To set up your production infrastructure, run `agents-cli infra cicd`.

## Observability

Built-in telemetry exports to Cloud Trace, BigQuery, and Cloud Logging.

## A2A Inspector

This agent supports the [A2A Protocol](https://a2a-protocol.org/). Use the [A2A Inspector](https://github.com/a2aproject/a2a-inspector) to test interoperability.
See the [A2A Inspector docs](https://github.com/a2aproject/a2a-inspector) for details.
