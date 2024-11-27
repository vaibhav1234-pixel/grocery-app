from io import BytesIO

from sqlalchemy import func
from datetime import datetime
from flask_cors import cross_origin
from flask import request, jsonify, send_file
from sqlalchemy import not_, and_
from back.model import User, Product, Category, Subcategory, Upload, Cart
from back import db, app, bcrypt
from back import tasks
from flask_caching import Cache

cache = Cache(
    config={
        "CACHE_TYPE": "RedisCache",
        "CACHE_REDIS_HOST": "localhost",
        "CACHE_REDIS_PORT": 6380,
    }
)
cache.init_app(app)


# from run import user_datastore


from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    jwt_required,
    get_jwt_identity,
)


jwt = JWTManager(app)


@app.route("/manager_export/<manager_id>", methods=["POST"])
@jwt_required()
def call_method(manager_id):
    job = tasks.manager_export.delay(manager_id)
    return str(job), 200


@app.route("/userlogin", methods=["POST", "GET"])
@cross_origin()
def user_login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = User.query.filter(
            func.lower(User.username) == func.lower(username)
        ).first()

        if user and bcrypt.check_password_hash(user.password, password):
            user_id = user.id
            # Get user roles
            roles = [role.name for role in user.roles]

            # Include roles in the JWT token
            access_token = create_access_token(
                identity=username, additional_claims={"roles": roles}
            )

            return (
                jsonify(
                    {"access_token": access_token, "user_id": user_id, "roles": roles}
                ),
                200,
            )
        else:
            return jsonify({"error": "Invalid username or password"}), 401

    return jsonify({"message": "You reached the login endpoint"}), 405


@app.route("/userlogout", methods=["POST"])
@jwt_required()
def logout():
    current_user = get_jwt_identity()
    print(f"Logout request for user: {current_user}")
    # No explicit action needed for logout since JWTs are stateless
    return jsonify({"message": "Logout successful"})


@app.route("/categories", methods=["GET"])
@cross_origin()
@cache.cached(timeout=5)
def get_categories():
    categories = Category.query.filter_by(approval="approved")
    category_list = [
        {"id": category.id, "name": category.name, "upload_id": category.upload_id}
        for category in categories
    ]
    return jsonify({"categories": category_list})


@app.route("/subcategories/<int:cat_id>", methods=["GET"])
@cross_origin()
@cache.cached(timeout=5)
def get_subcategories(cat_id):
    subcategories = Subcategory.query.filter_by(cat_id=cat_id, approval="approved")
    subcategory_list = [
        {
            "id": subcategory.id,
            "name": subcategory.name,
            "upload_id": subcategory.upload_id,
        }
        for subcategory in subcategories
    ]
    return jsonify({"subcategories": subcategory_list})


@app.route("/products/<int:subcat_id>", methods=["GET"])
@cross_origin()
@cache.cached(timeout=5)
def get_products(subcat_id):
    if subcat_id == 0:
        products = Product.query.all()
    else:
        products = Product.query.filter_by(subcat_id=subcat_id)
    product_list = [
        {
            "id": product.id,
            "name": product.name,
            "price": product.price,
            "expiry": product.expiry,
            "description": product.description,
            "status": product.status,
            "upload_id": product.upload_id,
        }
        for product in products
    ]
    return jsonify({"products": product_list})


@app.route("/product/<int:id>", methods=["GET"])
@cross_origin()
@cache.cached(timeout=5)
def get_product(id):
    products = Product.query.filter_by(id=id)
    product_list = [
        {
            "id": product.id,
            "name": product.name,
            "price": product.price,
            "expiry": product.expiry,
            "description": product.description,
            "status": product.status,
            "upload_id": product.upload_id,
        }
        for product in products
    ]
    return jsonify({"products": product_list})


@app.route("/req_categories/<role>", methods=["GET"])
@cross_origin()
@cache.cached(timeout=5)
def req_categories(role):
    if role == "manager":
        categories = Category.query.all()
    else:
        categories = Category.query.filter(
            and_(
                not_(Category.approval == "approved"),
                not_(Category.approval == "rejected"),
            )
        )
    category_list = [
        {"id": category.id, "name": category.name, "approval": category.approval}
        for category in categories
    ]
    return jsonify({"categories": category_list})


@app.route("/req_subcategories/<role>", methods=["GET"])
@cross_origin()
@cache.cached(timeout=5)
def req_subcategories(role):
    if role == "manager":
        subcategories = Category.query.all()
    else:
        subcategories = Subcategory.query.filter(
            and_(
                not_(Subcategory.approval == "approved"),
                not_(Subcategory.approval == "rejected"),
            )
        )
    subcategory_list = [
        {
            "id": subcategory.id,
            "name": subcategory.name,
            "approval": subcategory.approval,
        }
        for subcategory in subcategories
    ]
    return jsonify({"subcategories": subcategory_list})


