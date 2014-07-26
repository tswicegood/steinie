from .decorators import route
from .routes import get


def application(request):
    # TODO Does it make more sense to do route first?
    # get("/") > request > do_response()

    request > get("/") > do_response()
    request > get("/msg") > say_hello()


@route
def do_response(request):
    return "Hello!\n"


@route
def say_hello(request):
    who = request.args.get('who', 'World')
    return "Hello, %s!\n" % who
