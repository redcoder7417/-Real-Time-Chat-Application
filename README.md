
Real-Time Chat Application

This is a simple real-time chat application built using Flask, HTML, CSS, and JavaScript. The app enables users to register, log in, and communicate with others in real-time through a dynamic chat interface. The backend handles user authentication, stores messages in a database, and supports real-time updates through AJAX. The application is fully responsive, ensuring it works seamlessly across both mobile and desktop devices.

Key Features:
User Authentication

Secure registration and login system with password hashing.
Session management to keep users logged in for 30 minutes of inactivity.
Real-Time Messaging

Messages are updated in real-time via AJAX, without the need for page reloads.
Latest messages are fetched every 2 seconds to keep the chat updated.
Database Integration

SQLite is used to persist user data and chat messages.
Each message is linked to the corresponding user for easy tracking.
Responsive Design

Fully optimized for mobile, tablet, and desktop screens using CSS media queries.
Clean and user-friendly interface for ease of use.
Security Measures

Input sanitization to prevent XSS attacks.
Passwords are stored securely using hashed values.
Tech Stack:
Backend: Flask (Python)
Frontend: HTML, CSS, JavaScript
Database: SQLite
