"""Upload validation helpers for the Streamlit prediction boundary."""


def validate_upload_size(uploaded_file, max_size_mb: int) -> None:
    """Reject uploads larger than the configured maximum size.

    Streamlit's UploadedFile exposes ``size`` in bytes. The check is kept
    separate from the UI so it can be regression-tested without Streamlit.
    """
    if max_size_mb <= 0:
        raise ValueError("max_size_mb must be greater than zero")

    size = getattr(uploaded_file, "size", None)
    if size is None:
        raise ValueError("Uploaded file size is unavailable")

    max_size_bytes = max_size_mb * 1024 * 1024
    if size > max_size_bytes:
        raise ValueError(
            f"Uploaded file exceeds the {max_size_mb} MB limit "
            f"({size / (1024 * 1024):.2f} MB)."
        )
