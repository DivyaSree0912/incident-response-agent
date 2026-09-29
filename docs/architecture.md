#Project Architecture
# Incident Response Agent — Architecture

## Overview

The Incident Response Agent helps investigate incidents by combining the
current incident with relevant historical incident memory.

## Core Flow

Incident
↓
Investigate
↓
Resolve
↓
Hindsight Retain
↓
Persistent Memory
↓
New Incident
↓
Hindsight Recall
↓
Historical Evidence
↓
AI Agent
↓
Investigation and Recommendation

## Main Components

### Frontend
Provides the interface for viewing incidents and investigation results.

### Backend
Acts as the central bridge between the frontend, AI agent, and Hindsight
memory system.

### AI Agent
Investigates the current incident using the incident details and relevant
historical evidence.

### Hindsight Memory
Stores resolved incident experiences using Retain and retrieves relevant
historical experiences using Recall.

## Memory Loop

The key demonstration is that a resolved incident is retained as persistent
memory and can later be recalled when a similar incident occurs.
