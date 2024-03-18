# import imaplib
# import email
# import re
# from datetime import datetime, timedelta
# from apis.models import Email, MailExpense
# from google.generativeai import generative_model  # Import Gemini here
# import json
# import google.generativeai as genai 
# from celery import shared_task




# genai.configure(api_key="AIzaSyCvKJkmaRe-mSDEiz-biZS-xT2jkjGY9RU")
# model = genai.GenerativeModel('gemini-pro')

# # Function to connect to the IMAP server
# def connect_to_imap(username, password):
#     mail = imaplib.IMAP4_SSL('imap.gmail.com')
#     mail.login(username, password)
#     return mail

# # Function to fetch emails from the inbox within the last 5 minutes
# def fetch_emails_within_last_five_minutes(mail):
#     five_minutes_ago = datetime.now() - timedelta(minutes=5)
#     date_five_minutes_ago = five_minutes_ago.strftime('%d-%b-%Y')
#     mail.select('inbox')
#     _, data = mail.search(None, f'(SINCE "{date_five_minutes_ago}")')
#     email_ids = data[0].split()
#     emails = []
#     for email_id in email_ids:
#         _, data = mail.fetch(email_id, '(RFC822)')
#         emails.append(data[0][1])
#     return emails

# # Function to parse email content and extract relevant information
# def parse_email(email_content):
#     msg = email.message_from_bytes(email_content)
#     sender = msg['From']
#     subject = msg['Subject']
#     body = ""
#     if msg.is_multipart():
#         for part in msg.walk():
#             if part.get_content_type() == "text/plain":
#                 body += part.get_payload(decode=True).decode()
#     else:
#         body = msg.get_payload(decode=True).decode()
#     return {"sender": sender, "subject": subject, "body": body}

# # Function to identify order-related emails using regular expressions
# def identify_order_emails(emails):
#     order_emails = []
#     for email_content in emails:
#         try:
#             email_data = parse_email(email_content)
#             if re.search(r'(order\s+(summary|confirmation)|order\s+placed)', email_data["subject"], re.IGNORECASE) or \
#                     re.search(r'(order\s+(summary|confirmation)|order\s+placed)', email_data["body"], re.IGNORECASE):
#                 order_emails.append(email_data)
#         except Exception as e:
#             print(f"Error processing email: {str(e)}")
#     return order_emails

# # Function to store emails in the database
# def store_emails_in_db(emails):
#     for email_data in emails:
#         Email.objects.create(
#             user_id=email_data["user_id"],
#             sender=email_data["sender"],
#             subject=email_data["subject"],
#             body=email_data["body"],
#             received_at=datetime.now()
#         )

# # Function to process order-related emails and insert into MailExpense model
# def process_order_emails(emails):
#     for email_data in emails:
#            # Process email body with Gemini
#         gemini_prompt = '''the Gemini will give me the user_id (same as given above) , Sender_platform (the ecommerce platform name from where the order has been place: can be decoded by the senders email) ,sender_icon (a code to decode the e-commerce platform from the sender email and then in the table insert their respective icon) , order_id ( any id/number that is given in the email as an order id) , the product name ( identity the name of the product from the mail body if not identified any then save as ITEM) , category ( try to classify the type of product as in a category , like electronics ,clothes ,homeware etc, If the product name is ITEM or not able to classify the product then save as OTHER) , amount ( identify the total amount of the order from the email body, generally the max amount followed by the symbol Rs. ) , date/time ( date/time of the order placed) , status ( whether the order is confirmed, delivered, returned, also if the Gemini finds a email with same email order, then without adding a new row, only update this status )  , feedback ( if there is a link in the body asking the user to give the feedback , then upload that link in this column , if nothing is given then keep it empty )  

# If the email body includes a cart order, then divide that cart into individual product items and then add that data in the new table in the same format as given above. on '''+f"{email_data[0]},{email_data[1]},{email_data[2]},{email_data[3]},{email_data[4]},{email_data[5]}"
#         # model = genai.PredictionServiceClient.from_api_key("AIzaSyCvKJkmaRe-mSDEiz-biZS-xT2jkjGY9RU")
#         response = model.generate_content(gemini_prompt)
#         # print(response)
#         # Extract information from Gemini response (replace with more robust logic based on your actual response format)
#         # Assuming Gemini response provides order information in a structured format (like JSON)
#         order_info = response.text.split("|")
        
        
#         MailExpense.objects.create(
#             amount=float(order_info[7]),  # Example: Extracting amount
#             item=order_info[5],  # Example: Extracting item name
#             category=order_info[6],  # Replace with actual category extracted from email
#             date_of_purchase=datetime.now(),  # Replace with actual date extracted from email
#             platform=email_data[2].split('@','.'),  # Replace with actual platform extracted from email
#             status=order_info[9],  # Replace with actual status extracted from email
#             order_id=order_info[4],  # Example: Extracting order ID
#             feedback= order_info[10],  # Replace with actual feedback extracted from email
#             # user=email_data["user_id"]
#         )

