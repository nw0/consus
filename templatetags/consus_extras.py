# -*- coding: latin-1 -*-
from django import template
from django.core.urlresolvers import reverse
from django.utils.html import format_html, mark_safe

from consus.models import Location

register = template.Library()

@register.simple_tag
def nav_active(request, urls):
    if request.path in (reverse(url) for url in urls.split()):
        return "active"
    return ""

@register.filter
def item_table(item_list):
    output = [ format_html('''<div class="table-responsive">
    <table class="table table-striped">
        <thead>
            <th>ID</th>
            <th>Name</th>
            <th>Type</th>
            <th>Location</th>
            <th>Comment</th>
        </thead>
        <tbody>''') ]

    for item in item_list:
        output.append(format_html('''
            <tr>
                <td>#{}</td>
                <td>{}</td>
                <td>{}</td>
                <td><a href="{}">{}</a></td>
                <td>{}</td>
            </tr>''',
            item.id, item.name, item.item_type,
            reverse("consus:location_detail", args=[item.location.id]),
            item.location, item.comment))
    output.append(format_html('''</tbody></table></div>'''))
    return mark_safe('\n'.join(output))

@register.filter
def subloc_print(subloc_list):
    output = []
    for subloc in subloc_list:
        if not isinstance(subloc, Location):
            return subloc_list

        output.append(format_html('''
            <div class="panel panel-default">
                <div class="panel-heading">
                    <p class="panel-title"><a href="{}">{}{}</a></p>
                </div>
                <div class="panel-body">''',
            reverse("consus:location_detail", args=[subloc.id]), subloc,
            format_html(": <em>{}</em>", subloc.comment)
                if subloc.comment else ""))

        if subloc.item_list():
            output.append(format_html("<p>Items</p>"))
            output.append(item_table(subloc.item_list()))

        if subloc.sublocations():
            output.append(format_html("<p>Sublocations</p>"))
            output.append(subloc_print(subloc.sublocations()))

        output.append('</div></div>')
    return mark_safe('\n'.join(output))
