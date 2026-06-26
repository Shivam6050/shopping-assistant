# ruff: noqa
# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import google.auth
from google.auth.exceptions import DefaultCredentialsError

# Handle GCP auth gracefully if not authenticated
try:
    _, project_id = google.auth.default()
    os.environ["GOOGLE_CLOUD_PROJECT"] = project_id or "mock-project"
except DefaultCredentialsError:
    os.environ["GOOGLE_CLOUD_PROJECT"] = "mock-project"

os.environ["GOOGLE_CLOUD_LOCATION"] = "global"
# Explicitly disable Vertex AI to use the API key model setup
os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "False"

from google.adk.agents import Agent
from google.adk.apps import App
from google.adk.models import Gemini
from google.genai import types

# In-memory database of single-use discount codes
# Each code maps to a dictionary tracking whether it has been redeemed and by whom.
DISCOUNT_CODES = {
    "WELCOME50": {"redeemed_by": None},
    "SUMMER20": {"redeemed_by": None},
}

# Simulated registered user IDs
REGISTERED_USERS = {"user123", "user456", "customer_jack", "alice_prime"}


def redeem_discount_code(code: str, user_id: str) -> str:
    """Redeems a single-use discount code for a registered user.

    Args:
        code: The discount code to redeem (e.g. WELCOME50 or SUMMER20).
        user_id: The registered user ID of the customer.

    Returns:
        A message indicating success or the specific reason for failure.
    """
    code_upper = code.strip().upper()

    # 1. Check if the user is registered
    if user_id not in REGISTERED_USERS:
        return (
            f"Error: User ID '{user_id}' is not a registered user. Redemption failed."
        )

    # 2. Check if the discount code exists
    if code_upper not in DISCOUNT_CODES:
        return f"Error: Discount code '{code_upper}' is invalid."

    # 3. Check if the discount code has already been redeemed
    code_info = DISCOUNT_CODES[code_upper]
    if code_info["redeemed_by"] is not None:
        return f"Error: Discount code '{code_upper}' has already been redeemed by user '{code_info['redeemed_by']}'."

    # 4. Process redemption
    code_info["redeemed_by"] = user_id
    return f"Success: Discount code '{code_upper}' has been successfully redeemed for user '{user_id}'."


root_agent = Agent(
    name="root_agent",
    model=Gemini(
        model="gemini-flash-latest",
        api_key=os.environ.get("GEMINI_API_KEY"),
        retry_options=types.HttpRetryOptions(attempts=3),
    ),
    instruction=(
        "You are a helpful AI shopping assistant for a retail store. Assist customers "
        "with finding products, answering questions, and redeeming discount codes. "
        "If a customer requests to redeem a discount code, you MUST ask for their "
        "registered user ID and the code. Then, use the `redeem_discount_code` tool to "
        "process the discount code redemption."
    ),
    tools=[redeem_discount_code],
)

app = App(
    root_agent=root_agent,
    name="app",
)
