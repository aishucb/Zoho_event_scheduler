from flask import Flask, render_template, request
import os
from PIL import Image, ImageDraw, ImageFont
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process_form', methods=['POST'])
def process_form():
    try:
        name = request.form['name']
        email = request.form['email']

    # Load the image

        image = Image.open('backdrop.jpg')

    # Set font color and size
        text_color = (255, 255, 255)


    # Define text to be added
        text = f"{name.upper()}"

    # Calculate text position
        if len(name)<=6:
            font_size = 120
            x = 1100
            y = 350
        elif len(name)>6 and len(name)<9:
            font_size = 110
            x = 1000
            y = 370
        else:
            font_size = 95
            x = 990
            y = 370
      # Y-coordinate

    # Add text to image
        draw = ImageDraw.Draw(image)
        font_path = 'poppins.ttf'
        font = ImageFont.truetype(font_path, font_size)
        draw.text((x, y), text, fill=text_color, font=font)

    # Save modified image
        image.save('modified_image.jpg')

    # Send email with the modified image attached
        subject = "Modified Image"
        message = f"Hello {name},\n\nPlease find the modified image attached."
        sender_email = "ash@vong.in"
        recipient_email = email

        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = subject

        msg.attach(MIMEText(message, 'plain'))

        with open('modified_image.jpg', 'rb') as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())

        encoders.encode_base64(part)

        part.add_header(
            "Content-Disposition",
            f"attachment; filename= {os.path.basename('modified_image.jpg')}",
        )

        msg.attach(part)
        smtp_server = 'email-smtp.us-east-2.amazonaws.com'
        smtp_port = 587  # Use 465 for SSL
        smtp_username = 'AKIA5KRQ5RSOP5KD5SNQ'  # Your Gmail email address
        smtp_password = 'BLKo9ZQKH070VNQZyKfXoCQ5ODw6B1/7+V9Cw5Q+xeqL'
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.sendmail(sender_email, recipient_email, msg.as_string())
        server.quit()
        return "Email sent successfully."
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == '__main__':
    app.run(debug=True)