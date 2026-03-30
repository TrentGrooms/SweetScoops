from flask import Flask, render_template, request, redirect, url_for, session
from models import Base, Order, engine, get_session
import uuid



app = Flask(__name__)
app.secret_key = "secret_key"



Base.metadata.create_all(engine)

SIZE_PRICES = {"Small": 3.0, "Medium": 4.5, "Large": 6.0}
TOPPING_PRICES = {
    "Sprinkles": 0.5,
    "Chocolate Syrup": 0.75,
    "Cherries": 0.6,
    "Cookie Crumbles": 0.8,
    "Whipped Cream": 0.7
}
FLAVORS = ["Vanilla", "Chocolate", "Strawberry", "Mint"]




def get_user_id():
    def generate_random_user_id():
        return str(uuid.uuid4())




    if "user_id" not in session:
        session["user_id"] = generate_random_user_id()
        return session["user_id"]

    else:
        return session["user_id"]




@app.route("/", methods=["GET", "POST"])
def order():
    user_id = get_user_id()

    if request.method == "POST":
        db_session = get_session()

        customer_name = request.form["name"]
        flavor = request.form["flavor"]
        size = request.form["size"]
        quantity = request.form["quantity"]

        toppings = request.form.getlist("toppings")
        toppings_str = ",".join(toppings)
        card = request.form["card"]

        if len(card) != 16 or not card.isnumeric():
            return "Invalid card number", 400

        card_last_four = card[-4:]

        if int(quantity) < 1:
            return "Invalid quantity", 400

        total = SIZE_PRICES[size] * int(quantity) + sum(TOPPING_PRICES.get(t, 0) for t in toppings)



        if user_id and customer_name and flavor and size and quantity and toppings and card_last_four:
            new_order = Order(user_id=user_id, customer_name=customer_name, flavor=flavor, size=size, quantity=quantity, toppings=toppings_str, card_last_four=card_last_four, total=total)

            db_session.add(new_order)
            db_session.commit()

            if "order_ids" not in session:
                session["order_ids"] = [new_order.id]
            else:
                session["order_ids"].append(new_order.id)

            db_session.close()
            return redirect(url_for("history"))

        else:
            db_session.close()
            return redirect(url_for("order"))











    return render_template("order.html", flavors=FLAVORS, sizes=SIZE_PRICES, toppings=TOPPING_PRICES)

@app.route("/history")
def history():
    user_id = get_user_id()
    db_session = get_session()

    orders = db_session.query(Order).filter(Order.user_id == user_id).all()

    db_session.close()

    return render_template("history.html", orders=orders)

@app.route("/staff")
def staff():
    db_session = get_session()
    orders = db_session.query(Order).all()
    db_session.close()
    return render_template("staff.html", orders=orders)



@app.route("/reset")
def reset():
    session.clear()
    return redirect(url_for("order"))

if __name__ == "__main__":
    app.run(debug=True)
