#!/bin/bash

# მონაცემთა ბაზის ინფორმაცია
USER="root"  # შეცვალეთ თქვენი MySQL-ის მომხმარებლის სახელი
PASSWORD="Ml_Root88"  # შეცვალეთ თქვენი MySQL-ის პაროლი
DATABASE="iesprojects"  # შეცვალეთ თქვენი მონაცემთა ბაზის სახელი
BACKUP_PATH="/iesprojects/backups/databases"
DATE=$(date +"%Y%m%d")

mkdir -p "$BACKUP_DIR"

# ბექაფის გაკეთება
docker exec mysql mysqldump -u $USER -p$PASSWORD $DATABASE > $BACKUP_PATH/${DATABASE}_backup_$DATE.sql

# ძველი ბექაფების წაშლა (მხოლოდ 7 ახალი ბექაფის შენახვა)
find $BACKUP_PATH -name "${DATABASE}_backup_*.sql" -mtime +7 -exec rm {} \;

# სექრეტული ინფორმაცია
echo "Backup completed for $DATABASE at $BACKUP_PATH/${DATABASE}_backup_$DATE.sql"
