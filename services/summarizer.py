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

    # Format the controls into a readable list
    formatted_controls = "\n".join([
        f"- [{c['framework']}] {c['control_id']} - {c['name']}: {c['description']}"
        for c in control_list
    ])

    # Explicit and safe prompt
    prompt = f"""
You are a cybersecurity compliance assistant tasked with summarizing semantically similar security controls.

Using the following list of security controls, generate a unified title, a concise 2–3 sentence description, and 2–3 implementation steps in strict JSON format.

### Input Controls ###
{formatted_controls}

### Output Format ###
Respond with ONLY a valid JSON object like this:

{{
  "title": "Short but meaningful unified control title",
  "description": "2–3 sentence unified summary combining all control goals",
  "implementation_steps": [
    {{
      "step": "Step Title 1",
      "description": "What should be done and why"
    }},
    {{
      "step": "Step Title 2",
      "description": "Action with clarity and value"
    }}
  ]
}}

DO NOT include explanations, markdown, or text outside the JSON object.
Make sure it is valid JSON.
"""

    try:
        response = ollama.generate(
            model="llama2",
            prompt=prompt,
            options={"temperature": 0.4}
        )

        raw_output = response["response"].strip()

        # Extract JSON content only
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
        print("Error during summarization:", str(e))
        print("LLM Response:", response.get("response", "No response"))
        return {
            "title": "Error generating title",
            "description": f"Error: {str(e)}",
            "implementation_steps": []
        }
