#!/bin/bash

# შეამოწმეთ, გადმოცემულია თუ არა ზუსტად 2 არგუმენტი (სორსი და მიზანი)
if [ $# -ne 2 ]; then
    echo "უნდა გადასცეთ ზუსტად 2 არგუმენტი: <სორსი> <მიზანი>"
    echo "გამოყენების მაგალითი: uploads_backup.sh <source> <target>"
    echo "გთხოვთ, სცადეთ თავიდან."
    exit 1
fi

SOURCE=$1      # სორსის დირექტორია
TARGET=$2      # მიზნის დირექტორია

# შეამოწმეთ, არის თუ არა `rsync` ინსტალირებული სისტემაში
if ! command -v rsync > /dev/null 2>&1; then
    echo "ეს სკრიპტი საჭიროებს rsync ინსტრუმენტის ინსტალაციას."
    echo "Ubuntu-სთვის: sudo apt install rsync"
    exit 2
fi

# მიმდინარე თარიღის მიღება ფორმატით YYYY-MM-DD
CURRENT_DATE=$(date +%Y-%m-%d)

# ბექაფის დირექტორიის განსაზღვრა (თარიღის მიხედვით)
BACKUP_DIR="${TARGET}/${CURRENT_DATE}"

# შექმენით ბექაფის დირექტორია, თუ ის არ არსებობს
mkdir -p "$BACKUP_DIR"

# ლოგ-ფაილის განსაზღვრა ბექაფის პროცესისთვის
LOG_FILE="${BACKUP_DIR}/backup_${CURRENT_DATE}.log"

# rsync-ის ოპციების განსაზღვრა
RSYNC_OPTIONS="-av --delete"

# შეასრულეთ ბექაფი `rsync`-ის გამოყენებით და დაწერეთ ლოგ-ფაილში
echo "ბექაფის დაწყება: $(date)" >> "$LOG_FILE"
rsync $RSYNC_OPTIONS "$SOURCE" "$BACKUP_DIR" >> "$LOG_FILE" 2>&1 || {
    echo "Rsync ვერ შესრულდა. გადახედეთ ლოგ-ფაილს: $LOG_FILE"
    exit 3
}

# ძველი ბექაფების წაშლა: მხოლოდ 7 ახალი ბექაფის დატოვება
echo "ძველი ბექაფების გაწმენდა..." >> "$LOG_FILE"
ls -1dt "${TARGET}/"20[0-9][0-9]-[0-9][0-9]-[0-9][0-9] | tail -n +8 | xargs -r rm -rf >> "$LOG_FILE" 2>&1

# დასრულების შეტყობინება ლოგ-ფაილში
echo "ბექაფი წარმატებით დასრულდა: $(date)" >> "$LOG_FILE"
