# Cronzimus Project Structure

## Overview

This document provides a detailed overview of the Cronzimus project structure, explaining the purpose and contents of each directory and file.

## Directory Structure

```
cronzimus/
├── cronzimus/              # Main application package
├── docker/                 # Docker configuration
├── k8s/                   # Kubernetes manifests
├── tests/                 # Test suite
├── docs/                  # Additional documentation
├── .venv/                 # Virtual environment (not in git)
├── Makefile              # Build automation
├── README.md             # Project overview
├── API.md                # API documentation
├── STRUCTURE.md          # This file
├── requirements.txt      # Python dependencies
└── cronzimus-supervisord.ini  # Supervisord configuration
```

## Core Application (`cronzimus/`)

### Main Files

#### `app.py`
- **Purpose**: Entry point for the Flask application
- **Key Components**:
  - Flask app initialization
  - APScheduler setup
  - Health check endpoint
  - Database connection initialization
- **Dependencies**: Flask, Flask-APScheduler, Database, config

#### `config.py`
- **Purpose**: Application bootstrap and configuration
- **Key Components**:
  - `bootstrap_app()`: Initializes logger and loads configuration
  - TODO: Dynaconf integration for configuration management
- **Dependencies**: logger

#### `VERSION`
- **Purpose**: Contains the application version number
- **Usage**: Version tracking for deployments and releases

### Common Utilities (`common/`)

#### `db.py`
- **Purpose**: Database connection management
- **Key Components**:
  - `Database` class for connection handling
  - Connection pooling (to be implemented)
  - Transaction management (to be implemented)
- **Usage**: Provides database access to all job functions

#### `logger.py`
- **Purpose**: Centralized logging configuration
- **Key Components**:
  - `init_logger()`: Configures loguru for application-wide logging
  - Log formatting and output configuration
  - Log level management
- **Dependencies**: loguru

### Controllers (`controller/`)

#### `task.py`
- **Purpose**: Sample task implementation
- **Key Components**:
  - `task()`: Example task function that receives database connection
  - Demonstrates proper task structure
- **Usage**: Template for creating new task functions

### Jobs Management (`jobs/`)

#### `__init__.py`
- **Purpose**: APScheduler configuration and job registration
- **Key Components**:
  - `APSchedulerConfig`: Main scheduler configuration class
  - `JOBS` property: Returns list of configured jobs
  - Job registration examples
- **Features**:
  - Dynamic job loading
  - Support for multiple trigger types
  - Database injection into jobs

#### `job_factory.py`
- **Purpose**: Factory pattern implementation for job creation
- **Key Components**:
  - `JobFactory.create_job()`: Creates jobs with different trigger types
  - Support for interval, cron, and date triggers
  - Standardized job creation interface
- **Usage**: Simplifies job creation and ensures consistency

### Utilities (`utils/`)

#### `env.py`
- **Purpose**: Environment variable management (to be implemented)
- **Planned Features**:
  - Environment variable validation
  - Type conversion
  - Default value handling

## Docker Configuration (`docker/`)

### `Dockerfile`
- **Purpose**: Container image definition
- **Key Components**:
  - Base image selection
  - Dependency installation
  - Application setup
  - Entry point configuration
- **Usage**: Building production-ready containers

## Kubernetes Manifests (`k8s/`)

### `Chart.yaml`
- **Purpose**: Helm chart metadata
- **Contents**:
  - Chart name and version
  - Description
  - Maintainer information

### Templates (`templates/`)

#### `cronzimus-deployment.yaml`
- **Purpose**: Kubernetes Deployment resource
- **Features**:
  - Container specification
  - Resource limits
  - Health checks
  - Environment variables

#### `cronzimus-service.yaml`
- **Purpose**: Kubernetes Service resource
- **Features**:
  - Service exposure
  - Port configuration
  - Load balancing

### Values (`values/`)

#### `values.yaml`
- **Purpose**: Default Helm values
- **Contents**: Base configuration for all environments

#### `yondu-stage.yaml`
- **Purpose**: Staging environment overrides
- **Contents**: Stage-specific configuration

#### `yondu-prod.yaml`
- **Purpose**: Production environment overrides
- **Contents**: Production-specific configuration

## Tests (`tests/`)

### `common/test_db.py`
- **Purpose**: Database module tests
- **Coverage**: Connection handling, error cases

### `controller/test_task.py`
- **Purpose**: Task controller tests
- **Coverage**: Task execution, return values

## Configuration Files

### `Makefile`
- **Purpose**: Build automation and development tasks
- **Commands**:
  - `install`: Install dependencies
  - `run`: Start application
  - `test`: Run test suite
  - `lint`: Code quality checks
  - `format`: Code formatting
  - `security`: Security scanning
  - `clean`: Cleanup

### `requirements.txt`
- **Purpose**: Python dependency specification
- **Key Dependencies**:
  - Flask==2.3.2
  - Flask-APScheduler==1.12.4
  - gunicorn==21.2.0
  - loguru==0.6.0
  - Development tools (pytest, black, flake8, isort, bandit)

### `cronzimus-supervisord.ini`
- **Purpose**: Process management configuration
- **Usage**: Production deployment with supervisord
- **Features**: Auto-restart, logging, process monitoring

## Development Workflow

### Adding New Features

1. **New Task**:
   - Create task function in `controller/`
   - Register in `jobs/__init__.py`
   - Add tests in `tests/controller/`

2. **New API Endpoint**:
   - Add route in `app.py`
   - Update API documentation
   - Add integration tests

3. **Configuration Changes**:
   - Update `config.py`
   - Add environment variables to Kubernetes values
   - Update documentation

### Code Organization Principles

1. **Separation of Concerns**: Each module has a single responsibility
2. **Factory Pattern**: Consistent job creation through JobFactory
3. **Dependency Injection**: Database passed to tasks as parameter
4. **Configuration Management**: Centralized in config module
5. **Testing**: Parallel test structure mirrors source code

## Future Structure Additions

### Planned Directories

- `migrations/`: Database schema migrations
- `static/`: Static assets for web UI
- `templates/`: HTML templates for web UI
- `api/`: Dedicated API module
- `models/`: Database models
- `services/`: Business logic services

### Planned Files

- `.env.example`: Environment variable template
- `docker-compose.yml`: Local development orchestration
- `setup.py`: Package installation configuration
- `CHANGELOG.md`: Version history
- `CONTRIBUTING.md`: Contribution guidelines

## Security Considerations

1. **No Secrets in Code**: Use environment variables
2. **Input Validation**: Validate all external inputs
3. **Dependency Scanning**: Regular security updates
4. **Access Control**: Implement authentication when needed
5. **Logging**: No sensitive data in logs

## Performance Considerations

1. **Job Isolation**: Each job runs independently
2. **Resource Limits**: Configure in Kubernetes
3. **Database Pooling**: To be implemented
4. **Async Operations**: Consider for I/O-bound tasks
5. **Monitoring**: Implement metrics collection