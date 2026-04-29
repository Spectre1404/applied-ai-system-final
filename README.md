# Explainable AI Music Recommendation Assistant

An applied AI system that takes a natural-language music request, retrieves relevant songs from a local dataset, ranks the best matches, and explains why each recommendation was chosen. This project extends my earlier **Music_recommender** into a more complete AI system with retrieval-based reasoning, guardrails, logging, and reliability testing.

## Original Project

The original **Music_recommender** project focused on recommending songs based on similarity and user preference patterns. It could suggest related music, but it did not yet support natural-language queries, explanation generation, guardrails, or structured reliability evaluation.

## Title and Summary

This project improves the recommender into an explainable applied AI system. It matters because music recommendation is a useful everyday task, and transparent recommendations are easier to trust than black-box outputs.

## Architecture Overview

The system takes a natural-language prompt and extracts useful intent such as mood, genre, artist, or activity. It then retrieves matching songs from the dataset, ranks the best candidates, and generates short explanations for each recommendation. Guardrails handle weak inputs or no-match cases, while logging and evaluation components track performance and support reliability testing.

![Architecture Diagram](assets/applied-ai-flowchart.png)

## Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/Spectre1404/applied-ai-system-final.git
cd applied-ai-system-final
```

### 2. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

## Run the Project

```bash
python src/main.py
```

## Sample Interactions

### Example 1
**Input:** `Recommend calm songs for studying`

**Output:**  
- Top recommendations from the dataset.
- Short reasons like calm mood, low energy, or acoustic fit.
- Confidence score showing how strong the match is.

### Example 2
**Input:** `Give me upbeat pop songs for a workout`

**Output:**  
- Energetic pop songs from the dataset.
- Explanations based on genre and energy.
- Higher confidence because the query is specific.

### Example 3
**Input:** `asdfghjkl`

**Output:**  
`Please enter a mood, artist, genre, or activity.`

## Design Decisions

A retrieval-based design was chosen so the system uses real songs from the dataset before generating the final recommendation. This makes the AI more grounded and explainable than a generic response.

A simple workflow was preferred over a more complex agentic setup because the main goal was a reliable, polished system that could be tested and explained clearly. Logging and guardrails were added so failures would be easier to diagnose and the app could fail safely.

## Testing Summary

The system was tested with clear prompts, vague prompts, invalid input, and edge cases where no strong match existed. It performed best when the user gave a clear mood, genre, artist, or activity.

Example summary:
- 5 out of 6 tests passed.
- Average confidence score: 0.81.
- Main weakness: vague prompts with too little context.

## Reflection

This project showed that AI systems are strongest when they are transparent, testable, and grounded in real data. Retrieval improved trust because recommendations were based on the dataset rather than invented output.

It also showed the value of guardrails and evaluation. Even a useful AI system needs fallback behavior, logging, and clear explanations to be dependable. One helpful AI suggestion was splitting the app into modular files; one weaker suggestion was adding unnecessary complexity before the core workflow was stable.

AI isn't just about what works — it's about what's responsible. This project taught me that even a simple recommendation system can reflect the limitations and biases of its data and rules. One limitation of this system is that recommendations depend heavily on the available metadata; if certain genres, moods, or artists are underrepresented in the dataset, they will be underrepresented in the suggestions. This can introduce bias toward more popular or well‑labeled tracks. The system could also be misused if users treat its suggestions as authoritative “truth” rather than as probabilistic, data‑driven guesses. To prevent misuse, I added explicit confidence scores and fallback messages, so users can see when the system is uncertain or when no strong match exists.

While testing reliability, I was surprised by how sharply the system’s performance dropped on vague or overlapping prompts like “Recommend something good.” These cases often matched too many songs loosely, so the confidence and explanation were weak and less useful. This led me to strengthen the guardrails and add clearer fallbacks for truly ambiguous inputs.

Collaborating with AI during this project helped me move faster and explore better designs. One helpful suggestion was breaking the recommender into modular components: retriever, recommender, guardrails, and evaluator, which made the code cleaner and easier to test. One flawed suggestion was proposing a more complex agent‑style loop early in the project; it would have added layers of abstraction and unnecessary planning steps that did not improve the core recommendation quality, made the behavior harder to debug, and risked over‑engineering the code. Overall, this project deepened my respect for the balance between powerful AI features, simple, testable code, and clear, responsible communication to the user.

## VIDEO LINK: GOOGLE DRIVE (ANYONE WITH A LINK CAN ACCESS)

https://drive.google.com/file/d/11-idlwMS6S6MGxTQjx-CmXZAjSSakTiX/view?usp=sharing

## Repository Link
GitHub Repository: https://github.com/Spectre1404/applied-ai-system-final

## Portfolio Reflection
This project shows that I can take an existing recommendation system and extend it into a more complete applied AI workflow with retrieval, explainability, guardrails, and evaluation. It reflects the way I approach AI engineering: I care about building systems that are practical, testable, and transparent, not just systems that generate outputs. I want my work to be useful in real settings and responsible in how it handles uncertainty, edge cases, and user trust.