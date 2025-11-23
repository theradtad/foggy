"""Random response templates for dummy conversation simulation.

This module contains predefined response templates categorized by conversation
context (Planning, Teaching, Evaluation) to simulate realistic AI tutor responses.
"""

import random
from typing import Dict, List


# Response categories mapped to conversation contexts
RESPONSES: Dict[str, List[str]] = {
    "planning": [
        "I understand you'd like to learn more about that topic. Let me analyze your current skill level and create a personalized learning plan.",
        "Based on what you've shared, I can design a structured curriculum that builds your knowledge progressively.",
        "Great! Let's assess your goals and background to craft the perfect learning journey for you.",
        "I'm analyzing your learning objectives now. This will help me suggest the most effective learning path.",
        "Tell me more about your experience level and what specific aspects interest you the most.",
        "I can create a comprehensive plan that includes theoretical foundations and practical projects.",
        "Your learning objectives are clear. Now let me map out the key milestones for your journey.",
        "Let's break down this complex topic into manageable, achievable learning objectives.",
        "I notice you have some foundational knowledge. We'll build upon that strategically.",
        "Perfect! I can design a curriculum that matches your learning style and pace.",
    ],
    "teaching": [
        "Let's start with a simple example to demonstrate this concept in action.",
        "Here's how we can implement this idea step by step.",
        "Let me walk you through this code example and explain each component.",
        "Have you tried implementing this yourself? I'd love to see your approach.",
        "This concept builds on what we learned earlier. Let me show you the connection.",
        "Let's modify this example to better suit your learning needs.",
        "Excellent question! The key insight here is understanding how these pieces fit together.",
        "I can see you're grasping the fundamentals. Let's move to a more advanced application.",
        "Let me break down this complex operation into smaller, understandable steps.",
        "That's a great observation! Now let's apply this understanding to a real-world scenario.",
    ],
    "evaluation": [
        "Let me review your understanding by asking a few targeted questions.",
        "Your progress has been impressive! Here are my observations about your learning journey.",
        "Based on our interactions, I can identify both your strengths and areas for improvement.",
        "Let's assess how well you've internalized these concepts through a quick review.",
        "I'm analyzing your problem-solving approach. You have some excellent insights!",
        "Your understanding of the fundamentals is solid. Let's test the application skills.",
        "I've noticed you excel in certain areas. Here are my recommendations for next steps.",
        "This evaluation shows you've mastered the core concepts. Let's identify advanced topics.",
        "Great work on this assessment! You have a strong grasp of the material.",
        "Your creative approach to problem-solving is noteworthy. Let's discuss your results.",
    ],
    "general": [
        "That's an interesting point. How does that relate to what we're learning?",
        "I see where you're coming from. Let's explore that idea further.",
        "Great observation! This connects to several important concepts we'll cover.",
        "That's a common question. Let me provide some clarity on this topic.",
        "I appreciate you bringing this up. It shows you're thinking deeply about the material.",
        "This touches on an important principle. Allow me to elaborate.",
        "Your curiosity is leading us to some valuable insights. Let's investigate.",
        "That's a nuanced question that deserves a thoughtful response.",
        "This relates to best practices in the field. Here's what I recommend.",
        "Excellent engagement with the material! Let me build on your understanding.",
    ]
}


def get_random_response(context: str) -> str:
    """Get a random response appropriate for the given conversation context.

    Args:
        context: The conversation context (e.g., "planning", "teaching",
                "evaluation", or "general").

    Returns:
        A randomly selected response string appropriate for the context.

    Raises:
        ValueError: If the provided context is not recognized.
    """
    context_lower = context.lower()
    if context_lower not in RESPONSES:
        raise ValueError(f"Unknown conversation context: {context}. "
                        f"Available contexts: {', '.join(RESPONSES.keys())}")

    return random.choice(RESPONSES[context_lower])


def get_greeting(context: str) -> str:
    """Get a context-appropriate greeting message.

    Args:
        context: The conversation context.

    Returns:
        A welcoming message for starting the conversation.
    """
    greetings = {
        "planning": "Ready to craft your personalized learning plan! What are your goals?",
        "teaching": "Let's dive into learning with hands-on examples. What would you like to start with?",
        "evaluation": "Time to assess your progress and identify strengths. How do you feel about your learning so far?",
    }
    return greetings.get(context.lower(), "Hello! I'm ready to help. What would you like to discuss?")
