#!/bin/bash

# -------- LOAD .env VARIABLES --------
ENV_FILE="/home/iesflask/IesProjects/.env"

if [ -f "$ENV_FILE" ]; then
    set -a 
    . "$ENV_FILE"
    set +a
else
    echo "❌ .env ფაილი არ მოიძებნა: $ENV_FILE"
    exit 1
fi

# -------- MYSQL BACKUP --------

DB_BACKUP_PATH="/flask_app/backups/IesProjects/databases"
DATE=$(date +"%Y%m%d")
SQL_FILE="${DB_BACKUP_PATH}/${MYSQL_DATABASE}_backup_${DATE}.sql"
LOG_FILE="${DB_BACKUP_PATH}/${MYSQL_DATABASE}_backup_${DATE}.log"

# შექმენით ბექაფის დირექტორია, თუ არ არსებობს
mkdir -p "$DB_BACKUP_PATH"

# ბექაფის ლოგის შექმნა და შესრულება
{
    echo "📅 ბექაფის დაწყება: $(date)"
    
    docker exec "$MYSQL_CONTAINER_NAME" \
        mysqldump -u "$MYSQL_ROOT_USER" -p"$MYSQL_ROOT_PASSWORD" "$MYSQL_DATABASE" > "$SQL_FILE"

    if [ $? -eq 0 ]; then
        echo "✅ MySQL ბექაფი წარმატებით დასრულდა: $SQL_FILE"
    else
        echo "❌ ბექაფის შეცდომა!"
        rm -f "$SQL_FILE"
        exit 2
    fi
} >> "$LOG_FILE" 2>&1

# ძველი SQL და ლოგ ფაილების წაშლა (7 დღეზე უფროსი)
find "$DB_BACKUP_PATH" -name "${MYSQL_DATABASE}_backup_*.sql" -mtime +7 | while read OLD_SQL; do
    OLD_LOG="${OLD_SQL%.sql}.log"
    echo "🗑️ წაშლა: $OLD_SQL" >> "$LOG_FILE"
    rm -f "$OLD_SQL"
    [ -f "$OLD_LOG" ] && rm -f "$OLD_LOG"
done

echo "🎉 ყველა ბექაფი წარმატებით დასრულდა: $(date)" >> "$LOG_FILE"

# -------- UPLOADS BACKUP --------

SOURCE="/home/iesflask/IesProjects/uploads"
UPLOAD_BACKUP_ROOT="/flask_app/backups/IesProjects/uploads"
CURRENT_DATE=$(date +%Y-%m-%d)
UPLOAD_BACKUP_DIR="${UPLOAD_BACKUP_ROOT}/${CURRENT_DATE}"

# შეამოწმეთ, არის თუ არა rsync ინსტალირებული
if ! command -v rsync > /dev/null 2>&1; then
    echo "❌ Rsync ინსტალირებული არ არის. Ubuntu-ზე დააყენეთ: sudo apt install rsync"
    exit 2
fi

# ბექაფის დირექტორია და ლოგ ფაილი
mkdir -p "$UPLOAD_BACKUP_DIR"
LOG_FILE="${UPLOAD_BACKUP_DIR}/backup_${CURRENT_DATE}.log"

# ატვირთვების ბექაფი
echo "ბექაფის დაწყება: $(date)" >> "$LOG_FILE"
rsync -av --delete "$SOURCE/" "$UPLOAD_BACKUP_DIR/" >> "$LOG_FILE" 2>&1 || {
    echo "❌ Rsync ვერ შესრულდა. გადაამოწმეთ ლოგი: $LOG_FILE"
    exit 3
}

# ძველი ატვირთვების ბექაფების წაშლა (მხოლოდ 7 დაიტოვოს)
echo "ძველი ატვირთვების ბექაფების წაშლა..." >> "$LOG_FILE"
ls -1dt "${UPLOAD_BACKUP_ROOT}/"20[0-9][0-9]-[0-9][0-9]-[0-9][0-9] | tail -n +8 | xargs -r rm -rf >> "$LOG_FILE" 2>&1

echo "✅ ატვირთვების ბექაფი წარმატებით დასრულდა: $(date)" >> "$LOG_FILE"
