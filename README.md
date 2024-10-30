Simple Social API
A basic backend API built with FastAPI and PostgreSQL for a social platform where users can create accounts, log in, and interact by sharing and retrieving posts. Users can also vote on posts, enabling a simple voting system.

Features
User Authentication
Register and log in with secure password hashing.
On each login, a unique token is generated for the user, allowing limited-time access.
Action Authorization
The token is required for all user actions, verifying that the user is authorized to interact with the platform.
Post Creation
Authenticated users can create and share posts.
Post Retrieval
Retrieve all posts or specific posts by ID.
Voting System
Users can upvote or downvote posts.
Tech Stack
FastAPI: For creating a high-performance API.
PostgreSQL: Database to store users, posts, and votes.
JWT Authentication: JSON Web Tokens (JWTs) are generated on each login, allowing secure, time-bound access and ensuring that users are authorized to perform actions.
Getting Started
Prerequisites
Python (3.7 or higher)
PostgreSQL database
