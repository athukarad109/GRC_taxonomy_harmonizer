from typing import Dict, List, Optional
import json
from ollama import Client

ollama = Client(host='http://localhost:11434')

# Enhanced Framework database with additional metadata
FRAMEWORKS_DATABASE = {
    "NIST 800-53": {
        "name": "NIST Cybersecurity Framework",
        "description": "Comprehensive cybersecurity framework for federal agencies and critical infrastructure",
        "complexity": "high",
        "cost": "medium",
        "implementation_time": "6months-1year",
        "best_for": ["enterprise", "government", "critical_infrastructure"],
        "compliance_mappings": ["FISMA", "FedRAMP"],
        "controls_count": 1000,
        "industry_focus": ["government", "defense", "energy", "finance"],
        "data_types": ["PII", "PHI", "CUI", "Classified"],
        "infrastructure_support": ["on-premise", "cloud", "hybrid"],
        "customer_types": ["B2B", "B2G", "B2C"],
        "revenue_brackets": ["$10M+", "$100M+", "$1B+"]
    },
    "ISO 27001": {
        "name": "ISO/IEC 27001 Information Security Management",
        "description": "International standard for information security management systems",
        "complexity": "high",
        "cost": "high",
        "implementation_time": "6months-1year",
        "best_for": ["enterprise", "large", "medium"],
        "compliance_mappings": ["GDPR", "SOX"],
        "controls_count": 114,
        "industry_focus": ["technology", "finance", "healthcare", "manufacturing"],
        "data_types": ["PII", "PHI", "Financial", "Intellectual Property"],
        "infrastructure_support": ["on-premise", "cloud", "hybrid"],
        "customer_types": ["B2B", "B2C"],
        "revenue_brackets": ["$1M+", "$10M+", "$100M+"]
    },
    "SOC 2": {
        "name": "System and Organization Controls 2",
        "description": "Trust service criteria for security, availability, processing integrity, confidentiality, and privacy",
        "complexity": "medium",
        "cost": "medium",
        "implementation_time": "3months-6months",
        "best_for": ["medium", "large", "enterprise"],
        "compliance_mappings": ["SOX", "GDPR"],
        "controls_count": 200,
        "industry_focus": ["technology", "finance", "healthcare", "retail"],
        "data_types": ["PII", "PHI", "Financial", "Customer Data"],
        "infrastructure_support": ["cloud", "hybrid"],
        "customer_types": ["B2B", "B2C"],
        "revenue_brackets": ["$1M+", "$10M+", "$100M+"]
    },
    "PCI DSS": {
        "name": "Payment Card Industry Data Security Standard",
        "description": "Security standard for organizations handling credit card data",
        "complexity": "medium",
        "cost": "medium",
        "implementation_time": "3months-6months",
        "best_for": ["small", "medium", "large"],
        "compliance_mappings": ["SOX"],
        "controls_count": 78,
        "industry_focus": ["finance", "retail", "ecommerce"],
        "data_types": ["Payment Card Data", "PII"],
        "infrastructure_support": ["on-premise", "cloud", "hybrid"],
        "customer_types": ["B2B", "B2C"],
        "revenue_brackets": ["$100K+", "$1M+", "$10M+"]
    },
    "HIPAA": {
        "name": "Health Insurance Portability and Accountability Act",
        "description": "Security and privacy standards for healthcare organizations",
        "complexity": "medium",
        "cost": "medium",
        "implementation_time": "3months-6months",
        "best_for": ["small", "medium", "large"],
        "compliance_mappings": ["HITECH"],
        "controls_count": 45,
        "industry_focus": ["healthcare", "medical", "pharmaceutical"],
        "data_types": ["PHI", "PII"],
        "infrastructure_support": ["on-premise", "cloud", "hybrid"],
        "customer_types": ["B2B", "B2C"],
        "revenue_brackets": ["$100K+", "$1M+", "$10M+"]
    },
    "GDPR": {
        "name": "General Data Protection Regulation",
        "description": "EU regulation for data protection and privacy",
        "complexity": "medium",
        "cost": "medium",
        "implementation_time": "3months-6months",
        "best_for": ["medium", "large", "enterprise"],
        "compliance_mappings": ["CCPA", "LGPD"],
        "controls_count": 99,
        "industry_focus": ["technology", "finance", "retail", "healthcare"],
        "data_types": ["PII", "Personal Data"],
        "infrastructure_support": ["on-premise", "cloud", "hybrid"],
        "customer_types": ["B2B", "B2C"],
        "revenue_brackets": ["$1M+", "$10M+", "$100M+"],
        "geographic_focus": ["EU", "Global"]
    },
    "CIS Controls": {
        "name": "Center for Internet Security Controls",
        "description": "Prioritized cybersecurity best practices and controls",
        "complexity": "low",
        "cost": "low",
        "implementation_time": "1month-3months",
        "best_for": ["startup", "small", "medium"],
        "compliance_mappings": ["NIST", "ISO27001"],
        "controls_count": 153,
        "industry_focus": ["technology", "finance", "healthcare", "manufacturing"],
        "data_types": ["PII", "PHI", "Business Data"],
        "infrastructure_support": ["on-premise", "cloud", "hybrid"],
        "customer_types": ["B2B", "B2C"],
        "revenue_brackets": ["$100K+", "$1M+", "$10M+"]
    },
    "COBIT": {
        "name": "Control Objectives for Information and Related Technologies",
        "description": "IT governance framework for enterprise IT management",
        "complexity": "high",
        "cost": "high",
        "implementation_time": "6months-1year",
        "best_for": ["large", "enterprise"],
        "compliance_mappings": ["SOX", "ISO27001"],
        "controls_count": 40,
        "industry_focus": ["finance", "technology", "manufacturing"],
        "data_types": ["PII", "Financial", "Intellectual Property"],
        "infrastructure_support": ["on-premise", "hybrid"],
        "customer_types": ["B2B"],
        "revenue_brackets": ["$10M+", "$100M+", "$1B+"]
    }
}

