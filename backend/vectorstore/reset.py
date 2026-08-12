"""Separate destructive reset command with exact-target guards."""
import argparse

from core.settings_loader import load_settings
from vectorstore.qdrant import client_from_settings, validate_collection_info

SCROLL_LIMIT = 1000


def reset_collection(client, settings, *, expected_count, confirmation):
    """Delete the exact configured collection after all guards pass.

    Never recreates the collection; the next ingestion run owns creation.
    """
    db = settings["vector_database"]
    name = db["collection_name"]
    model_id = settings["embedding"]["model"]
    dimension = db["vector_size"]
    if confirmation != f"DELETE {name}":
        raise ValueError(f"confirmation mismatch; expected 'DELETE {name}'")
    if not client.collection_exists(name):
        raise ValueError(f"collection {name} does not exist; nothing to reset")
    validate_collection_info(client.get_collection(name), settings)
    records, _ = client.scroll(
        name,
        limit=SCROLL_LIMIT,
        with_payload=True,
        with_vectors=False,
        timeout=db["timeout"],
    )
    for record in records:
        payload = record.payload or {}
        if payload.get("embedding_model") != model_id:
            raise ValueError(f"payload embedding_model mismatch for point {record.id}")
        if payload.get("embedding_dimension") != dimension:
            raise ValueError(f"payload embedding_dimension mismatch for point {record.id}")
    actual = client.count(name, exact=True).count
    if actual != expected_count:
        raise ValueError(f"collection {name} count {actual} != expected {expected_count}")
    client.delete_collection(name, timeout=db["timeout"])
    if client.collection_exists(name):
        raise RuntimeError(f"collection {name} still exists after delete")
    return name


def main(argv=None):
    """CLI entry point; refuses to run without exact confirmation and count."""
    parser = argparse.ArgumentParser(
        description="Delete the Hue Foods Qdrant collection after user approval."
    )
    parser.add_argument(
        "--confirmation",
        required=True,
        help="exact confirmation string, e.g. DELETE <collection_name>",
    )
    parser.add_argument(
        "--expected-count",
        type=int,
        required=True,
        help="exact point count the collection must have",
    )
    args = parser.parse_args(argv)
    settings = load_settings()
    name = reset_collection(
        client_from_settings(settings),
        settings,
        expected_count=args.expected_count,
        confirmation=args.confirmation,
    )
    print(f"collection {name} deleted")


if __name__ == "__main__":
    main()
