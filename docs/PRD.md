# Requirements for Foggy - Your personalized coding tutor

## Requirements:
1. The agent should be able to interact with the user to identify the goal of the user.
2. The agent should be capable of searching the web to identify the relevant items based on the user's goal.
3. The agent should list out the pre-requisites and ask the user the knowledge they have on each of the pre-requisites.
4. The agent can craft the plan to include pre-requisites as well based on the user's requirements.
5. Based on the user's goal, pre-requisites of the language and the user's understanding of the pre-requisites, the agent must draft a plan.
    - The plan must be section wise.
    - Each section must first cover core concepts first through conceptual understandings, then cover the same using examples post which a mini project is given for the user to complete.
    - Based on the completion, the evaluator agent gives feedback and helps correct mistakes of the learner.
    - The evaluator also must suggest redoing the section with different examples if required.
6. The application must support per section examples used and project to be summarized and stored to ensure no repeat in the case user wishes to redo the section.
7. The application must support redoing a section.
8. The application must track user progress through storing data in .md files within the user-learning folder.
9. Agent state must be wiped after every section.
10. Human in loop every step of the way wether it is planning, understanding or suggesting a redo.
11. Support Q&A on the generated example.