def _calculate_framework_score(framework: str, org_data: Dict) -> float:
    """Calculate a suitability score for a framework based on enhanced organization data"""
    framework_info = FRAMEWORKS_DATABASE[framework]
    score = 0.0
    
    # Skip if organization already has this framework
    existing_frameworks = org_data.get("existing_frameworks", [])
    if framework in existing_frameworks:
        return 0.0  # Don't recommend frameworks they already have
    
    # Company size matching
    size_mapping = {
        "startup": ["CIS Controls"],
        "small": ["CIS Controls", "PCI DSS", "HIPAA"],
        "medium": ["SOC 2", "PCI DSS", "HIPAA", "GDPR", "ISO 27001"],
        "large": ["SOC 2", "ISO 27001", "NIST 800-53", "COBIT"],
        "enterprise": ["NIST 800-53", "ISO 27001", "COBIT"]
    }
    
    if org_data["company_size"] in size_mapping:
        if framework in size_mapping[org_data["company_size"]]:
            score += 3.0
    
    # Industry/Business sector matching
    industry = org_data.get("business_sector", org_data.get("industry", "")).lower()
    if industry in [focus.lower() for focus in framework_info["industry_focus"]]:
        score += 2.0
    
    # Bonus points for organizations with existing frameworks (shows maturity)
    if existing_frameworks:
        score += 0.5  # Small bonus for organizations that already have some compliance
    
    # Risk profile matching
    risk_complexity_mapping = {
        "low": ["CIS Controls"],
        "medium": ["SOC 2", "PCI DSS", "HIPAA", "GDPR"],
        "high": ["ISO 27001", "NIST 800-53"],
        "critical": ["NIST 800-53", "COBIT"]
    }
    
    if org_data["risk_profile"] in risk_complexity_mapping:
        if framework in risk_complexity_mapping[org_data["risk_profile"]]:
            score += 1.5
    
    # Budget constraints
    budget_complexity_mapping = {
        "low": ["CIS Controls"],
        "medium": ["SOC 2", "PCI DSS", "HIPAA", "GDPR"],
        "high": ["ISO 27001", "NIST 800-53", "COBIT"]
    }
    
    if org_data.get("budget_constraints") in budget_complexity_mapping:
        if framework in budget_complexity_mapping[org_data["budget_constraints"]]:
            score += 1.0
    
    # Implementation timeline
    timeline_mapping = {
        "immediate": ["CIS Controls"],
        "3months": ["SOC 2", "PCI DSS", "HIPAA"],
        "6months": ["ISO 27001", "GDPR"],
        "1year": ["NIST 800-53", "COBIT"]
    }
    
    if org_data.get("implementation_timeline") in timeline_mapping:
        if framework in timeline_mapping[org_data["implementation_timeline"]]:
            score += 1.0
    
    # Data types matching
    if org_data.get("data_types"):
        for data_type in org_data["data_types"]:
            if data_type.upper() in [dt.upper() for dt in framework_info["data_types"]]:
                score += 1.5
    
    # Infrastructure matching
    if org_data.get("infrastructure"):
        infrastructure = org_data["infrastructure"].lower()
        if infrastructure in [inf.lower() for inf in framework_info["infrastructure_support"]]:
            score += 1.0
    
    # Customer type matching
    if org_data.get("customer_type"):
        customer_type = org_data["customer_type"].upper()
        if customer_type in [ct.upper() for ct in framework_info["customer_types"]]:
            score += 1.0
    
    # Revenue bracket matching
    if org_data.get("revenue_bracket"):
        revenue = org_data["revenue_bracket"]
        if revenue in framework_info["revenue_brackets"]:
            score += 1.0
    
    # Geographic considerations
    if org_data.get("customer_locations") or org_data.get("business_locations"):
        locations = []
        if org_data.get("customer_locations"):
            locations.extend(org_data["customer_locations"])
        if org_data.get("business_locations"):
            locations.extend(org_data["business_locations"])
        
        # GDPR consideration for EU presence
        if any("EU" in loc.upper() or "EUROPE" in loc.upper() for loc in locations):
            if "GDPR" in framework:
                score += 1.5
        
        # Global presence considerations
        if len(locations) > 3:  # Multi-regional
            if framework in ["ISO 27001", "SOC 2"]:
                score += 1.0
    
    return score

