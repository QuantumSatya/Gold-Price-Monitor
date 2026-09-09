# 24K Gold Manual Reference Cloud Monitor

Enter any reference date, reference 24K price, and threshold in the dashboard.

The cloud cron checks Goodreturns 24K India every 15 minutes. It emails the configured recipient if the current price is at least the threshold below or above your manually entered reference.

Gmail:
- SMTP_USERNAME is prefilled with satyajeetpatil1992@gmail.com
- Add SMTP_APP_PASSWORD in Render as a secret
- Never put the normal Gmail password in GitHub.

Important: this uses the published Goodreturns 24K rate, not an intraday high.
