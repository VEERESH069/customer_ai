# modules/gemini_utils.py

import google.generativeai as genai

# Defining the persona and format instructions here
PERSONA_PROMPTS = {
    "Default": "You are a helpful and intelligent assistant.",
    "Expert Analyst": "You are a world-class professional analyst. Your response should be formal, data-driven, and structured. Use bullet points and bold text to highlight key findings.",
    "Creative Brainstormer": "You are a creative partner. Your response should be imaginative and focus on generating new ideas, possibilities, or different angles based on the document's content.",
    "ELI5 (Explain Like I'm 5)": "You are a friendly teacher explaining things to a five-year-old. Your response must be extremely simple, use easy words, and short sentences. Use analogies if possible."
}

FORMAT_PROMPTS = {
    "Default": "Please format your response clearly.",
    "Bullet Points": "Please provide your entire answer as a well-structured bulleted list.",
    "JSON": "Please provide your entire answer as a single, valid JSON object. Do not include any text or formatting outside of the JSON structure.",
    "Short Paragraph": "Please provide your answer as a single, concise paragraph."
}


def get_gemini_response(base_prompt, persona, output_format):
    """
    Sends a request to the Gemini model with persona and format instructions.
    
    Args:
        base_prompt (list): The core prompt parts (question + context).
        persona (str): The key for the selected persona.
        output_format (str): The key for the selected output format.
    
    Returns:
        str: The text response from the model.
    """
    model = genai.GenerativeModel('gemini-1.5-flash-latest')
    
    # Get the specific instructions from our dictionaries
    persona_instruction = PERSONA_PROMPTS.get(persona, PERSONA_PROMPTS["Default"])
    format_instruction = FORMAT_PROMPTS.get(output_format, FORMAT_PROMPTS["Default"])
    
    # Construct the final prompt with all instructions
    final_prompt = [
        f"**Agent Instructions**\n"
        f"Persona: {persona_instruction}\n"
        f"Output Format: {format_instruction}\n\n"
        f"--------------------\n\n"
    ]
    final_prompt.extend(base_prompt) # Add the user question and context
    
    try:
        response = model.generate_content(final_prompt)
        return response.text
    except Exception as e:
        return f"Error communicating with Gemini API: {e}"

