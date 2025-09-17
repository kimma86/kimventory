from flask import Flask, render_template, request, redirect, url_for
from models import db, Item

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///inventory.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

with app.app_context():
    db.create_all()
    #db.drop_all()  # nuke database

@app.route('/')
def index():
    items = Item.query.all()
    return render_template('index.html', items=items)

@app.route('/add', methods=['GET', 'POST'])
def add_item():
    if request.method == 'POST':
        name = request.form['name']
        quantity = int(request.form['quantity'])
        artnr = request.form['artnr']
        price = float(request.form['price'])
        description = request.form['description']

        existing_item = Item.query.filter_by(artnr=artnr).first() # Check for existing item by artnr

        if existing_item:
            existing_item.quantity += quantity
            db.session.commit()
        else:
            new_item = Item(
                name=name,
                quantity=quantity,
                artnr=artnr,
                price=price,
                description=description
            )
            db.session.add(new_item)
            db.session.commit()

        return redirect(url_for('index'))

    return render_template('add_item.html')

@app.route('/scan', methods=['POST'])
def scan_ean():
    ean = request.form['ean']

    item = Item.query.filter_by(artnr=ean).first()

    # TODO: integrate with an api to collect item data based on EAN, we could use ahlsell maybe

    if item:
        item.quantity += 1
        db.session.commit()
    else:
        new_item = Item(
            name=f"Item {ean}",
            quantity=1,
            artnr=ean,
            price=0.0,
            description="Scanned item"
        )
        db.session.add(new_item)
        db.session.commit()

    return redirect(url_for('index'))


@app.route('/edit/<int:item_id>', methods=['GET', 'POST'])
def edit_item(item_id):
    item = Item.query.get_or_404(item_id)
    if request.method == 'POST':
        item.name = request.form['name']
        item.quantity = int(request.form['quantity'])
        item.artnr = request.form['artnr']
        item.price = float(request.form['price'])
        item.description = request.form['description']
        item.ean = request.form['description']

        db.session.commit()
        return redirect(url_for('index'))
    return render_template('edit_item.html', item=item)

@app.route('/delete/<int:item_id>', methods=['POST'])
def delete_item(item_id):
    item = Item.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)#
#     def from_dict(self, data):
#         for field in ['name', 'quantity', 'artnr', 'price', 'description']:
#             if field in data: