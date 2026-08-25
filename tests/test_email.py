from app.utils.email import extract_public_email
def test_email(): assert extract_public_email("Business: hello@example.com")=="hello@example.com"
def test_missing(): assert extract_public_email("No contact")=="Not Found"
