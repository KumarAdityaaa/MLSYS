import subprocess
import tempfile
import os
import re
import sys
import uuid

# =========================
# CLEAN CODE
# =========================
def clean_code(code: str, image_name: str):
    # remove markdown
    code = re.sub(r"```python", "", code)
    code = re.sub(r"```", "", code)

    # inject savefig ONLY if plotting used
    if "plt." in code and "savefig" not in code:
        code += f"""
import matplotlib.pyplot as plt
plt.savefig("{image_name}")
plt.close()
"""

    return code.strip()


# =========================
# AUTO INSTALL PACKAGES
# =========================
def install_missing_package(error_msg):
    match = re.search(r"No module named '(.+?)'", error_msg)
    if match:
        package = match.group(1)
        print(f"[INSTALLING] {package}")
        subprocess.run([sys.executable, "-m", "pip", "install", package])
        return True
    return False


# =========================
# EXECUTE CODE
# =========================
def execute_code(code: str):
    image_name = f"output_{uuid.uuid4().hex}.png"

    code = clean_code(code, image_name)

    for attempt in range(2):

        with tempfile.NamedTemporaryFile(delete=False, suffix=".py") as temp:
            temp.write(code.encode())
            temp_path = temp.name

        try:
            result = subprocess.run(
                [sys.executable, temp_path],
                capture_output=True,
                text=True,
                timeout=30
            )
        except subprocess.TimeoutExpired:
            os.remove(temp_path)
            return {
                "code": code,
                "error": "Execution timed out"
            }

        os.remove(temp_path)

        # ✅ SUCCESS
        if result.returncode == 0:
            response = {
                "code": code,
                "output": result.stdout.strip()
            }

            if os.path.exists(image_name):
                response["image"] = image_name

            return response

        # 🔄 TRY INSTALL MISSING PACKAGE
        if install_missing_package(result.stderr):
            continue

        # ❌ FAIL
        return {
            "code": code,
            "error": result.stderr.strip()
        }

    return {
        "code": code,
        "error": "Execution failed after retries"
    }