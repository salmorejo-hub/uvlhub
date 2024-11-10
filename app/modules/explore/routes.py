from flask import render_template, request, jsonify

from app.modules.explore import explore_bp
from app.modules.explore.forms import ExploreForm, ExploreUvl
from app.modules.explore.services import ExploreService, ExploreServiceUvl


@explore_bp.route('/explore', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        query = request.args.get('query', '')
        form = ExploreForm()
        return render_template('explore/index.html', form=form, query=query)

    if request.method == 'POST':
        criteria = request.get_json()
        datasets = ExploreService().filter(**criteria)
        return jsonify([dataset.to_dict() for dataset in datasets])


@explore_bp.route('/exploreuvl', methods=['GET', 'POST'])
def indexUvl():
    if request.method == 'GET':
        query = request.args.get('query', '')
        form = ExploreUvl()
        return render_template('explore/indexSearch.html', form=form, query=query)

    if request.method == 'POST':
        criteria = request.get_json()
        uvls = ExploreServiceUvl().filter(**criteria)
        return jsonify([uvl.to_dict() for uvl in uvls])
