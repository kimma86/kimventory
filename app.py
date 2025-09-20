from flask import Flask, render_template, request, redirect, url_for
from models import db, Item
from some_api import SomeAPI, domain

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///inventory.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

with app.app_context():
    db.create_all()
    #db.drop_all()  # nuke database

api = SomeAPI(base_url=f"{domain}/api/search?parameters.SearchPhrase=")

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

        existing_item = Item.query.filter_by(artnr=artnr).first() #  existing item by artnr

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
    checkbox = request.form.get('flexSwitchCheckChecked')
    print(request.form)

    print(checkbox)
    print(f"Checkbox is {'checked' if checkbox else 'not checked'}")
    # something here is messed up
    item = Item.query.filter_by(ean=ean).first() # existing item by ean


    if item:
        item.quantity += 1
        db.session.commit()
    else:

        products = api.get_data(ean)
        if products and len(products) > 0:
            product = products[0]
            artnr = product.get("variantNumber", ean)
            name = product.get("name", f"Item {ean}")
            brand = product.get("brand", "Scanned item")
        else:
            artnr = ean
            name = f"Item {ean}"
            brand = "Scanned item"

        new_item = Item(
            name=name,
            quantity=1,
            artnr=artnr,
            price=0.0,
            description=brand,
            ean=ean
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
    quantity = item.quantity
    if quantity > 1:
        item.quantity -= 1
        db.session.commit()
    else:
        db.session.delete(item)
        db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)