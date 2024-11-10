from flask import render_template, request, flash
from app.modules.api import api_bp
from flask_login import login_required, current_user
from app.modules.api.services import APITokenService
from app.modules.api.decorators import token_required
from app.modules.dataset.services import DataSetService

api_service = APITokenService()
dataset_service = DataSetService()


@api_bp.route('/api/configuration', methods=["GET", "POST"])
@login_required
def generate():
    if request.method == "POST":
        expiration_days = request.form.get("expiration", None)

        if not expiration_days:
            flash("Expiration is required.", "error")
            return render_template("api/index.html")

        token, error = api_service.generate_token_with_validation(
            user_id=current_user.id,
            expiration_days=expiration_days
        )

        if token:
            flash("API token generated successfully", "success")
            return render_template("api/index.html", generated_token=token)
        else:
            flash(error or "An error occurred while generating the token", "error")

    return render_template("api/index.html")


@api_bp.route("/api/dataset/list", methods=["GET"])  # Falta añadir POST
@token_required
def list_dataset_token():
    return render_template(
        "dataset/list_datasets.html",
        datasets=dataset_service.get_synchronized(current_user.id),
        local_datasets=dataset_service.get_unsynchronized(current_user.id),
    )
