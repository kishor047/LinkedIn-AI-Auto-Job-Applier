# LinkedIn AI Auto Job Applier

A Python-based bot that automates LinkedIn Easy Apply job applications. It searches for jobs based on your preferences, fills application forms, uploads your resume, and applies automatically.

## Features

- Apply to LinkedIn Easy Apply jobs automatically
- Search using multiple job titles
- Filter jobs by location, experience, and date posted
- Automatically answer common application questions
- Upload your resume
- Skip unwanted companies and keywords
- Save application history and logs

---

## Requirements

- Python 3.10+
- Google Chrome
- ChromeDriver (if required)
- LinkedIn Account

---

## Installation

1. Clone the repository.

```bash
git clone <repository-url>
cd <repository-folder>
```

2. Install the required packages.

```bash
pip install -r requirements.txt
```

3. Configure the files inside the `config` folder:

- `personals.py` – Personal details
- `questions.py` – Application answers
- `search.py` – Job search preferences
- `secrets.py` – LinkedIn credentials (optional)
- `settings.py` – Bot settings

4. Add your resume to the configured resume folder.

---

## How to Run

Run the bot:

```bash
python runAiBot.py
```

To view application history:

```bash
python app.py
```

Then open:

```
http://localhost:5000
```

---

## Folder Structure

```
config/
logs/
all resumes/
all excels/
runAiBot.py
app.py
requirements.txt
```

---

## Notes

- Use **Easy Apply** for best results.
- Test with a few applications before running continuously.
- Keep your configuration files updated.
- Run the bot responsibly and follow LinkedIn's Terms of Service.

---

## Disclaimer

This project is intended for educational purposes only. Use it responsibly and at your own risk.
