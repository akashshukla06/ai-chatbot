import os
import pymysql
import pymysql.cursors
from dotenv import load_dotenv
import bcrypt

load_dotenv()

DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
DB_PORT = int(os.getenv("DB_PORT", "3306"))
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "123456")
DB_NAME = os.getenv("DB_NAME", "abes_portal")


def get_server_connection():
    """Connect to MySQL server without selecting a database."""
    return pymysql.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=True
    )


def get_db_connection():
    """Connect to the specific application database."""
    return pymysql.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=True
    )


def check_db_health():
    """Check if MySQL is reachable and responsive."""
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute("SELECT 1 as is_alive;")
            result = cursor.fetchone()
        conn.close()
        return result and result.get("is_alive") == 1
    except Exception as e:
        print(f"Database health check error: {e}")
        return False


def hash_pwd(plain_password: str) -> str:
    """Hash password using bcrypt."""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(plain_password.encode("utf-8"), salt).decode("utf-8")


def init_db():
    """
    Initialize MySQL schema and seed baseline demonstration data.
    Ensures safe, idempotent creation of tables, foreign keys, and records.
    """
    # 1. Create database if it does not exist
    server_conn = get_server_connection()
    with server_conn.cursor() as cursor:
        cursor.execute(
            f"CREATE DATABASE IF NOT EXISTS `{DB_NAME}` "
            f"CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
        )
    server_conn.close()

    # 2. Connect to the database and create tables
    conn = get_db_connection()
    with conn.cursor() as cursor:
        # Students Table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS `students` (
            `id` INT AUTO_INCREMENT PRIMARY KEY,
            `student_id` VARCHAR(50) UNIQUE NOT NULL,
            `name` VARCHAR(100) NOT NULL,
            `email` VARCHAR(100) UNIQUE NOT NULL,
            `password_hash` VARCHAR(255) NOT NULL,
            `course` VARCHAR(50) NOT NULL,
            `branch` VARCHAR(100) NOT NULL,
            `semester` INT NOT NULL,
            `section` VARCHAR(20) NOT NULL,
            `enrollment_year` INT NOT NULL,
            `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        """)

        # Admins Table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS `admins` (
            `id` INT AUTO_INCREMENT PRIMARY KEY,
            `username` VARCHAR(50) UNIQUE NOT NULL,
            `password_hash` VARCHAR(255) NOT NULL,
            `name` VARCHAR(100) NOT NULL,
            `email` VARCHAR(100) UNIQUE NOT NULL,
            `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        """)

        # Subjects Table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS `subjects` (
            `id` INT AUTO_INCREMENT PRIMARY KEY,
            `subject_code` VARCHAR(20) UNIQUE NOT NULL,
            `subject_name` VARCHAR(100) NOT NULL,
            `semester` INT NOT NULL,
            `branch` VARCHAR(100) NOT NULL
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        """)

        # Student Subjects Mapping
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS `student_subjects` (
            `id` INT AUTO_INCREMENT PRIMARY KEY,
            `student_id` INT NOT NULL,
            `subject_id` INT NOT NULL,
            FOREIGN KEY (`student_id`) REFERENCES `students`(`id`) ON DELETE CASCADE,
            FOREIGN KEY (`subject_id`) REFERENCES `subjects`(`id`) ON DELETE CASCADE,
            UNIQUE KEY `uq_student_subject` (`student_id`, `subject_id`)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        """)

        # Attendance Table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS `attendance` (
            `id` INT AUTO_INCREMENT PRIMARY KEY,
            `student_id` INT NOT NULL,
            `subject_id` INT NOT NULL,
            `total_classes` INT NOT NULL DEFAULT 0,
            `attended_classes` INT NOT NULL DEFAULT 0,
            `attendance_percentage` DECIMAL(5,2) NOT NULL DEFAULT 0.00,
            `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            FOREIGN KEY (`student_id`) REFERENCES `students`(`id`) ON DELETE CASCADE,
            FOREIGN KEY (`subject_id`) REFERENCES `subjects`(`id`) ON DELETE CASCADE,
            UNIQUE KEY `uq_student_attendance` (`student_id`, `subject_id`)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        """)

        # Exams Table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS `exams` (
            `id` INT AUTO_INCREMENT PRIMARY KEY,
            `subject_id` INT NOT NULL,
            `exam_type` VARCHAR(50) NOT NULL,
            `exam_date` DATE NOT NULL,
            `start_time` TIME NOT NULL,
            `end_time` TIME NOT NULL,
            `room` VARCHAR(50) NOT NULL,
            FOREIGN KEY (`subject_id`) REFERENCES `subjects`(`id`) ON DELETE CASCADE
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        """)

        # Notices Table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS `notices` (
            `id` INT AUTO_INCREMENT PRIMARY KEY,
            `title` VARCHAR(255) NOT NULL,
            `description` TEXT NOT NULL,
            `category` VARCHAR(50) NOT NULL,
            `notice_date` DATE NOT NULL,
            `source_url` VARCHAR(255) DEFAULT '',
            `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        """)

        # Chat History Table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS `chat_history` (
            `id` INT AUTO_INCREMENT PRIMARY KEY,
            `student_id` INT NOT NULL,
            `question` TEXT NOT NULL,
            `answer` TEXT NOT NULL,
            `matched_question` VARCHAR(255) DEFAULT '',
            `source` VARCHAR(100) DEFAULT '',
            `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (`student_id`) REFERENCES `students`(`id`) ON DELETE CASCADE
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        """)

        # Knowledge Base Table (Mirrors abes_knowledge.csv for Admin Management)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS `abes_knowledge` (
            `id` INT AUTO_INCREMENT PRIMARY KEY,
            `question` VARCHAR(255) NOT NULL,
            `answer` TEXT NOT NULL,
            `category` VARCHAR(50) NOT NULL,
            `source` VARCHAR(100) NOT NULL,
            `source_url` VARCHAR(255) DEFAULT '',
            `last_verified` DATE NOT NULL,
            `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        """)

        # 3. Seed demo accounts if empty
        cursor.execute("SELECT COUNT(*) as cnt FROM `students`;")
        student_count = cursor.fetchone()["cnt"]

        if student_count == 0:
            print("Seeding initial student accounts...")
            # Hash default password
            hashed_p1 = hash_pwd("123456")
            hashed_p2 = hash_pwd("password123")

            cursor.execute("""
            INSERT INTO `students`
            (`student_id`, `name`, `email`, `password_hash`, `course`, `branch`, `semester`, `section`, `enrollment_year`)
            VALUES
            ('AK0001', 'Akash Shukla', 'akashshukla94097@gmail.com', %s, 'B.Tech', 'Computer Science and Engineering', 5, 'CSE-12', 2023),
            ('AKTU002', 'Priya Sharma', 'priya.it@abes.ac.in', %s, 'B.Tech', 'Information Technology', 6, 'IT-1', 2023);
            """, (hashed_p1, hashed_p2))

        # Seed admin account if empty
        cursor.execute("SELECT COUNT(*) as cnt FROM `admins`;")
        admin_count = cursor.fetchone()["cnt"]
        if admin_count == 0:
            print("Seeding admin account...")
            hashed_admin_pwd = hash_pwd("Admin@123")
            cursor.execute("""
            INSERT INTO `admins` (`username`, `password_hash`, `name`, `email`)
            VALUES ('admin', %s, 'Portal Administrator', 'admin@abes.ac.in');
            """, (hashed_admin_pwd,))

        # Seed subjects if empty
        cursor.execute("SELECT COUNT(*) as cnt FROM `subjects`;")
        subject_count = cursor.fetchone()["cnt"]
        if subject_count == 0:
            print("Seeding academic subjects...")
            cursor.execute("""
            INSERT INTO `subjects` (`subject_code`, `subject_name`, `semester`, `branch`)
            VALUES
            ('KCS601', 'Software Engineering', 6, 'Computer Science and Engineering'),
            ('KCS602', 'Web Technology', 6, 'Computer Science and Engineering'),
            ('KCS603', 'Computer Networks', 6, 'Computer Science and Engineering'),
            ('KCS061', 'Big Data', 6, 'Computer Science and Engineering'),
            ('KCS651', 'Software Engineering Lab', 6, 'Computer Science and Engineering');
            """)

        # Seed student_subjects and attendance for ALL students
        cursor.execute("SELECT id, student_id FROM `students`;")
        all_students = cursor.fetchall()
        cursor.execute("SELECT id, subject_code FROM `subjects`;")
        subs = cursor.fetchall()

        for st in all_students:
            s_id = st["id"]
            cursor.execute("SELECT COUNT(*) as cnt FROM `student_subjects` WHERE `student_id` = %s;", (s_id,))
            ss_cnt = cursor.fetchone()["cnt"]
            if ss_cnt == 0 and subs:
                for sub in subs:
                    cursor.execute("""
                    INSERT IGNORE INTO `student_subjects` (`student_id`, `subject_id`)
                    VALUES (%s, %s);
                    """, (s_id, sub["id"]))

                attendance_data = [
                    (s_id, subs[0]["id"], 42, 38, 90.48),
                    (s_id, subs[1]["id"], 40, 35, 87.50),
                    (s_id, subs[2]["id"], 44, 37, 84.09),
                    (s_id, subs[3]["id"], 36, 31, 86.11),
                    (s_id, subs[4]["id"], 14, 13, 92.86),
                ]
                for att in attendance_data:
                    cursor.execute("""
                    INSERT IGNORE INTO `attendance`
                    (`student_id`, `subject_id`, `total_classes`, `attended_classes`, `attendance_percentage`)
                    VALUES (%s, %s, %s, %s, %s);
                    """, att)

                # Seed upcoming exams
                cursor.execute("SELECT COUNT(*) as cnt FROM `exams`;")
                exam_cnt = cursor.fetchone()["cnt"]
                if exam_cnt == 0:
                    exams_data = [
                        (subs[0]["id"], "Pre-University Exam (PUE)", "2026-10-15", "10:00:00", "13:00:00", "B-Block 302"),
                        (subs[1]["id"], "Pre-University Exam (PUE)", "2026-10-17", "10:00:00", "13:00:00", "B-Block 304"),
                        (subs[2]["id"], "Pre-University Exam (PUE)", "2026-10-19", "10:00:00", "13:00:00", "B-Block 302"),
                        (subs[3]["id"], "Pre-University Exam (PUE)", "2026-10-21", "10:00:00", "13:00:00", "C-Block 201"),
                    ]
                    for ex in exams_data:
                        cursor.execute("""
                        INSERT INTO `exams` (`subject_id`, `exam_type`, `exam_date`, `start_time`, `end_time`, `room`)
                        VALUES (%s, %s, %s, %s, %s, %s);
                        """, ex)

        # Seed notices if empty
        cursor.execute("SELECT COUNT(*) as cnt FROM `notices`;")
        notices_count = cursor.fetchone()["cnt"]
        if notices_count == 0:
            print("Seeding official ABES notices...")
            cursor.execute("""
            INSERT INTO `notices` (`title`, `description`, `category`, `notice_date`, `source_url`)
            VALUES
            ('Pre-University Examination (PUE) Schedule Announced',
             'The schedule for Pre-University Examination for B.Tech 6th semester students has been published. Exams commence from October 15, 2026.',
             'Examination', '2026-09-28', 'https://www.abes.ac.in/circulars.html'),
            ('Submission of UP Government Post-Matric Scholarship Forms',
             'Eligible students must submit hard copies of their UP Scholarship online application along with required documents to Student Welfare by October 25, 2026.',
             'Scholarship', '2026-09-25', 'https://www.abes.ac.in/circulars.html'),
            ('Campus Placement Drive - Leading Tech MNCs for 2026/2027 Batches',
             'Registration is open for upcoming campus recruitment drives. Eligible candidates must ensure updated profiles with the Training & Placement Cell.',
             'Placement', '2026-09-22', 'https://www.abes.ac.in/circulars.html'),
            ('Mandatory Academic Bank of Credits (ABC) ID Verification',
             'All students must link their ABC ID on the AKTU ERP portal to avoid examination registration delays.',
             'Academic', '2026-09-18', 'https://www.abes.ac.in/circulars.html'),
            ('Central Library Timing Extension During Examination Period',
             'The central library will remain open from 8:00 AM to 10:00 PM on all working days and weekends during the examination preparatory period.',
             'General', '2026-09-15', 'https://www.abes.ac.in/circulars.html');
            """)

    conn.close()
    print("Database initialization and verification completed successfully!")


if __name__ == "__main__":
    init_db()
