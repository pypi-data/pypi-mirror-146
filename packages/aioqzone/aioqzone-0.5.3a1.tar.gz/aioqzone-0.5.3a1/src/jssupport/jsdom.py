from pathlib import Path
from shutil import which

from jssupport.execjs import ExecJS


class JSDOM(ExecJS):
    """.. note:: requires :js:mod:`jsdom` installed."""

    def __init__(self, node: str = "node", *, src: str, ua: str, location: str, referrer: str):
        src = src.replace("\n", " ")
        pre_def = f"var src=`{src}`,ua='{ua}',location='{location}',referrer='{referrer}';\n"
        super().__init__(node, js=pre_def + self._windowjs())
        assert self.check_jsdom(), "jsdom should be installed."

    def _windowjs(self):
        """Override this if you have other js files."""
        with open(Path(__file__).parent / "window.js") as f:
            return f.read()

    def eval(self, script: str):
        return self("window.eval", script)

    def add_eval(self, script: str):
        self.addfunc("window.eval", script)

    def check_jsdom(self):
        from subprocess import run

        require = lambda m: run(
            self.node, executable=which(self.node), input=f"require('{m}')", text=True
        )
        return require("jsdom").returncode == 0
