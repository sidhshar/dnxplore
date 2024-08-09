#!/bin/bash

# Variables
DB_HOST="13.201.96.49"            # MySQL Host (usually localhost)
DB_USER="speedscanuser"        # MySQL User
DB_PASSWORD="<pass>"    # MySQL Password
DB_NAME="dbspeedscan"    # MySQL Database name
BACKUP_DIR="/home/ubuntu/backups"    # Directory to store backups
DATE=$(date +'%Y-%m-%d_%H-%M-%S') # Date format for the backup file
BACKUP_FILE="$BACKUP_DIR/${DB_NAME}_backup_$DATE.sql" # Backup file name

# Create backup directory if it doesn't exist
mkdir -p $BACKUP_DIR

# Take a backup of the database
mysqldump -h $DB_HOST -u $DB_USER -p$DB_PASSWORD $DB_NAME > $BACKUP_FILE

# Optional: Compress the backup file
gzip $BACKUP_FILE

# Optional: Remove old backups (e.g., older than 4 weeks)
find $BACKUP_DIR -type f -name "*.gz" -mtime +28 -exec rm {} \;

# Log the backup status
echo "Backup for $DB_NAME completed at $DATE" >> $BACKUP_DIR/backup_log.txt
