from back.workers import celery
from celery.schedules import crontab
from datetime import datetime
from flask_mail import Message
from back import mail
from back.model import User, Product, Cart
import csv
import io
from flask import send_file


@celery.task()
def daily_mail():
    # Fetch all users from the User table
    users = User.query.filter(User.roles.any(name="user")).all()

    for user in users:
        msg = Message(
            "Daily Message",
            sender="noreply@demo.com",
            recipients=[user.email],  # Send the email to each user
        )
        msg.body = "Visit the app for new exciting deals!"
        mail.send(msg)


@celery.task()
def monthly_report():
    # Fetch all users from the User table
    users = User.query.filter(User.roles.any(name="user")).all()

    for user in users:
        # Calculate the total number of orders for the user from the Cart
        total_orders = Cart.query.filter_by(user_id=user.id, order=True).count()
        cart_items = Cart.query.filter_by(user_id=user.id).all()

        # Extract product IDs from cart items
        product_ids_in_cart = [item.product_id for item in cart_items]

        # Filter products based on the product IDs in the user's cart
        products = Product.query.filter(Product.id.in_(product_ids_in_cart)).all()
        total_price = sum(item.price for item in products)
        # Create an HTML email
        html_content = f"""
        <html>
            <body>
                <h2>Monthly Email</h2>
                <p>Hello {user.username},</p>
                <p>This is your monthly email content. You have {total_orders} orders in your cart.</p>
                <p>TAnd Your total expenditure is {total_price} orders in your cart.</p>
            </body>
        </html>
        """

        # Send the HTML email to the user
        msg = Message(
            "Monthly Email",
            sender="noreply@demo.com",
            recipients=[user.email],
            html=html_content,
        )
        mail.send(msg)


@celery.task
def manager_export(manager_id):
    # Fetch manager from the User table
    manager = User.query.get(manager_id)

    # Prepare CSV file content
    csv_data = [["Username", "Email", "Total Earnings", "Sold Items"]]

    # Fetch products for the manager
    total_earning = 0
    total_sold = 0
    products = Product.query.filter_by(user_id=manager.id).all()
    items = Cart.query.filter_by(order=True).all()
    for item in items:
        for product in products:
            if item.product_id == product.id:
                total_earning = total_earning + product.price
                total_sold = total_sold + 1
    # Calculate total cost and quantity for the manager

    # Append user data to the CSV list
    csv_data.append([manager.username, manager.email, total_earning, total_sold])

    # Create a CSV file in-memory
    csv_memory_file = io.StringIO()
    csv_writer = csv.writer(csv_memory_file)
    csv_writer.writerows(csv_data)

    # Create a Flask response with the CSV file
    attachment_filename = f"product_report_manager_{manager.id}.csv"
    csv_memory_file.seek(0)

    # Send email with attachment
    msg = Message(
        "Product Report",
        recipients=[manager.email],
        body="Attached is the product report CSV file.",
        sender="noreply@demo.com",
    )
    msg.attach(attachment_filename, "text/csv", csv_memory_file.read())
    mail.send(msg)

    return f"Email sent to {manager.email} with product report attached."


@celery.on_after_finalize.connect
def monlthy(sender, **kwargs):
    sender.add_periodic_task(
        crontab(minute=33, hour=10, day_of_month=30),
        monthly_report.s(),
        name="monthly report",
    )


@celery.on_after_finalize.connect
def daily(sender, **kwargs):
    sender.add_periodic_task(
        crontab(minute=32, hour=10),
        daily_mail.s(),
        name="daily report",
    )
