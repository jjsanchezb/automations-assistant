# **Automata: An AI-Powered Integration Platform**

**Automata** is a proof-of-concept for a self-contained, AI-native workflow automation platform built in Python. Its architecture is designed to be both powerful and highly extensible, centered around two key AI-native features:

1. A **generic and configurable "AI Call" action** that can be embedded as a step within any workflow to perform intelligent, dynamic tasks.
2. An **"AI Assistant Workflow Builder"** that translates a single, high-level user command into a complete, multi-step workflow blueprint.

This document outlines the architecture and key mechanisms of the platform.

## **🎬 Live Demo _Coming Soon_**

This demo should show the full, end-to-end "meta" workflow: the AI Assistant builds a workflow from a user command, and that workflow then executes, using the generic "AI Call" action to generate code for a new integration.

## **🎯 Core Use Case: The Generic Onboarding Workflow**

The entire system is designed to showcase its power by executing a "meta" workflow—using the platform's own standard building blocks to automate the creation and onboarding of a new integration for itself.

**User Command:** "Onboard the new 'Simple CRM' API. The OpenAPI spec is at http://crm-api:8055/server/specs/oas. After scaffolding the integration, create a health check monitor for its /users endpoint, create a Focalboard card for the 'Integration Review' board, and notify the \#integrations channel in Slack."

## **🏗️ System Architecture**

The platform runs as a self-contained set of services managed by Docker Compose. The architecture is designed for scalability and resilience, using a central database as the source of truth for all runtime configurations and integration code.

### **Technology Stack**

| Role in Platform        | Technology / Service | Purpose                                                                  |
| :---------------------- | :------------------- | :----------------------------------------------------------------------- |
| **The Brains & Engine** | **Django & Celery**  | Core application, API, and asynchronous task execution engine.           |
| **Central Database**    | **PostgreSQL**       | Stores workflow definitions and the Python code for all integrations.    |
| **Example Target API**  | **Directus**         | A sample service providing an OpenAPI spec for the demo workflow.        |
| **Code Source Control** | **Gitea**            | The Git service where the AI commits scaffolded code for human review.   |
| **Project Management**  | **Focalboard**       | Kanban board for managing the integration approval lifecycle.            |
| **Artifact Store**      | **MinIO (S3)**       | Stores the final, versioned integration "artifact" ready for deployment. |

## **⚙️ Key Mechanisms & Concepts**

#### **1\. The Generic "AI Call" Action**

The platform includes a standard, reusable AI Call action. This action is a powerful building block that can be configured with specific system prompts, user prompts, and a set of "tools" to structure its output.

In our showcase workflow, this action should be configured to act as a **code generator**. It's given a system prompt that instructs it to parse an OpenAPI specification and a user prompt containing the spec's URL. The result is a structured JSON object containing the generated Python code and a list of dependencies.

#### **2\. The AI Assistant Workflow Builder**

To create workflows, users interact with an AI Assistant. This assistant takes a high-level goal (like the user command above) and translates it into the platform's structured JSON workflow format. It intelligently selects from the library of available actions (like the AI Call action, Gitea actions, Focalboard actions, etc.) to construct the final blueprint.

#### **3\. The Deployment Pipeline (Simulated via Django Command)**

This project simulates a CI/CD deployment pipeline with a Django management command. This command is responsible for bridging the gap between development (Gitea) and production (the live platform).

```
# This command takes the code from a Gitea repo, packages it,
# uploads it to S3, and registers it in the database.
python manage.py deploy_integration --repo-url <gitea-repo-url>
```

#### **4\. Stateless Runtime & Integration Loading**

The Celery workers that execute workflows are completely stateless. They do not depend on a shared filesystem. When a workflow needs to run an integration, the worker:

1. Queries the PostgreSQL database to get the S3 path for the required integration artifact.
2. Downloads the artifact from MinIO.
3. Loads the code and its dependencies in an isolated environment to execute the action.

This architecture allows the Celery worker fleet to be scaled horizontally without any complex state synchronization.

#### **5\. The Approval & Activation Lifecycle**

An integration is not made live until it passes a human review and is explicitly deployed.

1. **Review**: A developer reviews the AI-generated code in the Gitea repository.
2. **Approval**: To signify approval, the developer moves the corresponding task card in Focalboard to the "Done" list.
3. **Activation**: The developer then manually runs the deploy_integration Django command. This command is the single point of activation: it packages the code, uploads it to the artifact store, registers it in the database, and sets `is_active = true`, making the integration live on the platform.

#### **5\. Graph-Based Workflows**

Workflows are modeled as directed graphs, This allows for powerful and flexible orchestration, including branching (if/else), parallel execution, and merging. The graph is defined by two tables: WorkflowStep (nodes) and WorkflowEdge (connections), enabling the platform to validate against issues like infinite loops or dead ends.

#### **6\. Stateless Choreographed Execution Engine**

The platform does not use a long-running "engine" process. Instead, it uses a stateless choreography pattern (a "relay race").

- A central Dispatcher initiates a workflow by dispatching the first task to Celery.

- Each Celery task is a short-lived, independent "runner" that executes a single step.

- Upon completion, each task is responsible for evaluating the workflow graph and dispatching the next task(s) in the sequence. This makes the system highly scalable and resilient.

#### **7\. Snapshotting for Auditing and Reliability**

When a workflow is executed, the system takes a complete, immutable snapshot of the workflow's definition (all its steps, edges, and inputs) and stores it in the WorkflowRun record. The execution engine uses this snapshot, not the live workflow definition. This critical feature ensures that:

- Historical accuracy is maintained, even if the main workflow is edited later.

- The execution is decoupled and reliable, unaffected by simultaneous user edits.

## **🚀 Implementation Plan**

This project will be built in distinct phases, each with a clear, demonstrable goal to ensure a fast feedback loop.

#### **Phase 0: Infrastructure Foundation**

- **Goal:** Launch and connect all required services (Django, Celery, PostgreSQL, Gitea, Focalboard, MinIO, Directus) using a single docker-compose up command. This phase establishes a stable development environment.

#### **Phase 1: Core Orchestration Engine**

- **Goal:** Prove the core mechanics by executing a hardcoded, multi-step workflow (e.g., create a Gitea repo, then a Focalboard card) triggered by a single API call. This validates the Celery task runner and inter-service communication.

#### **Phase 2: The Generic "AI Call" Action**

- **Goal:** Introduce the first AI-native feature. We will replace a static step from Phase 1 with the generic AI Call action, using an LLM to dynamically generate Python code from an OpenAPI specification and commit it to Gitea.

#### **Phase 3: AI Assistant & Deployment Simulation**

- **Goal:** Complete the full, end-to-end user story. This involves building an API endpoint that uses an LLM to translate a natural language command into a workflow blueprint and implementing the deploy_integration command to simulate the final activation of the generated integration.
