🌀 Nameh – Real-Time Chat App with Django Channels


🚀 Project Overview

Nameh is a blazing-fast, real-time chat application built with Django Channels. Users can create private or group chat rooms, send messages and files, and see who’s online—all updated instantly without refreshing the page.

This project demonstrates a modern, production-ready Django setup with ASGI, WebSockets, user authentication, file uploads, and live online status tracking.

⚡ Key Features

💬 Real-Time Messaging: Powered by Django Channels and WebSockets.

🏷 Group & Private Chats: Create group chats or one-on-one chat rooms dynamically.

🔐 Authentication: Full login/signup flow using Django Allauth.

📁 File Uploads: Send files directly in the chat.

👥 Online Status: Live display of users currently online in a chat room.

✏️ Chat Management: Admins can edit, delete, or leave chatrooms.

🌍 Multi-Platform Friendly: Works in modern browsers with minimal latency.

🛠 Developer-Ready: Clean modular architecture, ready to scale.

🎨 Screenshots / Demo (optional)

(Add screenshots of your app here, e.g., chat room view, file upload, online status panel.)

🏗 Tech Stack
Layer	Technology
Backend	Django 5, Django Channels, Daphne
Frontend	Django Templates, HTMX
Database	SQLite (default, can switch to Postgres/MySQL)
Realtime	WebSockets (via Channels)
Authentication	Django Allauth
Misc	Django Browser Reload, Django Cleanup
📦 Installation & Setup
Requirements

Python 3.12+

Django 5.0+

Node.js (optional for frontend tooling)

Pip or Poetry

Steps
# Clone the repository
git clone https://github.com/alirzglshn/nameh.git
cd nameh

# Install dependencies
pip install -r requirements.txt

# Apply migrations
python manage.py migrate

# Create superuser (optional)
python manage.py createsuperuser

# Run development server
python manage.py runserver


💡 Pro Tip: Run with Daphne for full ASGI/WebSocket support:

daphne a_core.asgi:application

🌐 URLs / Routing Overview

/ – Main chat dashboard

/chat/<username> – Start or access a private chat

/chat/<chatroom_name>/ – Group chat room

/chat/new_groupchat/ – Create a new group chat

/chat/edit/<chatroom_name> – Edit chat room name (admin)

/chat/delete/<chatroom_name> – Delete a chat room (admin)

/chat/leave/<chatroom_name> – Leave a group chat

/chat/fileupload/<chatroom_name> – Upload files to chat

/@<username>/ – User profile pages

📄 Models Overview
ChatGroup

group_name – Unique identifier

groupchat_name – Display name

admin – User with admin privileges

users_online – Live online users

members – All chat participants

is_private – Privacy toggle

GroupMessage

group – ChatGroup reference

author – Message sender

body – Text content

file – Optional uploaded file

created – Timestamp

is_image – Helper property to check if file is an image

🔌 WebSocket Consumers

ChatroomConsumer – Handles sending and receiving messages in a chat room, updates online user count in real-time.

OnlineStatusConsumer – Tracks and broadcasts user online presence globally.

🛠 Forms

ChatmessageCreateForm – For sending text messages.

NewGroupForm – For creating new group chats.

ChatRoomEditForm – For editing group chat names.

💡 Tips for Developers

Keep DEBUG=True during development; use django_browser_reload for live page reloads.

Switch to Redis channel layer for production instead of InMemoryChannelLayer for scalability.

CSRF and security: ALLOWED_HOSTS and CSRF_TRUSTED_ORIGINS must be updated in production.

🏆 Why Nameh is Cool

Combines real-time WebSockets with Django’s robust backend.

Clean, modular architecture – easy to extend with features like emoji reactions, message search, or notifications.

Ready for production deployment with minimal tweaks.
