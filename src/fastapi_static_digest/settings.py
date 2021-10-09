import os


class FastAPIStaticDigestSettings:
    """Configuration settings for fastapi_static_digest.
    """
    RELOAD = bool(os.getenv("FASTAPI_STATICDIGEST_RELOAD", False))