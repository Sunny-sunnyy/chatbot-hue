"""Separate destructive reset command with exact-target guards."""
import argparse

from core.settings_loader import load_settings
from vectorstore.qdrant import client_from_settings


def reset_collection(client, settings, *, collection_name, confirmation):
    """Delete the exact specified collection after confirmation passes.

    Never recreates the collection; the next ingestion run owns creation.
    """
    if confirmation != f"DELETE {collection_name}":
        raise ValueError(f"confirmation mismatch; expected 'DELETE {collection_name}'")
    if not client.collection_exists(collection_name):
        raise ValueError(f"collection {collection_name} does not exist; nothing to reset")
    count = client.count(collection_name, exact=True).count
    print(f"collection {collection_name} currently has {count} points")
    client.delete_collection(collection_name, timeout=settings["vector_database"]["timeout"])
    if client.collection_exists(collection_name):
        raise RuntimeError(f"collection {collection_name} still exists after delete")
    return collection_name, count


def main(argv=None):
    """CLI entry point; requires exact collection and confirmation string."""
    parser = argparse.ArgumentParser(
        description="Delete a specified Qdrant collection after user approval."
    )
    parser.add_argument(
        "--collection",
        required=True,
        help="exact collection name to delete",
    )
    parser.add_argument(
        "--confirm",
        required=True,
        help="exact confirmation string, e.g. DELETE <collection_name>",
    )
    args = parser.parse_args(argv)
    settings = load_settings()
    name, count = reset_collection(
        client_from_settings(settings),
        settings,
        collection_name=args.collection,
        confirmation=args.confirm,
    )
    print(f"collection {name} ({count} points) deleted")


if __name__ == "__main__":
    main()
