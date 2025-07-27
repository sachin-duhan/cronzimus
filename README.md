# Cronzimus 🚀

A lightweight, Kubernetes-native task scheduler and ad-hoc job manager built with Flask and APScheduler.

## Overview

Cronzimus is a microservice designed to manage scheduled tasks and ad-hoc jobs in Kubernetes environments. It provides a simple REST API for health monitoring and uses APScheduler for reliable task execution with support for interval, cron, and date-based triggers.

### Key Features

- **Kubernetes Native**: Designed for cloud-native deployments with Helm chart support
- **Flexible Scheduling**: Support for interval, cron, and date-based job triggers
- **Job Factory Pattern**: Easy job creation and management through factory pattern
- **Database Integration**: Built-in database connection management
- **Health Monitoring**: REST API endpoint for service health checks
- **Production Ready**: Includes supervisord configuration and Docker support

## Table of Contents

- [Installation](#installation)
- [Quick Start](#quick-start)
- [Architecture](#architecture)
- [Configuration](#configuration)
- [API Documentation](#api-documentation)
- [Job Management](#job-management)
- [Deployment](#deployment)
- [Development](#development)
- [Testing](#testing)
- [Contributing](#contributing)

## Installation

### Prerequisites

- Python 3.10+
- Docker (for containerized deployment)
- Kubernetes cluster (for K8s deployment)
- Make (for build automation)
- UV (optional, for faster dependency management)

### Local Development Setup

#### Option 1: Using UV (Recommended - Fast)

```bash
# Install UV if not already installed
$ curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone the repository
$ git clone https://github.com/sachin-duhan/cronzimus.git
$ cd cronzimus

# Create virtual environment with UV
$ uv venv
$ source .venv/bin/activate

# Install dependencies with UV
$ make uv-install

# Or sync from pyproject.toml
$ make uv-sync
```

#### Option 2: Using pip (Traditional)

```bash
# Clone the repository
$ git clone https://github.com/sachin-duhan/cronzimus.git
$ cd cronzimus

# Create and activate virtual environment
$ python3.10 -m venv .venv
$ source .venv/bin/activate

# Install dependencies
$ make install
```

## Quick Start

### Running Locally

```bash
# Start the application
$ make run

# The service will be available at http://localhost:5000
# Health check endpoint: http://localhost:5000/api/health
```

### Running with Docker

```bash
# Build Docker image
$ docker build -f docker/Dockerfile -t cronzimus:latest .

# Run container
$ docker run -p 5000:5000 cronzimus:latest
```

## Architecture

### Project Structure

```
cronzimus/
├── cronzimus/
│   ├── app.py              # Main Flask application
│   ├── config.py           # Application configuration
│   ├── common/
│   │   ├── db.py          # Database connection management
│   │   └── logger.py      # Logging configuration
│   ├── controller/
│   │   └── task.py        # Task implementations
│   ├── jobs/
│   │   ├── __init__.py    # APScheduler configuration
│   │   └── job_factory.py # Job creation factory
│   └── utils/
│       └── env.py         # Environment utilities
├── docker/
│   └── Dockerfile         # Container definition
├── k8s/                   # Kubernetes deployment files
│   ├── Chart.yaml         # Helm chart metadata
│   ├── templates/         # K8s resource templates
│   └── values/           # Environment-specific values
├── tests/                 # Test suite
├── requirements.txt       # Python dependencies
└── Makefile              # Build automation
```

## Configuration

### Environment Variables

```bash
# Database configuration (to be implemented)
DATABASE_URL=postgresql://user:pass@host:port/db

# Logging level
LOG_LEVEL=INFO

# Flask configuration
FLASK_ENV=production
FLASK_DEBUG=false
```

### Job Configuration

Jobs are configured in `cronzimus/jobs/__init__.py`. Example configurations:

```python
# Interval-based job (runs every 5 seconds)
JobFactory.create_job(
    func=task,
    trigger_type="interval",
    trigger_args={"seconds": 5},
    job_id="sample_task",
    args=(self.db,)
)

# Cron-based job (runs every 10 seconds)
JobFactory.create_job(
    func=task,
    trigger_type="cron",
    trigger_args={"second": "0-59/10"},
    job_id="cron_task",
    args=(self.db,)
)

# Date-based job (runs once at specific time)
JobFactory.create_job(
    func=task,
    trigger_type="date",
    trigger_args={"run_date": datetime(2024, 1, 1, 12, 0)},
    job_id="scheduled_task",
    args=(self.db,)
)
```

## API Documentation

### Endpoints

#### Health Check
- **GET** `/api/health`
- **Response**: `{"status": "running"}`
- **Status Code**: 200

### APScheduler API

When `SCHEDULER_API_ENABLED = True`, additional endpoints are available:

- **GET** `/scheduler/jobs` - List all jobs
- **POST** `/scheduler/jobs` - Add a new job
- **DELETE** `/scheduler/jobs/<job_id>` - Remove a job
- **GET** `/scheduler/jobs/<job_id>` - Get job details
- **PUT** `/scheduler/jobs/<job_id>` - Update job

## Job Management

### Creating Custom Jobs

1. Create a new task in `controller/`:
```python
# cronzimus/controller/my_task.py
import logging
from cronzimus.common.db import Database

LOGGER = logging.getLogger(__file__)

def my_custom_task(db: Database):
    LOGGER.info("Executing custom task")
    # Your task logic here
    return True
```

2. Register the job in `jobs/__init__.py`:
```python
from cronzimus.controller.my_task import my_custom_task

# In APSchedulerConfig.JOBS property
jobs.append(
    JobFactory.create_job(
        func=my_custom_task,
        trigger_type="interval",
        trigger_args={"minutes": 30},
        job_id="my_custom_task",
        args=(self.db,)
    )
)
```

### Trigger Types

1. **Interval Trigger**: Runs at fixed intervals
   - `seconds`, `minutes`, `hours`, `days`, `weeks`

2. **Cron Trigger**: Unix cron-style scheduling
   - Supports standard cron expressions

3. **Date Trigger**: Runs once at a specific date/time
   - Single execution at specified datetime

## Deployment

### Kubernetes Deployment

#### Using Helm

```bash
# Deploy to staging
$ helm install cronzimus ./k8s -f k8s/values/yondu-stage.yaml

# Deploy to production
$ helm install cronzimus ./k8s -f k8s/values/yondu-prod.yaml

# Upgrade deployment
$ helm upgrade cronzimus ./k8s -f k8s/values/yondu-prod.yaml
```

#### Manual Deployment

```bash
# Apply Kubernetes manifests
$ kubectl apply -f k8s/templates/
```

### Docker Deployment

```bash
# Build and tag image
$ docker build -f docker/Dockerfile -t cronzimus:v0.1 .

# Push to registry
$ docker push your-registry/cronzimus:v0.1
```

### Supervisord Configuration

For production deployments, use the provided supervisord configuration:

```ini
[program:cronzimus]
command=/path/to/venv/bin/python /path/to/cronzimus/app.py
directory=/path/to/cronzimus
autostart=true
autorestart=true
stderr_logfile=/var/log/cronzimus.err.log
stdout_logfile=/var/log/cronzimus.out.log
```

## Development

### Available Make Commands

#### Standard Commands
```bash
$ make help          # Show all available commands
$ make install       # Install dependencies (auto-detects UV)
$ make run          # Run the application
$ make test         # Run test suite
$ make lint         # Run linters (black, flake8, isort)
$ make format       # Format code
$ make security     # Run security checks (bandit)
$ make clean        # Clean cache files
$ make build        # Build the package
```

#### UV-Specific Commands
```bash
$ make install-uv    # Install UV package manager
$ make uv-install   # Install dependencies using UV
$ make uv-sync      # Sync dependencies from pyproject.toml
$ make uv-venv      # Create virtual environment with UV
```

### Code Style

The project uses:
- **Black** for code formatting
- **isort** for import sorting
- **flake8** for linting
- **bandit** for security analysis

### Adding Dependencies

```bash
# Add to requirements.txt
$ echo "new-package==1.0.0" >> requirements.txt

# Install in virtual environment
$ pip install -r requirements.txt
```

## Testing

### Running Tests

```bash
# Run all tests
$ make test

# Run specific test file
$ pytest tests/controller/test_task.py

# Run with coverage
$ pytest --cov=cronzimus tests/
```

### Writing Tests

Example test structure:
```python
# tests/controller/test_my_task.py
import pytest
from cronzimus.controller.my_task import my_custom_task
from cronzimus.common.db import Database

def test_my_custom_task():
    db = Database()
    result = my_custom_task(db)
    assert result == True
```

## Monitoring and Logging

### Logging

The application uses the `loguru` library for enhanced logging capabilities:

```python
from cronzimus.common.logger import init_logger

# Logs are configured in bootstrap_app()
# Default log level can be set via LOG_LEVEL environment variable
```

### Health Monitoring

Monitor service health:
```bash
# Check service health
$ curl http://localhost:5000/api/health

# Kubernetes liveness probe
livenessProbe:
  httpGet:
    path: /api/health
    port: 5000
```

## Troubleshooting

### Common Issues

1. **Database Connection Failed**
   - Check DATABASE_URL environment variable
   - Verify database is accessible

2. **Jobs Not Running**
   - Check APScheduler logs
   - Verify job configuration in `jobs/__init__.py`

3. **Import Errors**
   - Ensure virtual environment is activated
   - Run `make install` to install dependencies

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines

- Follow PEP 8 style guide
- Add tests for new features
- Update documentation as needed
- Run `make lint` before committing

## Future Enhancements

### Completed
- [x] UV package manager integration for faster dependency management
- [x] Modern Python packaging with pyproject.toml

### Planned
- [ ] Implement dynaconf for configuration management
- [ ] Add more job trigger types (complex cron patterns, calendar-based)
- [ ] Implement job persistence with database storage
- [ ] Add job execution history and audit logs
- [ ] Create web UI for job management
- [ ] Add metrics and monitoring (Prometheus/Grafana integration)
- [ ] Implement job dependencies and workflows
- [ ] Add support for distributed job execution
- [ ] Implement job retry policies and failure handling
- [ ] Add webhook notifications for job events
- [ ] Support for job priorities and resource limits
- [ ] Add REST API authentication and authorization
- [ ] Implement job templates and parameterization
- [ ] Add support for job scheduling across time zones

## Author

**Sachin Duhan** 
Github: https://github.com/sachin-duhan

---

For more information or support, please contact the maintainer or open an issue in the repository.