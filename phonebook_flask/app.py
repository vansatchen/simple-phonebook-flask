from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://user:userpass@localhost/asteriskdb'
app.config['SQLALCHEMY_BINDS'] = {
    'example1db': 'mysql://user:userpass@localhost/example1db',
    'example2db': 'mysql://user:userpass@localhost/example2db',
    'example3db': 'mysql://user:userpass@localhost/example3db',
}
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class example1(db.Model):
    __bind_key__ = 'example1db'
    __tablename__ = 'ps_endpoints'
    id = db.Column(db.Integer, primary_key=True)
    callerid = db.Column(db.String(100))

    def __repr__(self):
        return '<ps_endpoints %r>' % self.id


db.metadata.clear()


class example2(db.Model):
    __bind_key__ = 'example2db'
    __tablename__ = 'ps_endpoints'
    id = db.Column(db.Integer, primary_key=True)
    callerid = db.Column(db.String(100))

    def __repr__(self):
        return '<ps_endpoints %r>' % self.id


db.metadata.clear()


class example3(db.Model):
    __bind_key__ = 'example3db'
    __tablename__ = 'sipusers'
    name = db.Column(db.Integer, primary_key=True)
    callerid = db.Column(db.String(100))

    def __repr__(self):
        return '<ps_endpoints %r>' % self.name


@app.route('/')
def index():
    net = request.remote_addr.split('.')[1]
    defaultPage = '/example1'
    if net == '11': defaultPage = '/example2'
    if net == '14': defaultPage = '/example3'
    return redirect(defaultPage)

@app.route('/example1')
def example1():
    q = request.args.get('q')
    if q:
        persons = example1.query.filter(example1.callerid.contains(q)).all()
    else:
        persons = example1.query.filter(example1.id.notin_(['1112', '1116'])).order_by(example1.id).all()
    return render_template("example1.html", persons=persons)


@app.route('/example2')
def example2():
    q = request.args.get('q')
    if q:
        persons = example2.query.filter(example2.callerid.contains(q)).all()
    else:
        persons = example2.query.filter(example2.id.notin_(['2999',])).order_by(example2.id).all()
    return render_template("example2.html", persons=persons)


@app.route('/example3')
def example3():
    q = request.args.get('q')
    if q:
        persons = example3.query.filter(example3.callerid.contains(q)).all()
    else:
        persons = example3.query.filter(example3.name.notin_(['4444', '4445'])).order_by(example3.name).all()
    return render_template("example3.html", persons=persons)


@app.route('/useful')
def useful():
    return render_template("useful.html")


@app.route('/<string:url>')
def unusableUrl(url):
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=False)
