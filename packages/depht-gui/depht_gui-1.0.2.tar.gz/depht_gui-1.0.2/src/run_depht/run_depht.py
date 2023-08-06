"""Function to run depht."""
import pathlib
import shutil

from datetime import datetime
from tempfile import mkdtemp

from Bio import SeqIO

from depht.functions.annotation import (annotate_record,
                                        cleanup_flatfile_records)
from depht.functions.sniff_format import sniff_format
from depht.functions.mmseqs import assemble_bacterial_mask
from depht.functions.multiprocess import CPUS
from depht.functions.find_homologs import find_homologs
from depht.functions.prophage_prediction import predict_prophage_coords
from depht.data import GLOBAL_VARIABLES, PARAMETERS
from depht.__main__ import (load_contigs, load_initial_prophages,
                            detect_att_sites, write_prophage_output)


# ------------ GLOBAL VARIABLES ---------------
DEPHT_DIR = pathlib.Path().home().joinpath(
                                GLOBAL_VARIABLES["model_storage"]["home_dir"])
if not DEPHT_DIR.is_dir():
    DEPHT_DIR.mkdir()

MODEL_DIR = DEPHT_DIR.joinpath(GLOBAL_VARIABLES["model_storage"]["model_dir"])
if not MODEL_DIR.is_dir():
    MODEL_DIR.mkdir()

# Where temporary file I/O should happen
TMP_DIR = DEPHT_DIR.joinpath(GLOBAL_VARIABLES["model_storage"]["tmp_dir"])

# Model can't scan contigs with fewer CDS than window size
MIN_CDS_FEATURES = PARAMETERS["prophage_prediction"]["window"]
# For naming any identified prophages
PROPHAGE_PREFIX = GLOBAL_VARIABLES["phage_sequences"]["prophage_prefix"]
PROPHAGE_DELIMITER = GLOBAL_VARIABLES["phage_sequences"]["prophage_delimiter"]

# For attachment site detection
EXTEND_BY = PARAMETERS["att_detection"]["extention_length"]
ATT_SENSITIVITY = PARAMETERS["att_detection"]["att_sensitivity"]

# For deciding whether to cull predicted "prophages"
MIN_LENGTH = PARAMETERS["annotation"]["min_length"]
MIN_PRODUCTS_NORMAL = PARAMETERS["phage_homology_search"]["min_products"]
MIN_PRODUCTS_STRICT = PARAMETERS["phage_homology_search"][
                                 "min_products_strict"]


