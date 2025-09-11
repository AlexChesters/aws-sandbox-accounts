from aws_lambda_powertools import Logger

logger = Logger()

@logger.inject_lambda_context(log_event=True)
def handler(_event, _context):
    pass
