# WhatsApp Integration Test

This project demonstrates the integration of WhatsApp messaging with Django. It includes features like message sending, receiving webhook events, and a dashboard to view message logs.

---

## Installation and Setup

Follow the steps below to set up and run the project.

### 1. Clone the Repository

```bash
    git clone https://github.com/pareshinx/WhatsApp-Integration-Test.git
```

### 2. Set Environment Variables
Create a .env file in the project directory and specify the following environment variables:

```bash
    DJANGO_SECRET_KEY='django-insecure-#jk42y2oxghi1+z1057^tchr8o7!571yi!by&iqs5h5i4y@h#='
    WHATSAPP_PHONE_ID=<WHATSAPP_PHONE_ID>
    META_API_DOMAIN='https://graph.facebook.com/v21.0'
    WHATSAPP_API_ACCESS_TOKEN=<WHATSAPP_API_ACCESS_TOKEN>
    VERIFICATION_TOKEN='Z30uDImZOBthA3a3OpbqcD12xS5EsWKtZXHRp7FvOAKS1PbhtOVjfcDSKRTvjhVp'
    SENDER_PHONE_NUMBER="<WHATSAPP_TEST_SENDER_PHONE_NUMBER>"
```
### 3. Create Virtual Environment

```bash
  python -m venv myenv
```

### 4. Activate Virtual Environment

```bash
  source myenv/bin/activate
```
### 5. Go to root folder

```bash
    cd whatsapp_integration
```
### 6. Install Dependencies
Install the required python packages
```bash
  pip install -r requirements.txt
```

### 7. Apply Database Migrations
Run the following command to set up a database
```bash
  python manage.py migrate
```

### 8. Create Superuser
To access the Django admin panel, create a superuser
```bash
  python manage.py createsuperuser
```

### 9. Run the project
Start the Django development server
```bash
  python manage.py runserver
```