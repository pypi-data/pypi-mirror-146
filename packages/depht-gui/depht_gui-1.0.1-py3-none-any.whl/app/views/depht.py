"""DEPhT."""
import shutil
import webbrowser

from datetime import datetime
from pathlib import Path
from flask import (Blueprint, render_template, current_app, request,
                   send_from_directory)
from run_depht.run_depht import run_depht

bp = Blueprint("depht", __name__)


CWD = Path.cwd()


def check_dir(dirpath):
    """Check if directory exists, otherwise make it."""
    if not dirpath.is_dir():
        dirpath.mkdir(parents=True)


def make_output_dir():
    """Create directory structure for DEPhT output.

    Directory structure is as follows:
    home/Downloads/depht/<date>/<time>
    Output stored within this directory
    """
    # timestamp
    timestamp = str(datetime.now())

    # date
    date = timestamp.split(" ")[0]
    date_list = date.split("-")

    time = timestamp.split(" ")[1]
    time_list = time.split(":")
    time_list[2] = str(round(float(time_list[2])))
    time = ":".join(time_list)

    month = date_list[1]
    month_name = datetime.strptime(month, "%m")
    month_name = month_name.strftime("%b")

    date_dir_name = (date_list[0] + "-" + month_name + "-" + date_list[2])

    # outdir = Path.home()/"Downloads"/("depht_" + timestamp)

    depht_outdir = Path.home()/"Downloads"/"depht"

    outdir = depht_outdir/date_dir_name/time

    return outdir


def no_model_redirect(window_size, cpu_cores, model_url):
    """If no local models are saved, redirect.

    Opens a new tab with the models and also redirects to training page.
    """
    webbrowser.open_new_tab(model_url)

    return render_template("train/train.html", no_models=True,
                           window=window_size, cpu_cores=cpu_cores)


@bp.route("/")
def depht():
    """Render depht."""
    length = current_app.config["MIN_LENGTH"]
    cpu_cores = current_app.config["CPUS"]
    window_size = current_app.config["WINDOW"]
    att = current_app.config["ATT_SENSITIVITY"]
    model_dir = current_app.config["MODEL_DIR"]
    model_url = current_app.config["MODEL_URL"]

    # local_models = current_app.config["LOCAL_MODELS"]

    local_models = [model.name for model in model_dir.iterdir()
                    if model.is_dir()]

    # if there are no local models stored
    # open a new tab with the osf path
    # simultaneously open to train models page
    if len(local_models) == 0:
        return no_model_redirect(window_size, cpu_cores, model_url)

    return render_template("depht/depht.html",
                           length=length,
                           cpu_cores=cpu_cores,
                           att=att,
                           local_models=local_models)


@bp.route("/results", methods=["POST"])
def depht_results():
    """Display the results."""
    # infiles = [Path(request.args.get("input_file"))]
    # infile = infiles[0]
    input_dir = CWD.parents[1]

    # make sure there are no already existing tmp_infiles directories
    for dir in input_dir.iterdir():
        if dir.is_dir() and "tmp_infiles" in dir.name:
            shutil.rmtree(dir)

    print(list(request.files.items()))

    infiles = request.files.getlist("input_file")

    input_dir = CWD.parents[1]/"tmp_infiles"
    check_dir(input_dir)

    for file in infiles:
        file.save(Path(input_dir/file.filename))

    infiles = list(input_dir.iterdir())

    # outdir = Path(str(infile.stem) + "_output")
    # outdir = Path(request.args.get("output_folder"))

    # timestamp
    outdir = make_output_dir()

    model = request.form["model"]
    runmode = request.form["mode"]
    att_sens = int(request.form["att"])
    products = int(request.form["products"])
    length = int(request.form["length"])
    cpus = int(request.form["cores"])

    try:
        dump_data = request.form["dump"]
    except Exception:
        dump_data = False

    # always draw the html map
    draw = True

    args = {"Model": model,
            "Runmode": runmode,
            "Att Sensitivity parameter": att_sens,
            "Min. phage homologs": products,
            "Min. length": length,
            "CPU cores": cpus}

    run_depht(infiles, outdir, products, model, cpus=cpus, draw=draw,
              runmode=runmode, dump=dump_data, att_sens=att_sens,
              min_length=length)

    shutil.rmtree(input_dir)

    # filepaths = []

    # output
    # path to the html file if the draw option was selected
    # html file will be embedded in the results page
    # other files will be linked to their filepath in the user's outdir

    # output written to a directory named for the input file in outdir
    # if directory doesn't exist, no prophages were found

    prophage_table = {}

    for infile in infiles:
        # infile = infiles[0]
        results_dir = outdir/infile.stem

        html_file = None
        proph_count = 0
        # no prophage found if the results directory does not exist
        # or if there is no html file in the results directory
        if not results_dir.is_dir():
            prophage_table[infile.stem] = proph_count
            continue
        else:
            suffix_list = [file.suffix for file in results_dir.iterdir()]
            if ".html" not in suffix_list:
                prophage_table[infile.stem] = proph_count
                continue

        proph_count = 0
        # html_files = []

        for item in results_dir.iterdir():
            # found a prophage
            if item.is_dir() and item.name != "tmp_data":
                proph_count += 1

            '''
            # will display the html if there is one input file only
            if len(infiles) == 1:
                if item.suffix == ".html":
                    html_file = str(item)
            '''
            if item.suffix == ".html":
                html_file = str(item)
                # html_files.append(html_file)

        prophage_table[infile.stem] = proph_count

        if len(infiles) != 1:
            html_file = None

        webbrowser.open_new_tab(str(outdir))

        if html_file:
            outdir = str(results_dir)
        else:
            outdir = str(outdir)

    return render_template("depht/results.html", args=args,
                           table=prophage_table, outdir=outdir,
                           html_file=html_file)


@bp.route("/<path:filename>", methods=["GET"])
def html_display(filename):
    """Display prophage map."""
    filename = Path(filename).name
    dir = request.args.get("dir")

    return send_from_directory(dir, filename, as_attachment=False)


@bp.route("/<path:filepath>", methods=["POST"])
def output_link(filepath):
    """Display a link to where the output is stored."""
    dir = filepath.parent
    filename = filepath.stem
    return send_from_directory(dir, filename, as_attachment=True)
