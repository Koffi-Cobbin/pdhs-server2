# "department"
    department_name VARCHAR(50) PRIMARY KEY, 
    college VARCHAR(50) NOT NULL, 
    faculty VARCHAR(50)
-- Database.insert("department",["Department of Computer Engineering", "College of Engineering", "Faculty of Computer Engineering"])


# "staff"
    staff_id INT PRIMARY KEY, 
    first_name VARCHAR(20) NOT NULL, 
    last_name VARCHAR(100) NOT NULL, 
    email VARCHAR(50) NOT NULL, 
    password VARCHAR(20) NOT NULL, 
    position VARCHAR(50) NOT NULL, 
    department_name VARCHAR(50) NOT NULL, 
    profile_image_link VARCHAR(100), 
    FOREIGN KEY (department_name) REFERENCES department(department_name)
-- Database.inser("staff", ["12345678", "Koffi", "Cobbin", "yaphetofori@gmail.com", "12345678", 
"Head of Department", "Department of Computer Engineering", "img_link"])


# "association"
    association_name VARCHAR(50) PRIMARY KEY,  
    department_name VARCHAR(50) NOT NULL, 
    patron INT NOT NULL, 
    FOREIGN KEY (department_name) REFERENCES department(department_name), 
    CONSTRAINT patron FOREIGN KEY (patron) REFERENCES staff(staff_id)"
-- Database.insert("association", ["Association of Computer Engineering Students", "Department of Computer Engineering", "12345678"])


# "student"
    student_id INT PRIMARY KEY, 
    first_name VARCHAR(20) NOT NULL, 
    last_name VARCHAR(100) NOT NULL, 
    email VARCHAR(50) NOT NULL, 
    password VARCHAR(20) NOT NULL, 
    position VARCHAR(50) NOT NULL, 
    department_name VARCHAR(50) NOT NULL, 
    association_name VARCHAR(50) NOT NULL, 
    profile_image_link VARCHAR(100), 
    FOREIGN KEY (department_name) REFERENCES department(department_name), 
    FOREIGN KEY (association_name) REFERENCES association(association_name)
-- Database.insert("student", ["12345678", "Koffi", "Cobbin", "yaphetofori@gmail.com", "password", "General Secretary", "Department of Computer Engineering", "Association of Computer Engineering Students", "img_link"])


# "document"
    document_id VARCHAR(20) PRIMARY KEY, 
    doc_name VARCHAR(50) NOT NULL, 
    doc_type VARCHAR(20) NOT NULL, 
    status VARCHAR(20), 
    upload_time DATETIME, 
    student_id INT NOT NULL, 
    staff_id INT NOT NULL, 
    FOREIGN KEY (student_id) REFERENCES student(student_id), 
    FOREIGN KEY (staff_id) REFERENCES staff(staff_id)

# "message"
    message_id INT PRIMARY KEY, 
    content VARCHAR(255) NOT NULL, 
    student_id INT NOT NULL, 
    staff_id INT NOT NULL, 
    FOREIGN KEY (student_id) REFERENCES student(student_id), 
    FOREIGN KEY (staff_id) REFERENCES staff(staff_id)

# "approval"
    document_id VARCHAR(20), 
    staff_id INT, 
    PRIMARY KEY (document_id,staff_id), 
    FOREIGN KEY (document_id) REFERENCES document(document_id), 
    FOREIGN KEY (staff_id) REFERENCES staff(staff_id)
