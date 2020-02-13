from LPapp import app
import os


port=os.environ.get("PORT")

if port is None or port == "":
    port = 3000

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port)
