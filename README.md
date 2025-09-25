🧑‍💼 JobSite – A Modern Job Portal with Live Chat

🌐 Live Demo: https://job-site-u07r.onrender.com

📖 About

JobSite is a full-featured job portal platform, inspired by Jobberman.com, built with Django.
It connects job seekers and employers in an interactive and efficient way.

✨ Key Features:

👔 Employers can create job postings, manage applications, and connect with talent.

📄 Applicants can register, build profiles, and apply for jobs.

💬 Live Chat for direct communication between employers and applicants.

🔎 Job Search & Filters (by category, location, and keywords).

🖼️ Media support for job descriptions and applicant resumes (PDF, DOC, etc.).

🔐 Secure authentication with password hashing (bcrypt).

⚡ Fast and lightweight deployment with Gunicorn, Waitress, and Whitenoise for static file management.

🛠️ Tech Stack

Backend: Django 5.0.7

Database: SQLite (default) → supports MySQL with mysql-connector

Authentication: Django Auth + Bcrypt password hashing

Frontend: Django Templates + Static files (CSS, JS, Images)

Deployment: Gunicorn, Waitress, Whitenoise

Environment Management: python-dotenv

📂 Project Structure
jobsite/
│── applicants/        # Applicant-related features (profiles, applications)
│── jobber/            # Employer/job posting logic
│── static/            # CSS, JS, Images
│── templates/         # HTML templates
│── thunder.db         # Default SQLite DB
│── manage.py          # Django project manager
│── Procfile           # Deployment process
│── requirements.txt   # Dependencies
│── .gitignore

📦 Installation

Clone the repository

git clone https://github.com/your-username/jobsite.git
cd jobsite


Create a virtual environment & activate it

python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows


Install dependencies

pip install -r requirements.txt


Set up environment variables
Create a .env file in the project root:

SECRET_KEY=your_secret_key_here
DEBUG=True
DATABASE_URL=sqlite:///thunder.db


Apply migrations

python manage.py migrate


Create a superuser (admin panel access)

python manage.py createsuperuser


Run the development server

python manage.py runserver

🚀 Deployment

This project is ready for deployment on Render, Heroku, or any cloud service.
Procfile & Gunicorn are included.

To deploy with Render:

Push code to GitHub.

Connect repository on Render
.

Add environment variables.

Deploy 🚀.

📌 Future Enhancements

AI-powered job recommendations.

Employer subscription plans.

Video interview scheduling.

Push notifications for new job postings.

👨‍💻 Author

Developed with ❤️ by Udemezue Uchechukwu Jude

📬 Feel free to contribute or fork this project!