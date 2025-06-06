# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Academic_Research: Finding scholarly articles"""

from google.adk.agents import LlmAgent
import os
from . import prompt
from .tools import search_google_scholar, search_google_news, find_author

MODEL = "gemini-2.5-pro-preview-05-06"
SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY")


# Define state changes
state_changes = {'key': 'new_value'}



root_agent = LlmAgent(
    name="root_agent",
    model=MODEL,
    description=(
        "Finding research papers on Google scholar based on the user's query"
    ),
    instruction=prompt.RESEARCH_AGENT_PROMPT,
    tools=[
        search_google_scholar,
        search_google_news,
        find_author
    ],
)


