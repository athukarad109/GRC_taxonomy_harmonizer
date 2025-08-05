#!/usr/bin/env python3
"""
Test script for the updated Framework Recommendation System
Now works with existing frameworks instead of compliance requirements
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.framework_recommender import generate_framework_recommendation
import json

def test_framework_recommendations():
    """Test the updated framework recommendation system"""
    
    # Test Case 1: Healthcare startup with no existing frameworks
    print("=" * 60)
    print("TEST CASE 1: Healthcare Startup (No Existing Frameworks)")
    print("=" * 60)
    
    org_data_1 = {
        "business_sector": "healthcare",
        "company_size": "startup",
        "revenue_bracket": "$1M+",
        "business_locations": ["US"],
        "customer_locations": ["US"],
        "data_types": ["PHI", "PII"],
        "infrastructure": "cloud",
        "customer_type": "B2B",
        "existing_frameworks": [],  # No existing frameworks
        "risk_profile": "medium",
        "budget_constraints": "low",
        "implementation_timeline": "3months",
        "technical_maturity": "basic"
    }
    
    result1 = generate_framework_recommendation(org_data_1)
    print(f"Organization: {org_data_1['business_sector']} {org_data_1['company_size']}")
    print(f"Existing Frameworks: {org_data_1['existing_frameworks']}")
    print("\nRecommended Frameworks:")
    for framework in result1["recommended_frameworks"]:
        print(f"- {framework['framework']} ({framework['status'].upper()})")
        print(f"  Justification: {framework['justification']}")
        print()
    
    # Test Case 2: Financial company with existing PCI DSS
    print("=" * 60)
    print("TEST CASE 2: Financial Company (Has PCI DSS)")
    print("=" * 60)
    
    org_data_2 = {
        "business_sector": "finance",
        "company_size": "medium",
        "revenue_bracket": "$10M+",
        "business_locations": ["US", "EU"],
        "customer_locations": ["US", "EU", "Asia"],
        "data_types": ["Payment Card Data", "PII", "Financial"],
        "infrastructure": "hybrid",
        "customer_type": "B2C",
        "existing_frameworks": ["PCI DSS"],  # Already has PCI DSS
        "risk_profile": "high",
        "budget_constraints": "medium",
        "implementation_timeline": "6months",
        "technical_maturity": "intermediate"
    }
    
    result2 = generate_framework_recommendation(org_data_2)
    print(f"Organization: {org_data_2['business_sector']} {org_data_2['company_size']}")
    print(f"Existing Frameworks: {org_data_2['existing_frameworks']}")
    print("\nRecommended Frameworks:")
    for framework in result2["recommended_frameworks"]:
        print(f"- {framework['framework']} ({framework['status'].upper()})")
        print(f"  Justification: {framework['justification']}")
        print()
    
    # Test Case 3: Tech company with multiple existing frameworks
    print("=" * 60)
    print("TEST CASE 3: Tech Company (Has Multiple Frameworks)")
    print("=" * 60)
    
    org_data_3 = {
        "business_sector": "technology",
        "company_size": "large",
        "revenue_bracket": "$100M+",
        "business_locations": ["US", "EU", "Asia"],
        "customer_locations": ["Global"],
        "data_types": ["PII", "Customer Data", "Intellectual Property"],
        "infrastructure": "cloud",
        "customer_type": "B2B",
        "existing_frameworks": ["SOC 2", "ISO 27001", "GDPR"],  # Has multiple frameworks
        "risk_profile": "high",
        "budget_constraints": "high",
        "implementation_timeline": "1year",
        "technical_maturity": "advanced"
    }
    
    result3 = generate_framework_recommendation(org_data_3)
    print(f"Organization: {org_data_3['business_sector']} {org_data_3['company_size']}")
    print(f"Existing Frameworks: {org_data_3['existing_frameworks']}")
    print("\nRecommended Frameworks:")
    for framework in result3["recommended_frameworks"]:
        print(f"- {framework['framework']} ({framework['status'].upper()})")
        print(f"  Justification: {framework['justification']}")
        print()
    
    # Test Case 4: Government contractor with NIST
    print("=" * 60)
    print("TEST CASE 4: Government Contractor (Has NIST)")
    print("=" * 60)
    
    org_data_4 = {
        "business_sector": "government",
        "company_size": "enterprise",
        "revenue_bracket": "$1B+",
        "business_locations": ["US"],
        "customer_locations": ["US"],
        "data_types": ["CUI", "Classified", "PII"],
        "infrastructure": "on-premise",
        "customer_type": "B2G",
        "existing_frameworks": ["NIST 800-53"],  # Already has NIST
        "risk_profile": "critical",
        "budget_constraints": "high",
        "implementation_timeline": "1year",
        "technical_maturity": "advanced"
    }
    
    result4 = generate_framework_recommendation(org_data_4)
    print(f"Organization: {org_data_4['business_sector']} {org_data_4['company_size']}")
    print(f"Existing Frameworks: {org_data_4['existing_frameworks']}")
    print("\nRecommended Frameworks:")
    for framework in result4["recommended_frameworks"]:
        print(f"- {framework['framework']} ({framework['status'].upper()})")
        print(f"  Justification: {framework['justification']}")
        print()
    
    # Save all results
    all_results = {
        "healthcare_startup": result1,
        "financial_company": result2,
        "tech_company": result3,
        "government_contractor": result4
    }
    
    with open("updated_framework_recommendation_results.json", "w") as f:
        json.dump(all_results, f, indent=2)
    
    print("=" * 60)
    print("KEY INSIGHTS FROM UPDATED SYSTEM:")
    print("=" * 60)
    print("1. System now avoids recommending frameworks the organization already has")
    print("2. Mandatory status is determined by industry and data types, not compliance requirements")
    print("3. Organizations with existing frameworks get bonus points for maturity")
    print("4. Focus is on what frameworks they need, not what they already have")
    print("5. Results saved to 'updated_framework_recommendation_results.json'")

if __name__ == "__main__":
    test_framework_recommendations() 