def run_depht(infiles, outdir, product_threshold, model,
              cpus=CPUS, draw=True, dump=False, verbose=False,
              runmode="normal", att_sens=ATT_SENSITIVITY, tmpdir=TMP_DIR,
              min_length=MIN_LENGTH):
    """Run DEPhT."""
    # Make sure output dir is a valid path
    if not outdir.is_dir():
        print(f"'{str(outdir)}' does not exist - creating it...")
        outdir.mkdir(parents=True)

    # Get the temporary directory, refresh it if it exists
    if not tmpdir.is_dir():
        tmpdir.mkdir(parents=True)

    # Set up model directories
    model_dir = MODEL_DIR.joinpath(model)

    shell_db_dir = model_dir.joinpath(
                                GLOBAL_VARIABLES["shell_db"]["dir_name"])
    reference_db_dir = model_dir.joinpath(
                                GLOBAL_VARIABLES["reference_db"]["dir_name"])
    phage_homologs_dir = model_dir.joinpath(
                                GLOBAL_VARIABLES["phage_homologs"]["dir_name"])

    bact_ref_fasta = shell_db_dir.joinpath(
                        GLOBAL_VARIABLES["shell_db"]["fasta_name"])
    bact_ref_values = shell_db_dir.joinpath(
                        GLOBAL_VARIABLES["shell_db"]["hex_value_name"])
    essential_db = phage_homologs_dir.joinpath(
                        GLOBAL_VARIABLES["phage_homologs"]["essential_name"])
    extended_db = phage_homologs_dir.joinpath(
                        GLOBAL_VARIABLES["phage_homologs"]["extended_name"])
    blast_db = reference_db_dir.joinpath(
                        GLOBAL_VARIABLES["reference_db"]["name"])
    classifier = model_dir.joinpath(
                        GLOBAL_VARIABLES["classifier"]["name"])

    # Mark program start time
    mark = datetime.now()

    # OK, let's go!
    for infile in infiles:
        # Make sure filepath exists - skip if it doesn't
        if not infile.is_file():
            print(f"'{str(infile)}' does not exist - skipping it...")
            continue

        # Skip .DS_Store files
        if infile.name == ".DS_Store":
            print("skipping .DS_Store file...")
            continue

        # Set up a temporary directory for this genome
        genome_tmp_dir = pathlib.Path(mkdtemp(dir=tmpdir))
        if not genome_tmp_dir.is_dir():
            genome_tmp_dir.mkdir()

        # Automatically check the file format
        fmt = sniff_format(infile)

        # Parse all contigs of annotation-worthy length
        if verbose:
            print(f"\nparsing '{str(infile)}' as {fmt}...")

        # Parse the file and retain contigs above cutoff length
        records = [x for x in SeqIO.parse(infile, fmt) if len(x) >= MIN_LENGTH]

        if not records:
            if verbose:
                print(f"no {fmt}-formatted records of at least {MIN_LENGTH}bp "
                      f"found in '{str(infile)}' - skipping it...")

            shutil.rmtree(genome_tmp_dir)  # clean up after ourselves
            continue

        # Annotate contigs if format is "fasta"
        if fmt == "fasta":
            if verbose:
                print("annotating t(m)RNA and CDS genes de novo...")

            annotate_dir = genome_tmp_dir.joinpath("annotate")
            if not annotate_dir.is_dir():
                annotate_dir.mkdir()

            for record in records:
                annotate_record(record, annotate_dir)

        else:
            if verbose:
                print("using flat file annotation...")

            cleanup_flatfile_records(records)

        # Filter contigs that don't have enough CDS features
        records = [record for record in records if (len(
            [x for x in record.features
                if x.type == "CDS"]) >= MIN_CDS_FEATURES)]

        if not records:
            print(f"no contigs with enough CDS features to analyze in "
                  f"'{str(infile)}' - skipping it...")

            shutil.rmtree(genome_tmp_dir)  # clean up after ourselves
            continue

        contigs = load_contigs(records)

        if verbose:
            print("masking conserved bacterial features...")

        mmseqs_dir = genome_tmp_dir.joinpath("mmseqs")
        if not mmseqs_dir.is_dir():
            mmseqs_dir.mkdir()

        # Detect conserved bacterial genes for each contig
        bacterial_masks = assemble_bacterial_mask(
            contigs, bact_ref_fasta, bact_ref_values, mmseqs_dir)

        if verbose:
            print("looking for high-probability prophage regions...")

        # Predict prophage coordinates for each contig
        prophage_predictions = list()
        for i, contig in enumerate(contigs):
            prediction = predict_prophage_coords(
                contig, classifier, EXTEND_BY, mask=bacterial_masks[i])

            filtered_prediction = []
            for pred in prediction:
                if len(range(*pred)) < min_length:
                    continue

                filtered_prediction.append(pred)

            prophage_predictions.append(filtered_prediction)

        if all([not any(x) for x in prophage_predictions]) and not dump:
            print(f"no complete prophages found in '{str(infile)}'...")

            shutil.rmtree(genome_tmp_dir)  # clean up after ourselves
            continue

        product_threshold = 0
        if runmode in ("normal", "sensitive"):
            hhsearch_dir = genome_tmp_dir.joinpath("hhsearch")
            if not hhsearch_dir.is_dir():
                hhsearch_dir.mkdir()

            # Search for phage gene remote homologs
            if verbose:
                print("searching for phage gene homologs...")

            find_homologs(contigs, prophage_predictions, essential_db,
                          hhsearch_dir, cpus)
            product_threshold = MIN_PRODUCTS_NORMAL

            if runmode == "sensitive":
                if verbose:
                    print("extending search for phage gene homologs...")
                find_homologs(contigs, prophage_predictions, extended_db,
                              hhsearch_dir, cpus, cache_scores=False)
                product_threshold = MIN_PRODUCTS_STRICT
        else:
            for contig in contigs:
                contig.fill_hhsearch_scores()

        prophages = load_initial_prophages(contigs, prophage_predictions,
                                           product_threshold,
                                           prefix=PROPHAGE_PREFIX,
                                           delimiter=PROPHAGE_DELIMITER)

        if verbose and prophages:
            print("searching for attL/R...")

        # Set up directory where we can do attL/R detection
        att_dir = genome_tmp_dir.joinpath("att_core")
        if not att_dir.is_dir():
            att_dir.mkdir()

        # Detect attachment sites, where possible, for the predicted prophage
        search_space = att_sens * EXTEND_BY
        detect_att_sites(prophages, blast_db, search_space, att_dir)

        prophages = [prophage for prophage in prophages
                     if prophage.length >= min_length]

        if not prophages and not dump:
            print(f"no complete prophages found in '{str(infile)}'...")

            shutil.rmtree(genome_tmp_dir)  # clean up after ourselves
            continue

        if verbose:
            print("generating final reports...")

        genome_outdir = outdir.joinpath(f"{infile.stem}")
        if not genome_outdir.is_dir():
            genome_outdir.mkdir()

        draw_dir = genome_tmp_dir.joinpath("draw_diagram")
        if not draw_dir.is_dir():
            draw_dir.mkdir()
        write_prophage_output(genome_outdir, contigs, prophages, draw_dir,
                              draw)

        if dump:
            destination = genome_outdir.joinpath("tmp_data")

            if destination.exists():
                shutil.rmtree(destination)

            shutil.copytree(genome_tmp_dir, destination)
        shutil.rmtree(genome_tmp_dir)  # clean up after ourselves

    print(f"\nTotal runtime: {str(datetime.now() - mark)}")
