
import os
import requests
import json
import time
from datetime import datetime
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from dotenv import load_dotenv

load_dotenv()
TMDB_API_KEY = os.getenv("TMDB_API_KEY")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
BLOG_URL = os.getenv("BLOG_URL")

def get_blog_id(service):
    print("📋 Mencari blog yang tersedia di akun kamu...")
    blogs = service.blogs().listByUser(userId='self').execute()
    if not blogs.get("items"):
        raise Exception("🚫 Tidak ada blog ditemukan di akun ini.")
    for blog in blogs["items"]:
        if BLOG_URL in blog["url"]:
            print(f"✅ Blog ditemukan: {blog['name']} ({blog['id']})")
            return blog["id"]
    raise Exception("❌ Blog tidak ditemukan. Pastikan BLOG_URL cocok.")

def get_trending_movies():
    url = f"https://api.themoviedb.org/3/trending/movie/day?api_key={TMDB_API_KEY}"
    res = requests.get(url)
    data = res.json()
    return data.get("results", [])  # ambil semua film trending

def generate_article(title, overview):
    if not overview:
        overview = "Deskripsi film belum tersedia."
    prompt = f"Buatkan artikel panjang (500 kata) tentang film '{title}'. Sinopsis: {overview}. Tambahkan opini pribadi dan ajakan menonton."

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "mistralai/mixtral-8x7b-instruct",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.8
    }

    try:
        r = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)
        res_json = r.json()
        if "error" in res_json:
            print(f"❌ OpenRouter API Error: {res_json['error']['message']}")
            return None
        return res_json["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"⚠️ Gagal generate artikel: {e}")
        return None

def post_to_blogger(service, blog_id, title, content):
    body = {
        "kind": "blogger#post",
        "title": title,
        "content": content
    }
    post = service.posts().insert(blogId=blog_id, body=body, isDraft=False).execute()
    print(f"✅ Diposting ke Blogger: {post['url']}")

def authenticate_blogger():
    creds = Credentials.from_authorized_user_file("token.json", ["https://www.googleapis.com/auth/blogger"])
    return build("blogger", "v3", credentials=creds)

def main():
    service = authenticate_blogger()
    blog_id = get_blog_id(service)
    trending = get_trending_movies()
    print(f"🎬 Total film trending hari ini: {len(trending)}\n")

    for idx, movie in enumerate(trending):
        title = movie.get("title", "Tanpa Judul")
        overview = movie.get("overview", "")
        print(f"✍️ [{idx+1}] Menulis artikel: {title}")
        article = generate_article(title, overview)
        if article:
            img_url = f"https://image.tmdb.org/t/p/w500{movie.get('poster_path', '')}"
            html_content = f"<h2>{title}</h2><img src='{img_url}'/><p>{article}</p>"
            post_to_blogger(service, blog_id, title, html_content)
        else:
            print(f"⛔ Gagal buat artikel: {title}")
        time.sleep(60)

if __name__ == "__main__":
    main()
