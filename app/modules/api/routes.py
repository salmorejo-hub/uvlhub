from flask import render_template, request, flash
from app.modules.api import api_bp
from flask_login import login_required, current_user
from app.modules.api.services import APITokenService

api_service = APITokenService()


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
