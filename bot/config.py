import toml
import json
from pathlib import Path

VERSION = "0.0.1"

config_dir = Path(__file__).parent.parent.resolve() / "config"

config = None
with open(config_dir / "config.toml", "r") as f:
    config = toml.load(f)
    
telegram_token = config["telegram_token"]
download_dir = config["download_dir"]