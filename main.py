import os
from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Настройка базы данных SQLite
DB_FILE = "messages.db"
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_FILE}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# Модель сообщения
class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    date = db.Column(db.String(50), nullable=False)
    content = db.Column(db.Text, nullable=False)

# Конфигурация постраничного просмотра
PAGE_SIZE = 70

@app.route("/")
def index():
    """
    Главная страница с постраничным отображением сообщений.
    """
    page = int(request.args.get("page", 1))  # Номер текущей страницы (по умолчанию 1)
    messages = Message.query.paginate(page=page, per_page=PAGE_SIZE, error_out=False)
    
    return render_template(
        "index.html",
        messages=messages.items,
        page=page,
        total_pages=messages.pages
    )

@app.route("/receive", methods=["POST"])
def receive_message():
    """
    Эндпоинт для приема сообщений в формате JSON.
    """
    data = request.json
    if not data:
        return jsonify({"error": "Invalid JSON"}), 400
    
    username = data.get("Username", "Anonymous")
    date = data.get("date", "Unknown date")
    content = data.get("Message", "")

    # Сохраняем сообщение в базу данных
    message = Message(username=username, date=date, content=content)
    db.session.add(message)
    db.session.commit()
    
    return jsonify({"status": "Message received"}), 200

@app.route("/messages", methods=["GET"])
def get_all_messages():
    """
    Эндпоинт для получения всех сообщений в формате JSON.
    """
    all_messages = Message.query.all()
    return jsonify([{"username": m.username, "date": m.date, "content": m.content} for m in all_messages])

if __name__ == "__main__":
    # Проверка существования базы данных перед созданием
    if not os.path.exists(DB_FILE):
        with app.app_context():
            db.create_all()

    app.run(host="0.0.0.0", port=5000)
