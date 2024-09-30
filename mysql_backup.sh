#!/bin/bash

# მონაცემთა ბაზის ინფორმაცია
MYSQL_CONTAINER_NAME="mysql"    # Docker კონტეინერის სახელი
USER="root"     # შეცვალეთ თქვენი MySQL-ის მომხმარებლის სახელი
PASSWORD="Ml_Root88"    # შეცვალეთ თქვენი MySQL-ის პაროლი
DATABASE="iesprojects"  # შეცვალეთ თქვენი მონაცემთა ბაზის სახელი
BACKUP_PATH="/flask_app/backups/databases" # სერვერის დირექტორია, სადაც ბექაფი შეინახება
DATE=$(date +"%Y%m%d")

# შექმენით ბექაფის დირექტორია, თუ არ არსებობს
mkdir -p "$BACKUP_PATH"

# ბექაფის გაკეთება Docker კონტეინერიდან სერვერზე
docker exec $MYSQL_CONTAINER_NAME mysqldump -u $USER -p$PASSWORD $DATABASE > $BACKUP_PATH/${DATABASE}_backup_$DATE.sql

# ძველი ბექაფების წაშლა (მხოლოდ 7 ახალი ბექაფის შენახვა)
find $BACKUP_PATH -name "${DATABASE}_backup_*.sql" -mtime +7 -exec rm {} \;

# სექრეტული ინფორმაცია
echo "Backup completed for $DATABASE at $BACKUP_PATH/${DATABASE}_backup_$DATE.sql"
