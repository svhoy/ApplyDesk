def add_field(schema, field):

    schema = dict(schema)
    schema.setdefault("fields", [])
    schema["fields"].append(field)

    return schema


def remove_field(schema, name):

    schema = dict(schema)
    schema["fields"] = [f for f in schema.get("fields", []) if f["name"] != name]

    return schema


def reorder_fields(schema, order):

    schema = dict(schema)
    fields = {f["name"]: f for f in schema.get("fields", [])}

    schema["fields"] = [fields[name] for name in order if name in fields]

    return schema
