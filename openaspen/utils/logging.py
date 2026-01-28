import logging
import sys
from typing import Optional


def setup_logging(level: Optional[str] = None) -> None:
    log_level = level or "INFO"
    
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    logging.getLogger("openaspen").setLevel(getattr(logging, log_level.upper()))