@app.route("/download/<int:upload_id>")
def download(upload_id):
    upload = Upload.query.filter_by(id=upload_id).first()
    if upload is None:
        return "File not found", 404

    return send_file(
        BytesIO(upload.data), download_name=upload.filename, as_attachment=False
    )


@app.route("/catcreate/<role>", methods=["POST"])
@cross_origin()
@jwt_required()
def creat_cat(role):
    if request.method == "POST":
        # Check if the POST request has the file part
        if "image_file" not in request.files:
            return jsonify({"flash": "No file part"})

        image_file = request.files["image_file"]

        # Check if the file is empty
        if image_file.filename == "":
            return jsonify({"flash": "No selected file"})

        # Extract other data from the request
        name = request.form.get("name")

        # Now you can process the file as needed and save it to your database
        # For example, save the file to a folder on your server
        # image_file.save("path/to/your/folder/" + secure_filename(image_file.filename))

        # Create a new Category with the data
        existing_cat = Category.query.filter(
            func.lower(Category.name) == func.lower(name)
        ).first()

        if existing_cat:
            return jsonify({"flash": "Category already exists"})
        else:
            cat = Category(name=name)
            image = Upload(filename=image_file.filename, data=image_file.read())

            db.session.add(image)
            db.session.commit()
            cat.upload_id = image.id
            if role == "manager":
                cat.approval = "add_request"
                db.session.add(cat)

                db.session.commit()

                return (
                    jsonify(
                        {"success": "Category will be created after admin approval"}
                    ),
                    201,
                )

            db.session.add(cat)

            db.session.commit()

            return jsonify({"success": "Category created successfully"}), 201

    return jsonify({"message": "Welcome to the category creation endpoint"})


@app.route("/subcatcreate/<role>", methods=["POST"])
@cross_origin()
@jwt_required()
def create_subcat(role):
    if request.method == "POST":
        # Check if the POST request has the file part
        if "image_file" not in request.files:
            return jsonify({"flash": "No file part"})

        image_file = request.files["image_file"]

        # Check if the file is empty
        if image_file.filename == "":
            return jsonify({"flash": "No selected file"})

        # Extract other data from the request
        name = request.form.get("name")
        cat_id = request.form.get("cat_id")

        # Now you can process the file as needed and save it to your database
        # For example, save the file to a folder on your server
        # image_file.save("path/to/your/folder/" + secure_filename(image_file.filename))

        # Create a new Category with the data
        existing_subcat = Subcategory.query.filter(
            func.lower(Subcategory.name) == func.lower(name)
        ).first()

        if existing_subcat:
            return jsonify(
                {"flash": "Subcategory already exists for the selected category"}
            )
        else:
            subcat = Subcategory(name=name, cat_id=cat_id)

            image = Upload(filename=image_file.filename, data=image_file.read())

            db.session.add(image)
            db.session.commit()
            subcat.upload_id = image.id
            if role == "manager":
                subcat.approval = "add_request"
                db.session.add(subcat)
                db.session.commit()

                return (
                    jsonify(
                        {"success": "Subcategory will be created after admin approval"}
                    ),
                    201,
                )

            db.session.add(subcat)
            db.session.commit()

            return jsonify({"success": "Subcategory created successfully"}), 201

    return jsonify({"message": "Welcome to the subcategory creation endpoint"})


@app.route("/catedit/<role>/<int:cat_id>", methods=["POST", "PUT"])
@cross_origin()
@jwt_required()
def edit_cat(role, cat_id):
    if request.method == "POST":
        cat = db.session.get(Category, cat_id)

        if not cat:
            return jsonify({"flash": "Category not found"}), 404

        # Check if the POST request has the file part
        if "image_file" in request.files:
            image_file = request.files["image_file"]

            # Check if the file is empty
            if image_file.filename != "":
                # Process and save the new file
                # image_file.save("path/to/your/folder/" + secure_filename(image_file.filename))
                image = Upload(filename=image_file.filename, data=image_file.read())

                db.session.add(image)
                db.session.commit()
                cat.upload_id = image.id
        if role == "approval":
            approval = request.form.get("approval")
            cat.approval = approval
            db.session.commit()

            return (
                jsonify({"success": approval}),
                200,
            )

        if role == "manager":
            cat.approval = "edit_request"
            db.session.commit
            return (
                jsonify({"success": "Category edit will be done after admin approval"}),
                200,
            )

        # Extract other data from the request
        name = request.form.get("name")

        # Update the subcategory data
        cat.name = name

        db.session.commit()
        return (
            jsonify({"success": "Category updated Succefully!"}),
            200,
        )

    return jsonify({"message": "Welcome to the subcategory edit endpoint"})


