# Backup script for MySql

chmod +x mysql_backup.sh

crontab -e

Add the following line to schedule the backup script to run weekly (e.g., every Sunday at 2:00 AM):
0 2 * * 0 /home/ubuntu/scripts/mysql_backup.sh

Verify the Setup: Run the script manually to ensure it works:
./mysql_backup.sh

To confirm the cron job is set up correctly, you can
Check the /var/log/syslog file (or the cron log file) to see if the cron job ran as expected.

This setup ensures your MySQL database is backed up weekly, with older backups automatically deleted after 4 weeks (adjustable as needed).


