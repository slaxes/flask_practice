from app import app
import app.txt2html as t2h
if __name__ == '__main__':
    t2h.load_html()
    app.run()