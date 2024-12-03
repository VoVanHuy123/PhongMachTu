from app import create_app,db
import hashlib

app = create_app()

if __name__ == '__main__': 
    db.metadata.clear()
    print(str(hashlib.md5(("1").strip().encode('utf-8')).hexdigest()))
    app.run(debug=True)