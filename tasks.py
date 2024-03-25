from invoke import task
import platform

def system():
    if platform.system() == "Windows":
        return False
    else:
        return True


@task
def start(ctx):
    ctx.run("python3 src/index.py", pty=system())

@task
def test(ctx):
    ctx.run("pytest src/tests", pty=system())

@task
def coverage(ctx):
    ctx.run("coverage run --branch -m pytest src", pty=system())


@task(coverage)
def coverage_report(ctx):
    ctx.run("coverage html", pty=system())