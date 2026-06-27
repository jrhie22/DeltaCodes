def compute_diff(old: dict, new: dict) -> dict:
    """
    Pure deterministic diff — no AI.
    Compares two dicts of {code: fields}.
    """
    added = {k: new[k] for k in new if k not in old}
    deleted = {k: old[k] for k in old if k not in new}
    changed = {}

    for k in old:
        if k in new and old[k] != new[k]:
            changed[k] = {"old": old[k], "new": new[k]}

    return {
        "added": added,
        "deleted": deleted,
        "changed": changed,
        "stats": {
            "added_count": len(added),
            "deleted_count": len(deleted),
            "changed_count": len(changed),
        }
    }