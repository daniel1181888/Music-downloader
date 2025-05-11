import json
import os

from dotenv import load_dotenv


class Config:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        self.settings_path: str = "settings.json"
        self.env_path: str = ".env"

        # General settings
        self.spotify_client_id: str | None = None
        self.spotify_client_secret: str | None = None
        self.download_path: str = "songs"
        self.max_thread_workers: int = 10

        # Load settings from JSON file
        self.load()

    def save(self):
        self._save_json_settings()
        self._save_env_variables()
        print("Settings saved")

    def _save_json_settings(self):
        print("Saving settings to JSON file...")
        with open(self.settings_path, "w") as f:
            json.dump(
                {
                    "download_path": self.download_path,
                    "max_thread_workers": self.max_thread_workers,
                },
                f,
                indent=4,
            )

    def _save_env_variables(self):
        print("Saving env variables...")
        with open(self.env_path, "w") as f:
            f.write("# DO NOT SHARE THIS FILE\n")
            f.write(f"CLIENT_ID={self.spotify_client_id}\n")
            f.write(f"CLIENT_SECRET={self.spotify_client_secret}\n")

    def load(self):
        self._load_json_settings()
        self._load_env_variables()
        print("Settings loaded")

    def _load_json_settings(self):
        if not os.path.exists(self.settings_path):
            print("Settings file not found, using default settings...")
            return

        print("Loading settings from JSON file...")
        with open(self.settings_path, "r") as f:
            data: dict = json.load(f)
            self.download_path = data.get("download_path", self.download_path)
            self.max_thread_workers: int = data.get(
                "max_thread_workers", self.max_thread_workers
            )

    def _load_env_variables(self):
        if not os.path.exists(self.env_path):
            print("Env file not found, skipping...")
            return

        print("Loading env variables...")
        load_dotenv(self.env_path)
        spotify_client_id = os.getenv("CLIENT_ID", None)
        spotify_client_secret = os.getenv("CLIENT_SECRET", None)

        # Check for the string varient of the None type
        if spotify_client_id == "None" or spotify_client_secret == "None":
            print("Spotify credentials not found")
            return

        self.spotify_client_id = spotify_client_id
        self.spotify_client_secret = spotify_client_secret

    def get_spotify_credentials(self):
        return self.spotify_client_id, self.spotify_client_secret
