from app import Blog

if __name__=='__main__':
    for column in Blog.__table__.columns:
        print(column)
