from flask import render_template, request, flash, redirect, url_for, abort
from app.modules.api import api_bp
from app import db
from flask_login import login_required, current_user
from app.modules.api.services import APITokenService
from app.modules.api.decorators import token_required
from app.modules.auth.services import AuthenticationService
from app.modules.dataset.models import DataSet
from app.modules.profile.forms import UserProfileForm
from app.modules.dataset.forms import DataSetForm
from app.modules.dataset.services import (
    AuthorService,
    DSMetaDataService,
    DSViewRecordService,
    DataSetService,
    DOIMappingService
)
from app.modules.zenodo.services import ZenodoService

import logging

api_service = APITokenService()
dataset_service = DataSetService()
author_service = AuthorService()
dsmetadata_service = DSMetaDataService()
zenodo_service = ZenodoService()
doi_mapping_service = DOIMappingService()
ds_view_record_service = DSViewRecordService()

logger = logging.getLogger(__name__)


@api_bp.route('/api/configuration', methods=["GET", "POST"])
@login_required
def generate():
    if request.method == "POST":
        expiration_days = request.form.get("expiration", None)

        if not expiration_days:
            flash("Expiration is required.", "error")
            return render_template("api/index.html")

        token, error = api_service.generate_token(
            user_id=current_user.id,
            user_email=current_user.email,
            expiration_days=expiration_days
        )

        if token:
            flash("API token generated successfully", "success")
            return render_template("api/index.html", generated_token=token)
        else:
            flash(error or "An error occurred while generating the token", "error")

    return render_template("api/index.html")

# token_required endpoints:
# /dataset -----------------------------------------------------------------------


@api_bp.route("/api/dataset/list", methods=["GET"])
@token_required
def list_dataset_token():
    return render_template(
        "dataset/list_datasets.html",
        datasets=dataset_service.get_synchronized(current_user.id),
        local_datasets=dataset_service.get_unsynchronized(current_user.id),
    )


@api_bp.route("/api/dataset/upload", methods=["GET"])
@token_required
def see_dataset_create_page():
    form = DataSetForm()
    return render_template("dataset/upload_dataset.html", form=form)


@api_bp.route("/api/dataset/unsynchronized/<int:dataset_id>/")
@token_required
def list_unsynchronized_dataset(dataset_id):

    # Get dataset
    dataset = dataset_service.get_unsynchronized_dataset(current_user.id, dataset_id)

    if not dataset:
        abort(404)

    return render_template("dataset/view_dataset.html", dataset=dataset)

# /profile -----------------------------------------------------------------------


@api_bp.route("/api/profile/edit", methods=["GET"])
@token_required
def see_profile_edit_page():
    auth_service = AuthenticationService()
    profile = auth_service.get_authenticated_user_profile
    if not profile:
        return redirect(url_for("public.index"))

    form = UserProfileForm()

    return render_template("profile/edit.html", form=form)


@api_bp.route('/api/profile/summary')
@token_required
def see_profile_summary():
    page = request.args.get('page', 1, type=int)
    per_page = 5

    user_datasets_pagination = db.session.query(DataSet) \
        .filter(DataSet.user_id == current_user.id) \
        .order_by(DataSet.created_at.desc()) \
        .paginate(page=page, per_page=per_page, error_out=False)

    total_datasets_count = db.session.query(DataSet) \
        .filter(DataSet.user_id == current_user.id) \
        .count()

    return render_template(
        'profile/summary.html',
        user_profile=current_user.profile,
        user=current_user,
        datasets=user_datasets_pagination.items,
        pagination=user_datasets_pagination,
        total_datasets=total_datasets_count
    )
