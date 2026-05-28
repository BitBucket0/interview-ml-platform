<Up><Down># Database Schema Documentation

This document describes the core PostgreSQL schema for the `interview-ml-platform` project.

# Database Schema Documentation

This document describes the core PostgreSQL schema for the `interview-ml-platform` project.

The system tracks users, their study activity, and machine-learning labels that can later be used for prediction tasks.

## Overview

The database currently contains three main application tables:

1. `users`
2. `study_events`
3. `labels`

The basic data flow is:

```text
users
  └── study_events
  └── labels
