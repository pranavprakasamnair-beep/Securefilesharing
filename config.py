import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-this")

    MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
    MYSQL_USER = os.getenv("MYSQL_USER", "root")
    MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "")
    MYSQL_DB = os.getenv("MYSQL_DB", "secure_file_sharing")

    UPLOAD_FOLDER = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "static",
        "uploads"
    )

    ALLOWED_EXTENSIONS = {
        "txt", "pdf", "png", "jpg", "jpeg",
        "gif", "doc", "docx", "xls", "xlsx",
        "ppt", "pptx", "zip"
    }

    @staticmethod
    def allowed_file(filename):
        return (
            "." in filename
            and filename.rsplit(".", 1)[1].lower()
            in Config.ALLOWED_EXTENSIONS
        )