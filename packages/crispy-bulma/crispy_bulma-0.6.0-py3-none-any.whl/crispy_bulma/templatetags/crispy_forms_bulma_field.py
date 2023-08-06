# This file is currently copied directly from django-crispy-forms==0.12.0
# There are only a few small changes specific to bulma.
# https://github.com/django-crispy-forms/django-crispy-forms/blob/1.12.0/crispy_forms/templatetags/crispy_forms_field.py

from django import forms, template
from django.conf import settings

from crispy_forms.utils import TEMPLATE_PACK

register = template.Library()


@register.filter
def is_checkbox(field):
    return isinstance(field.field.widget, forms.CheckboxInput)


@register.filter
def is_password(field):
    return isinstance(field.field.widget, forms.PasswordInput)


@register.filter
def is_radioselect(field):
    # the extra CheckboxSelectMultiple check is needed for django 4.0
    return isinstance(field.field.widget, forms.RadioSelect) and not isinstance(
        field.field.widget, forms.CheckboxSelectMultiple
    )


@register.filter
def is_select(field):
    # warning: this function is True for forms.SelectMultiple too
    return isinstance(field.field.widget, forms.Select)


@register.filter
def is_selectmultiple(field):
    return isinstance(field.field.widget, forms.SelectMultiple)


@register.filter
def is_checkboxselectmultiple(field):
    return isinstance(field.field.widget, forms.CheckboxSelectMultiple)


@register.filter
def is_file(field):
    return isinstance(field.field.widget, forms.FileInput)


@register.filter
def is_clearable_file(field):
    return isinstance(field.field.widget, forms.ClearableFileInput)


@register.filter
def is_multivalue(field):
    return isinstance(field.field.widget, forms.MultiWidget)


@register.filter
def classes(field):
    """
    Returns CSS classes of a field
    """
    return field.widget.attrs.get("class", None)


@register.filter
def css_class(field):
    """
    Returns widgets class name in lowercase
    """
    return field.field.widget.__class__.__name__.lower()


def pairwise(iterable):
    """s -> (s0,s1), (s2,s3), (s4, s5), ..."""
    a = iter(iterable)
    return zip(a, a)


class CrispyBulmaFieldNode(template.Node):
    def __init__(self, field, attrs):
        self.field = field
        self.attrs = attrs
        self.html5_required = "html5_required"

    def render(self, context):
        # Nodes are not threadsafe so we must store and look up our instance
        # variables in the current rendering context first
        if self not in context.render_context:
            context.render_context[self] = (
                template.Variable(self.field),
                self.attrs,
                template.Variable(self.html5_required),
            )

        field, attrs, html5_required = context.render_context[self]
        field = field.resolve(context)
        try:
            html5_required = html5_required.resolve(context)
        except template.VariableDoesNotExist:
            html5_required = False

        # If template pack has been overridden in FormHelper we can pick it from context
        template_pack = context.get("template_pack", TEMPLATE_PACK)

        # There are special django widgets that wrap actual widgets,
        # such as forms.widgets.MultiWidget, admin.widgets.RelatedFieldWidgetWrapper
        widgets = getattr(
            field.field.widget,
            "widgets",
            [getattr(field.field.widget, "widget", field.field.widget)],
        )

        if isinstance(attrs, dict):
            attrs = [attrs] * len(widgets)

        converters = {
            "textinput": "input",
            "fileinput": "fileinput fileUpload",
            "passwordinput": "input",
            "emailinput": "input",
            "checkboxinput": "",
            "select": "",
            "selectmultiple": "",
        }
        converters.update(getattr(settings, "CRISPY_CLASS_CONVERTERS", {}))

        for widget, attr in zip(widgets, attrs):
            class_name = widget.__class__.__name__.lower()
            class_name = converters.get(class_name, class_name)
            css_class = widget.attrs.get("class", "")
            if css_class:
                if css_class.find(class_name) == -1:
                    css_class += " %s" % class_name
            else:
                css_class = class_name

            if template_pack == "bulma":
                if field.errors:
                    css_class += " is-danger"

            widget.attrs["class"] = css_class

            if "class" in widget.attrs and not widget.attrs["class"]:
                # remove the class="" attribute completely if empty
                del widget.attrs["class"]

            # HTML5 required attribute
            if (
                html5_required
                and field.field.required
                and "required" not in widget.attrs
            ):
                if field.field.widget.__class__.__name__ != "RadioSelect":
                    widget.attrs["required"] = "required"

            for attribute_name, attribute in attr.items():
                attribute_name = template.Variable(attribute_name).resolve(context)

                if attribute_name in widget.attrs:
                    widget.attrs[attribute_name] += " " + template.Variable(
                        attribute
                    ).resolve(context)
                else:
                    widget.attrs[attribute_name] = template.Variable(attribute).resolve(
                        context
                    )

        return str(field)


@register.tag(name="crispy_field")
def crispy_field(parser, token):
    """
    {% crispy_field field attrs %}
    """
    token = token.split_contents()
    field = token.pop(1)
    attrs = {}

    # We need to pop tag name, or pairwise would fail
    token.pop(0)
    for attribute_name, value in pairwise(token):
        attrs[attribute_name] = value

    return CrispyBulmaFieldNode(field, attrs)
