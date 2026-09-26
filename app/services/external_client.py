import requests
from tenacity import retry, stop_after_attempt, wait_exponential


@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=1, max=5)
)
def call_external_service():
    response = requests.get(
        "https://httpbin.org/delay/2",
        timeout=5
    )

    response.raise_for_status()

    return response.json()


def check_external_service():
    try:
        return call_external_service()

    except requests.RequestException:
        raise RuntimeError("External service unavailable")