from ollama import Client
import json

ollama = Client(host='http://localhost:11434')

def summarize_controls(control_list):
    if not control_list:
        return {
            "title": "No Controls Provided",
            "description": "The list of controls was empty.",
            "implementation_steps": []
        }

    formatted_controls = "\n".join([
        f"- [{c['framework']}] {c['control_id']} - {c['name']}: {c['description']}"
        for c in control_list
    ])

    format_instructions = """
{
  "title": "A short meaningful title combining all control intents",
  "description": "2-3 sentence unified description combining all control goals",
  "implementation_steps": [
    {
      "step": "Step Title 1",
      "description": "What should be done and why"
    },
    {
      "step": "Step Title 2",
      "description": "Action with clarity and value"
    }
  ]
}
"""

    prompt = f"""
You are a cybersecurity compliance assistant.

Your task is to merge the following semantically similar controls into one unified control, with a clear and professional title, summary description, and actionable implementation steps.

Here are the controls:
{formatted_controls}

Respond ONLY in this JSON format:
{format_instructions}
"""

    try:
        response = ollama.generate(
            model="llama2",
            prompt=prompt,
            options={"temperature": 0.4}
        )

        raw_output = response["response"].strip()
        start = raw_output.find("{")
        if start == -1:
            raise ValueError("No JSON object found in response.")
        json_text = raw_output[start:]

        parsed = json.loads(json_text)
        return {
            "title": parsed.get("title", "Untitled"),
            "description": parsed.get("description", ""),
            "implementation_steps": parsed.get("implementation_steps", [])
        }

    except Exception as e:
        print("🛑 Error during summarization:", str(e))
        print("🧠 LLM Response:", response["response"][:300] if "response" in locals() else "No response")
        return {
            "title": "Error generating title",
            "description": f"Error: {str(e)}",
            "implementation_steps": []
        }
