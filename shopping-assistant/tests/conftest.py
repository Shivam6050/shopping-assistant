import google.auth
import google.cloud.logging
import google.genai
from google.auth.credentials import AnonymousCredentials
from google.genai import types


# Mock google.auth.default to prevent DefaultCredentialsError during test discovery
def mock_default(*args, **kwargs):
    return AnonymousCredentials(), "mock-project"


google.auth.default = mock_default

# Mock google.cloud.logging.Client to avoid real logging requests


class MockLogger:
    def log_struct(self, *args, **kwargs):
        pass

    def log_text(self, *args, **kwargs):
        pass


class MockLoggingClient:
    def __init__(self, *args, **kwargs):
        pass

    def logger(self, name, *args, **kwargs):
        return MockLogger()


google.cloud.logging.Client = MockLoggingClient

# Mock google.genai.Client to avoid actual API calls and API key errors


class MockPart:
    def __init__(self, text="Sky is blue due to Rayleigh scattering."):
        self.text = text
        self.function_call = None
        self.function_response = None


class MockContent:
    def __init__(self, text="Sky is blue due to Rayleigh scattering."):
        self.parts = [MockPart(text)]
        self.role = "model"


class MockCandidate:
    def __init__(self, text="Sky is blue due to Rayleigh scattering."):
        self.content = MockContent(text)
        self.grounding_metadata = None
        self.finish_reason = types.FinishReason.STOP
        self.finish_message = None
        self.citation_metadata = None
        self.avg_logprobs = None
        self.logprobs_result = None


class MockGenerateContentResponse:
    def __init__(self, text="Sky is blue due to Rayleigh scattering."):
        self.text = text
        self.candidates = [MockCandidate(text)]
        self.function_calls = []
        self.usage_metadata = None
        self.model_version = "mock-model-version"
        self.prompt_feedback = None

    def model_dump(self, *args, **kwargs):
        return {
            "candidates": [
                {
                    "content": {"parts": [{"text": self.text}], "role": "model"},
                    "finish_reason": "STOP",
                }
            ],
            "model_version": self.model_version,
        }

    def model_dump_json(self, *args, **kwargs):
        import json

        return json.dumps(self.model_dump())


class MockAioModels:
    async def generate_content_stream(self, *args, **kwargs):
        async def async_generator():
            yield MockGenerateContentResponse()

        return async_generator()

    async def generate_content(self, *args, **kwargs):
        return MockGenerateContentResponse()


class MockAio:
    def __init__(self):
        self.models = MockAioModels()


class MockClient:
    def __init__(self, *args, **kwargs):
        self.aio = MockAio()
        self.vertexai = False


google.genai.Client = MockClient
