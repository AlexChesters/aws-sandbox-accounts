from aws_lambda_powertools import Logger, Tracer

logger = Logger()
tracer = Tracer()

@tracer.capture_lambda_handler
@logger.inject_lambda_context(log_event=True)
def handler(_event, _context):
    return {}
