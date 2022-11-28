from flask import Flask, render_template, request
import requests
import smtplib
import os

MY_EMAIL = os.getenv("MY_EMAIL")
MY_PASSWORD = os.getenv("MY_PASSWORD")

response = requests.get("https://api.npoint.io/c790b4d5cab58020d391")
all_posts = response.json()

app = Flask(__name__)


@app.route('/')
def get_all_posts():
    return render_template("index.html", posts=all_posts)


@app.route('/contact', methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        data = request.form
        send_email(data["name"], data["email"], data["phone"], data["message"])
        return render_template("contact.html", message_sent=True)
    else:
        return render_template("contact.html", message_sent=False)


def send_email(name, email, phone, message):
    with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
        connection.starttls()
        connection.login(user=MY_EMAIL, password=MY_PASSWORD)
        connection.sendmail(
            from_addr=MY_EMAIL,
            to_addrs="alexispaluch@gmail.com",
            msg=f"Subject: Message from Blog\n\n"
                f"Name: {name}\n"
                f"Email: {email}\n"
                f"Phone: {phone}\n"
                f"Message:{message}")


@app.route('/about')
def get_about_page():
    return render_template("about.html")


@app.route('/post/<int:index>')
def show_post(index):
    requested_post = None
    for post in all_posts:
        if post["id"] == index:
            requested_post = post
    return render_template("post.html", post=requested_post)


if __name__ == "__main__":
    app.run(debug=True)
