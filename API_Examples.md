# Harmonization Service API Examples

This document provides comprehensive examples of API requests and responses for the Control Harmonization Service.

## Table of Contents
1. [Basic Batch Harmonization (No Context)](#1-basic-batch-harmonization-no-context)
2. [Organization Context Harmonization (Finance Industry)](#2-organization-context-harmonization-finance-industry)
3. [Fast Mode Harmonization (Preview)](#3-fast-mode-harmonization-preview)
4. [Single Control Harmonization](#4-single-control-harmonization)
5. [System Configuration Check](#5-system-configuration-check)
6. [Health Check](#6-health-check)
7. [Clear Cache](#7-clear-cache)

---

## 1. Basic Batch Harmonization (No Context)

### Request:
```bash
POST /batch-harmonize
Content-Type: application/json
```

```json
{
  "controls": [
    {
      "framework": "AWS",
      "control_id": "IAM.1",
      "name": "Multi-Factor Authentication",
      "description": "Enable MFA for all users to enhance security"
    },
    {
      "framework": "GCP",
      "control_id": "IAM.001",
      "name": "Two-Factor Authentication",
      "description": "Require 2FA for all user accounts"
    },
    {
      "framework": "Azure",
      "control_id": "AAD.1",
      "name": "Conditional Access",
      "description": "Implement conditional access policies with MFA"
    },
    {
      "framework": "AWS",
      "control_id": "S3.1",
      "name": "Bucket Encryption",
      "description": "Enable encryption at rest for S3 buckets"
    }
  ]
}
```

### Response:
```json
{
  "unified_controls": [
    {
      "unified_control_id": "UC-000",
      "title": "Multi-Factor Authentication Implementation",
      "description": "Require multi-factor authentication for all user accounts across cloud platforms to enhance security posture and prevent unauthorized access.",
      "implementation_steps": [
        {
          "step": "Configure MFA in Identity Provider",
          "description": "Enable MFA settings in your cloud identity management system"
        },
        {
          "step": "Enforce MFA for All Users",
          "description": "Set policies requiring MFA for all user accounts, especially privileged users"
        }
      ],
      "mapped_controls": [
        {
          "framework": "AWS",
          "control_id": "IAM.1",
          "name": "Multi-Factor Authentication",
          "description": "Enable MFA for all users to enhance security"
        },
        {
          "framework": "GCP",
          "control_id": "IAM.001",
          "name": "Two-Factor Authentication",
          "description": "Require 2FA for all user accounts"
        },
        {
          "framework": "Azure",
          "control_id": "AAD.1",
          "name": "Conditional Access",
          "description": "Implement conditional access policies with MFA"
        }
      ],
      "is_clustered": true,
      "fast_mode": false,
      "org_context_applied": false
    },
    {
      "unified_control_id": "UC-001",
      "title": "Data Encryption at Rest",
      "description": "Implement encryption for data storage to protect sensitive information when stored.",
      "implementation_steps": [
        {
          "step": "Enable Storage Encryption",
          "description": "Configure encryption settings for your storage services"
        }
      ],
      "mapped_controls": [
        {
          "framework": "AWS",
          "control_id": "S3.1",
          "name": "Bucket Encryption",
          "description": "Enable encryption at rest for S3 buckets"
        }
      ],
      "is_clustered": true,
      "fast_mode": false,
      "org_context_applied": false
    }
  ],
  "total_clusters": 2,
  "organization_analysis": {
    "existing_controls_count": 0,
    "industry": null,
    "gaps": [],
    "overlaps": [],
    "recommendations": []
  },
  "performance": {
    "processing_time_seconds": 3.45,
    "controls_processed": 4,
    "fast_mode": false,
    "clusters_generated": 2,
    "org_context_applied": false
  },
  "org_context": null
}
```

---

## 2. Organization Context Harmonization (Finance Industry)

### Request:
```bash
POST /batch-harmonize
Content-Type: application/json
```

```json
{
  "controls": [
    {
      "framework": "PCI DSS",
      "control_id": "3.4",
      "name": "Encrypt PAN Data",
      "description": "Render PAN unreadable anywhere it is stored using strong cryptography"
    },
    {
      "framework": "SOX",
      "control_id": "IT-1",
      "name": "Data Protection",
      "description": "Implement controls to protect financial data integrity and confidentiality"
    },
    {
      "framework": "AWS",
      "control_id": "KMS.1",
      "name": "Key Management",
      "description": "Use AWS KMS for encryption key management"
    }
  ],
  "org_context": {
    "industry": "finance",
    "existing_controls": [
      "Multi-factor authentication enabled",
      "Regular security audits conducted",
      "Data encryption in transit"
    ],
    "risk_profile": "high",
    "compliance_frameworks": ["PCI", "SOX", "GDPR"]
  }
}
```

### Response:
```json
{
  "unified_controls": [
    {
      "unified_control_id": "UC-000",
      "title": "Financial Data Encryption and Key Management",
      "description": "Implement comprehensive encryption controls for financial data protection to meet PCI DSS and SOX compliance requirements for financial institutions.",
      "implementation_steps": [
        {
          "step": "Configure Encryption for PAN Data",
          "description": "Implement strong cryptography to render PAN data unreadable in storage as required by PCI DSS 3.4"
        },
        {
          "step": "Set Up Key Management System",
          "description": "Deploy AWS KMS or equivalent for centralized encryption key management with proper access controls"
        },
        {
          "step": "Establish Data Protection Policies",
          "description": "Create and enforce policies for financial data integrity and confidentiality per SOX requirements"
        }
      ],
      "mapped_controls": [
        {
          "framework": "PCI DSS",
          "control_id": "3.4",
          "name": "Encrypt PAN Data",
          "description": "Render PAN unreadable anywhere it is stored using strong cryptography"
        },
        {
          "framework": "SOX",
          "control_id": "IT-1",
          "name": "Data Protection",
          "description": "Implement controls to protect financial data integrity and confidentiality"
        },
        {
          "framework": "AWS",
          "control_id": "KMS.1",
          "name": "Key Management",
          "description": "Use AWS KMS for encryption key management"
        }
      ],
      "is_clustered": true,
      "fast_mode": false,
      "org_context_applied": true
    }
  ],
  "total_clusters": 1,
  "organization_analysis": {
    "existing_controls_count": 3,
    "industry": "finance",
    "gaps": [],
    "overlaps": [],
    "recommendations": [
      "Focus on regulatory compliance controls (PCI, SOX)"
    ]
  },
  "performance": {
    "processing_time_seconds": 2.87,
    "controls_processed": 3,
    "fast_mode": false,
    "clusters_generated": 1,
    "org_context_applied": true
  },
  "org_context": {
    "industry": "finance",
    "existing_controls": [
      "Multi-factor authentication enabled",
      "Regular security audits conducted",
      "Data encryption in transit"
    ],
    "risk_profile": "high",
    "compliance_frameworks": ["PCI", "SOX", "GDPR"]
  }
}
```

---

## 3. Fast Mode Harmonization (Preview)

### Request:
```bash
POST /batch-harmonize
Content-Type: application/json
```

```json
{
  "controls": [
    {
      "framework": "AWS",
      "control_id": "IAM.1",
      "name": "MFA",
      "description": "Enable MFA for all users"
    },
    {
      "framework": "GCP",
      "control_id": "IAM.001",
      "name": "2FA",
      "description": "Require 2FA for all accounts"
    }
  ],
  "fast_mode": true
}
```

### Response:
```json
{
  "unified_controls": [
    {
      "unified_control_id": "UC-000",
      "title": "MFA (2 controls)",
      "description": "Group of 2 similar controls from AWS, GCP frameworks",
      "implementation_steps": [],
      "mapped_controls": [
        {
          "framework": "AWS",
          "control_id": "IAM.1",
          "name": "MFA",
          "description": "Enable MFA for all users"
        },
        {
          "framework": "GCP",
          "control_id": "IAM.001",
          "name": "2FA",
          "description": "Require 2FA for all accounts"
        }
      ],
      "is_clustered": true,
      "fast_mode": true,
      "org_context_applied": false
    }
  ],
  "total_clusters": 1,
  "organization_analysis": {
    "existing_controls_count": 0,
    "industry": null,
    "gaps": [],
    "overlaps": [],
    "recommendations": []
  },
  "performance": {
    "processing_time_seconds": 0.23,
    "controls_processed": 2,
    "fast_mode": true,
    "clusters_generated": 1,
    "org_context_applied": false
  },
  "org_context": null
}
```

---

## 4. Single Control Harmonization

### Request:
```bash
POST /harmonize
Content-Type: application/json
```

```json
{
  "description": "Enable multi-factor authentication for all users",
  "top_n": 3
}
```

### Response:
```json
{
  "unified_result": {
    "title": "Multi-Factor Authentication Implementation",
    "description": "Implement MFA across all user accounts to enhance security and prevent unauthorized access.",
    "implementation_steps": [
      {
        "step": "Configure MFA Settings",
        "description": "Enable MFA in your identity provider"
      },
      {
        "step": "Enforce MFA Policy",
        "description": "Set policies requiring MFA for all users"
      }
    ]
  },
  "matched_controls": [
    {
      "framework": "AWS",
      "control_id": "IAM.1",
      "name": "Multi-Factor Authentication",
      "description": "Enable MFA for all users",
      "match_score": 0.92
    },
    {
      "framework": "GCP",
      "control_id": "IAM.001",
      "name": "Two-Factor Authentication",
      "description": "Require 2FA for all accounts",
      "match_score": 0.89
    }
  ],
  "performance": {
    "processing_time_seconds": 1.23,
    "controls_processed": 1
  }
}
```

---

## 5. System Configuration Check

### Request:
```bash
GET /config
```

### Response:
```json
{
  "configuration": {
    "clustering_eps": 0.4,
    "clustering_min_samples": 2,
    "llm_model": "llama2",
    "llm_temperature": 0.3,
    "max_workers": 4,
    "enable_parallel": true,
    "enable_embedding_cache": true,
    "default_fast_mode": false
  },
  "cache_stats": {
    "cache_size": 15,
    "cache_keys": ["abc123", "def456", "ghi789"]
  },
  "system_info": {
    "embedding_model": "all-MiniLM-L6-v2",
    "clustering_algorithm": "DBSCAN"
  }
}
```

---

## 6. Health Check

### Request:
```bash
GET /health
```

### Response:
```json
{
  "status": "healthy",
  "cache_size": 15,
  "config": {
    "fast_mode_default": false,
    "parallel_processing": true,
    "max_workers": 4
  }
}
```

---

## 7. Clear Cache

### Request:
```bash
POST /clear-cache
```

### Response:
```json
{
  "message": "Cache cleared successfully",
  "cache_stats": {
    "cache_size": 0,
    "cache_keys": []
  }
}
```

---

## API Endpoints Summary

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/batch-harmonize` | POST | Harmonize multiple controls with optional organization context |
| `/harmonize` | POST | Harmonize a single control by finding similar ones |
| `/config` | GET | Get system configuration and performance statistics |
| `/health` | GET | Health check with basic performance metrics |
| `/clear-cache` | POST | Clear the embedding cache to free memory |

## Request Parameters

### Batch Harmonization Parameters:
- `controls` (required): Array of control objects
- `fast_mode` (optional): Boolean for preview mode (default: false)
- `org_context` (optional): Organization context object

### Organization Context Structure:
```json
{
  "industry": "string",           // e.g., "finance", "healthcare"
  "existing_controls": ["string"], // List of existing control descriptions
  "risk_profile": "string",       // e.g., "high", "medium", "low"
  "compliance_frameworks": ["string"] // e.g., ["PCI", "SOX", "GDPR"]
}
```

### Control Object Structure:
```json
{
  "framework": "string",    // e.g., "AWS", "GCP", "PCI DSS"
  "control_id": "string",   // Framework-specific control ID
  "name": "string",         // Control name
  "description": "string"   // Control description
}
```

## Performance Modes

### Normal Mode (Default):
- ✅ Uses LLM for quality descriptions and implementation steps
- ✅ Provides semantic understanding and context
- ✅ Recommended for production use

### Fast Mode:
- ⚡ Instant results (no LLM calls)
- ⚡ Basic grouping and naming
- ⚡ For quick previews or when LLM is unavailable

## Response Fields

### Unified Control Fields:
- `unified_control_id`: Unique identifier for the harmonized control
- `title`: Unified control title
- `description`: Unified control description
- `implementation_steps`: Array of implementation steps
- `mapped_controls`: Original controls that were harmonized
- `is_clustered`: Whether the control was part of a cluster
- `fast_mode`: Whether fast mode was used
- `org_context_applied`: Whether organization context was applied

### Performance Fields:
- `processing_time_seconds`: Total processing time
- `controls_processed`: Number of controls processed
- `fast_mode`: Whether fast mode was used
- `clusters_generated`: Number of clusters created
- `org_context_applied`: Whether organization context was applied

### Organization Analysis Fields:
- `existing_controls_count`: Number of existing controls
- `industry`: Organization industry
- `gaps`: Identified control gaps
- `overlaps`: Overlaps with existing controls
- `recommendations`: Industry-specific recommendations 