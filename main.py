import os
import telebot
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch

# Railway ভেরিয়েবল থেকে টোকেন নিবে
BOT_TOKEN = os.environ.get('BOT_TOKEN') 
bot = telebot.TeleBot(BOT_TOKEN)

# ফন্ট রেজিস্টার ফাংশন
def register_fonts():
    try:
        pdfmetrics.registerFont(TTFont('NotoBengali', 'NotoSerifBengali-Regular.ttf'))
        pdfmetrics.registerFont(TTFont('NotoBengali-Bold', 'NotoSerifBengali-Regular.ttf'))
    except:
        print("Font file not found!")

# PDF জেনারেট ফাংশন
def generate_pdf(filename):
    register_fonts()
    doc = SimpleDocTemplate(filename, pagesize=A4, rightMargin=50, leftMargin=50, topMargin=50, bottomMargin=50)
    
    # স্টাইল তৈরি
    normal_style = ParagraphStyle(name='Normal', fontName='NotoBengali', fontSize=11, leading=16)
    bismillah_style = ParagraphStyle(name='Bismillah', fontName='NotoBengali-Bold', fontSize=14, alignment=1, spaceAfter=6)
    org_name_style = ParagraphStyle(name='OrgName', fontName='NotoBengali-Bold', fontSize=16, alignment=1, spaceAfter=15)
    question_style = ParagraphStyle(name='Question', fontName='NotoBengali', fontSize=12, leading=18, spaceAfter=8)

    story = []

    # হেডার
    story.append(Paragraph("বিসমিল্লাহির রহমানির রহিম", bismillah_style))
    story.append(Paragraph("কৃষ্ণরামপুর পূর্ব-পাড়া জামে মসজিদ", org_name_style))

    # টেবিল
    header_data = [[Paragraph("তারিখঃ ৩০-১২-২০২৫", normal_style), 
                    Paragraph("বিভাগঃ মক্তব", normal_style), 
                    Paragraph("প্রতি প্রশ্নের পূর্ণমানঃ ৫", normal_style)]]
    t = Table(header_data, colWidths=[2*inch, 2*inch, 2.5*inch])
    t.setStyle(TableStyle([('ALIGN', (0,0), (-1,-1), 'CENTER'),
                           ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
                           ('LINEBELOW', (0,0), (-1,-1), 1, colors.black),
                           ('BOTTOMPADDING', (0,0), (-1,-1), 10)]))
    story.append(t)
    story.append(Spacer(1, 20))

    # প্রশ্ন
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

    for q in questions:
        story.append(Paragraph(q, question_style))

    doc.build(story)

# টেলিগ্রাম কমান্ড হ্যান্ডলার
@bot.message_handler(commands=['exam'])
def send_exam_pdf(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "অপেক্ষা করুন, প্রশ্নপত্র তৈরি হচ্ছে...")
    
    file_name = "Islamic_Exam_Paper.pdf"
    
    try:
        # PDF তৈরি করা
        generate_pdf(file_name)
        
        # টেলিগ্রামে পাঠানো
        with open(file_name, 'rb') as doc_file:
            bot.send_document(chat_id, doc_file, caption="এই নিন আপনার প্রশ্নপত্র।")
            
        # পাঠানোর পর সার্ভার থেকে ফাইল ডিলেট করা (অপশনাল)
        os.remove(file_name)
        
    except Exception as e:
        bot.send_message(chat_id, f"সমস্যা হয়েছে: {str(e)}")

print("Bot is running...")
bot.infinity_polling()
