import subprocess
import time
from publish2GSheet import update_sheet, get_values

#  Liste des vidéos à lire (remplace ces liens par ceux de ton choix)
video_playlist = [
    "https://www.youtube.com/watch?v=XQ0B0cjq1-U",
    "https://www.youtube.com/watch?v=dQw4w9WgXcQ", 
    "https://www.youtube.com/watch?v=3JZ_D3ELwOQ"
]

def get_video_url(youtube_url):
    """Utilise yt-dlp pour récupérer l'URL directe du flux vidéo."""
    try:
        result = subprocess.run(
            ["yt-dlp", "-f", "best", "-g", youtube_url],
            capture_output=True, text=True, check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        print(f" Erreur lors de la récupération du lien pour {youtube_url}")
        return None

def play_videos(video_urls):
    """Joue les vidéos une par une avec mpv."""
    for url in video_urls:
        print(f" Lecture de : {url}")
        video_stream_url = get_video_url(url)
        info = get_values()
        title = info[0][3]
        channel = info[0][4]
        update_sheet("Sheet1", url, title, channel)
        if video_stream_url:
            subprocess.run([
                "mpv", 
                "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36", 
                "--fullscreen", 
                video_stream_url
            ])
        print(" Pause de 5 secondes avant la prochaine vidéo...")

        time.sleep(5)

if __name__ == "__main__":
    print(f" {len(video_playlist)} vidéos à lire.")
    play_videos(video_playlist)
    print(" Lecture terminée !")
