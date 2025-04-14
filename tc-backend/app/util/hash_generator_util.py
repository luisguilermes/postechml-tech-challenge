import uuid


NAMESPACE = uuid.UUID("6ba7b810-9dad-11d1-80b4-00c04fd430c8")


def generate_hash(strings: list[str]):
    # Ordena as strings para garantir consistência
    data = "".join(sorted(strings))
    return uuid.uuid5(NAMESPACE, data)
