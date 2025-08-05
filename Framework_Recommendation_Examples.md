# Framework Recommendation System

This document provides comprehensive examples and usage guidelines for the Framework Recommendation API.

## Overview

The Framework Recommendation System analyzes organization characteristics and provides tailored cybersecurity framework recommendations with implementation roadmaps.

## API Endpoint

```
POST /framework-recommendation
```

## Request Model

```json
{
  // Core organization information
  "business_sector": "string",             // Required: Primary business sector/industry
  "company_size": "string",                // Required: "startup", "small", "medium", "large", "enterprise"
  "revenue_bracket": "string",             // Optional: "$100K+", "$1M+", "$10M+", "$100M+", "$1B+"
  
  // Geographic information
  "business_locations": ["string"],        // Optional: ["US", "EU", "Asia", "Global"]
  "customer_locations": ["string"],        // Optional: ["US", "EU", "Asia", "Global"]
  
  // Data and infrastructure
  "data_types": ["string"],               // Optional: ["PII", "PHI", "Payment Card Data", "Financial", "Intellectual Property"]
  "infrastructure": "string",              // Optional: "on-premise", "cloud", "hybrid"
  "customer_type": "string",               // Optional: "B2B", "B2C", "B2G"
  
  // Existing compliance and risk
  "existing_frameworks": ["string"],       // Optional: Currently implemented frameworks
  "risk_profile": "string",                // Optional: "low", "medium", "high", "critical" (default: "medium")
  
  // Implementation constraints
  "budget_constraints": "string",          // Optional: "low", "medium", "high"
  "implementation_timeline": "string",      // Optional: "immediate", "3months", "6months", "1year"
  "technical_maturity": "string",          // Optional: "basic", "intermediate", "advanced"
  "existing_frameworks": ["string"]        // Optional: Currently implemented frameworks
}
```

## Example Requests

### 1. Global FinTech Startup (No Existing Frameworks)

```json
{
  "business_sector": "finance",
  "company_size": "startup",
  "revenue_bracket": "$1M+",
  "business_locations": ["US", "EU"],
  "customer_locations": ["US", "EU", "Asia"],
  "data_types": ["PII", "Payment Card Data", "Financial"],
  "infrastructure": "cloud",
  "customer_type": "B2C",
  "existing_frameworks": [],
  "risk_profile": "medium",
  "budget_constraints": "low",
  "implementation_timeline": "immediate",
  "technical_maturity": "basic"
}
```

### 2. Healthcare Enterprise with Existing Frameworks

```json
{
  "business_sector": "healthcare",
  "company_size": "enterprise",
  "revenue_bracket": "$1B+",
  "business_locations": ["US", "EU", "Asia", "Australia"],
  "customer_locations": ["US", "EU", "Asia", "Australia", "Canada"],
  "data_types": ["PHI", "PII", "Financial"],
  "infrastructure": "hybrid",
  "customer_type": "B2B",
  "existing_frameworks": ["HIPAA", "SOC 2", "ISO 27001"],
  "risk_profile": "critical",
  "budget_constraints": "high",
  "implementation_timeline": "1year",
  "technical_maturity": "advanced"
}
```

### 3. SaaS Technology Company with Existing SOC 2

```json
{
  "business_sector": "technology",
  "company_size": "medium",
  "revenue_bracket": "$10M+",
  "business_locations": ["US"],
  "customer_locations": ["US", "EU", "Asia", "Global"],
  "data_types": ["PII", "Customer Data", "Intellectual Property"],
  "infrastructure": "cloud",
  "customer_type": "B2B",
  "existing_frameworks": ["SOC 2"],
  "risk_profile": "medium",
  "budget_constraints": "medium",
  "implementation_timeline": "6months",
  "technical_maturity": "intermediate"
}
```

## Response Structure

```json
{
  "recommendation": {
    "organization_profile": {
      "business_sector": "string",
      "company_size": "string",
      "revenue_bracket": "string",
      "business_locations": ["string"],
      "customer_locations": ["string"],
      "data_types": ["string"],
      "infrastructure": "string",
      "customer_type": "string",
      "compliance_requirements": ["string"],
      "risk_profile": "string",
      "budget_constraints": "string",
      "implementation_timeline": "string",
      "technical_maturity": "string"
    },
    "recommended_frameworks": [
      {
        "framework": "string",
        "status": "string",  // "mandatory" or "recommended"
        "justification": "string"
      }
    ]
  },
  "performance": {
    "processing_time_seconds": "float",
    "organization_analyzed": "boolean"
  }
}
```

## Supported Frameworks

