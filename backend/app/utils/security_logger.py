# Security event logging

import logging
from datetime import datetime
from typing import Optional

# Create security specific logger
security_logger = logging.getLogger('security')
security_logger.setLevel(logging.WARNING)

# Add file handler for security events
handler = logging.FileHandler('security.log')
handler.setFormatter(logging.Formatter(
    '%(asctime)s - SECURITY - %(levelname)s - %(message)s'
))
security_logger.addHandler(handler)

def log_suspicious_input(
        input_text: str,
        pattern: str,
        user_id: Optional[str] = None
):
    # Log potential injection attacks
    security_logger.warning({
        'event': 'suspicious_input_detected',
        'timestamp': datetime.utcnow().isoformat(),
        'pattern_matched': pattern,
        'input_sample': input_text[:100],  
        'input_length': len(input_text),
        'user_id': user_id or 'anonymous'
    })

def log_validation_failure(
        input_type: str,
        error: str,
        user_id: Optional[str] = None
):
    # Log validation failure for monitoring
    security_logger.info({
        'event': 'validation_failure',
        'timestamp': datetime.utcnow().isoformat(),
        'input_type': input_type,
        'error': error,
        'user_id': user_id or 'anonymous'
    })