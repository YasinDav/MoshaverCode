from django import template

register = template.Library()

@register.simple_tag
def log_metadata(action):
    metadata = {
        0: {
            "bg": "#dcfce7", "icon": "plus-circle", "color": "#16a34a",
            "label": "ایجاد شد", "badge": "bg-success"
        },
        1: {
            "bg": "#fef9c3", "icon": "edit-3", "color": "#ca8a04",
            "label": "ویرایش شد", "badge": "bg-warning"
        },
        2: {
            "bg": "#fee2e2", "icon": "trash-2", "color": "#dc2626",
            "label": "حذف شد", "badge": "bg-danger"
        }
    }
    return metadata.get(action, {
        "bg": "#e5e7eb", "icon": "alert-circle", "color": "#6b7280",
        "label": "نامشخص", "badge": "bg-secondary"
    })