from typing import List
from .base import VueRenderer


class VuetifyRenderer(VueRenderer):
    def _write_body(self, context: object, scripts: List[str] = []) -> None:
        """
        Writes the body tag to the html
        """
        root = self.component_list.root.mount(context)

        scripts_html: str = "".join(
            map(lambda s: f'<script src="{s}"></script>', scripts)
        )

        self.html += f"<body><div id='root'><v-app><v-main>{root.template}</v-main></v-app></div>{scripts_html}<script>{self._write_components(context)} new Vue({{el:'#root', vuetify: new Vuetify() {root.script} }})</script></body>"
