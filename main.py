import os
import telebot
from weasyprint import HTML, CSS
from weasyprint.text.fonts import FontConfiguration

# Railway ভেরিয়েবল থেকে টোকেন
BOT_TOKEN = os.environ.get('BOT_TOKEN') 
bot = telebot.TeleBot(BOT_TOKEN)

def generate_pdf(filename):
    # প্রশ্ন এবং তথ্য
    date = "৩০-১২-২০২৫"
    dept = "মক্তব"
    marks = "৫"
    
    questions = [
        "১। কালিমা তাইয়্যিবাহ অর্থসহ বল।",
        "২। কালিমা শাহাদাত বল।",
        "৩। কালিমা তাওহীদ বল।",
        "৪। কালিমা তামজীদ বল।",
        "৫। আরবী হরফ কয়টি ও কী কী?",
        "৬। মাখরাজ কয়টি? প্রথম তিনটি মাখরাজ বল।",
        "৭। আরবী হরফে নোকতা কয়টি ও কী কী? (এক নোকতা, দুই নোকতা...)।",
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

    # HTML টেমপ্লেট তৈরি (CSS সহ)
    # খেয়াল করুন: font-family তে আপনার ফন্ট ফাইলের নাম সঠিক হতে হবে
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            @font-face {{
                font-family: 'NotoBengali';
                src: url('NotoSerifBengali-Regular.ttf');
            }}
            body {{
                font-family: 'NotoBengali', sans-serif;
                padding: 40px;
                font-size: 14px;
            }}
            .header {{
                text-align: center;
                margin-bottom: 20px;
            }}
            .bismillah {{
                font-size: 18px;
                font-weight: bold;
                margin-bottom: 5px;
            }}
            .org-name {{
                font-size: 22px;
                font-weight: bold;
                margin-bottom: 15px;
            }}
            .info-table {{
                width: 100%;
                border-collapse: collapse;
                margin-bottom: 30px;
                border-bottom: 1px solid black;
            }}
            .info-table td {{
                padding: 5px;
                text-align: center;
                font-weight: bold;
                padding-bottom: 10px;
            }}
            .question-list {{
                list-style-type: none;
                padding: 0;
            }}
            .question-item {{
                margin-bottom: 10px;
                font-size: 16px;
                line-height: 1.6;
            }}
        </style>
    </head>
    <body>
        <div class="header">
            <div class="bismillah">বিসমিল্লাহির রহমানির রহিম</div>
            <div class="org-name">কৃষ্ণরামপুর পূর্ব-পাড়া জামে মসজিদ</div>
        </div>

        <table class="info-table">
            <tr>
                <td>তারিখঃ {date}</td>
                <td>বিভাগঃ {dept}</td>
                <td>প্রতি প্রশ্নের পূর্ণমানঃ {marks}</td>
            </tr>
        </table>

        <div class="question-list">
            {''.join(f'<div class="question-item">{q}</div>' for q in questions)}
        </div>
    </body>
    </html>
    """

    # HTML থেকে PDF তৈরি
    # base_url='.' দেওয়ার কারণে সে বর্তমান ফোল্ডার থেকে ফন্ট খুঁজে নিবে
    HTML(string=html_content, base_url='.').write_pdf(filename)

# টেলিগ্রাম কমান্ড
@bot.message_handler(commands=['exam'])
def send_exam_pdf(message):
    chat_id = message.chat.id
    msg = bot.send_message(chat_id, "অপেক্ষা করুন, প্রশ্নপত্র তৈরি হচ্ছে...")
    
    file_name = "Islamic_Exam_Paper.pdf"
    
    try:
        generate_pdf(file_name)
        
        with open(file_name, 'rb') as doc_file:
            bot.send_document(chat_id, doc_file, caption="এই নিন আপনার প্রশ্নপত্র।")
            
        bot.delete_message(chat_id, msg.message_id)
        os.remove(file_name)
        
    except Exception as e:
        bot.edit_message_text(f"সমস্যা হয়েছে: {str(e)}", chat_id, msg.message_id)

print("Bot started...")
bot.infinity_polling()
