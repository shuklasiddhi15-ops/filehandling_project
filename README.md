LIVE DEMO : https://filehandlingproject-8329towh8cgqxxpvpb5hzj.streamlit.app/
 
 # filehandling_project
 # 🗂️ File Handling System using Python

## 📌 Overview
A simple **menu-driven Python application** that performs **CRUD operations** (Create, Read, Update, Delete) on files, along with **Rename**, **Create Folder**, and **Delete Folder** functionalities — all built using core Python concepts like **functions, loops, and if-elif-else statements**.

## 🚀 Features
| Option | Operation | Description |
|--------|-----------|--------------|
| 1 | Create File | Creates a new file with user-entered content |
| 2 | Read File | Displays the content of an existing file |
| 3 | Update File | Appends new content to an existing file |
| 4 | Delete File | Deletes a file if it exists |
| 5 | Rename File | Renames an existing file |
| 6 | Create Folder | Creates a new folder/directory |
| 7 | Delete Folder | Deletes an existing folder |
| 0 | Exit | Exits the program |

## 🛠️ Technologies & Concepts Used
- **Language:** Python
- **Modules:** `os`, `pathlib.Path`
- **Concepts:** Functions, `while` loop, `if-elif-else`, file I/O (`open`, `read`, `write`, `append`)

## ⚙️ How It Works
1. The program shows a menu with numbered options.
2. User enters a choice (0–7).
3. Based on the choice, the respective function is called using `if-elif` conditions.
4. The `while True` loop keeps showing the menu until the user selects `0` to exit.
5. `Path.exists()` is used to check file/folder existence before performing operations, avoiding errors.


