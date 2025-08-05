#!/usr/bin/env python3
"""
Test script for the Framework Recommendation System
"""

import json
from services.framework_recommender import generate_framework_recommendation

def test_framework_recommendation():
    """Test the framework recommendation system with different organization profiles"""
    
    # Test Case 1: Startup FinTech Company
    print("=" * 60)
    print("TEST CASE 1: Startup FinTech Company")
    print("=" * 60)
    
    startup_fintech = {
        "industry": "finance",
        "company_size": "startup",
        "compliance_requirements": ["PCI", "GDPR"],
        "risk_profile": "medium",
        "budget_constraints": "low",
        "implementation_timeline": "immediate",
        "technical_maturity": "basic"
    }
    
    result1 = generate_framework_recommendation(startup_fintech)
    print("Recommended Frameworks:")
    for framework in result1["recommended_frameworks"]:
        print(f"- {framework['framework']} (Score: {framework['score']})")
        print(f"  Description: {framework['details']['description']}")
        print(f"  Complexity: {framework['details']['complexity']}, Cost: {framework['details']['cost']}")
        print()
    
    # Test Case 2: Medium Healthcare Organization
    print("=" * 60)
    print("TEST CASE 2: Medium Healthcare Organization")
    print("=" * 60)
    
    healthcare_medium = {
        "industry": "healthcare",
        "company_size": "medium",
        "compliance_requirements": ["HIPAA", "SOC2"],
        "risk_profile": "high",
        "budget_constraints": "medium",
        "implementation_timeline": "6months",
        "technical_maturity": "intermediate"
    }
    
    result2 = generate_framework_recommendation(healthcare_medium)
    print("Recommended Frameworks:")
    for framework in result2["recommended_frameworks"]:
        print(f"- {framework['framework']} (Score: {framework['score']})")
        print(f"  Description: {framework['details']['description']}")
        print(f"  Complexity: {framework['details']['complexity']}, Cost: {framework['details']['cost']}")
        print()
    
    # Test Case 3: Enterprise Technology Company
    print("=" * 60)
    print("TEST CASE 3: Enterprise Technology Company")
    print("=" * 60)
    
    enterprise_tech = {
        "industry": "technology",
        "company_size": "enterprise",
        "compliance_requirements": ["SOX", "ISO27001", "GDPR"],
        "risk_profile": "critical",
        "budget_constraints": "high",
        "implementation_timeline": "1year",
        "technical_maturity": "advanced"
    }
    
    result3 = generate_framework_recommendation(enterprise_tech)
    print("Recommended Frameworks:")
    for framework in result3["recommended_frameworks"]:
        print(f"- {framework['framework']} (Score: {framework['score']})")
        print(f"  Description: {framework['details']['description']}")
        print(f"  Complexity: {framework['details']['complexity']}, Cost: {framework['details']['cost']}")
        print()
    
    # Test Case 4: Small Manufacturing Company
    print("=" * 60)
    print("TEST CASE 4: Small Manufacturing Company")
    print("=" * 60)
    
    small_manufacturing = {
        "industry": "manufacturing",
        "company_size": "small",
        "compliance_requirements": ["ISO27001"],
        "risk_profile": "low",
        "budget_constraints": "low",
        "implementation_timeline": "3months",
        "technical_maturity": "basic"
    }
    
    result4 = generate_framework_recommendation(small_manufacturing)
    print("Recommended Frameworks:")
    for framework in result4["recommended_frameworks"]:
        print(f"- {framework['framework']} (Score: {framework['score']})")
        print(f"  Description: {framework['details']['description']}")
        print(f"  Complexity: {framework['details']['complexity']}, Cost: {framework['details']['cost']}")
        print()
    
    # Save detailed results to file
    all_results = {
        "startup_fintech": result1,
        "healthcare_medium": result2,
        "enterprise_tech": result3,
        "small_manufacturing": result4
    }
    
    with open("framework_recommendation_results.json", "w") as f:
        json.dump(all_results, f, indent=2)
    
    print("=" * 60)
    print("Detailed results saved to 'framework_recommendation_results.json'")
    print("=" * 60)

if __name__ == "__main__":
    test_framework_recommendation() 