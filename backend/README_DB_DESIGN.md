# Database Design – README

## Overview

This project follows the provided **System Requirement Document**, but the database is designed in a clean and safe way so that:

- Data stays consistent
- Future changes are easy
- Duplicate structures are avoided
- API behavior stays exactly the same

Only the **database structure** is improved.  
**API endpoints and responses are unchanged.**

---

## Main Rule We Followed

> The database stores only real (source-of-truth) data.  
> Calculated values are computed in code.  
> Structured lists are stored as tables, not JSON.

This avoids bugs and makes the system easier to maintain.

---

## Authentication

🔒 **Auth models are unchanged.**

Authentication logic and tables are exactly the same as before.  
No redesign or refactor was done for auth.

---

## Training Model

### What the docs say
- Training has price, discount, benefits, mentors
- `effective_price` is auto-calculated

### What we did

#### 1. `effective_price` is NOT stored
- It depends on base price and discount
- Storing it could become incorrect later

**Simple reason:**  
If a value can be calculated, we should not store it.

---

#### 2. Benefits are stored in a separate table
- Docs say “array of strings”
- Benefits can be edited, reordered, or removed

**Simple reason:**  
Arrays are for APIs, tables are for databases.

---

#### 3. Mentors are stored in their own table
- Mentors are real people
- One mentor can belong to multiple trainings

**Simple reason:**  
Reusable data should not be stored as JSON.

---

## Services Model

### What the docs say
- Services have pricing, tech stack, offerings

### What we did
- Same pricing logic as Training
- `effective_price` is calculated, not stored
- `tech_stack` and `offerings` stored as JSON

**Why JSON is OK here**
- Simple lists
- No reuse
- No ordering needed

---

## Team & Intern Models

### What the docs say
- Intern has the same structure as Team

### What we did
- Used one table for both
- Added a `role` field (TEAM / INTERN)

**Simple reason:**  
Same structure means one table with different roles.

---

## Job & Internship Models

### What the docs say
- Job and Internship have the same structure

### What we did
- Used one table for both
- Added a `type` field (JOB / INTERNSHIP)
- Requirements stored in a separate table

**Simple reason:**  
One structure = one table, type tells the difference.

---

## Projects & Feedback

### What the docs say
- Projects have feedbacks

### What we did
- Projects stored in one table
- Feedback stored in a separate table

**Simple reason:**  
Feedback has its own data (rating, text, client info).

---

## Enums Usage

Enums are used for:
- Discount type
- Member role
- Opportunity type

**Simple reason:**  
Enums prevent invalid values and make future changes easier.

---

## API Compatibility

- All APIs work exactly as documented
- Arrays and embedded objects are returned by the API
- Database structure is hidden from API users

---

## One-Line Summary

> We followed the documentation for API behavior, but designed the database to store only source-of-truth data, normalize structured fields, and calculate derived values to keep the system correct and scalable.
