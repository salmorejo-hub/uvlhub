from flask import render_template, request, jsonify

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