# # Main function to orchestrate the email processing workflow
# def process_emails_workflow(username, password):
#     try:
#         # Connect to IMAP server
#         mail = connect_to_imap(username, password)

#         # Fetch emails within the last 5 minutes
#         emails = fetch_emails_within_last_five_minutes(mail)

#         # Identify order-related emails
#         order_emails = identify_order_emails(emails)

#         # Store emails in the database
#         store_emails_in_db(order_emails)

#         # Process order-related emails and insert into MailExpense model
#         process_order_emails(order_emails)

#         return "Email processing completed successfully"
#     except Exception as e:
#         return f"Error processing emails: {str(e)}"



import imaplib
import email
import re
from datetime import datetime, timedelta
from apis.models import Email, MailExpense

import json
import google.generativeai as genai 
from desis_project import celery
from celery import shared_task

genai.configure(api_key="YOUR_API_KEY")
model = genai.GenerativeModel('gemini-pro')

@shared_task
def process_emails(username, password):
    try:
        mail = imaplib.IMAP4_SSL('imap.gmail.com')
        mail.login(username, password)

        five_minutes_ago = datetime.now() - timedelta(minutes=5)
        date_five_minutes_ago = five_minutes_ago.strftime('%d-%b-%Y')
        mail.select('inbox')
        _, data = mail.search(None, f'(SINCE "{date_five_minutes_ago}")')
        email_ids = data[0].split()
        emails = []
        for email_id in email_ids:
            _, data = mail.fetch(email_id, '(RFC822)')
            emails.append(data[0][1])

        order_emails = []
        for email_content in emails:
            try:
                msg = email.message_from_bytes(email_content)
                sender = msg['From']
                subject = msg['Subject']
                body = ""
                if msg.is_multipart():
                    for part in msg.walk():
                        if part.get_content_type() == "text/plain":
                            body += part.get_payload(decode=True).decode()
                else:
                    body = msg.get_payload(decode=True).decode()
                
                if re.search(r'(order\s+(summary|confirmation)|order\s+placed)', subject, re.IGNORECASE) or \
                    re.search(r'(order\s+(summary|confirmation)|order\s+placed)', body, re.IGNORECASE):
                    order_emails.append({"sender": sender, "subject": subject, "body": body})
            except Exception as e:
                print(f"Error processing email: {str(e)}")

        for email_data in order_emails:
            gemini_prompt = '''the Gemini will give me the user_id (same as given above) , Sender_platform (the ecommerce platform name from where the order has been place: can be decoded by the senders email) ,sender_icon (a code to decode the e-commerce platform from the sender email and then in the table insert their respective icon) , order_id ( any id/number that is given in the email as an order id) , the product name ( identity the name of the product from the mail body if not identified any then save as ITEM) , category ( try to classify the type of product as in a category , like electronics ,clothes ,homeware etc, If the product name is ITEM or not able to classify the product then save as OTHER) , amount ( identify the total amount of the order from the email body, generally the max amount followed by the symbol Rs. ) , date/time ( date/time of the order placed) , status ( whether the order is confirmed, delivered, returned, also if the Gemini finds a email with same email order, then without adding a new row, only update this status )  , feedback ( if there is a link in the body asking the user to give the feedback , then upload that link in this column , if nothing is given then keep it empty )  

If the email body includes a cart order, then divide that cart into individual product items and then add that data in the new table in the same format as given above. on '''+f"{email_data['sender']},{email_data['subject']},{email_data['body']}"
            response = model.generate_content(gemini_prompt)
            order_info = response.text.split("|")
            
            MailExpense.objects.create(
                amount=float(order_info[7]),  
                item=order_info[5],  
                category=order_info[6],  
                date_of_purchase=datetime.now(),  
                platform=email_data['sender'].split('@')[1].split('.')[0],  
                status=order_info[9],  
                order_id=order_info[4],  
                feedback=order_info[10],  
            )

            Email.objects.create(
                sender=email_data['sender'],
                subject=email_data['subject'],
                body=email_data['body'],
                received_at=datetime.now()
            )

        return "Email processing completed successfully"
    except Exception as e:
        return f"Error processing emails: {str(e)}"