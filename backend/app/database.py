from app.config import settings
import logging

logger = logging.getLogger(__name__)

supabase = None

if settings.supabase_url and settings.supabase_service_key:
    try:
        from supabase import create_client, Client
        supabase = create_client(settings.supabase_url, settings.supabase_service_key)
        logger.info("Supabase client initialized")
    except Exception as e:
        logger.warning(f"Supabase init failed (using JSON): {e}")
        supabase = None
else:
    logger.info("No Supabase credentials — using JSON files")
