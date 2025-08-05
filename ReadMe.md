# Taxonomy Harmonizer - Compliance Framework Recommendation System

A comprehensive system that provides intelligent cybersecurity framework recommendations and control harmonization.

## Core Features

### 1. Framework Recommendation Engine
- **Organization Analysis**: Analyzes company characteristics (industry, size, compliance needs, risk profile)
- **Intelligent Matching**: Scores frameworks based on organization profile
- **Implementation Roadmap**: Provides phased implementation guidance
- **LLM-Powered Insights**: Detailed recommendations with challenges and mitigation strategies

### 2. Control Harmonization Engine
Given a list of cybersecurity controls (from multiple frameworks), the system:

- Groups similar controls by semantic meaning
- Merges them into unified versions (with new description + implementation steps)
- Outputs structured, machine-usable lists

## System Architecture

```
[Organization Data Input]
        ->
[Framework Recommendation Engine]
        ->
[Recommended Frameworks]
        ->
[Control Harmonization Engine]
        ->
[Unified Controls + Implementation Plan]
```

## API Endpoints

### Framework Recommendation
```
POST /framework-recommendation
```
Takes organization profile and returns tailored framework recommendations.

### Control Harmonization
```
POST /batch-harmonize
POST /harmonize
```
Harmonizes controls from multiple frameworks into unified versions.

## Supported Frameworks

- **NIST 800-53**: Federal agencies, critical infrastructure
- **ISO 27001**: International information security standard
- **SOC 2**: Trust service criteria for security and privacy
- **PCI DSS**: Payment card industry security standard
- **HIPAA**: Healthcare security and privacy standards
- **GDPR**: EU data protection regulation
- **CIS Controls**: Prioritized cybersecurity best practices
- **COBIT**: IT governance framework

## Quick Start

1. **Framework Recommendation**:
   ```bash
   curl -X POST "http://localhost:8000/framework-recommendation" \
     -H "Content-Type: application/json" \
     -d '{
       "industry": "finance",
       "company_size": "medium",
       "compliance_requirements": ["PCI", "SOC2"],
       "risk_profile": "medium"
     }'
   ```

2. **Control Harmonization**:
   ```bash
   curl -X POST "http://localhost:8000/batch-harmonize" \
     -H "Content-Type: application/json" \
     -d '{
       "controls": [
         {
           "framework": "NIST 800-53",
           "control_id": "AC-2",
           "name": "Account Management",
           "description": "The organization manages information system accounts"
         }
       ]
     }'
   ```

## Documentation

- [Framework Recommendation Examples](Framework_Recommendation_Examples.md)
- [API Examples](API_Examples.md)
