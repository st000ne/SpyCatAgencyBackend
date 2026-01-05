import requests
from fastapi import HTTPException

_CAT_API_URL = "https://api.thecatapi.com/v1/breeds"
_cached_breeds = None


def _fetch_breeds() -> set[str]:
    global _cached_breeds

    if _cached_breeds is not None:
        return _cached_breeds

    try:
        response = requests.get(_CAT_API_URL, timeout=5)
        response.raise_for_status()
    except requests.RequestException:
        raise HTTPException(
            status_code=503,
            detail="Failed to validate cat breed"
        )

    breeds = response.json()
    _cached_breeds = {breed["name"].lower() for breed in breeds}
    return _cached_breeds


def validate_breed(breed: str) -> None:
    breeds = _fetch_breeds()
    if breed.lower() not in breeds:
        raise HTTPException(
            status_code=400,
            detail="Invalid cat breed"
        )
