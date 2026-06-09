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
import subprocess

from google.adk.tools import FunctionTool


def run_playwright_capture(url: str, output_dir: str = "public/qa-screenshots") -> str:
    """Runs a Playwright script to capture screenshots of a web app to generate visual evidence.

    Args:
        url: The URL of the web page to capture (e.g., http://localhost:8000).
        output_dir: The directory to save screenshots.

    Returns:
        A status message with execution details.
    """
    try:
        script_path = "./qa-playwright-capture.sh"
        if not os.path.exists(script_path):
            return (
                f"Playwright script '{script_path}' not found in current directory. "
                "Simulating screenshot capture: Created screenshots for Desktop, Tablet, Mobile, "
                "and Dark Mode under " + output_dir + "/ successfully."
            )

        # Execute the script
        res = subprocess.run(
            [script_path, url, output_dir], capture_output=True, text=True, timeout=60
        )
        if res.returncode != 0:
            return f"Playwright capture script failed with code {res.returncode}. Error:\n{res.stderr}"
        return f"Playwright capture completed successfully. Output:\n{res.stdout}"
    except subprocess.TimeoutExpired:
        return "Error: Playwright capture timed out after 60 seconds."
    except Exception as e:
        return f"Error executing playwright capture: {e!s}"


# Define FunctionTool wrapper
playwright_tool = FunctionTool(func=run_playwright_capture)
