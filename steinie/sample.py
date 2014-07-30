from .decorators import get, post, route
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


class Router(object):
    pass


router = Router()


@router.get("/")
def index(request, response):
    return "Index\n"


@router.use
def middleware(request, response, _next):
    request.msg = "Hello, %s!"
    _next()


msg = router.route("/msg")


@msg.get
def get_msg(request, response):
    return request.msg % request.args.get("who", "World")


@msg.post
def post_msg(request, response):
    response.location = "/msg?who=%s" % request.args.get("who", "Poster")


@router.param("user")
def add_user(self, request):
    mapped_names = {
        't': 'Travis',
        'p': 'Peter',
    }
    request.user = mapped_names.get(request.params['user'], 'Whoever You Are')


@router.get("/msg/<user>")
def handle(request):
    return request.msg % request.user
