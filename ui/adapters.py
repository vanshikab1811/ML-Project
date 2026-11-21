"""Bridge between the UI and src/. Pages call only the functions in this file."""
from ui import mock_data


class ResumeLoadError(Exception):
    """Raised when a resume cannot be used.

    kind is one of: "empty", "unsupported", "corrupted", "text_poor".
    The page turns each kind into a calm explanatory note.
    """

    def __init__(self, kind: str):
        super().__init__(kind)
        self.kind = kind


def load_resume(file) -> dict:
    """Parse an uploaded file and return a resume_analysis dict (see docs/ui_contracts.md).

    `file` is a Streamlit UploadedFile. Raise ResumeLoadError for unusable files.
    """
    name = (getattr(file, "name", "") or "").lower()
    if not name.endswith((".pdf", ".docx")):
        raise ResumeLoadError("unsupported")
    if getattr(file, "size", 1) == 0:
        raise ResumeLoadError("empty")

    # TODO: replace the mock below with the real pipeline.
    #   from src.resume_parser import parse_resume        # bytes -> text (PyMuPDF / python-docx)
    #   from src.skill_extractor import analyse_resume    # text -> sections, skills, keywords
    #   try:
    #       text = parse_resume(file.getvalue(), file.name)
    #   except ValueError:                                 # unreadable or corrupted file
    #       raise ResumeLoadError("corrupted")
    #   if len(text.strip()) < 200:                        # little or no selectable text
    #       raise ResumeLoadError("text_poor")
    #   return analyse_resume(text)                        # must match the resume_analysis shape
    return mock_data.get_resume_analysis()
