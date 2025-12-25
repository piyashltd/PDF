import os
import threading
import telebot
from weasyprint import HTML
from flask import Flask

# --- কনফিগারেশন ---
BOT_TOKEN = os.environ.get('BOT_TOKEN')
if not BOT_TOKEN:
    print("Error: BOT_TOKEN not found!")

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

# --- PDF জেনারেটর ফাংশন ---
def generate_pdf(filename):
    # আপনার প্রশ্নগুলো
    questions = [
        "১। কালিমা তাইয়্যিবাহ অর্থসহ বল।",
        "২। কালিমা শাহাদাত বল।",
        "৩। কালিমা তাওহীদ বল।",
        "৪। কালিমা তামজীদ বল।",
        "৫। আরবী হরফ কয়টি ও কী কী?",
        "৬। মাখরাজ কয়টি? প্রথম তিনটি মাখরাজ বল।",
        "৭। আরবী হরফে নোকতা কয়টি ও কী কী?",
        "৮। নিজ পড়া থেকে ৫টি প্রশ্ন!",
        "৯। হরকত কাকে বলে ও কী কী?",
        "১০। মাদ্দের হরফ কয়টি ও কী কী?",
        "১১। সূরা ফাতিহা তিলাওয়াত কর/লেখ।",
        "১২। ওস্তাদের সামনে বসার আদব কী?",
        "১৩। কোন দিকে ফিরে ইস্তিঞ্জা (প্রস্রাব-পায়খানা) করা নিষেধ?",
        "১৪। পুরুষের দায়িমী ফরজ কয়টি ও কি কি?",
        "১৫। মহিলার দায়িমী ফরজ কয়টি ও কি কি?",
        "১৬। আমাদের শেষ নবীর নাম, তাঁর পিতার নাম ও মাতার নাম কী?",
        "১৭। ওযু ও গোসলের ফরজ কয়টি ও কী কী?",
        "১৮। খাড়া জবর, খাড়া জের ও উল্টা পেশ থাকলে কিভাবে পড়তে হয়?",
        "১৯। সুন্দর করে সালাম দাও (আসসালামু আলাইকুম...)।",
        "২০। আরবী বারো মাসের নাম বল।"
    ]

    # HTML টেমপ্লেট (CSS সহ)
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            @font-face {{
                font-family: 'NotoBengali';
                src: url('NotoSerifBengali-Regular.ttf');
            }}
            body {{ font-family: 'NotoBengali', sans-serif; padding: 40px; }}
            .header {{ text-align: center; margin-bottom: 20px; }}
            .bismillah {{ font-size: 18px; font-weight: bold; }}
            .org-name {{ font-size: 22px; font-weight: bold; margin-top: 5px; }}
            .info-table {{ width: 100%; border-collapse: collapse; margin-top: 20px; border-bottom: 1px solid black; }}
            .info-table td {{ text-align: center; padding-bottom: 10px; font-weight: bold; }}
            .question-item {{ margin-bottom: 8px; font-size: 15px; }}
        </style>
    </head>
    <body>
        <div class="header">
            <div class="bismillah">বিসমিল্লাহির রহমানির রহিম</div>
            <div class="org-name">কৃষ্ণরামপুর পূর্ব-পাড়া জামে মসজিদ</div>
        </div>
        <table class="info-table">
            <tr>
                <td>তারিখঃ ৩০-১২-২০২৫</td>
                <td>বিভাগঃ মক্তব</td>
                <td>পূর্ণমানঃ ৫</td>
            </tr>
        </table>
        <br>
        <div>
            {''.join(f'<div class="question-item">{q}</div>' for q in questions)}
        </div>
    </body>
    </html>
    """
    
    # PDF তৈরি (base_url='.' দিলে ফন্ট ফাইল ফোল্ডার থেকে পাবে)
    HTML(string=html_content, base_url='.').write_pdf(filename)

# --- বট কমান্ড ---
@bot.message_handler(commands=['exam'])
def send_exam(message):
    chat_id = message.chat.id
    msg = bot.send_message(chat_id, "অপেক্ষা করুন, প্রশ্নপত্র তৈরি হচ্ছে...")
    filename = "Islamic_Exam.pdf"
    
    try:
        generate_pdf(filename)
        with open(filename, 'rb') as f:
            bot.send_document(chat_id, f, caption="এই নিন আপনার প্রশ্নপত্র।")
        bot.delete_message(chat_id, msg.message_id)
        os.remove(filename)
    except Exception as e:
        bot.send_message(chat_id, f"Error: {str(e)}")

# --- সার্ভার সেটআপ (Railway এর জন্য) ---
@app.route('/')
def index():
    return "Bot is running!"

def run_bot():
    bot.infinity_polling()

if __name__ == "__main__":
    # বটকে আলাদা থ্রেডে চালানো হচ্ছে
    t = threading.Thread(target=run_bot)
    t.start()
    
    # Flask অ্যাপ রান করা (Railway এর PORT ভেরিয়েবল ব্যবহার করবে)
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