@app.route("/subcatedit/<role>/<int:subcat_id>", methods=["POST", "PUT"])
@cross_origin()
@jwt_required()
def edit_subcat(role, subcat_id):
    if request.method == "POST":
        subcat = db.session.get(Subcategory, subcat_id)

        if not subcat:
            return jsonify({"flash": "Subcategory not found"}), 404

        # Check if the POST request has the file part
        if "image_file" in request.files:
            image_file = request.files["image_file"]

            # Check if the file is empty
            if image_file.filename != "":
                # Process and save the new file
                # image_file.save("path/to/your/folder/" + secure_filename(image_file.filename))
                image = Upload(filename=image_file.filename, data=image_file.read())

                db.session.add(image)
                db.session.commit()
                subcat.upload_id = image.id

        # Extract other data from the request

        if role == "approval":
            approval = request.form.get("approval")
            subcat.approval = approval
            db.session.commit()

            return (
                jsonify({"success": approval}),
                200,
            )
        # Update the subcategory data

        if role == "manager":
            subcat.approval = "edit_request"
            db.session.commit()

            return (
                jsonify(
                    {"success": "Subcategory edit will be done after admin approval"}
                ),
                200,
            )
        name = request.form.get("name")
        cat_id = request.form.get("cat_id")
        subcat.name = name
        subcat.cat_id = cat_id
        db.session.commit()

        return jsonify({"success": "Subcategory updated successfully"}), 200

    return jsonify({"message": "Welcome to the subcategory edit endpoint"})


@app.route("/subcatremove/<role>/<int:subcat_id>", methods=["DELETE"])
@cross_origin()
@jwt_required()
def remove_subcat(role, subcat_id):
    if request.method == "DELETE":
        subcat = Subcategory.query.get(subcat_id)

        if not subcat:
            return jsonify({"flash": "Subcategory not found"}), 404
        if role == "admin":
            db.session.delete(subcat)
            db.session.commit()
            return jsonify({"success": "Subcategory removed successfully"}), 200
        if role == "manager":
            subcat.approval = "delete_request"
            db.session.commit()
            return (
                jsonify(
                    {"success": "Subcategory will be removed after admin approval"}
                ),
                200,
            )

    return jsonify({"message": "Welcome to the subcategory removal endpoint"})


@app.route("/catremove/<role>/<int:cat_id>", methods=["DELETE"])
@cross_origin()
@jwt_required()
def remove_cat(role, cat_id):
    if request.method == "DELETE":
        cat = Category.query.get(cat_id)

        if not cat:
            return jsonify({"flash": "Category not found"}), 404

        if role == "admin":
            db.session.delete(cat)
            db.session.commit()
            return jsonify({"success": "Subcategory removed successfully"}), 200
        if role == "manager":
            cat.approval = "delete_request"
            db.session.commit()
            return (
                jsonify(
                    {"success": "Subcategory will be removed after admin approval"}
                ),
                200,
            )

        return jsonify({"success": "Category removed successfully"}), 200

    return jsonify({"message": "Welcome to the category removal endpoint"})


@app.route("/product_create", methods=["POST"])
@cross_origin()
@jwt_required()
def creat_product():
    if request.method == "POST":
        # Check if the POST request has the file part
        if "image_file" not in request.files:
            return jsonify({"flash": "No file part"})

        image_file = request.files["image_file"]

        # Check if the file is empty
        if image_file.filename == "":
            return jsonify({"flash": "No selected file"})

        # Extract other data from the request
        name = request.form.get("name")
        subcat_id = request.form.get("subcat_id")
        expiry = request.form.get("expiry")
        description = request.form.get("description")
        price = request.form.get("price")
        status = request.form.get("status")
        user_id = request.form.get("user_id")

        expiry_date = datetime.strptime(expiry, "%Y-%m-%d")

        # Now you can process the file as needed and save it to your database
        # For example, save the file to a folder on your server
        # image_file.save("path/to/your/folder/" + secure_filename(image_file.filename))

        # Create a new Category with the data
        existing_product = Product.query.filter(
            func.lower(Product.name) == func.lower(name)
        ).first()

        if existing_product:
            return jsonify({"flash": "Product already exists"})
        elif expiry_date < datetime.now():
            return jsonify({"flash": "Expiry date must be in the future"})
        else:
            product = Product(
                name=name,
                expiry=expiry_date,
                subcat_id=subcat_id,
                description=description,
                status=status,
                price=price,
                user_id=user_id,
            )
            image = Upload(filename=image_file.filename, data=image_file.read())

            db.session.add(image)
            db.session.commit()
            product.upload_id = image.id

            db.session.add(product)
            db.session.commit()

            return jsonify({"success": "Product added successfully"}), 201

    return jsonify({"message": "Welcome to the category creation endpoint"})


