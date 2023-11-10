from app import create_app

import os 

app = create_app('default') #os.environ.get('FLASK_CONFIG')

if __name__ == '__main__':
    app.run(debug=True, port=4000)