def _determine_mandatory_status(framework: str, org_data: Dict) -> str:
    """Determine if a framework is mandatory or recommended based on organization data"""
    
    # Check if organization already has this framework
    existing_frameworks = org_data.get("existing_frameworks", [])
    if framework in existing_frameworks:
        return "already_implemented"  # They already have this framework
    
    # Mandatory frameworks based on industry and data types
    industry = org_data.get("business_sector", "").lower()
    data_types = org_data.get("data_types", [])
    
    # Industry-specific mandatory requirements
    if industry == "healthcare" and framework == "HIPAA":
        return "mandatory"
    if industry == "finance" and framework == "PCI DSS":
        return "mandatory"
    if industry == "government" and framework == "NIST 800-53":
        return "mandatory"
    
    # Data type specific mandatory requirements
    if "PHI" in data_types and framework == "HIPAA":
        return "mandatory"
    if "Payment Card Data" in data_types and framework == "PCI DSS":
        return "mandatory"
    
    # Geographic mandatory requirements
    if org_data.get("customer_locations") or org_data.get("business_locations"):
        locations = []
        if org_data.get("customer_locations"):
            locations.extend(org_data["customer_locations"])
        if org_data.get("business_locations"):
            locations.extend(org_data["business_locations"])
        
        # GDPR is mandatory for EU presence
        if any("EU" in loc.upper() or "EUROPE" in loc.upper() for loc in locations):
            if framework == "GDPR":
                return "mandatory"
    
    # Industry-specific mandatory requirements
    industry = org_data.get("business_sector", "").lower()
    if industry == "healthcare" and framework == "HIPAA":
        return "mandatory"
    if industry == "finance" and framework == "PCI DSS":
        return "mandatory"
    if industry == "government" and framework == "NIST 800-53":
        return "mandatory"
    
    return "recommended"

