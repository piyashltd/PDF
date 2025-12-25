import os
import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import BufferedInputFile
from weasyprint import HTML, CSS
from weasyprint.text.fonts import FontConfiguration

# --- কনফিগারেশন ---
API_TOKEN = os.getenv("BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")

# ফন্ট কনফিগারেশন (ফন্ট ফাইলটি fonts ফোল্ডারে থাকতে হবে)
FONT_PATH = os.path.join(os.path.dirname(__file__), 'fonts', 'SolaimanLipi.ttf')

# লগিং চালু করা
logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

def generate_html_content():
    # প্রশ্নের তালিকা
    questions = [
        "১। কালিমা তাইয়্যিবাহ অর্থসহ বল।",
        "২। কালিমা শাহাদাত বল।",
        "৩। কালিমা তাওহীদ বল।",
        "৪। কালিমা তামজীদ বল।",
        "৫। আরবী হরফ কয়টি ও কী কী?",
        "৬। মাখরাজ কয়টি? প্রথম তিনটি মাখরাজ বল।",
        "৭। আরবী হরফে নোকতা কয়টি ও কী কী? (এক নোকতা, দুই নোকতা ও তিন নোকতা বিশিষ্ট হরফ)।",
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

    questions_html = "".join([f"<div class='question-item'>{q}</div>" for q in questions])

    # HTML টেমপ্লেট
    html_template = f"""
    <!DOCTYPE html>
    <html lang="bn">
    <head>
        <meta charset="UTF-8">
        <style>
            @font-face {{
                font-family: 'BanglaFont';
                src: url('file://{FONT_PATH}');
            }}
            @page {{
                size: A4;
                margin: 0.5in; /* মার্জিন কমিয়ে দেওয়া হয়েছে */
            }}
            body {{
                font-family: 'BanglaFont', sans-serif;
                font-size: 13px; /* ফন্ট সামান্য ছোট করা হয়েছে */
                line-height: 1.4;
            }}
            .header {{
                text-align: center;
                margin-bottom: 15px;
            }}
            .bismillah {{
                font-size: 16px;
                font-weight: bold;
                margin-bottom: 5px;
            }}
            .org-name {{
                font-size: 20px;
                font-weight: bold;
                margin-bottom: 10px;
            }}
            .info-table {{
                width: 100%;
                border-collapse: collapse;
                margin-bottom: 5px;
                font-size: 13px;
            }}
            .info-table td {{
                padding: 2px;
                vertical-align: top;
            }}
            .border-line {{
                border-bottom: 1px solid #000;
                margin-bottom: 15px;
            }}
            
            /* দুই কলামের লেআউট */
            .questions-container {{
                column-count: 2;
                column-gap: 40px;
            }}
            .question-item {{
                margin-bottom: 8px; /* প্রশ্নের মাঝখানের ফাঁকা কমানো হয়েছে */
                font-size: 14px;
                break-inside: avoid; /* যাতে প্রশ্ন ভেঙে দুই কলামে না যায় */
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
                <td style="text-align: left; width: 33%;">তারিখঃ ৩০-১২-২০২৫</td>
                <td style="text-align: center; width: 33%;">বিভাগঃ মক্তব</td>
                <td style="text-align: right; width: 33%;">পূর্ণমানঃ ১০০</td>
            </tr>
        </table>
        
        <div class="border-line"></div>

        <div class="questions-container">
            {questions_html}
        </div>
    </body>
    </html>
    """
    return html_template

@dp.message(Command("start"))
async def send_welcome(message: types.Message):
    await message.reply("আসসালামু আলাইকুম। প্রশ্নপত্র পেতে /getpdf কমান্ডটি দিন।")

@dp.message(Command("getpdf"))
async def create_and_send_pdf(message: types.Message):
    status_msg = await message.reply("⏳ প্রশ্নপত্র তৈরি হচ্ছে...")
    
    try:
        html_content = generate_html_content()
        font_config = FontConfiguration()
        pdf_bytes = HTML(string=html_content).write_pdf(font_config=font_config)
        
        input_file = BufferedInputFile(pdf_bytes, filename="Islamic_Exam_Paper.pdf")
        
        await message.reply_document(
            document=input_file,
            caption="✅ আপনার প্রশ্নপত্র তৈরি হয়েছে। এটি এক পৃষ্ঠায় প্রিন্ট হবে।"
        )
        await status_msg.delete()
        
    except Exception as e:
        logging.error(f"Error: {e}")
        await message.reply(f"সমস্যা হয়েছে: {str(e)}")

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
