# Cronzimus API Documentation

## Overview

Cronzimus exposes a RESTful API for health monitoring and job management. The API is built using Flask and follows standard REST conventions.

## Base URL

```
http://localhost:5000
```

## Authentication

Currently, the API does not require authentication. This may change in future versions.

## Endpoints

### Health Check

#### GET /api/health

Check the health status of the Cronzimus service.

**Request:**
```http
GET /api/health HTTP/1.1
Host: localhost:5000
```

**Response:**
```json
{
  "status": "running"
}
```

**Status Codes:**
- `200 OK` - Service is healthy and running

**Example:**
```bash
curl http://localhost:5000/api/health
```

---

## APScheduler API Endpoints

When `SCHEDULER_API_ENABLED = True` in the configuration, the following job management endpoints become available:

### List All Jobs

#### GET /scheduler/jobs

Retrieve a list of all scheduled jobs.

**Request:**
```http
GET /scheduler/jobs HTTP/1.1
Host: localhost:5000
```

**Response:**
```json
[
  {
    "id": "sample_task",
    "name": "task",
    "trigger": "interval[0:00:05]",
    "next_run_time": "2024-01-15 10:30:00",
    "state": "running"
  }
]
```

**Status Codes:**
- `200 OK` - Successfully retrieved job list

---

### Get Job Details

#### GET /scheduler/jobs/{job_id}

Retrieve details of a specific job.

**Request:**
```http
GET /scheduler/jobs/sample_task HTTP/1.1
Host: localhost:5000
```

**Response:**
```json
{
  "id": "sample_task",
  "name": "task",
  "trigger": {
    "type": "interval",
    "seconds": 5
  },
  "next_run_time": "2024-01-15 10:30:00",
  "state": "running",
  "args": ["<Database instance>"],
  "kwargs": {}
}
```

**Status Codes:**
- `200 OK` - Job found
- `404 Not Found` - Job not found

---

### Add New Job

#### POST /scheduler/jobs

Create a new scheduled job.

**Request:**
```http
POST /scheduler/jobs HTTP/1.1
Host: localhost:5000
Content-Type: application/json

{
  "id": "new_task",
  "func": "cronzimus.controller.task:task",
  "trigger": "interval",
  "seconds": 10
}
```

**Response:**
```json
{
  "id": "new_task",
  "status": "added"
}
```

**Status Codes:**
- `200 OK` - Job successfully added
- `400 Bad Request` - Invalid job configuration
- `409 Conflict` - Job with same ID already exists

---

### Update Job

#### PUT /scheduler/jobs/{job_id}

Update an existing job configuration.

**Request:**
```http
PUT /scheduler/jobs/sample_task HTTP/1.1
Host: localhost:5000
Content-Type: application/json

{
  "trigger": "interval",
  "seconds": 30
}
```

**Response:**
```json
{
  "id": "sample_task",
  "status": "updated"
}
```

**Status Codes:**
- `200 OK` - Job successfully updated
- `404 Not Found` - Job not found
- `400 Bad Request` - Invalid configuration

---

### Remove Job

#### DELETE /scheduler/jobs/{job_id}

Remove a scheduled job.

**Request:**
```http
DELETE /scheduler/jobs/sample_task HTTP/1.1
Host: localhost:5000
```

**Response:**
```json
{
  "id": "sample_task",
  "status": "removed"
}
```

**Status Codes:**
- `200 OK` - Job successfully removed
- `404 Not Found` - Job not found

---

## Job Configuration

### Trigger Types

#### Interval Trigger

Run job at fixed intervals.

```json
{
  "trigger": "interval",
  "seconds": 30,
  "minutes": 5,
  "hours": 1
}
```

#### Cron Trigger

Run job using cron expression.

```json
{
  "trigger": "cron",
  "hour": 2,
  "minute": 30,
  "day_of_week": "mon-fri"
}
```

#### Date Trigger

Run job once at specific date/time.

```json
{
  "trigger": "date",
  "run_date": "2024-01-15 14:30:00"
}
```

### Job States

- `running` - Job is active and will execute at scheduled times
- `paused` - Job is temporarily paused
- `pending` - Job is waiting for its first execution

---

## Error Responses

All error responses follow this format:

```json
{
  "error": "Error message description",
  "code": "ERROR_CODE"
}
```

Common error codes:
- `JOB_NOT_FOUND` - Requested job does not exist
- `INVALID_TRIGGER` - Invalid trigger configuration
- `JOB_EXISTS` - Job with given ID already exists
- `INVALID_FUNCTION` - Function reference is invalid

---

## Rate Limiting

Currently, there are no rate limits on the API. This may change in future versions.

---

## Webhooks

Future versions may support webhooks for job execution events.

---

## Examples

### Create an Interval Job

```bash
curl -X POST http://localhost:5000/scheduler/jobs \
  -H "Content-Type: application/json" \
  -d '{
    "id": "cleanup_task",
    "func": "cronzimus.controller.task:task",
    "trigger": "interval",
    "minutes": 60
  }'
```

### Create a Cron Job

```bash
curl -X POST http://localhost:5000/scheduler/jobs \
  -H "Content-Type: application/json" \
  -d '{
    "id": "daily_report",
    "func": "cronzimus.controller.task:task",
    "trigger": "cron",
    "hour": 9,
    "minute": 0
  }'
```

### Pause a Job

```bash
curl -X POST http://localhost:5000/scheduler/jobs/sample_task/pause
```

### Resume a Job

```bash
curl -X POST http://localhost:5000/scheduler/jobs/sample_task/resume
```

---

## Best Practices

1. **Job IDs**: Use descriptive, unique IDs for jobs (e.g., `daily_backup`, `hourly_sync`)
2. **Error Handling**: Always handle potential errors in job functions
3. **Logging**: Use appropriate logging in job functions for debugging
4. **Resource Management**: Be mindful of resource usage in frequently running jobs
5. **Testing**: Test job functions independently before scheduling

---

## Versioning

This API documentation is for Cronzimus v0.1. Future versions may introduce breaking changes.

---

## Support

For API-related issues or questions, contact:
- Email: sachin.duhan@eulermotors.com
- GitHub: [cronzimus/issues](https://github.com/sachin-duhan/cronzimus/issues)