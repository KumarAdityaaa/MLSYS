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
    # Remove markdown
    code = re.sub(r"```python", "", code)
    code = re.sub(r"```", "", code)

    # Inject savefig ONLY if plotting used
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

        # SUCCESS
        if result.returncode == 0:
            response = {
                "code": code,
                "output": result.stdout.strip()
            }

            if os.path.exists(image_name):
                response["image"] = image_name
                # Schedule cleanup of old images (keep only latest 5)
                _cleanup_old_images()

            return response

        # TRY INSTALL MISSING PACKAGE
        if install_missing_package(result.stderr):
            continue

        # FAIL — clean up image if it was created
        if os.path.exists(image_name):
            os.remove(image_name)

        return {
            "code": code,
            "error": result.stderr.strip()
        }

    return {
        "code": code,
        "error": "Execution failed after retries"
    }


# =========================
# CLEANUP OLD IMAGES
# =========================
def _cleanup_old_images(keep: int = 5):
    """Keep only the most recent N output images, delete the rest."""
    images = [
        f for f in os.listdir(".")
        if f.startswith("output_") and f.endswith(".png")
    ]

    # Sort by modification time, newest first
    images.sort(key=lambda f: os.path.getmtime(f), reverse=True)

    for old_image in images[keep:]:
        try:
            os.remove(old_image)
            print(f"[CLEANUP] Deleted old image: {old_image}")
        except Exception as e:
            print(f"[CLEANUP] Could not delete {old_image}: {e}")