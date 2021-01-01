import smtplib
from tkinter import *
import requests
from bs4 import BeautifulSoup

root = Tk()
root.geometry('640x640')

def button_command():
    check_price()
    root.destroy()


# URL = 'https://www.amazon.de/-/en/gp/product/B01MD1GDWK?pf_rd_r=QNX61J4FVV3293CTQYHV&pf_rd_p=f6634045-2cd8-4654-8338-b9246a89c6f1&pd_rd_r=024867d3-a104-4a49-85ff-a72c8cb52de2&pd_rd_w=63p5K&pd_rd_wg=y8FPU&ref_=pd_gw_unk'
label_URL = Label(root, text="Link to the product").pack()
URL = Entry(root, width = 20)
URL.pack()

headers = {
    "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'}

# expected_price = 100
label_expected_price = Label(root, text="Expected Price").pack()
expected_price = Entry(root, width = 20)
expected_price.pack()

# login_mail = 'ishraq.h.c2@gmail.com'
# login_password = "*********"
label_login_mail = Label(root, text="Login Email").pack()
login_mail = Entry(root)
login_mail.pack()
label_login_password = Label(root, text="Login Password").pack()
login_password = Entry(root, show="*")
login_password.pack()
mail_from = login_mail.get()
# mail_to = 'entrep.haider@gmail.com'
label_mail_to = Label(root, text="Mail To").pack()
mail_to = Entry(root)
mail_to.pack()


Button(root, text="Input", command=button_command).pack()

def check_price():
    page = requests.get(URL.get(), headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')
    title = soup.find(id="productTitle").get_text()
    price = float(soup.find(id="priceblock_ourprice").get_text().replace('€', ''))

    if (price < float(expected_price.get())):
        send_positive_mail()
        print("Price is reasonable")
    else:
        send_negative_mail()
        print("Price is expensive")

    # print(title.strip())
    # print(price)


def send_positive_mail():
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()

    server.login(login_mail.get(), login_password.get())

    subject = "Price Down in Amazon"
    body = 'Check the link ' + URL.get()

    msg = f"Subject: {subject}\n\n{body}"
    server.sendmail(mail_from, mail_to.get(), msg)

    print("Email has been sent")

    server.quit()

def send_negative_mail():
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()

    server.login(login_mail.get(), login_password.get())

    subject = "Price is still up"
    body = 'Sorry the price is still up. Please check again a few days later'

    msg = f"Subject: {subject}\n\n{body}"
    server.sendmail(mail_from, mail_to.get(), msg)

    print("Email has been sent")

    server.quit()


root.mainloop()
