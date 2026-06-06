# ApplyDesk

ApplyDesk is a local-first desktop application for managing job applications, application documents, and the entire
application workflow in one place.

Built with Django, HTMX, and Electron, ApplyDesk focuses on simplicity, speed, and full ownership of your data.
Everything runs locally on your machine without requiring cloud services or external accounts.

---

## Overview

Searching for a new job often means managing dozens of applications, resumes, cover letters, interview invitations, and
company notes across multiple tools.

ApplyDesk brings everything together into a single workspace:

* Track applications through a visual Kanban pipeline
* Manage companies and contacts
* Store and organize application documents
* Track application history and status changes
* Analyze your application pipeline with dashboards and metrics
* Keep all data local and under your control

---

## Core Features

### Application Tracking

Manage your complete application pipeline:

* Saved
* Prepared
* Applied
* Waiting
* Interview
* Offer
* Rejected
* Archived

Applications can be moved through the workflow using:

* Status action buttons
* Drag & drop Kanban board

---

### Kanban Board

A visual overview of your application process.

Features:

* Drag & drop status updates
* Workflow validation
* Real-time updates with HTMX
* Status indicators
* Quick actions
* Application detail links

---

### Application Details

Each application contains:

* Position title
* Company information
* Contact details
* Application URL
* Notes
* Start date
* Current status
* Complete status history

---

### Company Management

Track companies independently from applications.

Store:

* Company name
* Location
* Notes
* Related applications

This allows building a personal company database over time.

---

### Document Management

Store and organize all documents related to an application.

Examples:

* Resume / CV
* Cover letters
* Certificates
* References
* Portfolio documents
* Application PDFs

Documents are linked directly to applications and companies.

Planned enhancements:

* Document templates
* Version management
* Generated application packages
* AI-assisted document creation

---

### Dashboard

Get insights into your application pipeline.

Metrics include:

* Total applications
* Active applications
* Interviews
* Offers
* Rejections
* Pipeline distribution

Future analytics:

* Conversion rates
* Time in status
* Monthly application activity
* Success tracking

---

## Architecture

ApplyDesk follows a server-driven UI architecture.

Frontend:

* HTMX
* Vanilla JavaScript
* Custom CSS

Backend:

* Django
* Service Layer Architecture
* SQLite (default)

Desktop Runtime:

* Electron

The application is intentionally built without a heavy SPA framework.

---

## Technology Stack

### Backend

* Python
* Django
* HTMX

### Desktop

* Electron

### Database

* SQLite

### Testing

* Pytest

### Python Tooling

* uv

---

## Installation

### Clone Repository

```bash
git clone https://github.com/<your-account>/applydesk.git
cd applydesk
```

### Create Environment

```bash
uv venv
source .venv/bin/activate
```

### Install Dependencies

```bash
uv sync
```

### Apply Migrations

```bash
uv run manage.py migrate
```

### Start Development Server

```bash
uv run manage.py runserver
```

---

## Testing

Run the complete test suite:

```bash
pytest
```

Run a specific test file:

```bash
pytest apps/applydesk/tests/views/
```

---

## Project Goals

ApplyDesk is designed around a few core principles:

### Local First

Your data belongs to you.

All application information, documents, and notes are stored locally.

### Fast UI

Use server-rendered HTML and HTMX instead of a large client-side application.

### Simplicity

Keep the workflow focused on job applications rather than becoming a generic CRM.

### Extensibility

Build a foundation that supports:

* Document generation
* Analytics
* AI-assisted application workflows
* Personal knowledge management

---

## Roadmap

### Phase 1

* Application management
* Company management
* Testing foundation

### Phase 2

* Workflow engine
* Kanban board
* Dashboard
* UX improvements

### Phase 3

* Document management
* Templates
* Analytics
* Reporting

### Phase 4

* AI-assisted application documents
* Resume optimization
* Cover letter generation
* Interview preparation support

---

## License

This project is licensed under the GNU GPLv3.

See LICENSE file for details.
