import random, os, time
from pathlib import Path
from datetime import datetime

print("=== BEYOND THOUGHT - FULL AUTO GENERATOR ===")

TOPICS = [
 "Why thought creates fear? - Krishnamurti",
 "Truth is a pathless land - No guru needed",
 "Observer is the observed - Deep truth",
 "You are the world - Krishnamurti",
 "Can mind be free from conditioning?",
 "Death is a great teacher",
 "Meditation is not control",
 "Love is not pleasure",
 "Relationship is a mirror",
 "Be a light to yourself",
 "Why we compare? Root of sorrow",
 "Can we live without conflict?",
 "Freedom from the self",
 "What is real silence?",
 "The ending of time",
 "Attention without effort",
 "Authority corrupts - Be free",
 "Can you end sorrow completely?",
 "Why mind seeks security?",
 "Happiness cannot be pursued",
]

for d in ["output","logs","data","temp"]: Path(d).mkdir(exist_ok=True)

topic = random.choice(TOPICS)
print(f"[TODAY] {topic}")

script = f"Beyond Thought - J Krishnamurti\nTopic: {topic}\n\nTruth is a pathless land. No organization, no guru can lead you to it.\n\n{topic} - Let's look.\n\nThought is response of memory. Memory is past. So thought is always old.\n\nObserve your fear. Not escape, but observe. In pure observation, there is ending.\n\nBe a light to yourself."

Path("output/script.txt").write_text(script)
print("[1/3] SCRIPT DONE")

try:
    from gtts import gTTS
    gTTS(text=script[:4000], lang='en', slow=False).save("output/voice.mp3")
    print("[2/3] VOICEOVER DONE")
except Exception as e:
    print(f"[2/3] VOICE ERROR: {e}")

try:
    from PIL import Image, ImageDraw
    img = Image.new('RGB', (1080,1920), color=(10,10,15))
    draw = ImageDraw.Draw(img)
    draw.text((80,800), "BEYOND THOUGHT", fill=(255,255,255))
    draw.text((80,900), topic[:45], fill=(200,200,200))
    img.save("temp/bg.jpg")
    os.system("ffmpeg -y -loop 1 -i temp/bg.jpg -i output/voice.mp3 -c:v libx264 -c:a aac -shortest -vf scale=1080:1920 output/final_video.mp4 > /dev/null 2>&1")
    print("[3/3] VIDEO DONE - output/final_video.mp4")
except Exception as e:
    print(f"[3/3] VIDEO ERROR: {e}")

# FIXED LOG
with open("logs/history.log","a") as f:
    f.write(f"{datetime.now()} - {topic}\n")

print(f"\n=== COMPLETE: {topic} ===")
print(f"Files ready for YouTube Shorts!")
