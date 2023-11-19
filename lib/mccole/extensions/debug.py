import ark

import util


@ark.events.register(ark.events.Event.CLI)
def debug_CLI():
    util.debug("EVENT CLI")


@ark.events.register(ark.events.Event.DEPLOY)
def debug_DEPLOY():
    util.debug("EVENT DEPLOY")


@ark.events.register(ark.events.Event.EXIT)
def debug_EXIT():
    util.debug("EVENT EXIT")


@ark.events.register(ark.events.Event.EXIT_BUILD)
def debug_EXIT_BUILD():
    util.debug("EVENT EXIT_BUILD")


@ark.events.register(ark.events.Event.INIT)
def debug_INIT():
    util.debug("EVENT INIT")


@ark.events.register(ark.events.Event.INIT_BUILD)
def debug_INIT_BUILD():
    util.debug("EVENT INIT_BUILD")


@ark.events.register(ark.events.Event.MAIN)
def debug_MAIN():
    util.debug("EVENT MAIN")


@ark.events.register(ark.events.Event.MAIN_BUILD)
def debug_MAIN_BUILD():
    util.debug("EVENT MAIN_BUILD")


@ark.events.register(ark.events.Event.RENDER_PAGE)
def debug_RENDER_PAGE(arg):
    util.debug("EVENT RENDER_PAGE")