@app.route("/product_edit/<int:pro_id>", methods=["POST", "PUT"])
@cross_origin()
@jwt_required()
def edit_product(pro_id):
    if request.method == "PUT":
        product = Product.query.get(pro_id)

        if not product:
            return jsonify({"flash": "Product not found"}), 404

        # Check if the POST request has the file part
        if "image_file" in request.files:
            image_file = request.files["image_file"]

            # Check if the file is empty
            if image_file.filename != "":
                # Process and save the new file
                # image_file.save("path/to/your/folder/" + secure_filename(image_file.filename))
                image = Upload(filename=image_file.filename, data=image_file.read())

                db.session.add(image)
                db.session.commit()
                product.upload_id = image.id

        # Extract other data from the request
        name = request.form.get("name")
        expiry = request.form.get("expiry")
        description = request.form.get("description")
        price = request.form.get("price")
        subcat_id = request.form.get("subcat_id")

        # Update the subcategory data
        if name != "":
            product.name = name
        if subcat_id != "":
            product.subcat_id = subcat_id
        if expiry != "":
            expiry_date = datetime.strptime(expiry, "%Y-%m-%d")
            product.expiry = expiry_date
        if description != "":
            product.description = description
        if price != "":
            product.price = price

        db.session.commit()

        return jsonify({"success": "Product updated successfully"}), 200

    return jsonify({"message": "Welcome to the product edit endpoint"})


@app.route("/productremove/<int:pro_id>", methods=["DELETE"])
@cross_origin()
@jwt_required()
def remove_product(pro_id):
    if request.method == "DELETE":
        product = Product.query.get(pro_id)

        if not product:
            return jsonify({"flash": "Product not found"}), 404

        db.session.delete(product)
        db.session.commit()

        return jsonify({"success": "Product removed successfully"}), 200

    return jsonify({"message": "Welcome to the product removal endpoint"})


@app.route("/addtocart/<int:pro_id>/<user_id>", methods=["POST"])
@cross_origin()
@jwt_required()
def add_to_cart(pro_id, user_id):
    if request.method == "POST":
        item = Cart(product_id=pro_id, user_id=user_id)
        db.session.add(item)
        db.session.commit()
    return jsonify({"message": "Item Added"})


@app.route("/removefromcart/<user_id>", methods=["POST"])
@cross_origin()
@jwt_required()
def removefromcart(user_id):
    if request.method == "POST":
        items = Cart.query.filter(Cart.user_id == user_id).all()

        # Delete all items associated with the user_id
        for item in items:
            item.order = True

        db.session.commit()

    return jsonify({"message": "Items Deleted"})


@app.route("/getitems/<user_id>", methods=["GET"])
@cross_origin()
@jwt_required()
@cache.cached(timeout=5)
def get_items(user_id):
    if request.method == "GET":
        # Get items in the user's cart
        items = Cart.query.filter_by(user_id=user_id, order=False).all()
        products = Product.query.filter_by().all()
        total_price = 0
        product_list = []
        # Extract product IDs from cart items
        for item in items:
            for product in products:
                if item.product_id == product.id:
                    total_price = total_price + product.price

                    product_list.append(
                        {
                            "id": product.id,
                            "name": product.name,
                            "price": product.price,
                            "expiry": product.expiry,
                            "description": product.description,
                            "status": product.status,
                            "upload_id": product.upload_id,
                        }
                    )

        return jsonify({"products": product_list, "total_price": total_price})


@app.route("/totalitems/<product_id>", methods=["GET"])
@cross_origin()
@jwt_required()
@cache.cached(timeout=5)
def total_items(product_id):
    if request.method == "GET":
        # Get items in the user's cart
        products = Product.query.filter_by(product_id=id).all()
        items = Cart.query.filter_by(product_id=product_id, order=False).all()
        for item in items:
            for product in products:
                if item.product_id == product.id:
                    total_sold = total_sold + 1

        return jsonify({"total_orders": total_sold})


@app.route("/getmanitems/<user_id>", methods=["GET"])
@cross_origin()
@jwt_required()
@cache.cached(timeout=5)
def get_manager_items(user_id):
    if request.method == "GET":
        # Extract product IDs from cart items

        # Filter products based on the product IDs in the user's cart
        products = Product.query.filter_by(user_id=user_id).all()

        product_list = [
            {
                "id": product.id,
                "name": product.name,
                "price": product.price,
                "expiry": product.expiry,
                "description": product.description,
                "status": product.status,
                "upload_id": product.upload_id,
            }
            for product in products
        ]

        return jsonify({"products": product_list})
