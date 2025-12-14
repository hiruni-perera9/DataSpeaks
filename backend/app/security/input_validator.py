# Input validation and sanitizatino

from pydantic import BaseModel, Field, validator
from typing import Optional
import re

class SecureQueryInput(BaseModel):
    # Validates User Questions for AI chat

    question: str = Field(
        ...,
        min_length = 1,
        max_length = 500,
        description = "User's question about the dashboard"
    )

    chart_id: str = Field(
        ...,
        description = "ID of the chart being asked about"
    )

    # Suspicious patterns that might indicate injection attempts
    INJECTION_PATTERNS = [
        r'ignore\s+(previous|all|above)',
        r'forget\s+(previous|everything)',
        r'new\s+instructions?',
        r'system\s+prompt',
        r'you\s+are\s+now',
        r'pretend\s+(you|to be)',
        r'act\s+as',
        r'disregard',
        r'override',
        r'<\s*script',  # XSS attempt
        r'javascript:',
        r'--.*$',  # SQL comment
        r';\s*drop\s+table',  # SQL injection
    ]

    # Allowed chart IDs
    ALLOWED_CHART_IDS = [
        'revenue-over-time',
        'customer-churn',
        'mrr-growth',
        'cohort-retention',
        'plan-distribution',
        'customer-activity'
    ]

    @validator('question')
    def validate_question(cls, v):
        # Validate and sanitize user questions

        # Strip whitespace
        v = v.strip()

        # Check for injection patterns
        for pattern in cls.INJECTION_PATTERNS:
            if re.search(pattern, v, re.IGNORECASE):
                # Log for security monitoring
                from app.utils.security_logger import log_suspicious_input
                log_suspicious_input(v, pattern)

                raise ValueError(
                    "Your question contains patterns that cannot be processed."
                    "Please rephrase and try again"
                )
            
        # Check for excessive special characters(obfuscation attempt)
        special_char_count = sum(not c.isalnum() and not c.isspace() for c in v)
        special_char_ratio = special_char_count / len(v)

        if special_char_ratio > 0.3: # More than 30% special characters
            raise ValueError("Questions contains too many special characters")
        
        return v
    
    @validator('chart_id')
    def validate_chart_id(cls, v):
        # Whitelist validation for chart IDs

        if v not in cls.ALLOWED_CHART_IDS:
            raise ValueError(f"Invalid chart_id: {v}")
        return v
    
class CustomerFilterInput(BaseModel):
    # Validate customer list filters

    plan: Optional[str] = None
    is_active: Optional[bool] = None
    min_mrr: Optional[float] = Field(None, ge=0)
    max_mrr: Optional[float] = Field(None, ge=0)

    @validator('plan')
    def validate_plan(cls, v):
        # Only allow vaild plan types

        if v is not None:
            allowed_plans = ['starter', 'growth', 'enterprise']
            if v.lower() not in allowed_plans:
                raise ValueError(f"Invalid plan. Must be one of: {allowed_plans}")
        return v.lower() if v else None
        
    @validator('max_mrr')
    def validate_mrr_range(cls, v, values):
        # Ensure max_mrr > min_mrr
        if v is not None and 'min_mrr' in values and values['min_mrr'] is not None:
            if v < values['min_mrr']:
                raise ValueError("max_mrr must be greater than min_mrr")
        return v
    
    