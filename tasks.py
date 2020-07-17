""" Invoke script: developer commands. Run ``invoke -l`` to list available commands.
"""

import os
import sys
import shutil
import importlib
import subprocess

from invoke import task


# ---------- Per project config ----------
NAME = os.path.join("movandi", "mvbrd_utils")
PY_PATHS = [NAME, "tasks.py", "setup.py", "tests"]  # for linting/formatting

# ----------------------------------------
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
assert os.path.isdir(os.path.join(ROOT_DIR, NAME)), "package NAME seems to be incorrect."

yapf_rules = """
    based_on_style: pep8
    column_limit: 100
    split_before_named_assigns: false
    split_before_first_argument: false
    split_arguments_when_comma_terminated: true
    dedent_closing_brackets: false
    coalesce_brackets: false
    split_before_logical_operator: false
""".strip().replace('    ', ' ').replace('\r', '').replace('\n', ',')


@task
def test(ctx, cover=False, junit=True, clean=False):
    """Perform unit tests. Use --cover to open a webbrowser to show coverage.
    """
    param = []
    # if not hardware:
    #     param += ["not hardware"]

    # build the command
    cmd = [sys.executable, "-m", "pytest"]
    if len(param) > 0:
        cmd += ["-m", (" and ").join(param)]
    cmd += ["tests"]
    cmd += ["--cov=movandi.mvbrd_utils", "--cov-report=term", "--cov-report=html"]
    if junit:
        cmd += ["--junitxml=junit.xml"]
    ret_code = subprocess.call(cmd, cwd=ROOT_DIR)
    if ret_code:
        sys.exit(ret_code)
    if cover:
        import webbrowser
        webbrowser.open(os.path.join(ROOT_DIR, "htmlcov", "index.html"))


@task
def lint(ctx):
    """ Validate the code style (e.g. undefined names)
    """
    try:
        importlib.import_module("flake8")
    except ImportError:
        sys.exit("You need to ``pip install flake8`` to lint")

    # We use flake8 with minimal settings
    # http://pep8.readthedocs.io/en/latest/intro.html#error-codes
    cmd = [sys.executable, "-m", "flake8"] + PY_PATHS + ["--select=F,E11"]
    ret_code = subprocess.call(cmd, cwd=ROOT_DIR)
    if ret_code == 0:
        print("No style errors found")
    else:
        sys.exit(ret_code)


@task
def checkformat(ctx):
    """ Check whether the code adheres to the style rules. Use autoformat to fix.
    """
    try:
        import yapf
    except ImportError:
        sys.exit("You need to ``pip install yapf`` to checkformat")

    # YAPF docs: if --diff is supplied, YAPF returns zero when no changes were
    # necessary, non-zero otherwise (including program error).
    cmd = ["yapf", "--recursive", "--diff", "--style", "{" + yapf_rules + "}"]
    cmd += PY_PATHS

    try:
        sys.exit(yapf.main(cmd))
    except yapf.errors.YapfError as e:
        sys.stderr.write('yapf: ' + str(e) + '\n')
        sys.exit(1)


@task
def autoformat(ctx):
    """ Automatically format the code (using yapf).
    """
    try:
        import yapf
    except ImportError:
        sys.exit("You need to ``pip install yapf`` to autoformat")

    cmd = ["yapf", "--recursive", "--in-place", "--style", "{" + yapf_rules + "}"]
    cmd += PY_PATHS

    try:
        sys.exit(yapf.main(cmd))
    except yapf.errors.YapfError as e:
        sys.stderr.write('yapf: ' + str(e) + '\n')
        sys.exit(1)


@task
def clean(ctx):
    """ Clean the repo of temp files etc.
    """
    test(ctx, clean=True)
    for root, dirs, files in os.walk(ROOT_DIR):
        for dname in dirs:
            if dname in (
                    "__pycache__",
                    ".cache",
                    "htmlcov",
                    ".hypothesis",
                    ".pytest_cache",
                    "dist",
                    "build",
                    "sim_build",  # from: cocotb_test
                    ".cocotb-results",
                    NAME + ".serial.egg-info",
            ):
                shutil.rmtree(os.path.join(root, dname))
                print("Removing", dname)
        for fname in files:
            if fname.endswith((".pyc", ".pyo")) or fname in (".coverage", "junit.xml"):
                os.remove(os.path.join(root, fname))
                print("Removing", fname)


@task
def doc(ctx):
    """ Build the documentation
    """
    with ctx.cd("docs"):
        ctx.run("make html")
