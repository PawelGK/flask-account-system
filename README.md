# Flask Account System

A simple Flask web application that allows users to:
- Sign up
- Log in
- View their profile
- See their account creation date
- Log out

---

## Requirements

- Python 3
- MySQL
- pip packages:


## Database Setup

1. Open MySQL and create a database:

```sql
CREATE DATABASE minidb;
USE minidb;


CREATE TABLE accounts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    created_at DATETIME
);