def _generate_justification(framework: str, org_data: Dict, status: str) -> str:
    """Generate justification for why a framework is required"""
    framework_info = FRAMEWORKS_DATABASE[framework]
    justifications = []
    
    # Check if organization already has this framework
    existing_frameworks = org_data.get("existing_frameworks", [])
    if framework in existing_frameworks:
        return "Already implemented by the organization"
    
    # Industry and data type based justification
    industry = org_data.get("business_sector", "").lower()
    data_types = org_data.get("data_types", [])
    
    # Industry-specific justification
    if industry == "healthcare" and framework == "HIPAA":
        justifications.append("Mandatory for healthcare organizations handling patient data")
    elif industry == "finance" and framework == "PCI DSS":
        justifications.append("Required for organizations processing payment card data")
    elif industry == "government" and framework == "NIST 800-53":
        justifications.append("Mandatory for federal government contractors and agencies")
    
    # Data type specific justification
    if "PHI" in data_types and framework == "HIPAA":
        justifications.append("Required for handling Protected Health Information")
    elif "Payment Card Data" in data_types and framework == "PCI DSS":
        justifications.append("Required for processing payment card data")
    
    # Geographic justification
    if org_data.get("customer_locations") or org_data.get("business_locations"):
        locations = []
        if org_data.get("customer_locations"):
            locations.extend(org_data["customer_locations"])
        if org_data.get("business_locations"):
            locations.extend(org_data["business_locations"])
        
        if any("EU" in loc.upper() or "EUROPE" in loc.upper() for loc in locations):
            if framework == "GDPR":
                justifications.append("Mandatory for EU data processing activities")
    
    # Industry-specific justification
    industry = org_data.get("business_sector", "").lower()
    if industry == "healthcare" and framework == "HIPAA":
        justifications.append("Mandatory for healthcare organizations handling patient data")
    elif industry == "finance" and framework == "PCI DSS":
        justifications.append("Required for organizations processing payment card data")
    elif industry == "government" and framework == "NIST 800-53":
        justifications.append("Mandatory for federal government contractors and agencies")
    
    # Data type justification
    if org_data.get("data_types"):
        for data_type in org_data["data_types"]:
            if data_type.upper() in [dt.upper() for dt in framework_info["data_types"]]:
                if data_type == "PHI" and framework == "HIPAA":
                    justifications.append("Required for handling Protected Health Information")
                elif data_type == "Payment Card Data" and framework == "PCI DSS":
                    justifications.append("Required for processing payment card data")
                elif data_type == "PII" and framework == "GDPR":
                    justifications.append("Required for EU personal data processing")
    
    # Size and complexity justification
    if org_data["company_size"] in ["large", "enterprise"] and framework in ["NIST 800-53", "ISO 27001", "COBIT"]:
        justifications.append("Appropriate for large enterprise security requirements")
    elif org_data["company_size"] in ["startup", "small"] and framework == "CIS Controls":
        justifications.append("Best practice framework for smaller organizations")
    
    # If no specific justifications, provide general one
    if not justifications:
        if status == "mandatory":
            justifications.append(f"Required based on organization characteristics and compliance needs")
        else:
            justifications.append(f"Recommended based on industry best practices and organization profile")
    
    return "; ".join(justifications)

def generate_framework_recommendation(org_data: Dict) -> Dict:
    """Generate simplified framework recommendations with mandatory/recommended status and justification"""
    
    # Calculate scores for all frameworks
    framework_scores = {}
    for framework in FRAMEWORKS_DATABASE.keys():
        score = _calculate_framework_score(framework, org_data)
        framework_scores[framework] = score
    
    # Sort frameworks by score
    sorted_frameworks = sorted(framework_scores.items(), key=lambda x: x[1], reverse=True)
    
    # Select top frameworks (score > 0)
    top_frameworks = [(fw, score) for fw, score in sorted_frameworks if score > 0][:5]
    
    # Generate recommendations
    recommendations = []
    for framework, score in top_frameworks:
        status = _determine_mandatory_status(framework, org_data)
        justification = _generate_justification(framework, org_data, status)
        
        # Only include frameworks that are not already implemented
        if status != "already_implemented":
            recommendations.append({
                "framework": framework,
                "status": status,  # "mandatory" or "recommended"
                "justification": justification
            })
    
    # Compile final recommendation
    recommendation = {
        "organization_profile": {
            "business_sector": org_data.get("business_sector", org_data.get("industry")),
            "company_size": org_data["company_size"],
            "revenue_bracket": org_data.get("revenue_bracket"),
            "business_locations": org_data.get("business_locations"),
            "customer_locations": org_data.get("customer_locations"),
            "data_types": org_data.get("data_types"),
            "infrastructure": org_data.get("infrastructure"),
            "customer_type": org_data.get("customer_type"),
            "existing_frameworks": org_data.get("existing_frameworks", []),
            "risk_profile": org_data["risk_profile"],
            "budget_constraints": org_data.get("budget_constraints"),
            "implementation_timeline": org_data.get("implementation_timeline"),
            "technical_maturity": org_data.get("technical_maturity")
        },
        "recommended_frameworks": recommendations
    }
    
    return recommendation 