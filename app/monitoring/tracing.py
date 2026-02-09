import uuid

class Tracer:
    """
    Distributed tracing helper (e.g. OpenTelemetry wraper).
    """
    def start_span(self, name: str):
        span_id = str(uuid.uuid4())
        # print(f"Start span: {name} ({span_id})")
        return span_id

    def end_span(self, span_id: str):
        # print(f"End span: {span_id}")
        pass
