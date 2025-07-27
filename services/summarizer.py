from ollama import Client
import json
import re
from typing import Optional, Dict

ollama = Client(host='http://localhost:11434')

def _extract_json_from_text(text: str) -> Optional[Dict]:
    """Extract JSON from LLM response with multiple fallback strategies"""
    if not text:
        return None
    
    # Strategy 1: Find JSON object with braces
    json_pattern = r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}'
    matches = re.findall(json_pattern, text, re.DOTALL)
    
    for match in matches:
        try:
            return json.loads(match)
        except json.JSONDecodeError:
            continue
    
    # Strategy 2: Find anything between curly braces
    start = text.find('{')
    if start != -1:
        # Find matching closing brace
        brace_count = 0
        end = start
        for i, char in enumerate(text[start:], start):
            if char == '{':
                brace_count += 1
            elif char == '}':
                brace_count -= 1
                if brace_count == 0:
                    end = i + 1
                    break
        
        if end > start:
            try:
                return json.loads(text[start:end])
            except json.JSONDecodeError:
                pass
    
    # Strategy 3: Try to fix common JSON issues
    # Remove markdown code blocks
    cleaned_text = re.sub(r'```json\s*', '', text)
    cleaned_text = re.sub(r'```\s*', '', cleaned_text)
    
    # Find JSON in cleaned text
    start = cleaned_text.find('{')
    if start != -1:
        try:
            return json.loads(cleaned_text[start:])
        except json.JSONDecodeError:
            pass
    
    return None

def _generate_fallback_summary(control_list, org_context: Optional[Dict] = None) -> Dict:
    """Generate a fallback summary when LLM fails"""
    if not control_list:
        return {
            "title": "No Controls Provided",
            "description": "The list of controls was empty.",
            "implementation_steps": []
        }
    
    # Simple heuristic-based summary
    frameworks = list(set(c['framework'] for c in control_list))
    names = [c['name'] for c in control_list]
    
    # Create a meaningful title
    if len(control_list) == 1:
        title = f"{names[0]} Implementation"
    else:
        # Find common keywords in names
        common_words = []
        for name in names:
            words = name.lower().split()
            common_words.extend(words)
        
        # Get most common meaningful words
        from collections import Counter
        word_counts = Counter(common_words)
        # Filter out common words
        stop_words = {'and', 'the', 'for', 'with', 'to', 'in', 'of', 'a', 'an', 'is', 'are', 'be', 'by'}
        meaningful_words = [word for word, count in word_counts.most_common(3) 
                          if word not in stop_words and len(word) > 2]
        
        if meaningful_words:
            title = f"{' '.join(meaningful_words).title()} Controls"
        else:
            title = f"Security Controls ({len(control_list)} items)"
    
    # Create description
    if org_context and org_context.get("industry"):
        industry = org_context["industry"]
        description = f"Implementation of {len(control_list)} security controls from {', '.join(frameworks)} frameworks, tailored for {industry} industry requirements."
    else:
        description = f"Implementation of {len(control_list)} security controls from {', '.join(frameworks)} frameworks to enhance overall security posture."
    
    # Generate basic implementation steps
    implementation_steps = []
    if len(control_list) > 0:
        implementation_steps.append({
            "step": "Review Control Requirements",
            "description": f"Analyze the {len(control_list)} controls to understand specific requirements and dependencies"
        })
        implementation_steps.append({
            "step": "Implement Controls",
            "description": "Deploy the controls according to framework-specific guidelines and best practices"
        })
        implementation_steps.append({
            "step": "Validate Implementation",
            "description": "Test and verify that all controls are properly implemented and functioning as expected"
        })
    
    return {
        "title": title,
        "description": description,
        "implementation_steps": implementation_steps
    }

def summarize_controls(control_list, org_context: Optional[Dict] = None):
    if not control_list:
        return {
            "title": "No Controls Provided",
            "description": "The list of controls was empty.",
            "implementation_steps": []
        }

    # OPTIMIZED: Shorter, more focused prompt
    # Only include essential info: framework, name, and key parts of description
    formatted_controls = "\n".join([
        f"- {c['framework']}: {c['name']} - {c['description'][:200]}{'...' if len(c['description']) > 200 else ''}"
        for c in control_list
    ])

    # Build context-aware prompt with stronger JSON formatting instructions
    prompt = f"""You are a cybersecurity expert. Summarize these security controls into a unified format.

Controls:
{formatted_controls}"""

    # Add organization context if provided
    if org_context:
        industry = org_context.get("industry", "")
        existing_count = len(org_context.get("existing_controls", []))
        risk_profile = org_context.get("risk_profile", "Standard")
        compliance_frameworks = org_context.get("compliance_frameworks", [])
        
        context_info = f"""

Organization Context:
- Industry: {industry}
- Existing controls: {existing_count}
- Risk profile: {risk_profile}
- Compliance frameworks: {', '.join(compliance_frameworks) if compliance_frameworks else 'None specified'}

Please tailor the implementation steps to be relevant for {industry} industry and consider the existing control landscape.
"""
        prompt += context_info

    prompt += """

IMPORTANT: Respond with ONLY valid JSON, no other text.

{
  "title": "Unified control title",
  "description": "2-3 sentence summary",
  "implementation_steps": [
    {"step": "Step 1", "description": "Action"},
    {"step": "Step 2", "description": "Action"}
  ]
}"""

    try:
        response = ollama.generate(
            model="llama2",
            prompt=prompt,
            options={"temperature": 0.2}  # Even lower temperature for more consistent JSON
        )

        raw_output = response["response"].strip()
        print(f"LLM Raw Response: {raw_output[:200]}...")  # Debug log

        # Try to extract JSON with multiple strategies
        parsed = _extract_json_from_text(raw_output)
        
        if parsed:
            return {
                "title": parsed.get("title", "Untitled"),
                "description": parsed.get("description", ""),
                "implementation_steps": parsed.get("implementation_steps", [])
            }
        else:
            # Fallback to heuristic-based summary
            print("LLM failed to return valid JSON, using fallback summary")
            return _generate_fallback_summary(control_list, org_context)

    except Exception as e:
        print(f"Error during summarization: {str(e)}")
        print(f"LLM Response: {response.get('response', 'No response')[:200]}...")
        
        # Return fallback summary
        return _generate_fallback_summary(control_list, org_context)
