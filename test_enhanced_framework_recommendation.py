#!/usr/bin/env python3
"""
Enhanced test script for the Framework Recommendation System
Demonstrates the simplified framework recommendations
"""

import json
from services.framework_recommender import generate_framework_recommendation

def test_enhanced_framework_recommendation():
    """Test the enhanced framework recommendation system with comprehensive organization profiles"""
    
    # Test Case 1: Global FinTech Startup
    print("=" * 80)
    print("TEST CASE 1: Global FinTech Startup")
    print("=" * 80)
    
    global_fintech = {
        "business_sector": "finance",
        "company_size": "startup",
        "revenue_bracket": "$1M+",
        "business_locations": ["US", "EU"],
        "customer_locations": ["US", "EU", "Asia"],
        "data_types": ["PII", "Payment Card Data", "Financial"],
        "infrastructure": "cloud",
        "customer_type": "B2C",
        "compliance_requirements": ["PCI", "GDPR"],
        "risk_profile": "medium",
        "budget_constraints": "low",
        "implementation_timeline": "immediate",
        "technical_maturity": "basic"
    }
    
    result1 = generate_framework_recommendation(global_fintech)
    print("Recommended Frameworks:")
    for framework in result1["recommended_frameworks"]:
        print(f"- {framework['framework']} ({framework['status'].upper()})")
        print(f"  Justification: {framework['justification']}")
        print()
    
    # Test Case 2: Healthcare Enterprise with Global Presence
    print("=" * 80)
    print("TEST CASE 2: Healthcare Enterprise with Global Presence")
    print("=" * 80)
    
    healthcare_enterprise = {
        "business_sector": "healthcare",
        "company_size": "enterprise",
        "revenue_bracket": "$1B+",
        "business_locations": ["US", "EU", "Asia", "Australia"],
        "customer_locations": ["US", "EU", "Asia", "Australia", "Canada"],
        "data_types": ["PHI", "PII", "Financial"],
        "infrastructure": "hybrid",
        "customer_type": "B2B",
        "compliance_requirements": ["HIPAA", "SOC2", "ISO27001", "GDPR"],
        "risk_profile": "critical",
        "budget_constraints": "high",
        "implementation_timeline": "1year",
        "technical_maturity": "advanced"
    }
    
    result2 = generate_framework_recommendation(healthcare_enterprise)
    print("Recommended Frameworks:")
    for framework in result2["recommended_frameworks"]:
        print(f"- {framework['framework']} ({framework['status'].upper()})")
        print(f"  Justification: {framework['justification']}")
        print()
    
    # Test Case 3: Manufacturing Company with On-Premise Infrastructure
    print("=" * 80)
    print("TEST CASE 3: Manufacturing Company with On-Premise Infrastructure")
    print("=" * 80)
    
    manufacturing_company = {
        "business_sector": "manufacturing",
        "company_size": "large",
        "revenue_bracket": "$100M+",
        "business_locations": ["US", "Mexico"],
        "customer_locations": ["US", "Canada", "Mexico"],
        "data_types": ["PII", "Intellectual Property", "Financial"],
        "infrastructure": "on-premise",
        "customer_type": "B2B",
        "compliance_requirements": ["SOX", "ISO27001"],
        "risk_profile": "high",
        "budget_constraints": "medium",
        "implementation_timeline": "6months",
        "technical_maturity": "intermediate"
    }
    
    result3 = generate_framework_recommendation(manufacturing_company)
    print("Recommended Frameworks:")
    for framework in result3["recommended_frameworks"]:
        print(f"- {framework['framework']} ({framework['status'].upper()})")
        print(f"  Justification: {framework['justification']}")
        print()
    
    # Test Case 4: SaaS Technology Company
    print("=" * 80)
    print("TEST CASE 4: SaaS Technology Company")
    print("=" * 80)
    
    saas_company = {
        "business_sector": "technology",
        "company_size": "medium",
        "revenue_bracket": "$10M+",
        "business_locations": ["US"],
        "customer_locations": ["US", "EU", "Asia", "Global"],
        "data_types": ["PII", "Customer Data", "Intellectual Property"],
        "infrastructure": "cloud",
        "customer_type": "B2B",
        "compliance_requirements": ["SOC2", "GDPR"],
        "risk_profile": "medium",
        "budget_constraints": "medium",
        "implementation_timeline": "6months",
        "technical_maturity": "intermediate"
    }
    
    result4 = generate_framework_recommendation(saas_company)
    print("Recommended Frameworks:")
    for framework in result4["recommended_frameworks"]:
        print(f"- {framework['framework']} ({framework['status'].upper()})")
        print(f"  Justification: {framework['justification']}")
        print()
    
    # Test Case 5: Government Contractor
    print("=" * 80)
    print("TEST CASE 5: Government Contractor")
    print("=" * 80)
    
    government_contractor = {
        "business_sector": "government",
        "company_size": "large",
        "revenue_bracket": "$100M+",
        "business_locations": ["US"],
        "customer_locations": ["US"],
        "data_types": ["PII", "CUI", "Classified"],
        "infrastructure": "on-premise",
        "customer_type": "B2G",
        "compliance_requirements": ["FISMA", "FedRAMP"],
        "risk_profile": "critical",
        "budget_constraints": "high",
        "implementation_timeline": "1year",
        "technical_maturity": "advanced"
    }
    
    result5 = generate_framework_recommendation(government_contractor)
    print("Recommended Frameworks:")
    for framework in result5["recommended_frameworks"]:
        print(f"- {framework['framework']} ({framework['status'].upper()})")
        print(f"  Justification: {framework['justification']}")
        print()
    
    # Save detailed results to file
    all_results = {
        "global_fintech": result1,
        "healthcare_enterprise": result2,
        "manufacturing_company": result3,
        "saas_company": result4,
        "government_contractor": result5
    }
    
    with open("simplified_framework_recommendation_results.json", "w") as f:
        json.dump(all_results, f, indent=2)
    
    print("=" * 80)
    print("Simplified results saved to 'simplified_framework_recommendation_results.json'")
    print("=" * 80)
    
    # Print summary of key insights
    print("\n" + "=" * 80)
    print("KEY INSIGHTS FROM SIMPLIFIED FRAMEWORK RECOMMENDATIONS")
    print("=" * 80)
    
    print("\n1. MANDATORY FRAMEWORKS:")
    print("   - HIPAA: Mandatory for healthcare organizations")
    print("   - PCI DSS: Mandatory for payment card processing")
    print("   - GDPR: Mandatory for EU data processing")
    print("   - NIST 800-53: Mandatory for government contractors")
    
    print("\n2. RECOMMENDED FRAMEWORKS:")
    print("   - SOC 2: Recommended for B2B companies")
    print("   - ISO 27001: Recommended for enterprise organizations")
    print("   - CIS Controls: Recommended for smaller organizations")
    print("   - COBIT: Recommended for large enterprises")
    
    print("\n3. JUSTIFICATION PATTERNS:")
    print("   - Compliance requirements drive mandatory status")
    print("   - Geographic presence influences GDPR requirements")
    print("   - Industry sector determines specific mandatory frameworks")
    print("   - Data types trigger specific framework requirements")

if __name__ == "__main__":
    test_enhanced_framework_recommendation() 