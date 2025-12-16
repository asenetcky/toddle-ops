# Agent Card: ToddleOps Research Team

## Agent Details
- **Name:** ToddleOpsResearchTeam
- **Type:** Specialist Team (Researcher + Synthesizer)
- **Underlying Model:** Gemini 2.5 Flash Lite
- **Framework:** Google ADK
- **Date:** December 2025
- **Maintainer:** ToddleOps Team

## Intended Use
- **Primary Use Case:** Discover and formulate safe, engaging toddler activities based on user requests.
- **Target Audience:** The Orchestrator Agent (internal system use).
- **Out-of-Scope Use Cases:**
    - Providing medical or safety advice directly to users.
    - Researching non-toddler topics.

## Team Composition & Capabilities
This "agent" is actually a sequential pipeline of two specialized agents:

1.  **`ProjectResearcher`**
    - **Role:** Information Gatherer.
    - **Tools:** `google_search`.
    - **Function:** Uses Google Search to find real-world examples of toddler crafts and activities that match the user's intent. It filters for safety and feasibility (household materials).

2.  **`ProjectSynthesizer`**
    - **Role:** Content Creator.
    - **Tools:** None (Pure LLM).
    - **Function:** Takes the raw research notes from the Researcher and structures them into a coherent `StandardProject` object. It combines the best elements from multiple sources if necessary.

## Logic & Behavior
- **Persona:**
    - **Researcher:** Curious, thorough, and safety-conscious.
    - **Synthesizer:** Organized, creative, and structured.
- **Workflow:**
    1.  Receive a topic/request (e.g., "sensory bin ideas").
    2.  Researcher queries Google for safe, age-appropriate ideas.
    3.  Researcher compiles a summary of findings (`project_research`).
    4.  Synthesizer analyzes the findings and creates a single, definitive project plan.
    5.  Output is strictly typed as a `StandardProject`.

## Inputs & Outputs
- **Input:** A research topic or user request string.
- **Output:** A `StandardProject` object containing:
    - `name`: Title of the activity.
    - `description`: Short summary.
    - `duration_minutes`: Estimated time.
    - `materials`: List of required items.
    - `instructions`: Ordered list of steps.

## Safety & Ethical Considerations
- **Source Verification:** The Researcher relies on public internet data. While it filters for "safe" and "toddler" keywords, it cannot physically verify the safety of a search result.
- **Hallucination Mitigation:** The Synthesizer is grounded in the Researcher's output, reducing the chance of inventing dangerous steps, but it is not immune to hallucinating details not present in the search results.

## Limitations
- **Search Dependence:** If Google Search returns poor or irrelevant results (e.g., for a very obscure request), the Synthesizer may struggle to create a high-quality project.
- **No Visuals:** The team currently processes text only and cannot verify if a project looks appealing or safe based on images.
