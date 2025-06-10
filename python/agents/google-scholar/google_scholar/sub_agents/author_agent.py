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

"""Author Agent to retreive Google Scholar profiles"""
from google.adk.agents import LlmAgent

from ..tools.find_author import find_author_tool
from ..tools.find_author_details import find_author_details_tool
from . import prompt

MODEL = "gemini-2.5-pro-preview-05-06"

AuthorAgent = LlmAgent(
    model=MODEL,
    name="author_agent",
    description=(
        "Find information on authors"
    ),
    instruction=prompt.AUTHOR_AGENT_PROMPT,
    tools=[
        find_author_tool,
        find_author_details_tool
    ],
)
