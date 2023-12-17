from app import create_app
from dotenv import load_dotenv

import os 

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')

if os.path.exists(dotenv_path):
    load_dotenv()

app = create_app(os.environ.get('FLASK_CONFIG', 'default'))

if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')
