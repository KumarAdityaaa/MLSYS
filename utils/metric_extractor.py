import re

def extract_metrics(output: str):
    metrics = {}

    # Final metrics
    acc_match = re.findall(r"accuracy[:=]\s*([0-9.]+)", output, re.IGNORECASE)
    loss_match = re.findall(r"loss[:=]\s*([0-9.]+)", output, re.IGNORECASE)

    if acc_match:
        metrics["accuracy"] = float(acc_match[-1])

    if loss_match:
        metrics["loss"] = float(loss_match[-1])

    # 📈 Epoch tracking
    epoch_data = []

    epoch_matches = re.findall(
        r"epoch\s*(\d+).*?loss[:=]\s*([0-9.]+).*?(?:acc|accuracy)[:=]\s*([0-9.]+)",
        output,
        re.IGNORECASE
    )

    for match in epoch_matches:
        epoch_data.append({
            "epoch": int(match[0]),
            "loss": float(match[1]),
            "accuracy": float(match[2])
        })

    if epoch_data:
        metrics["epochs"] = epoch_data

    return metrics