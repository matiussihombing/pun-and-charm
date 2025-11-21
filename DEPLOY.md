# How to Deploy "Pun & Charm" to Render.com

## Prerequisites
You need to have **Git** installed. If you saw a popup asking to install "Developer Tools" on your Mac, please click **Install**.

## Step 1: Create a GitHub Account
1. Go to [github.com](https://github.com) and create a free account.
2. Create a new repository (name it `pun-and-charm` or similar).
3. Make sure it is **Public** (easier) or Private.

## Step 2: Push Code to GitHub
Open your terminal (or ask me to do this part once you've installed the tools) and run:

```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/pun-and-charm.git
git push -u origin main
```
*(Replace `YOUR_USERNAME` with your actual GitHub username)*

## Step 3: Deploy on Render
1. Go to [render.com](https://render.com) and create a free account.
2. Click **"New +"** and select **"Web Service"**.
3. Connect your GitHub account and select the `pun-and-charm` repository.
4. Render will automatically detect the settings:
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
5. Click **"Create Web Service"**.

## Important Note about Data
Since we are using a simple local database (SQLite), **any new jokes or ratings submitted will be lost** whenever the website restarts or you deploy a new version. This is a limitation of the free cloud hosting. To fix this in the future, we would need to upgrade to a "PostgreSQL" database.
