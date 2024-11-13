from flask import Flask, request, jsonify
from flask_cors import CORS

from agent import create_agent
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
CORS(app)
# Initialize Swagger for API documentation
agent = create_agent()

@app.route('/api/ask', methods=['POST'])
def ask():
    data = request.get_json()
    query = data.get('query')
    if not query:
        return jsonify({'error': 'No query provided.'}), 400
    try:
        # Invoke the agent with the query as input
        response = agent.invoke({"input": query})
        return jsonify({'response': response})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, port=port)
