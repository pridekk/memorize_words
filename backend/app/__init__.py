from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordBearer
from .routes import users, words
from pydantic import BaseModel
from fastapi.logger import logger
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry import propagate
from opentelemetry.propagators.aws import AwsXRayPropagator
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
import logging

logging.basicConfig(
    format="%(asctime)s %(levelname)-8s %(message)s",
    level=logging.DEBUG,
    datefmt="%Y-%m-%d %H:%M:%S",
)

# Import the AWS X-Ray for OTel Python IDs Generator into the application.
from opentelemetry.sdk.extension.aws.trace import AwsXRayIdGenerator

# Sends generated traces in the OTLP format to an ADOT Collector running on port 4317
otlp_exporter = OTLPSpanExporter(endpoint="http://54.180.126.220:4317")
# Processes traces in batches as opposed to immediately one after the other
span_processor = BatchSpanProcessor(otlp_exporter)
# Configures the Global Tracer Provider
trace.set_tracer_provider(TracerProvider(active_span_processor=span_processor, id_generator=AwsXRayIdGenerator()))


propagate.set_global_textmap(AwsXRayPropagator())


class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None


def fake_decode_token(token):
    return User(
        username=token + "fakedecoded", email="john@example.com", full_name="John Doe"
    )


app = FastAPI()
FastAPIInstrumentor.instrument_app(app)

app.include_router(words.router, prefix="/api/v1/words", tags=["words"])
app.include_router(users.router, prefix="/api/v1/users", tags=["users"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def get_current_user(token: str = Depends(oauth2_scheme)):
    user = fake_decode_token(token)
    return user


@app.get("/users/me")
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user


@app.get("/")
async def root():
    return {"message": "WELCOME TO MW"}


@app.get("/test")
async def get_test(token: str = Depends(oauth2_scheme)):
    return {"token": token}


print("Memorize Words Api started!!!")
