import pathlib

import dotenv
import pytest
from google.adk.evaluation.agent_evaluator import AgentEvaluator

pytest_plugins = ("pytest_asyncio",)


@pytest.fixture(scope="session", autouse=True)
def load_env():
    dotenv.load_dotenv()


@pytest.mark.asyncio
async def test_all():
    """Test the agent's basic ability on a few examples."""
    print("Running evaluate")
    await AgentEvaluator.evaluate(
        "google_scholar",
        str("google_scholar/eval/data/google-scholar.test.json"),
        agent_name="root_agent"
    )
