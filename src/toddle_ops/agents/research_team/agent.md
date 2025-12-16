# Agent Card: ToddleOps Research Team

## Agent Details
- **Name:** ToddleOpsResearchTeam
- **Type:** Specialist Team (Coordinator + Parallel Researchers + Synthesizer)
- **Underlying Model:** Gemini 2.5 Flash Lite
- **Framework:** Google ADK
- **Date:** December 2025
- **Maintainer:** ToddleOps Team

## Intended Use
- **Primary Use Case:** Discover and formulate safe, engaging toddler activities based on user requests, leveraging diverse search strategies.
- **Target Audience:** The Orchestrator Agent (internal system use).
- **Out-of-Scope Use Cases:**
    - Providing medical or safety advice directly to users.
    - Researching non-toddler topics.

## Team Composition & Capabilities
This team is structured as a coordinated system with parallel research capabilities:

1.  **`ProjectResearchCoordinator` (Root Agent)**
    - **Role:** Team Lead.
    - **Function:** Coordinates the research process. It can choose to run a full parallel research workflow or delegate to a single researcher for specific tasks.

2.  **`ResearchParallel` (Workflow)**
    - **Role:** Diverse Information Gathering.
    - **Components:**
        - **`HighTempProjectResearcher` (Temp 1.2):** Explores creative, novel, and perhaps less conventional ideas.
        - **`LowTempProjectResearcher` (Temp 0.7):** Focuses on reliable, standard, and highly safe ideas.
    - **Function:** Runs both researchers simultaneously to gather a broad spectrum of potential projects.

3.  **`ProjectSynthesizer`**
    - **Role:** Content Creator & Merger.
    - **Function:** Analyzes the outputs from both the High and Low temperature researchers. It selects the best elements—combining creativity with reliability—to structure a single coherent `StandardProject`.

4.  **`DefaultTempProjectResearcher`**
    - **Role:** Generalist Researcher.
    - **Function:** Available as a direct tool for the coordinator for standard queries that may not require the full parallel pipeline.

## Logic & Behavior
- **Persona:**
    - **Coordinator:** Strategic and delegative.
    - **Researchers:** Thorough and safety-conscious (with varying degrees of creativity).
    - **Synthesizer:** Discerning and structured.
- **Workflow:**
    1.  **Coordination:** The Coordinator receives a request (e.g., "rainy day activities").
    2.  **Parallel Execution:** Typically delegates to `ResearchSequence`, triggering `ResearchParallel`.
    3.  **Divergent Search:**
        - High Temp agent looks for unique angles.
        - Low Temp agent looks for tried-and-true classics.
    4.  **Convergent Synthesis:** The Synthesizer reviews `high_temp_project_research` and `low_temp_project_research`. It merges the most engaging ideas into a single plan.
    5.  **Output:** A strictly typed `StandardProject` object.

## Inputs & Outputs
- **Input:** A research topic or user request string.
- **Output:** A `StandardProject` object containing:
    - `name`: Title of the activity.
    - `description`: Short summary.
    - `duration_minutes`: Estimated time.
    - `materials`: List of required items.
    - `instructions`: Ordered list of steps.

## Safety & Ethical Considerations
- **Safety Settings:** All researchers utilize `BLOCK_LOW_AND_ABOVE` for dangerous content to ensure high safety standards at the source.
- **Source Verification:** Relies on Google Search. The parallel approach helps cross-reference ideas—if a "creative" idea seems unsafe compared to the "conservative" baseline, the Synthesizer can filter it out.
- **Hallucination Mitigation:** The Synthesizer is grounded in two distinct research streams, providing a richer context window to verify details before generation.

## Limitations
- **Complexity:** The parallel workflow consumes more tokens and API calls than a single researcher.
- **Conflict Resolution:** If the high and low temp researchers find contradictory information, the Synthesizer must make a judgment call, which is not always perfect.
