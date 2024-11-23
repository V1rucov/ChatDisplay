from flask import Flask, request, jsonify, render_template
import math

app = Flask(__name__)
messages = []
PAGE_SIZE = 70

@app.route("/")
def index():
    """
    Главная страница с постраничным отображением сообщений.
    """
    page = int(request.args.get("page", 1))  # Номер текущей страницы (по умолчанию 1)
    start = (page - 1) * PAGE_SIZE
    end = start + PAGE_SIZE
    paginated_messages = messages[start:end]
    
    total_pages = math.ceil(len(messages) / PAGE_SIZE)
    return render_template(
        "index.html",
        messages=paginated_messages,
        page=page,
        total_pages=total_pages
    )

@app.route("/receive", methods=["POST"])
def receive_message():
    """
    Эндпоинт для приема сообщений в формате JSON.
    """
    data = request.json
    if not data:
        return jsonify({"error": "Invalid JSON"}), 400
    messages.append(data)
    print(request.json["Message"].encode('latin-1').decode('utf-8'))
    return jsonify({"status": "Message received"}), 200

@app.route("/messages", methods=["GET"])
def get_all_messages():
    """
    Эндпоинт для получения всех сообщений в формате JSON.
    """
    return jsonify(messages, ensure_ascii=False)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
