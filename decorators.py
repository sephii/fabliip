from functools import wraps

from fabric.api import env


def multisite(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if args:
            site = args[0]
        elif func.__defaults__:
            site = func.__defaults__[0]
        else:
            site = None

        selected_environment = func.__name__

        if site is not None:
            if site not in env.sites:
                raise Exception("Site {site} is not part of the possible sites"
                                " ({sites})".format(site=site,
                                                    sites=env.sites.keys()))

            if selected_environment not in env.sites[site]:
                raise Exception("Site {site} has no {env}"
                                " environment".format(site=site,
                                                      env=selected_environment))

            for setting, value in env.sites[site][selected_environment].iteritems():
                env[setting] = value

            env.site = site

        return func(*args, **kwargs)
    return wrapper