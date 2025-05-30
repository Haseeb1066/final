from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
import os
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
CORS(app)

api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

stored_data = None

# A global dictionary to hold data by dashboard
dashboard_data_store = {}

@app.route("/api/store_data", methods=["POST"])
def store_data():
    content = request.get_json()
    dashboard = content.get("dashboard")
    data = content.get("data")
    dashboard_data_store[dashboard] = data
    return jsonify({"status": "success"})

# @app.route('/api/ask', methods=['POST'])
# def ask():
#     global dashboard_data_store
#     try:
#         question = request.json.get('question', '')
#         if not dashboard_data_store:
#             return jsonify({"error": "No data stored yet"}), 400

#         prompt = f"The user has asked a question based on this data:\n{dashboard_data_store}\n\nQuestion: {question}"

#         response = client.chat.completions.create(
#             model="gpt-3.5-turbo",
#             messages=[
#                 {"role": "system", "content": "You are a Tableau dashboard analyst."},
#                 {"role": "user", "content": prompt}
#             ]
#         )

#         answer = response.choices[0].message.content
#         return jsonify({"answer": answer})

#     except Exception as e:
#         return jsonify({"error": str(e)}), 500



@app.route('/api/ask', methods=['POST'])
def ask():
    try:
        content = request.json
        question = content.get('question', '')
        dashboard = content.get('dashboard', None)

        if not dashboard or dashboard not in dashboard_data_store:
            return jsonify({"error": "Dashboard data not found"}), 400

        data = dashboard_data_store[dashboard]

        max_length = 2000
        if len(data) > max_length:
            data = data[:max_length] + "\n\n...(truncated)"

        prompt = f"The user has asked a question based on this data:\n{data}\n\nQuestion: {question}"

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a Tableau dashboard analyst."},
                {"role": "user", "content": prompt}
            ]
        )

        answer = response.choices[0].message.content
        return jsonify({"answer": answer})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
