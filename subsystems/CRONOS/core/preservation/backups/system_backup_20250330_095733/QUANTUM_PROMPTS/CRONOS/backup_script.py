import os
import json
import shutil
import datetime
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger('CRONOS-Backup')

class CRONOSBackup:
    def __init__(self):
        self.config_path = Path(__file__).parent / "backup_config.json"
        self.project_root = Path("C:/Eva Guarani EGOS")
        self.load_config()
        
    def load_config(self):
        """Load backup configuration"""
        try:
            with open(self.config_path, 'r') as f:
                self.config = json.load(f)
            logger.info(f"Configuration loaded from {self.config_path}")
        except FileNotFoundError:
            logger.error(f"Configuration file not found at {self.config_path}")
            raise
        except json.JSONDecodeError:
            logger.error(f"Invalid JSON in configuration file {self.config_path}")
            raise
    
    def should_exclude(self, path):
        """Check if a path should be excluded based on config rules"""
        path_obj = Path(path)
        
        # Check if any parent directory should be excluded
        for part in path_obj.parts:
            if part in self.config["excluded_directories"]:
                return True
                
        # Check file extension
        if path_obj.is_file() and path_obj.suffix in self.config["excluded_extensions"]:
            return True
            
        return False
    
    def create_backup(self):
        """Create a backup excluding unnecessary directories"""
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_dir = self.project_root / Path(self.config["backup_location"]) / f"system_backup_{timestamp}"
        
        logger.info(f"Starting backup to {backup_dir}")
        
        # Create the backup directory
        os.makedirs(backup_dir, exist_ok=True)
        
        # Walk through the directory tree and copy files
        for root, dirs, files in os.walk(self.project_root):
            # Skip the backup directory itself to avoid recursion
            rel_path = os.path.relpath(root, self.project_root)
            if rel_path.startswith(self.config["backup_location"]):
                continue
                
            # Remove excluded directories from dirs list (modifies dirs in-place)
            dirs[:] = [d for d in dirs if d not in self.config["excluded_directories"]]
            
            # Process each file
            for file in files:
                src_path = os.path.join(root, file)
                
                # Skip excluded files
                if self.should_exclude(src_path):
                    continue
                    
                # Create the relative path for the destination
                rel_path = os.path.relpath(src_path, self.project_root)
                dst_path = os.path.join(backup_dir, rel_path)
                
                # Create parent directories if they don't exist
                os.makedirs(os.path.dirname(dst_path), exist_ok=True)
                
                # Copy the file
                try:
                    shutil.copy2(src_path, dst_path)
                except Exception as e:
                    logger.error(f"Failed to copy {src_path}: {e}")
        
        logger.info(f"Backup completed successfully at {backup_dir}")
        return backup_dir
    
    def clean_old_backups(self):
        """Clean old backups according to retention policy"""
        backup_base = self.project_root / Path(self.config["backup_location"])
        backups = []
        
        # List all backup directories
        for item in os.listdir(backup_base):
            if item.startswith("system_backup_"):
                backup_path = os.path.join(backup_base, item)
                if os.path.isdir(backup_path):
                    # Extract timestamp from directory name
                    try:
                        timestamp = datetime.datetime.strptime(
                            item.replace("system_backup_", ""), 
                            "%Y%m%d_%H%M%S"
                        )
                        backups.append((backup_path, timestamp))
                    except ValueError:
                        logger.warning(f"Could not parse timestamp from {item}")
        
        # Sort backups by timestamp (newest first)
        backups.sort(key=lambda x: x[1], reverse=True)
        
        # Keep the required number of backups
        daily_kept = 0
        weekly_kept = 0
        monthly_kept = 0
        
        today = datetime.datetime.now()
        keep_backup = set()
        
        for backup_path, timestamp in backups:
            # Calculate days, weeks, months difference
            days_diff = (today - timestamp).days
            
            if days_diff < 7 and daily_kept < self.config["retention_policy"]["daily"]:
                # Keep daily backup
                keep_backup.add(backup_path)
                daily_kept += 1
            elif days_diff < 30 and weekly_kept < self.config["retention_policy"]["weekly"]:
                # Keep weekly backup
                keep_backup.add(backup_path)
                weekly_kept += 1
            elif monthly_kept < self.config["retention_policy"]["monthly"]:
                # Keep monthly backup
                keep_backup.add(backup_path)
                monthly_kept += 1
        
        # Delete backups that should not be kept
        for backup_path, _ in backups:
            if backup_path not in keep_backup:
                logger.info(f"Deleting old backup: {backup_path}")
                try:
                    shutil.rmtree(backup_path)
                except Exception as e:
                    logger.error(f"Failed to delete {backup_path}: {e}")
        
        logger.info(f"Backup cleanup completed. Kept {len(keep_backup)} backups")


if __name__ == "__main__":
    try:
        backup = CRONOSBackup()
        backup_dir = backup.create_backup()
        backup.clean_old_backups()
        print(f"✅ Backup concluído com sucesso: {backup_dir}")
        print(f"✅ Limpeza de backups antigos concluída conforme política de retenção")
    except Exception as e:
        logger.error(f"Backup failed: {e}")
        print(f"❌ Falha no backup: {e}")
