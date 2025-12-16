# Agent Card: ToddleOps Quality Assurance Team

## Agent Details
- **Name:** ToddleOpsQualityAssuranceTeam
- **Type:** Specialist Team (Safety Critic + Refiner + Editor)
- **Underlying Model:** Gemini 2.5 Flash Lite
- **Framework:** Google ADK
- **Date:** December 2025
- **Maintainer:** ToddleOps Team

## Intended Use
- **Primary Use Case:** Review, refine, and polish draft toddler projects to ensure they are safe, age-appropriate, and clearly written.
- **Target Audience:** The Orchestrator Agent (internal system use).
- **Out-of-Scope Use Cases:**
    - Generating original project ideas (this is the Research Team's job).
    - Legal compliance certification.

## Team Composition & Capabilities
This team operates as a pipeline with a feedback loop:

1.  **`SafetyCriticAgent`**
    - **Role:** Safety Auditor.
    - **Function:** Reviews a `StandardProject` for hazards (choking, toxicity, sharp objects). Outputs a `StatusReport` (APPROVED or REVISION_NEEDED) with specific feedback.

2.  **`SafetyRefinerAgent`**
    - **Role:** Safety Fixer.
    - **Function:** If the Critic requests revisions, this agent rewrites the project to address the safety concerns while maintaining the fun factor. It loops back to the Critic until approved.

3.  **`EditorialAgent`**
    - **Role:** Copy Editor.
    - **Function:** Once safety is approved, this agent polishes the text for clarity, grammar, and tone. It ensures instructions are easy for a sleep-deprived parent to follow.

## Logic & Behavior
- **Persona:**
    - **Critic:** Strict, vigilant, "Safety First."
    - **Refiner:** Problem-solver, adaptive.
    - **Editor:** Clear, concise, encouraging.
- **Workflow:**
    1.  Receive a draft `StandardProject`.
    2.  **Safety Loop:**
        - Critic evaluates the project.
        - If unsafe -> Refiner fixes it -> Critic re-evaluates.
        - If safe -> Exit loop.
    3.  **Editorial Pass:** Editor polishes the final safe draft.
    4.  Output the finalized `StandardProject`.

## Inputs & Outputs
- **Input:** A draft `StandardProject` object (likely from the Research Team).
- **Output:** A finalized, safety-approved, and edited `StandardProject` object.

## Safety & Ethical Considerations
- **Critical Safety Layer:** This team is the primary defense against harmful content. The Critic is explicitly instructed to look for age-specific hazards (e.g., small parts for <3 year olds).
- **Loop Limits:** The safety refinement loop has a maximum iteration count (default: 3) to prevent infinite loops if a project cannot be made safe. In such cases, it may fail or return the best effort.
- **Human-in-the-Loop:** While this automated QA is robust, it does not replace parental supervision. The system assumes a parent is facilitating the activity.

## Limitations
- **Context Blindness:** The Critic cannot know the specific physical abilities or allergies of a specific child unless provided in the context (which is currently not standard).
- **Subjectivity:** "Clarity" and "Age-Appropriateness" can be subjective. The Editor optimizes for a general audience.
