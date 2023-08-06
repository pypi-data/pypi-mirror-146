"""DEPhT Train."""
import shutil
import webbrowser

from pathlib import Path
from flask import (Blueprint, render_template, current_app, request,
                   send_from_directory)

from depht_train.pipelines.train_model import train_model
from app.views.depht import check_dir

bp = Blueprint("train", __name__)

CWD = Path.cwd()


@bp.route("/depht-train", methods=["GET"])
def depht_train():
    """Render depht_train page."""
    window_size = current_app.config["WINDOW"]
    cpu_cores = current_app.config["CPUS"]

    return render_template("train/train.html",
                           window=window_size,
                           cpu_cores=cpu_cores)


@bp.route("/model", methods=["POST"])
def training_results():
    """Run depht_train."""
    # get arguments to train a new model
    model_dir = current_app.config["MODEL_DIR"]

    model_name = request.form["name"]
    window = int(request.form["window"])
    cores = int(request.form["cpu"])

    # get the files from the upload, put into temporary directories for input
    # temporary directory is created outside src

    phages = request.files.getlist("phage")
    bacteria = request.files.getlist("bact")
    prophage_csv = request.files["csv"]

    input_dir = CWD.parents[1]/"tmp_infiles"
    phage_dir = input_dir/"phage_dir"
    bact_dir = input_dir/"bact_dir"

    check_dir(phage_dir)
    check_dir(bact_dir)

    for phage_file in phages:
        phage_file.save(Path(phage_dir/phage_file.filename))

    for bact_file in bacteria:
        bact_file.save(Path(bact_dir/bact_file.filename))

    try:
        prophage_csv.save(Path(input_dir/prophage_csv.filename))
        prophage_csv = Path(input_dir/prophage_csv.filename)
        csv_name = prophage_csv.name
    except IsADirectoryError:
        # if the user does not specify a csv file
        prophage_csv = None
        csv_name = None

    # train_model

    args = {"Model name": model_name,
            "Prophage CSV": csv_name,
            "Window Size": window,
            "CPU cores": cores}

    # train the model!
    train_model(model_name, phage_dir, bact_dir, window=window,
                prophages=prophage_csv, cpus=cores)

    # clean up
    shutil.rmtree(input_dir)

    model_dir = model_dir/model_name

    pdf_files = []

    for file in model_dir.iterdir():
        if file.suffix == ".pdf":
            pdf_files.append(file)

    webbrowser.open_new(model_dir)

    return render_template("train/results.html", args=args,
                           model_dir=model_dir,
                           display_files=pdf_files)


@bp.route("/<path:filename>", methods=["GET"])
def pdf_display(filename):
    """Display histograms."""
    filename = Path(filename).name
    dir = request.args.get("dir")

    return send_from_directory(dir, filename, as_attachment=False)
