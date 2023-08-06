import os
from typing import List

from django.template.backends.django import DjangoTemplates

from djavue.component_list import VueComponentList


class VueRenderer:
    """
    Gets template info and returns the appropriate html
    """

    def __init__(
        self,
        title: str,
        template_name: str,
        version: str = "development",
        engine: DjangoTemplates = None,
    ) -> "VueRenderer":
        self.title = title
        self.html = ""
        self.version = version

        if not engine:
            self._load_engine()
        else:
            self.engine = engine

        self.path, self.template_name = os.path.split(
            str(self.engine.get_template(template_name).origin)
        )

        self.component_list = VueComponentList.from_file(
            self.path, self.template_name, engine=self.engine
        )

    # UTILS
    def _load_engine(self) -> None:
        """
        Creates the Django Engine instance that we use to get path from file name
        """
        try:
            from django.conf import settings

            obj = settings.TEMPLATES[0].copy()
            obj["NAME"] = "a"
            obj.pop("BACKEND")
            self.engine = DjangoTemplates(params=obj).engine
        except:
            print("Error loading engine. Probably will break.")
            pass

    def _get_cdn(self) -> str:
        """
        Chooses which Vue CDN to get based on version
        """

        if self.version == "production":
            return '<script src="https://cdn.jsdelivr.net/npm/vue@2"></script>'
        else:
            return (
                '<script src="https://cdn.jsdelivr.net/npm/vue@2/dist/vue.js"></script>'
            )

    def _get_styles(self, context: object) -> str:
        root_css = self.component_list.root.mount(context).style
        components_css = [c.mount().style for c in self.component_list.components]

        return "".join([root_css] + components_css)

    # BUILDER FUNCTIONS
    def _write_header(self, context: object, style_sheets: List[str] = []) -> None:
        """
        Writes the head tag to the html
        """

        style_sheets_html: str = "".join(
            map(lambda s: f'<link href="{s}" rel="stylesheet">', style_sheets)
        )

        self.html += f"<html><head><title>{self.title}</title>{self._get_cdn()}{style_sheets_html}<style>{self._get_styles(context)}</style></head>"

    def _write_components(self, context: object) -> str:
        """
        Returns all Vue Components in component form, ready for html
        """

        return ";".join(
            map(lambda c: c.to_component(context), self.component_list.components)
        )

    def _write_body(self, context: object, scripts: List[str] = []) -> None:
        """
        Writes the body tag to the html
        """
        root = self.component_list.root.mount(context)

        scripts_html: str = "".join(
            map(lambda s: f'<script src="{s}"></script>', scripts)
        )

        self.html += f"<body><div id='root'>{root.template}</div><script>{self._write_components(context)}; new Vue({{el:'#root', {root.script} }})</script>{scripts_html}</body>"

    # RENDERINGS
    def render(
        self,
        context: object = {},
        style_sheets: List[str] = [],
        scripts: List[str] = [],
    ) -> str:
        """
        Creates the html based on the root Vue Component passed
        """

        self._write_header(context, style_sheets)
        self._write_body(context, scripts)

        return self.html


def get_vue_template(
    template_name, title="Dejavue Page", renderer=VueRenderer
) -> VueRenderer:
    """
    Loads a Vue file by it's file name and returns a VueRenderer instance ready for being rendered
    """

    return renderer(title, template_name)
