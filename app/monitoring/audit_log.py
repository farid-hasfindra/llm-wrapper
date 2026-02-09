from app.core.logging import logger

class AuditLogger:
    def log_action(self, user_id: str, action: str, details: dict):
        logger.info("audit_log", user=user_id, action=action, details=details)

audit_logger = AuditLogger()
