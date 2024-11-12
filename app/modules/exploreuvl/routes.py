import io
from zipfile import ZipFile
from flask import render_template, request, jsonify, send_from_directory
import os


from app.modules.exploreuvl import exploreuvl_bp
from app.modules.exploreuvl.forms import ExploreFormUvl
from app.modules.exploreuvl.services import ExploreServiceUvl


@exploreuvl_bp.route('/exploreuvl', methods=['GET', 'POST'])
def indexUvl():
    if request.method == 'GET':
        query = request.args.get('query', '')
        form = ExploreFormUvl()
        return render_template('exploreuvl/index.html', form=form, query=query)

    if request.method == 'POST':
        criteria = request.get_json()
        uvls = ExploreServiceUvl().filter(**criteria)
        return jsonify([uvl.to_dict() for uvl in uvls])


@exploreuvl_bp.route('/exploreuvl/download_all', methods=['POST'])
def download_uvls():

    criteria = request.get_json()
    uvls = ExploreServiceUvl().filter(**criteria)

    zip_buffer = io.BytesIO()
    with ZipFile(zip_buffer, 'w') as zip_file:
        for file in uvls:
            file_path = '/file/download/'+str(file.id)
            if file_path and os.path.exists(file_path):
                zip_file.write(file_path, os.path.basename(file_path))

    zip_buffer.seek(0)

    return send_from_directory(
            zip_buffer,
            "FeaturedModlesSearch.zip",
            as_attachment=True,
            mimetype="application/zip",
        )

