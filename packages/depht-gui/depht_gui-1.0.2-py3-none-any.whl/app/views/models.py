"""Models page."""
import shutil
import webbrowser

from flask import (Blueprint, render_template, request, current_app,
                   send_from_directory)
from pathlib import Path

from app.views.depht import no_model_redirect

bp = Blueprint("models", __name__)


@bp.route("/models")
def models():
    """Render Models page."""
    window_size = current_app.config["WINDOW"]
    cpu_cores = current_app.config["CPUS"]
    model_dir = current_app.config["MODEL_DIR"]
    model_url = current_app.config["MODEL_URL"]
    local_models = [model.name for model in model_dir.iterdir()
                    if model.is_dir()]

    if len(local_models) == 0:
        return no_model_redirect(window_size, cpu_cores, model_url)

    return render_template("models/models.html", local_models=local_models)


@bp.route("/models", methods=["POST"])
def models_action():
    """Carry out the models action."""
    action = request.form["model_action"]
    model_dir = current_app.config["MODEL_DIR"]
    window_size = current_app.config["WINDOW"]
    cpu_cores = current_app.config["CPUS"]
    model_url = current_app.config["MODEL_URL"]

    local_models = [model.name for model in model_dir.iterdir()
                    if model.is_dir()]

    if len(local_models) == 0:
        return no_model_redirect(window_size, cpu_cores, model_url)

    model = request.form["model"]

    # selected model
    model_dir = model_dir/model

    msg = None
    pdf_files = []
    if action == "delete":
        shutil.rmtree(model_dir)

        msg = f"{model} deleted."
        # pdf_files = None
        model_dir = current_app.config["MODEL_DIR"]
        local_models = [model.stem for model in model_dir.iterdir()
                        if model.is_dir()]
    else:
        for file in model_dir.iterdir():
            if file.suffix == ".pdf":
                pdf_files.append(file)
        if len(pdf_files) == 0:
            msg = f"No information found on model {model}."

    print(f"msg = {msg}")

    return render_template("models/models.html", local_models=local_models,
                           msg=msg, pdf_files=pdf_files)


@bp.route("/<path:filename>", methods=["GET"])
def pdf_display(filename):
    """Display histograms."""
    filename = Path(filename).name
    dir = request.args.get("dir")

    return send_from_directory(dir, filename, as_attachment=False)
