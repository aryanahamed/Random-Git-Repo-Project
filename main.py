import requests
import random
from flask import Flask, render_template

def fetch_trending_repos():
    url = "https://api.github.com/search/repositories"
    params = {
        "q": "stars:>20000",
        "sort": "stars",
        "order": "asc"
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        repos = response.json()["items"]
        return repos
    else:
        return []

repos = fetch_trending_repos()

def select_random_repo():
    global repos
    if not repos:
        repos = fetch_trending_repos()
    repo = random.choice(repos)
    repos.remove(repo)
    return repo

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/random-repo')
def random_repo():
    repo = select_random_repo()
    if repo:
        return repo['html_url']
    else:
        return "No trending repositories found", 404

if __name__ == "__main__":
    app.run(debug=True)