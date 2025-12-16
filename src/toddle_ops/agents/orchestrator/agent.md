# Agent Card: ToddleOps Orchestrator

## Agent Details
- **Name:** ToddleOpsOrchestrator
- **Type:** Orchestrator / Root Agent
- **Underlying Model:** Gemini 2.5 Flash Lite
- **Framework:** Google ADK
- **Date:** December 2025
- **Maintainer:** ToddleOps Team

## Intended Use
- **Primary Use Case:** Serve as the central entry point for the ToddleOps system. It interprets user requests for toddler activities and delegates the actual work to specialized workflows.
- **Target Audience:** Parents and caregivers of toddlers (ages 1-3) looking for quick, safe, and engaging activity ideas.
- **Out-of-Scope Use Cases:** 
    - Direct generation of medical advice or developmental diagnosis.
    - Generating activities for older children or adults without adaptation.
    - Answering general knowledge questions unrelated to toddler projects (though it may attempt to answer, it is not optimized for this).

## Capabilities & Tools
The agent is equipped with specific tools to fulfill its objective:

1.  **`ToddleOpsSequence` (Project Generation Workflow)**
    - **Description:** A specialized sequential workflow that handles the end-to-end process of researching, validating (safety/QA), and formatting toddler projects.
    - **Usage:** The agent is strictly instructed to use this tool for *all* project requests.

2.  **`preload_memory`**
    - **Description:** A service that loads past interaction context.
    - **Usage:** Enables the agent to recall user preferences (e.g., "we don't have glue") or previous projects to avoid repetition.

## Logic & Behavior
- **Persona:** "ToddleOps Root Agent" - Efficient, helpful, and decisive.
- **Decision Making Strategy:**
    - **Action-Oriented:** The agent is designed to be low-friction. If a user request is vague (e.g., "I need an idea"), the agent is instructed *not* to ask for more details but to proceed immediately with the `ToddleOpsSequence` tool to generate a suggestion.
    - **Delegation:** It does not attempt to generate project content (materials, steps) itself. It acts purely as a manager that passes the user's intent to the specialist workflow.
- **Key Rules:**
    - MUST use `ToddleOpsSequence` for project requests.
    - SHOULD NOT attempt to generate projects directly.
    - ALWAYS output the `human_project` key when the workflow completes.

## Inputs & Outputs
- **Input:** Natural language text from the user (e.g., "Make me a project using cardboard boxes").
- **Output:** A structured, human-readable markdown block (`human_project`) containing:
    - Project Name
    - Description
    - Duration
    - Materials List
    - Step-by-step Instructions

## Safety & Ethical Considerations
- **Safety First:** While this agent orchestrates, the actual safety validation happens within the `ToddleOpsSequence` via a dedicated Safety Critic agent. This separation of concerns ensures that safety checks are not bypassed by the orchestrator's desire to be helpful.
- **Underlying Model Safety:** Inherits the safety filters and alignment of the Gemini 2.5 Flash Lite model regarding harmful content.
- **Bias & Cultural Context:** The agent assumes "common household materials" based on a general Western context. Users in different regions may find some materials less accessible.

## Limitations
- **Tool Dependency:** The agent is functionally limited by the `ToddleOpsSequence`. If the research or QA sub-agents fail, the orchestrator cannot fulfill the request.
- **Ambiguity Handling:** By design, the agent avoids asking clarifying questions to speed up the process. This means it might occasionally generate a project that doesn't perfectly match a user's unstated constraints (which they can then correct in a follow-up turn).