| Framework | Complexity | Cost | Best For | Implementation Time | Data Types | Infrastructure |
|-----------|------------|------|----------|-------------------|------------|----------------|
| CIS Controls | Low | Low | Startups, Small | 1-3 months | PII, PHI, Business Data | All |
| PCI DSS | Medium | Medium | Small, Medium | 3-6 months | Payment Card Data, PII | All |
| HIPAA | Medium | Medium | Small, Medium | 3-6 months | PHI, PII | All |
| SOC 2 | Medium | Medium | Medium, Large | 3-6 months | PII, PHI, Financial, Customer Data | Cloud, Hybrid |
| GDPR | Medium | Medium | Medium, Large | 3-6 months | PII, Personal Data | All |
| ISO 27001 | High | High | Large, Enterprise | 6-12 months | PII, PHI, Financial, IP | All |
| NIST 800-53 | High | Medium | Enterprise, Government | 6-12 months | PII, PHI, CUI, Classified | On-premise, Hybrid |
| COBIT | High | High | Large, Enterprise | 6-12 months | PII, Financial, IP | On-premise, Hybrid |

## Enhanced Framework Recommendations

### Data Type-Driven Recommendations
- **PHI Data**: HIPAA + SOC 2 + ISO 27001
- **Payment Card Data**: PCI DSS + SOC 2
- **PII Data**: GDPR + SOC 2 + ISO 27001
- **Financial Data**: SOX + ISO 27001 + COBIT
- **Intellectual Property**: ISO 27001 + NIST 800-53

### Infrastructure-Driven Recommendations
- **Cloud-First**: SOC 2 + GDPR + ISO 27001
- **On-Premise**: NIST 800-53 + COBIT + ISO 27001
- **Hybrid**: ISO 27001 + SOC 2 + NIST 800-53

### Geographic-Driven Recommendations
- **EU Presence**: GDPR + ISO 27001 + SOC 2
- **Global Presence**: ISO 27001 + SOC 2 + GDPR
- **US Government**: NIST 800-53 + FISMA + FedRAMP

### Customer Type-Driven Recommendations
- **B2C**: GDPR + SOC 2 + PCI DSS
- **B2B**: SOC 2 + ISO 27001 + COBIT
- **B2G**: NIST 800-53 + FISMA + FedRAMP

### Revenue-Driven Recommendations
- **$100K-$1M**: CIS Controls + PCI DSS
- **$1M-$10M**: SOC 2 + PCI DSS + GDPR
- **$10M-$100M**: ISO 27001 + SOC 2 + COBIT
- **$100M+**: NIST 800-53 + ISO 27001 + COBIT

## Implementation Roadmap Phases

### Phase 1: Foundation (1-3 months)
- Security assessment and gap analysis
- Establish security policies and procedures
- Implement basic security controls
- Train staff on security awareness

### Phase 2: Framework Implementation (3-6 months)
- Deploy framework-specific controls
- Establish monitoring and logging
- Conduct internal audits
- Document processes and procedures

### Phase 3: Maturity and Optimization (6-12 months)
- Continuous monitoring and improvement
- External audits and certifications
- Advanced security controls
- Integration with business processes

## Usage Examples

### cURL Example

```bash
curl -X POST "http://localhost:8000/framework-recommendation" \
  -H "Content-Type: application/json" \
  -d '{
    "business_sector": "finance",
    "company_size": "medium",
    "revenue_bracket": "$10M+",
    "business_locations": ["US", "EU"],
    "customer_locations": ["US", "EU", "Asia"],
    "data_types": ["PII", "Payment Card Data", "Financial"],
    "infrastructure": "cloud",
    "customer_type": "B2C",
    "compliance_requirements": ["PCI", "SOC2", "GDPR"],
    "risk_profile": "medium",
    "budget_constraints": "medium",
    "implementation_timeline": "6months"
  }'
```

### Python Example

```python
import requests

url = "http://localhost:8000/framework-recommendation"
data = {
    "business_sector": "healthcare",
    "company_size": "large",
    "revenue_bracket": "$100M+",
    "business_locations": ["US", "EU"],
    "customer_locations": ["US", "EU", "Asia"],
    "data_types": ["PHI", "PII", "Financial"],
    "infrastructure": "hybrid",
    "customer_type": "B2B",
    "compliance_requirements": ["HIPAA", "SOC2", "ISO27001", "GDPR"],
    "risk_profile": "high",
    "budget_constraints": "high",
    "implementation_timeline": "1year"
}

response = requests.post(url, json=data)
recommendation = response.json()
print(recommendation)
```

## Best Practices

1. **Provide Complete Information**: Include all relevant organization characteristics for better recommendations
2. **Consider Budget Constraints**: Be realistic about budget limitations
3. **Plan Implementation Timeline**: Consider organizational capacity for change
4. **Assess Technical Maturity**: Evaluate current security posture
5. **Review Compliance Requirements**: Ensure all regulatory needs are captured

## Error Handling

The API returns appropriate HTTP status codes:
- `200`: Successful recommendation generated
- `400`: Invalid request data
- `500`: Internal server error

## Performance Considerations

- Processing time typically under 5 seconds
- LLM-based recommendations may take longer for complex scenarios
- Cache results for repeated queries with similar parameters 