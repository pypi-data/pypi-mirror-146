import os
from typing import Callable, List

from django.http import HttpResponse

from djavue.renderers import VueRenderer, get_vue_template
from djavue.renderers.vuetify import VuetifyRenderer


class VueTemplate:
    """
    Shortcut for creating a view that returns a Vue file
    """

    renderer_class: VueRenderer = VueRenderer

    def _validate(self, request) -> None:
        """
        Checks if template_name and context exists
        """

        if self.context is None:
            raise Exception(f"{self.get_template_name(request)} context is null.")

    def get_context(self, request) -> object:
        """
        Function for defining context that must be overriden by the user
        """

        return None

    def get_extra_style_sheets(self, request) -> List[str]:
        """
        Function for defining aditional style_sheets to be loaded that can be overriden by the user
        """

        return []

    def get_extra_scripts(self, request) -> List[str]:
        """
        Function for defining aditional style_sheets to be loaded that can be overriden by the user
        """

        return []

    def get_template_name(self, request) -> str:
        """
        Function for programatically defining the template that can be overriden by the user
        """

        return self.Meta.template_name

    def _mount(self, request) -> HttpResponse:
        """
        Validates, loads the template and returns the content in Http
        """

        self.context: object = self.get_context(request)
        self._validate(request)

        style_sheets: List[str] = self.get_extra_style_sheets(request)
        scripts: List[str] = self.get_extra_scripts(request)

        instance: VueRenderer = get_vue_template(
            os.path.split(self.get_template_name(request))[1],
            title=self.Meta.page_title,
            renderer=self.renderer_class,
        )

        self.content: str = instance.render(self.context, style_sheets, scripts)

        return HttpResponse(self.content)

    @classmethod
    def as_view(cls) -> Callable:
        """
        Returns a function to be used in Django's path() or url()
        """

        instance = cls()
        return lambda request: instance._mount(request)

    class Meta:
        """
        Class that must be overriden by the user with the view's details
        """

        page_title = "Djavue Page"
        root_path = ""
        template_name = None
        context = None


class VuetifyTemplate(VueTemplate):
    renderer_class: VueRenderer = VuetifyRenderer

    def get_extra_style_sheets(self, request) -> List[str]:
        return [
            "https://fonts.googleapis.com/css?family=Roboto:100,300,400,500,700,900",
            "https://cdn.jsdelivr.net/npm/@mdi/font@6.x/css/materialdesignicons.min.css",
            "https://cdn.jsdelivr.net/npm/vuetify@2.x/dist/vuetify.min.css",
        ]

    def get_extra_scripts(self, request) -> List[str]:
        return ["https://cdn.jsdelivr.net/npm/vuetify@2.x/dist/vuetify.js"]
