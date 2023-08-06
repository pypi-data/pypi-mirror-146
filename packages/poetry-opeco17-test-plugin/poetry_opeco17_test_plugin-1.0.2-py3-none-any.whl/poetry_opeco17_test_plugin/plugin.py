from poetry.console.application import Application
from poetry.plugins.application_plugin import ApplicationPlugin
from poetry.console.commands.command import Command


class TestCommand(Command):
    name = "test"
    description = "Testing"

    def handle(self) -> None:
        self.line("For testing.")


def factory():
    return TestCommand()


class TestApplicationPlugin(ApplicationPlugin):
    def activate(self, application: Application) -> None:
        application.command_loader.register_factory("test", factory)


