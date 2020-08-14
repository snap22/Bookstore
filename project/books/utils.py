from flask import session

def add_book_to_cart(book_id):
    if "cart" in session:
        if not (book_id  in session["cart"]):
            session["cart"].append(book_id)
    else:
        session["cart"] = [book_id]



def remove_book_from_cart(book_id):
    if "cart" in session:
        if book_id  in session["cart"]:
            session["cart"].remove(book_id)



def clear_cart():
    if "cart" in session:
        session.pop("cart", None)
    